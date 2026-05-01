from curling_league.identified_object import IdentifiedObject
from curling_league.exceptions import DuplicateOid

class League(IdentifiedObject):
    """Represents a curling league."""

    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._teams = []
        self._competitions = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        for existing_team in self.teams:
            if existing_team.oid == team.oid:
                raise DuplicateOid(team.oid)
        self.teams.append(team)

    def remove_team(self, team):
        for competition in self.competitions:
            if team in competition.teams_competing:
                raise ValueError(f"{team.name} is in a competition")
        if team in self.teams:
            self.teams.remove(team)

    def team_named(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team
        return None

    def add_competition(self, competition):
        for team in competition.teams_competing:
            if team not in self.teams:
                raise ValueError(f"{team.name} is not in this league")
        self.competitions.append(competition)


    def teams_for_member(self, member):
       return [team for team in self.teams if member in team.members]

    def competitions_for_team(self, team):
      return [c for c in self.competitions if team in c.teams_competing]

    def competitions_for_member(self, member):
        teams = self.teams_for_member(member)
        return [c for c in self.competitions
                if any(team in c.teams_competing for team in teams)]

    def __str__(self):
        """Returns league name with team and competition counts."""
        return f"{self.name}: {len(self.teams)} teams, {len(self.competitions)} competitions"