from curling_league.identified_object import IdentifiedObject
from curling_league.exceptions import DuplicateOid, DuplicateEmail

class Team(IdentifiedObject):
    """Represents a curling team."""

    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._members = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        for existing_member in self.members:
            if existing_member.oid == member.oid:
                raise DuplicateOid(member.oid)
            if existing_member.email is not None and member.email is not None:
                if existing_member.email.lower() == member.email.lower():
                    raise DuplicateEmail(member.email)
        self.members.append(member)

    def remove_member(self, member):
       if member in self.members:
            self.members.remove(member)

    def member_named(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    def send_email(self, emailer, subject, message):
        recipients = [member.email for member in self.members
                      if member.email is not None]
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        """Returns team name and number of members."""
        return f"{self.name}: {len(self.members)} members"