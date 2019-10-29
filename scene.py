class Scene:
    """Объект сцены. Хранит в себе канву и ее размеры"""
    def __init__(self, canvas, width, height, floor_height):
        """Конструктор. Требует объект канвы и размеры области, в которой
        происходит движение"""
        self.canvas = canvas
        self.width = width
        self.height = height
        self.floor_height = floor_height

    def is_on_left_border(self, obj):
        """Возвращает True если объект на или за левой границей"""
        return obj.x - obj.r <= 0

    def is_on_right_border(self, obj):
        """Возвращает True если объект на или за правой границей"""
        return obj.x + obj.r >= self.width

    def is_on_floor(self, obj):
        """Возвращает True если объект на или под полом"""
        return self.height - self.floor_height - obj.r <= obj.y

    def place_on_left_border(self, obj):
        """Помещает объект на левую границу"""
        obj.x = obj.r

    def place_on_right_border(self, obj):
        """Помещает объект на правую границу"""
        obj.x = self.width - obj.r

    def place_on_floor(self, obj):
        """Помещает объект на пол"""
        obj.y = self.height - self.floor_height - obj.r
