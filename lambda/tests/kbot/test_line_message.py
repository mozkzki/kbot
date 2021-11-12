import pytest

from line import Line
from line_message import LineMessage


class TestLineMessage:
    @pytest.fixture()
    def line(self):
        line = Line()
        return line

    def test_make_text_message(self, line: Line):
        message = LineMessage.make_text_message("this is test.")
        line._push_message(message)

    def test_make_button_message(self, line: Line):
        BUTTON_MESSAGE_DATA = {
            "title": "Dolphin Free",
            "text": "これは自由なイルカ",
            "image_url": "https://cdn2.picryl.com/photo/2012/05/05/dolphin-free-79340c-1024.jpg",
            "actions": [
                {
                    "type": "postback",
                    "label": "表示",
                    "data": "command:show(dolphin)",
                    "display_text": "イルカを表示して",
                },
                {"type": "url", "label": "YouTubeへ", "url": "https://www.youtube.com/"},
            ],
        }
        message = LineMessage.make_button_message(BUTTON_MESSAGE_DATA)
        line._push_message(message)

    def test_make_carousel_message(self, line: Line):
        CAROUSEL_MESSAGE_DATA = [
            {
                "title": "Dolphin Free",
                "text": "これは自由なイルカ",
                "image_url": "https://cdn2.picryl.com/photo/2012/05/05/dolphin-free-79340c-1024.jpg",  # noqa
                "actions": [
                    {
                        "type": "postback",
                        "label": "表示",
                        "data": "command:show(dolphin)",
                        "display_text": "イルカを表示して",
                    },
                    {"type": "url", "label": "YouTubeへ", "url": "https://www.youtube.com/"},
                ],
            },
            {
                "title": "Free Falcon",
                "text": "これは自由な隼",
                "image_url": "https://cdn.pixabay.com/photo/2017/08/25/23/22/falcon-2681854_960_720.jpg",  # noqa
                "actions": [
                    {
                        "type": "postback",
                        "label": "表示",
                        "data": "command:show(falcon)",
                        "display_text": "隼を表示して",
                    },
                    {"type": "url", "label": "YouTubeへ", "url": "https://www.youtube.com/"},
                ],
            },
        ]
        message = LineMessage.make_carousel_message(CAROUSEL_MESSAGE_DATA)
        line._push_message(message)
