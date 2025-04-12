# Kullanıcı Adı OSINT Aracı

Bu araç, belirli bir kullanıcı adını çeşitli sosyal medya platformlarında ve web sitelerinde arayarak, bu kullanıcı adına ait hesapları bulmaya yardımcı olur. Aynı zamanda, mümkün olduğunda bu hesaplara ait profil bilgilerini (isim, konum, biyografi vb.) çıkarmaya çalışır.

## Özellikler

- 20+ popüler platformda kullanıcı adı kontrolü
- Sosyal medya profillerinden kişisel bilgileri çıkarma:
  - İsim, soyisim
  - Biyografi
  - Konum
  - Takipçi ve takip edilen sayıları
  - Forum profil bilgileri (üyelik tarihi, mesaj sayısı, vb.)
- Bulunan isim bilgilerine göre muhtemel alternatif kullanıcı adlarını önerme
- Bulunan isim ve soyisim bilgileri ile doğrudan web'de arama yapma
- Google, LinkedIn, Facebook ve Twitter'da isim soyisim araması
- Multithreading ile hızlı tarama
- Renkli konsol çıktısı
- Sonuçları JSON formatında kaydetme

## Kurulum

1. Gerekli paketleri yükleyin:
```
pip install -r requirements.txt
```

## Kullanım

Temel kullanım:
```
python username_osint.py <kullanıcı_adı>
```

Sonuçları özel bir dosyaya kaydetmek için:
```
python username_osint.py <kullanıcı_adı> -o sonuclar.json
```

Bulunan isim bilgilerini kullanarak olası alternatif kullanıcı adlarını aramak için:
```
python username_osint.py <kullanıcı_adı> --similar
```

Bulunan isim bilgileriyle web'de arama yapmak için:
```
python username_osint.py <kullanıcı_adı> --search-web
```

Bulunan isim bilgileriyle web'de arama yapmak ve tarayıcıda açmak için:
```
python username_osint.py <kullanıcı_adı> --search-web --open-browser
```

## Örnek

```
python username_osint.py johndoe
```

Çıktı örneği:
```
[*] 'johndoe' kullanıcı adı için arama yapılıyor...
[+] Twitter: https://twitter.com/johndoe
[+] GitHub: https://github.com/johndoe
[-] Instagram: Kullanıcı bulunamadı
...

=== ÖZET ===
Kullanıcı adı: johndoe
Bulunan platformlar: 3

Bulunan Hesaplar:
- Twitter: https://twitter.com/johndoe
  Profil Bilgileri:
    name: John Doe
    bio: Software developer from New York
    location: New York, USA
    followers: 1523
    following: 432
...

Bulunan İsim Bilgileri:
- John Doe (Kaynak: Twitter)

[?] Bulunan isim bilgileri ile benzer hesapları aramak için:
    python username_osint.py johndoe --similar

[?] Bulunan isim bilgileri ile web araması yapmak için:
    python username_osint.py johndoe --search-web
    python username_osint.py johndoe --search-web --open-browser
```

Web Arama Örneği:
```
[*] Bulunan isimler için web araması yapılıyor...

[+] 'John Doe' (Twitter) için arama sonuçları:
  Google: https://www.google.com/search?q=John%20Doe
  LinkedIn: https://www.linkedin.com/search/results/all/?keywords=John%20Doe
  Facebook: https://www.facebook.com/search/top/?q=John%20Doe
  Twitter: https://twitter.com/search?q=John%20Doe
  Google (konum ile): https://www.google.com/search?q=John%20Doe%20New%20York%2C%20USA
```

## Desteklenen Platformlar

- Twitter
- Instagram
- GitHub
- Reddit
- Medium
- Quora
- Stackoverflow
- Steam
- Facebook
- Pinterest
- TikTok
- Soundcloud
- Twitch
- VKontakte
- Imgur
- Pastebin
- HackForums
- Cracked.to
- RaidForums
- LinuxForums
- Codecademy
- ...ve daha fazlası!

## Desteklenen Profil Bilgisi Çıkarma Özelliği Olan Platformlar

- Twitter: İsim, biyografi, konum, takipçi sayısı, takip edilen sayısı
- GitHub: İsim, biyografi, konum, şirket, e-posta, repository sayısı
- Instagram: İsim, biyografi, takipçi sayısı, takip edilen sayısı, gönderi sayısı, website
- Reddit: Kullanıcı adı, post karma, yorum karma, hesap yaşı
- Stackoverflow: İsim, itibar puanı, rozetler
- Steam: İsim, ülke, seviye, durum
- Forum siteleri: Kullanıcı adı, mesaj sayısı, üyelik tarihi, itibar puanı, kullanıcı grupları

## İsim ve Soyisim Bulma Özellikleri

- Sosyal medya platformlarından isim/soyisim bilgisi çıkarma
- Çıkarılan isim bilgileriyle muhtemel kullanıcı adları oluşturma
- İsim ve konum bilgilerini kullanarak Google ve diğer platformlarda arama
- Arama sonuçlarını doğrudan tarayıcıda açabilme

## Not

Bu araç, yalnızca yasal amaçlar için kullanılmalıdır. Başkalarının gizliliğine saygı gösterin ve elde ettiğiniz bilgileri kötüye kullanmayın. 