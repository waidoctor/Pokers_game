from tkinter import *
import tkinter as tk
import time

from poker import Poker
import random


root = Tk()
random.seed(time.time())
human_change_indices=[]
confirm_enable=True

def add_change_index(event,index):
    "  function response to the right mouse click of b6 to bx,  so position of cards to be changed is stored in the list 'human_change_indices'"
    clear_text_area(T1)
    T1.insert(END, "\n\nPress 'confirm' to change the card(s) you have chosen; or to press 'RESET' to enter your choice again")
    button_dict={0:b6,1:b7,2:b8,3:b9,4:bx}
    human_change_indices.append(index)
    button_dict[index].config(image=imgback)
    button_dict[index].unbind('<Button-1>')   # unbind the button which was pressed so no repeated entry is allowed
    print(index)

def display_cards(hands,b1,b2,b3,b4,b5,img_dict):
    "displaying cards images for both the human side and comp side"
    cards = [x[2] for x in hands]
    b1.config(image=img_dict[cards[0]])
    b2.config(image=img_dict[cards[1]])
    b3.config(image=img_dict[cards[2]])
    b4.config(image=img_dict[cards[3]])
    b5.config(image=img_dict[cards[4]])

def display_rank(ranks,textarea):
    textarea.delete(1.0, END)
    textarea.insert(END, "   "+ranks[0][2:])
def clear_text_area(textarea):
    textarea.delete(1.0, END)
def display_score(c_score,h_score):
    T2.delete(1.0, END)
    T2.insert(END, f"Comp score: {c_score}\n\n\n\nYour score: {h_score}")


def confirm_change_card(event, indices):
    "response to the event of the 'CONFIRM' button, to change the crards being selected by the instance method self.change_cards in Poker class.  "
    global human_change_indices
    human.change_cards( indices)
    display_cards(human.hand, b6, b7, b8, b9, bx, img_dict)
    clear_text_area(Thuman)
    clear_text_area(T1)
    T1.insert(END, "\n\nthis is the computer's turn to change it's hand after calculation, Please wait for a while.\n\n")
    display_rank(human.rank, Thuman)
    human_change_indices = []
    but_confirm.unbind('<Button-1>')
    computer_turn()

def computer_turn():
    "the core function for the computer to perform wise choice of selecting changing cards is computer.comp_choice_to_change() which return the indices to change"
    button_dict = {0: b1, 1: b2, 2: b3, 3: b4, 4: b5}
    indices=computer.comp_choice_to_change()
    T1.insert(END, "computer's changed cards:\t")
    for index in indices:       # img of back of cards are displayed
        button_dict[index].config(image=imgback)
        T1.insert(END, computer.hand[index][2]+"  ")
    computer.change_cards(indices)
    cards = [x[2] for x in computer.hand]
    "step by step displaying the cards is achieved by the widget.after() function with time delay msec"
    b1.after(1000,lambda : b1.config(image=img_dict[cards[0]]))
    b2.after(2000, lambda: b2.config(image=img_dict[cards[1]]))
    b3.after(3000, lambda: b3.config(image=img_dict[cards[2]]))
    b4.after(4000, lambda: b4.config(image=img_dict[cards[3]]))
    b5.after(5000, lambda: b5.config(image=img_dict[cards[4]]))
    T1.after(7500, lambda: T1.delete(1.0, END))
    T1.after(8000,lambda : T1.insert(END, f"""your rank:   {human.rank}\ncomp's rank: {computer.rank} """))
    "Poker's class function Poker.is_higher_rank(1st_arg, 2nd_arg) return True if 1st arg is higher ranked than 2nd arg"
    if Poker.is_higher_rank(computer, human):
        T1.after(8000, lambda: T1.insert(END, "\n\n\t\tComputer win"))
        c_score= int(computer.rank[0][0])
        computer.score+=c_score
    else:
        T1.after(8000, lambda: T1.insert(END, "\n\n\t\tYou win"))
        h_score = int(human.rank[0][0])
        human.score += h_score

    display_score(computer.score,human.score)
    T1.after(8500, lambda: T1.insert(END, "\n\nPress 'CONFIRM' to quit, 'RESET' to restart."))
    clear_text_area(Tcomp)
    display_rank(computer.rank, Tcomp)
    but_confirm.after(8500,lambda : but_confirm.bind('<Button-1>',  quit_game)) #"CONFIRM' bind to quit_game()
    but_reset.after(8500,lambda :  but_reset.bind('<Button-1>', restart_game)) #'RESET' bind to restart_game()

def quit_game(event):
    import sys
    sys.exit()

