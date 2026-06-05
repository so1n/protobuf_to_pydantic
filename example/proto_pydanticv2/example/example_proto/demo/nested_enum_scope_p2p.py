# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 4.24.4
# Pydantic Version: 2.5.3
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, ConfigDict, Field


class VehiclePosition(BaseModel):
    """
    Reproduces sibling nested enum references used by nested messages.
    """

    class CarriageDetails(BaseModel):
        model_config = ConfigDict(validate_default=True)
        id: str = Field(default="")
        occupancy_status: "VehiclePosition.OccupancyStatus" = Field(default=0)

    class OccupancyStatus(IntEnum):
        EMPTY = 0
        MANY_SEATS_AVAILABLE = 1
        FEW_SEATS_AVAILABLE = 2

    model_config = ConfigDict(validate_default=True)
    occupancy_status: "VehiclePosition.OccupancyStatus" = Field(default=0)
    multi_carriage_details: typing.List["VehiclePosition.CarriageDetails"] = Field(default_factory=list)


class FeedMessage(BaseModel):
    vehicle: VehiclePosition = Field(default_factory=VehiclePosition)
