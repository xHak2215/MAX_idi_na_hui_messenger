import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
 


def send_mail(html:str, recipients:str, text=None, server = 'smtp.gmail.com', user = 'example@mail.ru', password = 'password_mail', subject = 'код для подтверждения регистрации'):
    """
    ## отправка писем на электронную почту 
    
    **args:**
        - html - HTML код для красивого письма  
        - recipients - почта на которую совершается отправка письма  
        - text - текст письма (при наличии html не требуется ) 
        - server - почтовый smtp сервер 
        - user - пользователь от которого будет совершена отправка  
        - password - пароль пользователя   
        - subject - описание письма  
    """ 
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'служба регистрации <{user}>'
    msg['To'] = recipients
    msg['Reply-To'] = user
    msg['Return-Path'] = user
    msg['X-Mailer'] = 'Python/'+(python_version())
    
    if text:
        part_text = MIMEText(text, 'plain')
        msg.attach(part_text)
    
    if html:
        part_html = MIMEText(html, 'html')
        msg.attach(part_html)
    
    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(user, recipients, msg.as_string())
    mail.quit()

def user_identification_for_email(user_name:str, email:str):# на потом
    key=123
    html ='''
    <html>
    <head>

    <style>
    body {
        font-family: Arial; 
        background: #31241d; 
    } 

    .key {
    padding: 10px;
    display: inline-block;
    border: 3px solid #635e5c;

    text-align: center;
    font-style: italic;
    font-size: 25;
    }

    .centr {
        text-align: center;
    }
    </style>

    </head>
    <body>
    <div class="centr"><h2>привет {} !</h2></div>

    <h3>вот ваш код для подтверждения адреса электронной почты:</h3>

    <div class="key">{}</div>

    </body>
    </html>
    '''.format(user_name, key)
    
    send_mail(html, email)