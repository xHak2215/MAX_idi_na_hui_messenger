import json
import os
from loguru import logger

chats_dir_path=os.path.join(os.getcwd(), "chats")

if not os.path.isdir(chats_dir_path):
    os.mkdir(chats_dir_path)
    logger.warning("директория chats не была найдена и была создана")

def get_messages(chat_id:int)->tuple[dict, str] | None:
    """получкение содержимого чата 

    Args:
        chat_id (int): ID чата

    Returns:
        _dict_: отправка всего содержимого чата 
        _str_: путь до файла
    """
    for fn in os.listdir(chats_dir_path):
        if len(fn) > 0 and int(fn.split('.', -1)[0].replace('chat_','')) == chat_id:
            file = os.path.join(os.getcwd(), "chats", f"chat_{chat_id}.json")
            if os.path.isfile(file):
                with open(file, 'r') as f:
                    data = json.load(f)
            else:
                with open(file, 'w') as f:
                    f.write(r"{}")
                data = {}
        else:
            return None

        return data, file 

def creat_message(chat_id:int, login:str, message:str, reply_to:int, time:float)->dict:
    """отправление(создание) сообщения в чат 

    Args:
        chat_id (int): Chat ID
        login (str): логин пользователя
        message (str): сообщение
        reply_to (int): ID сообщения на котрое являеться ответом отпровляемое. если сообщение не должно ни на что отвечать передайте -1
        time (float): время отправки сообщения (в формате UNIX) 
    """
    chat_inf = get_messages(chat_id)
    if chat_inf:
        old_chat = chat_inf[0]
        mid = str(max(int(k) for k in old_chat.keys()) + 1)
    else:
        mid = "1"
        old_chat = {}

    chat_file = os.path.join(os.getcwd(), "chats", f"chat_{chat_id}.json")

    old_chat[mid] = {"login":login, "message":message, "time":time, "reply_to":reply_to, "edit":False}
    
    new_data = json.dumps(old_chat)
    
    with open(chat_file, 'w') as f:
        f.write(new_data)

    return {"is_ok": True, "error_code":None, "detalis":None, "data": None}

def edit_message(chat_id:int, login:str, message:str, message_id:int, time:float)->dict:
    """отправление(создание) сообщения в чат 

    Args:
        chat_id (int): Chat ID
        login (str): логин пользователя
        message (str): сообщение
        reply_to (int): ID сообщения на котрое являеться ответом отпровляемое. если сообщение не должно ни на что отвечать передайте -1
        time (float): время отправки сообщения (в формате UNIX) 
    """
    m_data = get_messages(chat_id)

    if m_data:
        if m_data[0].get(message_id):
            if m_data[0]["login"] == login:
                chat_file = os.path.join(os.getcwd(), "chats", f"chat_{chat_id}.json")
                m_data[0][message_id] = {"login":login, "message":message, "time":time, "reply_to":m_data[0][message_id]["reply_to"], "edit_time":time}
                
                new_data = json.dumps(m_data[0])
            
                with open(chat_file, 'w') as f:
                    f.write(new_data)
            else:
                return {"is_ok": False, "error_code":403, "detalis":"нет доступа, user не состоит в чате", "data": None}
        else:
            return {"is_ok": False, "error_code":404, "detalis":"нет сообщения с таким ID с этом чате", "data": None}
    else:
        return {"is_ok": False, "error_code":404, "detalis":"такого чата не существует", "data": None}

    return {"is_ok": True, "error_code":None, "detalis":None, "data": None}
        
    
    
    
    