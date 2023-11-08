import streamlit as st

# Define the conversation history
conversation_history = []

# Streamlit app title
st.title("ChatGPT - User and Assistant Chat Interface")

# Text input for user messages


# Function to add user and assistant messages to the conversation history
def add_message(role, message):
    conversation_history.append({"role": role, "message": message})

# Function to display the chat interface
def display_chat_interface():
    st.subheader("Chat Interface")
    for item in conversation_history.list():
        if item["role"] == "User":
            st.text(f"You: {item['message']}")
        else:
            st.text(f"Assistant: {item['message']}")

            # Display the chat interface
display_chat_interface()

user_input = st.text_input("User:", "")

# Submit button to send user message
if st.button("Submit"):
    if user_input:
        add_message("User", user_input)
        # You can send the user input to your ChatGPT model and receive an assistant response here.
        # For simplicity, let's assume an echo response from the assistant.
        assistant_response = user_input  # Replace this with the actual assistant response
        add_message("Assistant", assistant_response)
        user_input = ""


