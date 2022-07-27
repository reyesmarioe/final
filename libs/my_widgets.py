import os
import math
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkcalendar import *

from json_parser import JsonParser

class MainApp:
    def __init__(self):
        self.file_expenses = 'expenses.json'
        self.file_data = 'data.json'
        self.jp = JsonParser()
        self.settings = self.jp.load_json(self.file_data, 'settings')
        self.expense_types = self.jp.load_json(self.file_data, 'expense_types')


    def get_daily_limit(self):
        return int(self.settings['daily_limit'])

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

    def create_input_expense_text(self, container, w = 30, h = 1):
        self.txtExpense = tk.Text(container, height = h, width = w)
        self.txtExpense.grid(row=0, column=1, sticky='NW', padx=10, pady=10)

    def create_display_expense_text(self, container, w = 30, h = 1):
        self.txtDisplayExpense = tk.Text(container, height = h, width = w)
        self.txtDisplayExpense.grid(row=0, column=1, sticky='NW', padx=10, pady=10)

    def create_display_limit_text(self, container, w = 30, h = 1):
        self.txtDisplayLimit = tk.Text(container, height = h, width = w)
        self.txtDisplayLimit.grid(row=2, column=1, sticky='NW', padx=10, pady=10)

    def calculate_daily_total(self, expenses, day):
        print(expenses)
        dailyTotal = 0
        if day not in expenses:
            return dailyTotal 

        for k,v in expenses[day].items():
            dailyTotal += int(v)

        print('Daily ', dailyTotal)
        return dailyTotal

    def calculate_daily_total_from_file(self, date):
        date = date.replace('/', '_')
        if os.path.exists(self.file_expenses):
            ef = self.jp.load_json(self.file_expenses)
            dailyTotal = self.calculate_daily_total(ef,date)
        else:
            dailyTotal = 0

        print('Calculate daily : ', dailyTotal)
        return str(dailyTotal)

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

        if os.path.exists(self.file_expenses):
            self.ef = self.jp.load_json(self.file_expenses)
            if date in self.ef:
                self.ef[date].update({expense:amount})
            else:
                self.ef[date] = {expense:amount}
        else:
            initDict = {}
            fileInit = True

            initDict[date] = d
            initDict[date][expense] = amount
            self.jp.write_section(expensesFile, initDict)
            
        t = self.get_daily_limit()
        e = self.calculate_daily_total(self.ef,date)
        print(t, e)
        if t < e:
            print(t, e)
        else:
            print("NOOOO")

        print('Daily total ', self.calculate_daily_total(self.ef,date))
        if self.get_daily_limit() >  self.calculate_daily_total(self.ef,date):
            print('You are OK')
        else:
            print('You have no more money!!!')

        if not fileInit:
            self.jp.write_section(self.file_expenses, self.ef)
        else:
            pass
        self.display_expenses()
        
    def display_expenses(self):
        self.txtDisplayExpense.delete(1.0, END)
        self.txtDisplayExpense.insert(tk.END, self.calculate_daily_total_from_file(self.calendar.get_date()))
            
    def get_expense(self):
        d = {}
        expense = self.combo_get_sel_item()
        date = str(self.calendar.get_date())
        date = date.replace('/', '_')

        self.ef = self.jp.load_json(self.file_expenses)
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

    def create_text_label(self, container, msg):
        return Label(container, textvariable=msg, relief=RAISED)

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

        # Expense input text
        self.create_input_expense_text(self.frameSetExpenses)

        
        self.btnSetExpenses = self.create_button(self.frameSetExpenses, 'Enter Expense', self.capture_expense) 
        self.btnSetExpenses.grid(row=18, column=0, padx=10, pady=10)


        self.msgDailyExpense = StringVar()
        self.lblDailyExpense = self.create_text_label(self.frameGetExpenses, self.msgDailyExpense)
        self.msgDailyExpense.set('Daily Expense : ')
        self.lblDailyExpense.grid(row=0, column=0, padx=10, pady=10)
        

        # Get expenses
        self.create_display_expense_text(self.frameGetExpenses, 20)
        self.txtDisplayExpense.insert(tk.END, self.calculate_daily_total_from_file(self.calendar.get_date()))

        self.msgDailyLimit = StringVar()
        self.lblDailyLimit = self.create_text_label(self.frameGetExpenses, self.msgDailyLimit)
        self.msgDailyLimit.set('Daily Limit : ')
        self.lblDailyLimit.grid(row=2, column=0, padx=0, pady=0)
        

        self.create_display_limit_text(self.frameGetExpenses, 20)
        self.txtDisplayLimit.insert(tk.END, self.get_daily_limit())


        self.btnGetExpenses = self.create_button(self.frameGetExpenses, 'Get Expenses', self.display_expenses) 
        self.btnGetExpenses.grid(row=18, column=0, padx=10, pady=10)
