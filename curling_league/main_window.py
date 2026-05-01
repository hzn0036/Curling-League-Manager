import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide6.QtUiTools import loadUiType

from curling_league.league_database import LeagueDatabase

Ui_MainWindow, QtBaseWindow = loadUiType("main_window.ui")


class MainWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._leagues = []
        self.add_button.clicked.connect(self.add_button_clicked)
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.edit_button.clicked.connect(self.edit_button_clicked)
        self.actionLoad.triggered.connect(self.load_triggered)
        self.actionSave.triggered.connect(self.save_triggered)

    def get_selected_row(self):
        selection = self.league_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        try:
            return [str(league) for league in self._leagues].index(selected_item.text())
        except ValueError:
            return -1

    def update_ui(self):
        row = self.get_selected_row()
        self.league_list_widget.clear()
        for league in self._leagues:
            self.league_list_widget.addItem(str(league))
        if row != -1 and len(self._leagues) > row:
            self.league_list_widget.setCurrentItem(
                self.league_list_widget.item(row))

    def warn(self, title, message):
        mb = QMessageBox(self)
        mb.setWindowTitle(title)
        mb.setText(message)
        mb.exec()

    def add_button_clicked(self):
        name = self.league_name_line_edit.text()
        if name == "":
            self.warn("Error", "Please enter a league name")
            return
        from curling_league.league import League
        db = LeagueDatabase.instance()
        league = League(db.next_oid(), name)
        db.add_league(league)
        self._leagues = db.leagues
        self.league_name_line_edit.clear()
        self.update_ui()

    def delete_button_clicked(self):
        row = self.get_selected_row()
        if row == -1:
            self.warn("Error", "Please select a league to delete")
            return
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Delete League")
        dialog.setText("Are you sure you want to delete this league?")
        sure_button = dialog.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
        dialog.addButton("No", QMessageBox.ButtonRole.RejectRole)

        dialog.exec()
        if dialog.clickedButton() == sure_button:
            db = LeagueDatabase.instance()
            db.remove_league(self._leagues[row])
            self.update_ui()

    def edit_button_clicked(self):
        row = self.get_selected_row()
        if row == -1:
            self.warn("Error", "Please select a league to edit")
            return
        from curling_league.league_editor import LeagueEditor
        league = self._leagues[row]
        dialog = LeagueEditor(league, self)
        dialog.exec()
        self.update_ui()

    def load_triggered(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Database", "", "Database Files (*.db)")
        if filename:
            LeagueDatabase.load(filename)
            self._leagues = LeagueDatabase.instance().leagues
            self.update_ui()

    def save_triggered(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Database", "", "Database Files (*.db)")
        if filename:
            LeagueDatabase.instance().save(filename)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())