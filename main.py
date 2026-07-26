import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
st.set_page_config(page_title="OmniChat AI", page_icon="💬")

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