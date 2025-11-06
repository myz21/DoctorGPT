"""
instant chat with fastapi in the terminal
"""

import requests #Requests is a simple, yet elegant, HTTP library

API_URL = "http://127.0.0.1:8000/chat"

print("Merhaba, ben bir doktor asistanıyım. Size daha iyi hitap edebilmem için adınızı ve yaşınızı öğrenebilir miyim?")

name = input("Adınız: ")
age = int(input("Yaşınız: "))

#print(f"Merhaba {name}. Size nasıl yardımcı olabilirim?") 
print("(Sohbet basladi, cikmak için quit veya çıkış yazabilirsiniz.)")

while True:

    user_message = input(f"{name}: ")
    if user_message.lower() in ["exit", "quit", "çık", "cik", "kapat"]: # kullanıcı "exit" yazarsa döngüden çık
        print("Allah şifa versin, görüşmek üzere!")
        print("Çıkılıyor...")
        break

    # payload is the part of transmitted data that is the actual intended message
    # payload is sending to api
    payload = {
        "name": name,
        "age":age,
        "message": user_message
    }

    try:
        #send post request to fastapi server, wait for 30 secs
        #def post(url: Union[Text, bytes], data: _Data=..., json=..., **kwargs,timeout=...) 
        responsee = requests.post(API_URL,json=payload,timeout=30)

        # we can reach the server, everything is okay
        if responsee.status_code == 200:
            replyy = responsee.json()
            print(f"Doktor Asistanı: {replyy["response"]}")
        # we can reach the server but we have error inside fastapi application
        else:
            print("There's an error: ",responsee.status_code,responsee.text)
    #we cannot reach the server, timeout error will be raise
    except requests.exceptions.RequestException as e:
        print("Bağlantı hatası: ",e)