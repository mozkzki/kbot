from lambda_invoker import invoke


class TestLambdaInvoker:
    def test_invoke(self):
        invoke(
            # TODO: dev版を呼ぶようにしたい
            "arn:aws:lambda:ap-northeast-1:045254874683:function:library-checker-check-rental",
            {"param1": 1, "param2": 2, "param3": 3},
        )
