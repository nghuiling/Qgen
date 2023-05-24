import streamlit as st
import time
import numpy as np
from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

st.set_page_config(page_title="Qgen", page_icon="😕")

st.markdown("# Generate MCQs")
st.sidebar.header("Generate MCQs")
st.write(
    """Insert yout text here to generate MCQs"""
)

def get_text():
    text= st.text_input('Input your text:' , placeholder='Your text here...')
    return text

def get_file():
    uploaded_file = st.file_uploader("Choose a file:")
    return uploaded_file

def get_num_mcq():
    num_mcq = st.selectbox(
    'Number of MCQs',
    ('','1', '2', '3', '4','5'))
    return num_mcq

def get_num_choice():
    num_choice= st.selectbox(
        'Number of Options per MCQ',
        ('','2','4','6')
    )
    return num_choice


st.write("##### Step 1: Add your texts")

text_input = get_text()

st.write("###### or")

file_input = get_file()

st.write("##### Step 2: Select number of questions")

num_mcq_input = get_num_mcq()

st.write("##### Step 3: Select number of options")

num_mcq_choice = get_num_choice()


#################################






#################################


if st.button("Generate my MCQs now!"):
    if (text_input or file_input) and (num_mcq_input and num_mcq_choice):


        nav_page("questions")


