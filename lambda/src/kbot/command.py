import os
from lambda_invoker import invoke


class Command:
    @staticmethod
    def run(command: str) -> bool:
        if command == "図書館":
            return Command._check_library_rental_books_handler()
        elif command == "延滞":
            return Command._check_library_expire_books_handler()
        elif command == "予約":
            return Command._check_library_reserve_books_handler()
        elif command == "届いた本":
            return Command._check_library_prepare_books_handler()
        else:
            return False

    @staticmethod
    def _check_library_rental_books_handler() -> bool:
        invoke(
            os.environ["LIBRARY_CHECK_RENTAL_FUNCTION_ARN"],
            {"is_reply": True},
        )
        return True

    @staticmethod
    def _check_library_expire_books_handler() -> bool:
        invoke(
            os.environ["LIBRARY_CHECK_EXPIRE_FUNCTION_ARN"],
            {"is_reply": True},
        )
        return True

    @staticmethod
    def _check_library_reserve_books_handler() -> bool:
        invoke(
            os.environ["LIBRARY_CHECK_RESERVE_FUNCTION_ARN"],
            {"is_reply": True},
        )
        return True

    @staticmethod
    def _check_library_prepare_books_handler() -> bool:
        invoke(
            os.environ["LIBRARY_CHECK_PREPARE_FUNCTION_ARN"],
            {"is_reply": True},
        )
        return True
