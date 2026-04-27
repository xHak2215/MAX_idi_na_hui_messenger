import requests
import time

timer=time.time()

root_ip="http://127.0.1.1:8800"

relust_c=requests.get(f"{root_ip}/data_bese/new_user", params={
                                                        "password":"1234", 
                                                        "login":"user228", 
                                                        "name":"Павел Дуров",
                                                        "email":"arikr2886@gmail.com"})# запрос на создание пользователя

relust_d=requests.get(f"{root_ip}/data_bese/get_data_user", params={"login":"user228"})# запрос на получение его данных

timer=time.time()-timer

print(relust_c.json())
print(relust_d.json())
print(f"время исполнения: {timer} s.")