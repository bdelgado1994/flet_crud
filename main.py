from flet import *
import sqlite3

# Connect To Db
conn = sqlite3.connect("db/dbfood.db", check_same_thread=False)
cur = conn.cursor()


class Youclass(UserControl):
    def __init__(self) -> None:
        super().__init__()
        # List Data
        self.all_data = Column()
        self.add_data = TextField(label="Add New Data")
        self.edit_data = TextField(label="Edit data")

    # Life Cicle For Call Render
    def did_mount(self):
        self.renderAll()

    def build(self):
        return Column(
            [
                Text(value="CRUD SQLite", size=30),
                self.add_data,
                ElevatedButton(
                    "Add New Data",
                    on_click=self.addNew,
                    color="white",
                    bgcolor="blue",
                ),
                # See All Data
                self.all_data,
            ]
        )

    #
    def openYouAction(self, e):
        # Get Id From Data
        id_edit = e.control.subtitle.value
        # Edit TextEdit To Value Name From List Title
        self.edit_data.value = e.control.title.value
        # Open Alert Dialog
        alert_dialog = AlertDialog(
            modal=True,
            title=Text(f"Edit id: {id_edit}"),
            content=self.edit_data,
            actions=[
                # Delete Data
                ElevatedButton(
                    text="Delete Data",
                    color="white",
                    bgcolor="red",
                    on_click=lambda e: self.proccesDelete(
                        id_edit, alert_dialog, self.edit_data.value
                    ),
                ),
                # Edit Data
                ElevatedButton(
                    text="Update Data",
                    color="white",
                    bgcolor="green",
                    on_click=lambda e: self.proccessEdit(
                        id_edit, self.edit_data.value, alert_dialog
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.SPACE_BETWEEN,
        )
        # Show Dialog
        self.page.dialog = alert_dialog
        alert_dialog.open = True
        # Update Page for Show Alert
        self.page.update()

    # render to push to widget fetch
    def renderAll(self):
        cur.execute("SELECT * FROM mainan")
        # conn.commit()
        my_data = cur.fetchall()
        for x in my_data:
            self.all_data.controls.append(
                ListTile(
                    leading=Icon(icons.CHECK, color="green"),
                    # GEt Name
                    title=Text(x[1]),
                    # Get ID
                    subtitle=Text(x[0]),
                    on_click=self.openYouAction,
                )
            )
        self.update()

    # Insert a new name into database
    def addNew(self, e):
        new_data = self.add_data.value
        cur.execute("INSERT INTO mainan (name) values (?)", [self.add_data.value])
        conn.commit()
        self.add_data.value = ""
        self.add_data.focus()
        # Clear all DAta
        self.all_data.controls.clear()
        self.renderAll()
        added = SnackBar(
            Text(f"{new_data} was added", color="white", size=20),
            bgcolor="blue",
        )
        self.page.snack_bar = added
        added.open = True
        self.page.update()

    def proccessEdit(self, id_edit, edit_data, alert_dialog: AlertDialog):
        cur.execute("UPDATE mainan SET name=? WHERE id= ?", (edit_data, id_edit))
        conn.commit()
        # Close You Alert
        alert_dialog.open = False
        # CALL renderAll FUNCTION AGAIN FOR REFRESH THE DATA
        self.all_data.controls.clear()
        self.renderAll()
        update = SnackBar(
            Text(f"Data {id_edit} was updated", color="white", size=20),
            bgcolor="green",
        )
        self.page.snack_bar = update
        update.open = True
        self.page.update()

    def proccesDelete(self, id_edit, alert_dialog: AlertDialog, edit_data):
        cur.execute("DELETE FROM mainan WHERE id= ?", [id_edit])
        conn.commit()
        alert_dialog.open = False
        self.all_data.controls.clear()
        self.renderAll()
        delete = SnackBar(
            Text(f"{edit_data} was deleted", color="white", size=20),
            bgcolor="red",
        )
        self.page.snack_bar = delete
        delete.open = True
        self.page.update()


def main(page: Page):
    page.update()
    yourclass = Youclass()
    page.theme_mode = "light"
    page.add(yourclass)


if __name__ == "__main__":
    app(target=main)
