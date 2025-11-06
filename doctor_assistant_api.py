"""
we will create our api with fastapi
"""


"""
BaseModel is a core component of Pydantic, used for defining and validating data models. 
It plays a crucial role in FastAPI's data handling, ensuring type safety and validation
"""

#backend and ui libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

#libraries to make communication with system files
import os
from dotenv import load_dotenv
from typing import Dict

app = FastAPI(title = "Doctor Assistant API")

#langchain's modules
from langchain_google_genai import ChatGoogleGenerativeAI #to use gemini with the power of langchain
from langchain.memory import ConversationBufferMemory # Storage box that holds chat history
from langchain.chains import ConversationChain # Engine that uses this storage to have conversations

#just ignore the warnings 
import warnings
warnings.filterwarnings("ignore")

# load environmental variables (e.g. api)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.7
)

# 2. memory (we store it in a data structure)
user_memories: Dict[str, ConversationBufferMemory] = {}


# request and response schemes (classes -to create object with it-)

#request(input of the chat or the prompt)
class ChatRequest(BaseModel):
    name: str
    age: int
    message: str

#response(output or answer)
class ChatResponse(BaseModel):
    response: str

# 3. chat endpoint with asynchronous web service (i will also try https version )
"""
@ is a decorator enables us to call this function's decorators before.
it using for extend its functionality
"""
@app.post("/chat",response_model = ChatResponse)
# search about async
async def chat_with_doctor(request : ChatRequest): # it takes the input asynchronously 
    # we should use try except for handle the errors that we cannot see
    try:
        #if there is a memory, fetch it. otherwise create a new memory
        if request.name not in user_memories:
            user_memories[request.name] =ConversationBufferMemory(return_messages=True)

        #ChatRequest class's name variable (we will use it)
        memory = user_memories[request.name]

        #create an intro message for greet the guest :)
        # Writing the intro by hand is more cost-effective.
        if len(memory.chat_memory.messages) == 0:
            intro = (
                f"Sen her tıp ve diş hekimliği alanında bilgi sahibi, uzaktan teşhise yardımcı bir doktor asistanısın. Hasta {request.name}, {request.age} yaşında. "
                "Sağlık sorunları hakkında konuşmak istiyor. "
                "Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismiyle hitap et."
                " Hastayı bıktırmadan, kısa ve öz cevaplar ver. Doktor gibi cevap ver. "
            )
            #Full name: langchain_core.chat_history.BaseChatMessageHistory.add_user_message
            memory.chat_memory.add_user_message(intro)
        
        #combine llm with the memory with the CHAIN
        our_conversation = ConversationChain(llm = llm, memory=memory,verbose=False)
        bot_reply = our_conversation.predict(input = request.message)

        #print the stored memory of the chat to the screen
        print(f"\n Memory: ")
        # make an intro message (search about where memory.chat_memory.messages called from)
        for index, message in enumerate(memory.chat_memory.messages, start=1):
            #02d => 01th,02nd,03rd,04th,05.,06...
            print(f"{index:02d}.{message.type.upper()}: {message.content}" )
            """
            if messagelower() in ["exit", "quit", "çık", "cik", "kapat"]: # kullanıcı "exit" yazarsa döngüden çık
                print("Allah şifa versin, görüşmek üzere!")
                print("Çıkılıyor...")
                break
            """
        print("--------------------------------------------------------------")

        return ChatResponse(response = bot_reply)

    except Exception as e:
        #to debugging
        raise HTTPException(status_code=500,detail=str(e))

    

