import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
st.set_page_config(page_title="OmniChat AI", page_icon="💬",layout="centered")
st.title("OmniChat AI 💬")
st.info("Select any free model from the sidebar to start chatting!")
available_models={
    "Google Gemini 2.5 Flash": "google/gemini-2.5-flash",
    "Google Gemma 4-26b-a4b": "google/gemma-4-26b-a4b-it:free",
    "Nvidia Nemotron 3 Ultra": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "Nvidia Nano Omni": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "Ling 3 Flash": "inclusionai/ling-3.0-flash:free",
    "Cohere: North Mini Code": "cohere/north-mini-code:free",
    "PoolSide Laguna S2.1": "poolside/laguna-s-2.1:free",
    "PoolSide Laguna XS2.1": "poolside/laguna-xs-2.1:free",
    "OpenAI: gpt-oss-20b": "openai/gpt-oss-20b:free",
    "Auto Free Router": "openrouter/free",
}

with st.sidebar:
    st.title("Model Configuration")
    selected_model = st.radio(label='Select a model', options=list(available_models.keys()))
    selected_model_id = available_models[selected_model]

    if st.button("Clear Conversation",use_container_width=True):
        st.session_state.chat_history = [
            AIMessage(content="Hello! I am powered by OpenRouter & LangChain, developed by Mohiuddin Mahady. How can I assist you today?")
        ]
        st.rerun()

    st.header("Developer Information")
    st.markdown("""
    **Mohiuddin Mahady**  
    *BSc in CSE*  
    Mymensingh Engineering College  
    *(Affiliated with Dhaka University)*
    """)
    col3, col4 = st.columns([1, 1])
    with col3:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/mohiuddin-mahady/", use_container_width=True)
    with col4:
        st.link_button("Github", 'https://www.github.com/mahady13', use_container_width=True)
    st.markdown("---")

@st.cache_resource
def get_llm(model_id):
    return ChatOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model=model_id,
        temperature=0.7,
        max_tokens=2000,
        default_headers={"HTTP-Referer": "https://localhost:8501/",'X-Title':'OmniChat AI'},
    )


def get_response(user_query, chat_history, selected_model_id):
    template = """
    You are a helpful assistant. Answer the user's question by considering the conversation history.

    chat_history:{chat_history}
    user_query:{user_query}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = get_llm(selected_model_id)
    chain = prompt | llm | StrOutputParser()
    output = chain.stream({
        "user_query": user_query,
        "chat_history": chat_history
    })
    return output
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[
        AIMessage(content="Hello! I am powered by OpenRouter & Langchain, developed by Mohiuddin Mahady. How can I assist you today?")
    ]

for message in st.session_state.chat_history:
    if isinstance(message,AIMessage):
        with st.chat_message('assistant'):
            st.write(message.content)

    elif isinstance(message,HumanMessage):
        with st.chat_message('user'):
            st.write(message.content)
if user_query:=st.chat_input("Type your message here"):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message('user'):
        st.markdown(user_query)

    with st.chat_message('assistant'):
        response=st.write_stream(get_response(user_query,st.session_state.chat_history,selected_model_id))
    st.session_state.chat_history.append(AIMessage(content=response))
