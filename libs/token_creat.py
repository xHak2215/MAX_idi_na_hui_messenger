import hashlib
import json
import random
import time

random.seed(time.time())

def token(json_data:dict)->str:
    """создает токен на основе данных пользователя

    Args:
        json_data (dict): данные пользователся а именно `{"login":login, "password":password, "name":name}` словарь

    Returns:
        _str_: уникальный токен 
    """
    # Создание объекта хэширования
    hash_object = hashlib.sha256()

    # Обновление объекта хэширования данными
    hash_object.update(json_data["password"].encode())
    password_hash = hash_object.hexdigest()# Получение хэша в шестнадцатеричном формате
    json_data["password"]=password_hash
    
    hash_object.update(str(round(random.random())).encode())
    random_hash_num=hash_object.hexdigest()
    json_data["random"]=random_hash_num
    
    token_data = json.dumps(json_data)
    
    hash_object.update(token_data.encode())
    token=hash_object.hexdigest()
    
    return token


