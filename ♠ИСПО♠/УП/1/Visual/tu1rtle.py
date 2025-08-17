import turtle
import time



def draw_clock():
    # Создание экрана для рисования
    wn = turtle.Screen()
    wn.title("Dynamic Clock")
    wn.bgcolor("black")
    wn.setup(width=500, height=500)
    wn.tracer(0)

    # Создание объектов черепахи для отображения стрелок
    hour_hand = turtle.Turtle()
    hour_hand.shape("arrow")
    hour_hand.speed(1)
    hour_hand.color("white")
    hour_hand.shapesize(stretch_wid=0.4, stretch_len=15)

    minute_hand = turtle.Turtle()
    minute_hand.shape("arrow")
    minute_hand.speed(1)
    minute_hand.color("white")
    minute_hand.shapesize(stretch_wid=0.4, stretch_len=22)

    second_hand = turtle.Turtle()
    second_hand.shape("arrow")
    second_hand.speed(1)
    second_hand.color("red")
    second_hand.shapesize(stretch_wid=0.2, stretch_len=30)

    while True:
        # Получение текущего времени
        import datetime
        now = datetime.datetime.now()

        # Установка угла поворота для стрелок
        hour_angle = (now.hour % 12) * 30 + (now.minute / 60) * 30
        minute_angle = now.minute * 6 + (now.second / 60) * 6
        second_angle = now.second * 6

        # Поворот стрелок на заданный угол
        hour_hand.setheading(-hour_angle)
        minute_hand.setheading(-minute_angle)
        second_hand.setheading(-second_angle)

        # Прорисовка экрана
        wn.update()

        # Задержка перед обновлением времени
        turtle.delay(1000)

if __name__ == "__main__":
    draw_clock()
    
def draw_hand(t, angle, length, width):
    t.penup()
    t.goto(0, 0)
    t.right(angle)
    t.pendown()
    t.pensize(width)
    t.forward(length)

def main():
    # Создаем экземпляр экрана
    wn = turtle.Screen()
    # Задаем фоновый цвет
    wn.bgcolor("black")
    # Задаем заголовок окна
    wn.title("Часы")

    # Вызываем функцию для отрисовки часов
    draw_clock()

    # Закрываем окно по клику
    wn.exitonclick()

# Запускаем программу
if __name__ == '__main__':
    main()
