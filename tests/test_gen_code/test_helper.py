"""Helper classes and utilities for test_gen_code tests."""

from protobuf_to_pydantic.gen_code import P2C


class P2CNoHeader(P2C):
    """P2C subclass that excludes headers and imports for test comparisons."""
    
    head_content = ""  # Disable header for tests
    
    @property
    def content(self) -> str:
        """Override to exclude imports for test comparison"""
        # Only return the model definitions, skip imports
        if self._content_deque:
            _content_set = set()
            content_str = ""
            for content in self._content_deque:
                if content in _content_set:
                    continue
                _content_set.add(content)
                content_str += f"\n{content}"
            return self.format_content(content_str + self.tail_content)
        return self.format_content(self.tail_content)