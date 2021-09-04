import os
import sys
import json
import shutil
import pysftp
import stdiomask
from stat import S_ISDIR, S_ISREG

########################################################################################################################################
# Bu program Uzak cihaza bağlanıp, konfig(.json) dosyasındaki yazılım ve bilgileri kullanarak, ilgili yazılımlara ait konfigürasyon 
# dosyalarını, komutun çalıştırıldığı dizine çekmektedir.
# desing by UEKI
#######################################################################################################################################

myUsername = input("KULLANICI ADI = ") #kullanici adi girisi
#myPassword = input("Sifre: ") #sifre girisi
myPassword = stdiomask.getpass(prompt='SIFRE = ')
secret = myPassword

path_original = os.getcwd() #komutun calisma dizinini path_orginal degiskenine atiyor

cnopts = pysftp.CnOpts() # baglanti turu, default known_host kullanmasi icin alttaki degisken none yapilmistir.
cnopts.hostkeys = None

counter = int(0)

def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):  #fonksiyon stfp modulü kullanir ve remotedir, localdir olmak uzere iki degisken girilebilir.
    global counter
    for entry in sftp.listdir_attr(remotedir): # baglandigimiz remotedir klasorundeki eleman kadar donecek for dongusu
        remotepath = remotedir + "/" + entry.filename # remotepath degiskeni, remotedir yoluna remotedir yolundaki ilk eleman eklenerek guncelleniyor. path olusturdugu icin araya / atilmis.
        localpath = os.path.join(localdir, entry.filename) # yukardaki islemin aynisi, localpath degiskeni localdir+filename ile olusturuluyor.
        mode = entry.st_mode # dosya turunu mode degiskenine atiyor.
        if S_ISDIR(mode): #mode degiskeni bir klasör ise giriyor if icine.
            try:
                os.mkdir(localpath) #localpath yolunu tamamlayacak klasoru olusturur.
            except IOError:
                print("#########################################")
                print("Klasorler olusturulurken problem ile karsilasildi.")
                input("Devam etmek icin ENTER'a basiniz..")
                sys.exit()
            get_r_portable(sftp, remotepath, localpath, preserve_mtime) # recursive fonksiyon oldugu icin fonksiyonun sonucu fonksiyona tekrar gonderiliyor.
        elif S_ISREG(mode): # mode degiskeni regular file ise
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime) # get methodu ile dosyalari cekiyor. Ayrica sftp.put ile istedigimiz dosyalari aktarabiliriz.
            counter +=1
            print("##########Yukleniyor..#################### "+ remotepath)
    return counter

