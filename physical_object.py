class PhysicalObject:
    """Класс физического объекта"""
    def __init__(self, x, y, r, vx, vy, lifetime, scene, livedec=1,
                 gravitation_constant=1, saving_vel_const=0.4):
        """Конструктор. Требует задания скоростей и положения объекта,
        объекта сцены, время жизни.
        Опционально задается декремент времени жизни, ускорение свободного
        падения и доля сохраняющейся скорости"""
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.live = lifetime
        self.livedec = livedec
        self.scene = scene
        self.gravitation_const = gravitation_constant
        self.saving_vel_const = saving_vel_const

    def redraw(self):
        """Перерисовать объект"""
        return True

    def move(self):
        """Просчитать один такт жизни объекта"""
        self.live -= self.livedec
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gravitation_const
        if self.scene.is_on_left_border(self):
            self.vx = self.saving_vel_const * abs(self.vx)
            self.vy *= self.saving_vel_const
            self.scene.place_on_left_border(self)
        elif self.scene.is_on_right_border(self):
            self.vx = -self.saving_vel_const * abs(self.vx)
            self.vy *= self.saving_vel_const
            self.scene.place_on_right_border(self)
        if self.scene.is_on_floor(self):
            self.vy = self.saving_vel_const * abs(self.vy)
            self.vx *= self.saving_vel_const
            self.scene.place_on_floor(self)
        self.redraw()
        if self.live <= 0:
            return self.delete()
        else:
            return False

    def is_interact(self, other):
        """Возвращает True если данный объект пересекается с другим"""
        return (self.x - other.x)**2 + (self.y - other.y)**2 <= \
               (self.r + other.r)**2

    def delete(self):
        """Удаляет объект"""
        return True
