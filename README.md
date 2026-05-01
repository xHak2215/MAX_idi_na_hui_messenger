# MAX иди нахуй мессенджер

## навигация по документации

по __коду__: <a href="/doc/code.md">code.md</a> 

по __архитектуре__ и __API__: <a href="/doc/structure.md">structure.md</a>

---

# серверная часть 

## API

0. **установка зависимостей:**
```bash
pip install -r requirements.txt
```

1. **Запуск сервера:**
```bash
python api.py
```

2. **Тестирование:**
```bash
python test/api_test_user.py
ptyhon test/api_test_chat.py
python test/api_test_media.py
```

### работа с Makefile

1. **установка зависемостей:**
 
```bash
make install
```

2. **запуск:**

```bash
make run
```

3. **запуск тестов:**
перед запуском тестов нужно запустить сервер 2 командой

```bash
make test
```
