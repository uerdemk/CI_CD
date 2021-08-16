import paramiko
import os
import sys
import json
import shutil
import re
import stdiomask
from scp import SCPClient

user_name = "deneme"
password = "deneme"

#user_name = input("KULLANICI ADI = ")
#password = stdiomask.getpass(prompt='SIFRE = ')

path_original = os.getcwd()

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

while(1):
    os.chdir(path_original)
    ssh = createSSHClient("10.42.100.52", "22", user_name, password)

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

                with SCPClient(ssh.get_transport()) as scp:
                    for k in range(len(Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"])):
                        path_original_yazilim_alt3 = os.getcwd() + "\\" + Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_group"]
                        if not os.path.exists(path_original_yazilim_alt3):
                            os.makedirs(path_original_yazilim_alt3)
                            print(path_original_yazilim_alt3 + " isimli klasor yaratıldı...")
                        os.chdir(path_original_yazilim_alt3)
                        print(path_original_yazilim_alt3 + " klasorune konfig dosyaları oluturuluyor")
                        #path = "C:/TAITAI/TAI/SYY/SYY_AnkaS/config/"
                        path = "C:/TAI TAI/TAI/SYY/SYY_AnkaS/config/"
                        print(path)
                        scp.get(path, recursive=True)
                        #scp.get(Konfig_json["device_to_config"][t]["sw"][l]["sw_detail"][k]["sw_remote_path"], recursive=True)
                        os.chdir(path_original_yazilim_alt2)
    except Exception(e):
        print(e)

    a = 1
    while(a):
            print("   ")
            fake = input("Programi kapatmak icin '1'e, yeni islem icin herhangi bir tusa basiniz...")
            print(fake)
            if fake == "1":
                sys.exit()
            a = 0



