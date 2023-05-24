import streamlit as st
import time
import numpy as np
from base64 import b64encode
from fpdf import FPDF
import base64
from streamlit.components.v1 import html


#nav_page func
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

st.set_page_config(page_title="Qgen", page_icon="😕",  initial_sidebar_state="collapsed")

output = st.write("Generated questions") # final_result_from_processing_the_input

st.text_area(label="Q1:", value=output, height=100)
st.text_area(label="Q2:", value=output, height=100)
st.text_area(label="Q3:", value=output, height=100)
st.text_area(label="Q4:", value=output, height=100)
st.text_area(label="Q5:", value=output, height=100)


#button layouts
col1, col2, col3 = st.columns([1,1,1])

##col1= download as pdf button

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

with col1:
    pdf = FPDF()  # pdf object
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_font("Times", "B", 18)
    pdf.set_xy(10.0, 20)
    pdf.cell(w=75.0, h=5.0, align="L", txt="This is my sample text")

    st.download_button(
        "Download MCQs",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="Questions.pdf",
    )

with col2:
    if st.button("Answers"):
        nav_page("answers")
with col3:
    if st.button("Generate New Questions"):
        nav_page("generate")
