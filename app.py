import ttkbootstrap as ttk
from query_entry import Query
from PIL import Image, ImageTk
import customtkinter as ctk


def image_praser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.title("Chat-GPT")
        self.geometry("600x650")
        self.iconbitmap("images/ChatGPT-Logo.ico")
        self.query_var = ttk.StringVar()
        ttk.Label(self, text="Query", font=("Helvetica", 15, "normal")).place(
            relx=0.5, rely=0.43, anchor="center"
        )
        self.query = Query(self, style="success", var=self.query_var)
        self.widget_creator()
        self.mainloop()

    def widget_creator(self):
        def creator(_):
            ttk.Button(self, text="Submit", bootstyle="success-outline").place(
                relx=0.5, rely=0.6, anchor="center"
            )
            ctk.CTkButton(
                self,
                text="",
                height=16,
                width=16,
                image=image_praser(r"images\close.png", (25, 25)),
                fg_color="#002B36",
                corner_radius=10,
                hover_color="#002B36",
                command=lambda: (self.query_var.set("")),
            ).place(relx=0.885, rely=0.47)

        self.query.bind("<KeyRelease>", lambda _: creator(_))


if __name__ == "__main__":
    app = App("solar")
