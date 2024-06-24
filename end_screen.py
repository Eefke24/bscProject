import tkinter as tk

class End:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.mainloop()

    def setup_window(self):
        self.root.title("Between experiments")
        self.root.wm_attributes('-fullscreen', True)  
        self.root.bind('<Escape>', self.toggle_fullscreen)

    def toggle_fullscreen(self, event):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def create_widgets(self):
        self.create_between_message()
        self.create_next_button()

    def create_between_message(self):
        message = ("\n\nYou have completed the experiment!\n"
                   "Thank you for your participation."
                   )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_next_button(self):
        accept_button = tk.Button(
            self.root,
            text="End",
            command=self.accept_consent,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 16),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        accept_button.pack(pady=20)

    def accept_consent(self):
        self.root.destroy()
