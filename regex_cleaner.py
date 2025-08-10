import streamlit as st
import re
import nltk
import base64















def generate_code(clean_types):
    code = [
        "import re",
        "text = '''Your text here'''"
    ]
    
    # Add NLTK import if stopwords removal is selected
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
