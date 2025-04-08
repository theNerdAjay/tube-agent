import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import markdown


def sendemail(sender_email,sender_passoword,reciever_email,subject="Your YouTube Thumbnail Download is Ready", attachment=None):
    markdown_content = f'''
**Dear User,**

We are pleased to inform you that the thumbnail for your requested YouTube video has been successfully downloaded and is now available.

**Video Details:**

- **Title:** [Video Title]
- **URL:** [Video URL]

You will find the thumbnail image attached to this email.

If you have any questions or require further assistance, please feel free to reach out.

Best regards,

Ajay Dhanraj Sonar

Andyees YoutubeBOT
'''

    
    # convert markdown to html 
    
    html_content = markdown.markdown(markdown_content)

    # create a multipart message 

    message = MIMEMultipart("mixed") # mixed for attachments
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = reciever_email

    # Create a plain text part (optional)

    plain_text = markdown_content
    plain_part = MIMEText(plain_text,"plain")
    message.attach(plain_part)

    # create a html part

    html_part = MIMEText(html_content,"html")
    message.attach(html_part)

    # handle attachment

    if attachment:
        try:
            with open(f"thumbnails/{attachment}","rb") as attachment_file:
                image_part = MIMEImage(attachment_file.read())
                message.attach(image_part)
        except FileNotFoundError:
            print(f"Error: Attachment file not found: {attachment}")
        except Exception as e:
             print(f"Error attaching file {attachment}: {e}")
    
    try:
        # connect to smtp server

        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
            server.login(sender_email,sender_passoword)
            server.sendmail(sender_email,reciever_email,message.as_string())
        print(f"Email Was Sent Successfully to {reciever_email}")
    except smtplib.SMTPException as e:
        print(f"Error sending email {e}")

                
                



    
    