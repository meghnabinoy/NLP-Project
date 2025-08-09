import streamlit as st
import re


def generate_code(cleaning_type):
    if cleaning_type == "Remove HTML Tags":
        pattern = r"<.*?>"
        code = f"""import re
text = "YOUR_TEXT_HERE"
cleaned_text = re.sub(r"{pattern}", "", text)
print(cleaned_text)"""
    elif cleaning_type == "Remove Punctuation":
        pattern = r"[^\w\s]"
        code = f"""import re
text = "YOUR_TEXT_HERE"
cleaned_text = re.sub(r"{pattern}", "", text)
print(cleaned_text)"""
    else: 
        pattern = r"<.*?>|[^\w\s]"
        code = f"""import re
text = "YOUR_TEXT_HERE"
cleaned_text = re.sub(r"{pattern}", "", text)
print(cleaned_text)"""
    return code











if user_text.strip():
    if clean_type == "Remove HTML Tags":
        cleaned_text = re.sub(r"<.*?>", "", user_text)
    elif clean_type == "Remove Punctuation":
        cleaned_text = re.sub(r"[^\w\s]", "", user_text)
    else:
        cleaned_text = re.sub(r"<.*?>|[^\w\s]", "", user_text)
    st.write("Cleaned Text Preview:",cleaned_text)