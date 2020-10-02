from cld3 import get_language
from utilities.summary import Summary
import streamlit as st
import time

st.title("संkshep")
st.write("Hindi Text Summarization")

text = st.text_area('Input your text here:')

abstractive = False
percentage = None

if not st.checkbox("Use default compression percentage", value=True):
    percentage = st.slider("Compression Percentage", 0, 100, 0, 1)


if st.button('Summarize'):
	if get_language(text).language != 'hi':
		st.error("Summarization only available for Hindi.")
	with st.spinner("Fetching your summary..."):
		processed_summary, percentage = Summary(text, percentage, abstractive)
		time.sleep(5)
	st.success("Done!")
	st.write(f"## Summary ({format(percentage, '.2f')}% reduced)")
	st.write(f"***{processed_summary}***", unsafe_allow_html=True)
	st.write(f"""**Original Text:** *{len(text)} characters*
		**Summary:** *{len(processed_summary)} characters*""")
