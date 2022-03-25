from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, FileResponse
from incoming_messages import router

app = FastAPI()

app.include_router(router)




@app.get("/", response_class=HTMLResponse)
async def get():
    return FileResponse("main.html")


@app.websocket("/ws")
@app.get("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        request_message = {

            'id': data['messageId'],
            'body': data['body']

        }
        await websocket.send_json(request_message)

