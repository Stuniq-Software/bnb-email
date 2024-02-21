from typing import Tuple, Optional
from util import Mailer, CustomLogger



class MailRepository:
    mailer: Mailer
    logger: CustomLogger

    def __init__(self, mailer: Mailer, logger: CustomLogger) -> None:
        self.mailer = mailer
        self.logger = logger
    
    def send_mail(self, mail_type: str, data: dict) -> Tuple[bool, str]:
        to = data.get("to", None)
        subject = data.get("subject", None)
        attachments = data.get("attachments", [])
        keys_to_pop = ["to", "subject", "attachments"]
        for key in keys_to_pop:
            data.pop(key, None)
        
        try:
            success = self.mailer.send_mail(mail_type, to, subject, data, self.logger, attachments)
            if not success:
                return False, "Failed to send mail"
            self.logger.success("Mail sent successfully")
            return True, "Mail sent successfully"
        except Exception as e:
            self.logger.exception(str(e), _print=True)
            return False, str(e)