import tkinter as tk
from calculations import calculate


class CalculatorApp:
    def __init__(self, window):
        self.window = window
        self.window.title('Calculator')
        self.window.geometry('400x400+20+20')
        self.window.resizable(False, False)
        self.colors = {
            "background": "#1E1E1E",
            "display": "#252525",
            "number": "#333333",
            "operator": "#FF9500",
            "clear": "#555555",
            "text": "#FFFFFF",
        }
        self.window.configure(bg=self.colors["background"])

        self.has_error = False
        self.input_var = tk.StringVar(master=window)
        self.is_calculated = False

        # Buttons
        self.buttons = [
            ['del', 'AC', '%', '/'],
            [7, 8, 9, '*'],
            [4, 5, 6, '-'],
            [1, 2, 3, '+'],
            ['(+/-)', 0, '.', '='],
        ]

        # Button Group
        self.button_groups = {
            "clear": ["del", "AC"],
            "calculate": ["="],
            "operator": ["+", "-", "*", "/", "%"],
            "disabled": ["(+/-)"],
        }

        # Configure 4 equal-width columns
        for col in range(4):
            self.window.grid_columnconfigure(
                col, weight=1, uniform="buttons"
            )

        # Configure button rows
        for row in range(2, 7):
            self.window.grid_rowconfigure(row, minsize=60)

        self.create_display()
        self.create_buttons()

    def reset_error(self):
        self.input_var.set("")
        self.has_error = False
        self.is_calculated = False

    def clear_input(self, text):

        self.is_calculated = False

        if self.has_error:
            self.reset_error()
            return

        if text == 'del':
            self.input_var.set(self.input_var.get()[:-1])
        else:
            self.input_var.set("")

    def expression(self, text):
        current_text = self.input_var.get()

        try:
            result = calculate(current_text)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.input_var.set(result)
            self.has_error = False
            self.is_calculated = True
        except ZeroDivisionError:
            self.input_var.set("Cannot divide by zero")
            self.has_error = True
        except ValueError:
            self.input_var.set("Invalid expression")
            self.has_error = True

    def show_input(self, text):
        if self.has_error:
            self.reset_error()

        current_text = str(self.input_var.get())

        operators = ["+", "-", "*", "/", "%"]

        if text == '(+/-)':
            self.input_var.set(current_text + '')
            return

        if str(text) in operators:
            self.is_calculated = False
            if not current_text or current_text.endswith(tuple(operators)):
                return
        else:
            if self.is_calculated:
                self.input_var.set(str(text))
                self.is_calculated = False
                return

        if text == '.':
            last_index = max(current_text.rfind(op) for op in operators)

            current_str = current_text[last_index + 1:]
            if '.' in current_str:
                return

        self.input_var.set(current_text + str(text))

    def create_display(self):
        self.display = tk.Entry(
            self.window,
            borderwidth=5,
            cursor='arrow',
            font=('Arial', 30),
            bg=self.colors["display"],
            fg=self.colors["text"],
            readonlybackground=self.colors["display"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            state='readonly',
            textvariable=self.input_var,
            exportselection=True,
        )

        self.display.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky='ew',
            padx=12,
            pady=(20, 15),
            ipady=18,
        )

    def create_buttons(self):
        for row, buttonRow in enumerate(self.buttons, start=2):
            for col, text in enumerate(buttonRow):
                if text in self.button_groups["disabled"]:
                    continue

                if text in self.button_groups["clear"]:
                    action = self.clear_input
                    bg_color = self.colors["clear"]

                elif text in self.button_groups["calculate"]:
                    action = self.expression
                    bg_color = self.colors["operator"]

                elif text in self.button_groups["operator"]:
                    action = self.show_input
                    bg_color = self.colors["operator"]

                else:
                    action = self.show_input
                    bg_color = self.colors["number"]

                self.create_button(text, row, col, bg_color, action)

    def create_button(self, text, row, col, bg_color, action):
        button = tk.Label(
            self.window,
            text=text,
            bg=bg_color,
            fg=self.colors["text"],
            font=("Arial", 18),
            relief="flat",
            bd=0,
        )

        button.grid(
            row=row,
            column=col,
            padx=5,
            pady=5,
            sticky='nsew'
        )

        button.bind(
            "<Button-1>",
            lambda event: action(text)
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(bg="#484848")
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=bg_color)
        )
