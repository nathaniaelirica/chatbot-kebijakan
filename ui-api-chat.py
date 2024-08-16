import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Chatbot Kebijakan Bea dan Cukai",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("Chatbot Kebijakan Bea dan Cukai")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Silakan bertanya mengenai kebijakan ekspor impor!",
        }
    ]

def stream_data(response_content):
    for word in response_content.split(" "):
        yield word + " "
        time.sleep(0.02)

prompt = st.chat_input("Ask a question")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"prompt": prompt}
            )

            if response.status_code == 200:
                response_data = response.json()
                response_stream = stream_data(response_data["response"])
                response_placeholder = st.empty()
                assistant_message_content = ""

                for chunk in response_stream:
                    assistant_message_content += chunk
                    response_placeholder.write(assistant_message_content)
                
                assistant_message = {"role": "assistant", "content": assistant_message_content}
            else:
                assistant_message = {"role": "assistant", "content": "Error: Unable to get response from the backend"}

            st.session_state.messages.append(assistant_message)