import tkinter as tk
from tkinter import ttk
from functools import partial
from tkinter import messagebox
import random

b = []
bClick = []
nCommon = 0
cells = [19, 30]  # построение таблицы: строки * столбцы
nDificult = int(cells[0] * cells[1] / 8)

def IsInRowCol(pars, row, col):
    for el in pars:
        if el[0] == row and el[1] == col:
            return True
    return False

def DefineEmpty(pars, el):
    global bClick
    if IsInRowCol(pars, el[0], el[1]):  # Проверяем, обрабатывали ли этот элемент
        return
    pars.append(el)
    for col in range(el[1] - 1, -1, -1):
        if bClick[el[0]][col]: break
        if DefineCountMines(el[0], col):
            if not IsInRowCol(pars, el[0], col):
                pars.append([el[0], col, -1])
            break
        else:
            if not IsInRowCol(pars, el[0], col):
                pars.append([el[0], col, 0])

    # вправо
    for col in range(el[1] + 1, cells[1]):
        if bClick[el[0]][col]: break
        if DefineCountMines(el[0], col):
            if not IsInRowCol(pars, el[0], col):
                pars.append([el[0], col, -1])
            break
        else:
            if not IsInRowCol(pars, el[0], col):
                pars.append([el[0], col, 0])

    # вверх
    for row in range(el[0] - 1, -1, -1):
        if bClick[row][el[1]]:break
        if DefineCountMines(row, el[1]):
            if not IsInRowCol(pars, row, el[1]):
                pars.append([row, el[1], -1])
            break
        else:
            if not IsInRowCol(pars, row, el[1]):
                pars.append([row, el[1], 0])

    # вниз
    for row in range(el[0] + 1, cells[0]):
        if bClick[row][el[1]]:break
        if DefineCountMines(row, el[1]):
            if not IsInRowCol(pars, row, el[1]):
                pars.append([row, el[1], -1])
            break
        else:
            if not IsInRowCol(pars, row, el[1]):
                pars.append([row, el[1], 0])

    # находим не рассмотренный
    for elem in pars:
        if elem[2] == 0:
            elem[2] = -1
            break
    else:
        return

    DefineEmpty(pars, elem)

def FillEmpty(row, col):
    '''Заполняем пустоты'''
    global b, fields, nCommon, bClick
    queue = [(row, col)]  # Используем очередь для итеративного обхода
    visited = set()  # Храним уже посещённые клетки

    while queue:
        r, c = queue.pop(0)  # Берём элемент из очереди
        if (r, c) in visited:
            continue  # Если уже посещали, пропускаем
        visited.add((r, c))

        # Проверяем, сколько мин вокруг
        k = DefineCountMines(r, c)
        bClick[r][c] = -1
        nCommon += 1
        s = "" if k == 0 else str(k)
        fields[r][c].config(image="", text=s, background="#0A9DF8")

        # Если вокруг нет мин, добавляем соседние клетки в очередь
        if k == 0:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < cells[0] and 0 <= nc < cells[1] and bClick[nr][nc] == 0:
                    queue.append((nr, nc))

def DefineCountMines(row, col):
    global b
    k = 0

    if row == 0:
        if col == 0:
            k += b[row][col+1] + b[row+1][col] + b[row+1][col+1]
        elif col == cells[1] - 1:
            k += b[row][col-1] + b[row+1][col] + b[row+1][col-1]
        else:
            k += (
                b[row][col-1] + b[row][col+1] +
                b[row+1][col-1] + b[row+1][col] + b[row+1][col+1]
            )
    elif row == cells[0] - 1:
        if col == 0:
            k += b[row][col+1] + b[row-1][col] + b[row-1][col+1]
        elif col == cells[1] - 1:
            k += b[row][col-1] + b[row-1][col] + b[row-1][col-1]
        else:
            k += (
                b[row][col-1] + b[row][col+1] +
                b[row-1][col-1] + b[row-1][col] + b[row-1][col+1]
            )
    else:
        if col == 0:
            k += (
                b[row][col+1] + b[row-1][col] + b[row+1][col] +
                b[row-1][col+1] + b[row+1][col+1]
            )
        elif col == cells[1] - 1:
            k += (
                b[row][col-1] + b[row-1][col] + b[row+1][col] +
                b[row-1][col-1] + b[row+1][col-1])
        else:
            k += (
                b[row][col-1] + b[row][col+1] +
                b[row-1][col] + b[row+1][col] +
                b[row-1][col-1] + b[row-1][col+1] +
                b[row+1][col-1] + b[row+1][col+1]
            )
    return k

