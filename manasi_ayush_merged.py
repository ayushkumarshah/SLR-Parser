from Tkinter import *
from Tkinter import Tk
import Tkinter as tk
import random
import time
import os
from Tkinter import Canvas,Label,Frame,Button,Tk,Entry,Toplevel
from graphviz import Digraph


grammars = open("grammar.txt")
G = {}
C = {}
start = ""
terminals = []
nonterminals = []
symbols = []
error=0

def parse_grammar():
    global G, start, terminals, nonterminals, symbols
    for line in grammars:
        line = " ".join(line.split())
        if line == '\n':
            break
        head = line[:line.index("->")].strip()
        prods = [l.strip().split(' ') for l in ''.join(line[line.index("->") + 2:]).split('|')]
        if not start:
            start = head + "'"
            G[start] = [[head]]
            nonterminals.append(start)
        if head not in G:
            G[head] = []
        if head not in nonterminals:
            nonterminals.append(head)
        for prod in prods:
            G[head].append(prod)
            for char in prod:
                if not char.isupper() and char not in terminals:
                    terminals.append(char)
                elif char.isupper() and char not in nonterminals:
                    nonterminals.append(char)
                    G[char] = []    #non terminals dont produce other symbols
    symbols =  nonterminals+terminals
first_seen = []

def FIRST(X):
    global first_seen
    first = []
    first_seen.append(X)
    if X in terminals:  # CASE 1
        first.append(X)
    elif X in nonterminals:
        for prods in G[X]:  # CASE 2
            if prods[0] in terminals and prods[0] not in first:
                first.append(prods[0])
            else:  # CASE 3
                for nonterm in prods:
                    if nonterm not in first_seen:
                        for terms in FIRST(nonterm):
                            if terms not in first:
                                first.append(terms)
    first_seen.remove(X)
    return first


follow_seen = []
def FOLLOW(A):
    global follow_seen
    follow = []
    follow_seen.append(A)
    if A == start:  # CASE 1
        follow.append('$')
    for heads in G.keys():
        for prods in G[heads]:
            follow_head = False
            if A in prods:
                next_symbol_pos = prods.index(A) + 1
                if next_symbol_pos < len(prods):  # CASE 2
                    for terms in FIRST(prods[next_symbol_pos]):
                        if terms not in follow:
                            follow.append(terms)
                else:  # CASE 3
                    follow_head = True
                if follow_head and heads not in follow_seen:
                    for terms in FOLLOW(heads):
                        if terms not in follow:
                            follow.append(terms)
    follow_seen.remove(A)
    return follow

def closure(I):
    J = I
    while True:
        item_len = len(J) + sum(len(v) for v in J.itervalues())
        for heads in J.keys():
            for prods in J[heads]:
                dot_pos = prods.index('.')      #checks if final item or not
                if dot_pos + 1 < len(prods):
                    prod_after_dot = prods[dot_pos + 1]
                    if prod_after_dot in nonterminals:
                        for prod in G[prod_after_dot]:                   
                            item = ["."] + prod
                            if prod_after_dot not in J.keys():
                                J[prod_after_dot] = [item]
                            elif item not in J[prod_after_dot]:
                                J[prod_after_dot].append(item)
        if item_len == len(J) + sum(len(v) for v in J.itervalues()):
            return J

def GOTO(I, X):
    goto = {}
    for heads in I.keys():
        for prods in I[heads]:
            for i in range(len(prods) - 1):
                if "." == prods[i] and X == prods[i + 1]:
                    temp_prods = prods[:]
                    temp_prods[i], temp_prods[i + 1] = temp_prods[i + 1], temp_prods[i]
                    prod_closure = closure({heads: [temp_prods]})
                    for keys in prod_closure:
                        if keys not in goto.keys():
                            goto[keys] = prod_closure[keys]
                        elif prod_closure[keys] not in goto[keys]:
                            for prod in prod_closure[keys]:
                                goto[keys].append(prod)
    return goto

def items():
    global C
    i = 1
    C = {'I0': closure({start: [['.'] + G[start][0]]})}
    while True:
        item_len = len(C) + sum(len(v) for v in C.itervalues())
        for I in C.keys():
            for X in symbols:
                if GOTO(C[I], X) and GOTO(C[I], X) not in C.values():
                    C['I' + str(i)] = GOTO(C[I], X)
                    i += 1
        if item_len == len(C) + sum(len(v) for v in C.itervalues()):
            return


