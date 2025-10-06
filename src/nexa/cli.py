import uvicorn
from nexa.main import app

def dev_server() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)