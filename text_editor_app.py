import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
from tkinter.scrolledtext import ScrolledText


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TMenubutton', font=('Segoe UI', 10))

        # Color scheme
        self.bg_color = '#f5f5f5'
        self.text_bg = '#ffffff'
        self.text_fg = '#333333'
        self.toolbar_color = '#e0e0e0'
        self.accent_color = '#4285f4'

        # Current file
        self.current_file = None
        self.unsaved_changes = False

        # Initialize variables before creating widgets
        self.font_family = tk.StringVar()
        self.font_size = tk.StringVar()
        self.text = None
        self.line_numbers = None
        self.status_label = None

        # Create widgets
        self.create_widgets()

        # Bind events
        self.text.bind('<<Modified>>', self.on_text_modified)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Toolbar
        self.toolbar = ttk.Frame(self.main_frame, height=40, relief=tk.RAISED)
        self.toolbar.pack(fill=tk.X, padx=2, pady=2)

        # Toolbar buttons
        self.new_btn = ttk.Button( self.toolbar,text="New",command=self.new_file)
        self.new_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.open_btn = ttk.Button(self.toolbar,text="Open",command=self.open_file)
        self.open_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_btn = ttk.Button(self.toolbar,text="Save",command=self.save_file)
        self.save_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_as_btn = ttk.Button(self.toolbar,text="Save As",command=self.save_file_as)
        self.save_as_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)

        # Font family dropdown
        self.font_family.set('Segoe UI')
        font_families = sorted(font.families())

        self.font_family_menu = ttk.OptionMenu(self.toolbar,self.font_family,'Segoe UI',*font_families,command=self.change_font)
        self.font_family_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Font size dropdown
        self.font_size.set('12')
        font_sizes = ['8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24']

        self.font_size_menu = ttk.OptionMenu( self.toolbar,self.font_size, '12',*font_sizes,command=self.change_font)
        self.font_size_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Status bar
        self.status_bar = ttk.Frame(self.main_frame, height=20)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = ttk.Label(self.status_bar,text="Ready",anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5)

        # Text area with scrollbars
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Line numbers
        self.line_numbers = tk.Text(self.text_frame,width=4,padx=4,pady=2,takefocus=0,border=0,background='#f0f0f0',foreground='#666666',state='disabled',wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Main text widget
        self.text = ScrolledText(self.text_frame,wrap=tk.WORD,font=(self.font_family.get(), int(self.font_size.get())),bg=self.text_bg,fg=self.text_fg,
                                 insertbackground=self.text_fg,selectbackground=self.accent_color,undo=True,autoseparators=True,maxundo=-1)
        self.text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for text styling
        self.text.tag_configure('found', background='yellow')

        # Bind events for line numbers
        self.text.bind('<KeyPress>', self.update_line_numbers)
        self.text.bind('<KeyRelease>', self.update_line_numbers)
        self.text.bind('<Button-1>', self.update_line_numbers)
        self.text.bind('<MouseWheel>', self.update_line_numbers)

        # Initial line numbers update
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        if not self.line_numbers:
            return

        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)

        # Get current line count
        line_count = self.text.index('end-1c').split('.')[0]

        # Add line numbers
        for i in range(1, int(line_count) + 1):
            self.line_numbers.insert(tk.END, f'{i}\n')

        self.line_numbers.config(state='disabled')

        # Sync scrolling
        self.line_numbers.yview_moveto(self.text.yview()[0])

    def change_font(self, *args):
        if not hasattr(self, 'text') or not self.text:
            return

        font_family = self.font_family.get()
        try:
            font_size = int(self.font_size.get())
        except ValueError:
            font_size = 12

        self.text.config(font=(font_family, font_size))
        self.update_line_numbers()

    def new_file(self):
        if self.unsaved_changes:
            if not self.confirm_discard():
                return

        self.text.delete(1.0, tk.END)
        self.current_file = None
        self.unsaved_changes = False
        self.update_status("New file created")

    def open_file(self):
        if self.unsaved_changes:
            if not self.confirm_discard():
                return

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text.delete(1.0, tk.END)
                    self.text.insert(1.0, file.read())
                    self.current_file = file_path
                    self.unsaved_changes = False
                    self.update_status(f"Opened: {file_path}")
                    self.root.title(f"Advanced Text Editor - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.text.get(1.0, tk.END))
                    self.unsaved_changes = False
                    self.update_status(f"Saved: {self.current_file}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
                return False
        else:
            return self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text.get(1.0, tk.END))
                    self.current_file = file_path
                    self.unsaved_changes = False
                    self.update_status(f"Saved: {file_path}")
                    self.root.title(f"Advanced Text Editor - {file_path}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
                return False
        return False

    def on_text_modified(self, event=None):
        if self.text.edit_modified():
            self.unsaved_changes = True
            self.update_status("Unsaved changes")
            self.text.edit_modified(False)

    def confirm_discard(self):
        if not self.unsaved_changes:
            return True

        response = messagebox.askyesnocancel("Unsaved Changes","You have unsaved changes. Do you want to save before continuing?")

        if response is None:  # Cancel
            return False
        elif response:  # Yes
            return self.save_file()
        else:  # No
            return True

    def on_close(self):
        if self.unsaved_changes:
            if not self.confirm_discard():
                return

        self.root.destroy()

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.after(5000, lambda: self.status_label.config(text="Ready") if self.status_label.cget("text") == message else None)


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()