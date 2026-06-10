import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "todo_project"
        )
    )
)

from todo_project import app


def test_app_exists():
    assert app is not None


def test_secret_key_exists():
    assert app.config["SECRET_KEY"] is not None