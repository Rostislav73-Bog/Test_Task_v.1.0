import starlette
from fastapi import FastAPI,WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
from incoming_messages import data
from incoming_messages import router
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.include_router(router)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Message</title>
    </head>
    <body style="color:#2F4F4F; background-color:#FFF0F5">
        <h1>Messages</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
@app.get("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    index = 0
    while True:
        index += 1
        jsonable_encoder(index)
        data = await websocket.receive_text()
        jsonable_encoder(data)
        print(index, ".", data)
        await websocket.send_json(f"{index}. {data}")
        starlette.websockets.WebSocketDisconnect()


