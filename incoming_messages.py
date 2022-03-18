from fastapi import APIRouter, Request

from messages import Message

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

data = []

message = Message(
    id=1,
    text="kdvnkdokfebe",
)

data.append(message)


@router.get("/{id}")
async def sms(id: int):
    for message in data:
        if message.id == id:
            return message


@router.post("/{id}")
async def add_text(message: Message):
    message.id = data[-1].id + 1
    data.append(message)
    return data


@router.put("/{id}")
async def update_text(id: int, message: Message):
    for all_message in data:
        if all_message.id == id:
            all_message.text = message.text
            return all_message


@router.delete("/{id}")
async def del_text(id: int):
    for message in data:
        if message.id == id:
            data.remove(message)