def ACTION(i, a):
    global error
    for heads in C['I' + str(i)]:
        for prods in C['I' + str(i)][heads]:
            for j in range(len(prods) - 1):
                if prods[j] == '.' and prods[j + 1] == a:
                    for k in range(len(C)):
                        if GOTO(C['I' + str(i)], a) == C['I' + str(k)]:
                            if a in terminals:
                                if "r" in parse_table[i][terminals.index(a)]:
                                    if error!=1:
                                        print "ERROR: Shift-Reduce Conflict at State " + str(i) + ", Symbol \'" + str(terminals.index(a))+"\'"
                                    error=1
                                    if "s"+str(k) not in parse_table[i][terminals.index(a)]:
                                        parse_table[i][terminals.index(a)] = parse_table[i][terminals.index(a)]+ "/s" + str(k)
                                    return parse_table[i][terminals.index(a)]
                                else:
                                    parse_table[i][terminals.index(a)] = "s" + str(k)
                            else:
                                parse_table[i][len(terminals) + nonterminals.index(a)] = str(k)
                            return "s" + str(k)
    for heads in C['I' + str(i)]:
        if heads != start:
            for prods in C['I' + str(i)][heads]:
                if prods[-1] == '.':             #final item 
                    k = 0
                    for head in G.keys():
                        for Gprods in G[head]:
                            if head == heads and (Gprods == prods[:-1] ) and (a in terminals or a == '$'):
                                for terms in FOLLOW(heads):
                                    if terms == '$':
                                        index = len(terminals)
                                    else:
                                        index = terminals.index(terms)
                                    if "s" in parse_table[i][index]:
                                        if error!=1:
                                            print "ERROR: Shift-Reduce Conflict at State " + str(i) + ", Symbol \'" + str(terms)+"\'"
                                        error=1
                                        if "r"+str(k) not in parse_table[i][index]:
                                            parse_table[i][index] = parse_table[i][index]+ "/r" + str(k)
                                        return parse_table[i][index]
                                    elif parse_table[i][index] and parse_table[i][index] != "r" + str(k):
                                        if error!=1:
                                            print "ERROR: Reduce-Reduce Conflict at State " + str(i) + ", Symbol \'" + str(terms)+"\'"
                                        error=1
                                        if "r"+str(k) not in parse_table[i][index]:
                                                parse_table[i][index] = parse_table[i][index]+ "/r" + str(k)
                                        return parse_table[i][index]                                
                                    else:
                                        parse_table[i][index] = "r" + str(k)
                                return "r" + str(k)
                            k += 1
    if start in C['I' + str(i)] and G[start][0] + ['.'] in C['I' + str(i)][start]:
        parse_table[i][len(terminals)] = "acc"
        return "acc"
    return ""

