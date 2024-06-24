import tkinter as tk
import csv

class Demographics:
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
        self.create_message()

        # Question 1: Gender
        self.gender_label = tk.Label(self.root, text="What is your gender?", font=("Helvetica", 12))
        self.gender_label.pack(pady=10)
        self.gender_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.gender_entry.pack(pady=5)

        # Question 2: Age
        self.age_label = tk.Label(self.root, text="What is your age?", font=("Helvetica", 12))
        self.age_label.pack(pady=10)
        self.age_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.age_entry.pack(pady=5)

        # Question 3: Native Language
        self.language_label = tk.Label(self.root, text="What is your native language?", font=("Helvetica", 12))
        self.language_label.pack(pady=10)
        self.language_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.language_entry.pack(pady=5)

        # Question 4: experience
        self.experience_label = tk.Label(self.root, text="How much experience with meditation do you have?", font=("Helvetica", 12))
        self.experience_label.pack(pady=10)
        self.experience_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.experience_entry.pack(pady=5)

        # Question 5: education
        self.education_label = tk.Label(self.root, text="What is your highest level of education?", font=("Helvetica", 12))
        self.education_label.pack(pady=10)
        self.education_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.education_entry.pack(pady=5)

        self.create_button()

    def create_message(self):
        message = (
            '\n\nWelcome to this experiment. Before we start we would like to ask you a couple of questions.\n'
            'Your data will be processed and stored anonymously and only for the purposes of this study.\n'
            'Please answer all questions thruthfully.\n'
        )

        label = tk.Label(self.root, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

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
        gender = self.gender_entry.get()
        language = self.language_entry.get()
        age = self.age_entry.get()
        experience = self.experience_entry.get()
        education = self.education_entry.get()

        # Do something with the data (e.g., store it, move to the next step, etc.)
        # For demonstration, just print the collected data
        print("Gender:", gender)
        print("Native Language:", language)
        print("Age:", age)
        print("Experience with Meditations:", experience)
        with open("demographics.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([gender, language, age, experience, education])

        self.user_accepted = True
        self.root.destroy()

    def get_user_accepted(self):
        return self.user_accepted
