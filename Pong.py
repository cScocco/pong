# Import required library
import turtle

# ------------ parametri di configurazione ----------------------------

LEFT = 0  # indice per il giocatore di sinistra
RIGHT = 1  # indice per il giocatore di destra
UP = 0
DOWN = 1

SCREEN_TITLE = "Pong game"
SCREEN_BACKGROUND = "white"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_BORDER_X = SCREEN_BORDER_X_LIMIT = SCREEN_WIDTH / 2  # Bordo laterale
SCREEN_BORDER_Y = SCREEN_HEIGHT / 2  # bordo superiore o inferiore
SCREEN_BORDER_Y_LIMIT = SCREEN_BORDER_Y - 20  # impatto pallina con il bordo

PAD_SPEED = 0  # le racchette non hanno velocità. Si muovono solo premendo i tasti
PAD_SHAPE = "square"
PAD_COLOR = "black"
PAD_MOVE = 20  # movimento della racchetta quando si preme il tasto
PAD_X_POSITION = 400  # posizione iniziale delle racchette
PAD_POSITION_LEFT = (-PAD_X_POSITION, 0)
PAD_POSITION_RIGHT = (+PAD_X_POSITION, 0)
PAD_X_HIT_RANGE = [x for x in range(360, 370)]  # zona X di impatto racchetta
PAD_Y_HIT_WING = 50  # zona Y di impatto racchetta

BALL_SPEED = 40  # velocità della pallina
BALL_SHAPE = "circle"
BALL_COLOR = "blue"
BALL_START_X_MOVE = +5  # movimento iniziale lungo X
BALL_START_Y_MOVE = -5  # movimento iniziale lungo X

KEY_PAD = [["", ""], ["", ""]]  # inizializzazione array
KEY_PAD[LEFT][UP] = "e"  # tasti per il movimento delle racchette
KEY_PAD[LEFT][DOWN] = "x"
KEY_PAD[RIGHT][UP] = "Up"
KEY_PAD[RIGHT][DOWN] = "Down"

SCORE_FONT = ("Courier", 24, "normal")
SCORE_COLOR = "blue"
SCORE_POSITION = (0, 260)  # posizione del punteggio sullo schermo


# ------------ classi degli oggetti ----------------------------

# racchette
class Pad(turtle.Turtle):

    def __init__(self, position):
        super().__init__()
        self.speed(PAD_SPEED)
        self.shape(PAD_SHAPE)
        self.color(PAD_COLOR)
        self.shapesize(stretch_wid=6, stretch_len=2)
        self.penup()
        self.setposition(position)

    # properties per evitare di utilizzare xcor(),ycor(),sety()
    @property
    def x(self):
        return self.xcor()

    @property
    def y(self):
        return self.ycor()

    @y.setter
    def y(self, y):
        self.sety(y)

    # movimento racchetta a ogni pressione del tasto
    def move_up(self):
        self.y += PAD_MOVE

    def move_down(self):
        self.y -= PAD_MOVE

    # zona d'impatto in orizzontale
    @property
    def x_hit_range(self):
        if self.x > 0:
            return PAD_X_HIT_RANGE
        else:
            return [-x for x in PAD_X_HIT_RANGE]  # numeri negativi per la racchetta a sinistra

    # zona d'impatto in verticale
    @property
    def y_hit_range(self):
        return [y for y in range(int(self.y) - PAD_Y_HIT_WING,
                                 int(self.y) + PAD_Y_HIT_WING)]

    # zona d'impatto definita come lista di coordinate (x,y)
    @property
    def hit_range(self):
        return [(x, y) for x in self.x_hit_range for y in self.y_hit_range]


