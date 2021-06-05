import time
import tkinter
from PIL import Image, ImageTk, ImageDraw

global im

class Application(tkinter.Frame):
    def __init__(self, _update, title, master=None, size=(600, 600), buttonNames=(), buttonHandlers=()):
        super().__init__(master)
        self.master = master
        self._update = _update
        self.master.title(title)
        self.size = size
        self.pack()
        self.buttonNames = buttonNames
        self.buttonHandlers = buttonHandlers
        self.create_widgets()
        self.buftime = time.time()# タイマー初期化
        self.timeEvent()

    def create_widgets(self):
        global im

        # 画像の生成
        self.created_image = Image.new('RGB', self.size, 'white')
        self.draw = ImageDraw.Draw(self.created_image)

        # canvas作成
        self.canvas = tkinter.Canvas(self, width=self.created_image.width, height=self.created_image.height)
        self.canvas.grid(row=1, column=0, columnspan=len(self.buttonNames))

        # canvasに画像を表示
        im = ImageTk.PhotoImage(image=self.created_image)
        self.item = self.canvas.create_image(0, 0, anchor='nw', image=im)

        # ボタン作成
        self.buttons = []
        col = 0
        for buttonName in self.buttonNames:
            button = tkinter.Button(self, text = buttonName)
            button.grid(row = 0, column = col)
            button.bind('<Button-1>', self.buttonHandlers[col])
            self.buttons.append(button)
            col += 1

    # タイマー起動用関数
    def timeEvent(self):
        self.update()
        self.after(20, self.timeEvent)# ここで、再帰的に関数を呼び出す

    # スレッド処理実体
    def update(self):
        global im
        self._update(self.draw, self.created_image)
        im = ImageTk.PhotoImage(image=self.created_image)
        self.canvas.itemconfig(self.item,image=im)
