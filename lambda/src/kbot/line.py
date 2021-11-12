import os
from typing import List, Dict
from linebot import LineBotApi, WebhookHandler
from linebot.models import SendMessage, MessageEvent, TextMessage, PostbackEvent
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from reply_message import ReplyMessage
from command import Command

# Line Messaging API リファレンス
# https://developers.line.biz/ja/reference/messaging-api/


class Line:
    def __init__(self) -> None:
        channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
        self._line_bot_api = LineBotApi(channel_access_token)
        channel_secret = os.environ["LINE_CHANNEL_SECRET"]
        self._handler = WebhookHandler(channel_secret)

        # id = os.environ["LINE_SEND_ID_1"]
        id: str = os.environ["LINE_SEND_GROUP_ID_1"]
        self._send_ids: List[str] = [id]

    def message_handler(self, event, context):
        # for debug
        # print("event object: {}".format(event))
        # self._push_message("event object: {}".format(event))

        # LINEの仕様変更で、X-Line-Signature → x-line-signature になった
        # 今後もkey名が小文字になる可能性があるということなので
        # 区別しないように修正
        signature = get_hash_value(event["headers"], "X-Line-Signature")
        body = event["body"]
        ok_json = {"isBase64Encoded": False, "statusCode": 200, "headers": {}, "body": ""}
        error_json = {"isBase64Encoded": False, "statusCode": 403, "headers": {}, "body": "Error"}

        @self._handler.add(MessageEvent, message=TextMessage)
        def message(line_event):
            text = line_event.message.text
            self._reply_message(line_event, text)

        @self._handler.add(PostbackEvent)
        def message_handle(line_event):
            data = line_event.postback.data
            is_done = Command.run(data)
            if not is_done:
                self._reply_message(line_event, data)

        try:
            self._handler.handle(body, signature)
        except LineBotApiError as e:
            print("got exception from LINE Messaging API: {}\n".format(e.message))
            for m in e.error.details:
                print("  {}: {}".format(m.property, m.message))
            return error_json
        except InvalidSignatureError as e:
            print("got exception: {}".format(e.message))
            return error_json

        return ok_json

    def _push_message(self, message: SendMessage) -> None:
        for id in self._send_ids:
            self._line_bot_api.push_message(id, message)

    def _reply_message(self, line_event, text: str) -> None:
        reply_message = ReplyMessage.make(text)
        if reply_message is not None:
            self._line_bot_api.reply_message(line_event.reply_token, reply_message)


def get_hash_value(hash: Dict, key: str):
    try:
        return hash[key]
    except KeyError:
        return hash[key.lower()]
