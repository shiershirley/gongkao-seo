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
# V22批次 - Pexels图片
items = [
    ("study","https://images.pexels.com/photos/301982/pexels-photo-301982.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/1376969/pexels-photo-1376969.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/164836/pexels-photo-164836.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/2747449/pexels-photo-2747449.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/159751/laptop-office-desk-work-159755.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/5211438/pexels-photo-5211438.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/5077047/pexels-photo-5077047.jpeg?auto=compress&w=1920"),
    ("study","https://images.pexels.com/photos/4259140/pexels-photo-4259140.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7129713/pexels-photo-7129713.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7129716/pexels-photo-7129716.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7129720/pexels-photo-7129720.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651303/pexels-photo-7651303.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651294/pexels-photo-7651294.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651289/pexels-photo-7651289.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651283/pexels-photo-7651283.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651276/pexels-photo-7651276.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651269/pexels-photo-7651269.jpeg?auto=compress&w=1920"),
    ("office","https://images.pexels.com/photos/7651260/pexels-photo-7651260.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/904616/pexels-photo-904616.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/1144517/pexels-photo-1144517.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/2041549/pexels-photo-2041549.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/3358707/pexels-photo-3358707.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/415071/pexels-photo-415071.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/1200645/pexels-photo-1200645.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/159402/pexels-photo-159402.jpeg?auto=compress&w=1920"),
    ("books","https://images.pexels.com/photos/1619839/pexels-photo-1619839.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/8115857/pexels-photo-8115857.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/4778624/pexels-photo-4778624.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5720333/pexels-photo-5720333.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/3178810/pexels-photo-3178810.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5427670/pexels-photo-5427670.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5427686/pexels-photo-5427686.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5490778/pexels-photo-5490778.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5490883/pexels-photo-5490883.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5427680/pexels-photo-5427680.jpeg?auto=compress&w=1920"),
    ("exam","https://images.pexels.com/photos/5699585/pexels-photo-5699585.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/4427430/pexels-photo-4427430.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/4427432/pexels-photo-4427432.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/4427440/pexels-photo-4427440.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/4427445/pexels-photo-4427445.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730651/pexels-photo-3730651.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730655/pexels-photo-3730655.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730660/pexels-photo-3730660.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730665/pexels-photo-3730665.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730670/pexels-photo-3730670.jpeg?auto=compress&w=1920"),
    ("gov","https://images.pexels.com/photos/3730675/pexels-photo-3730675.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/207696/pexels-photo-207696.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1687845/pexels-photo-1687845.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1240263/pexels-photo-1240263.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/2405547/pexels-photo-2405547.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1365421/pexels-photo-1365421.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1083012/pexels-photo-1083012.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/136404/pexels-photo-136404.jpeg?auto=compress&w=1920"),
    ("motivation","https://images.pexels.com/photos/1409949/pexels-photo-1409949.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1089438/pexels-photo-1089438.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181673/pexels-photo-1181673.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181298/pexels-photo-1181298.jpeg?auto=compress&w=1920"),
    ("tech","https://images.pexels.com/photos/1181354/pexels-photo-1181354.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1558439/pexels-photo-1558439.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1563250/pexels-photo-1563250.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1563256/pexels-photo-1563256.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1563260/pexels-photo-1563260.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1563266/pexels-photo-1563266.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1506906/pexels-photo-1506906.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/1474739/pexels-photo-1474739.jpeg?auto=compress&w=1920"),
    ("city","https://images.pexels.com/photos/151817394/pexels-photo-151817394.jpeg?auto=compress&w=1920"),
    ("writing","https://images.pexels.com/photos/1024253/pexels-photo-1024253.jpeg?auto=compress&w=1920"),
    ("writing","https://images.pexels.com/photos/1024257/pexels-photo-1024257.jpeg?auto=compress&w=1920"),
    ("writing","https://images.pexels.com/photos/1024261/pexels-photo-1024261.jpeg?auto=compress&w=1920"),
    ("writing","https://images.pexels.com/photos/1024265/pexels-photo-1024265.jpeg?auto=compress&w=1920"),
    ("writing","https://images.pexels.com/photos/1024270/pexels-photo-1024270.jpeg?auto=compress&w=1920"),
    ("nature","https://images.pexels.com/photos/1166209/pexels-photo-1166209.jpeg?auto=compress&w=1920"),
    ("nature","https://images.pexels.com/photos/1170602/pexels-photo-1170602.jpeg?auto=compress&w=1920"),
    ("nature","https://images.pexels.com/photos/1166215/pexels-photo-1166215.jpeg?auto=compress&w=1920"),
    ("nature","https://images.pexels.com/photos/1166220/pexels-photo-1166220.jpeg?auto=compress&w=1920"),
    ("nature","https://images.pexels.com/photos/1166225/pexels-photo-1166225.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/762020/pexels-photo-762020.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/775558/pexels-photo-775558.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/814534/pexels-photo-814534.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/819754/pexels-photo-819754.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/820272/pexels-photo-820272.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/830589/pexels-photo-830589.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/840892/pexels-photo-840892.jpeg?auto=compress&w=1920"),
    ("people","https://images.pexels.com/photos/861783/pexels-photo-861783.jpeg?auto=compress&w=1920"),
]
cnt = {}
for cat, url in items:
    d = BASE / cat
    d.mkdir(exist_ok=True)
    n = len(list(d.glob("*.jpg")))
    path = d / f"{cat}_v22_{n+1:03d}.jpg"
    if dl(url, path):
        cnt[cat] = cnt.get(cat, 0) + 1
    time.sleep(0.15)
print("V22:", cnt, "Total:", sum(cnt.values()))
