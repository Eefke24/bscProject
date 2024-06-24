import tkinter as tk
import csv

class stressEvaluation:
    def __init__(self):
        self.user_accepted = False
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.mainloop()

    def setup_window(self):
        self.root.title("User Consent Form")
        self.root.wm_attributes('-fullscreen', True)  
        self.root.bind('<Escape>', self.toggle_fullscreen)

    def toggle_fullscreen(self, event):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def create_widgets(self):
        # self.create_message()

        self.stress_label = tk.Label(self.root, text="\n\n\n\n\nAfter finishing this task, how stressful did you find the task on a scale of 1 to 5?\nWith 1 being not stressful at all and 5 being very stressful.", font=("Helvetica", 16))
        self.stress_label.pack(pady=10)
        self.stress_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.stress_entry.pack(pady=5)

        self.create_button()

    # def create_message(self):
    #     message = (
    #         '\n\nAfter havin\n'
    #     )

    #     label = tk.Label(self.root, text=message, font=("Helvetica", 14))
    #     label.pack(pady=20)

    def create_button(self):
        accept_button = tk.Button(
            self.root,
            text="Next",
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
        # Validate the entries (you can add more validation as needed)
        stress = self.stress_entry.get()

        # Do something with the data (e.g., store it, move to the next step, etc.)
        # For demonstration, just print the collected data
        print("Stress level:", stress)
        with open("demographics.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([stress])

        self.user_accepted = True
        self.root.destroy()

    def get_user_accepted(self):
        return self.user_accepted