def print_info():
    print "GRAMMAR:"
    for head in G.keys():
        if head == start:
            continue
        print "{:>{width}} ->".format(head, width=len(max(G.keys(), key=len))),
        num_prods = 0
        for prods in G[head]:
            if num_prods > 0:
                print "|",
            for prod in prods:
                print prod,
            num_prods += 1
        print
    print "\nAUGMENTED GRAMMAR:"
    i = 0
    for head in G.keys():
        for prods in G[head]:
            print "{:>{width}}:".format(str(i), width=len(str(sum(len(v) for v in G.itervalues()) - 1))),
            print "{:>{width}} ->".format(head, width=len(max(G.keys(), key=len))),
            for prod in prods:
                print prod,
            print
            i += 1
    print "\nTERMINALS   :", terminals
    print "NONTERMINALS:", nonterminals
    print "SYMBOLS     :", symbols
    print "\nFIRST:"
    for head in G:
        print "{:>{width}} =".format(head, width=len(max(G.keys(), key=len))),
        print "{",
        num_terms = 0
        for terms in FIRST(head):
            if num_terms > 0:
                print ", ",
            print terms,
            num_terms += 1
        print "}"

    print "\nFOLLOW:"
    for head in G:
        print "{:>{width}} =".format(head, width=len(max(G.keys(), key=len))),
        print "{",
        num_terms = 0
        for terms in FOLLOW(head):
            if num_terms > 0:
                print ", ",
            print terms,
            num_terms += 1
        print "}"

    print "\nITEMS:"
    for i in range(len(C)):
        print 'I' + str(i) + ':'
        for keys in C['I' + str(i)]:
            for prods in C['I' + str(i)][keys]:
                print "{:>{width}} ->".format(keys, width=len(max(G.keys(), key=len))),
                for prod in prods:
                    print prod,
                print
        print

    for i in range(len(parse_table)):       #len gives number of states
        for j in symbols:
            ACTION(i, j)

    print "PARSING TABLE:"
    print "+" + "--------+" * (len(terminals) + len(nonterminals) + 1)
    print "|{:^8}|".format('STATE'),
    for terms in terminals:
        print "{:^7}|".format(terms),
    print "{:^7}|".format("$"),
    for nonterms in nonterminals:
        if nonterms == start:
            continue
        print "{:^7}|".format(nonterms),
    print "\n+" + "--------+" * (len(terminals) + len(nonterminals) + 1)
    for i in range(len(parse_table)):
        print "|{:^8}|".format(i),
        for j in range(len(parse_table[i]) - 1):
            print "{:^7}|".format(parse_table[i][j]),
        print
    print "+" + "--------+" * (len(terminals) + len(nonterminals) + 1)

def process_input():
    get_input = raw_input("\nEnter Input: ")
    to_parse = " ".join((get_input + " $").split()).split(" ")
    pointer = 0
    stack = ['0']

    print "\n+--------+----------------------------+----------------------------+----------------------------+"
    print "|{:^8}|{:^28}|{:^28}|{:^28}|".format("STEP", "STACK", "INPUT", "ACTION")
    print "+--------+----------------------------+----------------------------+----------------------------+"

    step = 1
    while True:
        curr_symbol = to_parse[pointer]
        top_stack = int(stack[-1])
        stack_content = ""
        input_content = ""

        print "|{:^8}|".format(step),
        for i in stack:
            stack_content += i
        print "{:27}|".format(stack_content),
        i = pointer
        while i < len(to_parse):
            input_content += to_parse[i]
            i += 1
        print "{:>26} | ".format(input_content),

        step += 1
        get_action = ACTION(top_stack, curr_symbol)
        if "/" in get_action:
            print "{:^26}|".format(get_action+". So conflict")
            break
        if "s" in get_action:
            print "{:^26}|".format(get_action)
            stack.append(curr_symbol)
            stack.append(get_action[1:])
            pointer += 1
        elif "r" in get_action:
            print "{:^26}|".format(get_action)
            i = 0
            for head in G.keys():
                for prods in G[head]:
                    if i == int(get_action[1:]):
                        for j in range(2 * len(prods)):
                            stack.pop()
                        state = stack[-1]
                        stack.append(head)
                        stack.append(parse_table[int(state)][len(terminals) + nonterminals.index(head)])
                    i += 1
        elif get_action == "acc":
            print "{:^26}|".format("ACCEPTED")
            break
        else:
            print "ERROR: Unrecognized symbol", curr_symbol, "|"
            break
    print "+--------+----------------------------+----------------------------+----------------------------+"




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

    
    print parse_table
    # a=[["","s4","s5","","1","2","3"],
    #    ["","","","accept","","",""],
    #    ["s6/r5","","","r5","","",""],
    #    ["","","","r2","","",""],
    #    ["","s4","s5","","","8","7"],
    #    ["r4", "", "", "r4", "", "", ""],
    #    ["", "s4", "s5", "", "", "8", "9"],
    #    ["r3", "", "", "r3", "", "", ""],
    #    ["r5", "", "", "r5"
    #                   "", "", "", ""],
    #    ]

    print terminals
    print nonterminalsr
    states = len(C)
    terminal = len(terminals)
    nonterminal = len(nonterminals)
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

def main():  
    parse_grammar()
    items()
    global parse_table
    parse_table = [["" for c in range(len(terminals) + len(nonterminals) + 1)] for r in range(len(C))]
    print_info()
    # process_input()

    global master
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

if __name__ == '__main__':
       main()

