import tkinter as tk
from tkinter import ttk
import random
import time
from experiment.practise import EquationTask
from experiment.feedback import Feedback

class StressTask:
    reward = 10

    def __init__(self, reward, outlet):
        self.correct_answers = 0
        self.total_answers = 0
        self.missed_answers = 0
        self.block_counter = 1
        StressTask.reward = reward
        self.outlet = outlet
        self.time_limit = EquationTask.average_response_time * 900 # in milli seconds 
        self.rest_state = False  
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.root.bind('<KeyPress>', self.check_answer)
        self.start_block()
        self.root.mainloop()
        
    def setup_window(self):
        self.root.title("Equation Task")
        self.root.attributes('-fullscreen', True)  
        self.root.bind('<Escape>', self.toggle_fullscreen)

    def toggle_fullscreen(self, event):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def create_widgets(self):
        self.equation_label = tk.Label(self.root, font=("Helvetica", 30))
        self.equation_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 24))
        self.answer_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.answer_entry.focus_force()

        # Create bar for time limit
        self.time_label = tk.Label(self.root, text="Time:", font=("Helvetica", 12))
        self.time_limit_bar = tk.Canvas(self.root, width=400, height=20, bg="white", borderwidth=2, relief="sunken")
        
        # Create bar for participant's accuracy
        self.your_accuracy_label = tk.Label(self.root, text="Your Accuracy:", font=("Helvetica", 12))
        self.progress_bar = tk.Canvas(self.root, width=400, height=20, bg="white", borderwidth=2, relief="sunken")
        
        # Create bar for other participants' accuracy
        self.others_accuracy_label = tk.Label(self.root, text="Average Participants Accuracy:", font=("Helvetica", 12))
        self.others_progress_bar = tk.Canvas(self.root, width=400, height=20, bg="white", borderwidth=2, relief="sunken")
        
        # Create reward
        self.reward_label = tk.Label(self.root, text=f"Reward: € {self.reward:.2f}", font=("Helvetica", 14))

        self.show_widgets()

    def show_widgets(self):
        self.answer_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.time_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.time_limit_bar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        self.your_accuracy_label.place(relx=0.25, rely=0.30, anchor=tk.CENTER)
        self.progress_bar.place(relx=0.5, rely=0.30, anchor=tk.CENTER)
        self.progress_bar.create_rectangle(0, 0, 4, 20, fill="red", tag="Your accuracy")
        self.others_accuracy_label.place(relx=0.25, rely=0.25, anchor=tk.CENTER)
        self.others_progress_bar.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        self.others_progress_bar.create_rectangle(0, 0, 83.8 * 4, 20, fill="green", tag="Other participants accuracy")
        self.reward_label.place(relx=0.42, rely=0.15, anchor="nw")

    def update_time_bar(self):
        if not self.rest_state:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            remaining_time = max(self.time_limit - elapsed_time * 1000, 0)  
            width = remaining_time / self.time_limit * 400
            self.time_limit_bar.delete("TimeLimit")  
            self.time_limit_bar.create_rectangle(0, 0, width, 20, fill="blue", tag="TimeLimit")  
            if remaining_time <= 0:
                self.show_feedback_timeout()
                self.show_equation()
            else:
                self.root.after(100, self.update_time_bar)

    def show_equation(self):
        self.outlet.push_sample([5])
        self.rest_state = False
        self.show_widgets()
        self.start_time = time.time()  
        self.update_time_bar()
        symbols = ['+', '-']
        while True:
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
            num3 = random.randint(1, 9)
            symbol1 = random.choice(symbols)
            symbol2 = random.choice(symbols)

            if symbol1 == '+':
                result = num1 + num2
            else:
                result = num1 - num2

            if symbol2 == '+':
                result += num3
            else:
                result -= num3

            if 0 <= result <= 9:
                break

        equation = f"{num1} {symbol1} {num2} {symbol2} {num3} = "
        self.equation_label.config(text=equation)
        self.current_answer = result
        self.answer_entry.delete(0, tk.END)  # Clear answer entry

    def update_progress_bar(self):
        if self.total_answers > 0:
            accuracy = (self.correct_answers / self.total_answers) * 100
        else:
            accuracy = 0
        self.progress_bar.delete("accuracy")
        self.progress_bar.create_rectangle(0, 0, accuracy * 4, 20, fill="red", tag="Your accuracy")

    def show_blank_screen(self):
        self.outlet.push_sample([3])
        self.rest_state = True
        self.equation_label.config(text='')
        self.answer_entry.place_forget()  
        self.time_label.place_forget()
        self.time_limit_bar.place_forget()
        self.create_fixation_dot()
        if self.block_counter < 6:
            self.outlet.push_sample([6])
            self.root.after(17000, self.update_fixation_dot, "3")  
            self.root.after(18000, self.update_fixation_dot, "2")  
            self.root.after(19000, self.update_fixation_dot, "1") 
        self.root.after(20000, self.hide_fixation_dot)  
        self.root.after(20000, self.start_block)  

    def update_fixation_dot(self, text):
        self.fixation_dot.config(text=text)

    def create_fixation_dot(self):
        self.fixation_dot = tk.Label(self.root, text="•", font=("Helvetica", 48))
        self.fixation_dot.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def hide_fixation_dot(self):
        self.fixation_dot.place_forget()

    def check_answer(self, event):
        if not self.rest_state:
            user_answer = event.char
            self.total_answers += 1
            if user_answer.isdigit():
                user_answer = int(user_answer)
                if user_answer == self.current_answer:
                    # print("Correct!")
                    self.correct_answers += 1
                    StressTask.reward += 0.05  
                    self.reward_label.config(text=f"Reward: € {StressTask.reward:.2f}")
                else:
                    # print("Incorrect!")
                    self.show_feedback_wrong_ans()
                self.update_progress_bar()  
                self.show_equation()

    def show_feedback_timeout(self):
        self.outlet.push_sample([8])
        feedback_label = tk.Label(self.root, text="Too late!", font=("Helvetica", 20), fg="red")
        feedback_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        StressTask.reward -= 0.05  
        self.missed_answers += 1
        self.total_answers += 1
        self.reward_label.config(text=f"Reward: € {StressTask.reward:.2f}")
        self.root.after(700, feedback_label.destroy)  

    def show_feedback_wrong_ans(self):
        self.outlet.push_sample([7])
        feedback_label = tk.Label(self.root, text="Wrong Answer!", font=("Helvetica", 20), fg="red")
        feedback_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        StressTask.reward -= 0.05  
        self.reward_label.config(text=f"Reward: € {StressTask.reward:.2f}")
        self.root.after(700, feedback_label.destroy)  

    def start_block(self):
        if self.block_counter <= 5:
            self.outlet.push_sample([2])
            print(f"Block {self.block_counter} Start")
            self.show_equation()
            self.block_counter += 1
            self.root.after(30000, self.show_blank_screen)  
        else:
            accuracy = self.correct_answers / self.total_answers * 100
            print(f"Your accuracy for the questioned you answered was: {accuracy:.1f} %")
            print(f"In total you answered {(self.total_answers - self.missed_answers)} out of {self.total_answers} questions")
            print(f"reward: {StressTask.reward:.2f}")
            self.root.destroy()
            self.outlet.push_sample([9])
            Feedback(accuracy, (self.total_answers - self.missed_answers), self.total_answers, self.time_limit, StressTask.reward)
            



            

# TODO: check grammatica (solve ipv answer)         , practise / practice  
# TODO: 3,2,1 count down after clicking buttons to start



    


