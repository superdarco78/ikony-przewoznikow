# wersja 1.3
import os
import subprocess
import concurrent.futures
import datetime
from pathlib import Path
from PIL import Image
from io import BytesIO

IKONY = Path("ikony")
IKONY.mkdir(parents=True, exist_ok=True)

przewoznicy = [
    ("ztm_warszawa",        "ZTM Warszawa",          "https://www.wtp.waw.pl/wp-content/themes/wtp-theme/images/favicon.ico",                                                    "wtp.waw.pl"),
    ("polregio",            "PolRegio",              "https://polregio.pl/images/favicons/apple-icon-57x57.png",                                                                  "polregio.pl"),
    ("pkp_intercity",       "PKP Intercity",         "https://ebilet.intercity.pl/favicon.ico",                                                                              "intercity.pl"),
    ("koleje_mazowieckie",  "Koleje Mazowieckie",    "https://mazowieckie.com.pl/sites/default/files/favicon.png",                                                                "mazowieckie.com.pl"),
    ("wkd",                 "WKD",                   "https://wkd.com.pl/templates/wkd/fav/apple-icon-57x57.png",                                                                "wkd.com.pl"),
    ("pkp_skm_trojmiasto",  "PKP SKM Trojmiasto",   "https://www.skm.pkp.pl/_assets/b733c679720d3533bec8682561dedb7a/img/favicons/apple-icon-57x57.png",                         "skm.pkp.pl"),
    ("koleje_slaskie",      "Koleje Slaskie",        "https://www.kolejeslaskie.pl/app/uploads/2026/02/favicon-white-color-48x48.png",                                           "kolejeslaskie.pl"),
    ("koleje_dolnoslaskie", "Koleje Dolnoslaskie",   "https://kolejedolnoslaskie.pl/favicon.ico",                                                                                "kolejedolnoslaskie.pl"),
    ("koleje_wielkopolskie","Koleje Wielkopolskie",  "https://koleje-wielkopolskie.com.pl/wp-content/themes/koleje_wielkopolskie/img/general/favicon.jpg",                       "koleje-wielkopolskie.com.pl"),
    ("skm_warszawa",        "SKM Warszawa",          "https://www.skm.warszawa.pl/wp-content/themes/skm//public/images/favicon/apple-touch-icon.png",                           "skm.warszawa.pl"),
    ("lka",                 "LKA",                   "https://lka.lodzkie.pl/favicon.ico",                                                                                       "lka.lodzkie.pl"),
    ("koleje_malopolskie",  "Koleje Malopolskie",    "https://kolejemalopolskie.com.pl/uploaded_images/1648251769_favn.ico",                                                     "kolejemalopolskie.com.pl"),
    ("arriva",              "Arriva RP",             "https://arriva.pl/public/img/favicon.ico",                                                                                 "arriva.pl"),
    ("regiojet",            "RegioJet",              "https://regiojet.pl/favicon.ico",                                                                                           "regiojet.pl"),
    ("leo_express",         "Leo Express",           "https://www.leoexpress.com/static/apple-touch-icon.png?v=2",                                                               "leoexpress.com"),
    ("ztm_gzm",             "ZTM GZM",               "https://www.metropoliaztm.pl/static/ztmweb/icons/favicon.ico",                                                            "metropoliaztm.pl"),
    ("zdmikp_bydgoszcz",    "ZDMiKP Bydgoszcz",     "https://zdmikp.bydgoszcz.pl/media/system/images/favicon.ico",                                                             "zdmikp.bydgoszcz.pl"),
    ("mzdik_radom",         "MZDiK Radom",           "https://www.mzdik.pl/images/static/icon.png",                                                                             "mzdik.pl"),
    ("ztm_rzeszow",         "ZTM Rzeszow",           "https://ztm.erzeszow.pl/media/uploads/2024/03/cropped-favicon_ZTM-02-32x32.png",                                         "ztm.rzeszow.pl"),
    ("ztm_lublin",          "ZTM Lublin",            "https://www.ztm.lublin.eu/favicon.ico",                                                                                   "ztm.lublin.eu"),
    ("ztm_kielce",          "ZTM Kielce",            "https://ztm.kielce.pl/templates/rptheme/favicon.ico",                                                                     "ztm.kielce.pl"),
    ("mzk_torun",           "MZK Torun",             "https://www.torun.pl/sites/default/files/favicons/apple-touch-icon.png",                                                  "torun.pl"),
    ("mzk_wejherowo",       "MZK Wejherowo",         "https://mzkwejherowo.pl/assets/spina/favicon-6f0f5d6f.png",                                                               "mzkwejherowo.pl"),
    ("mpk_lomza",           "MPK Lomza",             "https://www.mpklomza.pl/favicon.ico",                                                                                     "mpklomza.pl"),
    ("ka_swinoujscie",      "KA Swinoujscie",        "https://www.ka.swinoujscie.pl/templates/komunikacja/favicon.ico",                                                        "ka.swinoujscie.pl"),
    ("gzk_bystry",          "GZK Bystry",            "https://gzkbystry.pl/images/favicon.ico",                                                                                "gzkbystry.pl"),
    ("mzk_elk",             "MZK Elk",               "https://mzk.elk.pl/wp-content/uploads/2021/06/cropped-logo-mzk-32x32.jpg",                                               "mzk.elk.pl"),
    ("zkm_elblag",          "ZKM Elblag",            "https://www.zkm.elblag.com.pl/wp-content/uploads/2020/10/cropped-logo-300x300-1-e1602680131854-32x32.png",               "zkm.elblag.com.pl"),
    ("mzk_gorzow",          "MZK Gorzow Wlkp",      "https://mzk-gorzow.com.pl/favicon/32x32.png?ts=1628685347",                                                              "mzk-gorzow.com.pl"),
    ("ztp_krakow",          "ZTP Krakow",            "https://ztp.krakow.pl/wp-content/themes/wpsite/favicons/apple-touch-icon.png",                                           "ztp.krakow.pl"),
    ("um_wroclaw",          "UM Wroclaw",            "https://www.wroclaw.pl/themes/favicon/apple-touch-icon.png",                                                              "wroclaw.pl"),
    ("ztm_poznan",          "ZTM Poznan",            "https://www.ztm.poznan.pl/pwa/icons/192.png",                                                                             "ztm.poznan.pl"),
    ("ztm_gdansk",          "ZTM Gdansk",            "https://ztm.gda.pl/images/favicon.ico",                                                                                   "ztm.gda.pl"),
    ("zditm_szczecin",      "ZDiTM Szczecin",        "https://www.zditm.szczecin.pl/build/assets/apple-touch-icon-B3IrERv1.png",                                               "zditm.szczecin.pl"),
    ("bkm_bialystok",       "BKM Bialystok",         "http://komunikacja.bialystok.pl/projects/bkm/img/favicon.png",                                                           "komunikacja.bialystok.pl"),
    ("zkm_gdynia",          "ZKM Gdynia",            "https://zkmgdynia.pl/data/domains/1/favicon/favicon.ico",                                                                "zkmgdynia.pl"),
    ("mpk_czestochowa",     "MPK Czestochowa",       "https://mpk.czest.pl/img/favicon.ico",                                                                                   "mpk.czest.pl"),
    ("zdzit_olsztyn",       "ZDZiT Olsztyn",         "https://zdzit.olsztyn.eu/wp-content/uploads/2023/07/cropped-logozdzit-150x150.png",                                      "zdzit.olsztyn.eu"),
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"

MAGIC = [b'\x89PNG', b'\xff\xd8\xff', b'GIF8', b'\x00\x00\x01\x00', b'\x00\x00\x02\x00', b'BM']

def jest_obrazkiem(dane):
    for m in MAGIC:
        if dane[:len(m)] == m:
            return True
    return False

def curl(url, tor=False):
    cmd = ["curl", "-sL", "--max-time", "12", "--insecure", "--compressed",
           "-A", UA, "-H", "Accept: image/*,*/*;q=0.8",
           "-H", "Referer: https://" + url.split("/")[2] + "/"]
    if tor:
        cmd += ["--socks5-hostname", "127.0.0.1:9050", "--max-time", "15"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, timeout=18)
    if r.returncode == 0 and len(r.stdout) > 100 and jest_obrazkiem(r.stdout):
        return r.stdout
    raise Exception("rc={} len={} magic={}".format(r.returncode, len(r.stdout), r.stdout[:8]))

def pobierz(url, domena):
    for metoda in [
        lambda: curl(url),
        lambda: curl(url, tor=True),
        lambda: curl("https://www.google.com/s2/favicons?domain={}&sz=64".format(domena)),
        lambda: curl("https://icons.duckduckgo.com/ip3/{}.ico".format(domena)),
        lambda: curl("https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://{}&size=64".format(domena)),
    ]:
        try:
            return metoda()
        except Exception:
            pass
    raise Exception("wszystkie metody zawiodly dla: " + domena)

def usun_tlo(img):
    img = img.convert("RGBA")
    img = img.resize((64, 64), Image.LANCZOS)
    px = img.load()
    w, h = img.size
    TOL = 45
    bg = px[0, 0][:3]

    def bliski(c):
        return all(abs(int(c[i]) - int(bg[i])) <= TOL for i in range(3)) and c[3] > 10

    odwiedzony = [[False] * h for _ in range(w)]
    kolejka = []

    def dodaj(x, y):
        if 0 <= x < w and 0 <= y < h and not odwiedzony[x][y] and bliski(px[x, y]):
            odwiedzony[x][y] = True
            kolejka.append((x, y))

    for rog in [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]:
        dodaj(*rog)

    while kolejka:
        x, y = kolejka.pop()
        r2, g2, b2, a2 = px[x, y]
        px[x, y] = (r2, g2, b2, 0)
        dodaj(x-1, y); dodaj(x+1, y); dodaj(x, y-1); dodaj(x, y+1)

    return img

WYMUS = ["pkp_intercity"]  # lista id do wymuszonego pobrania

def przetworz(wpis):
    cid, nazwa, url, domena = wpis
    plik = IKONY / (cid + ".webp")
    if plik.exists() and plik.stat().st_size > 100 and cid not in WYMUS:
        print("pominiety: " + nazwa)
        return cid, "pominiety", None
    try:
        dane = pobierz(url, domena)
        img = Image.open(BytesIO(dane))
        img = usun_tlo(img)
        img.save(str(plik), "WEBP", lossless=True, quality=90)
        print("ok: " + nazwa)
        return cid, "ok", None
    except Exception as e:
        print("blad: " + nazwa + " — " + str(e))
        return cid, "blad", str(e)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    wyniki = list(executor.map(przetworz, przewoznicy))

ok        = [w for w in wyniki if w[1] == "ok"]
pominiete = [w for w in wyniki if w[1] == "pominiety"]
bledy     = [w for w in wyniki if w[1] == "blad"]

print("\nNowe: {}  Pominiete: {}  Bledy: {}".format(len(ok), len(pominiete), len(bledy)))
if bledy:
    print("Nieudane: " + ", ".join(b[0] for b in bledy))

linie = [
    "Wygenerowano: " + datetime.datetime.utcnow().isoformat(),
    "Nowe: {}  Pominiete: {}  Bledy: {}".format(len(ok), len(pominiete), len(bledy)),
] + ["BLAD " + b[0] + ": " + str(b[2]) for b in bledy]

(IKONY / "_raport.txt").write_text("\n".join(linie))
