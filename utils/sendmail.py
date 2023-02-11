import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication

def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment = None):
    # First, a MIMEMultipart object is defined 
    # and receiver, sender and subject of the email is added to the message dictionary.
    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message["From"] = Header(sender)
    message['Subject'] = Header(subject)
    # We attach the email body through the attach function and MIMEText object.
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))
    # We check if there is an attachment and if so, we use MIMEApplication object 
    # and message.attach() function for adhering the attachment to the message.
    with open(attachment, "rb") as result_file:
        if attachment:
            att = MIMEApplication(result_file.read(), _subtype="txt")
            # Adding a header to the attachment using add_header function
            att.add_header('Content-Disposition', 'attachment', filename=result_file.name)
            message.attach(att)
    
    

    # We use the smtplib.SMTP object which helps to send a secure email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
