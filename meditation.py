import tkinter as tk

class Meditation:
    def __init__(self):
        self.user_accepted = False
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.mainloop()

    def setup_window(self):
        self.root.title("Explanation")
        self.root.attributes('-fullscreen', True)  
        self.root.bind('<Escape>', self.toggle_fullscreen)

    def toggle_fullscreen(self, event):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def create_widgets(self):
        self.create_consent_message()
        self.create_accept_button()

    def create_consent_message(self):
        message = ('\n\nYou have completed the first part of the experiment.\n'
                   'There will be a break of approximately 15 minutes in which you have to listen to an audio fragment.\n'
                   'After this, you will have to answer some questions about what you have heard.\n\n'
                   'Listen to the instructions of the researcher before coming back to this screen.\n'
                   'NEVER click the button below without permission of the researcher.\n\n'
                   'The second part of this experiment will be a repetition of the task you just did.\n'
                   'Be aware that the second part of the experiment will start right after you click the button.')

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_accept_button(self):
        accept_button = tk.Button(
            self.root,
            text="Begin second part of experiment!",
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
