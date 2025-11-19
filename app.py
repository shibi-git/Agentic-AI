import streamlit as st
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

st.title("Simple Azure OpenAI Chat with Entra ID SSO")

# Use managed identity / DefaultAzureCredential (works locally with az login too)
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],  # e.g. https://your-resource.openai.azure.com/
    azure_ad_token_provider=token_provider,
    api_version="2024-08-01-preview",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",  # your deployment name
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(chunk.choices[0].delta.content or "" for chunk in stream)
    st.session_state.messages.append({"role": "assistant", "content": response})