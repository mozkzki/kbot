import logging
from typing import List, Dict, Optional
from linebot.models import SendMessage
from line_message import LineMessage
from command import Command


class ReplyMessage:
    @staticmethod
    def make(input_message: str) -> Optional[SendMessage]:
        return ReplyMessage._handle_message(input_message)

    @staticmethod
    def _handle_message(input_message: str) -> Optional[SendMessage]:
        filtered_maps = list(filter(lambda map: map["keyword"] in input_message, HANDLER_MAPS))
        if len(filtered_maps) > 0:
            # 最初の1個を採用
            handler = filtered_maps[0].get("handler", None)
            if handler is None:
                logging.info("handler is None.")
            else:
                return handler(input_message)

        return None
        # return _help_menu_handler(input_message)


def _command_handler(input_message: str) -> None:
    Command.run(input_message)


def _search_book_handler(input_message: str):
    return LineMessage.make_text_message("本の検索")


def _command_text_handler(input_message: str):
    reply_message = """次の言葉に反応します。

──────
図書館
──────
■貸出状況ﾁｪｯｸ
　◎図書館
■期限切れ間近本ﾁｪｯｸ
　◎延滞
■予約状況ﾁｪｯｸ
　◎予約
■届いた本があるかﾁｪｯｸ
　◎届いた本"""
    return LineMessage.make_text_message(reply_message)


def _help_menu_handler(input_message: str) -> SendMessage:
    text = "KBotのヘルプです。"
    return LineMessage.make_button_message(
        {
            "title": "[kbot] ヘルプ",
            "text": text,
            "actions": [
                {
                    "type": "postback",
                    "label": "図書館メニューを表示",
                    "data": "libコマンド",
                    "display_text": "libコマンド",
                },
                {"type": "postback", "label": "反応する文字の確認", "data": "文字", "display_text": "文字"},
            ],
        }
    )


def _library_command_menu_handler(input_message: str) -> SendMessage:
    text = "メニューを選択してください。"
    return LineMessage.make_button_message(
        {
            "title": "[kbot] 図書館メニュー",
            "text": text,
            "actions": [
                {"type": "postback", "label": "貸出状況の確認", "data": "図書館", "display_text": "図書館"},
                {"type": "postback", "label": "延滞本のチェック", "data": "延滞", "display_text": "延滞"},
                {"type": "postback", "label": "予約状況の確認", "data": "予約", "display_text": "予約"},
                {
                    "type": "postback",
                    "label": "届いた予約本のチェック",
                    "data": "届いた本",
                    "display_text": "届いた本",
                },
            ],
        }
    )


HANDLER_MAPS: List[Dict] = [
    {"keyword": "図書館", "handler": _command_handler},
    {"keyword": "延滞", "handler": _command_handler},
    {"keyword": "予約", "handler": _command_handler},
    {"keyword": "届いた本", "handler": _command_handler},
    # {"keyword": "ほ？", "handler": _search_book_handler},
    # {"keyword": "本？", "handler": _search_book_handler},
    # {"keyword": "著？", "handler": _search_book_handler},
    {"keyword": "文字", "handler": _command_text_handler},
    {"keyword": "libコマンド", "handler": _library_command_menu_handler},
    {"keyword": "ヘルプ", "handler": _help_menu_handler},
]
