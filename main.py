import streamlit as st

from PIL import Image



#change time of the tab
st.set_page_config(page_title='MCQ Generator', page_icon=":robot:")
# st.header('MCQ Generator')


st.sidebar.success("Select a demo above.")

#get image
image = Image.open('assets/logo.png')


##can add columns
col1, col2 = st.columns(2)

with col1:

    st.image(image)

with col2:
    st.markdown('## Column 1')
    st.write('col2')
    st.markdown('Testing')

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