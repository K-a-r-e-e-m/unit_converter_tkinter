import customtkinter as ctk
import math
import pygame

class UnitConverter:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Unit Converter")
        self.app.geometry("800x800")
        self.is_dark_mode = True

        # Initialize pygame mixer
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound("click_sound.wav")  # Click sound file
        self.exit_sound = pygame.mixer.Sound("exit_sound.wav")  # Exit sound file
        self.tab_switch_sound = pygame.mixer.Sound("click_sound.wav")  # Tab switch sound file

        # Set theme and color scheme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Main title
        self.title_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkLabel(self.title_frame, text="UNIT CONVERTER", font=("Times New Roman", 24, "bold")).pack()

        # Create tabview
        self.tabview = ctk.CTkTabview(self.app)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.theme_button = ctk.CTkButton(
            self.app,
            text="Toggle Light/Dark Mode",
            command=self.toggle_theme,
            width=150
        )
        self.theme_button.pack(pady=10)

        # Add tabs
        self.tabs = ["Welcome", "Area", "Weight", "Length", "Temperature", "Calculator"]
        for tab in self.tabs:
            self.tabview.add(tab)

        self.app.bind("<Configure>", self.on_tab_switch)  # Bind the event

        self.setup_welcome_tab()
        self.setup_converter_tabs()
        self.setup_calculator_tab()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        new_mode = "dark" if self.is_dark_mode else "light"
        ctk.set_appearance_mode(new_mode)

    def on_tab_switch(self, event):
        self.tab_switch_sound.play()  # Play sound when switching tabs

    def setup_welcome_tab(self):
        welcome_frame = self.tabview.tab("Welcome")

        text = """Welcome to the Unit Converter App!"""

        #A frame with some padding and border for the text
        text_frame = ctk.CTkFrame(welcome_frame, border_color="white", border_width=2, corner_radius=10, fg_color="#1f538d")
        text_frame.pack(pady=200, padx=200, fill="both", expand=True)

        ctk.CTkLabel(text_frame, text=text, font=("Arial", 16, "italic")).pack(pady=20, padx=10)

        button_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        # Create grid of buttons
        converters = ["Area", "Weight", "Length", "Temperature", "Calculator"]
        for i, converter in enumerate(converters):
            row = i // 2
            col = i % 2
            ctk.CTkButton(
                button_frame,
                text=f"Open {converter} Converter",
                command=lambda x=converter: [self.click_sound.play(), self.tabview.set(x)],  # Play sound on button click
                width=200
            ).grid(row=row, column=col, padx=10, pady=5)

        ctk.CTkButton(
            button_frame,
            text="Exit",
            command=lambda: [self.exit_sound.play(), self.app.destroy()], 
            fg_color="red",
            hover_color="darkred",
            width=420
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def create_converter_frame(self, tab_name, unit_dict=None, is_temperature=False):
        frame = self.tabview.tab(tab_name)

        ctk.CTkLabel(frame, text=f"{tab_name} Converter", font=("Arial", 20, "bold")).pack(pady=10)

        input_entry = ctk.CTkEntry(frame, placeholder_text="Enter value", width=200)
        input_entry.pack(pady=10)

        from_unit = ctk.CTkOptionMenu(frame, values=list(unit_dict.keys()) if unit_dict else ["Celsius", "Fahrenheit", "Kelvin"])
        from_unit.pack(pady=5)

        to_unit = ctk.CTkOptionMenu(frame, values=list(unit_dict.keys()) if unit_dict else ["Celsius", "Fahrenheit", "Kelvin"])
        to_unit.pack(pady=5)

        result_entry = ctk.CTkEntry(frame, placeholder_text="Result", width=200)
        result_entry.pack(pady=10)

        def convert():
            try:
                value = float(input_entry.get())
                if is_temperature:
                    result = self.convert_temperature(value, from_unit.get(), to_unit.get())
                else:
                    result = value * unit_dict[from_unit.get()] / unit_dict[to_unit.get()]
                result_entry.delete(0, "end")
                result_entry.insert(0, f"{result:.4f}")
            except ValueError:
                result_entry.delete(0, "end")
                result_entry.insert(0, "Invalid Input")
            self.click_sound.play()  # Play sound on convert button click

        ctk.CTkButton(frame, text="Convert", command=convert, width=150).pack(pady=10)

    def convert_temperature(self, value, from_unit, to_unit):
        conversions = {
            ("Celsius", "Fahrenheit"): lambda x: (x * 9/5) + 32,
            ("Celsius", "Kelvin"): lambda x: x + 273.15,
            ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9,
            ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
            ("Kelvin", "Celsius"): lambda x: x - 273.15,
            ("Kelvin", "Fahrenheit"): lambda x: (x - 32) * 9/5 + 273.15
        }
        return value if from_unit == to_unit else conversions[(from_unit, to_unit)](value)

    def setup_converter_tabs(self):
        units = {
            "Area": {
                "Square Meter": 1,
                "Square Kilometer": 1e6,
                "Square Foot": 0.092903,
                "Square Inch": 0.00064516,
                "Acre": 4046.86,
                "Hectare": 10000
            },
            "Weight": {
                "Kilogram": 1,
                "Gram": 0.001,
                "Pound": 0.453592,
                "Ounce": 0.0283495,
                "Tonne": 1000
            },
            "Length": {
                "Meter": 1,
                "Kilometer": 1000,
                "Centimeter": 0.01,
                "Millimeter": 0.001,
                "Mile": 1609.34,
                "Yard": 0.9144,
                "Foot": 0.3048,
                "Inch": 0.0254
            }
        }

        for unit_type, unit_dict in units.items():
            self.create_converter_frame(unit_type, unit_dict)

        self.create_converter_frame("Temperature", is_temperature=True)

    def setup_calculator_tab(self):
        calculator_frame = self.tabview.tab("Calculator")

        # Create a display for the calculator
        self.display = ctk.CTkLabel(calculator_frame, text="", font=("Arial", 24), width=200)
        self.display.pack(pady=10)

        # Create buttons for the calculator
        button_frame = ctk.CTkFrame(calculator_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+",
            "^", "√", "sin", "cos",
            "tan", "log", "exp", "C"
        ]

        row = 0
        col = 0
        for button_text in buttons:
            ctk.CTkButton(button_frame, text=button_text, command=lambda x=button_text: self.on_button_click(x), width=50).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def play_sound(self):
        self.click_sound.play()

    def append_to_display(self, value):
        self.play_sound()  # Play button click sound
        current_text = self.display.cget("text")
        self.display.configure(text=current_text + value)

    def on_button_click(self, value):
        try:
            current_text = self.display.cget("text")
            if value == "=":
                result = self.evaluate_expression(current_text)
                self.display.configure(text=str(result))
            elif value == "C":
                self.display.configure(text="")
            else:
                self.append_to_display(value)
        except Exception as e:
            self.display.configure(text="Error")

    def evaluate_expression(self, expression):
        expression = expression.replace(" ", "")
        if expression.startswith("sin"):
            return math.sin(math.radians(float(expression[3:])))
        elif expression.startswith("cos"):
            return math.cos(math.radians(float(expression[3:])))
        elif expression.startswith("tan"):
            return math.tan(math.radians(float(expression[3:])))
        elif expression.startswith("log"):
            return math.log10(float(expression[3:]))
        elif expression.startswith("exp"):
            return math.exp(float(expression[3:]))
        elif expression.startswith("√"):
            return math.sqrt(float(expression[1:]))
        elif "^" in expression:
            base, exponent = expression.split("^")
            return math.pow(float(base), float(exponent))
        else:
            return eval(expression)

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = UnitConverter()
    app.run()
