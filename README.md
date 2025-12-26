# Kriptoloji Projesi  
## AES – DES – RSA | Kütüphaneli & Manuel Şifreleme  
## İstemci–Sunucu Haberleşmesi & Wireshark Analizi

Bu proje, klasik ve modern kriptografi algoritmalarını kullanarak **şifreli istemci–sunucu haberleşmesini** uygulamalı olarak gerçekleştirmeyi amaçlamaktadır.  
AES, DES ve RSA algoritmaları hem **mevcut kriptografi kütüphaneleri** kullanılarak hem de **manuel (kütüphanesiz)** yaklaşımla ele alınmıştır.  
Ayrıca ağ üzerinden iletilen şifreli veriler **Wireshark** kullanılarak analiz edilmiştir.

> **Not:** Bu projede RSA, simetrik şifreleme yerine **anahtar dağıtımı amacıyla** kullanılmaktadır.

---

## Projenin Amacı

Bu çalışmanın temel amaçları şunlardır:

- Simetrik (AES, DES) ve asimetrik (RSA) şifreleme algoritmalarının **birlikte kullanımını** göstermek
- Kütüphaneli ve manuel şifreleme yaklaşımları arasındaki **performans ve çıktı farklarını** gözlemlemek
- Şifreli verinin ağ üzerindeki görünümünü **Wireshark ile analiz etmek**
- Kriptografinin gerçek zamanlı istemci–sunucu sistemlerindeki etkisini uygulamalı olarak incelemek

---

## Desteklenen Algoritmalar

### Klasik Şifreleme Algoritmaları
- Caesar Cipher  
- Substitution Cipher  
- Affine Cipher  
- Vigenere Cipher  
- Playfair Cipher  
- Rail Fence Cipher  
- Columnar Transposition Cipher  
- Hill Cipher (2×2 matris)  
- Polybius Cipher  
- Pigpen Cipher  
- ROT (Spiral Transposition)

Bu algoritmalar hem **şifreleme** hem **deşifreleme** modunda ayrı sayfalarda çalışmaktadır.

---

### Modern Kriptografi

#### Kütüphaneli
- **AES-128**
- **DES**
- **RSA** (PyCryptodome kullanılarak)

#### Manuel (Kütüphanesiz – Eğitim Amaçlı)
- AES (sadeleştirilmiş round yapısı)
- DES (sadeleştirilmiş Feistel yapısı)

> Manuel algoritmalar gerçek sistemler için güvenli değildir,  
> **eğitim ve algoritma mantığını kavrama** amacıyla geliştirilmiştir.

---

## İstemci–Sunucu Haberleşme Yapısı

- Backend: **Flask + Flask-SocketIO**
- Frontend: **HTML / CSS / JavaScript**
- Haberleşme: **WebSocket (Socket.IO)**

### Secure Chat Akışı

1. İstemci mesajı AES veya DES ile şifreler
2. Simetrik anahtar RSA **public key** ile şifrelenir
3. Sunucu RSA **private key** ile anahtarı çözer
4. Mesaj AES/DES ile çözülür
5. Şu bilgiler istemciye geri gönderilir:
   - Şifreli metin
   - Çözülmüş metin
   - RSA işlem süresi (ms)
   - Simetrik şifreleme süresi (ms)

---

## Performans Karşılaştırması

- AES ve DES işlemleri **çok hızlıdır**
- RSA işlemleri **daha yavaştır** ve daha büyük veri üretir
- Manuel algoritmalar, kütüphaneli versiyonlara göre:
  - Daha yavaş
  - Daha az güvenli
  - Ancak öğretici

---

## Wireshark Analizi

### Amaç
- Şifreli mesajların ağ üzerinde **okunamaz olduğunu göstermek**
- AES, DES ve RSA paket boyutlarını karşılaştırmak

### Uygulama Adımları
1. Wireshark çalıştırılır
2. Wi-Fi veya Ethernet arayüzü seçilir
3. Filtre uygulanır:
   ```text
   tcp.port == 5000
4. Secure Chat üzerinden mesaj gönderilir
5. TCP paketlerinin payload alanı incelenir

## Kurulum

### Projeyi Klonla
git clone https://github.com/fatmanurzb/classic2.git
cd classic2

### Sanal Ortam Oluştur
python -m venv .venv
.venv\Scripts\Activate.ps1

### Gerekli Paketleri Yükle
pip install flask flask-socketio pycryptodome

### Çalıştırma
python app.py


## Proje Yapısı (Özet)

<img width="389" height="507" alt="image" src="https://github.com/user-attachments/assets/616e7330-4a0b-464a-b206-fe59704f68a9" />