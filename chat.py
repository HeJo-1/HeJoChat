import socket
import threading
import random

def oda_kodu_olustur():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def sunucu_baslat():
    sunucu_ip = 'localhost'
    sunucu_port = 12345
    istemciler = []
    oda_kodu = oda_kodu_olustur()
    max_istemciler = int(input("Sohbet odasına izin verilen maksimum istemci sayısını girin: "))
    sunucu_nick = input("Bir nickname belirleyin: ")  # Sunucu nickname'i

    print(f"Sohbet Odası Kodu: {oda_kodu}")

    sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sunucu.bind((sunucu_ip, sunucu_port))
    sunucu.listen()

    print(f"Sunucu başlatıldı {sunucu_ip}:{sunucu_port}")

    def yayinla(mesaj, istemci_soketi=None):
        for istemci in istemciler:
            if istemci != istemci_soketi:
                try:
                    istemci.send(mesaj)
                except:
                    istemciler.remove(istemci)

    def istemciyi_yonet(istemci_soketi):
        try:
            isim = istemci_soketi.recv(1024).decode('utf-8')  # Kullanıcının ismini al
            print(f"{isim} bağlandı.")
            istemci_soketi.send("Hoş geldiniz!".encode('utf-8'))
            while True:
                mesaj = istemci_soketi.recv(1024)
                if not mesaj:
                    break
                print(f"{isim}: {mesaj.decode('utf-8')}")
                yayinla(f"{isim}: {mesaj.decode('utf-8')}".encode('utf-8'), istemci_soketi)
        except:
            istemciler.remove(istemci_soketi)
        finally:
            istemci_soketi.close()

    def mesaj_gonder():
        while True:
            mesaj = input(f"{sunucu_nick}: ")
            yayinla(f"{sunucu_nick}: {mesaj}".encode('utf-8'))

    def baglantilari_kabul_et():
        while True:
            if len(istemciler) < max_istemciler:
                istemci_soketi, istemci_adresi = sunucu.accept()
                print(f"Yeni bağlantı {istemci_adresi}")
                istemciler.append(istemci_soketi)
                thread = threading.Thread(target=istemciyi_yonet, args=(istemci_soketi,))
                thread.start()
            else:
                print("Maksimum istemci sayısına ulaşıldı, yeni bağlantılar kabul edilmiyor.")

    kabul_thread = threading.Thread(target=baglantilari_kabul_et)
    kabul_thread.start()

    gonder_thread = threading.Thread(target=mesaj_gonder)
    gonder_thread.start()

def istemci_baslat():
    istemci = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    oda_kodu_giris = input("6 haneli Oda Kodunu girin: ")

    try:
        istemci.connect(('localhost', 12345))
    except:
        print("Sunucuya bağlanılamadı.")
        return

    isim = input("Lütfen nickname giriniz: ")
    istemci.send(isim.encode('utf-8'))  # Kullanıcı ismini gönder

    def mesajlari_al():
        while True:
            try:
                mesaj = istemci.recv(1024).decode('utf-8')
                print(mesaj)
            except:
                print("Bir hata oluştu!")
                istemci.close()
                break

    def mesaj_gonder():
        while True:
            mesaj = input(f"{isim}: ")
            istemci.send(mesaj.encode('utf-8'))

    al_thread = threading.Thread(target=mesajlari_al)
    al_thread.start()

    gonder_thread = threading.Thread(target=mesaj_gonder)
    gonder_thread.start()

def ana():
    print('''

 ____ ____ ____ ____ ____ ____ ____ ____ 
||H |||e |||J |||o |||C |||h |||a |||t ||
||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|


''')
    rol = input("Oda oluşturmak için : 1\nOdaya katılmak için : 2\n").strip().lower()

    if rol == '1':
        sunucu_baslat()
    elif rol == '2':
        istemci_baslat()
    else:
        print("Geçersiz seçim. Lütfen 'sunucu' veya 'istemci' yazın.")

if __name__ == "__main__":
    ana()
