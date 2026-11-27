import turtle
import random

# 1. 게임 화면 설정
screen = turtle.Screen()
screen.title('Car Racing Game')
screen.setup(500, 600)
screen.bgcolor('forestgreen')
screen.tracer(0)

# 2. 도로 그리기
road = turtle.Turtle()
road.hideturtle()
road.speed(0)
road.color('dimgray')
road.penup()
road.goto(-150, 300)
road.pendown()
road.begin_fill()
for i in range(2):
    road.forward(300)
    road.right(90)
    road.forward(600)
    road.right(90)
road.end_fill()

# 움직이는 차선 만들기
lines = []
for x in [-50, 50]:
    for y in range(-300, 301, 60):
        line = turtle.Turtle()
        line.shape('square')
        line.color('white')
        line.shapesize(1.5, 0.15)
        line.penup()
        line.goto(x, y)
        lines.append(line)

# 3. 플레이어 자동차
player = turtle.Turtle()
player.shape('square')
player.color('deepskyblue')
player.shapesize(2.5, 1.5)
player.penup()
player.goto(0, -220)

# 4. 장애물 자동차
lanes = [-100, 0, 100]
enemies = []
for i in range(3):
    enemy = turtle.Turtle()
    enemy.shape('square')
    enemy.color(random.choice(['red', 'yellow', 'orange']))
    enemy.shapesize(2.5, 1.5)
    enemy.penup()
    enemy.goto(random.choice(lanes), 300 + i * 220)
    enemies.append(enemy)

# 5. 게임 변수
score = 0
life = 3
level = 1
speed = 5
best_score = 0
boost = 100
boosting = False
state = 'ready'

# 점수 표시용 거북이
pen = turtle.Turtle()
pen.hideturtle()
pen.color('white')
pen.penup()
pen.goto(0, 260)

# 시작 및 종료 메시지용 거북이
message = turtle.Turtle()
message.hideturtle()
message.color('white')
message.penup()

def show_score():
    pen.clear()
    pen.goto(0, 270)
    pen.write(f'Score: {score}   Best: {best_score}   Life: {life}',
              align='center', font=('Arial', 13, 'bold'))
    pen.goto(0, 245)
    pen.write(f'Level: {level}   Boost: {boost}%',
              align='center', font=('Arial', 12, 'normal'))

def show_message(title, subtitle):
    message.clear()
    message.goto(0, 30)
    message.write(title, align='center', font=('Arial', 25, 'bold'))
    message.goto(0, -10)
    message.write(subtitle, align='center', font=('Arial', 13, 'normal'))

# 6. 키보드 조작

def move_left():
    if state == 'playing' and player.xcor() > -100:
        player.setx(player.xcor() - 100)

def move_right():
    if state == 'playing' and player.xcor() < 100:
        player.setx(player.xcor() + 100)

def start_boost():
    global boosting
    if state == 'playing' and boost > 0:
        boosting = True

def stop_boost():
    global boosting
    boosting = False

# 시작 및 재시작: 최고 점수를 제외한 변수 초기화
def start_game():
    global score, life, level, speed, boost, boosting, state
    if state == 'playing':
        return
    score = 0
    life = 3
    level = 1
    speed = 5
    boost = 100
    boosting = False
    player.color('deepskyblue')
    player.goto(0, -220)
    for i in range(len(enemies)):
        enemies[i].goto(random.choice(lanes), 300 + i * 220)
    message.clear()
    state = 'playing'
    show_score()

# 장애물 자동차를 다시 화면 위로 이동

def reset_enemy(enemy):
    highest = 100
    for car in enemies:
        if car != enemy and car.ycor() > highest:
            highest = car.ycor()
    enemy.goto(random.choice(lanes), highest + 220)

# 7. 게임 진행 함수

def game():
    global score, life, level, speed, best_score, boost, boosting, state

    if state == 'playing':
        # 위 방향키를 누르면 부스터 사용
        current_speed = speed
        points = 10
        if boosting and boost > 0:
            current_speed = speed * 2
            boost -= 2
            if boost < 0:
                boost = 0
            player.color('gold')
            points = 20
            if boost == 0:
                boosting = False
        else:
            player.color('deepskyblue')

        # 차선을 아래로 이동시켜 주행 효과 만들기
        for line in lines:
            line.sety(line.ycor() - current_speed)
            if line.ycor() < -330:
                line.sety(line.ycor() + 660)

        # 장애물 자동차 이동 및 충돌 판정
        for enemy in enemies:
            enemy.sety(enemy.ycor() - current_speed)
            if player.xcor() == enemy.xcor() and abs(player.ycor() - enemy.ycor()) < 50:
                life -= 1
                reset_enemy(enemy)
            elif enemy.ycor() < -330:
                score += points
                reset_enemy(enemy)
                # 최고 점수 갱신
                if score > best_score:
                    best_score = score
                # 50점마다 난이도 증가
                level = score // 50 + 1
                speed = min(5 + level - 1, 15)

            if life == 0:
                state = 'over'
                boosting = False
                player.color('deepskyblue')
                show_message('GAME OVER', 'Press SPACE to restart')
                break

        show_score()

    screen.update()
    # 타이머는 항상 하나만 유지
    screen.ontimer(game, 30)

# 8. 키보드 이벤트 등록
screen.listen()
screen.onkeypress(move_left, 'Left')
screen.onkeypress(move_right, 'Right')
screen.onkeypress(start_game, 'space')
screen.onkeypress(start_boost, 'Up')
screen.onkeyrelease(stop_boost, 'Up')

# 9. 시작 화면 및 게임 실행
show_score()
show_message('CAR RACING', 'Press SPACE to start')
message.goto(0, -45)
message.write('LEFT / RIGHT : Move   UP : Boost',
              align='center', font=('Arial', 11, 'normal'))
game()
screen.mainloop()
