# pip install -qU langchain-ollama
# pip install langchain
# pip install streamlit

import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate

st.title(":brain: MY GPT")
model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434/")
system_message = SystemMessagePromptTemplate.from_template("You are Suzy, an AI assistant that Communicate in a casual, friendly, and conversational tone, mixing light humor and natural expressions to make interactions feel more personal and engaging. Act less like a rigid assistant and more like a collaborative partner who suggests ideas proactively, uses humor to lighten up the conversation, and provides value without being overly formal or repetitive. Blend professionalism with fun to create a vibe that's approachable and helpful while still offering thoughtful insights and actionable suggestions.")

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat messages from history on app rerun
for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_response(chat_history):
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    chain = chat_template | model | StrOutputParser()
    response = chain.invoke({})
    return response

def get_history():
    chat_history =[system_message]
    for chat in st.session_state['chat_history']:
        prompt = HumanMessagePromptTemplate.from_template(chat['content'])
        chat_history.append(prompt)

        ai_message = AIMessagePromptTemplate.from_template(chat['content'])
        chat_history.append(ai_message)

    return chat_history

# React to user input
if prompt := st.chat_input("How can I help you?"):
    HumanMessagePromptTemplate.from_template(prompt)
    chat_history = get_history()
    chat_history.append(prompt)
        

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state['chat_history'].append({"role": "user", "content": prompt})
    
    with st.spinner("Generating response..."):
        response = generate_response(chat_history)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state['chat_history'].append({"role": "assistant", "content": response})
