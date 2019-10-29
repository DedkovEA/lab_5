import physical_object, targets
from random import choice


class Bullet(physical_object.PhysicalObject):
    """Класс пули"""
    def __init__(self, scene, x=40, y=450):
        """ Конструктор. Требует передачи объекта сцены
        x - начальное положение пули по горизонтали
        y - начальное положение пули по вертикали
        """
        super().__init__(x, y, 10, 0, 0, 120, scene)
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = self.scene.canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def redraw(self):
        """Перерисовать пулю по текущим координатам"""
        super().redraw()
        self.scene.canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )
        return True

    def move(self):
        """Переместить пулю по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть, обновляет значения self.x и self.y с учетом скоростей
        self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна задан в объекте сцены).
        """
        return super().move()

    def test_hit(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью,
        описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном
            случае возвращает False.
        Кроме того, обновляет цели и очки
        """
        if isinstance(obj, targets.Targets):
            points = 0
            for target in obj.targets:
                if self.is_interact(target) and target.live:
                    target.hit()
                    points += 1
            obj.hit(points)
            return points
        else:
            return False

    def delete(self):
        """Удаляет пулю с экрана и возвращает True при успехе"""
        super().delete()
        self.scene.canvas.delete(self.id)
        return True
