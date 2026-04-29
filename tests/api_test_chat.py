import requests
import time

timer=time.time()

root_ip="http://127.0.1.1:8800"

tokin = "822093208073f0c4a2818e77d033887dc124871ece76abf07aed4c58ba337277"

relust_a=requests.get(f"{root_ip}/chat/creat_chat",params={
                                                        "name":"чат 1",
                                                        "avatar":0,
                                                        "private":True,
                                                        "about":"test chat",
                                                        "user_list":["user228"]})# запрос на создание чата

relust_b=requests.get(f"{root_ip}/chat/get_chat",params={
                                                        "login":"user228",
                                                        "chat_id":1})# получение информации о чате

relust_с=requests.get(f"{root_ip}/chat/chat_message",params={
                                                    "login":"user228",
                                                    "chat_id":1,
                                                    "token":tokin})# получение содержимого чата

relust_g=requests.get(f"{root_ip}/chat/send_message",params={
                                                    "chat_id":1,
                                                    "message":"hello world",
                                                    "reply_to":-1,
                                                    "login":"user228",
                                                    "token":tokin})# отправка сооббщений

relust_h=requests.get(f"{root_ip}/chat/get_message",params={
                                                    "login":"user228",
                                                    "chat_id":1,
                                                    "token":tokin,
                                                    "message_id":1})

relust_j=requests.get(f"{root_ip}/chat/get_message",params={ # проверка на ошибку об отсуцтвии сообщения
                                                    "login":"user228",
                                                    "chat_id":1,
                                                    "token":tokin,
                                                    "message_id":100})

timer=time.time()-timer

print(relust_a, relust_a.json())
print(relust_b, relust_b.json())
print(relust_с, relust_с.json())
print(relust_g, relust_g.json())
print(relust_h, relust_h.json())
print(relust_j, relust_j.json())
print(f"время исполнения: {timer} s.")