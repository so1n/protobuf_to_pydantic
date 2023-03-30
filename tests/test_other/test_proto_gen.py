import filecmp
import sys

project_path: str = ""

for path in set(sys.path):
    if path.endswith("protobuf_to_pydantic"):
        project_path = path
class TestProtoGen:
    """Check whether the PB file in pkg is consistent with the PB file in the example"""
    def test_p2p_validate_proto(self) -> None:
        assert filecmp.cmp(
            project_path + "/example/example_proto/common/p2p_validate.proto",
            project_path + "/protos/p2p_validate.proto",
        )

    def test_validate_proto(self) -> None:
        assert filecmp.cmp(
            project_path + "/example/example_proto/common/validate.proto",
            project_path + "/protos/validate.proto",
        )
