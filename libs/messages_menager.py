import json
import os
from loguru import logger

chats_dir_path=os.path.join(os.getcwd(), "chats")

if not os.path.isdir(chats_dir_path):
    os.mkdir(chats_dir_path)
    logger.warning("директория chats не была найдена и была создана")

def get_message(chat_id:int)->dict:
    """получкение содержимого чата 

    Args:
        chat_id (int): ID чата

    Returns:
        _dict_: отправка всего содержимого чата 
        _str_: путь до файла
    """
    for fn in os.listdir(chats_dir_path):
        if int(fn.split('.', -1)[0].replace('chat_','')) == chat_id:
            file = os.path.join(os.getcwd(), "chats", f"chat_{chat_id}.json")
            with open(file, 'r') as f:
                data=json.load(f)
    return data, file

def creat_message(chat_id:int, user:str, message:str, reply_to:int, time:float):
    """отправление(создание) сообщения в чат 

    Args:
        chat_id (int): _description_
        user (str): _description_
        message (str): _description_
        reply_to (int): _description_
        time (float): _description_
    """
    
    old_chat, chat_file=get_message(chat_id)
    if old_chat:
        mid = str(max(int(k) for k in old_chat.keys()) + 1)
    else:
        mid = "1"

    old_chat[mid] = {"user":user, "message":message, "time":time, "reply_to":reply_to}
    
    new_data=json.dumps(old_chat)
    
    with open(chat_file, 'w') as f:
        f.write(new_data)
        
    
    
    
    