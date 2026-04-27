from fastapi import FastAPI, Query, UploadFile, File
from fastapi.responses import StreamingResponse

import socket
from typing import List
import os
import json
import time

from data_bese import creat_new_user, get_data_user, creat_chat, get_data_chat, verification_token
from libs.gmail_send import send_mail
from libs.zip_images import zip_images
from libs.token_creat import token
from libs.messages_menager import get_message, creat_message

app = FastAPI()

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def sig_in_user(user_name:str, email:str):# на потом
    key=123
    html ='''
    <html>
    <head>

    <style>
    body {
        font-family: Arial; 
        background: #31241d; 
    } 

    .key {
    padding: 10px;
    display: inline-block;
    border: 3px solid #635e5c;

    text-align: center;
    font-style: italic;
    font-size: 25;
    }

    .centr {
        text-align: center;
    }
    </style>

    </head>
    <body>
    <div class="centr"><h2>привет {} !</h2></div>

    <h3>вот ваш код для подтверждения адреса электронной почты:</h3>

    <div class="key">{}</div>

    </body>
    </html>
    '''.format(user_name, key)
    
    send_mail(html, email)
    
def streamfile(path, chunk_size=1024*1024):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

@app.get("/")
def ping():
    return 200

@app.get("/data_bese/new_user")
def new_user(password:str, login:str, name:str, email:str):
    user_token = token({"login":login, "password":password, "name":name})
    data = creat_new_user(login, password, name, user_token)
    return data

@app.get("/data_bese/get_data_user")
def data_user(login:str):
    data = get_data_user(login)
    return data

@app.get("/media/get")
def get_media(id:int):
    path=os.path.join(os.getcwd(), "media")
    file_list=os.listdir(path)
    for fn in file_list:
        if int(fn.split('.', -1)[0]) == id:
            #отправка
            return StreamingResponse(streamfile(os.path.join(path, fn)), media_type="application/octet-stream")    
        
    return {"is_ok": False, "error_code":404, "detalis": f"файл не найден", "data": None}

@app.post("/media/uploadfiles")
async def uploadfiles(upload_file: UploadFile = File(...)):
    with open(os.path.join(os.getcwd(), "media","media_config.json"),'r') as f:
        conf=json.load(f)
        
    if conf["media_id"] or conf["media_id"] == 0:id=int(conf["media_id"])+1
    else:id=0
        
    with open(os.path.join(os.getcwd(), "media","media_config.json"), 'w') as f:
        json.dump({"media_id":id}, f)
        
    with open(os.path.join(os.getcwd(), "media", f"{id}{os.path.splitext(upload_file.filename)[1]}"), "wb") as f_d:
        bufer=b''
        while True:
            chunk = await upload_file.read(1024)
            if not chunk:
                break
            bufer+=chunk
        f_d.write(zip_images(bufer))
    
    return {"is_ok": True, "error_code":None, "detalis":None, "data": None}

@app.get("/chat/creat_chat")
def chat(name:str, avatar:int, private:bool, about:str|None, user_list:List[str] = Query(...)): # List[str] = Query(...) для приема сложных типов данных
    data = creat_chat(name, avatar, user_list, private, about)
    return data

@app.get("/chat/get_chat")
def get_chat(login:str, chat_id:int):
    data=get_data_chat(login, chat_id)
    return data

@app.get("/chat/chat_message")
def caht_get_message(login:str, chat_id:int, token:str):
    ver_data = verification_token(login, token)
    if ver_data["is_ok"] and ver_data["data"]:
        data = get_data_chat(login, chat_id)
        
        if data['is_ok']:
            if login in data['data']["users_list"]:
                data = get_message(chat_id)[0]
                return {"is_ok": True, "error_code":None, "detalis":None, "data": data}
            else:return {"is_ok": False, "error_code":403, "detalis":"нет доступа, user не состоит в чате", "data": None}
        else:return data
    else:return {"is_ok": False, "error_code":403, "detalis":"нет доступа, пользователь не подтверждён", "data": None}
    
@app.get("/chat/send_message")
def send_message(chat_id:int, message:str, reply_to:int, login:str, token:str):
    ver_data = verification_token(login, token)
    if ver_data["is_ok"] and ver_data["data"]:
        
        data=get_data_chat(login, chat_id)
        if data['is_ok']:
            if login in data['data']["users_list"]:
                if reply_to>0:
                    data = get_message(chat_id)[0]
                    message = data.get(str(reply_to))
                else:
                    message = True
                if message:
                    creat_message(chat_id, login, message, reply_to, time.time())
                else:
                    return {"is_ok": False, "error_code":404, "detalis":"нет сообщения с таким ID с этом чате", "data": None}
                return {"is_ok": True, "error_code":None, "detalis":None, "data":{"chat_id":chat_id, "name":login, "message":message, "reply_to":reply_to, "time":time.time()} }
            
            else:return {"is_ok": False, "error_code":403, "detalis":"нет доступа, user не состоит в чате", "data": None}
        else:return data 
    
@app.get("/chat/get_message")
def get_message_id(login:str, chat_id:int, token:str, message_id:int):
    ver_data = verification_token(login, token)
    if ver_data["is_ok"] and ver_data["data"]:
         
        data = get_data_chat(login, chat_id)
        if data['is_ok']:
            if login in data['data']["users_list"]:
                data = get_message(chat_id)[0]
                message = data.get(str(message_id))
                if message:
                    return {"is_ok": True, "error_code":None, "detalis":None, "data":message}
                else:return {"is_ok": False, "error_code":404, "detalis":"сообщение не найдено", "data": None}
            else:return {"is_ok": False, "error_code":403, "detalis":"нет доступа, user не состоит в чате", "data": None}
        else:return data
            
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=get_local_ip(), port=8800)  # Запуск FastAPI