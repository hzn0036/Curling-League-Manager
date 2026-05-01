import csv
import pickle
import os

from curling_league.team_member import TeamMember
from curling_league.team import Team


class LeagueDatabase:
    """Singleton database for managing curling leagues."""
    _sole_instance = None

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def __init__(self):
        self._leagues = []
        self._last_oid = 0

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            backup_file = file_name + ".backup"
            try:
                with open(backup_file, mode="rb") as f:
                    cls._sole_instance = pickle.load(f)
            except Exception as backup_error:
                print(f"Error loading backup file {backup_file}: {backup_error}")
                cls._sole_instance = cls()

    def add_league(self, league):
        self._leagues.append(league)

    def remove_league(self, league):
        if league in self._leagues:
            self._leagues.remove(league)

    def league_named(self, name):
        for league in self._leagues:
            if league.name == name:
                return league
        return None

    @property
    def leagues(self):
        return self._leagues

    def next_oid(self):
        self._last_oid = self._last_oid + 1
        return self._last_oid

    def save(self, file_name):
        try:
            if os.path.exists(file_name):
                os.rename(file_name, file_name + ".backup")
            with open(file_name, mode="wb") as f:
                pickle.dump(self, f)
        except Exception as e:
            print(f"Error saving {file_name}: {e}")

    def import_league_teams(self, league, file_name):
        try:
            with open(file_name, newline='', encoding="utf-8") as f:
                reader = csv.reader(f)

                next(reader)
                for row in reader:
                    team_name = row[0]
                    member_name = row[1]
                    member_email = row[2]

                    team = league.team_named(team_name)
                    if team is None:
                        team = Team(self.next_oid(), team_name)
                        league.add_team(team)

                    member = TeamMember(self.next_oid(), member_name, member_email)
                    team.add_member(member)
        except Exception as e:
            print(f"Error importing {file_name}: {e}")

    def export_league_teams(self, league, file_name):
        try:
            with open(file_name, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)

                # write header
                writer.writerow(["Team name", "Member name", "Member email"])

                # write data
                for team in league.teams:
                    for member in team.members:
                        writer.writerow([team.name, member.name, member.email])

        except Exception as e:
            print(f"Error exporting teams to {file_name}: {e}")
