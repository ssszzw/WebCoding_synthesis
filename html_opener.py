import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import webbrowser
import platform

class HtmlManagerTool:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML 文件查看器 & 启动器")
        self.root.geometry("800x600")

        # 变量存储
        self.folder_path = tk.StringVar()
        self.chrome_browser = self.get_chrome_controller() # 预先加载 Chrome 控制器

        # --- UI 布局 ---
        self.create_top_bar()
        self.create_list_view()
        self.create_bottom_bar()
        self.create_status_bar()

    def create_top_bar(self):
        """顶部：选择文件夹区域"""
        frame = tk.Frame(self.root, pady=10, padx=10)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="目标文件夹:").pack(side=tk.LEFT)
        
        entry = tk.Entry(frame, textvariable=self.folder_path)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        btn_select = tk.Button(frame, text="📂 选择文件夹并扫描", command=self.select_and_scan)
        btn_select.pack(side=tk.LEFT, padx=5)

    def create_list_view(self):
        """中间：文件列表表格"""
        frame = tk.Frame(self.root, padx=10, pady=5)
        frame.pack(fill=tk.BOTH, expand=True)

        # 滚动条
        scroll_y = tk.Scrollbar(frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # 表格 (Treeview)
        columns = ("filename", "rel_path")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scroll_y.set, selectmode="extended")
        
        # 定义列头
        self.tree.heading("filename", text="文件名", anchor=tk.W)
        self.tree.heading("rel_path", text="完整路径", anchor=tk.W)
        
        # 定义列宽
        self.tree.column("filename", width=200, minwidth=100)
        self.tree.column("rel_path", width=500, minwidth=200)

        self.tree.pack(fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.tree.yview)

        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_double_click)

    def create_bottom_bar(self):
        """底部：操作按钮"""
        frame = tk.Frame(self.root, pady=10, padx=10)
        frame.pack(fill=tk.X)

        btn_open = tk.Button(frame, text="🚀 在 Chrome 中打开选中文件", command=self.open_selected_files, 
                             bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), height=2)
        btn_open.pack(fill=tk.X)

    def create_status_bar(self):
        """最底部：状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 - 请选择文件夹")
        lbl = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        lbl.pack(side=tk.BOTTOM, fill=tk.X)

    # --- 逻辑处理 ---

    def get_chrome_controller(self):
        """获取 Chrome 浏览器控制器"""
        system_name = platform.system()
        chrome_path = None

        if system_name == "Windows":
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]
            for p in paths:
                if os.path.exists(p):
                    # Windows 下需要加 %s
                    chrome_path = p + ' %s'
                    break
        elif system_name == "Darwin":  # macOS
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        elif system_name == "Linux":
            chrome_path = '/usr/bin/google-chrome %s'

        try:
            if chrome_path:
                return webbrowser.get(chrome_path)
            else:
                return webbrowser.get() # 找不到就用默认
        except:
            return webbrowser.get()

    def select_and_scan(self):
        """选择文件夹并立即扫描"""
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)
            self.scan_files(path)

    def scan_files(self, folder):
        """扫描 HTML 文件并填充到表格"""
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        html_files = []
        try:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.html', '.htm')):
                        full_path = os.path.join(root, file)
                        html_files.append((file, full_path))
        except Exception as e:
            messagebox.showerror("错误", f"扫描失败: {e}")
            return

        # 填充表格
        for name, path in html_files:
            self.tree.insert("", tk.END, values=(name, path))

        self.status_var.set(f"扫描完成：共找到 {len(html_files)} 个 HTML 文件。")

    def on_double_click(self, event):
        """双击列表项直接打开"""
        self.open_selected_files()

    def open_selected_files(self):
        """打开所有选中的文件"""
        selected_items = self.tree.selection()
        
        if not selected_items:
            messagebox.showwarning("提示", "请先在列表中选择一个或多个文件。")
            return

        count = 0
        for item_id in selected_items:
            # 获取该行的数据 (文件名, 完整路径)
            item_data = self.tree.item(item_id)
            values = item_data['values']
            if values:
                file_path = values[1] # 获取第二列：完整路径
                self.open_url(file_path)
                count += 1
        
        self.status_var.set(f"已打开 {count} 个页面。")

    def open_url(self, file_path):
        """实际执行打开操作"""
        url = 'file://' + os.path.abspath(file_path)
        try:
            self.chrome_browser.open_new_tab(url)
        except Exception as e:
            print(f"打开失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HtmlManagerTool(root)
    root.mainloop()
