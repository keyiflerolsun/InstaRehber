# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikTaban import KekikTaban
from KekikInsta import KekikInsta
from json import dumps
from tabulate import tabulate
import os

taban = KekikTaban(
    baslik   = "@KekikAkademi Instagram Telefon Numarası Ayıklayıcı",
    aciklama = "KekikInsta Başlatıldı..",
    banner   = "KekikInsta",
    girinti  = 4
)

konsol = taban.konsol

CIKTI_DIZINI = "Numaralar/"
CIKTI_ISMI   = "KekikInsta"

def json_ver(veri:list):
    dosya_yolu = f"{CIKTI_DIZINI}{CIKTI_ISMI}.json"
    with open(dosya_yolu, "w+", encoding='utf-8') as dosya:
        dosya.write(dumps(veri, ensure_ascii=False, indent=2, sort_keys=False))
    return dosya_yolu

def tablo_ver(veri:list):
    dosya_yolu = f"{CIKTI_DIZINI}{CIKTI_ISMI}.md"
    with open(dosya_yolu, "w+", encoding='utf-8') as dosya:
        dosya.write(tabulate(veri, headers='keys', tablefmt='github'))
    return dosya_yolu

def vcf_ver(veri:list):
    dosya_yolu = f"{CIKTI_DIZINI}{CIKTI_ISMI}.vcf"
    with open(dosya_yolu, "a+", encoding='utf-8') as dosya:
        for kisi in veri:
            try:
                dosya.write(f"""BEGIN:VCARD
VERSION:3.0
FN:{kisi['kisi']}
N:{kisi['kisi']};;;
TEL;TYPE=CELL:{kisi['telefon']}
EMAIL;TYPE=INTERNET:{kisi['mail']}
END:VCARD
""")
            except KeyError:
                dosya.write(f"""BEGIN:VCARD
VERSION:3.0
FN:{kisi['kisi']}
N:{kisi['kisi']};;;
TEL;TYPE=CELL:{kisi['telefon']}
END:VCARD
""")
    return dosya_yolu


if __name__ == '__main__':
    hesap = KekikInsta(konsol.input("[bold red]Kullanıcı Adı : [/]"), konsol.input("[bold red]Giriş Şifresi : [/]"))
    if not os.path.isdir(CIKTI_DIZINI): os.mkdir(CIKTI_DIZINI)
    telefon_numaralari = hesap.telefon_ver
    print('\n')
    if isinstance(telefon_numaralari, list):
        konsol.print(f"[bold magenta]{json_ver(telefon_numaralari)}[/] [green]Kayıt Edildi..[/]")
        konsol.print(f"[bold magenta]{tablo_ver(telefon_numaralari)}[/] [green]Kayıt Edildi..[/]")
        konsol.print(f"[bold magenta]{vcf_ver(telefon_numaralari)}[/] [green]Kayıt Edildi..[/]")
    else:
        print(telefon_numaralari)