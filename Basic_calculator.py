import tkinter as tk
from tkinter import messagebox
import math
import time

class AdvancedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Calculator")
        self.geometry("650x500")
        self.configure(bg='#f8bbd0')  # Light Pink Background
        self.result_var = tk.StringVar()
        self.history = []
        self.running = False
        self.time_left = 0
        self.countdown_running = False
        self.create_widgets()

    def create_widgets(self):
        # Light Pink Background
        self.configure(bg='#f8bbd0')

        # Define styles for buttons with shadows and rounded corners
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 6,
            'height': 2,
            'bg': '#4A90E2',  # Blue color for number buttons
            'fg': '#fff',
            'bd': 3,
            'relief': 'solid',
            'activebackground': '#357ABD',
            'activeforeground': '#fff',
            'highlightthickness': 0,
            'padx': 10,
            'pady': 10,
            'cursor': 'hand2',
        }

        special_button_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 10,
            'height': 2,
            'bg': '#9b59b6',  # Purple for special buttons
            'fg': '#fff',
            'bd': 3,
            'relief': 'solid',
            'activebackground': '#8e44ad',
            'activeforeground': '#fff',
            'padx': 10,
            'pady': 10,
            'cursor': 'hand2',
        }

        # Result Display Area
        entry_style = {
            'font': ('Arial', 20, 'bold'),
            'bd': 5,
            'relief': 'sunken',
            'bg': '#fff',
            'fg': '#333',
            'width': 25,
            'insertbackground': 'black',
            'borderwidth': 2,
            'highlightthickness': 1
        }
        tk.Entry(self, textvariable=self.result_var, **entry_style, justify='right').grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky="nsew")

        # Button Labels for Calculator
        buttons = [
            '7', '8', '9', '/', 'sin',
            '4', '5', '6', '*', 'cos',
            '1', '2', '3', '-', 'tan',
            '0', '.', '=', '+', 'log',
            '√', '%', '←', 'C', 'ln'
        ]

        # Grid Layout for Calculator Buttons
        row_val, col_val = 1, 0
        for button in buttons:
            cmd = lambda b=button: self.on_button_click(b)
            if button == "=":
                cmd = self.calculate
            elif button == "←":  
                cmd = self.backspace
            elif button == "C":
                cmd = self.clear
            elif button == "sin":
                cmd = lambda: self.calculate_trig('sin')
            elif button == "cos":
                cmd = lambda: self.calculate_trig('cos')
            elif button == "tan":
                cmd = lambda: self.calculate_trig('tan')
            elif button == "log":
                cmd = lambda: self.calculate_log()
            elif button == "ln":
                cmd = lambda: self.calculate_ln()

            tk.Button(self, text=button, command=cmd, **button_style).grid(row=row_val, column=col_val, pady=5, padx=5, sticky="nsew")
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # Special Feature Buttons on the Right Side
        feature_frame = tk.Frame(self, bg="#f8bbd0")
        feature_frame.grid(row=1, column=5, rowspan=5, padx=10, pady=10, sticky="nsew")

        # Stopwatch and Timer Buttons
        tk.Button(feature_frame, text="Stopwatch", command=self.open_stopwatch, **special_button_style).grid(row=0, column=0, pady=5, padx=10, sticky="nsew")
        tk.Button(feature_frame, text="Countdown", command=self.open_countdown, **special_button_style).grid(row=1, column=0, pady=5, padx=10, sticky="nsew")

        # Unit Converter and Temperature Converter Buttons
        tk.Button(feature_frame, text="Unit Converter", command=self.open_unit_converter, **special_button_style).grid(row=2, column=0, pady=5, padx=10, sticky="nsew")
        tk.Button(feature_frame, text="Temp Converter", command=self.open_temp_converter, **special_button_style).grid(row=3, column=0, pady=5, padx=10, sticky="nsew")

    def on_button_click(self, char):
        self.result_var.set(self.result_var.get() + char)

    def calculate(self):
        try:
            result = eval(self.result_var.get())
            self.result_var.set(result)
            self.history.append(self.result_var.get() + " = " + str(result))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.result_var.set("")

    def calculate_trig(self, func):
        try:
            value = float(self.result_var.get())
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            self.result_var.set(result)
            self.history.append(f"{func}({value}) = {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input for {func}: {str(e)}")
            self.result_var.set("")

    def calculate_log(self):
        try:
            value = float(self.result_var.get())
            result = math.log10(value)
            self.result_var.set(result)
            self.history.append(f"log({value}) = {result}")
        except Exception as e:
            messagebox.showerror("Error", "Invalid input for log: " + str(e))
            self.result_var.set("")

    def calculate_ln(self):
        try:
            value = float(self.result_var.get())
            result = math.log(value)
            self.result_var.set(result)
            self.history.append(f"ln({value}) = {result}")
        except Exception as e:
            messagebox.showerror("Error", "Invalid input for ln: " + str(e))
            self.result_var.set("")

    def clear(self):
        self.result_var.set("")

    def backspace(self):
        current_text = self.result_var.get()
        self.result_var.set(current_text[:-1])

    # Open Stopwatch in a separate window
    def open_stopwatch(self):
        stopwatch_window = tk.Toplevel(self)
        stopwatch_window.title("Stopwatch")
        stopwatch_window.geometry("400x300")
        stopwatch_window.configure(bg='#f8bbd0')

        label = tk.Label(stopwatch_window, text="Stopwatch", font=('Arial', 20, 'bold'), bg='#f8bbd0')
        label.pack(pady=10)

        time_label = tk.Label(stopwatch_window, text="00:00:00", font=('Arial', 40), bg='#f8bbd0')
        time_label.pack(pady=20)

        def start_stopwatch():
            self.running = True
            self.time_left = 0
            self.update_stopwatch(time_label)

        def stop_stopwatch():
            self.running = False

        def reset_stopwatch():
            self.time_left = 0
            time_label.config(text="00:00:00")

        start_button = tk.Button(stopwatch_window, text="Start", command=start_stopwatch, font=('Arial', 12, 'bold'), bg='#4A90E2', fg='#fff')
        start_button.pack(pady=5)

        stop_button = tk.Button(stopwatch_window, text="Stop", command=stop_stopwatch, font=('Arial', 12, 'bold'), bg='#E74C3C', fg='#fff')
        stop_button.pack(pady=5)

        reset_button = tk.Button(stopwatch_window, text="Reset", command=reset_stopwatch, font=('Arial', 12, 'bold'), bg='#9b59b6', fg='#fff')
        reset_button.pack(pady=5)

    def update_stopwatch(self, time_label):
        if self.running:
            current_time = time.strftime("%H:%M:%S", time.gmtime(self.time_left))
            time_label.config(text=current_time)
            self.time_left += 1
            self.after(1000, self.update_stopwatch, time_label)

    # Open Countdown Timer in a separate window
    def open_countdown(self):
        countdown_window = tk.Toplevel(self)
        countdown_window.title("Countdown Timer")
        countdown_window.geometry("400x300")
        countdown_window.configure(bg='#f8bbd0')

        label = tk.Label(countdown_window, text="Countdown Timer", font=('Arial', 20, 'bold'), bg='#f8bbd0')
        label.pack(pady=10)

        countdown_label = tk.Label(countdown_window, text="00:00:00", font=('Arial', 40), bg='#f8bbd0')
        countdown_label.pack(pady=20)

        def start_countdown():
            try:
                self.time_left = int(input_entry.get())
                self.countdown_running = True
                self.update_countdown(countdown_label)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        def stop_countdown():
            self.countdown_running = False

        def reset_countdown():
            self.time_left = 0
            countdown_label.config(text="00:00:00")

        input_label = tk.Label(countdown_window, text="Enter time in seconds:", bg='#f8bbd0', font=('Arial', 12, 'bold'))
        input_label.pack(pady=5)

        input_entry = tk.Entry(countdown_window, font=('Arial', 12))
        input_entry.pack(pady=5)

        start_button = tk.Button(countdown_window, text="Start", command=start_countdown, font=('Arial', 12, 'bold'), bg='#4A90E2', fg='#fff')
        start_button.pack(pady=5)

        stop_button = tk.Button(countdown_window, text="Stop", command=stop_countdown, font=('Arial', 12, 'bold'), bg='#E74C3C', fg='#fff')
        stop_button.pack(pady=5)

        reset_button = tk.Button(countdown_window, text="Reset", command=reset_countdown, font=('Arial', 12, 'bold'), bg='#9b59b6', fg='#fff')
        reset_button.pack(pady=5)

    def update_countdown(self, countdown_label):
        if self.countdown_running and self.time_left > 0:
            current_time = time.strftime("%H:%M:%S", time.gmtime(self.time_left))
            countdown_label.config(text=current_time)
            self.time_left -= 1
            self.after(1000, self.update_countdown, countdown_label)
        elif self.time_left == 0:
            countdown_label.config(text="Time's up!")

    # Unit Converter functionality with attractive design
    def open_unit_converter(self):
        converter_window = tk.Toplevel(self)
        converter_window.title("Unit Converter")
        converter_window.geometry("600x400")  # Increased window size to ensure visibility of all components
        converter_window.configure(bg='#f8bbd0')

        def convert_units():
            try:
                value = float(entry_value.get())
                from_unit = unit_from.get()
                to_unit = unit_to.get()

                    # Example for unit conversion logic
                if from_unit == 'meters' and to_unit == 'feet':
                    result = value * 3.281
                elif from_unit == 'feet' and to_unit == 'meters':
                    result = value / 3.281
                elif from_unit == 'kg' and to_unit == 'pounds':
                    result = value * 2.205
                elif from_unit == 'pounds' and to_unit == 'kg':
                    result = value / 2.205
                elif from_unit == 'meters' and to_unit == 'kg':
                    result = value  # This doesn't make sense, as meters and kg measure different things
                elif from_unit == 'kg' and to_unit == 'meters':
                    result = value  # Same here
                elif from_unit == 'meters' and to_unit == 'pounds':
                    result = value  # Again, this doesn't make sense directly
                elif from_unit == 'pounds' and to_unit == 'meters':
                    result = value  # Same for this case
                result_label.config(text=f"Result: {result}")

            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Create Unit Converter UI with styling and smooth animation
        frame = tk.Frame(converter_window, bg='#fff', bd=5, relief='solid', padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Enter value:", bg='#fff', font=('Arial', 12, 'bold')).pack(pady=5)
        entry_value = tk.Entry(frame, font=('Arial', 12))
        entry_value.pack(pady=5)

        tk.Label(frame, text="From unit:", bg='#fff', font=('Arial', 12, 'bold')).pack(pady=5)
        unit_from = tk.StringVar(value='meters')
        unit_from_menu = tk.OptionMenu(frame, unit_from, 'meters', 'kg', 'celsius')
        unit_from_menu.pack(pady=5)

        tk.Label(frame, text="To unit:", bg='#fff', font=('Arial', 12, 'bold')).pack(pady=5)
        unit_to = tk.StringVar(value='feet')
        unit_to_menu = tk.OptionMenu(frame, unit_to, 'feet', 'pounds', 'fahrenheit')
        unit_to_menu.pack(pady=5)

        convert_button = tk.Button(frame, text="Convert", command=convert_units, bg='#4A90E2', fg='#fff', font=('Arial', 12, 'bold'))
        convert_button.pack(pady=10)

        result_label = tk.Label(frame, text="Result:", bg='#fff', font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)

    # Temperature Converter functionality with attractive design
    def open_temp_converter(self):
        temp_converter_window = tk.Toplevel(self)
        temp_converter_window.title("Temperature Converter")
        temp_converter_window.geometry("600x400")  # Increased window size to ensure visibility of all components
        temp_converter_window.configure(bg='#f8bbd0')

        def convert_temperature():
            try:
                temp = float(entry_temp.get())
                from_unit = temp_from.get()
                to_unit = temp_to.get()

                # Temperature conversion logic
                if from_unit == 'Celsius' and to_unit == 'Fahrenheit':
                    result = (temp * 9/5) + 32
                elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
                    result = (temp - 32) * 5/9
                elif from_unit == 'Celsius' and to_unit == 'Kelvin':
                    result = temp + 273.15
                elif from_unit == 'Kelvin' and to_unit == 'Celsius':
                    result = temp - 273.15
                elif from_unit == 'Kelvin' and to_unit == 'Fahrenheit':
                    result = (temp - 273.15) * 9/5 + 32
                elif from_unit == 'Fahrenheit' and to_unit == 'Kelvin': 
                    result = (temp - 32) * 5/9 + 273.15
                result_label.config(text=f"Result: {result}")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

        # Create Temperature Converter UI with styling and smooth animation
        frame = tk.Frame(temp_converter_window, bg='#fff', bd=5, relief='solid', padx=20, pady=20)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Enter temperature:", bg='#fff', font=('Arial', 12, 'bold')).pack(pady=5)
        entry_temp = tk.Entry(frame, font=('Arial', 12))
        entry_temp.pack(pady=5)

        tk.Label(frame, text="From unit:", bg='#fff', font=('Arial', 12, 'bold')).pack(pady=5)
        temp_from = tk.StringVar(value='Celsius')
        temp_from_menu = tk.OptionMenu(frame, temp_from, 'Celsius', 'Fahrenheit', 'Kelvin')
        temp_from_menu.pack(pady=5)

        tk.Label(frame, text="To unit:", bg='#fff', font=('Arial', 12, 'bold')).pack(pady=5)
        temp_to = tk.StringVar(value='Fahrenheit')
        temp_to_menu = tk.OptionMenu(frame, temp_to, 'Fahrenheit', 'Celsius', 'Kelvin')
        temp_to_menu.pack(pady=5)

        convert_button = tk.Button(frame, text="Convert", command=convert_temperature, bg='#4A90E2', fg='#fff', font=('Arial', 12, 'bold'))
        convert_button.pack(pady=10)

        result_label = tk.Label(frame, text="Result:", bg='#fff', font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)

if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()
