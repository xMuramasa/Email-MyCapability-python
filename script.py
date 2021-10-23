import numpy as np
from sqlConnection import connect_ppg2, create_df_from_ppg2
import smtplib
import ssl
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime

def sendEmail(receiver_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    # Yyour address
    sender_email = "Equipo de MyCapability <ramzj2.usm@gmail.com>"
    # Rreceiver address
    #receiver_email = "ramzj2.usm@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = codecs.open("mycap.html", 'r').read()

    # Turn these into plain/html MIMEText objects
    m = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(m)

    images = [
        'logo','saltovertical_1','saltohorizontal_1',
        'sprint_1','facebook2x','instagram2x','youtube2x'
        ]

    for i in range(1,8):

        # This example assumes the image is in the current directory
        fp = open('images/'+images[i-1]+'.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image' + str(i) + '>')
        message.attach(msgImage)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        print("server login")
        server.login("ramzj2.usm@gmail.com", "mc_rj2.usm")
        # Send email here
        print("server sendmail")
        
        server.sendmail(sender_email, receiver_email, message.as_string())


def parseRow(row):
    # date from db
    reg = row.register_date
    f = row.freq
    
    if f is None or f == 'NO':
        print('era fake')
        return
    else:
        f = int(f)

    # new date
    todayDate = datetime.date.today()

    d = datetime.timedelta(days= f * 7)

    newDate = abs((todayDate - reg).days)

    if newDate % f == 0:
        print('Se envia correo')
        #sendEmail(row.email)
    else:
        print('fake')


conn = connect_ppg2()
q = 'SELECT * FROM Users ORDER BY id ASC'
df = create_df_from_ppg2(q,conn)

q = 'SELECT * FROM results'
df2 = create_df_from_ppg2(q,conn)

print(df)

for i in range(df.shape[0]):
    parseRow(df.loc[i])
