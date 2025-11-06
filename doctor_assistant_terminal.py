"""
our ai model uses gemini 2.5 in the background
"""

#import necessary libraries
import os
from dotenv import load_dotenv #api için environment variable'ları güvenle yüklemek için
#from langchain.chat_models import ChatOpenAI #langchain ile gpt kullanmak için
from langchain_google_genai import ChatGoogleGenerativeAI #langchain ile gemini kullanmak için
from langchain.chains import ConversationChain #conversation chain oluşturmak için
from langchain.memory import ConversationBufferMemory #conversation memory için
from langchain.prompts import PromptTemplate #prompt template oluşturmak için

#load environment variables
load_dotenv() # .env dosyasındaki environment variable'ları yükle
api_key = os.getenv("GEMINI_API_KEY") # GEMINI_API_KEY environment variable'ını al

#gereksiz uyarıları kaldır
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='langchain')

# create_llm fonksiyonu, büyük dil modeli nesnesi oluşturur.
def create_llm(api_key=None, model=None, temperature=0.7):
    """
    Büyük dil modeli nesnesi oluşturur.
    model: kullanılacak model ismi.
    temperature: 0-1 arasında, cevabın kararlılığı.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key 
    )
    """
    #OPENAI ALTERNATİFİ
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=api_key
    )    
    """
    
# memory
memory = ConversationBufferMemory(return_messages = True)


# conversation
conversation = ConversationChain(llm= create_llm(api_key=api_key), 
                                 memory=memory, 
                                 verbose=True) #verbose=True, çıktıları gösterir.

name = input("Adiniz nedir? ") # kullanıcıdan ad al
age = input("Yasiniz nedir? ") # kullanıcıdan yaş al

# introyu elle yazmak maliyet açısından daha mantıklı.

'''
(sadece şakaydı)
intro = f"""Sen bir doktor asistanisin. Hastanın adı {name}, yasi {age}. "
    Saglik sorunlari hakkinda konusmak istiyor. "
    Ismiyle hitap et; yasina uygun tavsiyelerde bulun. "
    Sorularina nazikce, bir polymath uzman doktor gibi cevap ver. "
    Elesitrel bakis acisina sahip ol.
    Kısa ve öz cevaplar ver. """
'''

intro = (
    f"Sen bir doktor asistanısın. Hasta {name}, {age} yaşında. "
    "Sağlık sorunları hakkında konuşmak istiyor. "
    "Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismiyle hitap et."
    " Hastayı bıktırmadan, kısa ve öz cevaplar ver. Doktor gibi cevap ver. "
)

memory.chat_memory.add_user_message(intro) # belleğe kullanıcı mesajı ekle
print(f"Merhaba {name}, ben Doktor Asistanı. Size nasıl yardımcı olabilirim?") # başlangıç mesajı

#chatbot loop
# bellekte (memory.chat_memory.messages) 
# biriken konuşma geçmişinin ekrana yazdırılması için
while True:
    # hasta soru soruyor
    user_msg = input(f"{name}: ") # kullanıcıdan mesaj al
    if user_msg.lower() in ["exit", "quit", "çık", "cik", "kapat"]: # kullanıcı "exit" yazarsa döngüden çık
        print("Allah şifa versin, görüşmek üzere!")
        print("Çıkılıyor...")
        break
    # assistant cevap veriyor
    reply = conversation.predict(input=user_msg)
    print(f"Doktor Asistanı: {reply}") # chatbot'un cevabını yazdır

    # verilen cevabı belleğe ekle
    print("\nHafiza: ")
    for indexx, m in enumerate(memory.chat_memory.messages, start=1):
        print(f"{indexx:02d}. {m.type.upper()}: {m.content}")
    print("--------------------------------------------\n")
    
    """
    02d ifadesi, sayıyı iki basamaklı 
    (01, 02, 03 gibi) ve 
    başında sıfır olacak şekilde biçimlendirir.
    
    m.content Ne işe yarar?
    m nesnesinin (bu döngüde bir mesaj nesnesi) content (içerik) özelliğine erişir. Yani yazışmadaki gerçek metni getirir.
    Hangi kütüphane?
    Burada m nesnesi, büyük ihtimalle LangChain kütüphanesinin bir mesaj nesnesidir (örneğin, langchain.memory veya langchain.schema’dan).
    memory.chat_memory.messages yapısı, LangChain’in sohbet hafızası (Memory) sınıfından gelir.
    
    upper:  (ör: "human" → "HUMAN")
    """

