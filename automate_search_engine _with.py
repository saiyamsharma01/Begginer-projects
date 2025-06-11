import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from tkinter.font import Font


class AIAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("500x450")
        self.root.resizable(True, True)
        self.root.configure(bg="#e8ecef")  # Soft blue-gray background

        # Custom fonts
        self.title_font = Font(family="Segoe UI", size=18, weight="bold")
        self.button_font = Font(family="Segoe UI", size=10, weight="bold")
        self.entry_font = Font(family="Segoe UI", size=12)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme for better button visibility

        # Configure frame background
        self.style.configure("TFrame", background="#e8ecef")

        # Configure base button style
        self.style.configure("TButton",font=self.button_font,padding=8,borderwidth=1,relief="raised",focuscolor="#e8ecef")

        # Configure specific button colors
        # YouTube Button - Red
        self.style.configure("YouTube.TButton",background="#ff0000",foreground="white",bordercolor="#cc0000",darkcolor="#cc0000",lightcolor="#ff3333",focuscolor="#e8ecef")

        # Google Button - Blue
        self.style.configure("Google.TButton",background="#4285f4",foreground="white",bordercolor="#3367d6",darkcolor="#3367d6",lightcolor="#5a95f5",focuscolor="#e8ecef")

        # Instagram Button - Purple
        self.style.configure("Instagram.TButton",background="#c13584",foreground="white",bordercolor="#8a2a5c",darkcolor="#8a2a5c",lightcolor="#d1479e",focuscolor="#e8ecef")

        # Clear Button - Gray
        self.style.configure("Clear.TButton",background="#95a5a6",foreground="white",bordercolor="#7f8c8d",darkcolor="#7f8c8d",lightcolor="#b4c0c1",focuscolor="#e8ecef")

        # Header Frame
        self.header_frame = ttk.Frame(root, style="TFrame")
        self.header_frame.pack(pady=(20, 10), fill="x")

        # Title Label
        self.title_label = ttk.Label(self.header_frame,text="AI Assistant",font=self.title_font,foreground="#2c3e50",background="#e8ecef")
        self.title_label.pack()

        # Subtitle Label
        self.subtitle_label = ttk.Label(self.header_frame,text="Search anything across platforms",font=("Segoe UI", 10),foreground="#5a6a7a",background="#e8ecef")
        self.subtitle_label.pack()

        # Main Content Frame
        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Search Entry
        self.entry_label = ttk.Label(self.main_frame,text="Enter your search query or Instagram username:",font=("Segoe UI", 10),foreground="#5a6a7a",background="#e8ecef")
        self.entry_label.pack(anchor="w", pady=(0, 5))

        self.entry = ttk.Entry(self.main_frame,width=40,font=self.entry_font)
        self.entry.pack(pady=5, ipady=8)
        self.entry.focus()

        # Bind Enter key to search
        self.entry.bind("<Return>", lambda e: self.search_youtube())

        # Button Frame
        self.button_frame = ttk.Frame(self.main_frame, style="TFrame")
        self.button_frame.pack(pady=20)

        # YouTube Button
        self.youtube_btn = ttk.Button(self.button_frame,text="Search YouTube",command=self.search_youtube,style="YouTube.TButton")
        self.youtube_btn.grid(row=0, column=0, padx=5, pady=5, ipadx=10, sticky="ew")

        # Google Button
        self.google_btn = ttk.Button(self.button_frame,text="Search Google",command=self.search_google,style="Google.TButton")
        self.google_btn.grid(row=0, column=1, padx=5, pady=5, ipadx=10, sticky="ew")

        # Instagram Button
        self.instagram_btn = ttk.Button(self.button_frame,text="Open Instagram",command=self.search_instagram,style="Instagram.TButton" )
        self.instagram_btn.grid(row=1, column=0, columnspan=2, pady=(10, 5), ipadx=10, sticky="ew")

        # Clear Button
        self.clear_btn = ttk.Button(self.button_frame,text="Clear",command=lambda: self.entry.delete(0, tk.END),style="Clear.TButton")
        self.clear_btn.grid(row=2, column=0, columnspan=2, pady=5, ipadx=10, sticky="ew")

        # Footer
        self.footer_label = ttk.Label(root,text="© 2023 AI Assistant | Version 1.0",font=("Segoe UI", 8),foreground="#7f8c8d",background="#e8ecef")
        self.footer_label.pack(side="bottom", pady=10)

    def search_youtube(self):
        query = self.entry.get().strip()
        if query:
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Empty Query", "Please enter a search term for YouTube")

    def search_google(self):
        query = self.entry.get().strip()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Empty Query", "Please enter a search term for Google")

    def search_instagram(self):
        username = self.entry.get().strip().replace("@", "")
        if username:
            url = f"https://www.instagram.com/{username}/"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Empty Username", "Please enter an Instagram username")


if __name__ == "__main__":
    root = tk.Tk()
    app = AIAssistant(root)
    root.mainloop()