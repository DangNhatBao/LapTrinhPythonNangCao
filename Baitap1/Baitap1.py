import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Hàm tính phương trình bậc 2
def solve_quadratic():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        if a == 0:
            entry_result_quadratic.delete(0, tk.END)
            entry_result_quadratic.insert(0, "Hệ số a phải khác 0")
            return
        
        delta = b**2 - 4*a*c
        entry_result_quadratic.delete(0, tk.END)
        
        if delta < 0:
            entry_result_quadratic.insert(0, "Phương trình vô nghiệm")
        elif delta == 0:
            x = -b / (2*a)
            entry_result_quadratic.insert(0, f"Nghiệm kép: x = {x:.2f}")
        else:
            x1 = (-b + delta**0.5) / (2*a)
            x2 = (-b - delta**0.5) / (2*a)
            entry_result_quadratic.insert(0, f"x1 = {x1:.2f}, x2 = {x2:.2f}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập hệ số hợp lệ")

# Hàm chuyển đổi từ cm sang m, kết quả là số nguyên
def convert_cm_to_m():
    try:
        cm_value = float(entry_cm.get())
        meters = int(cm_value / 100)  # Lấy phần nguyên của số mét
        entry_result_cm.delete(0, tk.END)
        entry_result_cm.insert(0, f"{meters} m")  # Hiển thị dưới dạng số nguyên
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("DangNhatBao GUI")
root.geometry("400x300")  # Đặt kích thước cho cửa sổ chính

# Tạo các tab
tab_control = ttk.Notebook(root)

# Tab 1: Tính phương trình bậc 2
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='PTB2')

label_a = ttk.Label(tab1, text="Nhập hệ số a:")
label_a.grid(column=0, row=0, padx=10, pady=10, sticky="W")
entry_a = ttk.Entry(tab1, width=20)
entry_a.grid(column=1, row=0, padx=10, pady=10)

label_b = ttk.Label(tab1, text="Nhập hệ số b:")
label_b.grid(column=0, row=1, padx=10, pady=10, sticky="W")
entry_b = ttk.Entry(tab1, width=20)
entry_b.grid(column=1, row=1, padx=10, pady=10)

label_c = ttk.Label(tab1, text="Nhập hệ số c:")
label_c.grid(column=0, row=2, padx=10, pady=10, sticky="W")
entry_c = ttk.Entry(tab1, width=20)
entry_c.grid(column=1, row=2, padx=10, pady=10)

btn_solve = ttk.Button(tab1, text="Giải phương trình", command=solve_quadratic)
btn_solve.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

entry_result_quadratic = ttk.Entry(tab1, width=30)
entry_result_quadratic.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

# Tab 2: Chuyển đổi đơn vị từ cm sang m
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Đổi đơn vị')

label_cm = ttk.Label(tab2, text="Nhập chiều dài (cm):")
label_cm.grid(column=0, row=0, padx=10, pady=10, sticky="W")
entry_cm = ttk.Entry(tab2, width=20)
entry_cm.grid(column=1, row=0, padx=10, pady=10)

btn_convert = ttk.Button(tab2, text="Chuyển đổi", command=convert_cm_to_m)
btn_convert.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

entry_result_cm = ttk.Entry(tab2, width=30)
entry_result_cm.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

# Tab 3: Canvas với 2 khung màu cam
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Hiển thị màu canvas')

tab3_frame = tk.Frame(tab3, bg='green')
tab3_frame.pack()

for orange_color in range(2):
    canvas = tk.Canvas(tab3_frame, width=150, height=80, highlightthickness=0, bg='red')
    canvas.grid(row=orange_color, column=orange_color)

# Hiển thị các tab
tab_control.pack(expand=1, fill="both")

# Chạy ứng dụng
root.mainloop()
