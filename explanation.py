import tkinter as tk

class Explanation:
    def __init__(self):
        self.user_accepted = False
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.mainloop()

    def setup_window(self):
        self.root.title("Explanation")
        self.root.wm_attributes('-fullscreen', True)  
        self.root.bind('<Escape>', self.toggle_fullscreen)

    def toggle_fullscreen(self, event):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def create_widgets(self):
        self.create_welcome_message()
        self.create_accept_button()

    def create_welcome_message(self):
        message = ('\n\nThis are the instructions for the experiment. Read them carefully before continuing.\n\n'
                   'During this experiment you will solve simple equations, consisting of 3 numbers and 2 symbols (e.g. 1 + 2 - 3).\n'
                   'The final answers to these equations will always be single digits between and including 0 and 9.\n'
                   'Try to solve as many of these equations as accurately as possible.\n\n'
                   'You will first get a practice round to get acquainted with the task.\n'
                   'The practice round consists of 5 blocks of 30 seconds in which you are presented the equations.\n'
                   'In between these blocks of equations, you will get 20 seconds rest.\n'
                   'During this rest period you will see a fixation dot on the screen.\n'
                   'At the end of the rest, a countdown will show when the equations will appear again.\n\n'
                   'After completion of the practice round you will receive further instructions.\n'
                   'In case you have any questions, you can ask them now.\n'
                   'Whenever you are ready to start, click on "Begin!" to start your practise round.\n'
                   'Be aware that the experiment will start right after you click the button.'
                   )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_accept_button(self):
        accept_button = tk.Button(
            self.root,
            text="Begin!",
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
