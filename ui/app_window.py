import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from core.Scannerread import Scanner
#创建窗口
Myapp = tk.Tk()
Myapp.title("recall files")
Myapp.geometry("600x400")
Myapp.resizable(False, False)
Myapp.configure(background="#ffffff")
#窗口内组件框架
frame = tk.Frame(Myapp)
frame.pack(pady=10)
#组件
title_label = ttk.Label(frame, text="Files path")
entry_label = ttk.Entry(frame, width=50)
#位置
frame.place(x=200,y=300)

Myapp.mainloop()
