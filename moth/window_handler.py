import tkinter


class WindowHandler:
    def __init__(self, width: int, height: int):
        self.master = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.master, bg="white", height=height, width=width)
        self.canvas.create_rectangle((0, 0), (width, height), fill='black')
        self.canvas.pack()

    def new_image(self, coords: dict, size: float, fill: str):
        unit = self.canvas.create_oval((coords['x'] - size / 2, coords['y'] - size / 2),
                                       (coords['x'] + size / 2, coords['y'] + size / 2), fill=fill)
        return self.canvas, unit

    def start(self):
        self.master.mainloop()

    def add_on_timer_tick(self, f, speed: int):
        self.canvas.after(speed, lambda: f(speed))
