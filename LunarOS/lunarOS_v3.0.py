import tkinter as tk
from tkinter import messagebox
import threading
import time
import webbrowser
from datetime import datetime
import random

# ---------------- GUI DESKTOP ----------------
root = tk.Tk()
root.title("LunarOS Desktop")
root.geometry("900x500")
root.configure(bg="#40E0D0")  # turquoise wallpaper

# ---------- APP FUNCTIONS ----------

def open_notepad():
    win = tk.Toplevel(root)
    win.title("Notepad")
    win.geometry("400x300")
    text = tk.Text(win)
    text.pack(expand=True, fill="both")

# Calculator app
def open_calculator():
    win = tk.Toplevel(root)
    win.title("Calculator")
    win.geometry("300x350")

    entry = tk.Entry(win, font=("Arial", 18), justify="right")
    entry.pack(fill="x", padx=10, pady=10)

    def press(key):
        entry.insert("end", key)

    def calculate():
        try:
            # safe-ish eval for simple calculator
            result = eval(entry.get())
            entry.delete(0, "end")
            entry.insert("end", str(result))
        except Exception:
            entry.delete(0, "end")
            entry.insert("end", "Error")

    def clear_all():
        entry.delete(0, "end")

    btn_frame = tk.Frame(win)
    btn_frame.pack()

    buttons = [
        ("7","8","9","/"),
        ("4","5","6","*"),
        ("1","2","3","-"),
        ("0",".","C","+"),
    ]
    for row in buttons:
        rframe = tk.Frame(btn_frame)
        rframe.pack(fill="x")
        for ch in row:
            if ch == "C":
                tk.Button(rframe, text=ch, width=5, command=clear_all).pack(side="left")
            else:
                cmd = (calculate if ch == "=" else (lambda c=ch: press(c)))
                tk.Button(rframe, text=ch, width=5, command=(calculate if ch=="=" else lambda c=ch: press(c))).pack(side="left")
    # equals button
    tk.Button(win, text="=", width=20, command=calculate).pack(pady=8)

# Open Google in default browser
def open_google():
    webbrowser.open("https://www.google.com")

# About
def open_about():
    messagebox.showinfo("About", "LunarOS\nEducational OS shell built in Python")

# ---------- PONG GAME ----------
def open_pong():
    P_W, P_H = 600, 400
    pong = tk.Toplevel(root)
    pong.title("Pong")
    pong.resizable(False, False)
    canvas = tk.Canvas(pong, width=P_W, height=P_H, bg="black")
    canvas.pack()

    # paddles and ball
    pad_w, pad_h = 10, 60
    left_x = 20
    right_x = P_W - 20 - pad_w
    left_y = (P_H - pad_h) / 2
    right_y = (P_H - pad_h) / 2
    left = canvas.create_rectangle(left_x, left_y, left_x+pad_w, left_y+pad_h, fill="white")
    right = canvas.create_rectangle(right_x, right_y, right_x+pad_w, right_y+pad_h, fill="white")
    ball_size = 12
    bx, by = P_W/2, P_H/2
    ball = canvas.create_oval(bx-ball_size/2, by-ball_size/2, bx+ball_size/2, by+ball_size/2, fill="white")
    vx = random.choice((-4,4))
    vy = random.choice((-2,2))
    speed = 20  # ms

    scores = [0,0]
    score_text = canvas.create_text(P_W/2, 20, fill="white", text="0 : 0", font=("Consolas", 20))

    keys = {"w":False, "s":False, "Up":False, "Down":False}

    def key_down(event):
        k = event.keysym
        if k in ("w","s","Up","Down"):
            keys[k] = True

    def key_up(event):
        k = event.keysym
        if k in ("w","s","Up","Down"):
            keys[k] = False

    def update():
        nonlocal vx, vy, bx, by, left_y, right_y
        # paddles movement
        if keys["w"]:
            left_y -= 6
        if keys["s"]:
            left_y += 6
        if keys["Up"]:
            right_y -= 6
        if keys["Down"]:
            right_y += 6
        # clamp
        left_y = max(0, min(P_H-pad_h, left_y))
        right_y = max(0, min(P_H-pad_h, right_y))
        canvas.coords(left, left_x, left_y, left_x+pad_w, left_y+pad_h)
        canvas.coords(right, right_x, right_y, right_x+pad_w, right_y+pad_h)

        # ball move
        bx += vx
        by += vy
        canvas.coords(ball, bx-ball_size/2, by-ball_size/2, bx+ball_size/2, by+ball_size/2)

        # collisions top/bottom
        if by - ball_size/2 <= 0 or by + ball_size/2 >= P_H:
            vy = -vy

        # paddle collisions
        # left paddle
        if bx - ball_size/2 <= left_x + pad_w and left_y <= by <= left_y + pad_h:
            vx = abs(vx) + 0.5
            vx = min(vx, 8)
            # tweak vy for angle
            vy += (by - (left_y + pad_h/2)) / 20
        # right paddle
        if bx + ball_size/2 >= right_x and right_y <= by <= right_y + pad_h:
            vx = -abs(vx) - 0.5
            vx = max(vx, -8)
            vy += (by - (right_y + pad_h/2)) / 20

        # scoring
        if bx < 0:
            scores[1] += 1
            reset_ball()
        if bx > P_W:
            scores[0] += 1
            reset_ball()

        canvas.itemconfigure(score_text, text=f"{scores[0]} : {scores[1]}")

        pong.after(speed, update)

    def reset_ball():
        nonlocal bx, by, vx, vy
        bx, by = P_W/2, P_H/2
        vx = random.choice((-4,4))
        vy = random.choice((-2,2))

    # bind keys
    pong.bind_all("<KeyPress>", key_down)
    pong.bind_all("<KeyRelease>", key_up)

    update()

