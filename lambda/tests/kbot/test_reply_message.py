from reply_message import ReplyMessage


class TestReplyMessage:
    def test_make_1(self):
        ReplyMessage.make("test")

    def test_make_2(self):
        ReplyMessage.make("図書？豊")

    def test_make_3(self):
        ReplyMessage.make("図書館")

    def test_make_4(self):
        ReplyMessage.make("5日で延滞")

    def test_make_5(self):
        ReplyMessage.make("延滞")

    def test_make_6(self):
        ReplyMessage.make("予約？豊")

    def test_make_7(self):
        ReplyMessage.make("予約")

    def test_make_8(self):
        ReplyMessage.make("ほ？")

    def test_make_9(self):
        ReplyMessage.make("本？")

    def test_make_10(self):
        ReplyMessage.make("着？")

    def test_make_11(self):
        ReplyMessage.make("文字")

    def test_make_12(self):
        ReplyMessage.make("コマンド")
