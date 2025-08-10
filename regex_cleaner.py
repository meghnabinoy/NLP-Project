import streamlit as st
import re
import nltk
import base64

st.set_page_config(page_title="Regex Code Generator for Text Cleaning", layout="wide")
st.title("Regex Code Generator for Text Cleaning")
st.write("Enter text, choose what to clean, and generate Python code for regex-based cleaning.")
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "clean_types" not in st.session_state:
    st.session_state.clean_types = []
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "previous_text" not in st.session_state:
    st.session_state.previous_text = ""
if "previous_clean_types" not in st.session_state:
    st.session_state.previous_clean_types = []
col_input, col_options = st.columns([2, 1])
with col_input:
    user_text = st.text_area("Enter your text:", st.session_state.user_text, height=200)
with col_options:
    clean_types = st.multiselect(
        "Choose cleaning types:",
        ["Remove HTML Tags", "Remove Punctuation", "Remove Stopwords", "Lowercase"],
        default=st.session_state.clean_types
)
if (user_text != st.session_state.previous_text or 
    clean_types != st.session_state.previous_clean_types):
    st.session_state.show_results = False
st.session_state.user_text = user_text
st.session_state.clean_types = clean_types
st.session_state.previous_text = user_text
st.session_state.previous_clean_types = clean_types

@st.cache_resource
def download_nltk_data():
    nltk.download('stopwords', quiet=True)
    return set(stopwords.words('english'))

try:
    from nltk.corpus import stopwords
    stop_words = download_nltk_data()
except:
    st.error("Error downloading NLTK data. Please check your internet connection.")
    stop_words = set()

def remove_stopwords(text):
    return ' '.join(word for word in text.split() if word.lower() not in stop_words)

def clean_text(text, clean_types):
    for ctype in clean_types:
        if ctype == "Remove HTML Tags":
            text = re.sub(r"<.*?>", "", text)
        elif ctype == "Remove Punctuation":
            text = re.sub(r"[^\w\s]", "", text)
        elif ctype == "Remove Stopwords":
            text = remove_stopwords(text)
        elif ctype == "Lowercase":
            text = text.lower()
    return text

def generate_code(clean_types):
    code = [
        "import re",
        "text = '''Your text here'''"
    ]
    
    if "Remove Stopwords" in clean_types:
        code.insert(1, "import nltk")
        code.insert(2, "from nltk.corpus import stopwords")
        code.insert(3, "nltk.download('stopwords')")
        code.insert(4, "stop_words = set(stopwords.words('english'))")
    
    for ctype in clean_types:
        if ctype == "Remove HTML Tags":
            code.append("text = re.sub(r'<.*?>', '', text)")
        elif ctype == "Remove Punctuation":
            code.append("text = re.sub(r'[^\\w\\s]', '', text)")
        elif ctype == "Remove Stopwords":
            code.append("text = ' '.join(word for word in text.split() if word.lower() not in stop_words)")
        elif ctype == "Lowercase":
            code.append("text = text.lower()")
    
    code.append("print(text)")
    return "\n".join(code)

if st.button("Generate Python Code"):
    if st.session_state.user_text.strip():
        st.session_state.show_results = True
        output_code = generate_code(st.session_state.clean_types)
        st.code(output_code, language="python")
    else:
        st.warning("Please enter some text.")
        st.session_state.show_results = False


if st.session_state.show_results and st.session_state.user_text.strip():
    cleaned_text = clean_text(st.session_state.user_text, st.session_state.clean_types)


    st.subheader("Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.write("*Original Text:*")
        st.text_area("", st.session_state.user_text, height=200, key="original_readonly", disabled=True)
    with col2:
        st.write("*Cleaned Text:*")
        st.text_area("", cleaned_text, height=200, key="cleaned_readonly", disabled=True)

 
    def download_button(data, filename, label):
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
        return href

    st.markdown(download_button(cleaned_text, "cleaned_text.txt", "📥 Download Cleaned Text"), unsafe_allow_html=True)


if st.session_state.show_results:
    if st.button("Clear Results"):
        st.session_state.show_results = False
        st.rerun()
