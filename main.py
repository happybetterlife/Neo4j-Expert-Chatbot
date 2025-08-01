import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

#Title
st.header("Neo4j Expert Chatbot")

#Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

#User input
prompt = st.chat_input("Please enter what you want to ask about Neo4j")
if prompt:
    #Append user input to chat history
    with st.chat_message("user"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.write(prompt)
    #Dosen' have last chat_history
    if 'response_id' not in st.session_state:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="You are an expert in neo4j.",
            input=prompt,
            tools=[{
                "type": "file_search",
                "vector_store_ids": ["vs_688cb1cb4aac8191a133174863435691"]
            }]
        )
    #If have last chat_history, use it
    else:
        response = client.responses.create(
            previous_response_id=st.session_state.response_id,
            model="gpt-4o-mini",
            instructions="You are an expert in neo4j.",
            input=prompt,
            tools=[{
                "type": "file_search",
                "vector_store_ids": ["vs_688cb1cb4aac8191a133174863435691"]
            }]
        )
        
    #LLM response and append to chat history
    with st.chat_message("assistant"):
        st.write(response.output_text)
    st.session_state.chat_history.append({"role": "assistant", "content": response.output_text})
    st.session_state.response_id = response.id




response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are an expert in neo4j.",
    input="What is neo4j?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["vs_688cb1cb4aac8191a133174863435691"]
    }]
)

print(response.output_text)

second_response = client.responses.create(
    previous_response_id=response.id,
    model="gpt-4o-mini",
        instructions="You are an expert in neo4j.",
        input="What is the difference between neo4j and other databases?",
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["vs_688cb1cb4aac8191a133174863435691"]
     }]
)
print(second_response.output_text)