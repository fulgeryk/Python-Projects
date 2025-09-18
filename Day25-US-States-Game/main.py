import turtle
from us_states import States
screen = turtle.Screen()
states = States()
turtle_for_screen = turtle.Turtle()
screen.title("U.S. State Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle_for_screen.shape(image)
state_ghicitie = []
game_over = False

while not game_over:
    answer_state = screen.textinput(title=f"{len(state_ghicitie)}/{len(states.get_all_states())} States remains ",
                                    prompt="What is the state name ?").title()
    if len(state_ghicitie) == 50:
        game_over = True
    if answer_state == "Exit":
        game_over = True
        lista_state_neghicite = [state for state in states.get_all_states() if state not in state_ghicitie]
        states.remaining_states(lista_state_neghicite)
    if states.existing_state(answer_state):
        if answer_state not in state_ghicitie:
            state_ghicitie.append(answer_state)
            coordonate = states.get_coordinates(answer_state)
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(coordonate)
            turtle.write(f"{answer_state}")

screen.exitonclick()

