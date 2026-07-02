#!/usr/bin/env python3
"""
Pink Leaf Instagram post generator.

Reproduces the Pink Leaf post template (arch photo, big logo, care list, Hebrew
story) as 1080x1553 PNGs. This is the durable version of the design system built
in the studio session, so posts can be regenerated any time without redoing it.

Usage:
    pip install pillow pillow-heif
    python3 generate_posts.py

Reads content from posts_data.json and photos from ./photos/ , writes PNGs to
../../social-posts/ . Requires a Chromium binary (set CHROME env var, or it
looks in /opt/pw-browsers or PATH).

To add a plant: add an entry to posts_data.json and drop its photo in ./photos/ .
Product posts must use a real photo of the actual plant.
"""
import base64, json, os, subprocess, glob, sys
from PIL import Image
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "social-posts")
LOGO = os.path.join(REPO, "logo-dark.png")
PK = "#c98da0"; GR = "#324b39"; PKd = "#b87a92"

def find_chrome():
    if os.environ.get("CHROME"): return os.environ["CHROME"]
    g = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
    if g: return g[0]
    for c in ("chromium", "chromium-browser", "google-chrome"):
        p = subprocess.run(["which", c], capture_output=True, text=True)
        if p.stdout.strip(): return p.stdout.strip()
    sys.exit("No Chromium found. Set CHROME=/path/to/chrome")

def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

def logo_b64():
    """logo-dark.png with its white background knocked out to transparent."""
    im = Image.open(LOGO).convert("RGBA"); px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, bl, a = px[x, y]
            if r > 238 and g > 238 and bl > 238: px[x, y] = (r, g, bl, 0)
    tmp = os.path.join(HERE, "_logo_trans.png"); im.save(tmp); return b64(tmp)

def photo_b64(name):
    src = os.path.join(HERE, "photos", name)
    tmp = os.path.join(HERE, "_p.jpg")
    Image.open(src).convert("RGB").save(tmp, "JPEG", quality=92); return b64(tmp)

IC = {
"sun":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="4.3"/><path d="M12 2.5v2.3M12 19.2v2.3M2.5 12h2.3M19.2 12h2.3M5.2 5.2l1.6 1.6M17.2 17.2l1.6 1.6M18.8 5.2l-1.6 1.6M6.8 17.2l-1.6 1.6"/></svg>'%PK,
"drop":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round"><path d="M12 3.5c3.5 4 5.5 6.7 5.5 9.5a5.5 5.5 0 0 1-11 0c0-2.8 2-5.5 5.5-9.5z"/></svg>'%PK,
"leaf":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"><path d="M4 20c0-8.5 7-14 16-14 0 8.5-5.5 14-14 14"/><path d="M5 19c4-6 8.5-8.5 13-9.5"/></svg>'%PK,
"therm":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6"><path d="M12 4.5a2 2 0 0 1 2 2v8a4 4 0 1 1-4 0v-8a2 2 0 0 1 2-2z"/></svg>'%PK,
"spray":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round"><path d="M9 9h5v10.5a1.5 1.5 0 0 1-1.5 1.5H10.5A1.5 1.5 0 0 1 9 19.5z"/><path d="M9 9V5.5h5M14 6.5h3M14 4.5h2.2"/></svg>'%PK,
"pot":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round"><path d="M6 13.5h12l-1.4 6.5H7.4z"/><path d="M12 13.5c0-3 2-5 5-5M12 13.5c0-2.2-1.8-4-4.5-4"/></svg>'%PK,
"climb":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"><path d="M12 21V6"/><path d="M12 11c-3 0-5-2-5-5 3 0 5 2 5 5zM12 9c3 0 5-2 5-4-3 0-5 2-5 4z"/></svg>'%PK,
"ig":'<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="1.7"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17" cy="7" r="1.1" fill="%s" stroke="none"/></svg>'%(PKd,PKd),
"leafsm":'<svg viewBox="0 0 24 24" fill="%s" stroke="none"><path d="M4 20c0-8.5 7-14 16-14 0 8.5-5.5 14-14 14z" opacity=".85"/></svg>'%GR,
}
CARE = {
"ALO":[("sun","אור בהיר ועקיף, ללא שמש ישירה"),("drop","לחות גבוהה, 60% ומעלה"),("leaf","מצע קליל ומאוורר עם ניקוז מעולה"),("therm","השקיה מדודה, להמתין לייבוש קל"),("spray","רגיש לריקבון שורשים"),("pot","נכנסת לרדמה בחורף, נשירת עלים טבעית")],
"MON":[("sun","אור בהיר ועקיף"),("drop","לחות בינונית עד גבוהה"),("leaf","מצע מאוורר עם ניקוז טוב"),("therm","השקיה כשהמצע מתייבש קלות"),("climb","אוהבת מוט תמיכה לטיפוס"),("pot","צמיחה איטית, סבלנות משתלמת")],
}

def html(p, logo):
    photo = photo_b64(p["photo"])
    rows = "".join(f'<div class="cr"><div class="ci">{IC[k]}</div><div class="ct">{t}</div></div>' for k,t in CARE[p["care"]])
    return f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
