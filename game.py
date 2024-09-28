from tkinter import *

import random

GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPEED
    elif direction == "down":
        y += SPEED
    elif direction == "left":
        x -= SPEED
    elif direction == "right":
        x += SPEED

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPEED, y + SPEED, fill=SNAKE_COLOR)
    
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        
        score += 1

        label.config(text="Score:{}".format(score))
        
        canvas.delete("food")
        
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)

    # Create game over screen
    game_over_screen = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    game_over_screen.pack()

    # Display final score
    final_score_text = f"Final Score: {score}"
    game_over_screen.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50,font=('consolas', 40), text=final_score_text, fill="white")

    # Display game over message - use fixed coordinates
    game_over_screen.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 20,
                                 font=('consolas', 70), text="GAME OVER", fill="red")

    # Add restart button
    def restart_game():
        game_over_screen.destroy()
        start_game()

    restart_button = Button(window, text="Restart Game", command=restart_game, bg="#00FF00", fg="#000000", font=('consolas', 16))
    restart_button.place(relx=0.5, rely=0.8, anchor=CENTER)


def go_left(event=None):
    change_direction('left')

def go_right(event=None):
    change_direction('right')

def go_up(event=None):
    change_direction('up')

def go_down(event=None):
    change_direction('down')

def start_game():
    global score, direction, snake, food
    
    # Remove existing widgets
    for widget in window.winfo_children():
        widget.destroy()
    
    # Reset game state
    score = 0
    direction = 'down'
    
    # Create canvas
    global canvas
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    # Create snake and food
    snake = Snake()
    food = Food()

    # Create score label
    global label
    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()

    # Start game loop
    next_turn(snake, food)

    # Bind arrow keys
    window.bind('<Left>', go_left)
    window.bind('<Right>', go_right)
    window.bind('<Up>', go_up)
    window.bind('<Down>', go_down)

# Initialize global variables
direction = 'down'

# Create the main window
window = Tk()
window.title("Snake Game")
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
window.configure(bg="#000000")  # Set background color to black

# Create menu frame
menu_frame = Frame(window, bg="#000000", padx=50, pady=50)
menu_frame.pack(expand=True)

# Add button to the menu
start_button = Button(menu_frame, text="Start Game", command=start_game, bg="#00FF00", fg="#000000", font=('consolas', 16), relief=FLAT)
start_button.pack(pady=10)

# Start main loop
window.mainloop()