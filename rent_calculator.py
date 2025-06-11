import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont


class RentCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Rent Calculator")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(True,True)

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=12)
        self.button_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.result_font = tkfont.Font(family="Courier", size=14, weight="bold")

        # Colors
        self.primary_color = "#4a6fa5"
        self.secondary_color = "#166088"
        self.accent_color = "#4fc3f7"
        self.bg_color = "#f5f5f5"

        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Rent Calculator",font=self.title_font, bg=self.primary_color, fg="white")
        title_label.pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)

        # Rent Entry
        rent_label = tk.Label(input_frame, text="Hostel/Flat Rent (₹):",font=self.label_font, bg=self.bg_color)
        rent_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.rent_entry = ttk.Entry(input_frame, font=self.label_font)
        self.rent_entry.grid(row=0, column=1, padx=10, pady=10)

        # Food Entry
        food_label = tk.Label(input_frame, text="Food Ordered (₹):",font=self.label_font, bg=self.bg_color)
        food_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.food_entry = ttk.Entry(input_frame, font=self.label_font)
        self.food_entry.grid(row=1, column=1, padx=10, pady=10)

        # Electricity Units
        elec_label = tk.Label(input_frame, text="Electricity Units Spent:",font=self.label_font, bg=self.bg_color)
        elec_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.elec_entry = ttk.Entry(input_frame, font=self.label_font)
        self.elec_entry.grid(row=2, column=1, padx=10, pady=10)

        # Charge per Unit
        charge_label = tk.Label(input_frame, text="Charge per Unit (₹):",font=self.label_font, bg=self.bg_color)
        charge_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.charge_entry = ttk.Entry(input_frame, font=self.label_font)
        self.charge_entry.grid(row=3, column=1, padx=10, pady=10)

        # Persons
        persons_label = tk.Label(input_frame, text="Number of Persons:",font=self.label_font, bg=self.bg_color)
        persons_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.persons_entry = ttk.Entry(input_frame, font=self.label_font)
        self.persons_entry.grid(row=4, column=1, padx=10, pady=10)

        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Calculate Button
        calc_button = tk.Button(button_frame, text="Calculate", font=self.button_font,bg=self.secondary_color, fg="white", padx=20,command=self.calculate_rent)
        calc_button.pack(side="left", padx=10)

        # Reset Button
        reset_button = tk.Button(button_frame, text="Reset", font=self.button_font,bg="#e74c3c", fg="white", padx=20,command=self.reset_fields)
        reset_button.pack(side="left", padx=10)

        # Result Frame
        result_frame = tk.Frame(self.root, bg=self.bg_color)
        result_frame.pack(pady=20)

        self.result_label = tk.Label(result_frame, text="",font=self.result_font, bg=self.bg_color, fg="#2c3e50")
        self.result_label.pack()

        # Breakdown Frame
        self.breakdown_frame = tk.Frame(self.root, bg=self.bg_color)

        self.rent_breakdown = tk.Label(self.breakdown_frame, text="",font=self.label_font, bg=self.bg_color)
        self.rent_breakdown.pack(anchor="w")

        self.food_breakdown = tk.Label(self.breakdown_frame, text="",font=self.label_font, bg=self.bg_color)
        self.food_breakdown.pack(anchor="w")

        self.electricity_breakdown = tk.Label(self.breakdown_frame, text="",font=self.label_font, bg=self.bg_color)
        self.electricity_breakdown.pack(anchor="w")

        self.total_breakdown = tk.Label(self.breakdown_frame, text="",font=self.label_font, bg=self.bg_color)
        self.total_breakdown.pack(anchor="w")

        self.per_person_breakdown = tk.Label(self.breakdown_frame, text="",font=self.result_font, bg=self.bg_color, fg="#27ae60")
        self.per_person_breakdown.pack(anchor="w", pady=10)

    def calculate_rent(self):
        try:
            # Get values from entries
            rent = float(self.rent_entry.get())
            food = float(self.food_entry.get())
            electricity_units = float(self.elec_entry.get())
            charge_per_unit = float(self.charge_entry.get())
            persons = int(self.persons_entry.get())

            if persons <= 0:
                messagebox.showerror("Error", "Number of persons must be greater than 0")
                return

            # Calculate total electricity bill
            electricity_bill = electricity_units * charge_per_unit

            # Calculate total amount and per person share
            total_amount = rent + food + electricity_bill
            per_person = total_amount / persons

            # Display results
            self.result_label.config(text=f"Each person will pay: ₹{per_person:.2f}")

            # Show breakdown
            self.breakdown_frame.pack(pady=10)
            self.rent_breakdown.config(text=f"Rent: ₹{rent:.2f} (₹{rent / persons:.2f} per person)")
            self.food_breakdown.config(text=f"Food: ₹{food:.2f} (₹{food / persons:.2f} per person)")
            self.electricity_breakdown.config(text=f"Electricity: {electricity_units} units × ₹{charge_per_unit} = ₹{electricity_bill:.2f} (₹{electricity_bill / persons:.2f} per person)")
            self.total_breakdown.config(text=f"Total Amount: ₹{total_amount:.2f}")
            self.per_person_breakdown.config(text=f"Each person pays: ₹{per_person:.2f}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers in all fields")

    def reset_fields(self):
        # Clear all entry fields
        self.rent_entry.delete(0, tk.END)
        self.food_entry.delete(0, tk.END)
        self.elec_entry.delete(0, tk.END)
        self.charge_entry.delete(0, tk.END)
        self.persons_entry.delete(0, tk.END)

        # Clear results
        self.result_label.config(text="")
        self.breakdown_frame.pack_forget()


def main():
    root = tk.Tk()
    app = RentCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()