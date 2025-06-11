import qrcode
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os


class UPIQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("UPI QR Code Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2d3436')

        # Color scheme
        self.bg_color = '#f0f2f5'
        self.button_color = '#3498db'
        self.button_hover = '#2980b9'
        self.accent_color = '#2ecc71'

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.header_label = ttk.Label(self.header_frame,text="UPI Payment QR Code Generator",style='Header.TLabel')
        self.header_label.pack()

        # Input frame
        self.input_frame = ttk.LabelFrame(self.main_frame,text="Payment Details",padding=(15, 10))
        self.input_frame.pack(fill=tk.X, pady=(0, 20))

        # UPI ID input
        self.upi_label = ttk.Label(self.input_frame,text="UPI ID:")
        self.upi_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.upi_entry = ttk.Entry(self.input_frame,width=40,font=('Helvetica', 10))
        self.upi_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Recipient Name
        self.name_label = ttk.Label(self.input_frame,text="Recipient Name:")
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.name_entry = ttk.Entry(self.input_frame,width=40,font=('Helvetica', 10))
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Amount (optional)
        self.amount_label = ttk.Label(self.input_frame,text="Amount (₹):")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.amount_entry = ttk.Entry(self.input_frame,width=40,font=('Helvetica', 10))
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        # Note (optional)
        self.note_label = ttk.Label(self.input_frame,text="Note:")
        self.note_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.note_entry = ttk.Entry(self.input_frame,width=40,font=('Helvetica', 10) )
        self.note_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 20))

        self.generate_btn = tk.Button(self.button_frame,text="Generate QR Code",bg=self.button_color,fg='white',activebackground=self.button_hover,
                             activeforeground='white',bd=0, padx=15,pady=8,command=self.generate_qr,font=('Helvetica', 10, 'bold'))
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(self.button_frame,text="Save QR Code",bg=self.accent_color,fg='white',activebackground='#27ae60',
                        activeforeground='white',bd=0,padx=15,pady=8,command=self.save_qr,font=('Helvetica', 10, 'bold'),state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # QR Code display frame
        self.qr_frame = ttk.LabelFrame(self.main_frame,text="Generated QR Code",padding=(15, 10))
        self.qr_frame.pack(fill=tk.BOTH, expand=True)

        self.qr_label = ttk.Label(self.qr_frame,text="QR code will appear here after generation",anchor=tk.CENTER)
        self.qr_label.pack(fill=tk.BOTH, expand=True)

        # Add hover effects
        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=self.button_hover))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=self.button_color))

        self.save_btn.bind("<Enter>", lambda e: self.save_btn.config(bg='#27ae60'))
        self.save_btn.bind("<Leave>", lambda e: self.save_btn.config(bg=self.accent_color))

        # Initialize variables
        self.current_qr = None
        self.qr_image = None

    def generate_qr(self):
        upi_id = self.upi_entry.get()
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        note = self.note_entry.get()

        if not upi_id:
            messagebox.showerror("Error", "Please enter a UPI ID")
            return

        if not name:
            name = "Recipient"

        # Build UPI URL
        upi_url = f"upi://pay?pa={upi_id}&pn={name.replace(' ', '%20')}"

        if amount:
            try:
                float(amount)
                upi_url += f"&am={amount}"
            except ValueError:
                messagebox.showwarning("Warning", "Invalid amount entered. Amount will be ignored.")

        if note:
            upi_url += f"&tn={note.replace(' ', '%20')}"

        # Generate QR code
        try:
            qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,)
            qr.add_data(upi_url)
            qr.make(fit=True)

            self.current_qr = qr.make_image(fill_color="black", back_color="white")

            # Display QR code
            self.display_qr()

            # Enable save button
            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def display_qr(self):
        if self.current_qr:
            # Convert to PhotoImage
            self.qr_image = ImageTk.PhotoImage(self.current_qr)

            # Update label
            self.qr_label.config(image=self.qr_image)
            self.qr_label.image = self.qr_image

    def save_qr(self):
        if not self.current_qr:
            messagebox.showerror("Error", "No QR code to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"), ("All files", "*.*")],title="Save QR Code As")

        if file_path:
            try:
                self.current_qr.save(file_path)
                messagebox.showinfo("Success", f"QR code saved successfully at:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UPIQRGenerator(root)
    root.mainloop()