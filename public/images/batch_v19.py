# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os, time, requests
from pathlib import Path
from PIL import Image
from io import BytesIO

BASE_DIR = Path("lib")

def dl(url, path):
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            if img.width >= 800:
                img.save(path, "JPEG", quality=90)
                return True
    except: pass
    return False

# V19批次 - 200张精选Unsplash图片
urls = [
    ("study","https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1920"),
    ("study","https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1920"),
    ("study","https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1920"),
    ("study","https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920"),
    ("study","https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920"),
    ("study","https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1920"),
    ("study","https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?w=1920"),
    ("study","https://images.unsplash.com/photo-1519682577862-22b62b24e493?w=1920"),
    ("study","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920"),
    ("study","https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=1920"),
    ("study","https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920"),
    ("study","https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920"),
    ("study","https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1920"),
    ("study","https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920"),
    ("study","https://images.unsplash.com/photo-1519682577862-22b62b24e493?w=1920"),
    ("office","https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920"),
    ("office","https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1920"),
    ("office","https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=1920"),
    ("office","https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1920"),
    ("office","https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1920"),
    ("office","https://images.unsplash.com/photo-1552581234-26160f608093?w=1920"),
    ("office","https://images.unsplash.com/photo-1517502884422-41eaead166d4?w=1920"),
    ("office","https://images.unsplash.com/photo-1497215842964-222b430dc094?w=1920"),
    ("office","https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1920"),
    ("office","https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1920"),
    ("office","https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1920"),
    ("office","https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920"),
    ("office","https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=1920"),
    ("office","https://images.unsplash.com/photo-1552664730-d307ca884978?w=1920"),
    ("office","https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1920"),
    ("books","https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1920"),
    ("books","https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1920"),
    ("books","https://images.unsplash.com/photo-1491841550275-ad7854e35ca6?w=1920"),
    ("books","https://images.unsplash.com/photo-1512820790803-83ca734da794?w=1920"),
    ("books","https://images.unsplash.com/photo-1519682577862-22b62b24e493?w=1920"),
    ("books","https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=1920"),
    ("books","https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920"),
    ("books","https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=1920"),
    ("books","https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1920"),
    ("books","https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920"),
    ("books","https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920"),
    ("books","https://images.unsplash.com/photo-1456428746267-a1756408f782?w=1920"),
    ("books","https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920"),
    ("books","https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=1920"),
    ("exam","https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920"),
    ("exam","https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920"),
    ("exam","https://images.unsplash.com/photo-1513297887119-d46091b24bfa?w=1920"),
    ("exam","https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920"),
    ("exam","https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1920"),
    ("exam","https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=1920"),
    ("exam","https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1920"),
    ("exam","https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=1920"),
    ("exam","https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920"),
    ("exam","https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1920"),
    ("exam","https://images.unsplash.com/photo-1456428746267-a1756408f782?w=1920"),
    ("exam","https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1920"),
    ("exam","https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=1920"),
    ("exam","https://images.unsplash.com/photo-1530099486328-e021101a494a?w=1920"),
    ("gov","https://images.unsplash.com/photo-1523995462485-3d171b5c8fa9?w=1920"),
    ("gov","https://images.unsplash.com/photo-1577493340887-b7bfff550145?w=1920"),
    ("gov","https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920"),
    ("gov","https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920"),
    ("gov","https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920"),
    ("gov","https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=1920"),
    ("gov","https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920"),
    ("gov","https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920"),
    ("gov","https://images.unsplash.com/photo-1494522855154-9297ac14b55f?w=1920"),
    ("gov","https://images.unsplash.com/photo-1479839672679-a46483c0e7c8?w=1920"),
    ("gov","https://images.unsplash.com/photo-1464817739973-0128fe77aaa1?w=1920"),
    ("gov","https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=1920"),
    ("gov","https://images.unsplash.com/photo-1478827536114-da961b7f86d2?w=1920"),
    ("gov","https://images.unsplash.com/photo-1508780709619-79562169bc64?w=1920"),
    ("gov","https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1504700610630-ac6aba3536d3?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1495616811223-4d98c6e9c869?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1452704095509-f5c4e8b8b8e8?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1464820453369-31d2c0b651af?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920"),
    ("motivation","https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920"),
    ("tech","https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1920"),
    ("tech","https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1920"),
    ("tech","https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920"),
    ("tech","https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920"),
    ("tech","https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=1920"),
    ("tech","https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1920"),
    ("tech","https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1920"),
    ("tech","https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1920"),
    ("tech","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920"),
    ("tech","https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1920"),
    ("tech","https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920"),
    ("tech","https://images.unsplash.com/photo-1518932945647-7a1c969e8921?w=1920"),
    ("tech","https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1920"),
    ("tech","https://images.unsplash.com/photo-1487058792275-0ad4aaf24ca7?w=1920"),
    ("tech","https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920"),
    ("city","https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=1920"),
    ("city","https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920"),
    ("city","https://images.unsplash.com/photo-1444723121867-7a241cacace9?w=1920"),
    ("city","https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920"),
    ("city","https://images.unsplash.com/photo-1464817739973-0128fe77aaa1?w=1920"),
    ("city","https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920"),
    ("city","https://images.unsplash.com/photo-1494522855154-9297ac14b55f?w=1920"),
    ("city","https://images.unsplash.com/photo-1478827536114-da961b7f86d2?w=1920"),
    ("city","https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1920"),
    ("city","https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920"),
    ("city","https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=1920"),
    ("city","https://images.unsplash.com/photo-1509114397022-ed747cca3f65?w=1920"),
    ("city","https://images.unsplash.com/photo-1518391846015-55a9cc003b25?w=1920"),
    ("city","https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1920"),
    ("writing","https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1920"),
    ("writing","https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1920"),
    ("writing","https://images.unsplash.com/photo-1513258496099-48168024aec0?w=1920"),
    ("writing","https://images.unsplash.com/photo-1456428746267-a1756408f782?w=1920"),
    ("writing","https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=1920"),
    ("writing","https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=1920"),
    ("writing","https://images.unsplash.com/photo-1455390582262-044cdead277a?w=1920"),
    ("writing","https://images.unsplash.com/photo-1519791883288-dc8bd696e667?w=1920"),
    ("writing","https://images.unsplash.com/photo-1457804168348-a2c63dc1b8d5?w=1920"),
    ("writing","https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=1920"),
    ("writing","https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1920"),
    ("nature","https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920"),
    ("nature","https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920"),
    ("nature","https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=1920"),
    ("nature","https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920"),
    ("nature","https://images.unsplash.com/photo-1464820453369-31d2c0b651af?w=1920"),
    ("nature","https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920"),
    ("nature","https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1920"),
    ("nature","https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=1920"),
    ("nature","https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920"),
    ("people","https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=1920"),
    ("people","https://images.unsplash.com/photo-1560250097-0b93528c311a?w=1920"),
    ("people","https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=1920"),
    ("people","https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=1920"),
    ("people","https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920"),
    ("people","https://images.unsplash.com/photo-1560250097-0b93528c311a?w=1920"),
    ("people","https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=1920"),
    ("people","https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=1920"),
    ("people","https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=1920"),
    ("people","https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=1920"),
]

cnt = {}
for cat, url in urls:
    d = BASE_DIR / cat
    d.mkdir(exist_ok=True)
    n = len(list(d.glob("*.jpg")))
    path = d / f"{cat}_v19_{n+1:03d}.jpg"
    if dl(url, path):
        cnt[cat] = cnt.get(cat, 0) + 1
        time.sleep(0.2)
        
print("V19:", cnt)
print("Total:", sum(cnt.values()))
