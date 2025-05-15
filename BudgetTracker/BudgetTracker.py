import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime

# File paths
userDataFile = "users.json"
transaction_file_path = r"C:\BudgetTracker\transactions.txt"

# Ensure the users.json file exists
if not os.path.exists(userDataFile):
    with open(userDataFile, 'w') as f:
        json.dump({}, f)

# Ensure the directory for transactions exists
os.makedirs(os.path.dirname(transaction_file_path), exist_ok=True)

def loadUsers():
    with open(userDataFile, 'r') as f:
        return json.load(f)

def saveUsers(users):
    with open(userDataFile, 'w') as f:
        json.dump(users, f)

class BudgetTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Budget Tracker")
        self.geometry("500x600")
        self.transactions = []
        self.createLoginScreen()

    def createLoginScreen(self):
        self.clearScreen()
        ctk.CTkLabel(self, text="Budget Tracker Login", font=ctk.CTkFont(size=40, weight="bold")).pack(pady=70)
        ctk.CTkLabel(self, text="Username", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.usernameEntry = ctk.CTkEntry(self, width=300, justify="center")
        self.usernameEntry.pack(pady=(0, 10))
        ctk.CTkLabel(self, text="PIN", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.pinEntry = ctk.CTkEntry(self, show="*", width=300, justify="center")
        self.pinEntry.pack(pady=(0, 10))
        ctk.CTkButton(self, text=" Login", command=self.login,width=200, 
                      height=50,
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkButton(self, text="Register", command=self.createRegisterScreen,width=200, 
                      height=50,
                      font=ctk.CTkFont(size=16, weight="bold")).pack()

    def createRegisterScreen(self):
        self.clearScreen()
        ctk.CTkLabel(self, text="Register", font=ctk.CTkFont(size=40, weight="bold")).pack(pady=70)
        ctk.CTkLabel(self, text="New Username", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.newUsernameEntry = ctk.CTkEntry(self, width=300, justify="center")
        self.newUsernameEntry.pack(pady=(0, 10))
        ctk.CTkLabel(self, text="New PIN", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.newPinEntry = ctk.CTkEntry(self, show="*", width=300, justify="center")
        self.newPinEntry.pack()
        ctk.CTkButton(self, text="Submit", command=self.register, width=200, 
                      height=50,
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkButton(self, text="Back to Login", command=self.createLoginScreen, width=200, 
                      height=50,
                      font=ctk.CTkFont(size=16, weight="bold")).pack()

    def login(self):
        username = self.usernameEntry.get()
        pin = self.pinEntry.get()
        users = loadUsers()
        if username in users and users[username] == pin:
            messagebox.showinfo("Success", "Login successful!")
            self.createWelcomeScreen(username)
        else:
            messagebox.showerror("Error", "Invalid username or PIN")

    def register(self):
        username = self.newUsernameEntry.get()
        pin = self.newPinEntry.get()
        if not username or not pin:
            messagebox.showerror("Error", "All fields are required")
            return
        users = loadUsers()
        if username in users:
            messagebox.showerror("Error", "Username already exists")
        else:
            users[username] = pin
            saveUsers(users)
            messagebox.showinfo("Success", "Registration successful")
            self.createLoginScreen()

    def createWelcomeScreen(self, username):
        self.clearScreen()
        self.title(f"Budget Tracker - {username}")
        
        # Create a top frame for logout button
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10, anchor="ne")
        
        # Logout Button in the top right
        logout_button = ctk.CTkButton(top_frame, 
                      text="Logout", 
                      command=self.createLoginScreen,
                      width=100, 
                      height=30,
                      font=ctk.CTkFont(size=12, weight="bold"))
        logout_button.pack(side="right")
        
        ctk.CTkLabel(self, text=f"Welcome, {username}", font=ctk.CTkFont(size=40, weight="bold")).pack(pady=20)
        
        # Date Input - Using DateEntry from tkcalendar
        ctk.CTkLabel(self, text="Date", font=ctk.CTkFont(size=20, weight="bold")).pack()
        
        
        date_frame = ctk.CTkFrame(self, fg_color="gray")
        date_frame.pack(pady=(0, 10))
        
        self.dateEntry = DateEntry(
            date_frame, 
            width=70, 
            justify="center",
            height=40,
            background='darkblue', 
            foreground='white', 
            borderwidth=2,
            date_pattern='y-mm-dd'  # Format to match your original YYYY-MM-DD
        )
        self.dateEntry.pack()
        
        # Description Input
        ctk.CTkLabel(self, text="Description", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.descriptionEntry = ctk.CTkEntry(self, width=300, justify="center")
        self.descriptionEntry.pack(pady=(0, 10))
        
        # Amount Input
        ctk.CTkLabel(self, text="Amount", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.amountEntry = ctk.CTkEntry(self, width=300, justify="center")
        self.amountEntry.pack(pady=(0, 10))
        
        # Transaction Type Input
        ctk.CTkLabel(self, text="Transaction Type", font=ctk.CTkFont(size=20, weight="bold")).pack()
        self.typeCombo = ctk.CTkComboBox(self, values=["Income", "Expense"], width=300, justify="center")
        self.typeCombo.pack(pady=(0, 10))
        self.typeCombo.set("Income")
        
        # Buttons with consistent styling
        ctk.CTkButton(self, 
                      text="Add Transaction", 
                      command=self.addTransaction,
                      width=200, 
                      height=50,
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).pack(pady=5)
        ctk.CTkButton(self, 
                      text="View Transactions", 
                      command=self.viewTransactions,
                      width=200, 
                      height=50,
                      font=ctk.CTkFont(size=16, weight="bold")
                      ).pack(pady=5)
        
        # Transactions Display
        self.displayText = ctk.CTkTextbox(self, height=200, width=300)
        self.displayText.pack(pady=10)
        
    def addTransaction(self):
        dateStr = self.dateEntry.get()
        description = self.descriptionEntry.get()
        amountStr = self.amountEntry.get()
        transactionType = self.typeCombo.get()
        try:
            date = datetime.strptime(dateStr, "%Y-%m-%d").date()
            amount = float(amountStr)
            if transactionType == "Income":
                amount = abs(amount)
            elif transactionType == "Expense":
                amount = -abs(amount)
            else:
                raise ValueError("Invalid transaction type.")
            transaction = {
                "date": date,
                "description": description,
                "amount": amount,
                "type": transactionType
            }
            self.transactions.append(transaction)
            self.clearTransactionFields()
            messagebox.showinfo("Success", "Transaction added successfully!")

            # Save to file in C:\BudgetTracker\transactions.txt
            with open(transaction_file_path, "a") as f:
                f.write(f"{date} | {transactionType} | {description} | {amount:.2f}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")

    def viewTransactions(self):
        self.displayText.delete("1.0", "end")
        if not self.transactions:
            self.displayText.insert("end", "No transactions to display.\n")
            return
        for transaction in self.transactions:
            date = transaction["date"].strftime("%Y-%m-%d")
            desc = transaction["description"]
            amount = transaction["amount"]
            tType = transaction["type"]
            self.displayText.insert("end", f"{date} | {tType} | {desc} | {amount:.2f}\n")

    def clearTransactionFields(self):
        self.dateEntry.delete(0, "end")
        self.descriptionEntry.delete(0, "end")
        self.amountEntry.delete(0, "end")
        self.typeCombo.set("Income")

    def clearScreen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = BudgetTrackerApp()
    app.mainloop()