# la pallina
class Ball(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.speed(BALL_SPEED)
        self.shape(BALL_SHAPE)
        self.color(BALL_COLOR)
        self.penup()
        self.home()  # home corrisponde all'origine O (0,0)
        self.dx = BALL_START_X_MOVE
        self.dy = BALL_START_Y_MOVE

    # properties per evitare l'uso delle parentesi di xcor(), setx(), ycor(), sety()
    @property
    def x(self):
        return self.xcor()

    @x.setter
    def x(self, x):
        self.setx(x)

    @property
    def y(self):
        return self.ycor()

    @y.setter
    def y(self, y):
        self.sety(y)

    # movimento della pallina ad ogni loop
    def move(self):
        self.x += self.dx
        self.y += self.dy

    # cambio direzione orizzontale
    def change_x_direction(self):
        self.dx *= -1

    # rimbalzo sulla racchetta
    def bounce_on_pad(self):
        self.change_x_direction()

    # rimbalzo sul bordo superiore o inferiore
    def bounce_on_border(self):
        self.dy *= -1  # si inverte il segno di dy

    # impatto sul bordo laterale (sinistro o destro)
    def hits_side_border(self):
        return abs(self.x) > SCREEN_BORDER_X_LIMIT

    # impatto sul bordo destro
    def hits_right_border(self):
        return self.x > SCREEN_BORDER_X_LIMIT

    # impatto sul bordo superiore o inferiore
    def hits_horizontal_border(self):
        return abs(self.y) > SCREEN_BORDER_Y_LIMIT


# il punteggio
class Score(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.points = [0, 0]
        self.left_player = 0
        self.right_player = 0
        self.speed(0)
        self.color(SCORE_COLOR)
        self.penup()
        self.hideturtle()
        self.goto(SCORE_POSITION)
        self.update()

    def update(self):
        self.clear()
        self.write("Left_player : {} Right_player: {}"
                   .format(self.points[LEFT],
                           self.points[RIGHT]),
                   align="center",
                   font=SCORE_FONT)

    def point_to_player(self, player):
        self.points[player] += 1
        self.update()


# ---------- funzioni --------------------------------------

# inizializzazione schermo
def screen_init():
    screen = turtle.Screen()
    screen.title(SCREEN_TITLE)
    screen.bgcolor(SCREEN_BACKGROUND)
    screen.setup(width=SCREEN_WIDTH,
                 height=SCREEN_HEIGHT)
    return screen


# inizializzazione tasti di movimento racchette
def keys_for_pads(screen, pads):
    screen.listen()
    screen.onkeypress(pads[LEFT].move_up, KEY_PAD[LEFT][UP])
    screen.onkeypress(pads[LEFT].move_down, KEY_PAD[LEFT][DOWN])
    screen.onkeypress(pads[RIGHT].move_up, KEY_PAD[RIGHT][UP])
    screen.onkeypress(pads[RIGHT].move_down, KEY_PAD[RIGHT][DOWN])


# ---------- main program  --------------------------------------

def main():
    # inizializzazione
    screen = screen_init()  # creazione schermo

    pads = (Pad(PAD_POSITION_LEFT),  # creazione tupla con le 2 racchette
            Pad(PAD_POSITION_RIGHT))

    keys_for_pads(screen, pads)  # registrazione tasti per movimento racchette

    ball = Ball()  # creazione pallina

    score = Score()  # creazione punteggio

    # ciclo di esecuzione
    while True:

        screen.update()
        ball.move()

        # controllo impatto pallina con bordo superiore o inferiore
        if ball.hits_horizontal_border():
            # rimbalzo sul bordo
            ball.bounce_on_border()

        # controllo impatto con bordo laterale
        if ball.hits_side_border():
            # impatto con bordo destro
            if ball.hits_right_border():
                score.point_to_player(LEFT)
            # impatto con bordo sinistro
            else:
                score.point_to_player(RIGHT)
            # palla al centro
            ball.home()
            # pallina verso il giocatore che ha vinto
            ball.change_x_direction()

        # controllo impatto pallina sulle racchette
        for pad in pads:
            if ball.position() in pad.hit_range:
                # rimbalzo sulla racchetta
                ball.bounce_on_pad()


main()
