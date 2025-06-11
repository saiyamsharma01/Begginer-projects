import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from tkinter.font import Font


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager Pro")
        self.root.geometry("900x650")

        # Modern color palette
        self.primary_bg = "#f8f9fa"  # Light gray background
        self.secondary_bg = "#e9ecef"  # Slightly darker gray for panels
        self.primary_text = "#212529"  # Dark gray for text
        self.accent_color = "#0d6efd"  # Bootstrap primary blue
        self.success_color = "#198754"  # Bootstrap success green
        self.danger_color = "#dc3545"  # Bootstrap danger red
        self.warning_color = "#ffc107"  # Bootstrap warning yellow

        # Configure root window background
        self.root.configure(bg=self.primary_bg)

        # Custom font setup
        self.title_font = Font(family="Segoe UI", size=18, weight="bold")
        self.label_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=10, weight="bold")

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('TFrame', background=self.primary_bg)
        self.style.configure('TLabel', background=self.primary_bg, foreground=self.primary_text, font=self.label_font)
        self.style.configure('Header.TLabel', font=self.title_font, background=self.primary_bg,foreground=self.accent_color)

        # Button styles
        self.style.configure('TButton', font=self.button_font, borderwidth=1, foreground="white", padding=8)
        self.style.configure('Primary.TButton', background=self.accent_color)
        self.style.map('Primary.TButton', background=[('active', '#0b5ed7'), ('!active', self.accent_color)])
        self.style.configure('Success.TButton', background=self.success_color)
        self.style.map('Success.TButton', background=[('active', '#157347'), ('!active', self.success_color)])
        self.style.configure('Danger.TButton', background=self.danger_color)
        self.style.map('Danger.TButton', background=[('active', '#bb2d3b'), ('!active', self.danger_color)])
        self.style.configure('Warning.TButton', background=self.warning_color, foreground="black")
        self.style.map('Warning.TButton', background=[('active', '#e0a800'), ('!active', self.warning_color)])

        # Treeview style
        self.style.configure('Treeview', background="white", fieldbackground="white", foreground=self.primary_text,rowheight=25)
        self.style.configure('Treeview.Heading', background=self.secondary_bg, foreground=self.primary_text,font=self.button_font)
        self.style.map('Treeview', background=[('selected', '#dee2e6')])

        # Create main container
        self.main_frame = ttk.Frame(root, style='TFrame')
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Header
        self.header = ttk.Label(self.main_frame, text="📁 File Manager Pro", style='Header.TLabel')
        self.header.pack(pady=(0, 20))

        # Status bar (moved up before view_all_files call)
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN,anchor=tk.W, background=self.secondary_bg, foreground=self.primary_text)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        self.status_var.set("Ready")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_file_tab()
        self.create_view_tab()
        self.create_edit_tab()

    def create_file_tab(self):
        """Create the File Operations tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="File Operations")

        # Form frame
        form_frame = ttk.Frame(tab, style='TFrame', padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # File name entry
        ttk.Label(form_frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.filename_entry = ttk.Entry(form_frame, width=40, font=self.label_font)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Browse button
        browse_btn = ttk.Button(form_frame, text="Browse...", command=self.browse_file, style='Primary.TButton')
        browse_btn.grid(row=0, column=2, padx=5, pady=5)

        # Buttons frame
        btn_frame = ttk.Frame(form_frame, style='TFrame')
        btn_frame.grid(row=1, column=0, columnspan=3, pady=15)

        # Operation buttons
        ttk.Button(btn_frame, text="Create File", command=self.create_file, style='Success.TButton').pack(side=tk.LEFT,padx=5)
        ttk.Button(btn_frame, text="Delete File", command=self.delete_file, style='Danger.TButton').pack(side=tk.LEFT,padx=5)
        ttk.Button(btn_frame, text="Read File", command=self.read_file, style='Primary.TButton').pack(side=tk.LEFT,padx=5)

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def create_view_tab(self):
        """Create the View Files tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="View Files")

        # Treeview frame
        tree_frame = ttk.Frame(tab, style='TFrame')
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview widget
        self.tree = ttk.Treeview(tree_frame, columns=('Name', 'Size', 'Type'), selectmode='browse')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure columns
        self.tree.heading('#0', text='#')
        self.tree.heading('Name', text='File Name')
        self.tree.heading('Size', text='Size (KB)')
        self.tree.heading('Type', text='Type')

        self.tree.column('#0', width=50, stretch=tk.NO)
        self.tree.column('Name', width=200)
        self.tree.column('Size', width=100, anchor=tk.E)
        self.tree.column('Type', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Refresh button
        refresh_btn = ttk.Button(tab, text="Refresh List", command=self.view_all_files, style='Primary.TButton')
        refresh_btn.pack(pady=10)

        # Initial load
        self.view_all_files()

    def create_edit_tab(self):
        """Create the Edit File tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="Edit File")

        # Form frame
        form_frame = ttk.Frame(tab, style='TFrame', padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # File name entry
        ttk.Label(form_frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.edit_filename_entry = ttk.Entry(form_frame, width=40, font=self.label_font)
        self.edit_filename_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Browse button
        browse_btn = ttk.Button(form_frame, text="Browse...",command=lambda: self.browse_file(self.edit_filename_entry),style='Primary.TButton')
        browse_btn.grid(row=0, column=2, padx=5, pady=5)

        # Content editor
        ttk.Label(form_frame, text="File Content:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.NW)
        self.content_editor = scrolledtext.ScrolledText(form_frame, width=60, height=15, font=('Consolas', 10))
        self.content_editor.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

        # Buttons frame
        btn_frame = ttk.Frame(form_frame, style='TFrame')
        btn_frame.grid(row=2, column=1, columnspan=2, pady=10, sticky=tk.E)

        # Operation buttons
        ttk.Button(btn_frame, text="Load File", command=self.load_file_content, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save Changes", command=self.save_file, style='Success.TButton').pack(side=tk.LEFT,padx=5)

        # Configure row/column weights
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(1, weight=1)

    def browse_file(self, entry_widget=None):
        """Open file dialog to select a file"""
        filename = filedialog.askopenfilename()
        if filename:
            if entry_widget:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, filename)
            else:
                self.filename_entry.delete(0, tk.END)
                self.filename_entry.insert(0, filename)

    def create_file(self):
        """Create a new file"""
        filename = self.filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Input Error", "Please enter a file name", parent=self.root)
            return

        try:
            with open(filename, 'x') as f:
                self.status_var.set(f"File '{filename}' created successfully")
                messagebox.showinfo("Success", f"File '{filename}' created successfully", parent=self.root)
                self.view_all_files()
        except FileExistsError:
            messagebox.showwarning("Error", f"File '{filename}' already exists", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file: {str(e)}", parent=self.root)

    def view_all_files(self):
        """Display all files in the directory"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        files = os.listdir()
        if not files:
            self.tree.insert('', 'end', text="1", values=("No files found", "", ""))
            return

        for i, file in enumerate(files, 1):
            try:
                size = os.path.getsize(file) / 1024  # Size in KB
                file_type = "Folder" if os.path.isdir(file) else "File"
                self.tree.insert('', 'end', text=str(i), values=(file, f"{size:.2f}", file_type))
            except:
                self.tree.insert('', 'end', text=str(i), values=(file, "N/A", "Unknown"))

        self.status_var.set(f"Displaying {len(files)} files")

    def delete_file(self):
        """Delete a file"""
        filename = self.filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Input Error", "Please enter a file name", parent=self.root)
            return

        if not os.path.exists(filename):
            messagebox.showwarning("Error", f"File '{filename}' not found", parent=self.root)
            return

        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete '{filename}'?", parent=self.root):
            return

        try:
            os.remove(filename)
            self.status_var.set(f"File '{filename}' deleted successfully")
            messagebox.showinfo("Success", f"File '{filename}' deleted successfully", parent=self.root)
            self.view_all_files()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {str(e)}", parent=self.root)

    def read_file(self):
        """Read and display file content"""
        filename = self.filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Input Error", "Please enter a file name", parent=self.root)
            return

        if not os.path.exists(filename):
            messagebox.showwarning("Error", f"File '{filename}' not found", parent=self.root)
            return

        try:
            with open(filename, 'r') as f:
                content = f.read()
                # Create a new window to display content
                content_window = tk.Toplevel(self.root)
                content_window.title(f"Content of {filename}")
                content_window.geometry("700x500")

                text_widget = scrolledtext.ScrolledText(content_window, wrap=tk.WORD, font=('Consolas', 10))
                text_widget.pack(fill=tk.BOTH, expand=True)
                text_widget.insert(tk.END, content)
                text_widget.config(state=tk.DISABLED)

                self.status_var.set(f"Displaying content of '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}", parent=self.root)

    def load_file_content(self):
        """Load file content into editor"""
        filename = self.edit_filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Input Error", "Please enter a file name", parent=self.root)
            return

        if not os.path.exists(filename):
            messagebox.showwarning("Error", f"File '{filename}' not found", parent=self.root)
            return

        try:
            with open(filename, 'r') as f:
                content = f.read()
                self.content_editor.delete(1.0, tk.END)
                self.content_editor.insert(tk.END, content)
                self.status_var.set(f"Loaded content of '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}", parent=self.root)

    def save_file(self):
        """Save changes to file"""
        filename = self.edit_filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Input Error", "Please enter a file name", parent=self.root)
            return

        content = self.content_editor.get(1.0, tk.END)

        try:
            with open(filename, 'w') as f:
                f.write(content)
                self.status_var.set(f"Changes to '{filename}' saved successfully")
                messagebox.showinfo("Success", f"Changes to '{filename}' saved successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}", parent=self.root)


def main():
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()