import paramiko
import os
import sys
import json
import shutil
import pysftp
import stdiomask
from stat import S_ISDIR, S_ISREG

myUsername = input("KULLANICI ADI = ")
myPassword = stdiomask.getpass(prompt='SIFRE = ')

path_original = os.getcwd()

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):
    for entry in sftp.listdir_attr(remotedir):
        remotepath = remotedir + "/" + entry.filename
        localpath = os.path.join(localdir, entry.filename)
        mode = entry.st_mode
        if S_ISDIR(mode):
            try:
                os.mkdir(localpath)
            except OSError:
                pass
            get_r_portable(sftp, remotepath, localpath, preserve_mtime)
        elif S_ISREG(mode):
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

while(1):
    os.chdir(path_original)
    try:
        with open('AKINCI_win_cihazlari.json') as Konfig:
            Konfig_json = json.load(Konfig)
    except Exception(e):
        print("Cihaz ayarlarının oldugu dosyayi program ile ayni klasore koyunuz!!!")
        a = 1
        while (a):
            print("   ")
            fake = input("Programi kapatmak icin bir tusa basip ardindan ENTER'a basiniz...")
            a = 0
        sys.exit()


    path_original_yazilim = os.getcwd() + "\yazilim_konfig"

    if os.path.exists(path_original_yazilim):
        shutil.rmtree(path_original_yazilim)
        print(path_original_yazilim + " isimli klasor silindi...")
        os.makedirs(path_original_yazilim)
        print(path_original_yazilim + " isimli klasor yaratıldı...")
    else:
        os.makedirs(path_original_yazilim)
        print(path_original_yazilim + " isimli klasor yaratıldı...")

    os.chdir(path_original_yazilim)

    try:
        for t in range(len(Konfig_json["device_to_config"])):
            path_original_yazilim_alt1 = path_original_yazilim + "/" + Konfig_json["device_to_config"][t]["device"] + "_" + Konfig_json["device_to_config"][t]["ip"]
            if not os.path.exists(path_original_yazilim_alt1):
                os.makedirs(path_original_yazilim_alt1)
                print(path_original_yazilim_alt1 + " isimli klasor yaratıldı...")
            os.chdir(path_original_yazilim_alt1)

            for l in range(len(Konfig_json["device_to_config"][t]["sw"])):
                path_original_yazilim_alt2 = path_original_yazilim_alt1 + "/" + Konfig_json["device_to_config"][t]["sw"][l]["sw_name"]
                if not os.path.exists(path_original_yazilim_alt2):
                    os.makedirs(path_original_yazilim_alt2)
                    print(path_original_yazilim_alt2 + " isimli klasor yaratıldı...")
                os.chdir(path_original_yazilim_alt2)


                for k in range(len(Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"])):
                    path_original_yazilim_alt3 = os.getcwd() + "\\" + Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_group"]
                    if not os.path.exists(path_original_yazilim_alt3):
                        os.makedirs(path_original_yazilim_alt3)
                        print(path_original_yazilim_alt3 + " isimli klasor yaratıldı...")
                    os.chdir(path_original_yazilim_alt3)
                    print(path_original_yazilim_alt3 + " klasorune konfig dosyaları oluturuluyor")
                    with pysftp.Connection(host=Konfig_json["device_to_config"][t]["ip"], username=myUsername, password=myPassword,
                                           cnopts=cnopts) as sftp:
                        remoteFilePath = Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_remote_path"]
                        get_r_portable(sftp, remoteFilePath, os.getcwd(), preserve_mtime=False)
                    os.chdir(path_original_yazilim_alt2)
    except Exception as e:
        print(e)

    a = 1
    while(a):
            print("   ")
            fake = input("Programi kapatmak icin '1'e, yeni islem icin herhangi bir tusa basiniz...")
            print(fake)
            if fake == "1":
                sys.exit()
            a = 0
