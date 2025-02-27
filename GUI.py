import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import requests
import json
import time
import tkinter.ttk as ttk
import threading




class SimpleNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("简易记事本")
        self.filename = None

    
        # 创建菜单栏
        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新建", command=self.new_file)
        self.file_menu.add_command(label="打开", command=self.open_file)
        self.file_menu.add_command(label="保存", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.root.quit)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        self.menu_bar.config(font=("Arial",20))

        # 创建文本编辑区
        self.text_area = tk.Text(root, wrap="word", undo=True)
        self.text_area.config(font=("Arial", 16), bg="#2D2D2D", fg="white")
        self.text_area.pack(expand=True, fill="both")
        
        # 添加滚动条
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        
        # 绑定快捷键
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())

          # 在 __init__ 方法中添加这些菜单项
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="查找", command=self.find_text)
        self.edit_menu.add_command(label="替换", command=self.replace_text)
        self.menu_bar.add_cascade(label="编辑", menu=self.edit_menu)

        self.bili_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.bili_menu.add_command(label="笨笨的韭菜", command=self.dynamic_benbeng_text)
        self.bili_menu.add_command(label="莫大韭菜", command=self.dynamic_moda_text)
        self.menu_bar.add_cascade(label="动态", menu=self.bili_menu)

        root.config(menu=self.menu_bar)

    def new_file(self):
        self.filename = None
        self.text_area.delete(1.0, tk.END)
        self.root.title("新建文件 - 简易记事本")

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "r") as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, f.read())
                self.filename = filepath
                self.root.title(f"{filepath} - 简易记事本")
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")

    def save_file(self):
        if self.filename:
            try:
                with open(self.filename, "w") as f:
                    f.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("保存成功", "文件已保存!")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{str(e)}")
        else:
            self.save_as_file()

    def find_text(self):
        find_str = simpledialog.askstring("查找", "输入查找内容:")
        if find_str:
            start = self.text_area.search(find_str, "1.0", stopindex=tk.END)
            if start:
                end = f"{start}+{len(find_str)}c"
                self.text_area.tag_add("highlight", start, end)
                self.text_area.tag_config("highlight", background="yellow")

    def replace_text(self):
        find_str = simpledialog.askstring("替换", "查找内容:")
        replace_str = simpledialog.askstring("替换", "替换为:")
        if find_str and replace_str:
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_str, replace_str)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, new_content)

    def save_as_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filepath:
            self.filename = filepath
            self.save_file()
            self.root.title(f"{filepath} - 简易记事本")

    def insert_initial_content(self):
        """ 初始化时插入默认文本 """
        welcome_text = """欢迎使用简易记事本！
操作指南：
1. 使用 Ctrl+N 新建文件
2. 使用 Ctrl+S 保存文件
3. 使用 Ctrl+O 打开文件\n\n"""
        self.text_area.insert(tk.END, welcome_text)
    @staticmethod
    def get_comments(oid, max_page=5,web_location="1315875",w_rid="6e25965f065a59835ea4eaeb5544be86",wts="1740636936"):
        cookies = {
            'SESSDATA': 'xxx',
            'bili_jct': 'xxx'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'https://t.bilibili.com/{oid}'
        }
        comments = []
        for page in range(1, max_page+1):
            url = f'https://api.bilibili.com/x/v2/reply/main?oid={oid}&type=17&next={page}&mode=2&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location={web_location}&w_rid={w_rid}&wts={wts}'
            try:
                resp = requests.get(url, headers=headers, cookies=cookies)
                data = resp.json()
                if data['code'] == 0:
                    for reply in data['data']['replies']:
                        comment = {
                            '用户': reply['member']['uname'],
                            '内容': reply['content']['message'],
                            '时间': time.strftime("%Y-%m-%d %H:%M", 
                                    time.localtime(reply['ctime'])),
                            '点赞数': reply['like']
                        }
                        comments.append(comment)
                    print(f'第 {page} 页获取成功')
                else:
                    print(f'错误：{data["message"]}')
                time.sleep(1)  # 防止触发频率限制
            except Exception as e:
                print(f'请求失败：{str(e)}')
                break
        return comments
    
    @staticmethod
    def get_vip_comments(oid, max_page=5,web_location="1315875",w_rid="a97a71dfea613659b1a709c4b2b2436c",wts="1740638325"):
        cookies = {
            'SESSDATA': 'xxx',
            'bili_jct': 'xxx'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'https://t.bilibili.com/{oid}'
        }
        comments = []
        for page in range(1, max_page+1):
            url = f'https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=17&next={page}&mode=2&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location={web_location}&w_rid={w_rid}&wts={wts}'
            try:
                resp = requests.get(url, headers=headers, cookies=cookies)
                data = resp.json()
                if data['code'] == 0:
                    for reply in data['data']['replies']:
                        comment = {
                            '用户': reply['member']['uname'],
                            '内容': reply['content']['message'],
                            '时间': time.strftime("%Y-%m-%d %H:%M", 
                                    time.localtime(reply['ctime'])),
                            '点赞数': reply['like']
                        }
                        comments.append(comment)
                    print(f'第 {page} 页获取成功')
                else:
                    print(f'错误：{data["message"]}')
                time.sleep(1)  # 防止触发频率限制
            except Exception as e:
                print(f'请求失败：{str(e)}')
                break
        return comments

    
    def dynamic_benbeng_text(self):
        """ 插入动态内容示例 """
        dynamic_id = '836681344644808744'  # 替换实际动态ID
        comments = self.get_comments(dynamic_id)
        sample_text = self.comments_to_simple(comments)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, sample_text)  # 在光标处插入
            

    def thread_benbeng_text(self):
        while True:
            dynamic_id = '836681344644808744'  # 替换实际动态ID
            comments = self.get_comments(dynamic_id)
            sample_text = self.comments_to_simple(comments)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, sample_text)  # 在光标处插入
            time.sleep(60)

    def dynamic_moda_text(self):
        """ 插入动态内容示例 """
        dynamic_id = '993364062283759637'  # 替换实际动态ID
        comments = self.get_vip_comments(dynamic_id)
        sample_text = self.comments_to_simple(comments)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, sample_text)  # 在光标处插入

    @staticmethod
    def comments_to_markdown(comments):
        table = [
            "| 序号 | 用户 | 内容 | 时间 | 点赞 |",
            "|------|------|------|------|------|"
        ]
        for idx, comment in enumerate(comments, 1):
            row = f"| {idx} | {comment['用户']} | {comment['内容'][:30]}... | {comment['时间']} | {comment['点赞数']} |"
            table.append(row)
        return '\n'.join(table)

    @staticmethod
    def comments_to_simple(comments, max_length=200):
        output = []
        for idx, comment in enumerate(comments, 1):
            line = f"{idx:>2}. [{comment['用户']}({comment['时间']})] {comment['内容'][:max_length]}"
            if len(comment['内容']) > max_length:
                line += "..."
            output.append(line)
        return '\n'.join(output)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = SimpleNotepad(root)
    root.config(bg="#2D2D2D")
    style = ttk.Style()
    style.theme_use("alt")
    style.configure('TButton', 
                    background='#607D8B', 
                    foreground='white')
    timer_thread = threading.Thread(target=app.thread_benbeng_text, daemon=True)
    timer_thread.start()
    
    root.mainloop()