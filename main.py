import streamlit as st
from utils.sendmail import send_email
from utils.constants import (SMTP_SERVER_ADDRESS,PORT,SENDER_PASSWORD,SENDER_ADDRESS)
from utils.topsisProgram import topsis
import pandas as pd
import numpy as np

st.set_page_config(page_title="MCDM Web-App",)
st.title('Multi-Criteria-Decision-Making Application')


def check(input_file,weights,impacts,result_file,email):
    if weights == '' or impacts == '' or result_file == '' or input_file is None:
        st.error('Please fill all the fields')
        return False
    else:
        return True 


if __name__ == '__main__':
    
    # Creating email form
    with st.form("Email Form"):
        input_file = st.file_uploader(label='Input File', type=['csv'])
        weights = st.text_input(label='Weights', placeholder="1,1,1,1,1")
        impacts = st.text_input(label='Impacts',placeholder="+,-,+,-,+")
        result_file = st.text_input(label='Result File', placeholder="abc.csv")
        email = st.text_input(label='Email', placeholder="sample@gmail.com")
        submit_res = st.form_submit_button('Submit')


    if (check(input_file,weights,impacts,result_file,email) == True):
        if submit_res:
            df = pd.read_csv(input_file)
            topsis(df,weights,impacts,result_file)
            fullName = "Jasween Kaur Brar"
            subject = "TOPSIS Solution"
            message = """ Email Address of Sender {} \n Sender Full Name {} \n\n""".format(email,fullName)
            send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD,
            receiver=email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT,
            email_message=message, subject=subject, attachment=result_file)


