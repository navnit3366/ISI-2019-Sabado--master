import sys
import turtle
import random

TAM_CEL = 10

class QuadroVida:
    def __init__(self, xvert, yvert):
        self.estado = set()
        self.xvert, self.yvert = xvert, yvert

    def ehValido(self,x,y):
        return (0<=x<self.xvert) and (0<=y<self.yvert)

    def setar(self,x,y):
        if not self.ehValido(x,y):
            raise ValueError("Coordenadas {}, {} fora de alcance 0..{}, 0..{}".format( x, y, self.xvert, self.yvert))
        var = (x,y)
        self.estado.add(var)

    def apagar(self):
        self.estado.clear()

    def alterar(self,x,y):
        if not self.ehValido(x,y):
            raise ValueError("Coordenadas {}, {} fora de alcance 0..{}, 0..{}".format(x, y, self.xvert, self.yvert))
        var = (x,y)
        if var in self.estado:
            self.estado.remove(var)
        else:
            self.estado.add(var)

    def passo(self):
        var = set()
        for i in range(self.xvert):
            x_alcance = range(max(0, i-1),  min(self.xvert, i+2))
            for j in range(self.yvert):
                var2=0
                vivo = ((i,j) in self.estado)
                for yv in range(max(0, j-1), min(self.yvert, j+2)):
                    for xv in x_alcance:
                        if (xv, yv) in self.estado:
                            var2+=1
                var2-=vivo
                if var2 == 2:
                    var.add((i,j))
                elif var2 == 3 and vivo:
                    var.add((i,j))
                elif vivo:
                    pass
        self.estado=var
        
    def desenhar(self,x,y):
        turtle.penup()
        var = (x, y)
        if var in self.estado:
            turtle.setpos(x*TAM_CEL, y*TAM_CEL)
            turtle.color('black')
            turtle.pendown()
            turtle.setheading(0)
            turtle.begin_fill()
            for i in range(4):
                turtle.forward(TAM_CEL-1)
                turtle.left(90)
            turtle.end_fill()

    def display(self):
        turtle.clear()
        for i in range(self.xvert):
            for j in range(self.yvert):
                self.desenhar(i, j)
        turtle.update()

def telaAjudaDisplay():
    from turtle import TK
    raiz = TK.Tk()
    frame = TK.Frame()
    quadro = TK.Canvas(raiz, width=200, height=250, bg="grey")
    quadro.pack()
    telaAjuda = turtle.TurtleScreen(quadro)
    ajudaT = turtle.RawTurtle(telaAjuda)
    ajudaT.penup()
    ajudaT.hideturtle()
    ajudaT.speed('fastest')

    largura, altura=telaAjuda.screensize()
    alturaLinha = 20
    y = altura // 2 - 30
    for s in ("Clique nas celulas para definir se estao vivas ou mortas",
              "Comandos do teclado:",
              " A)Apaga o quadro",
              " U)Uma geracao",
              " C)Geracao continua",
              " P)Pausar Geracao Continua",
              " S)Sair"):
        ajudaT.setpos(-(largura / 2), y)
        ajudaT.write(s, font=('sans-serif', 14, 'normal'))
        y -= alturaLinha

def main():
    telaAjudaDisplay()

    tela = turtle.Screen()
    turtle.mode('standard')
    xvert, yvert = tela.screensize()
    turtle.setworldcoordinates(0, 0, xvert, yvert)

    turtle.hideturtle()
    turtle.speed('fastest')
    turtle.tracer(0, 0)
    turtle.penup()

    quadro=QuadroVida(xvert // TAM_CEL, 1 + yvert // TAM_CEL)

    def alterar(x, y):
        cel_x = x // TAM_CEL
        cel_y = y // TAM_CEL
        if quadro.ehValido(cel_x, cel_y):
            quadro.alterar(cel_x, cel_y)
            quadro.display()

    turtle.onscreenclick(turtle.listen)
    turtle.onscreenclick(alterar)

    quadro.display()

    def apagar():
        quadro.apagar()
        quadro.display()
    turtle.onkey(apagar, 'a')

    
    continuo = False
    def proxGeracao():
        quadro.passo()
        quadro.display()
        if continuo:
            turtle.ontimer(proxGeracao, 25)

    def umaGeracao():
        nonlocal continuo
        continuo = False
        proxGeracao()

    def geracaoContinua():
        nonlocal continuo
        continuo = True
        proxGeracao()

    def pausar():
        nonlocal continuo
        continuo = False

    turtle.onkey(umaGeracao, 'u')
    turtle.onkey(geracaoContinua, 'c')
    turtle.onkey(pausar, 'p')

    turtle.listen()
    turtle.mainloop()
if __name__ == '__main__':
    main()                    
