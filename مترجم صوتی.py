import time
import shutil
import translate
from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import pygame
from translate import *
from pygame import mixer
import json
import requests
import wikipedia
import sqlite3 as msc
from playsound import playsound
import requests
import io

def bip2():
    con = msc.connect("bip_sond.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM bip_start WHERE id = 56")
    ahang2 = cur.fetchall()[0]
    print(ahang2)
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(ahang2[3]))
    pygame.mixer.music.play()
def STT2(Lang) :
    LN = ""
    if Lang == 1 :
        LN = 'fa-IR'
    elif Lang == 2 :
        LN = "en-US"

    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as sours:
            bip2()
            time.sleep(0.5)
            audio = r.listen(sours)
            command = r.recognize_google(audio, language=LN)
            print(command + "\n")
            return command

    except Exception as er:
        print(f"{er}\nخطا در اینترنت !!!")
def play_audio(file_path):
    print(file_path)
    pygame.init()
    File = f"{file_path}"
    for ad in range(3):
        mixer.init()
        mixer.music.load(File)
        mixer.music.play()
def API_TTS2(Text):
    try:
        # model_name = "vits male1 (best)" #"صدای آقا"
        model_name = "vits female (best)" #"صدای خانم"
        text = str(Text)
        response = requests.post("https://kamtera-persian-tts-coquitts.hf.space/run/predict",json={"data": [text, model_name]}).json()
        data = response["data"]
        url_token = data[0]['name']
        return url_token
    except Exception :
        print("\n" + "مشکل در اتصال یا سرعت کند اینترنت")
def download_file(Text):
    url_token = API_TTS2(Text)
    url = f"https://kamtera-persian-tts-coquitts.hf.space/file={url_token}"
    download_path = r'C:\Users\computer\Downloads'

    response = requests.get(url)

    if response.status_code == 200:
        # دریافت نام فایل از URL
        filename = os.path.basename(url)
        # ایجاد مسیر کامل برای ذخیره فایل
        file_path = os.path.join(download_path, filename)
        # ذخیره فایل
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"فایل با نام {filename} با موفقیت دانلود شد.")
    else:
        print("خطا در دریافت فایل.")
def change_name_and_run_sond():
    directory = r'C:\Users\computer\Downloads'
    wav_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if filename.endswith('.wav'):
                wav_files.append(filename)
    output_path = ""
    wav_file = wav_files[0]
    # print(wav_file)
    os.rename(f'C:\\Users\\computer\\Downloads\\{wav_file}', 'C:\\Users\\computer\\Downloads\\sp.wav')
    output_path = "C:\\Users\\computer\\Downloads\\sp.wav"
    playsound(output_path)
    time.sleep(3)
    shutil.move("C:\\Users\\computer\\Downloads\\sp.wav", "C:\\Users\\computer\\Desktop\\sp.wav")
def TTS2(lang, Text):
    Lang = ""
    if lang == 1 :
        Lang = "en"
    elif lang == 2 :
        Lang = "fa"


    if Lang == "fa" :
        download_file(Text)
        change_name_and_run_sond()

    elif Lang == "en" :
        text = Text
        engine = pyttsx3.init()
        # تنظیم جنس صدا
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # صدای زنانه
        engine.setProperty('rate', 180)  # تنظیم سرعت گفتار (اختیاری)

        engine.say(text)
        engine.runAndWait()
def Translatetor(Text, From) :
    langs = {"فارسی" : "fa", "عربی" : "ar", "english" : "en", "هندی (hindi)" : "in"}
    from_lang = ""
    to_lang = ""
    if From == 1 :
        from_lang = 'fa-IR'
        to_lang = 'en-US'
    elif From == 2 :
        from_lang = 'en-US'
        to_lang = 'fa-IR'



    text = Text
    # تبدیل متن به یک خط با حذف خطوط خالی
    one_line_text = ' '.join(text.splitlines())
    outpute = (translate.Translator(f"{to_lang}", f"{from_lang}").translate(one_line_text))
    print("\n\n" + f"{outpute}")
    return f"\n\n{outpute}"


    if len(str(outpute)) > 500 :
        print("طول متن بیش از 500 کاراکتر است و نمیتوان به زبان مقابل ترجمه کرد")
    else:
        print(str(outpute))



while True :
    zab = int(input("1 : از فارسی\n2 : from english\n >>>"))
    if zab in range(1, 3) :
        command = STT2(zab)
        Tr = Translatetor(command, zab)
        TTS2(zab, Tr)

    else:
        pass

