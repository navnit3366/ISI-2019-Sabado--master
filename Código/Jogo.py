import sys
import turtle
import random

CELL_SIZE = 10                  # Measured in pixels

class QuadroVida:
    """Encapsulates a Life board
    Attributes:
    xsize, ysize : horizontal and vertical size of the board
    state : set containing (x,y) coordinates for live cells.
    Methods:
    display(update_board) -- Display the state of the board on-screen.
    erase() -- clear the entire board
    makeRandom() -- fill the board randomly
    set(x,y) -- set the given cell to Live; doesn't refresh the screen
    toggle(x,y) -- change the given cell from live to dead, or vice
                   versa, and refresh the screen display
    """
    def __init__(self, xsize, ysize):
        """Create a new QuadroVida instance.
        scr -- curses screen object to use for display
        char -- character used to render live cells (default: '*')
        """
        self.state = set()
        self.xsize, self.ysize = xsize, ysize

    def ehValido(self, x, y):
        "Returns true if the x,y coordinates are legal for this board."
        return (0 <= x < self.xsize) and (0 <= y < self.ysize)

    def set(self, x, y):
        """Set a cell to the live state."""
        if not self.ehValido(x, y):
            raise ValueError("Coordinates {}, {} out of range 0..{}, 0..{}".format(
                    x, y, self.xsize, self.ysize))
                             
        key = (x, y)
        self.state.add(key)


    def alterar(self, x, y):
        "Alterna o estado das celulas"
        if not self.ehValido(x, y):
            raise ValueError("Coordinates {}, {} out of range 0..{}, 0..{}".format(
                    x, y, self.xsize, self.ysize))
        key = (x, y)
        if key in self.state:
            self.state.remove(key)
        else:
            self.state.add(key)

    def apagar(self):
        "Limpa o quadro"
        self.state.clear()

    def step(self):
        "Passa uma geracao"
        d = set()
        for i in range(self.xsize):
            x_range = range( max(0, i-1), min(self.xsize, i+2) )
            for j in range(self.ysize):
                s = 0
                live = ((i,j) in self.state)
                for yp in range( max(0, j-1), min(self.ysize, j+2) ):
                    for xp in x_range:
                        if (xp, yp) in self.state:
                            s += 1

                s -= live             
                if s == 2:
                    # Nascimento
                    d.add((i,j))
                elif s == 3 and live: 
                    # Sobrevivencia
                    d.add((i,j))
                elif live:
                    # Morte
                    pass

        self.state = d          
    def draw(self, x, y):
        "atualiza a celula (x,y) no display."
        turtle.penup()
        key = (x, y)
        if key in self.state:
            turtle.setpos(x*CELL_SIZE, y*CELL_SIZE)
            turtle.color('black')
            turtle.pendown()
            turtle.setheading(0)
            turtle.begin_fill()
            for i in range(4):
                turtle.forward(CELL_SIZE-1)
                turtle.left(90)
            turtle.end_fill()
            
    def display(self):
        """Desenha o quadro"""
        turtle.clear()
        for i in range(self.xsize):
            for j in range(self.ysize):
                self.draw(i, j)
        turtle.update()


def display_help_window():
    from turtle import TK
    root = TK.Tk()
    frame = TK.Frame()
    canvas = TK.Canvas(root, width=200, height=250, bg="grey")
    canvas.pack()
    help_screen = turtle.TurtleScreen(canvas)
    help_t = turtle.RawTurtle(help_screen)
    help_t.penup()
    help_t.hideturtle()
    help_t.speed('fastest')

    width, height = help_screen.screensize()
    line_height = 20
    y = height // 2 - 30
    for s in ("Clique nas celulas para definir se estao vivas ou mortas",
              "Comandos do teclado:",
              " A)Apaga o quadro",
              " U)Uma geracao",
              " C)Geracao continua",
              " S)Sair"):
        help_t.setpos(-(width / 2), y)
        help_t.write(s, font=('sans-serif', 14, 'normal'))
        y -= line_height
    

def main():
    display_help_window()

    scr = turtle.Screen()
    turtle.mode('standard')
    xsize, ysize = scr.screensize()
    turtle.setworldcoordinates(0, 0, xsize, ysize)

    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.tracer(0, 0)
    turtle.penup()

    board = QuadroVida(xsize // CELL_SIZE, 1 + ysize // CELL_SIZE)

    def alterar(x, y):
        cell_x = x // CELL_SIZE
        cell_y = y // CELL_SIZE
        if board.ehValido(cell_x, cell_y):
            board.alterar(cell_x, cell_y)
            board.display()

    turtle.onscreenclick(turtle.listen)
    turtle.onscreenclick(alterar)

    board.display()

    def apagar():
        board.apagar()
        board.display()
    turtle.onkey(apagar, 'a')

    def aleatorio():
        board.aleatorio()
        board.display()
    turtle.onkey(aleatorio, 'r')

    turtle.onkey(sys.exit, 's')

    continuous = False
    def step_once():
        nonlocal continuous
        continuous = False
        perform_step()

    def step_continuous():
        nonlocal continuous
        continuous = True
        perform_step()

    def perform_step():
        board.step()
        board.display()
        if continuous:
            turtle.ontimer(perform_step, 25)

    turtle.onkey(step_once, 'u')
    turtle.onkey(step_continuous, 'c')

    turtle.listen()
    turtle.mainloop()

if __name__ == '__main__':
    main()
