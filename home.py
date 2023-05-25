import streamlit as st

from PIL import Image

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



#change time of the tab
st.set_page_config(page_title='MCQ Generator', initial_sidebar_state="collapsed", page_icon="🔍")
# st.header('MCQ Generator')

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

.med-font {
    font-size:18px !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


with open( "assets\style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


# st.sidebar.success("Select a demo above.")


#get image
image = Image.open('assets/logo.png')

vert_space = '<div style="padding: 4%;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)
##can add columns
col1, col2 = st.columns(2,  gap="large")

with col1:

    st.image(image)

with col2:
    st.markdown('<p>',unsafe_allow_html=True)
    st.markdown('<p class="med-font"><br><b>Qgen</b> is a tool that helps you generate Multiple Choice Questions (MCQ) from any text. Attach your notes, guidebooks and articles to generate questions for your learning.</p>', unsafe_allow_html=True)
    # st.markdown("<h1 style='text-align: center;'>Qgen is a tool that helps you generate Multiple Choice Questions (MCQ) from any text. Attach your notes, guidebooks and articles to generate questions for your learning.</h1><br>", unsafe_allow_html=True)
    st.markdown('<div style="padding: 5% 20%;"><a href="/generate" target = "_self"><button style="background-color:#697588;border: none;color: white;padding: 10px 25px;border-radius: 12px;">Create Your Quiz!</button></a></div>', unsafe_allow_html=True)
    vert_space = '<div style="padding: 50%;"></div>'
    # if st.button("Create Your Quiz!"):
    #     nav_page("generate")
# ##################################
# ##can add columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('## Column 1')
#     st.write('col1')
#     st.markdown('Testing')

# with col2:
#     st.write('col2')

# ##################################

# input_text = st.text_area(label="", placeholder="Your Email...", key="email_input")

# if input_text:
#     st.write('there is text now')
#     st.write(input_text)