@page{{size:1080px 1553px;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1553px;background:#f0e8dc;font-family:'DejaVu Sans',sans-serif;color:#463f36;position:relative;overflow:hidden}}
.wm{{position:absolute;left:60px;top:52px}}
.wm .a{{font-family:'FreeSerif',serif;font-size:33px;letter-spacing:5px;color:{GR};font-weight:bold}}
.wm .b{{font-size:14px;letter-spacing:6px;color:{PK};margin-top:3px}}
.hline{{position:absolute;left:300px;width:610px;top:74px;border-top:1px solid #d9bfc6}}
.hleaf{{position:absolute;left:998px;top:56px;width:30px;height:30px;transform:rotate(20deg)}}
.col{{position:absolute;left:60px;top:168px;width:452px;text-align:right}}
h1{{font-family:'FreeSerif',serif;font-size:74px;line-height:1.03;color:{GR};font-weight:bold}}
.subhe{{font-size:26px;color:{PK};font-weight:bold;margin-top:16px}}
.suben{{font-size:30px;color:{PK};font-weight:bold;letter-spacing:1px}}
.dot{{width:6px;height:6px;border-radius:50%;background:{PK};margin:18px 0 18px auto}}
.story{{font-size:24px;line-height:1.72;font-weight:300}}
.careh{{display:flex;align-items:center;gap:12px;margin:24px 0 4px;flex-direction:row-reverse}}
.careh .t{{font-family:'FreeSerif',serif;font-size:26px;color:{GR};font-weight:bold;white-space:nowrap}}
.careh .lv{{width:24px;height:24px}} .careh .ln{{flex:1;border-top:1px solid #d9bfc6}}
.cr{{display:flex;direction:ltr;align-items:center;padding:9px 0;border-bottom:1px solid #e6d8dc}}
.ci{{width:58px;flex:none;text-align:center}} .ci svg{{width:30px;height:30px}}
.ct{{flex:1;text-align:right;font-size:21px;font-weight:300;border-left:1px solid #e6d8dc;margin-left:18px;padding-right:18px}}
.photo{{position:absolute;left:552px;top:140px;width:474px;height:1168px;border-radius:237px 237px 22px 22px;background-image:url('data:image/jpeg;base64,{photo}');background-size:cover;background-position:{p['bgpos']};box-shadow:0 20px 46px rgba(60,40,45,.24)}}
.archln{{position:absolute;left:540px;top:120px;width:498px;height:1198px;border:1px solid #cbb0b8;border-radius:249px 249px 24px 24px}}
.sumbox{{position:absolute;left:60px;top:1224px;width:452px;height:282px;border:1px solid #d3bcc2;border-radius:18px;display:flex;direction:ltr;align-items:center;padding:0 30px;gap:24px}}
.sumbox .lg img{{height:238px;display:block}}
.sumbox .vd{{width:1px;height:206px;background:#e0cdd2;flex:none}}
.sumbox .tg{{flex:1;text-align:right;font-size:16px;line-height:1.55;color:#6a6157;font-weight:300}}
.ig{{position:absolute;left:702px;top:1352px;display:flex;direction:ltr;align-items:center;gap:11px}}
.ig svg{{width:34px;height:34px}} .ig span{{font-size:26px;color:{PKd};font-weight:bold}}
</style></head><body>
<div class="wm"><div class="a">PINK LEAF</div><div class="b">BOTANICAL STUDIOS</div></div>
<div class="hline"></div><div class="hleaf">{IC['leafsm']}</div>
<div class="archln"></div><div class="photo"></div>
<div class="col"><h1>{p['h1a']}<br>{p['h1b']}</h1><div class="subhe">{p['subhe']}</div><div class="suben">{p['suben']}</div><div class="dot"></div>
 <div class="story">{p['story']}</div>
 <div class="careh"><span class="lv">{IC['leafsm']}</span><span class="ln"></span><span class="t">איך מטפלים</span></div>{rows}</div>
<div class="sumbox"><div class="lg"><img src="data:image/png;base64,{logo}"></div><div class="vd"></div><div class="tg">נבחרת בקפידה.<br>גדלה באהבה.<br>נשלחת אליכם. <span style="color:{PK}">&#9829;</span></div></div>
<div class="ig">{IC['ig']}<span>@pinkleaf.studio</span></div>
</body></html>"""

def main():
    os.makedirs(OUT, exist_ok=True)
    chrome = find_chrome(); logo = logo_b64()
    data = json.load(open(os.path.join(HERE, "posts_data.json"), encoding="utf-8"))
    for p in data:
        hp = os.path.join(HERE, "_cur.html")
        open(hp, "w", encoding="utf-8").write(html(p, logo))
        out = os.path.join(OUT, p["id"] + ".png")
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            "--screenshot=" + out, "--window-size=1080,1553", hp],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("rendered", p["id"])
    for f in ("_logo_trans.png", "_p.jpg", "_cur.html"):
        try: os.remove(os.path.join(HERE, f))
        except OSError: pass
    print("done ->", OUT)

if __name__ == "__main__":
    main()
