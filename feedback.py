import tkinter as tk

class Feedback:
    def __init__(self, accuracy, answers, total, time, reward):
        self.accuracy = accuracy
        self.answers = answers
        self.total = total
        self.time = time
        self.reward = reward
        self.root = tk.Tk()
        self.root.title("Experiment Results")
        self.root.attributes('-fullscreen', True)
        
        self.create_widgets()
        self.root.mainloop()
    
    def create_widgets(self):
        label = tk.Label(self.root, text="Experiment Results", font=("Helvetica", 24))
        label.pack(pady=30)

        time_label = tk.Label(self.root, text=f"Your time limit was set to {self.time / 1000:.2f} seconds", font=("Helvetica", 18))
        time_label.pack(pady=20)

        answer_label = tk.Label(self.root, text=f"You answered {self.answers} out of {self.total} questions in time", font=("Helvetica", 18))
        answer_label.pack(pady=20)

        accuracy_label = tk.Label(self.root, text=f"Your accuracy was: {self.accuracy:.2f}%", font=("Helvetica", 18))
        accuracy_label.pack(pady=20)

        reward_label = tk.Label(self.root, text=f"Your reward is currently € {self.reward:.2f}", font=("Helvetica", 18))
        reward_label.pack(pady=20)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_button.pack(pady=30)