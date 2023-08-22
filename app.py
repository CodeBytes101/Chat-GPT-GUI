import ttkbootstrap as ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import threading
import openai
import os


def image_parser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.title("Chat-GPT")
        self.geometry("500x600")
        self.iconbitmap("images/logo.ico")
        self.maxsize(width=500, height=500)
        self.minsize(width=500, height=600)
        self.query_var = ttk.StringVar()
        self.y = 0.5
        self.label = ttk.Label(self, text="Query", font=("Helvetica", 15, "italic"))
        self.label.place(relx=0.5, rely=0.43, anchor="center")
        self.query = ttk.Entry(
            self, bootstyle="success", textvariable=self.query_var, width=32
        )
        self.query.place(relx=0.5, rely=self.y, anchor="center")
        self.widget_creator()
        self.sub_btn = ttk.Button(
            self,
            text="Submit",
            bootstyle="success-outline",
            command=self.submit_handler,
        )
        self.r = 0
        self.load_img = Image.open("images\load.png").resize((200, 200))
        self.animation_label = ctk.CTkLabel(
            self,
            text="",
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
            self, height=325, width=500, font=("Helvetica", 16, "normal")
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
            self.clear_btn.place(relx=0.835, rely=0.47)

        self.query.bind("<KeyRelease>", lambda _: creator(_))

    def submit_handler(self):
        self.sub_btn.place_forget()
        self.clear_btn.place_forget()
        self.label.place_forget()

        def animate():
            threading.Thread(target=self.inserter).start()
            if self.y > 0.11:
                self.y -= 0.0035
                self.query.place(relx=0.5, rely=self.y, anchor="center")
                self.after(1, animate)
            else:
                self.query.configure(state="readonly")
                self.load.place(relx=0.5, rely=0.45, anchor="center")
                self.Animate(r"images\loading")

        animate()

    def img_rotate(self):
        def rotate():
            if self.load:
                self.r -= 1.5
                self.load.configure(
                    image=ImageTk.PhotoImage(self.load_img.rotate(self.r))
                )
                self.after(1, rotate)

        rotate()

    def Animate(self, path):
        self.files_names = []
        for _, _, files in os.walk(path):
            self.files_names = files
        self.N_frames = len(self.files_names)
        self.count = 0

        def animate():
            if self.count == self.N_frames:
                self.count = 0
            self.load.configure(
                image=image_parser(f"{path}\{self.files_names[self.count]}", (200, 200))
            )
            self.count += 1
            self.after(35, animate)

        animate()

    def inserter(self):
        query = str(self.query_var.get())
        result = self.respone_genrator(query)
        self.animation_label.place_forget()
        self.result_box.pack(pady=8, padx=10, expand=True)
        self.result_box.insert("end", result)
        self.reset_btn.place(relx=0.42, rely=0.9, anchor="center")
        self.quit_btn.place(relx=0.55, rely=0.9, anchor="center")

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}]
        )
        return str((dict(((response["choices"])[0])["message"]))["content"])


if __name__ == "__main__":
    app = App("solar")
