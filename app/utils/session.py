import traceback
from typing import Callable, Any

from app.utils.connection import SessionLocal
from app.utils.terminal import print_to_console


def session_hook(func: Callable) -> object:
    def run(*args, **kwargs):
        global db

        try:
            db = SessionLocal()
            result: Any = func(db, *args, **kwargs)

            return result
        except Exception as exc:
            print_to_console("Error occur in session hook")
            traceback.print_exc()
            raise Exception(exc)

        finally:
            db.close()

    return run
