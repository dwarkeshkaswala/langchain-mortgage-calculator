import streamlit as st
from assistant import *
from PIL import Image
from datetime import datetime
from time import sleep
 
if 'thread_id' and 'uploaded_file' and 'assistant_id' and 'run' and 'conversation_history' and 'file_id' and 'tools' and 'is_gpt_loaded' and 'gpt_name' not in st.session_state:
    st.session_state.assistant_id = ""
    st.session_state.thread_id = ""
    st.session_state.uploaded_file = []
    st.session_state.conversation_history = []
    st.session_state.file_id = []
    st.session_state.tools = []
    st.session_state.gpt_name = ""
    st.session_state.is_gpt_loaded = False
    st.session_state.run = ""

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


#Sidebar
st.sidebar.title('Custom GPTs using GPT4-Turbo')

with st.sidebar.form("create_gpt_form"):
    st.markdown('Please enter the following information to generate your custom GPT-4 model.')

    gpt_name = st.text_input('Name of your GPT')
    gpt_instructions = st.text_area('Instructions for your GPT')
    use_codeinterpreter = st.checkbox('Code Interpreter')
    use_retrieval = st.checkbox('Retrieval')

    if use_codeinterpreter and use_retrieval:
        tools = [{"type": "code_interpreter"}, {"type": "retrieval"}]
    elif use_codeinterpreter:
        tools = [{"type": "code_interpreter"}]
    elif use_retrieval:
        tools = [{"type": "retrieval"}]
    else:
        tools = []
    
    submitted = st.form_submit_button("Create GPT")
    if submitted:
        assistant, thread = create_custom_assistant(gpt_name, gpt_instructions, tools)
        assistant_id = assistant.id
        thread_id = thread.id
        st.session_state.assistant_id = assistant_id
        st.session_state.thread_id = thread_id
        st.session_state.tools = tools

        print(f"Assistant ID: {assistant_id}")
        print(f"Thread ID: {thread_id}")

        st.success('GPT created successfully!')


all_assistants = list_assistants()

if all_assistants:
    st.sidebar.markdown('---')
    st.sidebar.title('Existing GPTs')
    for assistant in all_assistants:
        st.sidebar.write(assistant.name)
        st.sidebar.write(assistant.id)
        timestamp = assistant.created_at
        dt_object = datetime.fromtimestamp(timestamp)
        st.sidebar.write(dt_object)
        if st.sidebar.button('Use this GPT', key=assistant.id):
            st.session_state.gpt_name = assistant.name
            st.session_state.assistant_id = assistant.id
            st.header(get_assistant(assistant.id).name)
            st.success('GPT loaded successfully!')
            is_gpt_loaded = True
            st.session_state.is_gpt_loaded = is_gpt_loaded

        if st.sidebar.button('🗑️', key=f"delete_{assistant.id}"):
            # st.sidebar.error('Are you sure you want to delete this GPT?')
            deleted_assistant = delete_assistant(assistant_id=assistant.id)
            st.rerun()
        st.sidebar.markdown('---')
    
if st.session_state.is_gpt_loaded:
    prompt = st.chat_input("Say something")
    if prompt:
        user_msg = st.chat_message("user")
        assistant_msg = st.chat_message("assistant")
        user_msg.write(f"{prompt}")
        if st.session_state.thread_id:
            print(f"Thread ID: {st.session_state.thread_id}")
            msg, run = msg_to_assistant(prompt, st.session_state.assistant_id, st.session_state.thread_id, st.session_state.file_id)
            st.session_state.run = run
        else:
            thread_id = create_thread().id
            st.session_state.thread_id = thread_id
            print("Creating thread...")
            print(f"Thread ID: {st.session_state.thread_id}")
            # st.session_state.thread_id = "thread_2C8Py7B2g5mM3yfZhdaMcuyL"
            msg, run = msg_to_assistant(prompt, st.session_state.assistant_id, st.session_state.thread_id, st.session_state.file_id)
            st.session_state.run = run
        status = check_run_status(st.session_state.thread_id, run.id)
    
        with st.spinner('Wait for it...'):
            while status != "completed":
                sleep(2)
                status = check_run_status(st.session_state.thread_id, run.id)
                print(status)
                if status == "failed":
                    break
                elif status == "completed":
                    assistant_msg.write(f"{print_history(st.session_state.thread_id)[-1]['message']}")
                    break


# if st.sidebar.button('Initialize'):
#     if assistant_id:
#         st.write(render_chat_interface(print_history(thread_id)))
#         # st.write((print_history(thread_id)))
#         st.session_state.assistant_id = assistant_id
#         st.session_state.thread_id = thread_id        
#     else:
#         st.error('Please enter an assistant ID.')

# prompt = st.chat_input('Prompt')
# file_upload = st.checkbox('Upload a file')
# file_id = None
 
# if file_upload:
#     uploaded_file = st.file_uploader("Choose a data file", accept_multiple_files=False)
#     st.session_state.uploaded_file = uploaded_file

# if st.session_state.uploaded_file:
#     file_id = get_file_id(uploaded_file)
#     st.session_state.file_id.append(file_id)

# if prompt:
#     msg, run = msg_to_assistant(prompt, assistant_id, thread_id, st.session_state.file_id)

#     status = check_run_status(thread_id, run.id)
#     st.session_state.conversation_history.append({"role": "user", "message": prompt})

#     with st.spinner('Wait for it...'):
#         while status != "completed":
#             sleep(2)
#             status = check_run_status(thread_id, run.id)
#             print(status)
#             if status == "failed":
#                 break
#             elif status == "completed":
#                 render_chat_interface(print_history(thread_id))



    


