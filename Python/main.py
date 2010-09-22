# vim:fileencoding=utf8


from Canvas import Canvas
from Actor import Actor
from Wall import Wall
from Vector import Vector

def main():
    canvas = Canvas()

    actors = [
            Actor(0.0, 0.0, 0.5),
            Actor(1.0, 1.0, 0.45)
            ]
    walls = [
            Wall(-2, -2, 2, -2),
            Wall(-2, -2, -2, 2),
            Wall(-2, 2, 2, 2),
            Wall(2, -2, 2, 2)
            ]

    while canvas.tick():
        
        canvas.clear_screen()

        for w in walls:
            canvas.draw_wall(w)

        for a in actors:
            canvas.draw_actor(a)
        
        canvas.update()


if __name__ == "__main__":
    main()
