import smtplib
from email.mime.text import MIMEText


def send_mail(to_email, height):
    # Server configuration
    smtp_server = "smtp.server.com"
    port = 587  # For starttls
    user = "user"
    password = "password"
    from_email = "user@server.com"

    subject = "[Data Collector App] Thank you"
    body = "Thank you for taking part in this survey.<br> Your height is <strong>%s</strong>." % height

    # Create Message object
    message = MIMEText(body, 'html')
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email

    # connection will be automatically closed at the end of the indented code block
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()  # Secure the connection
        server.login(user, password)
        # server.sendmail(from_email, to_email, message)
        server.send_message(message)
