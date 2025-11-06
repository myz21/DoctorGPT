import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module='langchain')

# Load environment variables
load_dotenv()

def create_llm(api_key=None, model=None, temperature=0.7):
    """
    Büyük dil modeli nesnesi oluşturur.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key 
    )

def initialize_session_state():
    """Initialize session state variables"""
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'memory' not in st.session_state:
        st.session_state.memory = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {'name': '', 'age': ''}
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False

def setup_conversation(name, age):
    """Setup conversation chain with user info"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("GEMINI_API_KEY environment variable bulunamadı!")
        return False
    
    # Create memory and conversation
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
    st.session_state.conversation = ConversationChain(
        llm=create_llm(api_key=api_key), 
        memory=st.session_state.memory, 
        verbose=False
    )
    
    # Add intro to memory
    intro = (
        f"Sen her tıp ve diş hekimliği alanında bilgi sahibi, bir doktor asistanısın. Hasta {name}, {age} yaşında. "
        "Sağlık sorunları hakkında konuşmak istiyor. "
        "Yaşına uygun dikkatli ve nazik tavsiyeler ver; ismiyle hitap et."
        " Hastayı bıktırmadan, kısa ve öz cevaplar ver. Doktor gibi cevap ver. "
    )
    
    st.session_state.memory.chat_memory.add_user_message(intro)
    st.session_state.user_info = {'name': name, 'age': age}
    st.session_state.initialized = True
    
    # Add welcome message to chat history
    welcome_msg = f"Merhaba {name}, ben Doktor Asistanı. Size nasıl yardımcı olabilirim?"
    st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})
    
    return True

def main():
    st.set_page_config(
        page_title="Doktor Asistanı",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Doktor Asistanı")
    st.markdown("---")
    
    initialize_session_state()
    
    # Sidebar for user information
    with st.sidebar:
        st.header("👤 Hasta Bilgileri")
        
        if not st.session_state.initialized:
            with st.form("user_info_form"):
                name = st.text_input("Adınız:", placeholder="Örn: Ahmet")
                age = st.text_input("Yaşınız:", placeholder="Örn: 25")
                submitted = st.form_submit_button("Başlat")
                
                if submitted:
                    if name.strip() and age.strip():
                        if setup_conversation(name.strip(), age.strip()):
                            st.success("Konuşma başlatıldı!")
                            st.rerun()
                    else:
                        st.error("Lütfen ad ve yaş bilgilerini giriniz!")
        else:
            st.success("✅ Konuşma aktif")
            st.write(f"**Ad:** {st.session_state.user_info['name']}")
            st.write(f"**Yaş:** {st.session_state.user_info['age']}")
            
            if st.button("🔄 Yeni Konuşma", type="secondary"):
                # Reset session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Hafıza Durumu")
        if st.session_state.memory:
            message_count = len(st.session_state.memory.chat_memory.messages)
            st.write(f"Toplam mesaj: {message_count}")
        
        # Show memory details in expander
        if st.session_state.memory and st.session_state.memory.chat_memory.messages:
            with st.expander("🧠 Hafıza Detayları"):
                for idx, msg in enumerate(st.session_state.memory.chat_memory.messages, 1):
                    st.text(f"{idx:02d}. {msg.type.upper()}: {msg.content[:100]}...")
    
    # Main chat interface
    if not st.session_state.initialized:
        st.info("👈 Lütfen önce sol panelden ad ve yaş bilgilerinizi giriniz.")
        st.markdown("""
        ### 🩺 Doktor Asistanı Hakkında
        - Bu asistan sağlık konularında genel bilgi verir
        - Profesyonel tıbbi tavsiye yerine geçmez
        - Ciddi durumlar için mutlaka bir doktora başvurun
        """)
    else:
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="👨‍⚕️"):
                        st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Sağlık sorunuz nedir?")
        
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Display user message immediately
            with st.chat_message("user", avatar="👤"):
                st.write(user_input)
            
            # Get response from conversation chain
            with st.chat_message("assistant", avatar="👨‍⚕️"):
                with st.spinner("Doktor düşünüyor..."):
                    try:
                        response = st.session_state.conversation.predict(input=user_input)
                        st.write(response)
                        
                        # Add assistant response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        st.error(f"Hata oluştu: {str(e)}")
                        st.write("Üzgünüm, bir sorun yaşadım. Lütfen tekrar deneyin.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "⚠️ Bu asistan sadece genel bilgi amaçlıdır. Ciddi sağlık sorunları için doktorunuza başvurun."
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()