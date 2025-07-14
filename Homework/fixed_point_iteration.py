import json
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
def fixed_point_iteration(function, initial_guess, tol, max_iter):
    x_n = initial_guess
    iteration_history = [x_n]
    for iteration in range(1, max_iter + 1):
        x_n1 = function(x_n)
        iteration_history.append(x_n1)
        if abs(x_n1 - x_n) < tol:
            return {"root": x_n1, "iterations": iteration, "iteration_history": iteration_history}
        if iteration == max_iter:
            return {"root": x_n1, "iterations": iteration, "iteration_history": iteration_history}
        x_n = x_n1
def second_step(json_input):
    input_data = json.loads(json_input)
    function = input_data["function"]
    initial_guess = input_data["initialGuess"]
    tol = input_data["tol"]
    max_iter = input_data["maxIter"]
    result = fixed_point_iteration(function, initial_guess, tol, max_iter)
    return json.dumps(result)
def plot_iteration_history(iteration_history):
    fig, ax = plt.subplots()
    ax.plot(iteration_history, marker='o')
    ax.set(xlabel='Iteration', ylabel='Root Estimate',
           title='Fixed-Point Iteration History')
    ax.grid()
    return fig

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Fixed-Point Iteration GUI")

        self.label = tk.Label(self, text="Enter JSON Input:")
        self.label.pack()

        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.pack()

        self.run_button = tk.Button(self, text="Run Iteration", command=self.run_iteration)
        self.run_button.pack()

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack()

    def run_iteration(self):
        json_input = self.input_entry.get()
        result_json = second_step(json_input)
        result_dict = json.loads(result_json)

        iteration_history = []  # You need to collect iteration history during the Fixed-Point Iteration

        # Plot the iteration history
        fig = plot_iteration_history(iteration_history)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()

