from protobuf_to_pydantic.gen_code import P2C


class P2CTest(P2C):
    def format_content(self, content_str: str) -> str:
        try:
            import isort  # type: ignore
        except ImportError:
            pass
        else:
            content_str = isort.code(content_str)

        try:
            import autoflake  # type: ignore
        except ImportError:
            pass
        else:
            content_str = autoflake.fix_code(content_str)

        try:
            from yapf.yapflib.yapf_api import FormatCode  # type: ignore
        except ImportError:
            pass
        else:
            content_str, _ = FormatCode(content_str)
        return content_str
