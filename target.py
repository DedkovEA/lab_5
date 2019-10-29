import physical_object
from random import randrange as rnd


class Target(physical_object.PhysicalObject):
    """Объект цели"""
    def __init__(self, scene):
        """Конструктор. Требуется передаь объект сцены"""
        super().__init__(0, 0, 0, 0, 0, 1, scene, livedec=0,
                         gravitation_constant=0.2, saving_vel_const=0.95)
        self.id = self.scene.canvas.create_oval(0, 0, 0, 0)
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(self.scene.width - 200, self.scene.width - 20)
        y = self.y = rnd(200, self.scene.height - self.scene.floor_height)
        r = self.r = rnd(2, 50)
        self.vx = rnd(1, 10) - 5
        self.vy = rnd(1, 17)
        self.live = 1
        color = self.color = 'red'
        self.scene.canvas.coords(self.id, x - r, y - r, x + r, y + r)
        self.scene.canvas.itemconfig(self.id, fill=color)

    def hit(self):
        """Вызывать при попадании по цели"""
        self.scene.canvas.coords(self.id, -10, -10, -10, -10)
        self.live = 0

    def move(self):
        """Такт движения цели"""
        if self.live == 1:
            return super().move()

    def redraw(self):
        """Перерисовать объект по текущим координатам"""
        super().redraw()
        self.scene.canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )
        return True
