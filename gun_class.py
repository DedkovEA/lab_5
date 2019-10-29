import bullet
import math


class Gun:
    """Класс пушки"""
    def __init__(self, scene):
        """Конструктор. Требуется передать объект сцены"""
        self.scene = scene
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.shots = 0
        self.bullets = list()
        self.id = self.scene.canvas.create_line(20, 450, 50, 420, width=7)

    def refresh(self):
        """Обновить пушку"""
        self.bullets = list()
        self.shots = 0

    def remove(self, obj):
        """Убрать пулю из списка активных пуль"""
        return self.bullets.remove(obj)

    def fire2_start(self, event):
        """Начать зарядку. Происходит по ЛКМ"""
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел пулей.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от
        положения мыши.
        """
        self.shots += 1
        new_ball = bullet.Bullet(self.scene)
        new_ball.r += 5
        self.angle = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = - self.f2_power * math.sin(self.angle)
        self.bullets.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            self.scene.canvas.itemconfig(self.id, fill='orange')
        else:
            self.scene.canvas.itemconfig(self.id, fill='black')
        self.scene.canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.angle),
                      450 + max(self.f2_power, 20) * math.sin(self.angle)
                      )

    def power_up(self):
        """Процесс зарядки пушки. Происходит в цикле"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.scene.canvas.itemconfig(self.id, fill='orange')
        else:
            self.scene.canvas.itemconfig(self.id, fill='black')