def restart_game(event):
    "function to restart and reset everything"
    global confirm_enable, human_change_indices
    print("restart")
    b6.bind('<Button-1>', lambda event: add_change_index(event, index=0))
    b7.bind('<Button-1>', lambda event: add_change_index(event, index=1))
    b8.bind('<Button-1>', lambda event: add_change_index(event, index=2))
    b9.bind('<Button-1>', lambda event: add_change_index(event, index=3))
    bx.bind('<Button-1>', lambda event: add_change_index(event, index=4))
    but_reset.bind('<Button-1>', reset_choice)

    but_confirm.bind('<Button-1>', lambda event: confirm_change_card(event, indices=human_change_indices))

    Poker.cards_main = Poker.deck.copy() # new copy of original deck is required for a new game
    Poker.cards_shuffle()
    human_change_indices=[]
    confirm_enable=True
    computer.renew()        # instance method to create players all new attributes
    human.renew()

    display_cards(computer.hand, b1, b2, b3, b4, b5, img_dict)
    display_cards(human.hand, b6, b7, b8, b9, bx, img_dict)
    display_rank(human.rank, Thuman)
    display_rank(computer.rank, Tcomp)
    clear_text_area(T1)
    T1.insert(END, welcome_message)


def reset_choice(event):
    global human_change_indices
    clear_text_area(T1)
    T1.insert(END,"\n\nYour previous choice is remove, you can choose again, and press 'confirm' for final decision")
    human_change_indices=[]
    print("reset choice",human_change_indices)
    display_cards(human.hand, b6, b7, b8, b9, bx, img_dict)
    b6.bind('<Button-1>', lambda event: add_change_index(event, index=0))
    b7.bind('<Button-1>', lambda event: add_change_index(event, index=1))
    b8.bind('<Button-1>', lambda event: add_change_index(event, index=2))
    b9.bind('<Button-1>', lambda event: add_change_index(event, index=3))
    bx.bind('<Button-1>', lambda event: add_change_index(event, index=4))

imgtable = tk.PhotoImage(file="cardimg/paper.png")
root.config(bg='darkgreen')
root.title("Poker game")
root.geometry('1000x670+10+10')
root.resizable(width=False,height=False)

""" here is all the cards image definition"""
img2d = tk.PhotoImage(file="cardimg/2d.png"); img2c = tk.PhotoImage(file="cardimg/2c.png");img2h = tk.PhotoImage(file="cardimg/2h.png");img2s = tk.PhotoImage(file="cardimg/2s.png")
img3d = tk.PhotoImage(file="cardimg/3d.png"); img3c = tk.PhotoImage(file="cardimg/3c.png");img3h = tk.PhotoImage(file="cardimg/3h.png");img3s = tk.PhotoImage(file="cardimg/3s.png")
img4d = tk.PhotoImage(file="cardimg/4d.png"); img4c = tk.PhotoImage(file="cardimg/4c.png");img4h = tk.PhotoImage(file="cardimg/4h.png");img4s = tk.PhotoImage(file="cardimg/4s.png")
img5d = tk.PhotoImage(file="cardimg/5d.png"); img5c = tk.PhotoImage(file="cardimg/5c.png");img5h = tk.PhotoImage(file="cardimg/5h.png");img5s = tk.PhotoImage(file="cardimg/5s.png")
img6d = tk.PhotoImage(file="cardimg/6d.png"); img6c = tk.PhotoImage(file="cardimg/6c.png");img6h = tk.PhotoImage(file="cardimg/6h.png");img6s = tk.PhotoImage(file="cardimg/6s.png")
img7d = tk.PhotoImage(file="cardimg/7d.png"); img7c = tk.PhotoImage(file="cardimg/7c.png");img7h = tk.PhotoImage(file="cardimg/7h.png");img7s = tk.PhotoImage(file="cardimg/7s.png")
img8d = tk.PhotoImage(file="cardimg/8d.png"); img8c = tk.PhotoImage(file="cardimg/8c.png");img8h = tk.PhotoImage(file="cardimg/8h.png");img8s = tk.PhotoImage(file="cardimg/8s.png")
img9d = tk.PhotoImage(file="cardimg/9d.png"); img9c = tk.PhotoImage(file="cardimg/9c.png");img9h = tk.PhotoImage(file="cardimg/9h.png");img9s = tk.PhotoImage(file="cardimg/9s.png")
img10d = tk.PhotoImage(file="cardimg/10d.png"); img10c = tk.PhotoImage(file="cardimg/10c.png");img10h = tk.PhotoImage(file="cardimg/10h.png");img10s = tk.PhotoImage(file="cardimg/10s.png")
imgJd = tk.PhotoImage(file="cardimg/Jd.png"); imgJc = tk.PhotoImage(file="cardimg/Jc.png");imgJh = tk.PhotoImage(file="cardimg/Jh.png");imgJs = tk.PhotoImage(file="cardimg/Js.png")
imgQd = tk.PhotoImage(file="cardimg/Qd.png"); imgQc = tk.PhotoImage(file="cardimg/Qc.png");imgQh = tk.PhotoImage(file="cardimg/Qh.png");imgQs = tk.PhotoImage(file="cardimg/Qs.png")
imgKd = tk.PhotoImage(file="cardimg/Kd.png"); imgKc = tk.PhotoImage(file="cardimg/Kc.png");imgKh = tk.PhotoImage(file="cardimg/Kh.png");imgKs = tk.PhotoImage(file="cardimg/Ks.png")
imgAd = tk.PhotoImage(file="cardimg/Ad.png"); imgAc = tk.PhotoImage(file="cardimg/Ac.png");imgAh = tk.PhotoImage(file="cardimg/Ah.png");imgAs = tk.PhotoImage(file="cardimg/As.png")
imgback = tk.PhotoImage(file="cardimg/back.png")



