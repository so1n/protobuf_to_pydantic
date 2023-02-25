#!/usr/bin/env python
import logging

from protobuf_to_pydantic.plugin.code_gen import CodeGen

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        CodeGen()
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
