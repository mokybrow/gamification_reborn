from uvicorn import run

from .bootstrap import make_app  # noqa


def main() -> None:
    run(
        app='dudesplay_api.main:make_app',
        host='127.0.0.1',
        port=8000,
        factory=True,
        workers=1,
        reload=True,
    )
