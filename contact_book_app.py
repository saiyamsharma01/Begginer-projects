import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Pro")
        self.root.geometry("800x600")
        self.contacts = {}

        # Modern color palette
        self.primary_bg = "#f0f2f5"  # Light background
        self.secondary_bg = "#e1e5eb"  # Secondary background
        self.accent_color = "#4e73df"  # Blue accent
        self.success_color = "#1cc88a"  # Green for success
        self.danger_color = "#e74a3b"  # Red for danger
        self.text_color = "#2e2e2e"  # Dark text

        # Configure root window
        self.root.configure(bg=self.primary_bg)

        # Custom fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.label_font = Font(family="Helvetica", size=12)
        self.button_font = Font(family="Helvetica", size=10, weight="bold")

        # Create main container
        self.main_frame = tk.Frame(root, bg=self.primary_bg)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header = tk.Label(self.main_frame,text="📒 Contact Book Pro",font=self.title_font,bg=self.primary_bg,fg=self.accent_color)
        self.header.pack(pady=(0, 20))

        # Status bar (moved before view_contacts_tab)
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.main_frame,textvariable=self.status_var,relief=tk.SUNKEN,anchor=tk.W,bg=self.secondary_bg,fg=self.text_color  )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        self.status_var.set("Ready")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_contact_tab()
        self.view_contacts_tab()

    def create_contact_tab(self):
        """Tab for creating/updating contacts"""
        tab = tk.Frame(self.notebook, bg=self.primary_bg)
        self.notebook.add(tab, text="Manage Contacts")

        # Form frame
        form_frame = tk.Frame(tab, bg=self.primary_bg, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Name field
        tk.Label(form_frame,text="Name:",bg=self.primary_bg,fg=self.text_color,font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(form_frame, width=30, font=self.label_font)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Age field
        tk.Label(form_frame,text="Age:",bg=self.primary_bg,fg=self.text_color,font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.age_entry = tk.Entry(form_frame, width=30, font=self.label_font)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Email field
        tk.Label(form_frame,text="Email:",bg=self.primary_bg,fg=self.text_color,font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_entry = tk.Entry(form_frame, width=30, font=self.label_font)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        # Mobile field
        tk.Label(form_frame,text="Mobile:",bg=self.primary_bg,fg=self.text_color,font=self.label_font).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.mobile_entry = tk.Entry(form_frame, width=30, font=self.label_font)
        self.mobile_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        # Buttons frame
        btn_frame = tk.Frame(form_frame, bg=self.primary_bg)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        # Create button
        tk.Button(btn_frame,text="Create Contact",command=self.create_contact,bg=self.success_color,fg="white",font=self.button_font,padx=10,pady=5,bd=0).pack(side=tk.LEFT, padx=5)

        # Update button
        tk.Button(btn_frame,text="Update Contact",command=self.update_contact,bg=self.accent_color,fg="white",font=self.button_font,padx=10,pady=5,bd=0).pack(side=tk.LEFT, padx=5)

        # Delete button
        tk.Button(btn_frame,text="Delete Contact",command=self.delete_contact,bg=self.danger_color,fg="white",font=self.button_font,padx=10,pady=5,bd=0).pack(side=tk.LEFT, padx=5)

        # Search button
        tk.Button(btn_frame,text="Search Contact",command=self.search_contact,bg="#6c757d",fg="white",font=self.button_font,padx=10,pady=5,bd=0).pack(side=tk.LEFT, padx=5)

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def view_contacts_tab(self):
        """Tab for viewing all contacts"""
        tab = tk.Frame(self.notebook, bg=self.primary_bg)
        self.notebook.add(tab, text="View Contacts")

        # Treeview frame
        tree_frame = tk.Frame(tab, bg=self.primary_bg)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview widget
        self.tree = ttk.Treeview(tree_frame,columns=('Name', 'Age', 'Email', 'Mobile'),selectmode='browse')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configure columns
        self.tree.heading('#0', text='#')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Mobile', text='Mobile')

        self.tree.column('#0', width=50, stretch=tk.NO)
        self.tree.column('Name', width=150)
        self.tree.column('Age', width=50, anchor=tk.CENTER)
        self.tree.column('Email', width=200)
        self.tree.column('Mobile', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Count label
        self.count_label = tk.Label(tab,text="Total Contacts: 0",  bg=self.primary_bg,fg=self.text_color,font=self.label_font)
        self.count_label.pack(pady=10)

        # Enhanced Refresh button with icon and animation
        self.refresh_btn = tk.Button(tab,text="🔄 Refresh List",command=self.refresh_contacts,bg=self.accent_color,fg="white",font=self.button_font,padx=10,pady=5,bd=0,activebackground="#3a56b0",activeforeground="white")
        self.refresh_btn.pack(pady=10)

        # Bind double-click event to treeview
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # Initial load
        self.refresh_contacts()

    def on_tree_double_click(self, event):
        """Handle double-click on treeview item to load contact into form"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        if values:
            self.clear_form()
            self.name_entry.insert(0, values[0])
            self.age_entry.insert(0, values[1])
            self.email_entry.insert(0, values[2])
            self.mobile_entry.insert(0, values[3])
            self.notebook.select(0)  # Switch to Manage Contacts tab

    def create_contact(self):
        """Create a new contact"""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        email = self.email_entry.get().strip()
        mobile = self.mobile_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Please enter a name", parent=self.root)
            return

        if name in self.contacts:
            messagebox.showwarning("Error", f"Contact '{name}' already exists", parent=self.root)
            return

        if not age.isdigit():
            messagebox.showwarning("Input Error", "Age must be a number", parent=self.root)
            return

        self.contacts[name] = {
            'age': int(age),
            'email': email,
            'mobile': mobile
        }

        messagebox.showinfo("Success", f"Contact '{name}' created successfully", parent=self.root)
        self.status_var.set(f"Contact '{name}' created successfully")
        self.clear_form()
        self.refresh_contacts()

    def update_contact(self):
        """Update an existing contact"""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        email = self.email_entry.get().strip()
        mobile = self.mobile_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Please enter a name", parent=self.root)
            return

        if name not in self.contacts:
            messagebox.showwarning("Error", f"Contact '{name}' not found", parent=self.root)
            return

        if not age.isdigit():
            messagebox.showwarning("Input Error", "Age must be a number", parent=self.root)
            return

        self.contacts[name] = {
            'age': int(age),
            'email': email,
            'mobile': mobile
        }

        messagebox.showinfo("Success", f"Contact '{name}' updated successfully", parent=self.root)
        self.status_var.set(f"Contact '{name}' updated successfully")
        self.refresh_contacts()

    def delete_contact(self):
        """Delete a contact"""
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Error", "Please enter a name", parent=self.root)
            return

        if name not in self.contacts:
            messagebox.showwarning("Error", f"Contact '{name}' not found", parent=self.root)
            return

        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete '{name}'?", parent=self.root):
            return

        del self.contacts[name]
        messagebox.showinfo("Success", f"Contact '{name}' deleted successfully", parent=self.root)
        self.status_var.set(f"Contact '{name}' deleted successfully")
        self.clear_form()
        self.refresh_contacts()

    def search_contact(self):
        """Search for a contact"""
        search_term = self.name_entry.get().strip()

        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term", parent=self.root)
            return

        found = False
        for name, contact in self.contacts.items():
            if search_term.lower() in name.lower():
                self.display_contact(name, contact)
                found = True

        if not found:
            messagebox.showinfo("Search", "No contacts found with that name", parent=self.root)
            self.status_var.set("No contacts found with that name")

    def display_contact(self, name, contact):
        """Display contact details in the form"""
        self.clear_form()
        self.name_entry.insert(0, name)
        self.age_entry.insert(0, contact['age'])
        self.email_entry.insert(0, contact['email'])
        self.mobile_entry.insert(0, contact['mobile'])

    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)

    def refresh_contacts(self):
        """Refresh the contacts list with enhanced features"""
        # Animate the refresh button
        self.refresh_btn.config(text="⏳ Refreshing...")
        self.root.update()

        try:
            # Clear current items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add contacts to treeview with sorting
            sorted_contacts = sorted(self.contacts.items(), key=lambda x: x[0].lower())

            for i, (name, contact) in enumerate(sorted_contacts, 1):
                self.tree.insert(
                    '',
                    'end',
                    text=str(i),
                    values=(
                        name,
                        contact['age'],
                        contact['email'],
                        contact['mobile']
                    )
                )

            # Update count
            self.count_label.config(text=f"Total Contacts: {len(self.contacts)}")
            self.status_var.set(f"Displaying {len(self.contacts)} contacts")

            # Restore refresh button after completion
            self.refresh_btn.config(text="🔄 Refresh List")

        except Exception as e:
            self.status_var.set(f"Error refreshing contacts: {str(e)}")
            messagebox.showerror("Error", f"Failed to refresh contacts: {str(e)}", parent=self.root)
            self.refresh_btn.config(text="🔄 Refresh List")


def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()