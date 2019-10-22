from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

gravitation_const = 1
saving_vel_const = 0.4

root = tk.Tk()
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)


class Ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 120

    def set_coords(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.live -= 1
        self.x += self.vx
        self.y -= self.vy
        self.vy -= gravitation_const
        if self.x < 0 + self.r:
            self.vx = saving_vel_const * abs(self.vx)
            self.vy *= saving_vel_const
            self.x = 0 + self.r
        elif self.x > 800 - self.r:
            self.vx = -saving_vel_const * abs(self.vx)
            self.vy *= saving_vel_const
            self.x = 800 - self.r
        if self.y > 500 - self.r:
            self.vy = saving_vel_const * abs(self.vy)
            self.vx *= saving_vel_const
            self.y = 500 - self.r
        self.set_coords()
        if self.live <= 0:
            return self.delete()
        else:
            return False

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if isinstance(obj, Targets):
            points = 0
            for target in obj.targets:
                if ((self.x - target.x)**2 + (self.y - target.y)**2 <=
                            (self.r + target.r)**2) and target.live:
                    target.hit()
                    points += 1
            obj.hit(points)
            return points
        else:
            return False

    def delete(self):
        canvas.delete(self.id)
        return True


class Gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canvas.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.an),
                      450 + max(self.f2_power, 20) * math.sin(self.an)
                      )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Targets():
    def __init__(self, *args):
        self.targets = list(args)
        self.points = 0
        self.id_points = canvas.create_text(30, 30, text=self.points, font='28')

    def add(self, *args):
        self.targets.append(*args)
        return True

    def alive(self):
        flag = False
        for target in self.targets:
            if target.live:
                flag = True
        return flag

    def hit(self, points=1):
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)

    def renew(self):
        for target in self.targets:
            target.new_target()


class Target():
    def __init__(self):
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(200, 500)
        r = self.r = rnd(2, 50)
        self.live = 1
        color = self.color = 'red'
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.live = 0


targets = Targets(Target(), Target())
screen_1 = canvas.create_text(400, 300, text='', font='28')
gun_1 = Gun()
bullet = 0
balls = []


def new_game(event=''):
    global Gun, targets, screen_1, balls, bullet
    targets.renew()
    bullet = 0
    balls = []
    canvas.bind('<Button-1>', gun_1.fire2_start)
    canvas.bind('<ButtonRelease-1>', gun_1.fire2_end)
    canvas.bind('<Motion>', gun_1.targetting)

    delay = 0.03
    while targets.alive() or balls:
        for b in balls:
            if b.move():
                balls.remove(b)
            b.hittest(targets)
            if not targets.alive():
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(screen_1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canvas.update()
        time.sleep(delay)
        gun_1.targetting()
        gun_1.power_up()
    canvas.itemconfig(screen_1, text='')
    root.after(750, new_game)


new_game()

root.mainloop()
