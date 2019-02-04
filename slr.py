from Tkinter import *
from Tkinter import Tk
import Tkinter as tk
import random
import time
import os
from Tkinter import Canvas,Label,Frame,Button,Tk,Entry,Toplevel
from graphviz import Digraph


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)
import Tkinter


def view_lr():
    '''
    # LR_zero(self.master)
    show = Toplevel(master)
    show.title("LR(0)")
    dot = Digraph(comment='LR(0) Generation')
    i = ["A", "B", "C"]
    I0 = ["S' -> .S", "S -> .L = R", "S -> .R", "R -> .L", "L -> .*R", "L -> id"]
    I1 = ["R -> .L", "L -> * . R", "L -> .* R", "L -> .id"]
    I2 = ["L -> id."]
    I = ["I0", "I1", "I2"]
    dot.node("a", I[0])
    dot.node("b", I[1])
    dot.node("c", I[2])
    #dot.edges(["a", "b"])
    #dot.edges(["a", "c"])
    print(dot.source)
    dot.render('test-output/round-table.gv.pdf', view=True)  # doctest: +SKIP
    display = Label(show, text="Generation of LR(0) Grammar")

    #display.pack()

'''
def view_parsing():
    show = Toplevel(master)
    show.title("Parsing Table")
    show.geometry("%dx%d%+d%+d" % (1300, 1300, 0, 0))
    display = Label(show, text="Generation of Parsing Table")
    canvas = Canvas(show, width=2000, height=1000)
    canvas.grid(row=0, column=0)


    a=[["","s4","s5","","1","2","3"],
       ["","","","accept","","",""],
       ["s6/r5","","","r5","","",""],
       ["","","","r2","","",""],
       ["","s4","s5","","","8","7"],
       ["r4", "", "", "r4", "", "", ""],
       ["", "s4", "s5", "", "", "8", "9"],
       ["r3", "", "", "r3", "", "", ""],
       ["r5", "", "", "r5"
                      "", "", "", ""],
       ]


    states = 10
    terminal = 3
    nonterminal = 3
    row = states + 1
    col = terminal + nonterminal + 2
    m = 10
    n = 100

    for i in range(0, row + 1):
        for j in range(0, col):
            print(m, n)
            canvas.create_rectangle(m, n, m + 120, n + 30)
            m = m + 120
        m = 10
        n = n + 30

    canvas.create_rectangle(10, 70, (terminal + 2) * 120, 100)
    canvas.create_rectangle(((terminal + 2) * 120), 70, col * 120, 100)

    canvas.create_text((terminal + 2) * 60, 83, text="ACTION", font="Times 15 bold")
    canvas.create_text(col * 90, 83, text="GOTO", font="Times 15 bold")

    canvas.create_text(65, 110, text="States", font="Times 15 bold")

    show.geometry("%dx%d%+d%+d" % (1300, 800, 0, 0))

    # display.pack()


def view_stack():
    show = Toplevel(master)
    show.title("Stack Implementation")
    show.geometry("%dx%d%+d%+d" % (1300, 1300, 0, 0))
    canvas = Canvas(show, width=2000, height=1000)
    canvas.grid(row=0, column=0)

    states = 10
    terminal = 3
    nonterminal = 3
    row = 10
    col = 4
    m = 10
    n = 100

    for i in range(0, row + 1):
        for j in range(0, col):
            print(m, n)
            canvas.create_rectangle(m, n, m + 120, n + 30)
            m = m + 120
        m = 10
        n = n + 30

    canvas.create_text(65, 110, text="S.N.", font="Times 15 bold")
    canvas.create_text(185, 110, text="Stack", font="Times 15 bold")
    canvas.create_text(305, 110, text="Input", font="Times 15 bold")
    canvas.create_text(415, 110, text="Action", font="Times 15 bold")

    show.geometry("%dx%d%+d%+d" % (1300, 800, 0, 0))

    # display.pack()


master=Tk()



master.title('collision')


canvas=Canvas(master, width=master.winfo_screenwidth(),height=master.winfo_screenheight())


var = IntVar()


table = canvas.create_polygon(50, 100, 600, 100, 600, 310, 50, 310, fill='PaleVioletRed1')
canvas.create_text(150,110, text="Enter the grammar",font="Times 15 bold")

table1 = canvas.create_polygon(50, 350, 600, 350, 600, 500, 50, 500, fill='PaleVioletRed1')
canvas.create_text(150,360, text="Enter input string",font="Times 15 bold")

u1_entry = Entry(canvas)
canvas.create_window(220, 200, window=u1_entry, height=150, width=300)

u2_entry = Entry(canvas)
canvas.create_window(220,430, window=u2_entry, height=100, width=300)




lr0=Button(canvas, text="View LR(0) Items", font="Times 15 bold", command=view_lr())
canvas.create_window(750, 270, window=lr0, height=50, width=170)

pt=Button(canvas, text="View Parsing Table", font="Times 15 bold", command=view_parsing())
canvas.create_window(750, 350, window=pt, height=50, width=170)

vs=Button(canvas, text='View Stack', font="Times 15 bold",command=view_stack)
canvas.create_window(950, 270, window=vs, height=50, width=170)


quit=Button(canvas, text='QUIT', font="Times 15 bold",command=master.quit)
canvas.create_window(950, 350, window=quit, height=50, width=170)



canvas.pack()


mainloop()
