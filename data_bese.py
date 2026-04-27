import sqlite3
import traceback
import json

from loguru import logger


def update_user(login:str, password:str, relust:dict):
    """**update data bese**
    
    Args:
        login (_str_): логин пользователя
        password (_str_): пароль пользователя
        relust (dict): словарь где ключ это название столбца а содержимое данные

    Returns:
        None:при ошибке
    """
    # Создаем подключение к базе данных
    connection = sqlite3.connect('data_base.db', timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Формируем запрос для обновления
    query = "UPDATE Users SET "
    params = []
    updates = []
    
    if relust is not None:
        for key in list(relust.keys()):
            updates.append(key+"= ?")
            params.append(str(relust[key]))
    
    # Проверяем, были ли добавлены параметры
    if not updates:
        connection.close()
        #logger.warning("update_user Нет параметров для обновления.")
        return None
    
    query += ", ".join(updates)
    query += " WHERE login = ? AND password = ? "
    params.append(login)
    params.append(password)
    
    try:
        cursor.execute(query, params)
        connection.commit()
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return None
    finally:
        connection.close()
         
def init_users():
    # Создаем подключение к базе данных
    connection = sqlite3.connect('data_base.db',timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Создаем таблицу (если она еще не существует)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        about TEXT,
        avatar INTEGER,
        token TEXT NOT NULL
        
    )
    ''')
    
    # Создаем индекс (если он еще не существует)
    cursor.execute('CREATE INDEX IF NOT EXISTS user_id_index ON Users (id)')
    return connection, cursor

def init_chat():
    # Создаем подключение к базе данных
    connection = sqlite3.connect('data_base.db',timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Создаем таблицу (если она еще не существует)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Chats (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        avatar INTEGER,
        about TEXT,
        users_list LIST,
        private BOOL NOT NULL
    )
    ''')
    
    # Создаем индекс (если он еще не существует)
    cursor.execute('CREATE INDEX IF NOT EXISTS user_id_index ON Users (id)')
    return connection, cursor
        
def creat_new_user(login:str, password:str, name:str, token:str)-> dict: 
    try:
        connection, cursor = init_users()
        
        # Проверяем, существует ли пользователь с данными login и password
        cursor.execute('SELECT * FROM Users WHERE login = ?  AND name = ?', (login, name))
        result = cursor.fetchone()

        if result is  None:
            cursor.execute('INSERT INTO Users (login, password, name, token) VALUES (?, ?, ?, ?)', (login, password, name, token))
            connection.commit()
            connection.close()
            return {"is_ok": True, "error_code":None, "detalis": None, "data": {"login":login, "password":password, "name":name, "token":token}}
        else:
            connection.commit()
            connection.close()
            return {"is_ok": False, "error_code":403, "detalis":"такой пользователь уже существует", "data":None}

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "detalis": f"server error: {e}", "data": None}
    finally:
        # Закрываем соединение
        connection.close()
        
def get_data_user(login:str)-> dict: 
    try:
        connection, cursor = init_users()
        
        # Проверяем, существует ли пользователь с данными login и name
        cursor.execute('SELECT * FROM Users WHERE login = ?', (login, ))
        result = cursor.fetchone()

        if result is not None:
            login=result[1]
            password=result[2]
            name=result[3]
            connection.commit()
            connection.close()
            return {"is_ok": True, "error_code":None, "detalis": None, "data": {"login":login, "password":password, "name":name}}
 
        else:
            connection.commit()
            connection.close()
            return {"is_ok": False, "error_code":404, "detalis": "пользователь не найден", "data": None}

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "detalis": f"server error: {e}", "data": None}  
    finally:
        # Закрываем соединение
        connection.close()
        
def creat_chat(name:str, avatar:int, users_list:list, private:bool, about=None)-> dict:
    try:
        connection, cursor = init_chat()
        
        # Проверяем, существует ли чат с таким именем и создаем id
        cursor.execute("SELECT * FROM Chats ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            chat_id=row[0]+1
        else:
            chat_id=1
        
        cursor.execute('SELECT * FROM Chats WHERE name = ? ', (name, ))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO Chats (chat_id, name, avatar, about, users_list, private) VALUES (?, ?, ?, ?, ?, ?)', (chat_id, name, avatar, about, json.dumps(users_list), private))
            connection.commit()
            connection.close()
            return {"is_ok": True, "error_code":None, "detalis": None, "data": {"chat_id":chat_id, "name":name, "avatar":avatar, "about":about, "users_list":users_list, "private":private}}
        else:
            return {"is_ok": False, "error_code":403, "detalis": f"чат с таким именем уже существует", "data": None}
        
    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "detalis": f"server error: {e}", "data": None}
    finally:
        # Закрываем соединение
        connection.close()
        
def get_data_chat(user:str, chat_id:int) -> dict:
    try:
        connection, cursor = init_chat()
        
        cursor.execute('SELECT * FROM Chats WHERE chat_id = ? ', (chat_id, ))
        result = cursor.fetchone()
        
        if result is not None:
            name=result[2]
            avatar=result[3]
            about=result[4]
            users_list=result[5]
            private=result[6]
            
            if private:
                if user in json.loads(users_list):
                    return {"is_ok": True, "error_code":None, "detalis": None, "data": {"chat_id":chat_id, "name":name, "avatar":avatar, "about":about, "users_list":users_list, "private":private}}
                else:
                    return {"is_ok": False, "error_code":403, "detalis": f"нет доступа", "data": None}
            else:
                return {"is_ok": True, "error_code":None, "detalis": None, "data": {"chat_id":chat_id, "name":name, "avatar":avatar, "about":about, "users_list":users_list, "private":private}}
        else:
            return {"is_ok": False, "error_code":404, "detalis": f"такого чата не существует", "data": None}
        
    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "detalis": f"server error: {e}", "data": None}
    finally:
        # Закрываем соединение
        connection.close()
        
def verification_token(login:str, token:str)->dict:
    """функция подтверждения токена 

    Args:
        login (str): имя пользователя 
        token (str): токен пользователя 

    Returns:
        dict: шаблонный ответ от БД где `data` это True в случае успеха и False в обратном случите 
    """
    try:
        connection, cursor = init_users()
        
        # Проверяем, существует ли пользователь с данными login и password
        cursor.execute('SELECT * FROM Users WHERE login = ? AND token = ?', (login, token))
        result = cursor.fetchone()

        if result is not None:
            connection.commit()
            connection.close()
            return {"is_ok": True, "error_code":None, "detalis": None, "data": True}
 
        else:
            connection.commit()
            connection.close()
            return {"is_ok": False, "error_code":403, "detalis": f"токен или имя указаны не верно !", "data": False}

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "detalis": f"server error: {e}", "data": None}  
    finally:
        # Закрываем соединение
        connection.close()
    


