import ttkbootstrap as ttk
from query_entry import Query
from PIL import Image, ImageTk
import customtkinter as ctk
from submit_handler import respone_genrator


def image_parser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.title("Chat-GPT")
        self.geometry("600x650")
        self.iconbitmap("images/ChatGPT-Logo.ico")
        self.query_var = ttk.StringVar()
        self.y = 0.5
        self.label = ttk.Label(self, text="Query", font=("Helvetica", 15, "normal"))
        self.label.place(relx=0.5, rely=0.43, anchor="center")
        self.query = Query(self, style="success", var=self.query_var, y=self.y)
        self.widget_creator()
        self.mainloop()

    def widget_creator(self):
        def creator(_):
            global sub_btn
            sub_btn = ttk.Button(
                self,
                text="Submit",
                bootstyle="success-outline",
                command=self.animate_widget,
            )
            sub_btn.place(relx=0.5, rely=0.6, anchor="center")
            global clear_btn
            clear_btn = ctk.CTkButton(
                self,
                text="",
                height=18,
                width=18,
                image=image_parser(r"images\close.png", (25, 25)),
                fg_color="#002B36",
                corner_radius=10,
                hover_color="#002B36",
                command=lambda: (self.query_var.set("")),
            )
            clear_btn.place(relx=0.9, rely=0.47)

        self.query.bind("<KeyRelease>", lambda _: creator(_))

    def animate_widget(self):
        sub_btn.place_forget()
        clear_btn.place_forget()


if __name__ == "__main__":
    app = App("solar")
