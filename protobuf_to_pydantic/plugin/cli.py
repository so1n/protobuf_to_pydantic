import sys
from protobuf_to_pydantic.__version__ import __version__

def p2p_cli() -> None:
    if not len(sys.argv) > 1:
        return
    if sys.argv[1] in ("-V", "--version"):
        # Overwrite the version information of mypy-protobuf
        print("protobuf-to-pydantic " + __version__)
    elif sys.argv[1] in ("-I", "--info"):
        try:
            from pydantic import VERSION as pydantic_version
        except ImportError:
            pydantic_version = "Not Install"
        try:
            from grpc import __version__ as grpc_version
        except ImportError:
            grpc_version = "Not Install"
        try:
            from mypy_protobuf.main import __version__ as mypy_protobuf_version
        except ImportError:
            mypy_protobuf_version = "Not Install"
        try:
            from lark import __version__ as lark_version
        except ImportError:
            lark_version = "Not Install"
        try:
            from toml import __version__ as toml_version
        except ImportError:
            toml_version = "Not Install"

        try:
            from black import __version__ as black_version
        except ImportError:
            black_version = "Not Install"
        try:
            from isort import __version__ as isort_version
        except ImportError:
            isort_version = "Not Install"
        try:
            from autoflake import __version__ as autoflake_version
        except ImportError:
            autoflake_version = "Not Install"

        print()
        print()
        print("protobuf-to-pydantic:" + __version__)
        print()
        print("############# dependencies ############## ")
        print("    grpc:            " + grpc_version)
        print("    pydantic:        " + pydantic_version)
        print()
        print("########## Expand dependencies ########## ")
        print("    mypy-protobuf:   " + mypy_protobuf_version)
        print("    lark:            " + lark_version)
        print("    toml:            " + toml_version)
        print()
        print("########## Format dependencies ########## ")
        print("    autoflake:       " + autoflake_version)
        print("    black:           " + black_version)
        print("    isort:           " + isort_version)
        print()
    sys.exit(0)
