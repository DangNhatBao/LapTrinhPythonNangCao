import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from main_app import open_main_app  # Import the function from main_app.py

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đặng Nhật Bảo - Login")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # Login credentials
        self.valid_username = "admin"
        self.valid_password = "123"
        
        # Database connection info
        self.db_name = 'dbtest'
        self.user = 'postgres'
        self.password = '123456'
        self.host = 'localhost'
        self.port = '5432'

        # Create input fields
        self.username = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Tên tài khoản:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(frame, textvariable=self.username).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(frame, textvariable=self.password_var, show="*").grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(frame, text="Đăng nhập", command=self.authenticate).grid(row=2, columnspan=2, pady=10)
    
    def authenticate(self):
        user = self.username.get()
        pwd = self.password_var.get()
        
        if user == self.valid_username and pwd == self.valid_password:
            try:
                self.conn = self.connect_to_db()  # Save connection
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                self.root.destroy()
                open_main_app(self.conn)  # Pass connection to main app
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể kết nối cơ sở dữ liệu: {e}")
        else:
            messagebox.showerror("Lỗi", "Thông tin đăng nhập không hợp lệ!")

    def connect_to_db(self):
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return conn  # Return connection for later use
