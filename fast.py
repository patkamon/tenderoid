from fastapi import FastAPI
from create_bio import create_bio
import random
from dotenv import load_dotenv
import os
import requests
import write
import read
import string
import csv
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI()


# allow cors
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# uvicorn fast:app --host localhost --port 8000

load_dotenv()
secret_key = os.getenv("GETIMG_API")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List


class ChatManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create-bio")
def create_profile():
    random_seed = random.randint(1, 1_000_000)
    bio = create_bio(random_seed=random_seed)

    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    images = {}
    # loop random from 2-5
    rand = random.randint(2, 5)
    for i in range(rand):
        json = get_img(bio)
        img = write.write_img(json, filename, i+1)
        images['img'+str(i+1)] = img

    for i in range(rand, 5):
        images['img'+str(i+1)] = None

    new_row = write.new_row_format(bio=bio, **images)
    res = write.write_bio(new_row)
    return res

# TODO: add pagination
@app.get("/all-bio")
def all_bio():
    with open("bio.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

@app.get("/get-bio/{item_id}")
def get_bio(item_id: int):
    with open("bio.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data[item_id-1]


class Message(BaseModel):
    message: str
    id: int


@app.post("/chat")
def chat(message: Message):
    from langchain_ollama import ChatOllama
    llm = ChatOllama(
        model="llama3.2",
        temperature=0.8,
    )

    START_BEHAVIOR =  "Start with short, casual, and friendly responses,"
    LATER_BEHAVIOR = "Gradually become more chatty as the interaction progresses."

    def create_chat(bio):
        return [
            (
            "system",
            "Act as a girl chatting on a dating app."+ 
            f"{bio}"+
            START_BEHAVIOR+
            LATER_BEHAVIOR+
            "Use emojis to add personality but do not invite to meet in person."
            "If you receive a weird, aggressive, or undesirable message, respond with 'BLOCK' to indicate blocking the user."
            ),
        ]
    bio = get_bio(message.id)['bio']

    chat = create_chat(bio) 
    #check in db if chat already exist
    old = read.read_chat(message.id)
    for o in old:
        if o['isUser'] == 'True':
            chat.append(("human", o['msg']))
        else:
            chat.append(("assistant", o['msg']))

    ask = message.message
    chat.append(("human", ask))
    write.write_chat({"id":message.id, "isUser": True, "msg": ask, "time": datetime.now()})
    msg = llm.invoke(chat)
    print(msg.content)
    chat.append(("assistant", msg.content))
    print("========================================")
    #store chat in db
    write.write_chat({"id":message.id,"isUser": False, "msg": msg.content, "time": datetime.now()})
    return msg.content

@app.get("/chat/{item_id}")
def get_chat(item_id: int):
    return read.read_chat(item_id)


chat_manager = ChatManager()


def get_img(prompt):
    url = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }
    body={
        "prompt": prompt,
        "model": "dark-sushi-mix-v2-25"
    }
    response = requests.post(url, headers=headers, json=body)
    return response.text


# retrieve chat from db and banned status
@app.get("/all-chat")
def all_chat():
    res = list()
    ids = read.read_all_chat()
    for i in ids:
        res.append({**get_bio(int(i['id'])), 'msg': i['msg'], 'isUser': i['isUser']})
    return res


@app.websocket("/ws/{item_id}")
async def websocket_endpoint(websocket: WebSocket, item_id: int):
    await chat_manager.connect(websocket)
    
    # Initial message upon connection
    # await websocket.send_text(json.dumps({"message": f"Connected to item {item_id}", "item_id": item_id}))
    
    for old_message in read.read_chat(item_id):
        await websocket.send_text(json.dumps(old_message))

    try:
        while True:
            # Receive the message, expect it to be a JSON string
            msg = await websocket.receive_text()
            print(f"Received message from item {item_id}: {msg}")

            # Process the received message (e.g., interacting with LangChain or your database)
            if msg:
             

                # await chat_manager.broadcast({"isUser": True, "msg": msg, "time": 'now'})
                # Here you would process the chat message and generate a response
                # For example, interacting with LangChain (the part you already wrote)
                await chat_for_websocket(Message(message=msg, id=item_id))
                
                # response = {"id": item_id, "isUser": False, "msg": f"Reply to {message}", "time": str(datetime.now())}
                # await chat_manager.broadcast(response, item_id)

                # Store the chat in your database or perform any other necessary operations
                # Write your DB storing logic here

    except WebSocketDisconnect:
        # When the WebSocket disconnects, remove the connection from the manager
        await chat_manager.disconnect(websocket)
        print(f"Client {item_id} disconnected")

    except Exception as e:
        # Catch unexpected errors and print the error message
        print(f"Error processing message for item {item_id}: {e}")
        await chat_manager.disconnect(websocket)




async def chat_for_websocket(message: Message):
    from langchain_ollama import ChatOllama
    llm = ChatOllama(
        model="llama3.2",
        temperature=0.8,
    )

    START_BEHAVIOR =  "Start with short, casual, and friendly responses,"
    LATER_BEHAVIOR = "Gradually become more chatty as the interaction progresses."

    def create_chat(bio):
        return [
            (
            "system",
            "Act as a girl chatting on a dating app."+ 
            f"{bio}"+
            START_BEHAVIOR+
            LATER_BEHAVIOR+
            "Use emojis to add personality but do not invite to meet in person."
            "If you receive a weird, aggressive, or undesirable message, respond with 'BLOCK' to indicate blocking the user."
            ),
        ]
    bio = get_bio(message.id)['bio']

    chat = create_chat(bio) 
    #check in db if chat already exist
    old = read.read_chat(message.id)
    for o in old:
        if o['isUser'] == 'True':
            chat.append(("human", o['msg']))
        else:
            chat.append(("assistant", o['msg']))

    ask = message.message
    chat.append(("human", ask))
    write.write_chat({"id":message.id, "isUser": True, "msg": ask, "time": datetime.now()})
    msg = llm.invoke(chat)
    print(msg.content)
    chat.append(("assistant", msg.content))
    print("========================================")
    #store chat in db
    write.write_chat({"id":message.id,"isUser": False, "msg": msg.content, "time": datetime.now()})
    await chat_manager.broadcast({"id":message.id,"isUser": False, "msg": msg.content, "time": 'now'})
    return msg.content


