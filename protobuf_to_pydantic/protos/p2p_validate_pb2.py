from google.protobuf import __version__


if __version__ > "4.0.0":
    from protobuf_to_pydantic.protos.protos.p2p_validate_pb2 import * # isort:skip
else:
    from protobuf_to_pydantic.protos.old.protos.p2p_validate_pb2 import * # type: ignore[no-redef]  # isort:skip
