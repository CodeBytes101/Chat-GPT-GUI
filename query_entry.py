import ttkbootstrap as ttk


class Query(ttk.Entry):
    def __init__(self, parent=None, style="default", var=None, y=None):
        super().__init__(master=parent, bootstyle=style, width=50, textvariable=var)
        self.place(relx=0.5, rely=y, anchor="center")
