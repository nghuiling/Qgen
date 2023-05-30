import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

import os
import json
import base64
import math

from fpdf import FPDF


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
</style>
""",
    unsafe_allow_html=True,
)


######################## SESSION STATE ########################
# "session state:", st.session_state


######################## FILE PATH ########################
css_path = os.path.realpath('assets/style.css')


######################## GET CSS ########################
with open( css_path ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


######################## GET CONTENTS ########################
if st.button("Back to Home 🏠"):
    for key in st.session_state.keys():
        del st.session_state[key]
    switch_page("home")

st.markdown('<p class="big-font">Answers</p>', unsafe_allow_html=True)

#get multiple choices
def get_choices(options,shuffled):
  
  items1 = [options[x] + ': '+shuffled[x] for x in range(0,len(shuffled))]
  items1 = tuple(items1)
  return items1


def get_output():

    your_answer = []
    correct_answer = []

    # Reading from json file
    output = st.session_state['output']

    try:
        st.write('##### Your score: ' +str( len([i for i, j in zip(st.session_state['your_answer'], st.session_state['correct_answer']) if i == j]))+'/'+str(len(st.session_state['correct_answer'])))
    except Exception:
        st.write()

    for index,qns in enumerate(output):
        question = 'Q'+str(index+1) + ': ' + output[index]['question']
        shuffled_choices = get_choices(output[index]['options'],output[index]['shuffled'])
        status = st.radio(question,shuffled_choices, index=output[index]['shuffled'].index(st.session_state['your_answer'][index]))
        your_answer.append(str(status.split(':')[1]).strip())
        correct_answer.append(output[index]['answer'])

        if str(status.split(':')[1]).strip() == str(output[index]['answer']):
            st.success('Correct!')
        else:
            st.error('Wrong!')

    return output, your_answer, correct_answer

#if refresh session will bring back to home page (refresh will restart states)
try:
    output, your_answer, correct_answer= get_output()
except:
    switch_page("home")

#button layouts
col1, col2, col3 = st.columns([1,1,1])

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

with col1:

    if st.button("Try Again"):
        temp_json_data = {}
        temp_json_data['your_answer'] = your_answer
        temp_json_data['correct_answer'] = correct_answer

        switch_page("questions")

with col2:

    export_as_pdf = st.button("Download MCQs as PDF")

    #temp catch error
    try:
        if export_as_pdf:
            pdf = FPDF()
            pdf.add_page()

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(190, 10, txt='MCQ Questions', align='C')
            pdf.ln(h=15)

            page_lines = 0

            for qn_num in range(len(output)):
                pdf.set_font('Arial', 'B', 10)
                tmp_qn = "(" + str(qn_num+1) + ")" + "  " + output[qn_num]['question']

                string_width = pdf.get_string_width(tmp_qn)
                num_lines = math.ceil(string_width / (190-1))
                num_lines_options = len(output[qn_num]['shuffled'])
                total_lines_for_qn = num_lines + num_lines_options

                if (page_lines+total_lines_for_qn)>=20:
                    pdf.add_page()
                    page_lines = 0
                else:
                    page_lines += total_lines_for_qn

                pdf.multi_cell(190, 10, txt=tmp_qn)

                for choices in range(len(output[qn_num]['shuffled'])):
                    pdf.set_font(family='Arial', size=10)
                    tmp_option = "        " + output[qn_num]['options'][choices] + ") " + output[qn_num]['shuffled'][choices]
                    pdf.cell(190, 10, txt=tmp_option)
                    pdf.ln()

                    if choices==len(output[qn_num]['options'])-1:
                        pdf.ln(h=1)

            pdf.add_page()

            pdf.set_font('Arial', 'B', 16)
            pdf.cell(190, 10, txt='Answers', align='C')
            pdf.ln(h=15)

            for qn_num in range(len(output)):
                pdf.set_font('Arial', 'B', 12)
                tmp_answer = "(" + str(qn_num+1) + ")" + "  " + output[qn_num]['options'][output[qn_num]['answer_index']]
                pdf.cell(190, 10, txt=tmp_answer)
                pdf.ln()
            
            html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

            st.markdown(html, unsafe_allow_html=True)

    except Exception:
        st.error('😔 Unable to download PDF due to incompatible characters.')

with col3:

    if st.button("Generate New Questions"):

        for key in st.session_state.keys():
            del st.session_state[key]

        switch_page("generate")
