import os
from langchain import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, ConversationSummaryMemory,
                                                  ConversationBufferWindowMemory
                                                  )
import streamlit as st
from streamlit_chat import message
import tiktoken
from langchain.memory import ConversationTokenBufferMemory
import time

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

st.set_page_config(page_title="Chat GPT Lite", page_icon="💻")
st.markdown("<h1 style='text-align:center;'>How can I assist you.?</h1>",
            unsafe_allow_html=True)

st.sidebar.title("😎")
st.session_state['API_Key'] = st.sidebar.text_input(
    "What's your API Key..?", type="password")
summarise_button = st.sidebar.button(
    "Summarise the Conversation", key="summarise")


if summarise_button:
    summarise_placeholder = st.sidebar.write(
        "Nice chatting with you my Friend:\n\n"+st.session_state['conversation'].memory.buffer)
    st.session_state['messages'] = []

# os.environ["OPENAI_API_KEY"] = "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"


def getresponse(userInput, api_key):
    if st.session_state['conversation'] is None:
        llm = OpenAI(
            temperature=0,
            openai_api_key=api_key,
            model_name='text-davinci-003'
        )
        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )

    response = st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)
    return response


response_container = st.container()
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your Question goes here", key=input, height=100)
        submit_button = st.form_submit_button(label="Send")

        # if submit_button:
        #     st.session_state['API_Key'] == ''
        #     st.write("Please Enter You API Key")
        try:
            if submit_button:
                st.session_state['messages'].append(user_input)
                model_response = getresponse(
                    user_input, st.session_state['API_Key'])
                st.session_state['messages'].append(model_response)
                with response_container:
                    for i in range(len(st.session_state['messages'])):
                        if (i % 2) == 0:
                            message(st.session_state['messages'][i],
                                    is_user=True, key=str(i) + 'user')
                        else:
                            message(
                                st.session_state['messages'][i], key=str(i) + 'AI')

        except:
            st.write("Please Enter Your API Key in Sidebar")
            st.session_state['messages'] = []
            time.sleep(4)
            st.rerun()
            # else:
        #     st.write("Please Enter API Key")
            # st.write(st.session_state['messages'])
