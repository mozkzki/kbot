import pytest
from typing import Dict
from line import Line, get_hash_value
from line_message import LineMessage


class TestLine:
    @pytest.fixture()
    def line(self):
        line = Line()
        return line

    @pytest.mark.parametrize("message", [("これはテストです。"), ("あ" * 1901)])
    def test_push_message_text(self, line: Line, message: str) -> None:
        line._push_message(LineMessage.make_text_message(message))

    def test_get_hash_value(self) -> None:
        expected = "hoge"
        event: Dict = {"headers": {}}
        event["headers"]["x-line-signature"] = expected
        result = get_hash_value(event["headers"], "X-Line-Signature")
        assert result == expected
