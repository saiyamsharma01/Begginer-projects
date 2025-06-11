from itertools import cycle
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, font


class SlideshowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Premium Image Slideshow")
        self.root.geometry("850x850")
        self.root.configure(bg='#2E2E2E')

        # Custom font
        self.custom_font = font.Font(family='Helvetica', size=12, weight='bold')

        # Color scheme
        self.bg_color = '#2E2E2E'
        self.button_bg = '#4A4A4A'
        self.button_active_bg = '#5E5E5E'
        self.text_color = '#FFFFFF'
        self.accent_color = '#3498DB'
        self.frame_color = '#3D3D3D'

        # List of images path
        self.image_paths = [
            r"C:\Users\hp\Desktop\detective.jpeg",
            r"C:\Users\hp\Desktop\img22.jpg",
            r"C:\Users\hp\Desktop\images (1).jpg",
            r"C:\Users\hp\Desktop\login_bg.jpg"
        ]

        # Resize the images
        self.image_size = (700, 500)
        try:
            self.images = [Image.open(path).resize(self.image_size) for path in self.image_paths]
            self.photo_images = [ImageTk.PhotoImage(image) for image in self.images]
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load images: {str(e)}")
            self.root.destroy()
            return

        # Create UI elements
        self.create_widgets()

        # Slideshow control variables
        self.slideshow_active = False
        self.slideshow_cycle = cycle(self.photo_images)
        self.current_image = None

    def create_widgets(self):
        # Main container frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title label
        self.title_label = tk.Label(self.main_frame,text="PREMIUM SLIDESHOW",font=('Helvetica', 18, 'bold'),fg=self.accent_color,bg=self.bg_color
        )
        self.title_label.pack(pady=(0, 15))

        # Image frame with stylish border
        self.image_frame = tk.Frame(self.main_frame,bg=self.frame_color,bd=0,highlightthickness=3,highlightbackground=self.accent_color,highlightcolor=self.accent_color)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # Image label with subtle shadow effect
        self.label = tk.Label(self.image_frame,bg=self.frame_color,bd=0)
        self.label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Control panel frame
        self.control_frame = tk.Frame(self.main_frame,bg=self.bg_color)
        self.control_frame.pack(fill=tk.X, pady=(20, 10))

        # Play button with modern style
        self.play_button = tk.Button(self.control_frame,text="▶ PLAY",font=self.custom_font,bg=self.button_bg,fg=self.text_color,activebackground=self.button_active_bg,
                                activeforeground=self.text_color,bd=0,padx=20,pady=8,command=self.start_slideshow,relief=tk.FLAT,highlightthickness=0)
        self.play_button.pack(side=tk.LEFT, padx=10, expand=True)

        # Stop button with modern style
        self.stop_button = tk.Button(self.control_frame,text="■ STOP",font=self.custom_font,bg=self.button_bg,fg=self.text_color,activebackground='#E74C3C',
                                     activeforeground=self.text_color,bd=0,padx=20,pady=8,command=self.stop_slideshow,state=tk.DISABLED,relief=tk.FLAT,highlightthickness=0)
        self.stop_button.pack(side=tk.LEFT, padx=10, expand=True)

        # Status bar
        self.status_bar = tk.Frame(self.main_frame,bg=self.frame_color,height=30)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start slideshow")
        self.status_label = tk.Label(self.status_bar,textvariable=self.status_var,font=('Helvetica', 10),fg=self.text_color,bg=self.frame_color)
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Add hover effects to buttons
        self.play_button.bind("<Enter>", lambda e: self.play_button.config(bg=self.accent_color))
        self.play_button.bind("<Leave>", lambda e: self.play_button.config(bg=self.button_bg))

        self.stop_button.bind("<Enter>", lambda e: self.stop_button.config(bg='#E74C3C'))
        self.stop_button.bind("<Leave>", lambda e: self.stop_button.config(bg=self.button_bg))

    def start_slideshow(self):
        if not self.slideshow_active:
            self.slideshow_active = True
            self.play_button.config(state=tk.DISABLED, bg='#27AE60')
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set("Slideshow running...")
            self.update_image()

    def stop_slideshow(self):
        self.slideshow_active = False
        self.play_button.config(state=tk.NORMAL, bg=self.button_bg)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Slideshow stopped")

    def update_image(self):
        if self.slideshow_active:
            self.current_image = next(self.slideshow_cycle)
            self.label.config(image=self.current_image)
            # Smooth transition effect
            self.label.config(bg=self.frame_color)
            self.root.after(3000, self.update_image)  # 3 second delay


# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SlideshowApp(root)

    # Center the window on screen
    window_width = 850
    window_height = 850
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.mainloop()