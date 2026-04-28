import requests
from pathlib import Path
import time 

root_ip="http://26.238.36.134:8800"

timer=time.time()
with requests.get(root_ip+"/media/get", stream=True, params={"id":0}) as r:
    r.raise_for_status()
    total = int(r.headers.get("Content-Length", 1))
    out_path = Path("file.jpg")
    downloaded = 0
    with out_path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if not chunk:
                continue
            f.write(chunk)
            downloaded += len(chunk)
            print(f"\r{downloaded}/{total} bytes ({downloaded*100/total}%)", end="")



with open("tests/test_file.bin", "rb") as f:
    r = requests.post(root_ip+"/media/uploadfiles", files={"upload_file": f})
    print(r.json())

           
timer=time.time()-timer

print(f"время исполнения: {timer} s.")
