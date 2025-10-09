import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Hesap Makinesi")
        self.geometry("380x550")
        self.resizable(False, False)

        self.expression = ""

        self.create_widgets()

    def create_widgets(self):
        self.display_frame = ctk.CTkFrame(self, corner_radius=0)
        self.display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.display_frame.grid_columnconfigure(0, weight=1)

        self.display_entry = ctk.CTkEntry(
            self.display_frame,
            font=("Arial", 40),
            textvariable=ctk.StringVar(),
            justify="right",
            border_width=0,
            fg_color="transparent",
            state="readonly"
        )
        self.display_entry.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

        self.buttons_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        buttons = [
            ('C', 1, 0, 'special'), ('%', 1, 1, 'special'), ('/', 1, 2, 'operator'), ('*', 1, 3, 'operator'),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('-', 2, 3, 'operator'),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('+', 3, 3, 'operator'),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('=', 4, 3, 'equals'),
            ('0', 5, 0, None, 2), ('.', 5, 2)
        ]

        for btn_data in buttons:
            text = btn_data[0]
            row = btn_data[1]
            col = btn_data[2]
            btn_type = btn_data[3] if len(btn_data) > 3 else None
            colspan = btn_data[4] if len(btn_data) > 4 else 1
            self.create_button(text, row, col, btn_type, colspan)

    def create_button(self, text, row, col, btn_type=None, colspan=1):
        if btn_type == 'operator':
            fg_color = ("#FF9500", "#FF9500")
            hover_color = ("#D97E00", "#D97E00")
        elif btn_type == 'special':
            fg_color = ("#D4D4D2", "#505050")
            text_color = ("#000000", "#FFFFFF")
            hover_color = ("#BDBDBD", "#686868")
        elif btn_type == 'equals':
             fg_color = ("#FF9500", "#FF9500")
             hover_color = ("#D97E00", "#D97E00")
        else:
            fg_color = ("#E0E0E0", "#333333")
            text_color = ("#000000", "#FFFFFF")
            hover_color = ("#C7C7C7", "#4F4F4F")

        button = ctk.CTkButton(
            self.buttons_frame,
            text=text,
            font=("Arial", 24, "bold"),
            command=lambda t=text: self.on_button_click(t),
            corner_radius=12,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=text_color if 'text_color' in locals() else ("#FFFFFF", "#FFFFFF")
        )
        button.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")
        self.buttons_frame.grid_columnconfigure(col, weight=1)
        self.buttons_frame.grid_rowconfigure(row, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            self.calculate()
            return
        else:
            self.expression += str(char)
        
        self.update_display()

    def calculate(self):
        try:
            result = str(eval(self.expression.replace('%', '/100')))
            self.expression = result
        except ZeroDivisionError:
            self.expression = "Hata: 0'a Bölme"
        except Exception:
            self.expression = "Geçersiz İşlem"

        self.update_display()

    def update_display(self):
        self.display_entry.configure(state="normal")
        self.display_entry.delete(0, 'end')
        self.display_entry.insert(0, self.expression)
        self.display_entry.configure(state="readonly")

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()