import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from .Config import SERVER, HTML

def send_email(server,fromaddr, destinataire, sujet, contenu_html):

    message = MIMEMultipart()

    html_message = MIMEText(contenu_html, 'html')
    message.attach(html_message)

    # Configurer les en-têtes du message
    message['From'] = fromaddr
    message['To'] = destinataire
    message['Subject'] = sujet
    message['Date'] = formatdate(localtime=True)

    try:
        server.sendmail(fromaddr, [destinataire], message.as_string())
        return True
    except smtplib.SMTPException as e:
        return False



def EmailSender(nom,destinataires,sujet,html_content):
    server = smtplib.SMTP(SERVER["SMTP_SERVER"], SERVER["SMTP_PORT"])
    server.connect(SERVER["SMTP_SERVER"], SERVER["SMTP_PORT"])
    server.ehlo()
    server.starttls()
    server.login(SERVER["EMAIL"], SERVER["PASSWORD"])

    sended = []
    fromaddr = nom+' <qYdDfdgYKEUZcc@outlook.fr>'

    for destinataire in destinataires:
        res = send_email(server,fromaddr,destinataire, sujet, html_content)
        if res:
            sended.append(destinataire)

    server.quit()
    return sended
