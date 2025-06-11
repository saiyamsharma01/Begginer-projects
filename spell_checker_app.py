from spellchecker import SpellChecker
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font


class SpellCheckerApp:
    def __init__(self, root):
        self.root = root
        self.spell = SpellChecker()
        self.setup_ui()

    def setup_ui(self):
        # Color Palette
        self.colors = {
            'primary': '#6C63FF',  # Vibrant purple-blue
            'primary_dark': '#564FD1',  # Darker shade for hover
            'secondary': '#F8F9FA',  # Light gray background
            'accent': '#FF6584',  # Soft pink accent
            'text_dark': '#2D3748',  # Dark text
            'text_light': '#FFFFFF',  # White text
            'text_muted': '#718096',  # Gray text
            'card': '#FFFFFF',  # White card background
            'border': '#E2E8F0',  # Light border
            'success': '#48BB78',  # Green for success messages
            'warning': '#ED8936',  # Orange for warnings
        }

        # Configure main window
        self.root.title("Linguo Spell Checker")
        self.root.geometry("850x650")
        self.root.configure(bg=self.colors['secondary'])
        self.root.minsize(750, 550)

        # Custom fonts
        title_font = Font(family="Segoe UI", size=20, weight="bold")
        button_font = Font(family="Segoe UI", size=12)
        text_font = Font(family="Segoe UI", size=12)
        small_font = Font(family="Segoe UI", size=10)

        # Style configuration
        self.style = ttk.Style()

        # Configure rounded corners for buttons (using ttk doesn't support radius directly)
        self.style.configure('TFrame', background=self.colors['secondary'])

        # Primary Button Style
        self.style.configure('Primary.TButton',font=button_font,foreground=self.colors['text_light'],background=self.colors['primary'],borderwidth=0,padding=12,relief="flat")
        self.style.map('Primary.TButton',foreground=[('pressed', self.colors['text_light']),('active', self.colors['text_light'])],background=[('pressed', self.colors['primary_dark']),('active', self.colors['primary_dark'])])

        # Secondary Button Style
        self.style.configure('Secondary.TButton',font=button_font,foreground=self.colors['text_dark'],background=self.colors['card'],borderwidth=1,bordercolor=self.colors['border'],padding=12,relief="flat")
        self.style.map('Secondary.TButton',foreground=[('pressed', self.colors['text_dark']),('active', self.colors['text_dark'])],background=[('pressed', self.colors['border']),('active', self.colors['border'])])

        # Accent Button Style
        self.style.configure('Accent.TButton',font=button_font,foreground=self.colors['text_light'],background=self.colors['accent'],borderwidth=0,padding=12,relief="flat")
        self.style.map('Accent.TButton',foreground=[('pressed', self.colors['text_light']),('active', self.colors['text_light'])],background=[('pressed', '#E04F70'),('active', '#E04F70')])

        # Header frame with gradient effect
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill="x", padx=0, pady=0)

        tk.Label(header_frame,text="Linguo Spell Checker",font=title_font,bg=self.colors['primary'],fg=self.colors['text_light'],pady=20).pack(pady=10)

        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.colors['secondary'])
        main_frame.pack(fill="both", expand=True, padx=25, pady=15)

        # Input card
        input_card = tk.Frame(main_frame, bg=self.colors['card'],highlightbackground=self.colors['border'],highlightthickness=1)
        input_card.pack(fill="x", pady=(0, 15))

        tk.Label(input_card,text="Enter your text:",font=button_font,bg=self.colors['card'],fg=self.colors['text_dark'],padx=15).pack(anchor="w", pady=(15, 5))  # Fixed pady format here

        self.input_text = scrolledtext.ScrolledText(input_card,wrap=tk.WORD,width=60,height=10,font=text_font,bg=self.colors['card'],fg=self.colors['text_dark'],insertbackground=self.colors['text_dark'],selectbackground=self.colors['primary'],
                                selectforeground=self.colors['text_light'],padx=15,pady=10,bd=0,highlightthickness=0)
        self.input_text.pack(fill="x", padx=15, pady=(0, 15))

        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['secondary'])
        button_frame.pack(fill="x", pady=(0, 15))

        check_button = ttk.Button(button_frame,text="Check Spelling",command=self.check_spelling,style="Primary.TButton" )
        check_button.pack(side="left", padx=(0, 10))

        clear_button = ttk.Button(button_frame,text="Clear Text",command=self.clear_text,style="Secondary.TButton")
        clear_button.pack(side="left")

        # Help button with accent color
        help_button = ttk.Button(button_frame,text="Help",command=self.show_help,style="Accent.TButton")
        help_button.pack(side="right")

        # Output card
        output_card = tk.Frame(main_frame, bg=self.colors['card'],highlightbackground=self.colors['border'],highlightthickness=1)
        output_card.pack(fill="both", expand=True)

        tk.Label(output_card,text="Corrected text:",font=button_font,bg=self.colors['card'],fg=self.colors['text_dark'],padx=15 ).pack(anchor="w", pady=(15, 5))  # Fixed pady format here

        self.output_text = scrolledtext.ScrolledText(output_card,wrap=tk.WORD,width=60,height=10,font=text_font,bg=self.colors['card'],fg=self.colors['text_dark'],state="disabled",
                            padx=15,pady=10,bd=0,highlightthickness=0)
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=40)
        footer_frame.pack(fill="x", padx=25, pady=(0, 10))

        tk.Label(footer_frame,text="© 2023 Linguo Spell Checker | v2.0",font=small_font,bg=self.colors['secondary'],fg=self.colors['text_muted']).pack(side="left")

        # Add a subtle status label
        self.status_label = tk.Label(footer_frame,text="Ready",font=small_font,bg=self.colors['secondary'],fg=self.colors['primary'])
        self.status_label.pack(side="right")

    def check_spelling(self):
        self.status_label.config(text="Checking...", fg=self.colors['primary'])
        self.root.update()

        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            self.status_label.config(text="Please enter text", fg=self.colors['warning'])
            messagebox.showwarning("Empty Input", "Please enter some text to check.")
            return

        words = text.split()
        corrected_words = []
        corrections = []

        for word in words:
            corrected_word = self.spell.correction(word)
            if corrected_word is not None and corrected_word.lower() != word.lower():
                corrections.append((word, corrected_word))
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)

        corrected_text = ' '.join(corrected_words)

        # Display corrections in output area
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, corrected_text)
        self.output_text.config(state="disabled")

        # Update status
        if corrections:
            self.status_label.config(text=f"Found {len(corrections)} corrections", fg=self.colors['success'])
            correction_list = "\n".join([f"• '{orig}' → '{corr}'" for orig, corr in corrections])
            messagebox.showinfo(
                "Corrections Made",
                f"The following corrections were made:\n\n{correction_list}",
                parent=self.root
            )
        else:
            self.status_label.config(text="No errors found", fg=self.colors['success'])
            messagebox.showinfo("No Corrections", "No spelling errors found!", parent=self.root)

    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        self.status_label.config(text="Ready", fg=self.colors['primary'])

    def show_help(self):
        help_text = """Linguo Spell Checker Help:

1. Type or paste your text into the input box
2. Click 'Check Spelling' to analyze your text
3. View corrected text in the output panel
4. Use 'Clear Text' to reset both panels

Features:
- Automatic spelling correction
- Color-coded interface
- Status notifications
- Modern, clean design"""
        messagebox.showinfo("Help", help_text, parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        # Windows style
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    app = SpellCheckerApp(root)
    root.mainloop()