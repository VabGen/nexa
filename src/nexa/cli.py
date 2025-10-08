import webbrowser

import uvicorn


def dev_server() -> None:
    uvicorn.run(
        "nexa.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )

    # webbrowser.open("http://127.0.0.1:8080")
