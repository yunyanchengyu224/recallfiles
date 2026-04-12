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
        self.sidebar_frame =tk.CTkFrame(self,width=200,corner_radius=0)
        self.sidebar_frame.grid(row=0,column=0,sticky="nsew")
        self.logo_lable = tk.CTkLabel(self.sidebar_frame, text="control center",font = tk.CTkFont(size=18,weight="bold")).pack(pady = 20)
        self.select_btn = tk.CTkButton(self.sidebar_frame, text="select file",fg_color = "#007AFF",command=self.select_path_event)
        self.select_btn.pack(pady=10, padx=20)
        self.undo_btn = tk.CTkButton(self.sidebar_frame, text="delete",fg_color = "#c0392b",border_width=2,command=self.undo_event)
        self.undo_btn.pack(pady=10, padx=20)
        self.rename_folder_btn = tk.CTkButton(self.sidebar_frame, text="rename folder",fg_color="#8e44ad",command=self.rename_folder_event)
        self.rename_folder_btn.pack(pady=10, padx=20)
#改名选项
        self.rename_files_var = tk.BooleanVar(value=True)
        self.check_files = tk.CTkCheckBox(self.sidebar_frame, text="rename files",variable=self.rename_files_var)
        self.check_files.pack(pady=5, padx=20,anchor="w")
        self.opt_folders_var = tk.BooleanVar(value=False)
        self.check_folders_var = tk.CTkCheckBox(self.sidebar_frame, text="include folders",variable=self.opt_folders_var)
        self.check_folders_var.pack(pady=5, padx=20,anchor="w")
#主界面
        self.main_frame = tk.CTkFrame(self)
        self.main_frame.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.path_label = tk.CTkLabel(self.main_frame, text="path:no choose",anchor="w")
        self.path_label.grid(row=0,column=0,padx=10,pady=10,sticky="ew")
#文件预览
        self.file_list_box = tk.CTkTextbox(self.main_frame)
        self.file_list_box.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")
#底部操作
        self.entry_prefix = tk.CTkEntry(self.main_frame, placeholder_text="new name:")
        self.entry_prefix.grid(row=2,column=0,padx=10,pady=10,sticky="ew")
        self.run_btn = tk.CTkButton(self.main_frame, text="run",fg_color="#2ecc71",hover_color="#27ae60",command=self.run_event)
        self.run_btn.grid(row=3,column=0,padx=10,pady=10)
#刷新列表
    def refresh_list(self, directory):
                try:
                    files, folders = Scanner.scan(directory)
                    self.file_list_box.delete("1.0", "end")
                    for d in folders:
                       self.file_list_box.insert("end",f"{d.name}\n")
                    for f in files:
                       self.file_list_box.insert("end",f"{f.name}\n")
                except Exception as e:
                    messagebox.showerror("Error",{e})
#交互事件
    def select_path_event(self):
            #选择文件夹并扫描
            directory = filedialog.askdirectory()
            if directory:
                self.path_label.configure(text=f"path:{directory}")
                self.refresh_list(directory)

    def run_event(self):
        new_base_name = self.entry_prefix.get()
    #获取路径
        current_path = self.path_label.cget("text").replace("path:","")
        if not new_base_name or "no choose" in current_path:
            messagebox.showwarning("tip","choose path and rules")
            return
        try:
            items = os.listdir(current_path)
            batch_ops = []

            for index,item in enumerate(items):
                old_path = os.path.join(current_path,item)
                is_dir = os.path.isdir(old_path)
                if (is_dir and not self.opt_folders_var.get()) or (not is_dir and not self.rename_files_var.get()):
                    continue
                ext = os.path.splitext(item)[1] if not is_dir else ""
                new_name = f"{new_base_name}{ext}"
                new_path = os.path.join(current_path,new_name)
                os.rename(old_path,new_path)
                batch_ops.append((old_path, new_path))

            if batch_ops:
                self.history.append(batch_ops)
                messagebox.showinfo("success", f"deal file:{len(batch_ops)} batches")
                self.refresh_list(current_path)
            else:
                messagebox.showerror("error","no more files")
        except Exception as e:
             messagebox.showerror("error",str(e))

    def rename_folder_event(self):
        new_name = self.entry_prefix.get()
        current_path = self.path_label.cget("text").replace("path:", "")
        if not new_name or "no choose" in current_path:
            messagebox.showwarning("tip", "choose a folder and enter a new name")
            return
        from pathlib import Path
        folder = Path(current_path)
        new_path = folder.parent / new_name
        try:
            os.rename(folder, new_path)
            self.history.append([(str(folder), str(new_path))])
            self.path_label.configure(text=f"path:{new_path}")
            self.refresh_list(str(new_path))
            messagebox.showinfo("success", f"folder renamed to '{new_name}'")
        except Exception as e:
            messagebox.showerror("error", str(e))

    def undo_event(self):
        if not self.history:
            messagebox.showerror("error","no more files")
            return
        try:
            last_batch = self.history.pop()
            for old_path,new_path in reversed(last_batch):
                if os.path.exists(new_path):
                    os.rename(new_path,old_path)
            messagebox.showinfo("success","origin files restored")
            current_path = self.path_label.cget("text").replace("path:","")
            self.refresh_list(current_path)
        except Exception as e:
            messagebox.showerror("error",f"default delete:{e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
