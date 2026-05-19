import yaml
import sys

files = [
    'content/zhengce-jiedu/2026-05-19-shegong-keyi-kaogongwuyuan-ma.md',
    'content/zhengce-jiedu/2026-05-19-shegong-kaoshi-baomingfei-biaozhun.md',
    'content/gangwei-fenxi/2026-05-19-shegong-shiyongqi-duojiu.md',
    'content/beikao-zhinan/2026-05-19-shegong-kaoshi-yinian-jici.md',
    'content/baokao-gonggao/2026-05-19-shegong-zhengsha-yanjige-ma.md',
    'content/zhengce-jiedu/2026-05-19-shegong-youxiaoqi-jinian.md',
    'content/beikao-zhinan/2026-05-19-shegong-kaoshi-nan-bu-nan.md',
    'content/gangwei-fenxi/2026-05-19-shegong-tuixiu-daiyu-yanglaojin.md',
    'content/zhenti-jiexi/2026-05-19-shegong-bishi-nandian-jiexi.md',
]

ok_count = 0
for f in files:
    fname = f.split('/')[-1]
    try:
        with open(f, encoding='utf-8') as fp:
            content = fp.read()
        if content.startswith('---'):
            end = content.find('---', 3)
            fm = content[3:end]
            data = yaml.safe_load(fm)
            required = ['title','description','date','category','tags','author']
            missing = [k for k in required if k not in data]
            if missing:
                msg = 'MISSING FIELDS in ' + fname + ': ' + str(missing)
            else:
                msg = 'OK: ' + fname
                ok_count += 1
        else:
            msg = 'NO FRONTMATTER: ' + fname
    except Exception as e:
        msg = 'ERROR ' + fname + ': ' + str(e)
    sys.stdout.buffer.write((msg + '\n').encode('utf-8', errors='replace'))

sys.stdout.buffer.write(('Total OK: ' + str(ok_count) + '/' + str(len(files)) + '\n').encode('utf-8'))
