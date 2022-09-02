import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class Snake():
    def __init__(self, size):
        if size > 0:
            self.size = size
            self.x = []
            self.y = []
        else:
            print("Game Over")

class Tabuleiro():
    def __init__(self, width, height):
        if width > 2:
            self.width = width
        else:
            print("Game Over")
        if height > 2:
            self.height = height
        else:
            print("Game Over")
        self.posicoes = np.zeros((self.width, self.height))

    def print_tabuleiro(self):
        plt.figure()
        c = plt.pcolor(self.posicoes, linewidths=4, cmap='RdBu')
        plt.axis('off')
        plt.show()


class Game():
    def __init__(self, size, width, height):
        self.snake = Snake(size)
        self.tabuleiro = Tabuleiro(width, height)
        self.score = 0
    
    def spawn(self, value):
        aux = 1
        while aux != 0:
            x = random.randint(0, self.tabuleiro.width-1)
            y = random.randint(0, self.tabuleiro.height-1)
            aux = self.tabuleiro.posicoes[x][y]
        self.tabuleiro.posicoes[x][y] = value

        return x, y

    def move(self, direction):
        if direction == 'down':
            self.x = self.x + 1
            self.y = self.y
            if self.x >= self.tabuleiro.width:
                self.x = 0
        elif direction == 'up':
            self.x = self.x - 1
            self.y = self.y
            if self.x < 0:
                self.x = self.tabuleiro.width - 1
        elif direction == 'right':
            self.x = self.x
            self.y = self.y + 1
            if self.y >= self.tabuleiro.height:
                self.y = 0
        elif direction == 'left':
            self.x = self.x
            self.y = self.y - 1
            if self.y < 0:
                self.y = self.tabuleiro.height - 1

        self.snake.x.append(self.x)
        self.snake.y.append(self.y)

        if self.tabuleiro.posicoes[self.x][self.y] == 1:
            print('Game Over')
            self.game = 0
            self.tabuleiro.posicoes = np.zeros((self.tabuleiro.width, self.tabuleiro.height))
        elif self.tabuleiro.posicoes[self.x][self.y] == 2:
            self.tabuleiro.posicoes[self.x][self.y] = 1
            self.snake.size += 1
            self.score += 10
            self.x_fruta, self.y_fruta = self.spawn(2)
        else:
            self.tabuleiro.posicoes[self.x][self.y] = 1
            self.tabuleiro.posicoes[self.snake.x[0]][self.snake.y[0]] = 0
            self.snake.x.pop(0)
            self.snake.y.pop(0)

    def start_game(self):
        self.game = 1
        self.x, self.y = self.spawn(1)
        self.snake.x.append(self.x)
        self.snake.y.append(self.y)
        self.x_fruta, self.y_fruta = self.spawn(2)

class GraphBuilder:
    def __init__(self, im, game):
        self.im = im
        self.game = game
        self.cid = im.figure.canvas.mpl_connect('key_press_event', self)

    def __call__(self, event):
        print(self.game.score)
        print('buttom', event.key)
        self.game.move(event.key)
        self.im.set_data(self.game.tabuleiro.posicoes)
        self.im.figure.canvas.draw()

game = Game(1, 5, 5)

game.start_game()

fig, ax = plt.subplots()
ax.set_title('guie a cobra até a fruta')
im = ax.imshow(game.tabuleiro.posicoes)  # empty line
grafico = GraphBuilder(im, game)
plt.show()