import tkinter as tk
import time
import scene
import targets
import target
import gun_class


class Application:
    """Класс приложения"""
    def __init__(self):
        """Конструктор. Инициализируем необходимые параметры"""
        self.root = tk.Tk()
        self.width = 800
        self.height = 600
        self.floor_height = 100
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.scene = scene.Scene(self.canvas, self.width, self.height,
                                 self.floor_height)
        self.targets = targets.Targets(self.scene, target.Target(self.scene),
                                       target.Target(self.scene))
        self.win_screen = self.canvas.create_text(self.width / 2,
                                                 self.height / 2,
                                                 text='', font='28')
        self.gun = gun_class.Gun(self.scene)

    def new_game(self):
        """Начало нового этапа игры"""
        self.targets.renew()
        self.gun.refresh()
        self.canvas.bind('<Button-1>', self.gun.fire2_start)
        self.canvas.bind('<ButtonRelease-1>', self.gun.fire2_end)
        self.canvas.bind('<Motion>', self.gun.targetting)
        delay = 0.03

        while self.targets.alive() or self.gun.bullets:
            for b in self.gun.bullets:
                if b.move():
                    self.gun.remove(b)
                b.test_hit(self.targets)
                if not self.targets.alive():
                    self.canvas.bind('<Button-1>', '')
                    self.canvas.bind('<ButtonRelease-1>', '')
                    self.canvas.itemconfig(self.win_screen,
                                           text='Вы уничтожили цели за ' +
                                                str(self.gun.shots) +
                                                ' выстрелов')
            self.targets.evolute()
            self.canvas.update()
            time.sleep(delay)
            self.gun.targetting()
            self.gun.power_up()
        self.canvas.itemconfig(self.win_screen, text='')
        self.root.after(750, self.new_game)
        self.root.mainloop()


app = Application()
app.new_game()
