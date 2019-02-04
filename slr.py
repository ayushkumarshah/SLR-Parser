from tkinter import Canvas,Label,Frame,Button,Tk,Entry,Toplevel
from graphviz import Digraph

# class LR_zero():
#     def __init__(self,master):
#         self.master=master
#         master.title('LR(0) Generation')
#         master.minsize(500, 500)
#         self.canvas = Canvas(master)



class SLR():
    def __init__(self, master):

        self.master = master
        master.title('SLR Parser')
        master.minsize(500, 500)

        self.canvas = Canvas(master)
        self.canvas.grid(row=0,column=0)

        self.control = Frame(master)
        self.control.grid(row=0,column=1)

#        Button(self.control, text='Generate').grid(row=3, column=0, columnspan=2,pady=5)
        Button(self.control, text='View LR(0) items',command=self.view_lr).grid(row=4, column=0, columnspan=2,pady=5)
        Button(self.control, text='View Parsing Table',command=self.view_parsing).grid(row=5, column=0, columnspan=2,pady=5)
        Button(self.control, text='QUIT',command=master.quit).grid(row=9, column=0, columnspan=2,pady=25)

        self.grammar_can=Canvas(self.canvas, width=200, height=200)
        self.grammar_can.grid(row=0,column=0)

        self.input_can=Canvas(self.canvas, width=200, height=200)
        self.input_can.grid(row=1,column=0)

        Label(self.grammar_can, text="First Name").grid(row=0)
        Label(self.input_can, text="Last Name").grid(row=0)
        e1 = Entry(self.grammar_can)
        e2 = Entry(self.input_can)
        e1.grid(column=0)
        e2.grid(column=0)

    def view_lr(self):
        # LR_zero(self.master)
        self.show = Toplevel(self.master)
        self.show.title("LR(0)")
        self.dot = Digraph(comment='LR(0) Generation')
        i=["A","B","C"]
        I0 = ["S' -> .S", "S -> .L = R", "S -> .R", "R -> .L", "L -> .*R", "L -> id"]
        I1 = [ "R -> .L", "L -> * . R","L -> .* R", "L -> .id"]
        I2 = ["L -> id."]
        I=["I0","I1","I2"]
        self.dot.node("a", I[0])
        self.dot.node("b", I[1])
        self.dot.node("c", I[2])
        self.dot.edges(["a", "b"])
        self.dot.edges(["a", "c"])
        print(self.dot.source)
        self.dot.render('test-output/round-table.gv.pdf', view=True)  # doctest: +SKIP
        display = Label(self.show, text="Generation of LR(0) Grammar")




        display.pack()

    def view_parsing(self):


        self.show = Toplevel(self.master)
        self.show.title("Parsing Table")
        self.show.geometry("%dx%d%+d%+d" % (1300, 1300, 0, 0))
        display = Label(self.show, text="Generation of Parsing Table")
        self.canvas = Canvas(self.show, width=2000,height=1000)
        self.canvas.grid(row=0, column=0)


        states=10
        terminal=3
        nonterminal=3
        row=states+1
        col=terminal+nonterminal+2
        m=10
        n=100

        for i in range(0,row+1):
            for j in range(0,col):
                print(m,n)
                self.canvas.create_rectangle(m, n, m+120, n+30)
                m=m+120
            m=10
            n=n+30

        self.canvas.create_rectangle(10, 70, (terminal+2)*120,  100)
        self.canvas.create_rectangle(((terminal+2)*120), 70, col*120,  100)

        self.canvas.create_text((terminal+2)*60, 83, text="ACTION", font="Times 15 bold")
        self.canvas.create_text(col * 90, 83, text="GOTO", font="Times 15 bold")

        self.show.geometry("%dx%d%+d%+d" % (1300, 800, 0, 0))

        #display.pack()


def main():
    root = Tk()
    gui = SLR(root)
    root.mainloop()

if __name__ == '__main__':
    main()
