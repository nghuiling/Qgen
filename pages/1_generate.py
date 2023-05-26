import streamlit as st
import time
import numpy as np

from streamlit.components.v1 import html

from codes.Qgen import run_qgen

import json

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

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


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


with open( css_path ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown('<p class="big-font">Generate MCQs</p>', unsafe_allow_html=True)


# import streamlit as st
# import webbrowser

# url = 'https://www.streamlit.io/'

# if st.button('Open browser'):
#     webbrowser.open_new_tab(url)

# if st.button("Back"):
#     nav_page("home")

# st.write(
#     """Insert yout text here to generate MCQs"""
# )

def get_text():
    text= st.text_area('Input your text:' , placeholder='Your text here...')
    return text

def get_file():
    uploaded_file = st.file_uploader("Choose a file:")
    return uploaded_file

def get_num_mcq():
    num_mcq = st.number_input(
    'Number of MCQs (from 1 to 50)',
    min_value=1, max_value= 50)
    return num_mcq

def get_num_choice():
    num_choice= st.number_input(
        'Number of Options per MCQ (from 4 to 6)',
        min_value=4, max_value= 6)
    return num_choice


st.markdown('<p class="med-font">Step 1: Add your texts</p>', unsafe_allow_html=True)


text_input = get_text()

st.write("###### or")

file_input = get_file()

#################################
#testing
def get_min_max_qns(min, max):
  items = list(range(min,max+1))
  items1 = [str(x) for x in items]
  items1.insert(0,'')
  items1 = tuple(items1)
  return items1


#settings
min_max_num_mcq = get_min_max_qns(1,50)
min_max_num_choice = get_min_max_qns(4,6)


#################################

st.markdown('<p class="med-font"><br>Step 2: Select number of questions</p>', unsafe_allow_html=True)

num_mcq_input = get_num_mcq()


st.markdown('<p class="med-font"><br>Step 3: Select number of options</p>', unsafe_allow_html=True)


num_mcq_choice = get_num_choice()


def save_output(output):

    #save into json file
    jsonString = json.dumps(output)
    jsonFile = open(data_path, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    # st.write("##### Your results:")
    # for index,qns in enumerate(output):
    #     question = 'Q'+str(index+1) + ': ' + output[index]['question']
    #     shuffled_choices = get_choices(output[index]['options'],output[index]['shuffled'])
    #     status = st.radio(question,shuffled_choices)



if st.button("Generate my MCQs now!"):
    if (num_mcq_input and num_mcq_choice):
        if (text_input and not file_input) or (file_input and not text_input):
        
        
        
            if file_input:
                bytes_data = file_input.getvalue()
                file_text_input = str(bytes_data, encoding='utf-8')
                output = run_qgen(file_text_input, int(num_mcq_input), int(num_mcq_choice)-1)
                save_output(output)
                nav_page("questions")

            else:
                output = run_qgen(text_input, int(num_mcq_input), int(num_mcq_choice)-1)
                save_output(output)
                nav_page("questions")


        else:
            st.error('😥 Unable to generate questions... Please choose to either input text or upoad a file!')        
              

    else:
        st.error('😥 Unable to generate questions... Please select all the options!')
        


