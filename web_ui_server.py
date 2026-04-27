from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import os

app = FastAPI()

test=True


if not  test:
    path_index=os.path.join(os.getcwd(), "...", "index.html")
    with open(path_index, 'r') as f:
        content=f.read()
else:
    content="""
<!DOCTYPE html>
<html lang="ru">
<head>
</head>
<body>
<h1>Hello !</h1>
<hr size="5" style="color:#731600">
<h3>content</h3>
</body>
"""

@app.get("/", response_class=HTMLResponse)
async def main():
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8800)  # Запуск FastAPI