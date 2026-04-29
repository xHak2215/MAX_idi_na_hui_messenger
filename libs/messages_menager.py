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

def creat_message(chat_id:int, user:str, message:str, reply_to:int, time:float)->dict:
    """отправление(создание) сообщения в чат 

    Args:
        chat_id (int): Chat ID
        user (str): имя пользователя
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

    old_chat[mid] = {"user":user, "message":message, "time":time, "reply_to":reply_to}
    
    new_data = json.dumps(old_chat)
    
    with open(chat_file, 'w') as f:
        f.write(new_data)

    return {"is_ok": True, "error_code":None, "detalis":None, "data": None}
        
    
    
    
    