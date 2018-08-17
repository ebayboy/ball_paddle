from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, color, paddle):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.paddle = paddle
        self.canvas.move(self.id, 245, 100)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3  #向上移动

    def draw(self):
        #移动， 负数代表向上移动， 正数代表向下移动
        self.canvas.move(self.id, self.x, self.y)

        #coords返回椭圆左上和右下坐标
        pos = self.canvas.coords(self.id)

        #左侧边缘检测，小球左上角x左边
        if pos[0] <= 0:
            self.x = 3

        #上侧边缘检测，如果上边缘的y坐标小于等于0， 则向下移动
        if pos[1] <= 0:
            self.y = 3

        #判断小球底部是否碰到球拍
        if self.hit_paddle(pos):
            self.y = -3

        #底面边缘检测，如果小球下边缘的坐标小于等于0， 则向上移动
        if pos[3] >= self.canvas_height:
            self.y = -3
            self.hit_bottom = True

        #右侧边缘检测
        if pos[2] >= self.canvas_width:
            self.x = -3

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0]  and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        #bind left && right
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):

        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0;
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

tk = Tk()
tk.title('Game')
tk.resizable(0,0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, 'red', paddle)

while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