def DisplayMines():
    '''Показ мин, когда проиграли'''
    global b, fields
    for i in range(len(fields)):
        for j in range(len(fields[i])):
            sColor = str(fields[i][j].cget("background"))
            if b[i][j]:
                if sColor != "red":
                    fields[i][j].config(image=mine_lost)
            else:
                if sColor == "red":
                    k = DefineCountMines(i, j)
                    s = "" if k == 0 else str(k)
                    fields[i][j].config(image="", text=s)

def FormMines(n):
    '''заполняем мины случайным образом'''
    global b, bClick
    z = [(i, j) for i in range(cells[0]) for j in range(cells[1])]
    random.shuffle(z)
    zList = z[:n]
    b.clear()
    bClick.clear()

    for i in range(cells[0]):
        b1 = []
        b2 = []
        for j in range(cells[1]):
            if (i, j) in zList:
                b1.append(1)
            else:
                b1.append(0)
            b2.append(0)
        b.append(b1)
        bClick.append(b2)

    # случайно выбираем пустую
    zBegin = []
    for i in range(cells[0]):
        for j in range(cells[1]):
            if (i, j) not in zList:
                if not DefineCountMines(i, j):
                    zBegin.append((i, j))

    n = random.randrange(0, len(zBegin) - 1)
    left_click(zBegin[n][0], zBegin[n][1])

def clear_mark():
    global fields, nCommon
    nCommon = 0
    for i in range(cells[0]):
        for j in range(cells[1]):
            fields[i][j].config(image="", background="silver", text="")

def left_click(row, col, event=None):
    '''Расстановка мин'''
    global b, fields, mine_logo, nDificult, nCommon, bClick
    if not bClick[row][col]:
        bClick[row][col] = -1
        if b[row][col] == 1:
            fields[row][col].config(image=mine_boom, background="red")
            DisplayMines()
            messagebox.showwarning("САПЁР", "К сожалению Вы проиграли")
            nDificult -= 1
            nDificult = int(max(nDificult, cells[0] * cells[1] / 8))
            countMines.set(str(nDificult))
            clear_mark()
            FormMines(nDificult)
            return
        else:
            nCommon += 1
            k = DefineCountMines(row, col)
            s = "" if k == 0 else str(k)
            fields[row][col].config(image="", text=s, background="#0A9DF8")

            if k == 0:
                FillEmpty(row, col)

            if nCommon == (cells[0] * cells[1] - nDificult):
                messagebox.showinfo("САПЁР", "Вы выиграли")
                nDificult += 1
                nDificult = int(min(nDificult, cells[0] * cells[1] / 2))
                countMines.set(str(nDificult))
                clear_mark()
                FormMines(nDificult)
        return

def right_click(row, col, event):
    global fields, mine_logo
    color = fields[row][col].cget("background")
    if str(color) == "#0A9DF8":
        return
    bClick[row][col] = not bClick[row][col]
    n = int(countMines.get())

    if str(color) == "red":
        fields[row][col].config(image="", background="silver")
        countMines.set(str(n + 1))
    else:
        fields[row][col].config(image=mine_logo, background="red")
        countMines.set(str(n - 1))

root = tk.Tk()
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

mine_logo = tk.PhotoImage(file="gnomemines.png")
mine_lost = tk.PhotoImage(file="blackMine.png")
mine_boom = tk.PhotoImage(file="boom.png")

s = str(36 * cells[1]) + "x" + str(38 * cells[0])
# root.geometry("360x385")

root.resizable(False, False)
root.title("Wрa-cапер")

countMines = tk.StringVar(value=str(nDificult))
fields = []
label = tk.Label(
    text="Кол-во мин : ",
    relief="flat",
    background="white",
    font=("Arial", 12),
    anchor="center"
)
label.grid(row=0, column=0, columnspan=3,)

labelMines = ttk.Label(
    relief="flat",
    background="white",
    font=("Arial", 12, "bold"),
    anchor="center",
    textvariable=countMines
)
labelMines.grid(row=0, column=3, )

for i in range(cells[0]):
    f = []
    for j in range(cells[1]):
        label = ttk.Label(
            width=2,

            relief="sunken",
            background="silver",
            font=("Arial", 21),
            anchor="center"
        )
        label.grid(row=i + 1, column=j, sticky=(tk.W, tk.E))
        label.bind("<Button-1>", partial(left_click, i, j))
        label.bind("<Button-3>", partial(right_click, i, j))
        f.append(label)
    fields.append(f)

FormMines(nDificult)
root.mainloop()