secim = int(input("1- A\n2- S\n3- I\n4- J\n5- D\n6- T\nSeciminiz = "))
if secim == 1:
    try:
        with open('A_cihazlar.json') as Konfig:
            Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
    except IOError:
        print("#########################################")
        print(
            "Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        print("#########################################")
        a = int(input("Tekrar denemek icin 1'e, Programi kapatmak icin herhangi bir tusa basip ENTER'a basiniz... : "))
        if a == 1:
            print("#########################################")
            print("Ayar Dosyalari yukleniyor..")
            with open('A_cihazlar.json') as Konfig:
                Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
        else:
            print("#########################################")
            print("PROGRAM KAPATILIYOR.")
            input("Devam etmek icin ENTER'a basiniz..")
            sys.exit()
if secim == 2:
    try:
        with open('S_cihazlar.json') as Konfig:
            Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
    except IOError:
        print("#########################################")
        print(
            "Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        print("#########################################")
        a = int(input("Tekrar denemek icin 1'e, Programi kapatmak icin herhangi bir tusa basip ENTER'a basiniz... : "))
        if a == 1:
            print("#########################################")
            print("Ayar Dosyalari yukleniyor..")
            with open('S_cihazlar.json') as Konfig:
                Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
        else:
            print("#########################################")
            print("PROGRAM KAPATILIYOR.")
            input("Devam etmek icin ENTER'a basiniz..")
            sys.exit()
if secim == 3:
    try:
        with open('I_cihazlar.json') as Konfig:
            Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
    except IOError:
        print("#########################################")
        print(
            "Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        print("#########################################")
        a = int(input("Tekrar denemek icin 1'e, Programi kapatmak icin herhangi bir tusa basip ENTER'a basiniz... : "))
        if a == 1:
            print("#########################################")
            print("Ayar Dosyalari yukleniyor..")
            with open('I_cihazlar.json') as Konfig:
                Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
        else:
            print("#########################################")
            print("PROGRAM KAPATILIYOR.")
            input("Devam etmek icin ENTER'a basiniz..")
            sys.exit()
if secim == 4:
    try:
        with open('J_cihazlar.json') as Konfig:
            Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
    except IOError:
        print("#########################################")
        print(
            "Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        print("#########################################")
        a = int(input("Tekrar denemek icin 1'e, Programi kapatmak icin herhangi bir tusa basip ENTER'a basiniz... : "))
        if a == 1:
            print("#########################################")
            print("Ayar Dosyalari yukleniyor..")
            with open('J_cihazlar.json') as Konfig:
                Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
        else:
            print("#########################################")
            print("PROGRAM KAPATILIYOR.")
            input("Devam etmek icin ENTER'a basiniz..")
            sys.exit()
if secim == 5:
    try:
        with open('D_cihazlar.json') as Konfig:
            Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
    except IOError:
        print("#########################################")
        print(
            "Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        print("#########################################")
        a = int(input("Tekrar denemek icin 1'e, Programi kapatmak icin herhangi bir tusa basip ENTER'a basiniz... : "))
        if a == 1:
            print("#########################################")
            print("Ayar Dosyalari yukleniyor..")
            with open('D_cihazlar.json') as Konfig:
                Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
        else:
            print("#########################################")
            print("PROGRAM KAPATILIYOR.")
            input("Devam etmek icin ENTER'a basiniz..")
            sys.exit()
if secim == 6:
    try:
        with open('T_cihazlar.json') as Konfig:
            Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
    except IOError:
        print("#########################################")
        print(
            "Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        print("#########################################")
        a = int(input("Tekrar denemek icin 1'e, Programi kapatmak icin herhangi bir tusa basip ENTER'a basiniz... : "))
        if a == 1:
            print("#########################################")
            print("Ayar Dosyalari yukleniyor..")
            with open('T_cihazlar.json') as Konfig:
                Konfig_json = json.load(Konfig)  # Konfig bilgileri yukleniyor.
        else:
            print("#########################################")
            print("PROGRAM KAPATILIYOR.")
            input("Devam etmek icin ENTER'a basiniz..")
            sys.exit()
a = 1
while (a):
    os.chdir(path_original) # ilk komutun gerceklestigi path_original pathine gidiyor.
    path_original_yazilim = os.getcwd() + "\yazilim_konfig" # bu degiskende, komutun calistigi dosya yoluna, yazilim_konfig ekleyerek yeni yol olusturuyor.
    if os.path.exists(path_original_yazilim): #degiskendeki yol varsa if'e giriyor. asagidaki komutta fazlalıklari temizleyecek
        shutil.rmtree(path_original_yazilim) #path_orjinal_yazilim degiskeni disinda kalan klasorleri temizliyor.
        print(path_original_yazilim + " isimli klasor silindi...")
        os.makedirs(path_original_yazilim) #path_orginal_yazilim dosya yolunda olmasi gereken klasorleri olusturuyor.
        print(path_original_yazilim + " isimli klasor yaratıldı...")
    else:
        os.makedirs(path_original_yazilim) #path_orginal_yazilim dosya yolunda olmasi gereken klasorleri olusturuyor.
        print(path_original_yazilim + " isimli klasor yaratıldı...")

    os.chdir(path_original_yazilim) #yukarida remotepath klasor yapisini birebir olusturdu, ve burada icine giriyor.

    try:
        for t in range(len(Konfig_json["device_to_config"])): # device_to_config ayarlari sayisinca donen bir dongu.
            path_original_yazilim_alt1 = path_original_yazilim + "/" + Konfig_json["device_to_config"][t]["device"]
            #Konfig dosyasindan aldigi ip verilerini kullanarak yeni path olusturuyor.
            if not os.path.exists(path_original_yazilim_alt1): #if not koşulu ile yeni olusturudgu path yoksa islem yapıyor.
                os.makedirs(path_original_yazilim_alt1) #if kosulundaki path yoksa, klasorleri olusturdugu komut.
                print(path_original_yazilim_alt1 + " isimli klasor yaratıldı...")
            os.chdir(path_original_yazilim_alt1) #yeni olusturdugu path icine giriyor.

            for l in range(len(Konfig_json["device_to_config"][t]["sw"])): #device_to_config ayarlari icerisindeki "sw" konfigurasyon sayisinca donen bir for dongusu.
                path_original_yazilim_alt2 = path_original_yazilim_alt1 + "/" + Konfig_json["device_to_config"][t]["sw"][l]["sw_name"]
                #sw_name verilesini kullanarak yeni path olusturdu.
                if not os.path.exists(path_original_yazilim_alt2): #yukarida oldugu gibi path yoksa klasörleri olusturarak path'i tamamlayacak.
                    os.makedirs(path_original_yazilim_alt2) # path'i tamamlamak icin gerekli klasorleri olusturdu.
                    print(path_original_yazilim_alt2 + " isimli klasor yaratıldı...")
                os.chdir(path_original_yazilim_alt2) # yeni olusturdugu path icerisinde girdi.


                for k in range(len(Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"])): #sw_detail'deki ayar sayisi kadar donen dongu.
                    path_original_yazilim_alt3 = os.getcwd() + "\\" + Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_group"]
                    #yeni ayarlar icin yeni path olusturdu.
                    if not os.path.exists(path_original_yazilim_alt3): #yukarida oldugu gibi path yoksa klasörleri olusturarak path'i tamamlayacak.
                        os.makedirs(path_original_yazilim_alt3)
                        print(path_original_yazilim_alt3 + " isimli klasor yaratıldı...")
                    os.chdir(path_original_yazilim_alt3) #yeni path icine girdi.
                    print(path_original_yazilim_alt3 + " klasorune konfig dosyaları oluturuluyor")
                    try:
                        with pysftp.Connection(host=Konfig_json["device_to_config"][t]["ip"], username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
                            # device_to_config'te bulunan ip bilgisine ftp baglantisi kurdu.
                            remoteFilePath = Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_remote_path"]  # uzak software dosya yolunu remoteFilePath degiskenine atadi.
                            get_r_portable(sftp, remoteFilePath, os.getcwd(), preserve_mtime=False)  # yukarida dosyalari ceken recursive fonksiyonumuza remoteFilePath, localPath(os.getcwd) degiskenlerini yolladi.
                        os.chdir(path_original_yazilim_alt2)
                    except IOError:
                        print("#########################################")
                        print(Konfig_json["device_to_config"][t]["device"] + " CIHAZA BAGLANTI SAGLANAMADI!!!!!")  # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
                        print("#########################################")

        a = 0
    except IOError:
        print("Kullanici Adinin, Sifrenin ve ayar dosyasindaki IP'lerin dogru oldugundan emin olunuz! ")
        print("#########################################")
        print("PROGRAM KAPATILACAK...")
        input("Devam etmek icin ENTER'a basiniz..")
        a = 0
        sys.exit()


print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Toplam " + str(counter) + " ayar dosyasi kopyalandi.")
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
input("Programi kapatmak ENTER'a basiniz...")
