from PySide6.QtWidgets import  QMessageBox, QFileDialog
from PySide6.QtUiTools import loadUiType
from curling_league.league_database import LeagueDatabase
from curling_league.team import Team

Ui_LeagueEditor, QtBaseDialog = loadUiType("league_editor.ui")


class LeagueEditor(QtBaseDialog, Ui_LeagueEditor):
    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._league = league
        self.add_team_button.clicked.connect(self.add_team_button_clicked)
        self.delete_team_button.clicked.connect(self.delete_team_button_clicked)
        self.edit_team_button.clicked.connect(self.edit_team_button_clicked)
        self.import_button.clicked.connect(self.import_button_clicked)
        self.export_button.clicked.connect(self.export_button_clicked)
        self.setWindowTitle(f"League Editor - {league.name}")
        self.update_ui()

    def get_selected_row(self):
        selection = self.team_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        try:
            return [str(team) for team in self._league.teams].index(selected_item.text())
        except ValueError:
            return -1

    def update_ui(self):
        row = self.get_selected_row()
        self.team_list_widget.clear()
        for team in self._league.teams:
            self.team_list_widget.addItem(str(team))
        if row != -1 and len(self._league.teams) > row:
            self.team_list_widget.setCurrentItem(
                self.team_list_widget.item(row))

    def warn(self, title, message):
        mb = QMessageBox(self)
        mb.setWindowTitle(title)
        mb.setText(message)
        mb.exec()

    def add_team_button_clicked(self):
        name = self.team_name_line_edit.text()
        if name == "":
            self.warn("Error", "Please enter a team name")
            return
        db = LeagueDatabase.instance()
        team = Team(db.next_oid(), name)
        self._league.add_team(team)
        self.team_name_line_edit.clear()
        self.update_ui()

    def delete_team_button_clicked(self):
        row = self.get_selected_row()
        if row == -1:
            self.warn("Error", "Please select a team to delete")
            return
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Delete Team")
        dialog.setText("Are you sure you want to delete this team?")
        sure_button = dialog.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
        dialog.addButton("No", QMessageBox.ButtonRole.RejectRole)
        dialog.exec()
        if dialog.clickedButton() == sure_button:
            self._league.remove_team(self._league.teams[row])
            self.update_ui()

    def edit_team_button_clicked(self):
        row = self.get_selected_row()
        if row == -1:
            self.warn("Error", "Please select a team to edit")
            return
        from curling_league.team_editor import TeamEditor
        team = self._league.teams[row]
        dialog = TeamEditor(team, self)
        dialog.exec()
        self.update_ui()

    def import_button_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Import Teams", "", "CSV Files (*.csv)")
        if filename:
            db = LeagueDatabase.instance()
            db.import_league_teams(self._league, filename)
            self.update_ui()

    def export_button_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Teams", "", "CSV Files (*.csv)")
        if filename:
            db = LeagueDatabase.instance()
            db.export_league_teams(self._league, filename)