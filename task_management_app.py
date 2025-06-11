import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from tkinter.scrolledtext import ScrolledText


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f7fa")
        self.root.resizable(True, True)

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.text_font = tkfont.Font(family="Arial", size=12)

        # Colors
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"
        self.accent_color = "#4fc3f7"
        self.success_color = "#2ecc71"
        self.danger_color = "#e74c3c"
        self.warning_color = "#f39c12"
        self.bg_color = "#f5f7fa"

        # Task list
        self.tasks = []

        self.setup_ui()

    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=100)
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Task Management System",font=self.title_font, bg=self.primary_color, fg="white")
        title_label.pack(pady=20)

        # Main Container Frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Panel - Task Input
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Task Entry
        task_label = tk.Label(left_frame, text="Enter Task:", font=self.text_font, bg=self.bg_color)
        task_label.pack(anchor="w", pady=5)

        self.task_entry = ttk.Entry(left_frame, font=self.text_font, width=30)
        self.task_entry.pack(pady=5)

        # Buttons Frame
        buttons_frame = tk.Frame(left_frame, bg=self.bg_color)
        buttons_frame.pack(pady=20)

        # Add Button
        add_btn = tk.Button(buttons_frame, text="Add Task", font=self.button_font,bg=self.success_color, fg="white", width=12,command=self.add_task)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        # Update Button
        update_btn = tk.Button(buttons_frame, text="Update Task", font=self.button_font,bg=self.warning_color, fg="white", width=12,command=self.update_task_dialog)
        update_btn.grid(row=0, column=1, padx=5, pady=5)

        # Delete Button
        delete_btn = tk.Button(buttons_frame, text="Delete Task", font=self.button_font,bg=self.danger_color, fg="white", width=12,command=self.delete_task_dialog)
        delete_btn.grid(row=1, column=0, padx=5, pady=5)

        # Clear All Button
        clear_btn = tk.Button(buttons_frame, text="Clear All", font=self.button_font,bg=self.danger_color, fg="white", width=12,command=self.clear_all_tasks)
        clear_btn.grid(row=1, column=1, padx=5, pady=5)

        # Right Panel - Task Display
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Task List Label
        task_list_label = tk.Label(right_frame, text="Your Tasks:", font=self.text_font, bg=self.bg_color)
        task_list_label.pack(anchor="w", pady=5)

        # Task List Display
        self.task_list = ScrolledText(right_frame, font=self.text_font,width=40, height=15, wrap=tk.WORD,bg="white", fg="#333333", padx=10, pady=10)
        self.task_list.pack(fill="both", expand=True)
        self.task_list.config(state="disabled")

        # Configure tags for highlighting
        self.task_list.tag_config("updated", foreground="green", font=self.text_font)
        self.task_list.tag_config("normal", font=self.text_font)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,anchor=tk.W, font=self.text_font, bg="#e0e0e0")
        self.status_bar.pack(fill="x", padx=10, pady=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.update_task_display()
            self.status_bar.config(text=f"Task '{task}' added successfully", fg="black")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task")

    def update_task_dialog(self):
        if not self.tasks:
            messagebox.showwarning("Warning", "No tasks available to update")
            return

        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Task")
        self.update_window.geometry("400x300")
        self.update_window.configure(bg=self.bg_color)
        self.update_window.grab_set()  # Make window modal

        # Current Task Selection
        tk.Label(self.update_window, text="Select Task to Update:",font=self.text_font, bg=self.bg_color).pack(pady=10)

        self.task_var = tk.StringVar()
        self.task_combobox = ttk.Combobox(self.update_window, textvariable=self.task_var,values=self.tasks, font=self.text_font, state="readonly")
        self.task_combobox.pack(pady=5)
        self.task_combobox.current(0)

        # Bind selection event
        self.task_combobox.bind("<<ComboboxSelected>>", self.show_selected_task)

        # New Task Entry
        tk.Label(self.update_window, text="Enter New Task:",font=self.text_font, bg=self.bg_color).pack(pady=10)

        self.new_task_entry = ttk.Entry(self.update_window, font=self.text_font)
        self.new_task_entry.pack(pady=5)
        self.new_task_entry.insert(0, self.task_combobox.get())

        # Update Button
        update_btn = tk.Button(self.update_window, text="Update", font=self.button_font,bg=self.warning_color, fg="white", width=12,command=self.update_task)
        update_btn.pack(pady=20)

    def show_selected_task(self, event=None):
        """Update the entry field with the currently selected task"""
        selected_task = self.task_combobox.get()
        self.new_task_entry.delete(0, tk.END)
        self.new_task_entry.insert(0, selected_task)

    def update_task(self):
        old_task = self.task_var.get()
        new_task = self.new_task_entry.get().strip()

        if not new_task:
            messagebox.showwarning("Warning", "Please enter a new task")
            return

        if old_task == new_task:
            messagebox.showinfo("Info", "No changes made - task is the same")
            return

        try:
            index = self.tasks.index(old_task)
            self.tasks[index] = new_task
            self.update_task_display(updated_index=index)
            self.status_bar.config(text=f"Task updated: '{old_task}' → '{new_task}'", fg="black")
            self.update_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Selected task not found in list")

    def delete_task_dialog(self):
        if not self.tasks:
            messagebox.showwarning("Warning", "No tasks available to delete")
            return

        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Delete Task")
        self.delete_window.geometry("400x200")
        self.delete_window.configure(bg=self.bg_color)
        self.delete_window.grab_set()  # Make window modal

        # Task Selection
        tk.Label(self.delete_window, text="Select Task to Delete:",font=self.text_font, bg=self.bg_color).pack(pady=20)

        self.del_task_var = tk.StringVar()
        task_combobox = ttk.Combobox(self.delete_window, textvariable=self.del_task_var,values=self.tasks, font=self.text_font, state="readonly")
        task_combobox.pack(pady=5)
        task_combobox.current(0)

        # Delete Button
        delete_btn = tk.Button(self.delete_window, text="Delete", font=self.button_font,bg=self.danger_color, fg="white", width=12,command=self.delete_task)
        delete_btn.pack(pady=20)

    def delete_task(self):
        task = self.del_task_var.get()
        self.tasks.remove(task)
        self.update_task_display()
        self.status_bar.config(text=f"Task '{task}' deleted successfully", fg="black")
        self.delete_window.destroy()

    def clear_all_tasks(self):
        if not self.tasks:
            messagebox.showwarning("Warning", "No tasks to clear")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            self.update_task_display()
            self.status_bar.config(text="All tasks cleared", fg="black")

    def update_task_display(self, updated_index=None):
        self.task_list.config(state="normal")
        self.task_list.delete(1.0, tk.END)

        if self.tasks:
            for i, task in enumerate(self.tasks, 1):
                if updated_index is not None and i - 1 == updated_index:
                    # Highlight the updated task
                    self.task_list.insert(tk.END, f"{i}. ", "normal")
                    self.task_list.insert(tk.END, f"{task}\n", "updated")
                else:
                    self.task_list.insert(tk.END, f"{i}. {task}\n")
        else:
            self.task_list.insert(tk.END, "No tasks added yet")

        self.task_list.config(state="disabled")


def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()