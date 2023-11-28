import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from .Config import SERVER, HTML

def send_email(server,fromaddr, destinataire, sujet, contenu_html,url_fish):

    message = MIMEMultipart()

    contenu_html_avec_url = f"{contenu_html}<p>Consultez cette URL : <a href='{url_fish}'>lien</a><img src='http://localhost:8000/jaiouvertlemail' width='1' height='1' style='display:none;'></p>"

    # Créez l'objet MIMEText avec le contenu HTML mis à jour
    html_message = MIMEText(contenu_html_avec_url, 'html')
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



def EmailSender(campagne_id, nom,destinataires,sujet,html_content):
    server = smtplib.SMTP(SERVER["SMTP_SERVER"], SERVER["SMTP_PORT"])
    server.connect(SERVER["SMTP_SERVER"], SERVER["SMTP_PORT"])
    server.ehlo()
    server.starttls()
    server.login(SERVER["EMAIL"], SERVER["PASSWORD"])

    sended = []
    fromaddr = nom+' <qYdDfdgYKEUZcc@outlook.fr>'

    for destinataire in destinataires:
        stocked_uuid = uuid.uuid4()
        url = "http://localhost:8000/"+"campagnes/"+campagne_id+"?follow="+str(stocked_uuid)

        res = send_email(server,fromaddr,destinataire, sujet, html_content,url)
        if res:
            sended.append(stocked_uuid)

    server.quit()
    return sended
