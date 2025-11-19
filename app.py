import os
import streamlit as st
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# =============================================
# CONFIGURATION – works locally AND in Azure
# =============================================

# Get endpoint from Streamlit secrets (local) OR Azure App Settings (production)
AZURE_OPENAI_ENDPOINT = st.secrets.get("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")

if not AZURE_OPENAI_ENDPOINT:
    st.error("❌ AZURE_OPENAI_ENDPOINT is not set. Add it in Azure App Settings or local .streamlit/secrets.toml")
    st.stop()

# Ensure trailing slash
if not AZURE_OPENAI_ENDPOINT.endswith("/"):
    AZURE_OPENAI_ENDPOINT += "/"

# Model deployment name (change to whatever you deployed, e.g. gpt-4o, gpt-35-turbo, etc.)
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")   # default to gpt-4o

# =============================================
# KEYLESS AUTHENTICATION (Managed Identity)
# =============================================

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
    api_version="2024-08-01-preview",
)

# =============================================
# STREAMLIT UI
# =============================================

st.set_page_config(page_title="Avanade AI Chat", page_icon="🤖", layout="centered")

# Show logged-in user (from Entra ID SSO)
if "user" not in st.session_state:
    user_email = st.experimental_get_query_params().get("email", [None])[0]
    if user_email:
        st.session_state.user = user_email
        st.success(f"Welcome {user_email.split('@')[0]}! You're authenticated via Entra ID SSO")

st.title("🤖 Avanade Azure OpenAI Chat")
st.caption("Secure • Keyless • Enterprise SSO • Powered by GPT-4o")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant for Avanade employees."}
    ]

# Display chat messages
for message in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
                max_tokens=1500,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"OpenAI API error: {str(e)}")

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Optional: Clear chat button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = st.session_state.messages[:1]  # keep system prompt
    st.rerun()
