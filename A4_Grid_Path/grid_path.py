# -*- coding: utf-8 -*-

import random
import pandas as pd
import numpy as np
from tkinter import *
import tkinter.ttk as ttk

# for command line execution (especially for pyinstaller) 
# import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

def makeplot_withoutline(data): # function to make a plot by matplotlib
    fig, ax = plt.subplots(figsize=(2,2)) # initiate the plot
    ax.axis('off') # set axis off
    the_table =ax.table(cellText=data,cellLoc='center',loc='center',bbox=[0,0,1,1]) # create a table
    the_table[(4, 0)].set_facecolor("#CCCCCC") # set gray color
    the_table[(0, 4)].set_facecolor("#CCCCCC") # set gray color
    the_table.set_fontsize(20) # set font size
    the_table.scale(3, 3)      # set the table size
    the_table.auto_set_font_size(False) # set font size without auto modification
    return fig,ax

class makeGrid: # class for making grids and finding the best path 
    
    def __init__(self):
        
        # create the 5x5 dataframe with random numbers within 0-9
        self.df = pd.DataFrame(np.random.randint(0,10,size=(5, 5)), columns=list('01234'))

        # create the possible direction choice list.
        # In pandas index, [1,0] is equivalent to going up and [0,1] is moving to right.
        self.directions = [[1,0],[1,0],[1,0],[1,0],[0,1],[0,1],[0,1],[0,1]]
        
        # set values to each grids
        self.grid_x0_y0= "S"
        self.grid_x0_y1= self.df.iloc[1,0]
        self.grid_x0_y2= self.df.iloc[2,0]
        self.grid_x0_y3= self.df.iloc[3,0]
        self.grid_x0_y4= self.df.iloc[4,0]
        self.grid_x1_y0= self.df.iloc[0,1]
        self.grid_x1_y1= self.df.iloc[1,1]
        self.grid_x1_y2= self.df.iloc[2,1]
        self.grid_x1_y3= self.df.iloc[3,1]
        self.grid_x1_y4= self.df.iloc[4,1]
        self.grid_x2_y0= self.df.iloc[0,2]
        self.grid_x2_y1= self.df.iloc[1,2]
        self.grid_x2_y2= self.df.iloc[2,2]
        self.grid_x2_y3= self.df.iloc[3,2]
        self.grid_x2_y4= self.df.iloc[4,2]
        self.grid_x3_y0= self.df.iloc[0,3]
        self.grid_x3_y1= self.df.iloc[1,3]
        self.grid_x3_y2= self.df.iloc[2,3]
        self.grid_x3_y3= self.df.iloc[3,3]
        self.grid_x3_y4= self.df.iloc[4,3]
        self.grid_x4_y0= self.df.iloc[0,4]
        self.grid_x4_y1= self.df.iloc[1,4]
        self.grid_x4_y2= self.df.iloc[2,4]
        self.grid_x4_y3= self.df.iloc[3,4]
        self.grid_x4_y4= "G"
        
        # initialize the fields
        self.maxpathvalue = 0
        
        # create a field for the table
        self.data=[[self.grid_x0_y4,self.grid_x1_y4,self.grid_x2_y4,self.grid_x3_y4,self.grid_x4_y4],
              [self.grid_x0_y3,self.grid_x1_y3,self.grid_x2_y3,self.grid_x3_y3,self.grid_x4_y3],
              [self.grid_x0_y2,self.grid_x1_y2,self.grid_x2_y2,self.grid_x3_y2,self.grid_x4_y2],
              [self.grid_x0_y1,self.grid_x1_y1,self.grid_x2_y1,self.grid_x3_y1,self.grid_x4_y1],
              [self.grid_x0_y0,self.grid_x1_y0,self.grid_x2_y0,self.grid_x3_y0,self.grid_x4_y0]]
        
        # call the function which we defined above
        # the function returns fig and ax of matplotlib
        self.fig, self.ax = makeplot_withoutline(self.data)

