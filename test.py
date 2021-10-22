import smtplib
import ssl
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
# Yyour address
sender_email = "ramzj2.usm@gmail.com"
# Rreceiver address
receiver_email = "martin.salinas.scussolin@gmail.com"
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