import tkinter as tk
from solver import solve

FACE_COLOR = {
    'U': 'white',
    'D': 'yellow',
    'F': 'green',
    'B': 'blue',
    'R': 'red',
    'L': 'orange'
}

NET_POS = {
    'U': (0, 1),
    'L': (1, 0), 'F': (1, 1), 'R': (1, 2), 'B': (1, 3),
    'D': (2, 1)
}

CELL_SIZE = 40
MARGIN = 20
ROW_GAP = CELL_SIZE
LABEL_OFFSET = 20

class Cube2D:
    def __init__(self):
        self.net = {face: [[face for _ in range(3)] for _ in range(3)] for face in NET_POS}

    def rotate_face(self, face, cw=True):
        mat = self.net[face]
        if cw:
            self.net[face] = [list(row) for row in zip(*mat[::-1])]
        else:
            self.net[face] = [list(row) for row in zip(*mat)][::-1]

    def move_U(self, times=1):
        for _ in range(times):
            self.rotate_face('U', cw=True)
            tmp = self.net['F'][0][:]
            self.net['F'][0] = self.net['L'][0][:]
            self.net['L'][0] = self.net['B'][0][:]
            self.net['B'][0] = self.net['R'][0][:]
            self.net['R'][0] = tmp

    def move_R(self, times=1):
        for _ in range(times):
            self.rotate_face('R', cw=True)
            tmp = [self.net['U'][i][2] for i in range(3)]
            for i in range(3): self.net['U'][i][2] = self.net['B'][2-i][0]
            for i in range(3): self.net['B'][i][0] = self.net['D'][2-i][2]
            for i in range(3): self.net['D'][i][2] = self.net['F'][i][2]
            for i in range(3): self.net['F'][i][2] = tmp[i]

    def apply_move(self, move):
        if move.endswith("2"):
            times, face = 2, move[0]
        elif move.endswith("'"):
            times, face = 3, move[0]
        else:
            times, face = 1, move
        if face == 'U': self.move_U(times)
        elif face == 'R': self.move_R(times)

class CubeUI(tk.Tk):
    def __init__(self, scramble):
        super().__init__()
        self.title("2D Rubik's Cube Simulator")
        self.cube = Cube2D()
        for mv in scramble.split():
            self.cube.apply_move(mv)
        self.solution = solve(scramble)
        self.index = 0
        width = MARGIN*2 + CELL_SIZE*3*4
        height = MARGIN*2 + CELL_SIZE*3*3 + ROW_GAP*2 + LABEL_OFFSET
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.bind('<Right>', self.next_move)
        tk.Label(self, text=f"Solution: {' '.join(self.solution)}").pack(pady=5)
        self.draw_net()

    def draw_net(self):
        self.canvas.delete('all')
        for face, (r_off, c_off) in NET_POS.items():
            x_start = MARGIN + c_off * 3 * CELL_SIZE
            y_start = MARGIN + r_off * (3 * CELL_SIZE + ROW_GAP)
            for i in range(3):
                for j in range(3):
                    x0 = x_start + j * CELL_SIZE
                    y0 = y_start + i * CELL_SIZE
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE
                    color = FACE_COLOR[self.cube.net[face][i][j]]
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')
            fx = x_start + 1.5 * CELL_SIZE
            fy = y_start + 3 * CELL_SIZE + LABEL_OFFSET
            self.canvas.create_text(fx, fy, text=face, font=('Arial', 14, 'bold'))

    def next_move(self, event):
        if self.index < len(self.solution):
            mv = self.solution[self.index]
            self.cube.apply_move(mv)
            self.index += 1
            self.draw_net()

if __name__ == '__main__':
    scramble = "R U R' U R U2 R'"
    app = CubeUI(scramble)
    app.mainloop()
