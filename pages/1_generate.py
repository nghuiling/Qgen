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

st.set_page_config(page_title="Qgen", page_icon="😕", initial_sidebar_state="collapsed")

st.markdown("# Generate MCQs")

st.write(
    """Insert yout text here to generate MCQs"""
)
text= st.text_input('Input your text:' )
st.write("or")
uploaded_file = st.file_uploader("Choose a file")

option = st.selectbox(
 'Number of MCQs',
  ('1', '2', '3', '4','5'))
option2= st.selectbox(
    'Number of Options per MCQ',
    ('2','4','6')
)
if st.button("Generate my MCQs now!"):
    nav_page("questions")


