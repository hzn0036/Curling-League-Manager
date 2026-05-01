from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import loadUiType
from curling_league.league_database import LeagueDatabase
from curling_league.team_member import TeamMember

Ui_TeamEditor, QtBaseDialog = loadUiType("team_editor.ui")


class TeamEditor(QtBaseDialog, Ui_TeamEditor):
    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._team = team
        self.add_member_button.clicked.connect(self.add_member_button_clicked)
        self.delete_member_button.clicked.connect(self.delete_member_button_clicked)
        self.update_member_button.clicked.connect(self.update_member_button_clicked)
        self.setWindowTitle(f"Team Editor - {team.name}")
        self.update_ui()

    def get_selected_row(self):
        selection = self.member_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        try:
            return [str(member) for member in self._team.members].index(selected_item.text())
        except ValueError:
            return -1

    def update_ui(self):
        row = self.get_selected_row()
        self.member_list_widget.clear()
        for member in self._team.members:
            self.member_list_widget.addItem(str(member))
        if row != -1 and len(self._team.members) > row:
            self.member_list_widget.setCurrentItem(
                self.member_list_widget.item(row))

    def warn(self, title, message):
        mb = QMessageBox(self)
        mb.setWindowTitle(title)
        mb.setText(message)
        mb.exec()

    def add_member_button_clicked(self):
        name = self.name_line_edit.text()
        email = self.email_line_edit.text()
        if name == "" or email == "":
            self.warn("Error", "Please enter both name and email")
            return
        db = LeagueDatabase.instance()
        member = TeamMember(db.next_oid(), name, email)
        self._team.add_member(member)
        self.name_line_edit.clear()
        self.email_line_edit.clear()
        self.update_ui()

    def delete_member_button_clicked(self):
        row = self.get_selected_row()
        if row == -1:
            self.warn("Error", "Please select a member to delete")
            return
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Delete Member")
        dialog.setText("Are you sure you want to delete this member?")
        sure_button = dialog.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
        dialog.addButton("No", QMessageBox.ButtonRole.RejectRole)
        dialog.exec()
        if dialog.clickedButton() == sure_button:
            self._team.remove_member(self._team.members[row])
            self.update_ui()

    def update_member_button_clicked(self):
        row = self.get_selected_row()
        if row == -1:
            self.warn("Error", "Please select a member to update")
            return
        name = self.name_line_edit.text()
        email = self.email_line_edit.text()
        if name == "" or email == "":
            self.warn("Error", "Please enter both name and email")
            return
        member = self._team.members[row]
        member.name = name
        member.email = email
        self.name_line_edit.clear()
        self.email_line_edit.clear()
        self.update_ui()