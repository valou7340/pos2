# main.py
import customtkinter as ctk
from database.seed_data import init_db
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main():
    init_db()  # Crée la DB + données de démo au premier lancement

    app = ctk.CTk()
    app.withdraw()  # cacher la fenêtre principale

    def on_login_success(employee):
        app.deiconify()
        main_win = MainWindow(employee)
        main_win.protocol("WM_DELETE_WINDOW", app.destroy)
        app.mainloop()

    LoginWindow(on_login_success)
    app.mainloop()

if __name__ == "__main__":
    main()
