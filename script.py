import numpy as np
from sqlConnection import connect_ppg2, create_df_from_ppg2
import smtplib
import ssl
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import datetime
from q import query_down


def sendEmail(receiver_email, id):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "Equipo de MyCapability <ramzj2.usm@gmail.com>"
    
    ########### PSQL QUERY ###########
    conn = connect_ppg2()
    df2 = create_df_from_ppg2(query_down.format(id,id,id), conn)

    dfVert = df2[df2.type == 0].reset_index()
    dfHor = df2[df2.type == 1].reset_index()
    dfSpe = df2[df2.type == 2].reset_index()

    if dfVert.shape[0] > 1:
        if dfVert.loc[0].result != np.NaN and dfVert.loc[1].result != np.NaN:
            v = "Tu salto vertical ha mejorado en <b>{:10.4f}</b> metros"
            v = v.format(dfVert.loc[0].result-dfVert.loc[1].result)
        else: 
            v = 'No hay suficientes datos para ver si mejoraste, prueba saltar más :c'
    else:
        v = 'No hay suficientes datos para ver si mejoraste, prueba saltar más :c'
        
    if dfHor.shape[0] > 1:
        if dfHor.loc[0].result != np.NaN and dfHor.loc[1].result != np.NaN:
            h = "Tu salto horizontal ha mejorado en <b>{:10.4f}</b> metros"
            h = h.format(dfHor.loc[0].result-dfHor.loc[1].result)
        else: 
            h = 'No hay suficientes datos para ver si mejoraste, prueba saltar más :c'
    else:
        h = 'No hay suficientes datos para ver si mejoraste, prueba saltar más :c'
    
    if dfSpe.shape[0] > 1:
        if dfSpe.loc[0].result != np.NaN and dfSpe.loc[1].result != np.NaN:
            s = "Tu velocidad de sprint ha mejorado en <b>{:10.4f}</b> m/s"
            s = s.format(dfSpe.loc[0].result-dfSpe.loc[1].result)
        else: 
            s = 'No hay suficientes datos para ver si mejoraste, prueba correr más :c'
    else:
        s = 'No hay suficientes datos para ver si mejoraste, prueba correr más :c'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Informe Periódico MyCapability"
    message["From"] = sender_email
    
    #receiver_email = 'martin.salinas.scussolin@gmail.com'
    message["To"] = receiver_email

    html = codecs.open("mycap.html", 'r').read()
    html = html.format(vertical=v,horizontal=h,velocidad=s)

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
        f = int(f)*7

    # new date
    todayDate = datetime.date.today()

    newDate = abs((todayDate - reg).days)

    if newDate % f == 0 and row.email is not None and row.email != '':
        print('Se envia correo')
        sendEmail(row.email, row.id)
    else:
        print('fake')



conn = connect_ppg2()
q = 'SELECT * FROM Users ORDER BY id ASC'
df = create_df_from_ppg2(q,conn)

# print(df.loc[0].id, df.loc[0].username, df.loc[0].email, '\n')
# parseRow(df.loc[0])

for i in range(df.shape[0]):
    parseRow(df.loc[i])
