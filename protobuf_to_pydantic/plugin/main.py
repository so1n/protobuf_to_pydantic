#!/usr/bin/env python
import logging

from protobuf_to_pydantic.cli import p2p_cli
from protobuf_to_pydantic.plugin.code_gen import CodeGen
from protobuf_to_pydantic.plugin.config import ConfigModel

logger = logging.getLogger(__name__)


def main() -> None:
    p2p_cli()
    try:
        CodeGen(ConfigModel)
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
