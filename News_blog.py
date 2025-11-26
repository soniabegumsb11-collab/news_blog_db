import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_FILE = "news_blog.db"

def init_db():

    conn = sqlite3.connect(DB_FILE)

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(

            user_id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL,

            email TEXT NOT NULL,

            age INTEGER,

            contact_number TEXT,

            bio TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news(

            news_id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            body TEXT NOT NULL,

            user_id INTEGER NOT NULL,

            username TEXT NOT NULL,

            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()

    conn.close()

class NewsBlogGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("News Blog System - Full CRUD Improved UI")

        self.root.geometry("1100x650")

        self.root.configure(bg="gray")

        title = tk.Label(root, text="News Blog Management System",
                         font=("Segoe UI", 18, "bold"), fg="black", bg="gray")

        title.pack(pady=10)

        notebook = ttk.Notebook(root)

        self.user_tab = ttk.Frame(notebook)

        self.news_tab = ttk.Frame(notebook)

        notebook.add(self.user_tab, text="Users")

        notebook.add(self.news_tab, text="News")

        notebook.pack(expand=True, fill="both")

        self.build_user_tab()

        self.build_news_tab()

    def build_user_tab(self):

        frame = tk.Frame(self.user_tab, bg="gray")

        frame.pack(fill="both", expand=True)

        labels = ["Username:", "Email:", "Age:", "Contact:", "Bio:"]

        self.entries = {}

        input_frame = tk.Frame(frame, bg="gray")

        input_frame.grid(row=0, column=0, sticky="nw", padx=50, pady=20)

        for i, text in enumerate(labels):

            tk.Label(input_frame, text=text, fg="black", bg="gray").grid(row=i, column=0, pady=6, sticky="w")

            entry = tk.Entry(input_frame, width=35)

            entry.grid(row=i, column=1)

            self.entries[text] = entry

        tk.Button(input_frame, text="Add User", width=15, bg="green", fg="white",
                  command=self.add_user).grid(row=6, column=0, pady=10)

        tk.Button(input_frame, text="Update User", width=15, bg="blue", fg="white",
                  command=self.update_user).grid(row=6, column=1, pady=10)

        tk.Button(input_frame, text="Delete User", width=15, bg="red", fg="white",
                  command=self.delete_user).grid(row=7, column=0, pady=10)

        self.user_list = ttk.Treeview(frame, columns=("ID", "Name", "Email"), show="headings", height=14)
        self.user_list.heading("ID", text="ID")

        self.user_list.heading("Name", text="Username")

        self.user_list.heading("Email", text="Email")

        self.user_list.grid(row=0, column=1, padx=20, pady=20)

        self.user_list.bind("<<TreeviewSelect>>", self.user_selected)

        self.load_users()


    def build_news_tab(self):

        frame = tk.Frame(self.news_tab, bg="gray")

        frame.pack(fill="both", expand=True)

        center_frame = tk.Frame(frame, bg="gray")

        center_frame.pack(pady=20)

        tk.Label(center_frame, text="Title:", bg="gray").grid(row=0, column=0, sticky="w", pady=5)

        tk.Label(center_frame, text="Body:", bg="gray").grid(row=1, column=0, sticky="w", pady=5)

        tk.Label(center_frame, text="User ID:", bg="gray").grid(row=2, column=0, sticky="w", pady=5)

        self.news_title = tk.Entry(center_frame, width=50)

        self.news_body = tk.Entry(center_frame, width=50)

        self.news_user_id = tk.Entry(center_frame, width=20)

        self.news_title.grid(row=0, column=1)

        self.news_body.grid(row=1, column=1)

        self.news_user_id.grid(row=2, column=1)

        btn_frame = tk.Frame(center_frame, bg="gray")

        btn_frame.grid(row=3, column=1, pady=10)


        tk.Button(btn_frame, text="Add News", width=12, bg="green", fg="white",
                  command=self.add_news).grid(row=0, column=0, padx=4)


        tk.Button(btn_frame, text="Update News", width=12, bg="blue", fg="white",
                  command=self.update_news).grid(row=0, column=1, padx=4)


        tk.Button(btn_frame, text="Delete News", width=12, bg="red", fg="white",
                  command=self.delete_news).grid(row=0, column=2, padx=4)


        search_frame = tk.Frame(frame, bg="gray")

        search_frame.pack()

        tk.Label(search_frame, text="Search Title:", bg="gray").grid(row=0, column=0)

        self.search_entry = tk.Entry(search_frame, width=40)

        self.search_entry.grid(row=0, column=1)


        tk.Button(search_frame, text="Search", bg="black", fg="white",
                  command=self.search_news).grid(row=0, column=2, padx=5)


        tk.Button(search_frame, text="Clear Search", bg="black", fg="white",
                  command=self.clear_search).grid(row=0, column=3, padx=5)


        tk.Button(search_frame, text="Show All", bg="black", fg="white",
                  command=self.load_news).grid(row=0, column=4, padx=5)
                  


        self.news_list = ttk.Treeview(frame, columns=("ID", "Title", "Body"), show="headings", height=12)

        self.news_list.heading("ID", text="ID")

        self.news_list.heading("Title", text="Title")

        self.news_list.heading("Body", text="Body")

        self.news_list.pack(pady=20)

        self.news_list.bind("<<TreeviewSelect>>", self.news_selected)

        self.load_news()

    def load_users(self):

        for r in self.user_list.get_children():

            self.user_list.delete(r)

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        cur.execute("SELECT user_id, username, email FROM users")

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.user_list.insert("", "end", values=row)

    def add_user(self):

        username = self.entries["Username:"].get()

        email = self.entries["Email:"].get()

        if not username or not email:

            messagebox.showerror("Error", "Username & Email required")

            return

        age = self.entries["Age:"].get()

        contact = self.entries["Contact:"].get()

        bio = self.entries["Bio:"].get()

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        cur.execute("INSERT INTO users(username,email,age,contact_number,bio) VALUES (?,?,?,?,?)",
                    (username,email,age or None,contact,bio))

        conn.commit()

        conn.close()

        self.load_users()

        messagebox.showinfo("Success","User Added!")


    def user_selected(self, event):

        selected = self.user_list.focus()

        if not selected:

            return

        data = self.user_list.item(selected,"values")

        self.selected_user_id = data[0]

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE user_id=?",(self.selected_user_id,))

        user = cur.fetchone()

        conn.close()

        if user:

            _, username, email, age, contact, bio = user

            self.entries["Username:"].delete(0, tk.END)

            self.entries["Username:"].insert(0, username)

            self.entries["Email:"].delete(0, tk.END)

            self.entries["Email:"].insert(0, email)

            self.entries["Age:"].delete(0, tk.END)

            self.entries["Age:"].insert(0, age if age else "")

            self.entries["Contact:"].delete(0, tk.END)

            self.entries["Contact:"].insert(0, contact if contact else "")

            self.entries["Bio:"].delete(0, tk.END)

            self.entries["Bio:"].insert(0, bio if bio else "")


    def update_user(self):

        if not hasattr(self,"selected_user_id"):

            messagebox.showerror("Error","Select a user first")

            return

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        cur.execute("""UPDATE users SET username=?,email=?,age=?,contact_number=?,bio=? WHERE user_id=?""",
                    (self.entries["Username:"].get(),self.entries["Email:"].get(),
                     self.entries["Age:"].get(),self.entries["Contact:"].get(),
                     self.entries["Bio:"].get(),self.selected_user_id))

        conn.commit()

        conn.close()

        self.load_users()

        messagebox.showinfo("Success","User Updated!")


    def delete_user(self):

        if not hasattr(self,"selected_user_id"):

            messagebox.showerror("Error","Select a user first")

            return

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE user_id=?",(self.selected_user_id,))

        conn.commit()

        conn.close()

        self.load_users()

        messagebox.showinfo("Success","User Deleted!")


    def load_news(self):

        for r in self.news_list.get_children():

            self.news_list.delete(r)

        conn = sqlite3.connect(DB_FILE)

        cur = conn.cursor()

        cur.execute("SELECT news_id,title,body FROM news ORDER BY news_id DESC")

        rows = cur.fetchall()

        conn.close()

        for row in rows:

            self.news_list.insert("", "end", values=row)

    def add_news(self):

        title=self.news_title.get()

        body=self.news_body.get()

        user_id=self.news_user_id.get()

        if not title or not body or not user_id:

            messagebox.showerror("Error","All fields required")

            return

        conn=sqlite3.connect(DB_FILE)

        cur=conn.cursor()

        cur.execute("SELECT username FROM users WHERE user_id=?",(user_id,))

        result=cur.fetchone()

        if not result:

            messagebox.showerror("Error","User ID not found")

            conn.close()

            return

        username=result[0]

        cur.execute("INSERT INTO news(title,body,user_id,username) VALUES (?,?,?,?)",
                    (title,body,user_id,username))

        conn.commit()

        conn.close()

        self.load_news()

        messagebox.showinfo("Success","News Added!")


    def news_selected(self,event):

        selected=self.news_list.focus()

        if not selected:

            return

        data=self.news_list.item(selected,"values")

        self.selected_news_id=data[0]

        conn=sqlite3.connect(DB_FILE)

        cur=conn.cursor()

        cur.execute("SELECT news_id,title,body FROM news WHERE news_id=?",(self.selected_news_id,))

        news=cur.fetchone()

        conn.close()

        if news:

            _, title, body = news

            self.news_title.delete(0, tk.END)

            self.news_title.insert(0,title)

            self.news_body.delete(0, tk.END)

            self.news_body.insert(0,body)

    def update_news(self):

        if not hasattr(self,"selected_news_id"):

            messagebox.showerror("Error","Select news first")

            return

        conn=sqlite3.connect(DB_FILE)

        cur=conn.cursor()

        cur.execute("UPDATE news SET title=?,body=? WHERE news_id=?",
                    (self.news_title.get(),self.news_body.get(),self.selected_news_id))

        conn.commit()

        conn.close()

        self.load_news()

        messagebox.showinfo("Success","News Updated!")

    def delete_news(self):

        if not hasattr(self,"selected_news_id"):

            messagebox.showerror("Error","Select news first")

            return

        conn=sqlite3.connect(DB_FILE)

        cur=conn.cursor()

        cur.execute("DELETE FROM news WHERE news_id=?",(self.selected_news_id,))

        conn.commit()

        conn.close()

        self.load_news()

        messagebox.showinfo("Success","News Deleted!")

    def search_news(self):

        keyword=self.search_entry.get()

        if not keyword.strip():

            return

        for r in self.news_list.get_children():

            self.news_list.delete(r)

        conn=sqlite3.connect(DB_FILE)

        cur=conn.cursor()

        cur.execute("SELECT news_id,title,body FROM news WHERE title LIKE ?",('%'+keyword+'%',))

        rows=cur.fetchall()

        conn.close()

        for row in rows:

            self.news_list.insert("", "end", values=row)


    def clear_search(self):

        self.search_entry.delete(0, tk.END)

        self.load_news()


init_db()

root=tk.Tk()

app=NewsBlogGUI(root)

root.mainloop()