class PathFinder: # class for first window, to input player name and instruction
    def __init__(self, master):
        self.master = master
        self.UserIn = StringVar()
        
        # Create frame
        self.frame = Frame(master)
        self.frame.grid()
       
        # Label for display message
        self.instruction  = Label(master, text="INSTRUCTION", font =  ('Helvetica', 9, 'bold'))
        self.instruction.grid(row = 5, columnspan = 5)
        text1 = """1. Find the path from S to G on which the sum of the numbers on the visited fields is the highest.\n2. You are only allowed to step upwards and to the right (not down or to the left)\n3. You have 3 attempts to find the best path"""
        self.instruction2  = Message(master, text = text1, font =  ('Helvetica', 10))
        self.instruction2.grid(row = 7, column = 0)
        
        # Button to start playing
        self.button_window = Button(master, text="Play", font =  ('Helvetica', 10, 'bold'))
        self.button_window.grid(columnspan = 5)
        self.button_window.bind("<Button-1>", self.new_window)

    def new_window(self, event):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        start = numberApp(self.newWindow)
        
class numberApp(makeGrid): # class for the main windows
 
    def __init__(self,parent):
        makeGrid.__init__(self) 
        self.parent = parent        
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)  # Generate canvas instance, Embedding fig in root
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, rowspan=3) #canvas._tkcanvas.pack()
        self.parent.update()
        self.parent.deiconify()  
        self.UserIn = StringVar()
        
        #attempt tracker
        self.attempts = 0

        # Create entry for player guess the number
        self.guess_num = Entry(parent, 
                                   textvariable = self.UserIn, 
                                   justify = CENTER, 
                                   width = 5,
                                   bd = 3,
                                   font =  ('Helvetica', 9, 'bold'))
        
        self.guess_num.grid(row=7,column=1)

        # Create message for guess the number
        self.text_guess = Label(parent, text = "Your answer:", 
                                justify = 'left', 
                                font =  ('Helvetica', 9, 'bold'),
                                padx = 2, pady = 2)
        self.text_guess.grid(row=7,column=0)

        # Create message for maximal value
        self.max_path = Label(parent, text = "Maximal value is :"+"", 
                              justify = LEFT, 
                              font =  ('Helvetica', 9, 'bold'),
                              padx = 2, pady = 2)
        self.max_path.grid(row=8,column=0)
        
        # Create button random number
        self.button_random = Button(parent,
                                    padx = 3, pady = 5, bd = 5,
                                    text = 'Play Again',
                                    width = 12,
                                    font =  ('Helvetica', 9, 'bold'))
        self.button_random.bind("<Button-1>", self.randomClick)
        self.button_random.grid(row = 0, column = 2)
        
        
        # Create button for show best path
        self.button_path = Button(parent,
                                  padx = 3, pady = 5, bd = 5,
                                  text = 'Find Best Path',
                                  width = 12,
                                  font =  ('Helvetica', 9, 'bold'))
        self.button_path.bind("<Button-1>", self.pathClick)
        self.button_path.grid(row = 1, column = 2)
        
        # Create button for exit
        self.button_exit = Button(parent,
                                  padx = 3, pady = 5, bd = 5,
                                  text = 'Exit Program',
                                  width = 12,
                                  font =  ('Helvetica', 9, 'bold'))
        self.button_exit.bind("<Button-1>", self.exitClick)
        self.button_exit.grid(row = 2, column = 2)
        
        # Create button check
        self.button_check = Button(parent,
                                    padx = 3, pady = 1, bd = 5,
                                    text = 'Check',
                                    width = 12,
                                    font =  ('Helvetica', 9, 'bold'))
        self.button_check.bind("<Button-1>", self.checkClick)
        self.button_check.grid(row = 7, column = 2)
        
    def randomClick(self,event):
        
        # re-initialize the table numbers
        makeGrid.__init__(self) 
        
        # re-render canvas instance
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)  
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, rowspan=3) 
        self.parent.update()
        self.parent.deiconify()
        
        #resets text fields for new game
        self.max_path.config(text="Maximal value is :"+"", fg="black")
        
        #enables the check button and resets attempts
        self.attempts = 0
        self.button_check.config(state = 'normal')

    def pathClick(self,event): # function to find the best path by simulation
        
        # create an empty dataframe to stack simulation result
        simulation = pd.DataFrame(columns=['directions', 'sum'])
        
        ###########################################
        ###  Alogorithm to find the best path   ###
        ##########################################
        
        #### 1. get all paths                 ####
        #### 2. calculate scores of all paths ####
        #### 3. find the max value and paths  ####
        
        ### 1. get all paths
        # get 70 possible combinations of directions
        # 1000 times random sampling can produce all paths
        # then, remove duplicated paths
        
        temp = [] # paths stacking temporary list
        for i in range(0,1000):
            # randomly choose the order of moving directions
            choice = random.sample(self.directions,8)
            temp.append(choice)
        temp.sort()
        
        # remove the duplicated paths and get 70 paths
        all_path_combinations = list(k for k,_ in itertools.groupby(temp))
        
        
        # calculate all scores of the 70 paths
        for direction_choice in all_path_combinations:
            
            # get the coordinates of the player
            position_1 = direction_choice[0]
            position_2 = [position_1[0] + direction_choice[1][0],
                          position_1[1] + direction_choice[1][1]]
            position_3 = [position_2[0] + direction_choice[2][0],
                          position_2[1] + direction_choice[2][1]]
            position_4 = [position_3[0] + direction_choice[3][0],
                          position_3[1] + direction_choice[3][1]]
            position_5 = [position_4[0] + direction_choice[4][0],
                          position_4[1] + direction_choice[4][1]]
            position_6 = [position_5[0] + direction_choice[5][0],
                          position_5[1] + direction_choice[5][1]]
            position_7 = [position_6[0] + direction_choice[6][0],
                          position_6[1] + direction_choice[6][1]]
            
            # summation of the values where the player went through
            sum_value = self.df.iloc[position_1[0],position_1[1]]+\
                        self.df.iloc[position_2[0],position_2[1]]+\
                        self.df.iloc[position_3[0],position_3[1]]+\
                        self.df.iloc[position_4[0],position_4[1]]+\
                        self.df.iloc[position_5[0],position_5[1]]+\
                        self.df.iloc[position_6[0],position_6[1]]+\
                        self.df.iloc[position_7[0],position_7[1]]
            
            # append the result to the empty dataframe
            simulation = simulation.append({"directions":direction_choice,
                                            "sum":sum_value},
                                           ignore_index = True)
        
        # find the max value and assign it to the corresponding field
        self.maxpathvalue = simulation["sum"].max()
        
        # display the max value 
        self.max_path.config(text=f"Maximal value is : {self.maxpathvalue}", fg="black")
        
        #disable the check button (since solution is displayed)
        self.button_check.config(state = 'disabled')
              
        # get the best path
        self.bestpath_pandas_index = simulation.iloc[pd.to_numeric(simulation["sum"]).idxmax(),0]
        
        # draw lines of the best path
        axis_y = 0.1 # set the first position of y axis
        axis_x = 0.1 # set the first position of x axis
        
        for i,direction in enumerate(self.bestpath_pandas_index): 
            if direction == [0,1]: # right
                axis_x += 0.2 # go right
                self.ax.axhline(y=axis_y, xmin=axis_x-0.2, xmax=axis_x) # draw a horizontal line
            elif direction == [1,0]: # upword
                axis_y += 0.2 # go upword
                self.ax.axvline(x=axis_x, ymin=axis_y-0.2, ymax=axis_y) # draw a vertical line
        
        # re-render canvas instance
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)  # Generate canvas instance, Embedding fig in root
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, columnspan=2, rowspan=3) #canvas._tkcanvas.pack()
        self.parent.update()
        self.parent.deiconify() 

    def exitClick(self,event):
        self.parent.destroy()
        root.quit() #exits root.mainloop()
        
    def checkClick(self,event):
        
        try:
             # get guessed number from input field
            number_guessed = int(self.guess_num.get())
            
            # depending on the guess, display message
            if number_guessed == self.maxpathvalue:
                 self.max_path.config(text="Correct!!", fg = "green")
            else:
                self.attempts += 1
                self.max_path.config(text="Try Again!!", fg = "red")
                self.guess_num.delete(0, END)
                
            #uppon reaching the 3rd attempt, block the check button
            if self.attempts >= 3:
                self.max_path.config(text = "Max attempts reached!", fg = "red")
                self.button_path.config(text = "Show Solution")
                self.button_check.config(state = 'disabled')
                
        except Exception as err:
            #print(err)
            pass
 
root = Tk() 
root.title("Pathfinder")
root.resizable(width=False, height=False)
app = PathFinder(root)
root.mainloop()
