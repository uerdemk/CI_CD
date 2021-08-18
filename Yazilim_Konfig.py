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
myPassword = stdiomask.getpass(prompt='SIFRE = ') #sifre girisi

path_original = os.getcwd() #komutun calisma dizinini path_orginal degiskenine atiyor

cnopts = pysftp.CnOpts() # baglanti turu, default known_host kullanmasi icin alttaki degisken none yapilmistir.
cnopts.hostkeys = None

def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):  #fonksiyon stfp modulü kullanir ve remotedir, localdir olmak uzere iki degisken girilebilir.
    for entry in sftp.listdir_attr(remotedir): # baglandigimiz remotedir klasorundeki eleman kadar donecek for dongusu
        remotepath = remotedir + "/" + entry.filename # remotepath degiskeni, remotedir yoluna remotedir yolundaki ilk eleman eklenerek guncelleniyor. path olusturdugu icin araya / atilmis. 
        localpath = os.path.join(localdir, entry.filename) # yukardaki islemin aynisi, localpath degiskeni localdir+filename ile olusturuluyor.
        mode = entry.st_mode # dosya turunu mode degiskenine atiyor.
        if S_ISDIR(mode): #mode degiskeni bir klasör ise giriyor if icine.
            try:
                os.mkdir(localpath) #localpath yolunu tamamlayacak klasoru olusturur.
            except OSError:
                pass
            get_r_portable(sftp, remotepath, localpath, preserve_mtime) # recursive fonksiyon oldugu icin fonksiyonun sonucu fonksiyona tekrar gonderiliyor.
        elif S_ISREG(mode): # mode degiskeni regular file ise
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime) # get methodu ile dosyalari cekiyor. Ayrica sftp.put ile istedigimiz dosyalari aktarabiliriz.

while(1):
    os.chdir(path_original) # ilk komutun gerceklestigi path_original pathine gidiyor.
    try:
        with open('AKINCI_win_cihazlari.json') as Konfig:
            Konfig_json = json.load(Konfig) # Konfig bilgileri yukleniyor.
    except Exception(e):
        print("Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!") # try-except yapisina kullanilmis, sorun olursa uyari vermesi icin.
        a = 1
        while (a):
            print("   ")
            fake = input("Programi kapatmak icin bir tusa basip ardindan ENTER'a basiniz...")
            a = 0
        sys.exit()


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
            path_original_yazilim_alt1 = path_original_yazilim + "/" + Konfig_json["device_to_config"][t]["device"] + "_" + Konfig_json["device_to_config"][t]["ip"]
            #Konfig dosyasindan aldigi ip verilerini kullanarak yeni path olusturuyor.
            if not os.path.exists(path_original_yazilim_alt1): #if not koşulu ile yeni olusturudgu path yoksa islem yapıyor.
                os.makedirs(path_original_yazilim_alt1) #if kosulundaki path yoksa, klasorleri olusturdugu komut.
                print(path_original_yazilim_alt1 + " isimli klasor yaratıldı...")
            os.chdir(path_original_yazilim_alt1) #yeni olusturdugu path icine giriyor.

            for l in range(len(Konfig_json["device_to_config"][t]["sw"])): #device_to_config ayarlari icerisindeki "sw" konfigurasyon sayisince donen bir for dongusu.
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
                    with pysftp.Connection(host=Konfig_json["device_to_config"][t]["ip"], username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
                        #device_to_config'te bulunan ip bilgisine ftp baglantisi kurdu.
                        remoteFilePath = Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_remote_path"] # uzak software dosya yolunu remoteFilePath degiskenine atadi.
                        get_r_portable(sftp, remoteFilePath, os.getcwd(), preserve_mtime=False) #yukarida dosyalari ceken recursive fonksiyonumuza remoteFilePath, localPath(os.getcwd) degiskenlerini yolladi. 
                    os.chdir(path_original_yazilim_alt2) 
    except Exception as e:
        print(e)

    a = 1
    while(a):
            print("   ")
            fake = input("Programi kapatmak icin '1'e, yeni islem icin herhangi bir tusa basiniz...")#kullanicidan aldigi degeri fake degiskenine atadi.
            print(fake)
            if fake == "1": #fake=1 ise cikis komutu verdi. 
            a = 0
