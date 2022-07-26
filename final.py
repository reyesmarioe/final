from tkinter import *
from tkinter import ttk
from tkcalendar import *
import sys


sys.path.append('libs')
from json_parser import JsonParser
from my_utils import MyUtils


class MainApp:
    def __init__(self):
        self.jp = JsonParser()
        self.utils = MyUtils()
        self.utils.touch_file('expenses.json', 'a+')


    def create_main_window(self, width, height, title = 'Some App'):
        print('create_main_window')
        self.window = Tk()
        self.window_size = '{}x{}'.format(width,height)
        self.window.title(title)
        self.window.geometry(self.window_size)

    def main_loop(self):
        print('main loop')
        self.window.mainloop()

    def create_calendar(self, mode = 'day', DAY = 1, MONTH = 1, YEAR = 2000):
        self.cal= Calendar(self.window, selectmode=mode,year = YEAR, month = MONTH, day = DAY)
        self.cal.pack(pady=20)


    def get_date(self):
        self.date = self.cal.get_date()
        print(self.date)
        expense = self.combo_get_sel_item()
        print('Daily expense for day : ' + self.date + ' for ' + expense + ' is ')



    def create_button(self, txt, func):
        self.btn = Button(self.window, text=txt, command=lambda: func())
        self.btn.pack(pady=20)
       
    def create_combo(self, items):
        self.combo = ttk.Combobox(self.window)
        self.combo['values'] = items
        self.combo.current(1)
        self.combo.pack()

    def combo_get_sel_item(self):
        return self.combo['values'][self.combo.current()]


    def capture_expense(self):
        d = {}
        expense = self.combo_get_sel_item()
        amount = 100.00

        date = str(self.cal.get_date())
        date = date.replace('/', '_')
        print(date)
        d[expense] = amount

        self.ef = self.jp.load_json('expenses.json')
        print(type(self.ef))
        print(self.ef)
        self.ef[expense] = amount
        print(self.ef)
            


#lbl = Label(window, text="Hello")

#lbl.grid(column=0, row=0)


#combo = ttk.Combobox(window)

#combo['values']= (1, 2, 3, 4, 5, "Text")

#combo.current(1) #set the selected item

#combo.grid(column=0, row=0)
# Add Calendar


if __name__ == '__main__':
    # Instance of parse
    jp = JsonParser()

    # Retrieve app config data
    settings = jp.load_json('data.json', 'settings')
    expense_types = jp.load_json('data.json', 'expense_types')

    app = MainApp()
    app.create_main_window(800, 650, 'Expense tracker')
    app.create_calendar()
    app.create_button('Get daily expense', app.get_date)
    app.create_button('Set daily expense', app.capture_expense)
    app.create_combo(expense_types)
    app.main_loop()
