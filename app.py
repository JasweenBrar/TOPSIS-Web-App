import streamlit as st
import pandas as pd
import numpy as np
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.set_page_config(page_title="Topsis",)
st.title('Topsis-Jasween')
PASSWORD = st.secrets["PASSWORD"]

def checkValidation(df,weights,criteria,result_file) :
    if weights.__contains__(',') == False:
        st.error("Weights should be separated by comma")
        return False
    if criteria.__contains__(',') == False:
        st.error("Weights should be separated by comma")
        return False
    if result_file.__contains__('.csv') == False:
        st.error("Result file should be csv")
        return False
    weights = weights.split(',')
    criteria = criteria.split(',')
    weights = [float(x) for x in weights]
    rows,cols = df.shape
    if cols<3:
        st.error("File should have atleast 3 columns")
        return False
    if(len(weights) != cols-1):
        st.error("Number of weights should be " + str(cols-1))
        return False
    if(len(criteria) != cols-1):
        st.error("Number of criteria should be " + str(cols-1))
        return False
    return True


def topsis(df, weights, criteria,result_file):
    df2 = df.iloc[:, 1:]
    
    df2 = df2.apply(lambda x: x / np.sqrt(np.sum(np.square(x))), axis=0)
    
    df2 = df2 * weights
    
    rows, cols = df2.shape
    df2_ideal_best = []
    df2_ideal_worst = []

    for i in range(cols):
        if criteria[i] == '-':
            df2_ideal_best.append(df2.iloc[:, i].min())
            df2_ideal_worst.append(df2.iloc[:, i].max())
        else:
            df2_ideal_best.append(df2.iloc[:, i].max())
            df2_ideal_worst.append(df2.iloc[:, i].min())
    df2_s_best = []
    df2_s_worst = []
    for i in range(rows):
        df2_s_best.append(np.sqrt(np.sum(np.square(df2.iloc[i, :] - df2_ideal_best))))
        df2_s_worst.append(np.sqrt(np.sum(np.square(df2.iloc[i, :] - df2_ideal_worst))))

    topsis_score = [x/(x+y) for x, y in zip(df2_s_worst, df2_s_best)]

    sorted_score = sorted(topsis_score, reverse=True)

    topsis_rank = [sorted_score.index(x)+1 for x in topsis_score]

    df = df.assign(topsis_score=topsis_score, topsis_rank=topsis_rank)
    df = df.rename(columns={'topsis_score': 'Topsis Score', 'topsis_rank': 'Rank'})
    df.to_csv(result_file, index=False)

def sendEmail(email, result_file) : 
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "simplehands8888@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address

        # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Topsis Final CSV Attachment"

        # Add body to email
    message.attach(MIMEText("Please find the attached CSV file.", "plain"))

        # Open PDF file in bynary
    with open(result_file, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())

        # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

        # Add header with pdf name
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={result_file}",
    )

        # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

        # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, PASSWORD)
        server.sendmail(sender_email, receiver_email, text)
    

def onSubmit(df,weights,criteria,result_file,email):
    if weights == '' or criteria == '' or result_file == '':
        st.error('Please fill all the fields')
        return
    isValidated = checkValidation(df,weights,criteria,result_file)
    if isValidated == True:
        weights = weights.split(',')
        criteria = criteria.split(',')
        weights = [float(x) for x in weights]
        topsis(df, weights, criteria,result_file)
        sendEmail(email,result_file)
        st.success('Submitted')

forms = st.form(key='my_form')
input_file = forms.file_uploader('Input File', type=['csv'])
weights = forms.text_input('Weights')
criteria = forms.text_input('Criteria')
result_file = forms.text_input('Result File')
email = forms.text_input('Email')
submit = forms.form_submit_button('Submit')

if input_file is not None:

    df = pd.read_csv(input_file)

if submit:
    onSubmit(df,weights,criteria,result_file,email)