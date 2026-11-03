import tkinter as tk
from app import CalculatorApp


# Canvas
def main():
    window = tk.Tk()
    app = CalculatorApp(window)

    window.mainloop()


if __name__ == "__main__":
    main()
