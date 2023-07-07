import ttkbootstrap as ttk
from PIL import Image, ImageTk
import customtkinter as ctk

import openai


def image_parser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.title("Chat-GPT")
        self.geometry("600x650")
        self.iconbitmap("images/ChatGPT-Logo.ico")
        self.maxsize(width=600, height=650)
        self.minsize(width=600, height=650)
        self.query_var = ttk.StringVar()
        self.y = 0.5
        self.label = ttk.Label(self, text="Query", font=("Helvetica", 15, "italic"))
        self.label.place(relx=0.5, rely=0.43, anchor="center")
        self.query = ttk.Entry(
            self, bootstyle="success", textvariable=self.query_var, width=75
        )
        self.query.place(relx=0.5, rely=self.y, anchor="center")
        self.widget_creator()
        self.sub_btn = ttk.Button(
            self,
            text="Submit",
            bootstyle="success-outline",
            command=lambda: self.animate_widget(),
        )
        self.clear_btn = ctk.CTkButton(
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
        self.result_box = ctk.CTkTextbox(
            self, height=375, width=500, font=("Helvetica", 16, "normal")
        )
        self.reset_btn = ttk.Button(
            self,
            text="Reset",
            command=self.reset,
            bootstyle="success-outline",
        )
        self.quit_btn = ttk.Button(
            self,
            text="Quit",
            bootstyle="danger-outline",
            command=self.destroy,
        )
        self.mainloop()

    def widget_creator(self):
        def creator(_):
            self.sub_btn.place(relx=0.5, rely=0.6, anchor="center")
            self.clear_btn.place(relx=0.775, rely=0.47)

        self.query.bind("<KeyRelease>", lambda _: creator(_))

    def animate_widget(self):
        self.sub_btn.place_forget()
        self.clear_btn.place_forget()
        self.label.place_forget()

        def animate():
            if self.y > 0.15:
                self.y -= 0.0035
                self.query.place(relx=0.5, rely=self.y, anchor="center")
                self.after(1, animate)
            else:
                self.query.configure(state="readonly")
                self.result_box.pack(pady=5, padx=5, expand=True)
                self.inserter()
                self.reset_btn.place(relx=0.5, rely=0.85, anchor="center")
                self.quit_btn.place(relx=0.6, rely=0.85, anchor="center")

        animate()

    def inserter(self):
        query = str(self.query_var.get())
        result = self.respone_genrator(query)
        self.result_box.insert("end", result)

    def reset(self):
        self.result_box.pack_forget()
        self.query.place_forget()
        self.y = 0.5
        self.query.place(relx=0.5, rely=self.y, anchor="center")
        self.query.configure(state="normal")
        self.query_var.set("")
        self.label.place(relx=0.5, rely=0.43, anchor="center")
        self.reset_btn.place_forget()
        self.quit_btn.place_forget()

    def respone_genrator(self, query: str) -> str:
        openai.api_key = open("api.txt", "r").read()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}]
        )
        return str((dict(((response["choices"])[0])["message"]))["content"])


if __name__ == "__main__":
    app = App("solar")
