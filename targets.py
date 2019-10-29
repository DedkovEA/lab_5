class Targets:
    """Класс целей"""
    def __init__(self, scene, *args):
        """Конструктор. Параметры - объект сцены и необходимое количество
        объектов целей"""
        self.scene = scene
        self.targets = list(args)
        self.points = 0
        self.id_points = self.scene.canvas.create_text(30, 30,
                                                       text=self.points,
                                                       font='28')

    def add(self, *args):
        """Добавление новой цели"""
        self.targets.append(*args)
        return True

    def alive(self):
        """Возвращает True если осталась хоть одна цель"""
        flag = False
        for t in self.targets:
            if t.live:
                flag = True
        return flag

    def hit(self, points=1):
        """Засчитывает points очков и обновляет счетчик"""
        self.points += points
        self.scene.canvas.itemconfig(self.id_points, text=self.points)

    def renew(self):
        """Обновляет цели"""
        for t in self.targets:
            t.new_target()

    def evolute(self):
        """Просчитывает анимацию целей"""
        for t in self.targets:
            t.move()
