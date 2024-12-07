#!/usr/bin/env python
import logging

from protobuf_to_pydantic.cli import p2p_cli

logger = logging.getLogger(__name__)


def main() -> None:
    p2p_cli(include_executable=False, include_sys_path=False)


if __name__ == "__main__":
    main()
