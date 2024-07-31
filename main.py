import streamlit as st
import PyPDF2
import asyncio
import grok
# from document_model import model, parser

# Set up page configuration
st.set_page_config(layout="wide")

# Initialize session state for messages if not already done
if 'all_messages' not in st.session_state:
    st.session_state.all_messages = []

# Display the subheader if there are no messages
if len(st.session_state.all_messages) == 0:
    st.markdown("<h2 style='text-align: center;'>How can I help  ?🤖🤖🤖</h2>", unsafe_allow_html=True)
 


# Sidebar setup
st.sidebar.title('OmniDocAI 🤖📄⚡')
st.sidebar.divider()

# Dialog function
@st.dialog("Upgrade to premium")
def dialogue():
    st.write("Upgrade to pro and you can upload larger sizes of data")
    st.write("Premium users can perform unlimited quick searches, allowing for fast access to information.")
    if st.button("Upgrade"):
        st.session_state.upgrade = {"upgrade": "true"}
        st.rerun()
# Sidebar options and file uploader
st.sidebar.subheader("Chatbot Options")
if st.sidebar.button("Become a Pro 💵 "):
    dialogue()

option = st.sidebar.selectbox(
    "What type of documents Are we dealing with ?",
    ("Agriculture", "Land Administration", "Healthcare"),
)

uploaded_files = st.sidebar.file_uploader("Choose files 🗃️", accept_multiple_files=True)

if uploaded_files:
    st.sidebar.subheader("Uploaded Files:")
    for uploaded_file in uploaded_files:
        st.sidebar.write(f"**File Name:** {uploaded_file.name}")

        bytes_data = uploaded_file.getvalue()

        if uploaded_file.type == "text/plain":
            string_data = bytes_data.decode("utf-8")
            st.sidebar.write("**Content:**")
            st.sidebar.write(string_data)
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() + "\n"
            st.sidebar.write("**Content:**")
            st.sidebar.write(pdf_text)
        else:
            st.sidebar.write("**Content:** File type not supported for content display.")

if not uploaded_files:
    st.markdown("<h2 style='text-align: center;'>Upload documents for extraction📄📄📄📄 </h2>", unsafe_allow_html=True)

# Chat input and message handling
if uploaded_files:
    prompt = st.chat_input("Your message", key='prompt')

    if prompt:
        st.session_state.all_messages.append({'user': 'user', 'message': prompt})
        ai_response = grok.make_inference(prompt)
        st.session_state.all_messages.append({'user':'A.I', 'message': ai_response})


# Display all messages
if len(st.session_state.all_messages) > 0:
    for message in st.session_state.all_messages:
        
        match message.get('user'):
            case 'you':
                st.html(f"<h2>{message.get('message')}</h2>")
            case _:
                st.write(f"{message.get('user')} : {message.get('message')}")

# Additional sidebar section
st.sidebar.subheader("Optimus")
st.sidebar.subheader(" made with 🇬 🇭  🇬🇭 🇬🇭 ") 
st.sidebar.write(len(st.session_state.all_messages))
