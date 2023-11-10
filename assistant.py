from openai import OpenAI
import requests
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def create_thread():
    thread = client.beta.threads.create()
    return thread

def create_custom_assistant(name, instructions, tools=[{"type": "code_interpreter"}], model="gpt-4-1106-preview"):
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model=model
    )

    thread = create_thread()
    return assistant, thread

def msg_to_assistant(msg, assistant_id, thread_id, files):
    if len(files) > 0:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=msg,
            file_ids = files
        )
        print(f"File ID: {files}")
    else:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=msg
        )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Only play with the given data. The user has a premium account."
    )
        
    return message, run

def check_run_status(thread_id, run_id):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return run.status

def print_history(thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    chat_history = []

    for message in messages.data[::-1]:
        for msg in message.content:
            if msg.type == "text":
                chat_history.append({"role": message.role, "message": msg.text.value, "type": "text"})
            elif msg.type == "image_file":
                file_id = msg.image_file.file_id      
                
                url=f"https://api.openai.com/v1/files/{file_id}/content"
                headers = {"Authorization": f"Bearer {client.api_key}"}
                response = requests.get(url, headers=headers)

                content = response.content

                chat_history.append({"role": message.role, "message": content, "type": "image_file"})

    return chat_history
   

def get_assistant(assistant_id):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant

def get_file_contents(uploaded_file):
    if uploaded_file is not None:
        file_contents = client.files.retrieve_content(uploaded_file.id)
        return file_contents
    else:
        return None

def get_file_id(file_path):
    file = client.files.create(
        file=file_path,
        purpose='assistants'
    )
    return file.id

def list_assistants():
    assistants = client.beta.assistants.list()
    return assistants.data

def delete_assistant(assistant_id):
    assistant = client.beta.assistants.delete(assistant_id)
    return assistant

def main():
    # name = "Data Engineer Assistant"
    # instructions = "You are a professional data engineer hired by me to help with my data."
    # tools = [{"type": "code_interpreter"}, {"type": "retrieval"}]

    # assistant, thread = create_custom_assistant(name, instructions, tools)
    # print(f"Assistant ID: {assistant.id}")
    # print(f"Thread ID: {thread.id}")

    assistant_id = "asst_rPoDakLcCCbsWASSlL1jRr3Z"
    thread_id = "thread_dMI4tDChMAxpGrs3exqrNjN2"
    # # Message = "msg_vKTPSTm0fr9PGgLV6ZxlDACa"
    # # Run = "run_vE4FvLPDFURX6gM2ZjrIodI0"

    # msg = "Can you help me with JSON files?"
    # message, run = msg_to_assistant(msg, assistant_id, thread_id)
    # print(f"Message ID: {message.id}")
    # print(f"Run ID: {run.id}")

    # status = check_run_status(thread_id, run.id)
    # print(f"Status: {status}")

    # while status != "completed":
    #     status = check_run_status(thread_id, run.id)

     
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    print(f"Messages: {messages.data}")

    # print_history(thread_id)

    # my_updated_assistant = client.beta.assistants.update(
    #     assistant_id,
    #     tools=[{"type": "code_interpreter"}],
    #     file_ids=[],
    # )
    
    # print(my_updated_assistant)

# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
# )

# run = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id=assistant.id,
#   instructions="Please address the user as Jane Doe. The user has a premium account."
# )

# run = client.beta.threads.runs.retrieve(
#   thread_id=thread.id,
#   run_id=run.id
# )

# messages = client.beta.threads.messages.list(
#   thread_id="thread_XMvZXJN24McZMpmO0aac1SnW"
# )

# print((messages.data)[0].content[0].text.value)
# msg_id = "msg_PJNzmaLUfu0VEjmNwlsC6Pt5"
# thread_id = "thread_XMvZXJN24McZMpmO0aac1SnW"

if __name__ == "__main__":
    # main()
    status = check_run_status("thread_dMI4tDChMAxpGrs3exqrNjN2", "run_n0admmET5HRphx4veTqn5azA")
    print(f"Status: {status}")