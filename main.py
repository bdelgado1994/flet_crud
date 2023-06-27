from flet import *
import sqlite3

# Connect To Db
conn = sqlite3.connect("db/dbfood.db")
cur = conn.cursor()


class Youclass(UserControl):
    def __init__(self) -> None:
        super().__init__()
        # List Data
        self.all_data = Column()
        self.add_data = TextField(label="Add New Data")
        self.edit_data = TextField(label="Add New Data")

    # render to push to widget fetch
    def renderAll(self, e):
        cur.execute("SELECT * FROM mainan")
        conn.commit()
        my_data = cur.fetchall()

    # Insert a new name into database
    def addNew(self, e):
        cur.execute("INSERT INTO mainan (name) values (?)", [self.add_data.value])
        conn.commit()

    def build(self):
        print("Soy el build")
        return Column(
            [
                Text(value="CRUD SQLite", size=30),
                self.add_data,
                ElevatedButton("Add New Data", on_click=self.addNew),
            ]
        )


def main(page: Page):
    page.update()
    yourclass = Youclass()
    page.add(yourclass)


if __name__ == "__main__":
    app(target=main)
