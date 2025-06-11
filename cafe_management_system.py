import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os


class CafeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Management System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Menu items with prices and images
        self.menu = {
            "Pizza": {"price": 90, "image": "pizza.png"},
            "Pasta": {"price": 60, "image": "pasta.png"},
            "Burger": {"price": 50, "image": "burger.png"},
            "Salad": {"price": 70, "image": "salad.png"},
            "Coffee": {"price": 80, "image": "coffee.png"}
        }

        # Current order with quantities
        self.order_items = {}  # Now using dictionary to store items and quantities
        self.order_total = 0

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.configure('Header.TLabel', font=('Helvetica', 18, 'bold'), foreground='#333')

        # Color scheme
        self.bg_color = '#f5f5f5'
        self.button_color = '#4CAF50'
        self.button_hover = '#45a049'
        self.accent_color = '#FF5722'
        self.text_color = '#333'
        self.cart_button_color = '#2196F3'
        self.cart_button_hover = '#0b7dda'

        # Create widgets first
        self.create_widgets()

        # Then load images (with error handling)
        self.load_images()

    def load_images(self):
        self.menu_images = {}
        for item in self.menu:
            try:
                # Try to load the specified image
                img_path = self.menu[item]["image"]
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                else:
                    # Create a blank image if file doesn't exist
                    img = Image.new('RGB', (150, 150), color='#f5f5f5')

                img = img.resize((150, 150), Image.LANCZOS)
                self.menu_images[item] = ImageTk.PhotoImage(img)

                # Update the image label if it exists
                if hasattr(self, 'image_labels') and item in self.image_labels:
                    self.image_labels[item].config(image=self.menu_images[item])
            except Exception as e:
                print(f"Error loading image for {item}: {e}")
                # Create a blank image as fallback
                img = Image.new('RGB', (150, 150), color='#f5f5f5')
                img = img.resize((150, 150), Image.LANCZOS)
                self.menu_images[item] = ImageTk.PhotoImage(img)

    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.header_label = ttk.Label(self.header_frame,text="Welcome to Delicious Cafe",style='Header.TLabel')
        self.header_label.pack()

        # Menu display frame
        self.menu_frame = ttk.LabelFrame(self.main_frame,text="Our Menu",padding=(15, 10))
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        # Create menu items with images
        self.image_labels = {}  # To store image labels for updating later
        row = 0
        col = 0
        for item, details in self.menu.items():
            item_frame = ttk.Frame(self.menu_frame)
            item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Item image (placeholder, will be updated when images are loaded)
            img_label = ttk.Label(item_frame)
            img_label.pack()
            self.image_labels[item] = img_label  # Store reference to update later

            # Item name and price
            item_label = ttk.Label(item_frame,text=f"{item} - ₹{details['price']}",font=('Helvetica', 10, 'bold'))
            item_label.pack()

            # Add to order button
            add_button = tk.Button(item_frame,text="Add to Order",bg=self.button_color,fg='white',activebackground=self.button_hover,
                        activeforeground='white',bd=0,padx=10,pady=5,command=lambda i=item: self.add_to_order(i),font=('Helvetica', 9))
            add_button.pack(pady=5)

            # Add hover effect
            add_button.bind("<Enter>", lambda e, b=add_button: b.config(bg=self.button_hover))
            add_button.bind("<Leave>", lambda e, b=add_button: b.config(bg=self.button_color))

            col += 1
            if col > 2:  # 3 items per row
                col = 0
                row += 1

        # Order summary frame
        self.order_frame = ttk.LabelFrame(self.main_frame,text="Your Order",padding=(15, 10))
        self.order_frame.pack(fill=tk.X, pady=(20, 10))

        # Order listbox
        self.order_listbox = tk.Listbox(self.order_frame,height=5,font=('Helvetica', 10),bg='white',selectbackground=self.accent_color)
        self.order_listbox.pack(fill=tk.X, pady=5)

        # Total label
        self.total_label = ttk.Label(self.order_frame,text="Total: ₹0",font=('Helvetica', 12, 'bold'),foreground=self.accent_color)
        self.total_label.pack(anchor=tk.E)

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))

        # Cart button
        self.cart_btn = tk.Button(self.button_frame,text="View Cart",bg=self.cart_button_color,fg='white',activebackground=self.cart_button_hover,
                        activeforeground='white',bd=0,padx=20, pady=10,command=self.view_cart,font=('Helvetica', 12))
        self.cart_btn.pack(side=tk.LEFT, padx=5)

        # Checkout button
        self.checkout_btn = tk.Button(self.button_frame,text="Checkout",bg=self.accent_color,fg='white',activebackground='#e64a19',
                            activeforeground='white',bd=0,padx=20,pady=10,command=self.checkout,font=('Helvetica', 12, 'bold'),state=tk.DISABLED)
        self.checkout_btn.pack(side=tk.RIGHT, padx=5)

        # Clear order button
        self.clear_btn = tk.Button(self.button_frame,text="Clear Order",bg='#f44336',fg='white',activebackground='#d32f2f',
                        activeforeground='white',bd=0,padx=20,pady=10,command=self.clear_order,font=('Helvetica', 12))
        self.clear_btn.pack(side=tk.RIGHT, padx=5)

        # Add hover effects
        self.cart_btn.bind("<Enter>", lambda e: self.cart_btn.config(bg=self.cart_button_hover))
        self.cart_btn.bind("<Leave>", lambda e: self.cart_btn.config(bg=self.cart_button_color))

        self.checkout_btn.bind("<Enter>", lambda e: self.checkout_btn.config(bg='#e64a19'))
        self.checkout_btn.bind("<Leave>", lambda e: self.checkout_btn.config(bg=self.accent_color))

        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg='#d32f2f'))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg='#f44336'))

    def add_to_order(self, item):
        price = self.menu[item]["price"]

        # Update quantity if item already exists, else add new item
        if item in self.order_items:
            self.order_items[item] += 1
        else:
            self.order_items[item] = 1

        self.order_total += price

        # Update order listbox
        self.update_order_display()

        # Enable checkout button if items in order
        if self.order_items:
            self.checkout_btn.config(state=tk.NORMAL)

        # Show confirmation
        messagebox.showinfo("Added to Order", f"{item} has been added to your order!")

    def update_order_display(self):
        """Update the order listbox with current items and quantities"""
        self.order_listbox.delete(0, tk.END)
        for item, quantity in self.order_items.items():
            price = self.menu[item]["price"]
            self.order_listbox.insert(tk.END, f"{item} x{quantity} - ₹{price * quantity}")

        # Update total
        self.total_label.config(text=f"Total: ₹{self.order_total}")

    def view_cart(self):
        """Show a popup window with cart details and quantity adjustment"""
        if not self.order_items:
            messagebox.showinfo("Your Cart", "Your cart is empty!")
            return

        cart_window = tk.Toplevel(self.root)
        cart_window.title("Your Cart")
        cart_window.geometry("400x400")
        cart_window.resizable(False, False)

        # Main frame
        cart_frame = ttk.Frame(cart_window, padding=10)
        cart_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(cart_frame, text="Your Cart Items", font=('Helvetica', 14, 'bold')).pack(pady=5)

        # Items frame with scrollbar
        items_frame = ttk.Frame(cart_frame)
        items_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(items_frame)
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add items with quantity controls
        for item, quantity in self.order_items.items():
            item_frame = ttk.Frame(scrollable_frame, padding=5)
            item_frame.pack(fill=tk.X, pady=2)

            # Item name and price
            ttk.Label(item_frame, text=f"{item} - ₹{self.menu[item]['price']} each",
                      font=('Helvetica', 10)).pack(side=tk.LEFT)

            # Quantity controls
            qty_frame = ttk.Frame(item_frame)
            qty_frame.pack(side=tk.RIGHT)

            # Decrease button
            tk.Button(qty_frame, text="-", width=2,command=lambda i=item: self.adjust_quantity(i, -1, cart_window),bg='#f44336', fg='white',bd=0).pack(side=tk.LEFT, padx=2)

            # Quantity display
            ttk.Label(qty_frame, text=str(quantity), width=3).pack(side=tk.LEFT)

            # Increase button
            tk.Button(qty_frame, text="+", width=2,command=lambda i=item: self.adjust_quantity(i, 1, cart_window), bg='#4CAF50', fg='white', bd=0).pack(side=tk.LEFT, padx=2)

            # Remove button
            tk.Button(item_frame, text="Remove",command=lambda i=item: self.remove_item(i, cart_window), bg='#ff9800', fg='white', bd=0, padx=5).pack(side=tk.RIGHT, padx=5)

        # Total label
        ttk.Label(cart_frame, text=f"Total: ₹{self.order_total}",font=('Helvetica', 12, 'bold')).pack(pady=5)

        # Done button
        tk.Button(cart_frame, text="Done", command=cart_window.destroy,bg='#4CAF50', fg='white', padx=20, pady=5).pack(pady=10)

    def adjust_quantity(self, item, change, cart_window):
        """Adjust quantity of an item in the cart"""
        current_qty = self.order_items[item]
        new_qty = current_qty + change

        if new_qty <= 0:
            # Remove item if quantity reaches 0
            del self.order_items[item]
        else:
            self.order_items[item] = new_qty

        # Recalculate total
        self.order_total = sum(self.menu[item]["price"] * qty
                               for item, qty in self.order_items.items())

        # Update displays
        self.update_order_display()

        # Refresh cart window
        cart_window.destroy()
        self.view_cart()

        # Disable checkout if cart is empty
        if not self.order_items:
            self.checkout_btn.config(state=tk.DISABLED)

    def remove_item(self, item, cart_window):
        """Completely remove an item from the cart"""
        if item in self.order_items:
            # Subtract item's total from order total
            self.order_total -= self.menu[item]["price"] * self.order_items[item]
            del self.order_items[item]

            # Update displays
            self.update_order_display()

            # Refresh cart window
            cart_window.destroy()
            self.view_cart()

            # Disable checkout if cart is empty
            if not self.order_items:
                self.checkout_btn.config(state=tk.DISABLED)

    def clear_order(self):
        self.order_items = {}
        self.order_total = 0
        self.order_listbox.delete(0, tk.END)
        self.total_label.config(text="Total: ₹0")
        self.checkout_btn.config(state=tk.DISABLED)

    def checkout(self):
        if not self.order_items:
            messagebox.showwarning("Empty Order", "Your order is empty!")
            return

        order_summary = "\n".join(
            [f"• {item} x{quantity} - ₹{self.menu[item]['price'] * quantity}"
             for item, quantity in self.order_items.items()]
        )

        response = messagebox.askyesno(
            "Confirm Order",
            f"Your Order:\n{order_summary}\n\nTotal: ₹{self.order_total}\n\nConfirm checkout?"
        )

        if response:
            messagebox.showinfo(
                "Order Placed",
                f"Thank you for your order!\n\nYour total is ₹{self.order_total}\n\nPlease proceed to payment."
            )
            self.clear_order()


if __name__ == "__main__":
    root = tk.Tk()
    app = CafeManagementSystem(root)
    root.mainloop()