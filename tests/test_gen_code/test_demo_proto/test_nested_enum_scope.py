"""Tests that nested IntEnums referenced by sibling nested models are injected inside those models."""

import pytest

from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_code
from protobuf_to_pydantic.gen_model import clear_create_model_cache


gtfs_realtime_pb2 = pytest.importorskip(
    "google.transit.gtfs_realtime_pb2",
    reason="gtfs-realtime-bindings not installed",
)


class TestNestedEnumScope:
    @staticmethod
    def _model_output(msg: object) -> str:
        clear_create_model_cache()
        return pydantic_model_to_py_code(msg_to_pydantic_model(msg, parse_msg_desc_method="ignore"))

    def test_sibling_enum_emitted_inside_nested_model(self) -> None:
        """OccupancyStatus must be defined inside CarriageDetails before the field that uses it."""
        code = self._model_output(gtfs_realtime_pb2.VehiclePosition)

        carriage_start = code.find("class CarriageDetails(BaseModel):")
        assert carriage_start != -1, "CarriageDetails not found in output"

        # find OccupancyStatus definition inside CarriageDetails
        occ_def_inside = code.find("class OccupancyStatus(IntEnum):", carriage_start)
        assert occ_def_inside != -1, "OccupancyStatus not defined inside CarriageDetails"

        # find the field that references OccupancyStatus
        field_ref = code.find("occupancy_status: OccupancyStatus", carriage_start)
        assert field_ref != -1, "occupancy_status field not found inside CarriageDetails"

        # the definition must come before the field reference
        assert occ_def_inside < field_ref, (
            "OccupancyStatus must be defined before occupancy_status field inside CarriageDetails"
        )

    def test_sibling_enum_still_emitted_at_parent_level(self) -> None:
        """OccupancyStatus must also remain at the VehiclePosition level for VehiclePosition's own fields."""
        code = self._model_output(gtfs_realtime_pb2.VehiclePosition)

        vp_start = code.find("class VehiclePosition(BaseModel):")
        assert vp_start != -1, "VehiclePosition not found in output"

        # find OccupancyStatus at VehiclePosition body level (indented 4 spaces inside VehiclePosition)
        # look for the definition after VehiclePosition starts but outside CarriageDetails
        carriage_start = code.find("class CarriageDetails(BaseModel):", vp_start)
        carriage_end = code.find("\n    class ", carriage_start + 1)
        if carriage_end == -1:
            # CarriageDetails is the last nested class; find where parent fields start
            carriage_end = code.find("\n    model_config", carriage_start)

        occ_at_parent = code.find("class OccupancyStatus(IntEnum):", carriage_end)
        assert occ_at_parent != -1, "OccupancyStatus not found at VehiclePosition level after CarriageDetails"

    def test_generated_code_is_ruff_clean(self) -> None:
        """Generated FeedMessage code must pass ruff with no F821 errors."""
        import subprocess

        clear_create_model_cache()
        code = pydantic_model_to_py_code(
            msg_to_pydantic_model(gtfs_realtime_pb2.FeedMessage, parse_msg_desc_method="ignore")
        )
        result = subprocess.run(
            ["ruff", "check", "--select", "F821", "-"],
            input=code.encode(),
            capture_output=True,
        )
        assert result.returncode == 0, f"ruff reported F821 errors:\n{result.stdout.decode()}"
