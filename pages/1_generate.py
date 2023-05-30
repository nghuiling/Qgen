import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

import os
import time
import json
import numpy as np

from codes.Qgen import run_qgen


######################## GET DIRECTORY ########################
os.getcwd()


######################## CONFIG PAGE ########################
st.set_page_config(page_title="Qgen", page_icon="🔍", initial_sidebar_state="collapsed")


######################## HTML STYLE ########################
st.markdown(
    """
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    .big-font {
    font-size:35px !important;
    font-weight: bold;
}
.med-font {
    font-size:20px !important;
    font-weight: bold;
}
""",
    unsafe_allow_html=True,
)


######################## SESSION STATE ########################
# Delete all the items in Session state
# for key in st.session_state.keys():
#     del st.session_state[key]

# "session state:", st.session_state


######################## FILE PATH ########################
css_path = os.path.realpath('assets/style.css')


######################## GET CSS ########################
with open( css_path ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


######################## GET CONTENTS ########################
if st.button("Back to Home 🏠"):
    switch_page("home")

st.markdown('<p class="big-font">Generate MCQs</p>', unsafe_allow_html=True)


def get_text():
    text= st.text_area('Input your text:' , placeholder='Your text here...')
    return text

def get_file():
    uploaded_file = st.file_uploader("Choose a file:")
    return uploaded_file

def get_num_mcq():
    num_mcq = st.number_input(
    'Number of MCQs (from 1 to 20)',
    min_value=1, max_value= 20)
    return num_mcq

def get_num_choice():
    num_choice= st.number_input(
        'Number of Options per MCQ (from 4 to 6)',
        min_value=4, max_value= 6)
    return num_choice

st.error('⚠️Warning: By using our services, you are responsible for the data security and usage. Please do not add any sensitive data!')


st.markdown('<p class="med-font">Step 1: Add your texts</p>', unsafe_allow_html=True)


# Please ensure data security and responsible usage. Do not add any sensitive data!
text_input = get_text()

st.write("###### or")

file_input = get_file()

st.markdown('<p class="med-font"><br>Step 2: Select number of questions</p>', unsafe_allow_html=True)

num_mcq_input = get_num_mcq()

st.markdown('<p class="med-font"><br>Step 3: Select number of options</p>', unsafe_allow_html=True)

num_mcq_choice = get_num_choice()



if st.button("Generate my MCQs now! 🪄"):
    if (num_mcq_input and num_mcq_choice):
        if (text_input and not file_input) or (file_input and not text_input):
        
            if file_input:
                bytes_data = file_input.getvalue()
                file_text_input = str(bytes_data, encoding='utf-8')
                output = run_qgen(file_text_input, int(num_mcq_input), int(num_mcq_choice)-1)

                #add session states
                if 'num_mcq' not in st.session_state:
                    st.session_state['num_mcq'] = num_mcq_input

                if 'output' not in st.session_state:
                    st.session_state['output'] = output

                switch_page("questions")

            else:
                output = run_qgen(text_input, int(num_mcq_input), int(num_mcq_choice)-1)

                #add session states
                if 'num_mcq' not in st.session_state:
                    st.session_state['num_mcq'] = num_mcq_input

                if 'output' not in st.session_state:
                    st.session_state['output'] = output

                switch_page("questions")

        else:
            st.error('😥 Unable to generate questions... Please choose to either input text or upoad a file!')        
            
    else:
        st.error('😥 Unable to generate questions... Please select all the options!')
