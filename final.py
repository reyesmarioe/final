import sys

sys.path.append('libs')
from my_widgets import MainApp

if __name__ == '__main__':
    app = MainApp()
    app.create_main_window(800, 650, 'Expense tracker')
    app.create_app_gui()

    app.main_loop()
