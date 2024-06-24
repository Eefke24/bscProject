import tkinter as tk
import random
import time
from experiment.between_exp import BetweenExp


class EquationTask:
    # Define average_response_time as a class attribute
    average_response_time = 3  

    def __init__(self, outlet):
        self.outlet = outlet
        self.correct_answers = 0
        self.total_answers = 0
        self.block_counter = 1
        self.response_times = []
        self.rest_state = False  
        self.countdown = True
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
        self.equation_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 24))
        self.answer_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.answer_entry.focus_force()

    def show_equation(self):
        self.outlet.push_sample([5])
        self.rest_state = False
        self.answer_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.start_time = time.time()  
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
        self.answer_entry.delete(0, tk.END)  

    def show_blank_screen(self):
        self.outlet.push_sample([3])
        self.rest_state = True
        self.equation_label.config(text='')
        self.answer_entry.place_forget()  
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
            if user_answer.isdigit():
                user_answer = int(user_answer)
                if user_answer == self.current_answer:
                    # print("Correct!")
                    self.correct_answers += 1
                # else:
                    # print("Incorrect!")
                self.total_answers += 1
                end_time = time.time()  
                response_time = end_time - self.start_time
                self.response_times.append(response_time)
                self.show_equation()

    # TODO: look into trigger2 and 6 : not working inside if statement?
    def start_block(self):
        if self.block_counter <= 5:
            self.outlet.push_sample([2])
            print(f"Block {self.block_counter} Start")
            self.show_equation()
            self.block_counter += 1
            self.root.after(30000, self.show_blank_screen)  
        else:
            self.calculate_average_response_time()
            self.root.destroy()

    def calculate_average_response_time(self):
        if self.response_times:
            EquationTask.average_response_time = sum(self.response_times) / len(self.response_times)
            print(f"Average response time: {EquationTask.average_response_time:.2f} seconds")
            accuracy = self.correct_answers / self.total_answers * 100
            print(f"Accuracy practice: {accuracy:.1f} %")
        else:
            print("No response times recorded.")

            
