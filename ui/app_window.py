from sys import exception

import customtkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from core.Scannerread import Scanner
#设置主题风格
tk.set_appearance_mode("System")
tk.set_default_color_theme("blue")
class Application(tk.CTk):
    def __init__(self):
        super().__init__()

#窗口
        self.title("recall-files")
        self.geometry("600x500")
        self.history = []
#侧边栏
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
#侧边栏控制
        self.sidebar_frame =(tk.CTkFrame(self,width=160,corner_radius=0))
        self.sidebar_frame.grid(row=0,column=0,sticky="nsew")
        self.logo_label = tk.CTkLabel(self.sidebar_frame, text="control setting",font = tk.CTkFont(size=18,weight="bold")).pack(pady = 20)
        self.select_btn = tk.CTkButton(self.sidebar_frame, text="select file",fg_color = "#007AFF",command=self.select_path_event)
        self.select_btn.pack(pady=10, padx=20)
        self.undo_btn = tk.CTkButton(self.sidebar_frame, text="delete",fg_color = "#007AFF",border_width=2)
        self.undo_btn.pack(pady=10, padx=20)
#主界面
        self.main_frame = tk.CTkFrame(self)
        self.main_frame.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.path_label = tk.CTkLabel(self.main_frame, text="path:no choose",anchor="w")
        self.path_label.grid(row=0,column=0,padx=10,pady=10,sticky="ew")
#文件预览
        self.file_list_box = tk.CTkTextbox(self.main_frame)
        self.file_list_box.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")
#底部操作
        self.entry_prefix = tk.CTkEntry(self.main_frame, placeholder_text="prefix rules:")
        self.entry_prefix.grid(row=2,column=0,padx=10,pady=10,sticky="ew")
        self.run_btn = tk.CTkButton(self.main_frame, text="run",fg_color="#2ecc71",hover_color="#27ae60",command=self.run_event)
        self.run_btn.grid(row=3,column=0,padx=10,pady=10)
#交互事件
    def select_path_event(self):
            #选择文件夹并扫描
            directory = filedialog.askdirectory()
            self.refresh_list(directory)
            def refresh_list(self, directory):
                try:
                    files, folders = Scanner.scan(directory)
                    self.file_list_box.delete("1.0", "end")
                    for d in folders:
                       self.file_list_box.insert("end",f"{d.name}\n")
                    for f in files:
                       self.file_list_box.insert("end",f"{f.name}\n")
                except Exception as e:
                    messagebox.showerror("Error",e)

    def run_event(self):
        new_base_name = self.entry_prefix.get()
    #获取路径
        current_path = self.path_label.cget("text").replace("当前路径：","")
        if not new_base_name or "no choose" in current_path:
            messagebox.showwarning("tip","choose path and rules")
            return
        import os
        try:
            items = os.listdir(current_path)
            success_count = 0

            for index,item in enumerate(items):
                old_path = os.path.join(current_path,item)
                if os.path.isdir(old_path):
                 name_part,extension = os.path.splitext(item)
                 new_name = f"{new_base_name}{extension}"
                 new_path = os.path.join(current_path,new_name)
                 os.rename(old_path,new_path)
                 success_count += 1
            messagebox.showinfo(f"success\ndeal file:{success_count}")
            self.select_path_event()
        except Exception as e:
             messagebox.showerror("error",str(e))
        self.select_path_event()
if __name__ == "__main__":
    app = Application()
    app.mainloop()