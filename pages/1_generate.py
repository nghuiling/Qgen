import streamlit as st
import time
import numpy as np

from streamlit.components.v1 import html

from codes.Qgen import run_qgen



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

st.set_page_config(page_title="Qgen", page_icon="😕", initial_sidebar_state="collapsed")

st.markdown("# Generate MCQs")

st.write(
    """Insert yout text here to generate MCQs"""
)

def get_text():
    text= st.text_input('Input your text:' , placeholder='Your text here...')
    return text

def get_file():
    uploaded_file = st.file_uploader("Choose a file:")
    return uploaded_file

def get_num_mcq(min_max):
    num_mcq = st.selectbox(
    'Number of MCQs',
    min_max)
    return num_mcq

def get_num_choice(min_max):
    num_choice= st.selectbox(
        'Number of Options per MCQ',
        min_max)
    return num_choice


st.write("##### Step 1: Add your texts")

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
min_max_num_mcq = get_min_max_qns(1,5)
min_max_num_choice = get_min_max_qns(2,5)


#################################


st.write("##### Step 2: Select number of questions")

num_mcq_input = get_num_mcq(min_max_num_mcq)

st.write("##### Step 3: Select number of options")

num_mcq_choice = get_num_choice(min_max_num_choice)




if st.button("Generate my MCQs now!"):
    if (text_input and not file_input) or (file_input and not text_input):
        
        
        if (num_mcq_input and num_mcq_choice):
            if file_input:
                bytes_data = file_input.getvalue()
                file_text_input = str(bytes_data, encoding='utf-8')
                output = run_qgen(file_text_input, int(num_mcq_input), int(num_mcq_choice))
                st.write(output)

                # if int(num_mcq_input)>len(output):
                #     st.write('Unable to generate the desired number of questions!')
                #     st.write(output)

                # else:
                #     output = output[:int(num_mcq_input)]
                #     st.write(output)

            else:
                output = run_qgen(text_input, int(num_mcq_input), int(num_mcq_choice))
                st.write(output)

                # if int(num_mcq_input)>len(output):
                #     st.write('Unable to generate the desired number of questions!')
                #     st.write(output)

                # else:
                #     output = output[:num_mcq_input+1]
                #     st.write(output)
  
        else:
            st.write('😥 Unable to generate questions... Please select all the options!')  

    else:
        st.write('😥 Unable to generate questions... Please choose to either input text or upoad a file!')        

        


        # nav_page("questions")


