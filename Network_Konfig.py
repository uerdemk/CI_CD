from netmiko import ConnectHandler
from tkinter import *
import json
import os
import getpass
import stdiomask
import datetime

user_name = input("KULLANICI ADI = ")
password = stdiomask.getpass(prompt='SIFRE = ')
secret = password

ssh_fail = 0
stop = 0

path_original = os.getcwd()

while(1):
    os.chdir(path_original)
    content_list = os.listdir(os.getcwd())
    eq_json = ["*_cihazlari.json"] * 30
    index_json_file = 0
    file_exist = 0
    print("")
    print("Mevcut cihaz bilgi dosyaları...")
    for i in content_list:
        if "cihazlari.json" in i:
            print(int(index_json_file + 1), "-", i)
            eq_json[index_json_file] = i
            index_json_file = index_json_file + 1
            file_exist = 1

    if file_exist == 0:
        print("Cihaz bilgi dosyası bulunmamaktadir!!!")
        a = 1
        while (a):
            print("   ")
            fake = input("Programi kapatmak icin bir tusa basip ardindan ENTER'a basiniz...")
            a = 0
        sys.exit()
    #print(eq_json)

    eq_select = input("Numara giriniz, ardindan ENTER'a basiniz...")
    p = int(eq_select)-1
    print("Secilen cihazlar = ", eq_json[p])
    print("")

    try:
        with open(eq_json[p]) as Konfig:
        #with open('AKINCI_cihazlari.json') as Konfig:
        #with open('ANKA_S_cihazlari.json') as Konfig:
        #with open('konfig_saver_fw_forti.json') as Konfig:
            Konfig_json = json.load(Konfig)
    except:
        #print(eq_to_be_used)
        print("Cihaz IP'lerinin oldugu ", eq_json[p], " isimli dosyayi program ile ayni klasore koyunuz!!!")
        a = 1
        while (a):
            print("   ")
            fake = input("Programi kapatmak icin bir tusa basip ardindan ENTER'a basiniz...")
            a = 0
        sys.exit()

    def eq_declare(eq_IP, eq_OS):
        csc = {
            "device_type": eq_OS,
            "host": eq_IP,
            "port": 22,
            "username": user_name,
            "password": password,
            "secret": secret
        }
        return csc

    eq_list = [""] * len(Konfig_json["device_to_config"])

    print("                                                                                                               ")
    print("----------------------------------------SSH BAGLANTI KONTROLU--------------------------------------------------")
    print("                                                                                                                ")

    try:
        for t in range(len(Konfig_json["device_to_config"])):
            try:
                eq_list[t] = eq_declare(Konfig_json["device_to_config"][t]["ip"], Konfig_json["device_to_config"][t]["os"])
                net_connect = ConnectHandler(**eq_list[t])
                net_connect.enable()
                print("Baglanti saglandi...     {:<15} {:<15}".format(Konfig_json["device_to_config"][t]["ip"],
                                                                     Konfig_json["device_to_config"][t]["device"]))
            except:
                print("Baglanti PROBLEMI!!!     {:<15} {:<15}".format(Konfig_json["device_to_config"][t]["ip"], Konfig_json["device_to_config"][t]["device"]))
                #print("Baglanti PROBLEMI!!!!,", Konfig_json["device_to_config"][t]["ip"], ":", Konfig_json["device_to_config"][t]["device"])
    except EXCEPTION as e:
        print(e)

    a = 1
    while(a):
            print("   ")
            key = input("Devam etmek icin bir tusa basip ardindan ENTER tusuna basin...")
            a = 0

    print("                                                                                                               ")
    print("----------------------------------------SSH KOMUT GONDERIMI--------------------------------------------------")
    print("                                                                                                               ")

    path = os.getcwd() + "\konfig"
    if not os.path.exists(path):
        os.makedirs(path)
        print("'Konfig' isimli klasor yaratıldı...")
    os.chdir(path)
    print("'" + path + "'" + " klasorune konfig dosyaları oluturuluyor")

    try:
        for t in range(len(Konfig_json["device_to_config"])):
            try:
                eq_list[t] = eq_declare(Konfig_json["device_to_config"][t]["ip"], Konfig_json["device_to_config"][t]["os"])
                net_connect = ConnectHandler(**eq_list[t])
                net_connect.enable()
                #print("Baglanti saglandi!,", Konfig_json["device_to_config"][t]["ip"], ":", Konfig_json["device_to_config"][t]["device"])
                print("Baglanti saglandi        {:<15} {:<15}".format(Konfig_json["device_to_config"][t]["ip"],
                                                                      Konfig_json["device_to_config"][t]["device"]))
                try:
                    for command in range(len(Konfig_json["device_to_config"][t]["command"])):
                        output = net_connect.send_command(Konfig_json["device_to_config"][t]["command"][command], delay_factor=2)
                        print("             ", Konfig_json["device_to_config"][t]["command"][command])
                        with open(str(Konfig_json["device_to_config"][t]["device"] + "__" + str(Konfig_json["device_to_config"][t]["command"][command])), "+w") as file_name:
                            file_name.write(output)
                except EXCEPTION as e:
                    print("HATA")
            except:
                print("Baglanti PROBLEMI!!!     {:<15} {:<15}".format(Konfig_json["device_to_config"][t]["ip"],
                                                                      Konfig_json["device_to_config"][t]["device"]))
                #print("Baglanti PROBLEMI!!!!,", "SSH HATASI,", Konfig_json["device_to_config"][t]["ip"], ":", Konfig_json["device_to_config"][t]["device"])
    except EXCEPTION as e:
        print(e)

    a = 1
    while(a):
            print("   ")
            fake = input("Programi kapatmak icin '1'e, yeni islem icin herhangi bir tusa basiniz...")
            print(fake)
            if fake == "1":
                sys.exit()
            a = 0
