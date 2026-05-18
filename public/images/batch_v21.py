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
items = [
    ("study","https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920"),
    ("study","https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1920"),
    ("study","https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920"),
    ("study","https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920"),
    ("study","https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1920"),
    ("study","https://images.unsplash.com/photo-1519682577862-22b62b24e493?w=1920"),
    ("office","https://images.unsplash.com/photo-1552581234-26160f608093?w=1920"),
    ("office","https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=1920"),
    ("office","https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1920"),
    ("office","https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1920"),
    ("office","https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920"),
    ("office","https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=1920"),
    ("office","https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920"),
    ("books","https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920"),
    ("books","https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1920"),
    ("books","https://images.unsplash.com/photo-1456428746267-a1756408f782?w=1920"),
    ("books","https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920"),
    ("books","https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=1920"),
    ("exam","https://images.unsplash.com/photo-1513297887119-d46091b24bfa?w=1920"),
    ("exam","https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=1920"),
    ("exam","https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1920"),
    ("exam","https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920"),
    ("exam","https://images.unsplash.com/photo-1530099486328-e021101a494a?w=1920"),
    ("gov","https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920"),
    ("gov","https://images.unsplash.com/photo-1494522855154-9297ac14b55f?w=1920"),
    ("gov","https://images.unsplash.com/photo-1479839672679-a46483c0e7c8?w=1920"),
    ("gov","https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=1920"),
    ("gov","https://images.unsplash.com/photo-1478827536114-da961b7f86d2?w=1920"),
    ("gov","https://images.unsplash.com/photo-1508780709619-79562169bc64?w=1920"),
    ("gov","https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1504700610630-ac6aba3536d3?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1452704095509-f5c4e8b8b8e8?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1464820453369-31d2c0b651af?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=1920"),
    ("tech","https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920"),
    ("tech","https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920"),
    ("tech","https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1920"),
    ("tech","https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1920"),
    ("tech","https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1920"),
    ("city","https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1920"),
    ("city","https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920"),
    ("city","https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1920"),
    ("city","https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=1920"),
    ("city","https://images.unsplash.com/photo-1518391846015-55a9cc003b25?w=1920"),
    ("city","https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1920"),
    ("writing","https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=1920"),
    ("writing","https://images.unsplash.com/photo-1457804168348-a2c63dc1b8d5?w=1920"),
    ("nature","https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920"),
    ("nature","https://images.unsplash.com/photo-1464820453369-31d2c0b651af?w=1920"),
    ("nature","https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920"),
    ("nature","https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920"),
    ("people","https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1920"),
    ("people","https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920"),
    ("people","https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=1920"),
    ("people","https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=1920"),
    ("people","https://images.unsplash.com/photo-1507152832242-10c240b0fabc?w=1920"),
]
cnt = {}
for cat, url in items:
    d = BASE / cat
    d.mkdir(exist_ok=True)
    n = len(list(d.glob("*.jpg")))
    path = d / f"{cat}_v21_{n+1:03d}.jpg"
    if dl(url, path):
        cnt[cat] = cnt.get(cat, 0) + 1
    time.sleep(0.15)
print("V21:", cnt, "Total:", sum(cnt.values()))
