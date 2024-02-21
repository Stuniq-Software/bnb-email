import smtplib, ssl, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Tuple
from string import Template
from .logger import CustomLogger

BASE_DIR = Path(__file__).parent.parent

mail_templates = {
    'welcome': BASE_DIR / 'template' / 'welcome-mail.html',
    'invoice': BASE_DIR / 'template' / 'invoice-mail.html',
    'verification': BASE_DIR / 'template' / 'verification-mail.html',
    'reset_password': BASE_DIR / 'template' / 'reset-password-mail.html'
}


class Mailer:
    def __init__(self) -> None:
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.port = os.getenv("SMTP_PORT")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("SENDER_PASSWORD")
        self.context = ssl.create_default_context()
    
    def _attach_file(self, email_msg: MIMEMultipart, file: Path) -> None:
        with open(file, "rb") as f:
            part = MIMEApplication(f.read(), Name=file.name)
        part["Content-Disposition"] = f'attachment; filename="{file.name}"'
        email_msg.attach(part)

    def _generate_body_from_template(self, mail_type: str, data: dict) -> str:
        if mail_type not in mail_templates:
            raise ValueError(f"Mail type '{mail_type}' not found")
        
        with open(mail_templates[mail_type], "r") as f:
            template = Template(f.read())
            return template.substitute(data)

    def _parse_mail(self, mail_type: str, data: dict, to: str, subject: str, attachments: Tuple[Path]) -> str:
        try:
            email_msg = MIMEMultipart()
            email_msg["From"] = self.sender_email
            email_msg["To"] = to
            email_msg["Subject"] = subject

            body = self._generate_body_from_template(mail_type, data)

            email_msg.attach(MIMEText(body, "html"))

            for attachment in attachments:
                self._attach_file(email_msg, attachment)
            
            return email_msg.as_string()
        
        except Exception as e:
            raise e


    def send_mail(self, mail_type: str, to: str, subject: str, data: dict, logger: CustomLogger, attachments: Tuple[Path] = []) -> bool:
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                server.login(self.sender_email, self.password)

                body = self._parse_mail(mail_type, data, to, subject, attachments)
                server.sendmail(self.sender_email, to, body)
                return True
        except Exception as e:
            logger.exception(str(e))
            return False
        