from curling_league.identified_object import IdentifiedObject


class Competition(IdentifiedObject):
    """Represents a competition between two teams."""

    def __init__(self, oid, teams, location, date_time):
        super().__init__(oid)
        self._teams_competing = teams
        self._location = location
        self._date_time = date_time

    @property
    def teams_competing(self):
        return self._teams_competing

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, value):
        self._date_time = value

    def __str__(self):
        if self.date_time is None:
            return (f"Competition at {self.location} with "
                    f"{self.teams_competing[0].name} vs. {self.teams_competing[1].name}")
        else:
            date_str = self.date_time.strftime("%m/%d/%Y %H:%M")
            return (f"Competition at {self.location} on {date_str} with "
                    f"{self.teams_competing[0].name} vs. {self.teams_competing[1].name}")

    def send_email(self, emailer, subject, message):
        recipients = []
        for team in self.teams_competing:
            for member in team.members:
                if member.email is not None and member.email not in recipients:
                    recipients.append(member.email)
        emailer.send_plain_email(recipients, subject, message)