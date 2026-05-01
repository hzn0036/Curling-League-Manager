from curling_league.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):
    """Represents a member of a curling team."""

    def __init__(self, oid, name, email):
        super().__init__(oid)
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    def __str__(self):
        return f"{self.name}<{self.email}>"

    def send_email(self, emailer, subject, message):
        emailer.send_plain_email([self.email], subject, message)