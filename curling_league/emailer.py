import yagmail


class Emailer:
    """A single class for sending emails."""

    sender_address = None
    _sole_instance = None

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        yag = yagmail.SMTP(self.sender_address)
        for recipient in recipients:
            yag.send(to=recipient, subject=subject, contents=message)
