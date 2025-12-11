# ui/login_window.py
import customtkinter as ctk
import bcrypt
from database.models import Employee
from config.database import SessionLocal

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, callback):
        super().__init__()
        self.title("Connexion employé")
        self.geometry("400x500")
        self.resizable(False, False)
        self.callback = callback

        ctk.CTkLabel(self, text="Code PIN", font=("Helvetica", 24)).pack(pady=50)
        self.pin_entry = ctk.CTkEntry(self, show="*", font=("Helvetica", 32), width=200, justify="center")
        self.pin_entry.pack(pady=20)
        self.pin_entry.focus()

        ctk.CTkButton(self, text="Valider", command=self.check_pin, height=60).pack(pady=30)

        self.pin_entry.bind("<Return>", lambda e: self.check_pin())

    def check_pin(self):
        pin = self.pin_entry.get()
        db = SessionLocal()
        employee = db.query(Employee).first()  # pour l'exemple on prend le premier
        db.close()

        if employee and bcrypt.checkpw(pin.encode('utf-8'), employee.pin.encode('utf-8')):
            self.destroy()
            self.callback(employee)
        else:
            ctk.CTkLabel(self, text="Code incorrect", text_color="red").pack()
