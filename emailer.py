from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def sendEmail(message, toAddress):
    '''Send message to one or multiple addresses'''
    if isinstance(toAddress, list):
        for address in toAddress:
            msg = MIMEText(message)
            msg["From"] = "donotreply@gtech.com"
            msg["To"] = address
            msg["Subject"] = "Update on mail server (Attention Required)"
            p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
            p.communicate(msg.as_string())
    else:
        msg = MIMEText(message)
        msg["From"] = "donotreply@gtech.com"
        msg["To"] = toAddress
        msg["Subject"] = "Update on mail server (Attention Required)"
        p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        p.communicate(msg.as_string())

