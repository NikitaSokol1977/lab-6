import sqlite3
import tkinter as tk
from tkinter import messagebox


# --- Database functions ---

def create_database():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def register_user(username, password):
    """Registers a new user in the database."""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful!")
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return False


def authenticate_user(username, password):
    """Authenticates a user based on username and password."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


# --- UI functions ---

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login")

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.register_button = tk.Button(master, text="Register", command=self.open_registration)
        self.register_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if authenticate_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_registration(self):
        self.master.withdraw()  # Hide the login window
        registration_window = tk.Toplevel(self.master)
        RegistrationWindow(registration_window, self)


class RegistrationWindow:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        master.title("Registration")

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if register_user(username, password):
            self.master.destroy()
            self.login_window.master.deiconify()

    def on_closing(self):
        """Handles the closing of the registration window."""
        self.master.destroy()
        self.login_window.master.deiconify()  # Show the login window again


# --- Main ---

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()