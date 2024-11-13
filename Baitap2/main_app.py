import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Treeview
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root, conn):  # Receive connection from LoginWindow
        self.root = root    
        self.root.title("Đặng Nhật Bảo - Database App")
        self.root.geometry("700x600")
        
        # Save connection and create cursor
        self.conn = conn
        self.cur = self.conn.cursor()  

        # Create a main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create a query section
        query_frame = tk.LabelFrame(self.root, text="Hoạt động dữ liệu")
        query_frame.pack(padx=10, pady=10, fill="x")

        self.table_name = tk.StringVar(value='sinhvien')

        tk.Label(query_frame, text="Bảng:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Tải danh sách", command=self.load_data).grid(row=1, columnspan=2, pady=5)

        # Insert section
        insert_frame = tk.LabelFrame(self.root, text="Tùy chọn sinh viên")
        insert_frame.pack(padx=10, pady=10, fill="x")

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()
        self.column3 = tk.StringVar()  # For "nganh"
        self.column4 = tk.IntVar()     # For "namsinh"

        tk.Label(insert_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Mssv:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Ngành:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(insert_frame, textvariable=self.column3).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Năm sinh:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(insert_frame, textvariable=self.column4).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Thêm sinh viên", command=self.insert_data).grid(row=4, columnspan=2, pady=10)

        # Search section
        search_frame = tk.LabelFrame(self.root, text="Tìm sinh viên")
        search_frame.pack(padx=10, pady=10, fill="x")

        self.search_value = tk.StringVar()

        tk.Label(search_frame, text="Nhập dữ liệu sinh viên cần tìm:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(search_frame, textvariable=self.search_value).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(search_frame, text="Tìm", command=self.search_data).grid(row=1, columnspan=2, pady=5)

        # Create a Treeview for displaying data
        self.tree = ttk.Treeview(self.root, columns=("MSSV", "Ho Ten", "Nganh", "Nam Sinh"), show="headings")

        self.tree.heading("MSSV", text="MSSV")
        self.tree.column("MSSV", width=100)

        self.tree.heading("Ho Ten", text="Ho Ten")
        self.tree.column("Ho Ten", width=150)

        self.tree.heading("Nganh", text="Nganh")
        self.tree.column("Nganh", width=150)

        self.tree.heading("Nam Sinh", text="Nam Sinh")
        self.tree.column("Nam Sinh", width=100)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Add a scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Clear existing data in Treeview
            for row in rows:
                self.tree.insert("", tk.END, values=row)  # Insert row into Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, mssv, nganh, namsinh) VALUES (%s, %s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get(), self.column3.get(), self.column4.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
            self.load_data()  # Optionally refresh data after insert
        except Exception as e:
            self.conn.rollback()  # Rollback transaction on error
            messagebox.showerror("Lỗi", f"Thêm sinh viên thất bại: {e}")

    def search_data(self):
        try:
            search_value = self.search_value.get()
            search_query = sql.SQL("SELECT * FROM {} WHERE hoten ILIKE %s OR CAST(mssv AS TEXT) ILIKE %s OR nganh ILIKE %s OR CAST(namsinh AS TEXT) ILIKE %s").format(sql.Identifier(self.table_name.get()))
            search_pattern = f"%{search_value}%"
            self.cur.execute(search_query, (search_pattern, search_pattern, search_pattern, search_pattern))
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Tìm kiếm không thành công: {e}")

def open_main_app(conn):
    root = tk.Tk()
    app = DatabaseApp(root, conn)
    root.mainloop()