# ---------- SNAKE GAME ----------
def open_snake():
    S_W, S_H = 400, 400
    snake_win = tk.Toplevel(root)
    snake_win.title("Snake")
    canvas = tk.Canvas(snake_win, width=S_W, height=S_H, bg="black")
    canvas.pack()
    cell = 20
    cols = S_W // cell
    rows = S_H // cell

    # initial snake
    snake = [(cols//2, rows//2), (cols//2-1, rows//2), (cols//2-2, rows//2)]
    direction = (1,0)
    food = None
    running = True
    score = 0
    score_text = canvas.create_text(50, 10, fill="white", text=f"Score: {score}", anchor="nw", font=("Consolas",12))

    def place_food():
        nonlocal food
        while True:
            fx = random.randint(0, cols-1)
            fy = random.randint(0, rows-1)
            if (fx,fy) not in snake:
                food = (fx,fy)
                break

    def draw_cell(x,y,color):
        canvas.create_rectangle(x*cell, y*cell, x*cell+cell, y*cell+cell, fill=color, outline="")

    def draw_all():
        canvas.delete("all")
        # food
        if food:
            draw_cell(food[0], food[1], "red")
        # snake
        for i,(x,y) in enumerate(snake):
            draw_cell(x,y,"#00FF9C" if i==0 else "#00A36A")
        canvas.create_text(10,10, anchor="nw", fill="white", text=f"Score: {score}", font=("Consolas",12))

    def step():
        nonlocal running, direction, score
        if not running:
            return
        head = snake[0]
        nx = (head[0] + direction[0]) % cols
        ny = (head[1] + direction[1]) % rows
        new_head = (nx,ny)
        if new_head in snake:
            # game over
            canvas.create_text(S_W/2, S_H/2, text="GAME OVER", fill="white", font=("Consolas",24))
            running = False
            return
        snake.insert(0, new_head)
        if food and new_head == food:
            score += 1
            place_food()
        else:
            snake.pop()
        draw_all()
        snake_win.after(120, step)

    def on_key(event):
        nonlocal direction
        k = event.keysym
        if k in ("Up","w") and direction != (0,1):
            direction = (0,-1)
        elif k in ("Down","s") and direction != (0,-1):
            direction = (0,1)
        elif k in ("Left","a") and direction != (1,0):
            direction = (-1,0)
        elif k in ("Right","d") and direction != (-1,0):
            direction = (1,0)

    place_food()
    draw_all()
    snake_win.bind_all("<Key>", on_key)
    step()

# ---------- LEFT-SIDE ICONS ----------
icon_style = {
    "bg": "#E0FFFF",
    "activebackground": "#B0E0E6",
    "width": 12,
    "height": 2,
    "relief": "raised"
}

tk.Button(root, text="Notepad", command=open_notepad, **icon_style).place(x=20, y=40)
tk.Button(root, text="Calculator", command=open_calculator, **icon_style).place(x=20, y=100)
tk.Button(root, text="Pong", command=open_pong, **icon_style).place(x=20, y=160)
tk.Button(root, text="Snake", command=open_snake, **icon_style).place(x=20, y=220)
tk.Button(root, text="Google", command=open_google, **icon_style).place(x=20, y=280)
tk.Button(root, text="About", command=open_about, **icon_style).place(x=20, y=340)

# ---------- Wallpaper text ----------
lunar_text = tk.Label(root, text="LunarOS", font=("Segoe UI", 36, "bold"),
                      fg="#2CABA3", bg="#40E0D0")
lunar_text.place(x=600, y=180)

# ---------- Console Shell (runs in background thread) ----------
def terminal_shell():
    print("LunarOS Shell (console). Type 'help' for commands.")
    while True:
        try:
            cmd = input("> ").strip()
        except EOFError:
            break
        if not cmd:
            continue
        if cmd == "help":
            print("help        show commands")
            print("time        show time")
            print("open calc   open calculator")
            print("open pong   open pong")
            print("open snake  open snake")
            print("open google open google in browser")
            print("exit        exit shell (GUI stays)")
        elif cmd == "time":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif cmd == "open calc":
            root.after(0, open_calculator)
        elif cmd == "open pong":
            root.after(0, open_pong)
        elif cmd == "open snake":
            root.after(0, open_snake)
        elif cmd == "open google":
            root.after(0, open_google)
        elif cmd == "exit":
            print("Shell exiting (GUI remains).")
            break
        else:
            print("Unknown command:", cmd)

# start shell in background
threading.Thread(target=terminal_shell, daemon=True).start()

# run the Tkinter GUI in main thread
root.mainloop()
