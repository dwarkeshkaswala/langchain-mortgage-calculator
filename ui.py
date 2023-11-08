import streamlit as st
from assistant import *
from PIL import Image
from time import sleep

if 'thread_id' and 'uploaded_file' and 'assistant_id' and 'conversation_history' and 'file_id' not in st.session_state:
    st.session_state.assistant_id = []
    st.session_state.thread_id = []
    st.session_state.uploaded_file = []
    st.session_state.conversation_history = []
    st.session_state.file_id = []

def render_chat_interface(conversation_history):
    # print(conversation_history)
    for item in conversation_history:
        if item["role"] == "user":
            if item["message"] != "":
                # st.write(f"**You:** {item['message']}")
                st.markdown(f'<div style="background-color: #cceeff; padding: 10px; border-radius: 10px; text-align: right; margin: 5px 5px 5px 30%;">{item["message"]}</div>', unsafe_allow_html=True)
        elif item["role"] == "assistant":
            if item["message"] != "":
                # st.write(f"**Assistant:** {item['message']}")
                if item["type"] == "image_file":
                    content_bytes = item["message"]
                    import io
                    image_data = io.BytesIO(content_bytes)
                    image = Image.open(image_data)
                    st.image(image)
                else:
                    st.markdown(f'<div style="background-color: #f0e2e2; padding: 10px; border-radius: 10px; text-align: left; margin: 5px; max-width: 70%;">{item["message"]}</div>', unsafe_allow_html=True)
            
assistant_id = 'asst_rPoDakLcCCbsWASSlL1jRr3Z'
thread_id = 'thread_dMI4tDChMAxpGrs3exqrNjN2'

st.title('Custom GPTs using GPT4-Turbo')

st.sidebar.title('Required Inputs')
st.header(get_assistant_name(assistant_id))
st.sidebar.markdown('Please enter the following information to generate your custom GPT-4 model.')
# assistant_id = st.sidebar.text_input('Assistant ID')
# thread_id = st.sidebar.text_input('Thread ID')


if st.sidebar.button('Initialize'):
    if assistant_id:
        st.write(render_chat_interface(print_history(thread_id)))
        # st.write((print_history(thread_id)))
        st.session_state.assistant_id = assistant_id
        st.session_state.thread_id = thread_id        
    else:
        st.error('Please enter an assistant ID.')

prompt = st.chat_input('Prompt')
file_upload = st.checkbox('Upload a file')
file_id = None
 
if file_upload:
    uploaded_file = st.file_uploader("Choose a data file", accept_multiple_files=False)
    st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file:
    file_id = get_file_id(uploaded_file)
    st.session_state.file_id.append(file_id)

if prompt:
    msg, run = msg_to_assistant(prompt, assistant_id, thread_id, st.session_state.file_id)

    status = check_run_status(thread_id, run.id)
    st.session_state.conversation_history.append({"role": "user", "message": prompt})

    with st.spinner('Wait for it...'):
        while status != "completed":
            sleep(2)
            status = check_run_status(thread_id, run.id)
            print(status)
            if status == "failed":
                break
            elif status == "completed":
                render_chat_interface(print_history(thread_id))



    


