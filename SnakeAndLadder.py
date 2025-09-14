import tkinter as tk
import random
from tkinter import messagebox

# Game data
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19,
          64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84,
           36: 44, 51: 67, 71: 91, 80: 100}

positions = {1: 0, 2: 0}
turn = 1

# GUI setup
root = tk.Tk()
root.title("🎲 Snake and Ladder")
root.geometry("600x700")
root.configure(bg="#FFF5F5")

canvas = tk.Canvas(root, width=500, height=500, bg="white", highlightthickness=0)
canvas.pack(pady=20)

info_frame = tk.Frame(root, bg="#FFF5F5")
info_frame.pack()

turn_label = tk.Label(info_frame, text="🎯 Player 1's Turn (Red)", font=("Arial", 14, "bold"), fg="red", bg="#FFF5F5")
turn_label.pack(pady=5)

dice_label = tk.Label(info_frame, text="🎲", font=("Arial", 40), bg="#FFF5F5")
dice_label.pack()

msg_label = tk.Label(info_frame, text="", font=("Arial", 12), bg="#FFF5F5")
msg_label.pack(pady=5)

# Get pixel coordinates for a board position
def get_coordinates(pos):
    if pos == 0:
        return (25, 475)
    pos -= 1
    row = pos // 10
    col = pos % 10 if row % 2 == 0 else 9 - pos % 10
    x = col * 50 + 25
    y = 475 - row * 50 + 25
    return (x, y)

# Draw the board
def draw_board():
    canvas.delete("all")

    for i in range(10):
        for j in range(10):
            num = i * 10 + (j + 1 if i % 2 == 0 else 10 - j)
            x1, y1 = j * 50, 450 - i * 50
            x2, y2 = x1 + 50, y1 + 50
            canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFACD", outline="#999")
            canvas.create_text(x1 + 25, y1 + 25, text=str(num), font=("Arial", 9, "bold"))

    # Draw ladders
    for start, end in ladders.items():
        x1, y1 = get_coordinates(start)
        x2, y2 = get_coordinates(end)
        canvas.create_line(x1, y1, x2, y2, fill="green", width=4, arrow=tk.LAST)
        canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="🪜", font=("Arial", 14))

    # Draw snakes
    for start, end in snakes.items():
        x1, y1 = get_coordinates(start)
        x2, y2 = get_coordinates(end)
        canvas.create_line(x1, y1, x2, y2, fill="red", width=4, arrow=tk.LAST)
        canvas.create_text((x1 + x2)//2, (y1 + y2)//2, text="🐍", font=("Arial", 14))

    # Draw player tokens
    for player, pos in positions.items():
        x, y = get_coordinates(pos)
        offset = -10 if player == 1 else 10
        color = "red" if player == 1 else "blue"
        canvas.create_oval(x-10, y-10+offset, x+10, y+10+offset, fill=color)

# Dice roll function
def roll_dice():
    global turn
    dice = random.randint(1, 6)
    dice_label.config(text=f"🎲 {dice}")

    pos = positions[turn] + dice

    if pos > 100:
        msg_label.config(text=f"Player {turn} must roll exactly to reach 100.")
    else:
        if pos in snakes:
            msg_label.config(text=f"Player {turn} bitten! 🐍 {pos} → {snakes[pos]}")
            pos = snakes[pos]
        elif pos in ladders:
            msg_label.config(text=f"Player {turn} climbed! 🪜 {pos} → {ladders[pos]}")
            pos = ladders[pos]
        else:
            msg_label.config(text=f"Player {turn} moved to {pos}")

        positions[turn] = pos

        if pos == 100:
            draw_board()
            messagebox.showinfo("🎉 Game Over", f"Player {turn} wins!")
            reset_game()
            return

    draw_board()
    turn = 2 if turn == 1 else 1
    next_color = "red" if turn == 1 else "blue"
    turn_label.config(text=f"🎯 Player {turn}'s Turn ({'Red' if turn == 1 else 'Blue'})", fg=next_color)

# Reset function
def reset_game():
    global positions, turn
    positions = {1: 0, 2: 0}
    turn = 1
    dice_label.config(text="🎲")
    msg_label.config(text="Game reset! Player 1 starts.")
    turn_label.config(text="🎯 Player 1's Turn (Red)", fg="red")
    draw_board()

# Control buttons
control_frame = tk.Frame(root, bg="#FFF5F5")
control_frame.pack(pady=10)

tk.Button(control_frame, text="🎲 Roll Dice", command=roll_dice, font=("Arial", 14, "bold"), bg="#B0FFB0").pack(side=tk.LEFT, padx=10)
tk.Button(control_frame, text="🔄 Reset Game", command=reset_game, font=("Arial", 14), bg="#FFB0B0").pack(side=tk.LEFT, padx=10)

draw_board()
root.mainloop()
