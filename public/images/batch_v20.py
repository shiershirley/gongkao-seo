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

# 快速V20批次 - 精选50张
items = [
    ("study","https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920"),
    ("study","https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1920"),
    ("study","https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920"),
    ("study","https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920"),
    ("study","https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920"),
    ("office","https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920"),
    ("office","https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1920"),
    ("office","https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=1920"),
    ("office","https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1920"),
    ("office","https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1920"),
    ("books","https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?w=1920"),
    ("books","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920"),
    ("books","https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=1920"),
    ("books","https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920"),
    ("books","https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1920"),
    ("exam","https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920"),
    ("exam","https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920"),
    ("exam","https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920"),
    ("exam","https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1920"),
    ("exam","https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920"),
    ("gov","https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=1920"),
    ("gov","https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920"),
    ("gov","https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920"),
    ("gov","https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920"),
    ("gov","https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920"),
    ("tech","https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1920"),
    ("tech","https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1920"),
    ("tech","https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920"),
    ("tech","https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920"),
    ("tech","https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1920"),
    ("city","https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920"),
    ("city","https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920"),
    ("city","https://images.unsplash.com/photo-1464817739973-0128fe77aaa1?w=1920"),
    ("city","https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920"),
    ("city","https://images.unsplash.com/photo-1494522855154-9297ac14b55f?w=1920"),
    ("writing","https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1920"),
    ("writing","https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1920"),
    ("writing","https://images.unsplash.com/photo-1519791883288-dc8bd696e667?w=1920"),
    ("nature","https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920"),
    ("nature","https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920"),
    ("nature","https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=1920"),
    ("people","https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920"),
    ("people","https://images.unsplash.com/photo-1560250097-0b93528c311a?w=1920"),
    ("people","https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920"),
    ("people","https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920"),
    ("people","https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1920"),
]

cnt = {}
for cat, url in items:
    d = BASE / cat
    d.mkdir(exist_ok=True)
    n = len(list(d.glob("*.jpg")))
    path = d / f"{cat}_v20_{n+1:03d}.jpg"
    if dl(url, path):
        cnt[cat] = cnt.get(cat, 0) + 1
    time.sleep(0.15)

print("V20:", cnt)
print("Total:", sum(cnt.values()))
