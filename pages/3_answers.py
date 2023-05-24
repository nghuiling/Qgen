import streamlit as st
import json
from streamlit.components.v1 import html
from fpdf import FPDF
import base64

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

st.markdown("# Answers")

#get multiple choices
def get_choices(options,shuffled):
  items1 = [options[x] + ': '+shuffled[x] for x in range(0,len(shuffled))]
  items1 = tuple(items1)
  return items1


def get_output():

    # Opening JSON file
    with open('data/compare_answer.json', 'r') as openfile:
    
        # Reading from json file
        compare = json.load(openfile)

      # Opening JSON file
    with open('data/data.json', 'r') as openfile:
    
        # Reading from json file
        output = json.load(openfile)

    st.write('##### Your score: ' +str( len([i for i, j in zip(compare['your_answer'], compare['correct_answer']) if i == j]))+'/'+str(len(compare['correct_answer'])))

    for index,qns in enumerate(output):
        question = 'Q'+str(index+1) + ': ' + output[index]['question']
        shuffled_choices = get_choices(output[index]['options'],output[index]['shuffled'])
        status = st.radio(question,shuffled_choices, index=output[index]['shuffled'].index(compare['your_answer'][index]))

        if str(status.split(':')[1]).strip() == str(output[index]['answer']):
            st.success('Correct!')
        else:
            st.error('Wrong!')

get_output()

#button layouts
col1, col2, col3 = st.columns([1,1,1])

##col1= download as pdf button

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

with col1:

    if st.button("Try Questions Again"):
        nav_page("questions")

with col2:

    export_as_pdf = st.button("Download MCQs as PDF")

    if export_as_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)


        output = 'testing'

        pdf.cell(40, 10, output)
        
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

        st.markdown(html, unsafe_allow_html=True)
with col3:
    if st.button("Generate New Questions"):
        
        #remove previous json file
        jsonString = json.dumps({})
        jsonFile = open("data/data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

        jsonString = json.dumps({})
        jsonFile = open("data/compare_answer.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

        nav_page("generate")
