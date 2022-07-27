import os
import math
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkcalendar import *

from json_parser import JsonParser

class MainApp:
    def __init__(self):
        self.jp = JsonParser()
        self.settings = self.jp.load_json('data.json', 'settings')
        self.expense_types = self.jp.load_json('data.json', 'expense_types')


    def get_daily_limit(self):
        print('Daily limit : ',  float(self.settings['daily_limit']))
        return float(self.settings['daily_limit'])

    def create_main_window(self, width, height, title = 'Some App'):
        #print('create_main_window')
        self.window = Tk()
        self.window_size = '{}x{}'.format(width,height)
        self.window.title(title)
        self.window.geometry(self.window_size)

    def main_loop(self):
        #print('main loop')
        self.window.mainloop()

    def create_calendar(self, mode = 'day', DAY = 1, MONTH = 1, YEAR = 2000):
        self.calendar= Calendar(self.window, selectmode=mode,year = YEAR, month = MONTH, day = DAY)
        self.calendar.pack(pady=20)


    def get_date(self):
        self.date = self.calendar.get_date()
        #print(self.date)
        expense = self.combo_get_sel_item()
        print('Daily expense for day : ' + self.date + ' for ' + expense + ' is ')



    def create_button(self, container, txt, func):
        return Button(container, text=txt, command=lambda: func())
       
    def create_combo(self, container, items):
        self.combo = ttk.Combobox(container)
        self.combo['values'] = items
        self.combo.current(1)
        self.combo.grid(row=0, column=0, sticky='NW', padx=10, pady=10)

    def combo_get_sel_item(self):
        return self.combo['values'][self.combo.current()]

    def create_input_text(self, container, w = 30, h = 1):
        self.txtExpense = tk.Text(container, height = h, width = w)
        self.txtExpense.grid(row=0, column=1, sticky='NW', padx=10, pady=10)

    def calculate_daily_total(self, expensesDay):
        dailyTotal = 0
        for k,v in expensesDay.items():
            #print(k, v)
            dailyTotal += float(v)

        return dailyTotal


    def capture_expense(self):
        fileInit = False
        d = {}
        expense = self.combo_get_sel_item()
        amount = self.txtExpense.get('1.0', END).strip('\n\r')
        print(amount)
        #amount = 100.00

        date = str(self.calendar.get_date())
        date = date.replace('/', '_')
        #print(date)
        d[expense] = amount

        expensesFile = 'expenses.json'
        if os.path.exists(expensesFile):
            self.ef = self.jp.load_json('expenses.json')
            if date in self.ef:
                self.ef[date].update({expense:amount})
            else:
                self.ef[date] = {expense:amount}
            

            #print(self.ef)
        else:
            initDict = {}
            fileInit = True
            #self.ef = open(expensesFile, 'w')

            initDict[date] = d
            initDict[date][expense] = amount
            #self.ef.write(json.dumpinitDict)
            self.jp.write_section(expensesFile, initDict)
            
        print('Daily total ', self.calculate_daily_total(self.ef[date]))
        if math.isclose(self.get_daily_limit(), self.calculate_daily_total(self.ef[date])):
            print('You are OK')
        else:
            print('You have no more money!!!')

        if not fileInit:
            self.jp.write_section('expenses.json', self.ef)
        else:
            pass
            #self.ef.close()
            
    def get_expense(self):
        d = {}
        expense = self.combo_get_sel_item()
        date = str(self.calendar.get_date())
        date = date.replace('/', '_')

        self.ef = self.jp.load_json('expenses.json')
        #print('in get', self.ef)
        if date in self.ef:
            print(self.ef[date])
        else:
            print('No expense found for this day: ' + str(self.calendar.get_date()))

    def create_label_frame(self, container, frameText, fw, fh):
        if frameText is not None:
            frame = LabelFrame(container, text=frameText)
        else:
            frame = LabelFrame(container)

        container.update_idletasks()
        frame.configure(width=fw , height=fh)
        frame.grid_propagate(0)
        frame.grid_columnconfigure(0, weight=1)
        return frame

    def create_caledar_frame(self, container):
        self.calendar = Calendar(container, mode = 'day', DAY = 1, MONTH = 1, YEAR = 2000)
        self.calendar.pack(padx = 10, pady = 10, fill = 'both', expand = True)


    def create_app_gui(self):
        self.create_caledar_frame(self.window)

        # To enter expenses
        self.window.update_idletasks()
        self.frameSetExpenses = self.create_label_frame(self.window, 'Enter Expenses', (self.window.winfo_width() - 20) / 2, 700)
        self.frameSetExpenses.pack(padx = 10, pady = 10, side = LEFT)

        # To get expenses
        self.frameGetExpenses = self.create_label_frame(self.window, 'Daily Expenses', (self.window.winfo_width() - 20) / 2, 700)
        self.frameGetExpenses.pack(padx = 10, pady = 10, side = RIGHT)

        # Combo box 
        self.create_combo(self.frameSetExpenses, self.expense_types)

        self.create_input_text(self.frameSetExpenses)

        self.btnGetExpenses = self.create_button(self.frameSetExpenses, 'Enter Expense', self.capture_expense) 
        self.btnGetExpenses.grid(row=18, column=0, padx=10, pady=10)

