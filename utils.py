import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para enviar email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Configura o email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Adiciona o corpo do email
        msg.attach(MIMEText(body, 'plain'))
        
        # Conecta ao servidor SMTP e envia o email
        server = smtplib.SMTP('smtp.gmail.com', 587) # Para Gmail
        # server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print("Email com os erros foi enviado.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")