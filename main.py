import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from pymysql.cursors import DictCursor


class Database:
    connection_data = dict(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='exam_1'
    )

    def __init__(self):
        self.db = pymysql.connect(**self.connection_data, cursorclass=DictCursor)
        self.cursor = self.db.cursor()
        self.init_db()

    def init_db(self):
        query = 'CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY AUTO_INCREMENT, first_name VARCHAR(100), last_name VARCHAR(100), surname VARCHAR(100))'
        self.cursor.execute(query, ())
        self.db.commit()

    def get_records(self):
        query = 'SELECT * FROM users'
        self.cursor.execute(query, ())
        return self.cursor.fetchall()

    def add_record(self, first_name, last_name, surname):
        query = 'INSERT INTO users (first_name, last_name, surname) VALUES (%s, %s, %s)'
        args = (first_name, last_name, surname)
        self.cursor.execute(query, args)
        self.db.commit()


class AddProductView(tk.Toplevel):
    last_name_entry: tk.Entry
    first_name_entry: tk.Entry
    surname_entry: tk.Entry

    database = Database()

    def __init__(self, on_destroy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_destroy = on_destroy
        self.init_ui()

    def init_ui(self):
        title_label = tk.Label(self, text='Добавить пользователя')
        title_label.place(anchor='center')
        title_label.grid(row=0, column=0)

        tk.Label(self, text='Фамилия: ').grid(row=1, column=0)
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self, text='Имя: ').grid(row=2, column=0)
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(row=2, column=1)

        tk.Label(self, text='Отчество: ').grid(row=3, column=0)
        self.surname_entry = tk.Entry(self)
        self.surname_entry.grid(row=3, column=1)

        tk.Button(self, text='Добавить', command=self.add_value).grid(row=4)

    def destroy(self) -> None:
        if self.on_destroy:
            self.on_destroy()
        super().destroy()

    def add_value(self):
        first_name, last_name, surname = self.first_name_entry.get(), self.last_name_entry.get(), self.surname_entry.get()
        self.database.add_record(first_name, last_name, surname)
        messagebox.showinfo('Успех', 'Данные в БД обновлены!')
        self.destroy()



class MainView:
    tree: ttk.Treeview

    tree_columns = dict(
        id='ID',
        first_name='Имя',
        last_name='Фамилия',
        surname='Отчество'
    )

    database = Database()

    def __init__(self, root: tk.Tk = None):
        self.root = tk.Tk() if not root else root
        self.root.title("Матвеев К.Д")
        self.root.geometry('800x400')
        self.init_ui()

    def build_tree(self):
        columns = tuple(self.tree_columns.keys())
        tree = ttk.Treeview(self.root,
                            columns=columns,
                            show='headings')

        for key, heading in self.tree_columns.items():
            tree.heading(key, text=heading)

        self.update_tree(tree)
        return tree

    def update_tree(self, tree: ttk.Treeview = None):
        if not tree:
            tree = self.tree

        for item in tree.get_children():
            tree.delete(item)

        database_records = self.database.get_records()
        for index, record in enumerate(database_records):
            tree.insert("", index, values=tuple(record.values()))

    def to_add_view(self):
        AddProductView(on_destroy=None)


    def init_ui(self):
        self.tree = self.build_tree()
        self.tree.grid(row=0, column=0)
        self.tree.place(x=10, y=10)

        tk.Button(self.root, text='Добавить', command=self.to_add_view).place(x=10, y=250)
        tk.Button(self.root, text='Обновить', command= lambda a=self: a.update_tree()).place(x=100, y=250)


    def mainloop(self):
        return self.root.mainloop()


if __name__ == '__main__':
    main = MainView()
    main.mainloop()