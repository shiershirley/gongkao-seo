"""Fix unquoted date fields in frontmatter to prevent YAML Date object parsing."""
import os
import re

files = [
    "content/zhenti-jiexi/shegong-xingce-kaodian-shezhi-2026.md",
    "content/zhenti-jiexi/2026-05-21-gongji-falv-changshi-gaopin-kaodian.md",
    "content/shang-an-jingyan/shegong-beikao-yiban-jingyan-2026.md",
    "content/zhengce-jiedu/shegong-zhengce-2026-nian-du-gaishu.md",
    "content/guokao/2026-05-21-guokao-xingce-yanyu-lijie-tifen.md",
    "content/guokao/2026-05-21-guokao-baoming-xuangang-celue.md",
    "content/zhengce-jiedu/2026-05-18-shehuigongzuozhe-vs-shequgongzuozhe.md",
    "content/zhengce-jiedu/2026-05-18-shegong-zhendebachi-ma.md",
    "content/zhengce-jiedu/2026-05-18-shegong-vs-shiyedanwei-qubie.md",
    "content/zhengce-jiedu/2026-05-18-shegong-tuixiu-daiyu-yanglaojin.md",
    "content/zhengce-jiedu/2026-05-18-shegong-shangban-shijian-jiaban.md",
    "content/zhengce-jiedu/2026-05-18-shegong-gongzuo-qiangdu-jiaban.md",
    "content/zhengce-jiedu/2026-05-18-jiedaoban-vs-shegong-qubie.md",
    "content/gangwei-fenxi/shegong-gangwei-zhinenghua-2026.md",
    "content/gangwei-fenxi/2026-05-21-gongkao-gangwei-jingzhengbi-fenxi.md",
    "content/beikao-zhinan/shegong-bishi-fenshu-xian-2026.md",
    "content/shengkao/2026-05-21-shengkao-ziliao-fenxi-susuan.md",
    "content/shengkao/2026-05-21-shengkao-shenlun-duice-dajiegou.md",
    "content/baokao-gonggao/2026-shequ-gongzuo-zhaopin-gaikuang.md",
    "content/shanghai-shegong/2026-05-18-shanghai-shegong-xinzi-daiyu.md",
    "content/shanghai-shegong/shanghai-shegong-xinzi-gangkou-2026.md",
    "content/shanghai-shegong/shanghai-shegong-beikao-shijian-2026.md",
    "content/shanghai-shegong/2026-05-21-shanghai-shegong-wanggehua-guanli.md",
    "content/shanghai-shegong/2026-05-21-shanghai-shegong-bishi-gongji-fuxi.md",
]

fixed = 0
for f in files:
    fp = os.path.join(os.path.dirname(os.path.dirname(__file__)), f.replace("/", os.sep))
    if not os.path.exists(fp):
        print(f"SKIP (not found): {f}")
        continue
    with open(fp, "r", encoding="utf-8") as fh:
        content = fh.read()
    new_content = re.sub(
        r'^date: (\d{4}-\d{2}-\d{2})\s*$',
        r'date: "\1"',
        content,
        flags=re.MULTILINE,
    )
    if new_content != content:
        with open(fp, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        fixed += 1
        print(f"FIXED: {f}")
    else:
        print(f"NO CHANGE: {f}")

print(f"\nTotal fixed: {fixed} files")
