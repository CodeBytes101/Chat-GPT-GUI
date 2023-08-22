import ttkbootstrap as ttk
from PIL import Image, ImageTk
import customtkinter as ctk
import threading
import openai
import os

# create a new system variable under the name of OPENAI_API_KEY and store your openai api key
# You can find your openai api key at https://platform.openai.com/account/api-keys


def image_parser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="solar")
        self.title("Chat-GPT")
        self.geometry("500x600")
        self.iconbitmap("images/logo.ico")
        self.maxsize(width=500, height=500)
        self.minsize(width=500, height=600)
        # variables
        self.query_var = ttk.StringVar()
        self.y = 0.5
        self.query_label = ttk.Label(
            self, text="Query", font=("Helvetica", 20, "italic")
        )
        self.query_label.place(relx=0.5, rely=0.38, anchor="center")
        self.query_entry = ttk.Entry(
            self, bootstyle="success", textvariable=self.query_var, width=40
        )
        self.query_entry.place(relx=0.5, rely=self.y, anchor="center")
        self.animation_label = ctk.CTkLabel(self, text="", height=200, width=200)
        self.result_box = ttk.Text(
            self, height=17, width=50, font=("Helvetica", 10, "normal")
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
        self.sub_btn = ttk.Button(
            self,
            text="Search",
            bootstyle="success-outline",
            command=lambda: threading.Thread(target=self.searchHandler).start(),
        )
        self.query_entry.bind("<KeyRelease>", lambda _: self.button_placer(_))

    def button_placer(self, _):
        self.sub_btn.place(relx=0.5, rely=0.65, anchor="center")
        self.clear_btn.place(relx=0.9, rely=0.47)

    def button_remover(self):
        self.sub_btn.place_forget()
        self.clear_btn.place_forget()

    def animateQueryEntry(self):
        if self.y >= 0.15:
            self.y -= 0.04
            self.query_entry.place(relx=0.5, rely=self.y, anchor="center")
            self.after(15, self.animateQueryEntry)

    def Animate(self, path):
        threading.Thread(target=self.inserter).start()
        self.files_names = []
        for _, _, files in os.walk(path):
            self.files_names = files
        self.N_frames = len(self.files_names)
        self.count = 0

        def animate():
            if self.count == self.N_frames:
                self.count = 0
            self.animation_label.configure(
                image=image_parser(f"{path}\{self.files_names[self.count]}", (200, 200))
            )
            self.count += 1
            self.after(35, animate)

        animate()

    def reset(self):
        self.result_box.place_forget()
        self.reset_btn.place_forget()
        self.quit_btn.place_forget()
        self.result_box.delete(1.0, "end")
        self.y = 0.5
        self.query_entry.place(relx=0.5, rely=self.y, anchor="center")
        self.query_var.set("")
        self.query_label.place(relx=0.5, rely=0.38, anchor="center")

    def inserter(self):
        query = str(self.query_var.get())
        result = self.respone_genrator(query)
        self.animation_label.place_forget()
        self.result_box.place(relx=0.5, rely=0.5, anchor="center")
        self.result_box.insert("end", result)
        self.reset_btn.place(relx=0.40, rely=0.9, anchor="center")
        self.quit_btn.place(relx=0.59, rely=0.9, anchor="center")

    def searchHandler(self):
        if self.query_var.get() != "":
            self.query_label.place_forget()
            self.button_remover()
            self.animateQueryEntry()
            self.animation_label.place(relx=0.5, rely=0.5, anchor="center")
            self.Animate(r"images\loading")

    def respone_genrator(self, query: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}]
            )
            return str((dict(((response["choices"])[0])["message"]))["content"])
        except:
            return "Something Went Wrong !!\nMay be Rate Limit Exceed"


if __name__ == "__main__":
    App().mainloop()