"""     image dictionary for indexing the correct file name of the images  """
img_dict = {'♦ 2': img2d, '♣ 2': img2c ,'♥ 2': img2h, '♠ 2': img2s,'♦ 3':img3d, '♣ 3':img3c, '♥ 3':img3h, '♠ 3':img3s, '♦ 4':img4d, '♣ 4':img4c, '♥ 4':img4h, '♠ 4':img4s, '♦ 5':img5d, '♣ 5':img5c, '♥ 5':img5h, '♠ 5':img5s,
           '♦ 6':img6d, '♣ 6':img6c, '♥ 6':img6h, '♠ 6':img6s, '♦ 7':img7d, '♣ 7':img7c, '♥ 7':img7h, '♠ 7':img7s, '♦ 8':img8d, '♣ 8':img8c, '♥ 8':img8h, '♠ 8':img8s, '♦ 9':img9d, '♣ 9':img9c, '♥ 9':img9h, '♠ 9':img9s,
           '♦ 10':img10d, '♣ 10':img10c, '♥ 10':img10h, '♠ 10':img10s, '♦ J':imgJd, '♣ J':imgJc, '♥ J':imgJh, '♠ J':imgJs, '♦ Q':imgQd, '♣ Q':imgQc, '♥ Q':imgQh, '♠ Q':imgQs, '♦ K':imgKd, '♣ K':imgKc, '♥ K':imgKh, '♠ K':imgKs,
           '♦ A':imgAd, '♣ A':imgAc, '♥ A':imgAh, '♠ A':imgAs }

frame1 = Frame(root, bg="darkgreen", borderwidth=10, relief=tk.RAISED)
frame1.grid(row=0, column=0, sticky=N, pady=20, columnspan=1, padx=20)

frame2 = Frame(root, bg="green", borderwidth=10, relief=tk.RAISED)
frame2.grid(row=2, column=0, sticky=N, pady=20, columnspan=1, padx=20)

frame3 = Frame(root, bg="red")
frame3.grid(row=1, column=0, sticky=N, pady=0, columnspan=1, padx=20)

frame4 = Frame(root, bg="darkgreen", borderwidth=6, relief=tk.RAISED)
frame4.grid(row=0, column=2, sticky=N, pady=20, columnspan=1, padx=20)

frame5 = Frame(root, bg="green", borderwidth=6, relief=tk.RAISED)
frame5.grid(row=2, column=2, sticky=N, pady=20, columnspan=1, padx=20)

frame6 = Frame(root, bg="green", borderwidth=6, relief=tk.RAISED)
frame6.grid(row=1, column=2, sticky=N, pady=20, columnspan=1, padx=20)

"""b1 to b5 is comp's cards, b6 to bx is human's cards  """
b1 = Button(frame1, text="button1",  bg='yellow', image=imgback,)
b1.grid(row=0, column=0, sticky=S, pady=5, columnspan=1, padx=2)

b2 = Button(frame1, text="button2", bg='yellow', image=imgback)
b2.grid(row=0, column=1, sticky=S, pady=5, columnspan=1, padx=2)

b3 = Button(frame1, text="button3", bg='yellow', image=imgJd)
b3.grid(row=0, column=2, sticky=S, pady=5, columnspan=1, padx=2)

b4 = Button(frame1, text="button4", bg='yellow', image=imgJs)
b4.grid(row=0, column=3, sticky=S, pady=5, columnspan=1, padx=2)

