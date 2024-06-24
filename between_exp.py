import tkinter as tk

class BetweenExp:
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
        message = ("\n\nYou have completed the practice round! Read the following instructions carefully.\n\n"
                  "The actual experiment is very similar to the practice round you just did.\n"
                  "Again, there will be 5 blocks of 30 seconds in which you have to solve as many equations as possible and as accurately as possible.\n\n"
                  "This time, it will be made a little bit harder for you:\n"
                  "- There will be a time limit for each question, based on how fast you answered them in the practice round.\n"
                  "- The reward you will receive for participating in this experiment will depend on your performance.\n"
                  "It will be initialized to 7 euros.\n"
                  "For each incorrect answer you give, your reward will be reduced by 5 cents.\n"
                  "For every correct answer you give, your reward will be increased by 5 cents.\n"
                  "The maximum reward you can receive is 8 euros.\n"
                  "- Your accuracy will be displayed as well as the accuracy of other participants having completed this experiment.\n"
                  "Both your reward and accuracy scores will also be visible to you during the rest period.\n\n"
                  "BEFORE YOU START: let the researcher check the recording of your EEG data.\n\n"
                  "Now, take your time to relax! You can start the experiment whenever you feel ready by clicking on the button.\n"
                  'Be aware that the experiment will start right after you click the button.' 
                   )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

    def create_next_button(self):
        accept_button = tk.Button(
            self.root,
            text="Real Experiment",
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
