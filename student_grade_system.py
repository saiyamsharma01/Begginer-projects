import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font


class StudentGradesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grades Management System")
        self.root.geometry("900x650")

        # Modern color palette
        self.primary_bg = "#f8f9fa"  # Light gray background
        self.secondary_bg = "#e9ecef"  # Slightly darker gray for panels
        self.primary_text = "#212529"  # Dark gray for text
        self.accent_color = "#0d6efd"  # Bootstrap primary blue
        self.success_color = "#198754"  # Bootstrap success green
        self.danger_color = "#dc3545"  # Bootstrap danger red
        self.warning_color = "#ffc107"  # Bootstrap warning yellow
        self.info_color = "#0dcaf0"  # Bootstrap info teal

        # Configure root window background
        self.root.configure(bg=self.primary_bg)

        # Initialize dictionary to store student grades
        self.student_grades = {}

        # Custom font setup
        self.title_font = Font(family="Segoe UI", size=18, weight="bold")
        self.label_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=10, weight="bold")

        # Style configuration
        self.style = ttk.Style()

        # Configure styles
        self.style.configure('TFrame', background=self.primary_bg)
        self.style.configure('TLabel', background=self.primary_bg, foreground=self.primary_text, font=self.label_font)
        self.style.configure('Header.TLabel', font=self.title_font, background=self.primary_bg,foreground=self.accent_color)
        self.style.configure('TNotebook', background=self.secondary_bg)
        self.style.configure('TNotebook.Tab',background=self.secondary_bg,foreground=self.primary_text,padding=[15, 5],font=self.button_font)
        self.style.map('TNotebook.Tab',background=[('selected', self.primary_bg)],foreground=[('selected', self.accent_color)])

        # Button styles
        self.style.configure('TButton',font=self.button_font,borderwidth=1,foreground="white",padding=8)

        # Primary buttons (blue)
        self.style.configure('Primary.TButton', background=self.accent_color)
        self.style.map('Primary.TButton',background=[('active', '#0b5ed7'), ('!active', self.accent_color)])

        # Success buttons (green)
        self.style.configure('Success.TButton', background=self.success_color)
        self.style.map('Success.TButton',background=[('active', '#157347'), ('!active', self.success_color)])

        # Danger buttons (red)
        self.style.configure('Danger.TButton', background=self.danger_color)
        self.style.map('Danger.TButton',background=[('active', '#bb2d3b'), ('!active', self.danger_color)])

        # Info buttons (teal)
        self.style.configure('Info.TButton', background=self.info_color)
        self.style.map('Info.TButton',background=[('active', '#0aa2c0'), ('!active', self.info_color)])

        # Treeview style
        self.style.configure('Treeview',background="white",fieldbackground="white",foreground=self.primary_text,rowheight=25,font=self.label_font)
        self.style.configure('Treeview.Heading',background=self.secondary_bg,foreground=self.primary_text,font=self.button_font)
        self.style.map('Treeview',background=[('selected', '#dee2e6')], foreground=[('selected', self.primary_text)])

        # Create main container
        self.main_frame = ttk.Frame(root, style='TFrame')
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Header with title
        self.header_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.header = ttk.Label(self.header_frame,text="Student Grades Management System",style='Header.TLabel')
        self.header.pack(side=tk.LEFT)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_add_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_view_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame,textvariable=self.status_var,relief=tk.SUNKEN,anchor=tk.W,background=self.secondary_bg,foreground=self.primary_text,font=self.label_font)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        self.status_var.set("Ready to manage student grades")

    def create_add_tab(self):
        """Create the Add Student tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="Add Student")

        # Form frame with border
        form_frame = ttk.Frame(tab, style='TFrame', padding=(20, 15))
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Form title
        ttk.Label(form_frame,text="Add New Student",style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Name entry
        ttk.Label(form_frame, text="Student Name:").grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.add_name_entry = ttk.Entry(form_frame, width=30, font=self.label_font)
        self.add_name_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        # Grade entry
        ttk.Label(form_frame, text="Student Grade:").grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
        self.add_grade_entry = ttk.Entry(form_frame, width=30, font=self.label_font)
        self.add_grade_entry.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)

        # Add button with success color
        add_btn = ttk.Button(form_frame,text="Add Student",command=self.add_student,style='Success.TButton')
        add_btn.grid(row=3, column=1, pady=15, sticky=tk.E)

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def create_update_tab(self):
        """Create the Update Student tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="Update Student")

        # Form frame with border
        form_frame = ttk.Frame(tab, style='TFrame', padding=(20, 15))
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Form title
        ttk.Label(form_frame,text="Update Student Grade",style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Name entry
        ttk.Label(form_frame, text="Student Name:").grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.update_name_entry = ttk.Entry(form_frame, width=30, font=self.label_font)
        self.update_name_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        # Grade entry
        ttk.Label(form_frame, text="New Grade:").grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
        self.update_grade_entry = ttk.Entry(form_frame, width=30, font=self.label_font)
        self.update_grade_entry.grid(row=2, column=1, padx=5, pady=10, sticky=tk.EW)

        # Update button with primary color
        update_btn = ttk.Button(form_frame,text="Update Student",command=self.update_student,style='Primary.TButton')
        update_btn.grid(row=3, column=1, pady=15, sticky=tk.E)

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def create_delete_tab(self):
        """Create the Delete Student tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="Delete Student")

        # Form frame with border
        form_frame = ttk.Frame(tab, style='TFrame', padding=(20, 15))
        form_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Form title with warning color
        ttk.Label(form_frame,text="Delete Student Record",style='Header.TLabel',foreground=self.danger_color).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Name entry
        ttk.Label(form_frame, text="Student Name:").grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.delete_name_entry = ttk.Entry(form_frame, width=30, font=self.label_font)
        self.delete_name_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.EW)

        # Delete button with danger color
        delete_btn = ttk.Button(form_frame,text="Delete Student",command=self.delete_student,style='Danger.TButton')
        delete_btn.grid(row=2, column=1, pady=15, sticky=tk.E)

        # Warning label
        warning_label = ttk.Label(form_frame,text="This action cannot be undone!",foreground=self.danger_color,font=self.label_font)
        warning_label.grid(row=3, column=1, pady=(5, 0), sticky=tk.E)

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def create_view_tab(self):
        """Create the View Students tab"""
        tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(tab, text="View Students")

        # Treeview frame with border
        tree_frame = ttk.Frame(tab, style='TFrame')
        tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview widget
        self.tree = ttk.Treeview(tree_frame,columns=('Name', 'Grade'),yscrollcommand=scrollbar.set,selectmode='browse',style='Treeview')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure columns
        self.tree.heading('#0', text='ID')
        self.tree.heading('Name', text='Student Name')
        self.tree.heading('Grade', text='Grade')

        self.tree.column('#0', width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.tree.column('Name', width=200, anchor=tk.W)
        self.tree.column('Grade', width=100, anchor=tk.CENTER)

        # Configure scrollbar
        scrollbar.config(command=self.tree.yview)

        # Button frame
        button_frame = ttk.Frame(tab, style='TFrame')
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Refresh button
        refresh_btn = ttk.Button(button_frame,text="Refresh List",command=self.display_all_students,style='Primary.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=5)

        # Export button
        export_btn = ttk.Button(button_frame,text="Export to CSV",command=self.export_to_csv,style='Info.TButton')
        export_btn.pack(side=tk.RIGHT, padx=5)

        # Stats label
        self.stats_var = tk.StringVar()
        stats_label = ttk.Label(button_frame,textvariable=self.stats_var,style='TLabel')
        stats_label.pack(side=tk.LEFT, padx=5)
        self.stats_var.set("Total students: 0")

    def add_student(self):
        """Add a new student to the system"""
        name = self.add_name_entry.get().strip()
        grade = self.add_grade_entry.get().strip()

        if not name or not grade:
            messagebox.showwarning("Input Error", "Both name and grade are required!", parent=self.root)
            return

        if name in self.student_grades:
            messagebox.showwarning("Duplicate", f"Student {name} already exists!", parent=self.root)
            return

        self.student_grades[name] = grade
        self.status_var.set(f"Added {name} with grade {grade}")
        messagebox.showinfo("Success", f"Added {name} with grade {grade}", parent=self.root)

        # Clear entries
        self.add_name_entry.delete(0, tk.END)
        self.add_grade_entry.delete(0, tk.END)

        # Update view
        self.display_all_students()

    def update_student(self):
        """Update an existing student's grade"""
        name = self.update_name_entry.get().strip()
        grade = self.update_grade_entry.get().strip()

        if not name or not grade:
            messagebox.showwarning("Input Error", "Both name and grade are required!", parent=self.root)
            return

        if name not in self.student_grades:
            messagebox.showwarning("Not Found", f"Student {name} not found!", parent=self.root)
            return

        self.student_grades[name] = grade
        self.status_var.set(f"Updated {name}'s grade to {grade}")
        messagebox.showinfo("Success", f"Updated {name}'s grade to {grade}", parent=self.root)

        # Clear entries
        self.update_name_entry.delete(0, tk.END)
        self.update_grade_entry.delete(0, tk.END)

        # Update view
        self.display_all_students()

    def delete_student(self):
        """Delete a student from the system"""
        name = self.delete_name_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Student name is required!", parent=self.root)
            return

        if name not in self.student_grades:
            messagebox.showwarning("Not Found", f"Student {name} not found!", parent=self.root)
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion",
                                   f"Are you sure you want to delete {name}?",
                                   parent=self.root):
            return

        del self.student_grades[name]
        self.status_var.set(f"Deleted student {name}")
        messagebox.showinfo("Success", f"Deleted student {name}", parent=self.root)

        # Clear entry
        self.delete_name_entry.delete(0, tk.END)

        # Update view
        self.display_all_students()

    def display_all_students(self):
        """Display all students in the treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.student_grades:
            self.tree.insert('', 'end', text="1", values=("No students found", ""))
            self.stats_var.set("Total students: 0")
            return

        # Add all students to the treeview
        for i, (name, grade) in enumerate(self.student_grades.items(), 1):
            self.tree.insert('', 'end', text=str(i), values=(name, grade))

        self.status_var.set(f"Displaying {len(self.student_grades)} students")
        self.stats_var.set(f"Total students: {len(self.student_grades)}")

    def export_to_csv(self):
        """Example of additional functionality - export to CSV"""
        if not self.student_grades:
            messagebox.showwarning("No Data", "There are no students to export!", parent=self.root)
            return

        # In a real app, you would implement actual CSV export here
        messagebox.showinfo("Export", "Export functionality would save to CSV file", parent=self.root)
        self.status_var.set("Export functionality would save to CSV file")


def main():
    root = tk.Tk()
    app = StudentGradesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()