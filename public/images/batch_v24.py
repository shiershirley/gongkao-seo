# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests, time
from pathlib import Path
from PIL import Image
from io import BytesIO
BASE = Path("lib")
def dl(url, path):
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            if img.width >= 800:
                img.save(path, "JPEG", quality=88)
                return True
    except: pass
    return False
# V24 最后冲刺
items = [
    ("study","https://images.pexels.com/photos/590493/pexels-photo-590493.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/8613089/pexels-photo-8613089.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/8613108/pexels-photo-8613108.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/3807517/pexels-photo-3807517.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/5211438/pexels-photo-5211438.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7129719/pexels-photo-7129719.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651299/pexels-photo-7651299.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651308/pexels-photo-7651308.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651316/pexels-photo-7651316.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651320/pexels-photo-7651320.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/209329/pexels-photo-209329.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/267609/pexels-photo-267609.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/2744107/pexels-photo-2744107.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/7773537/pexels-photo-7773537.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/7773509/pexels-photo-7773509.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/7773489/pexels-photo-7773489.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730680/pexels-photo-3730680.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730685/pexels-photo-3730685.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730690/pexels-photo-3730690.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730695/pexels-photo-3730695.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1166275/pexels-photo-1166275.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1166265/pexels-photo-1166265.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1486325/pexels-photo-1486325.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1497528/pexels-photo-1497528.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/863926/pexels-photo-863926.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/875117/pexels-photo-875117.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/896106/pexels-photo-896106.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/912654/pexels-photo-912654.jpeg?auto=compress&w=1920"),
]
cnt = {}
for cat, url in items:
    d = BASE / cat
    d.mkdir(exist_ok=True)
    n = len(list(d.glob("*.jpg")))
    path = d / f"{cat}_v24_{n+1:03d}.jpg"
    if dl(url, path):
        cnt[cat] = cnt.get(cat, 0) + 1
    time.sleep(0.15)
print("V24:", cnt, "Total:", sum(cnt.values()))
