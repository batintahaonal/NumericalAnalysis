import json
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

def fixed_point_iteration(function, initial_guess, tol, max_iter):
    x_n = initial_guess
    iteration_history = [x_n]
    for iteration in range(1, max_iter + 1):
        try:
            x_n1 = function(x_n)
        except Exception as e:
            return {"error": f"Function evaluation error: {e}"}
        iteration_history.append(x_n1)
        if abs(x_n1 - x_n) < tol:
            return {"root": x_n1, "iterations": iteration, "iteration_history": iteration_history}
        x_n = x_n1
    return {"root": x_n1, "iterations": max_iter, "iteration_history": iteration_history}

def second_step(json_input):
    input_data = json.loads(json_input)
    func_str = input_data["function"]  # e.g., "np.cos(x)"
    initial_guess = float(input_data["initialGuess"])
    tol = float(input_data["tol"])
    max_iter = int(input_data["maxIter"])

    # Convert the function string to a Python function safely
    try:
        function = lambda x: eval(func_str, {"x": x, "np": np, "math": np})
    except Exception as e:
        return json.dumps({"error": f"Function parsing error: {e}"})

    result = fixed_point_iteration(function, initial_guess, tol, max_iter)
    return json.dumps(result)

def plot_iteration_history(iteration_history):
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(range(len(iteration_history)), iteration_history, marker='o')
    ax.set(xlabel='Iteration', ylabel='Root Estimate',
           title='Fixed-Point Iteration History')
    ax.grid()
    return fig

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Fixed-Point Iteration GUI")

        self.label = tk.Label(self, text="Enter JSON Input (e.g. {'function': 'np.cos(x)', ...}):")
        self.label.pack()

        self.input_entry = tk.Entry(self, width=80)
        self.input_entry.pack()

        self.run_button = tk.Button(self, text="Run Iteration", command=self.run_iteration)
        self.run_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack()

        self.canvas = None  # Store canvas to clear it later

    def run_iteration(self):
        json_input = self.input_entry.get()
        result_json = second_step(json_input)
        result_dict = json.loads(result_json)

        if "error" in result_dict:
            self.result_label.config(text="Error: " + result_dict["error"])
            return

        root = result_dict["root"]
        iterations = result_dict["iterations"]
        iteration_history = result_dict["iteration_history"]

        self.result_label.config(
            text=f"Root: {root:.6f}, Iterations: {iterations}"
        )

        # Clear previous canvas
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Plot the iteration history
        fig = plot_iteration_history(iteration_history)
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
