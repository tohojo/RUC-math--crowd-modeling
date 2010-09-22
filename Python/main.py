# vim:fileencoding=utf8


from drawing import Canvas
from Actor import Actor
from Wall import Wall
from Vector import Vector

def main():
    canvas = Canvas()

    actors = [
            Actor(0.0, 1.0, 0.25),
            Actor(1.0, 2.0, 0.20),
            Actor(-2.0, -4.0, 0.40),
            ]
    walls = [
            Wall(-5, -5, 5, -5),
            Wall(-5, -5, -5, 5),
            Wall(-5, 5, 5, 5),
            Wall(5, -5, 5, 5),
            Wall(-2, -2, 2, -2),
            Wall(-2, -2, -2, 2),
            Wall(-2, 2, 2, 2),
            Wall(2, -2, 2, 2),
            ]

    while canvas.tick():
        
        canvas.clear_screen()

        for w in walls:
            canvas.draw_wall(w)

        for a in actors:
            a.update_move_vector(walls)
            a.update_pos()
            canvas.draw_actor(a)
        
        canvas.update()


if __name__ == "__main__":
    main()
