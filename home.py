import streamlit as st

from PIL import Image



#change time of the tab
st.set_page_config(page_title='MCQ Generator', initial_sidebar_state="collapsed", page_icon="😕")
# st.header('MCQ Generator')

with open( "assets\style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


st.sidebar.success("Select a demo above.")


#get image
image = Image.open('assets/logo.png')

vert_space = '<div style="padding: 8%;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)
##can add columns
col1, col2 = st.columns(2,  gap="large")

with col1:

    st.image(image)

with col2:
    st.markdown("<h1 style='text-align: center; color: red;'>Qgen is a tool that helps you generate Multiple Choice Questions (MCQ) from any text. Feel free to attach your notes, guidebooks and articles to generate questions for your learning.</h1><br>", unsafe_allow_html=True)
    st.markdown('<div style="padding: 0% 20%;"><a href="/generate" target = "_self"><button style="background-color:#697588;border: none;color: white;padding: 10px 25px;border-radius: 12px;">Create Your Quiz!</button></a></div>', unsafe_allow_html=True)

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