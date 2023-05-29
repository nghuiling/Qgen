import streamlit as st
import json
from streamlit.components.v1 import html
from fpdf import FPDF
import base64
import math

import os

os.getcwd()



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



st.set_page_config(page_title="Qgen", page_icon="🔍", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.big-font {
    font-size:35px !important;
    font-weight: bold;
}
.med-font {
    font-size:20px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

#file path
css_path = os.path.realpath('assets/style.css')
data_path = os.path.realpath('data/data.json')
compare_data_path = os.path.realpath('data/compare_answer.json')



with open( css_path ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown('<p class="big-font">Answers</p>', unsafe_allow_html=True)

#get multiple choices
def get_choices(options,shuffled):
  items1 = [options[x] + ': '+shuffled[x] for x in range(0,len(shuffled))]
  items1 = tuple(items1)
  return items1


def get_output():

    your_answer = []
    correct_answer = []

    # Opening JSON file
    with open(compare_data_path, 'r') as openfile:
    
        # Reading from json file
        compare = json.load(openfile)

      # Opening JSON file
    with open(data_path, 'r') as openfile:
    
        # Reading from json file
        output = json.load(openfile)
    try:
        st.write('##### Your score: ' +str( len([i for i, j in zip(compare['your_answer'], compare['correct_answer']) if i == j]))+'/'+str(len(compare['correct_answer'])))
    except Exception:
        st.write()

    for index,qns in enumerate(output):
        question = 'Q'+str(index+1) + ': ' + output[index]['question']
        shuffled_choices = get_choices(output[index]['options'],output[index]['shuffled'])
        status = st.radio(question,shuffled_choices, index=output[index]['shuffled'].index(compare['your_answer'][index]))
        your_answer.append(str(status.split(':')[1]).strip())
        correct_answer.append(output[index]['answer'])

        if str(status.split(':')[1]).strip() == str(output[index]['answer']):
            st.success('Correct!')
        else:
            st.error('Wrong!')

    return output, your_answer, correct_answer

output, your_answer, correct_answer =get_output()

#button layouts
col1, col2, col3 = st.columns([1,1,1])

##col1= download as pdf button

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

with col1:

    if st.button("Try Again"):
        temp_json_data = {}
        temp_json_data['your_answer'] = your_answer
        temp_json_data['correct_answer'] = correct_answer
        jsonString = json.dumps(temp_json_data)
        jsonFile = open(compare_data_path, "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        nav_page("questions")

with col2:

    export_as_pdf = st.button("Download MCQs as PDF")

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
with col3:
    if st.button("Generate New Questions"):

        #remove previous json file
        # jsonString = json.dumps({})
        # jsonFile = open(data_path, "w")
        # jsonFile.write(jsonString)
        # jsonFile.close()

        # jsonString = json.dumps({})
        # jsonFile = open(compare_data_path, "w")
        # jsonFile.write(jsonString)
        # jsonFile.close()

        nav_page("generate")
