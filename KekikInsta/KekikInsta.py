# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import Session

class KekikInsta():
    def __init__(self, kull_adi:str, sifre:str):
        """Kullanıcı Adı ve Şifreniz ile Instagram'a Giriş Yapmanızı Sağlar

        Method:
            .telefon_ver
        """
        self.insta  = "https://instagram.com"
        self.oturum = Session()
        self.oturum.headers.update({"User-Agent": "Mozilla/5.0"})

        self.oturum.get(self.insta)
        self.oturum.headers.update({"X-CSRFToken": self.oturum.cookies["csrftoken"]})

        login_data = {
            "username"     : kull_adi,
            "enc_password" : f"#PWD_INSTAGRAM_BROWSER:0:0:{sifre}",
            "queryParams"  : "{}",
        }

        istek = self.oturum.post(f"{self.insta}/accounts/login/ajax/", data=login_data)

        self.oturum.headers.update({"X-CSRFToken": self.oturum.cookies["csrftoken"]})

        self.yetki = istek.json()

    @property
    def yetkilendirme(self):
        if "authenticated" in self.yetki:
            if self.yetki["authenticated"]:
                return self.oturum
            else:
                return "[!] - Şifre yanlış"
        elif self.yetki["two_factor_required"]:
            iki_asama_data = {
                "username"         : self.yetki["two_factor_info"]["username"],
                "verificationCode" : input(f"Sms Doğrulama Kodu ({self.yetki['two_factor_info']['obfuscated_phone_number']}) : "),
                "identifier"       : self.yetki["two_factor_info"]["two_factor_identifier"],
                "queryParams"      : '{"next": "/"}',
            }
            self.yetki.post(f"{self.insta}/accounts/login/ajax/two_factor/", data=iki_asama_data)
            self.yetki.headers.update({"X-CSRFToken": self.yetki.cookies["csrftoken"]})

            return self.yetki
        else:
            print(self.yetki)
            return "[!] - Bir şeyler yanlış gitti"

    @property
    def telefon_ver(self):
        if not isinstance(self.yetkilendirme, Session):
            return self.yetkilendirme

        veriler = self.oturum.get("https://z-p3.www.instagram.com/graphql/query/?query_hash=68b15837c4c60cf5bb0c3df17a4791f8&variables=%7B%7D").json()['data']['user']['contact_history']

        kisiler = []
        for veri in veriler:
            ad     = veri['first_name']
            soyad  = veri['last_name']
            tam_ad = f"{ad} {soyad or ''}".strip()
            numara = f"90{veri['raw_value']}" if veri['raw_value'].startswith('5') and len(veri['raw_value']) == 10 else veri['raw_value']

            if numara[0].isdigit():
                kisiler.append({
                    'kisi'     : tam_ad,
                    'telefon'  : f'+{numara}' if str(numara).startswith('90') else numara
                })
            else:
                for kisi in kisiler:
                    try:
                        kisi_adi, _ = kisi.values()
                        if kisi_adi == tam_ad:
                            kisi.update({'mail' : numara})
                            break
                    except ValueError:
                        pass

        essiz = [dict(sozluk)for sozluk in {tuple(liste_ici.items()) for liste_ici in kisiler}]
        a_z   = sorted(essiz, key=lambda sozluk: sozluk['kisi'])
        return a_z