b5 = Button(frame1, text="button5", bg='yellow', image=imgJs)
b5.grid(row=0, column=4, sticky=S, pady=5, columnspan=1, padx=2)

b6 = Button(frame2, text="button6", bg='yellow', image=imgback)
b6.grid(row=0, column=0, sticky=S, pady=5, columnspan=1, padx=2)
b6.bind('<Button-1>', lambda event:add_change_index(event,index= 0))

b7 = Button(frame2, text="button7", bg='yellow', image=imgback)
b7.grid(row=0, column=1, sticky=S, pady=5, columnspan=1, padx=2)
b7.bind('<Button-1>',lambda event:add_change_index(event,index= 1))

b8 = Button(frame2, text="button8", bg='yellow', image=img5c)
b8.grid(row=0, column=2, sticky=S, pady=5, columnspan=1, padx=2)
b8.bind('<Button-1>', lambda event:add_change_index(event,index= 2))

b9 = Button(frame2, text="button9", bg='yellow', image=img6c)
b9.grid(row=0, column=3, sticky=S, pady=5, columnspan=1, padx=2)
b9.bind('<Button-1>', lambda event:add_change_index(event,index= 3))

bx = Button(frame2, text="buttonx", bg='yellow', image=imgAs)
bx.grid(row=0, column=4, sticky=S, pady=5, columnspan=1, padx=2)
bx.bind('<Button-1>', lambda event:add_change_index(event,index= 4))

# T1 is the largest tex tarea in the middle for all the messages display
T1 = Text(frame3, font=('courier', 14), height=8, width=50, bg='brown', wrap=tk.WORD,
         relief=tk.RIDGE, fg='cyan', borderwidth=18)
T1.grid(row=0, column=0, sticky=S, pady=0, columnspan=1, padx=0)
welcome_message = """
\tWelcome to the game of Poker, you are playing the game with computer, computer is the dealer, you and the computer will be given a hand (five cards) in random; you both have one chance to change any numbers of cards you wanted

"""
T1.insert(END, welcome_message)

"""  T2 is the text area to display score       """

T2 = Text(frame6, font=('courier', 16), height=5, width=15, bg='purple', wrap=tk.WORD,
         relief=tk.RIDGE, fg='cyan', pady=15,  padx=15,borderwidth=6)
T2.grid(row=0, column=0, sticky=S, pady=5, columnspan=1, padx=5)


""" Tcomp is the text area to display comp's score """
Tcomp = Text(frame4, font=('courier', 14), height=2, width=15, bg='black', wrap=tk.WORD,
         relief=tk.RIDGE, fg='white', borderwidth=5)
Tcomp.grid(row=0, column=0, sticky=S, pady=0, columnspan=1, padx=0)

""" Thuman is the text area to display human's score"""
Thuman = Text(frame5, font=('courier', 14), height=2, width=15, bg='black', wrap=tk.WORD,
         relief=tk.RIDGE, fg='white', borderwidth=5)
Thuman.grid(row=0, column=0, sticky=S, pady=0, columnspan=1, padx=0)

""" button 'CONFIRM' of two functions 1. to confirm human' cards changes input; 2. to confirm quit of the game"""

but_confirm= Button(frame5, font=('courier', 14),text="  CONFIRM  ",
                    bg='silver',borderwidth=8,relief=tk.RAISED)
but_confirm.grid(row=1, column=0, sticky=S, pady=5, columnspan=1, padx=2)
but_confirm.bind('<Button-1>',lambda event: confirm_change_card(event,indices=human_change_indices))

"""button 'RESET' of two functions 1. to reset human' cards changes, so can redo the choices; 2. to start a new game """

but_reset = Button(frame5, font=('courier', 14),text="   RESET   ",
                   bg='silver',borderwidth=8,relief=tk.RAISED)
but_reset.grid(row=2, column=0, sticky=S, pady=5, columnspan=1, padx=2)
but_reset.bind('<Button-1>',reset_choice)

"""

Here is  the game started , shuffling the deck of cards, instantiate 2 player objects as the type Poker, computer 
and human. Display the ranking and score (initially zero) of human and computer, all the 10 cards randomly chosen 
from the deck 

"""

if __name__ == "__main__":

    Poker.cards_shuffle()
    human = Poker()
    computer = Poker()

    display_rank(human.rank,Thuman)
    display_rank(computer.rank,Tcomp)
    display_cards(computer.hand,b1,b2,b3,b4,b5,img_dict)
    display_cards(human.hand,b6,b7,b8,b9,bx,img_dict)
    display_score(computer.score,human.score)



    root.mainloop()
