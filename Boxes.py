# Things to do
# improve detection for line clicking,
# if mouse click not inside box then pick nearest?

# Begin by importing modules required for project

from tkinter import *
from tkinter import messagebox

# Define arrays for holding the game objects and state data
GridState = []
GridSetState = []
HLines = []
VLines = []
HLinesSet = []
VLinesSet = []

# Define the size of the game grid
GridSizeX = 6
GridSizeY = 6

# Define game grid offsets and spacing
Xoffs = 10
Yoffs = 10
GridSpacing = 40

# Define player variables
TurnCount = [0]
TurnTracker = [0]
Player1ScoreVal = [0]
Player2ScoreVal = [0]

def GetPosByXY(x,y,xs):
    # Takes an x and y lookup and returns the 1D array index
    return x + (y * xs)

    
def create_circle(x,y,r,Canvas,Binding):
    # center coordinates, radius
    x0 = x-r
    y0 = y-r
    x1 = x+r
    y1 = y+r
    return Canvas.create_oval(x0,y0,x1,y1,fill="black", tags=Binding)

def GetLineInstance(x,y,Ref):
    # Returns the calculated line instance number using the x/y coordinates of
    # The mouse pointer as a reference point
    
    for Lines in range(len(Ref)):
        tar = []
        tar = w.coords(Ref[Lines])
        X0 = tar[0]
        Y0 = tar[1]
        X1 = tar[2]
        Y1 = tar[3]
        if x > X0:
            if x < X1:
                if y >= Y0:
                    if y <= Y1:
                        return Lines
        

def onObjectClickH(event):
    Index = GetLineInstance(event.x,event.y,HLines)
    if Index is not None:
        if HLinesSet[Index] == 0:
            w.itemconfig(HLines[Index],fill="black")
            HLinesSet[Index] = 1
            CheckPlayerTurn()

def onObjectClickV(event):
    Index = GetLineInstance(event.x,event.y,VLines)
    if Index is not None:
        if VLinesSet[Index] == 0:
            w.itemconfig(VLines[Index],fill="black")
            VLinesSet[Index] = 1
            CheckPlayerTurn()

def CheckPlayerTurn():
    TurnCount[0] = TurnCount[0] + 1

    if CheckBoxClosed() == 0:
        if TurnTracker[0] == 0:
            TurnTracker[0] = 1
        else:
            TurnTracker[0] = 0

    UpdatePlayerScores()
    UpdateGameState()
    if CheckEndOfGame() == 1:
        messagebox.showinfo("Game Over",DetermineWinner())
        ResetGame()

def ResetGame():
    # clears all game variables and prepares for a restart

    # Reset score and count variables
    Player1ScoreVal[0] = 0
    Player2ScoreVal[0] = 0
    TurnCount[0] = 0
    
    # Reset all grid markers and states to 0 or " "
    for itm in range(len(GridSetState)):
        GridSetState[itm] = 0
    for itm in GridState:
        w.itemconfig(itm,text=" ")
    for itm in HLines:
        w.itemconfig(itm,fill="white")
    for itm in VLines:
        w.itemconfig(itm,fill="white")
    for itm in range(len(HLinesSet)):
        HLinesSet[itm] = 0
    for itm in range(len(VLinesSet)):
        VLinesSet[itm] = 0

    UpdateGameState()
        

def DetermineWinner():
    if Player1ScoreVal[0] > Player2ScoreVal[0]:
        return "Player 1 is the winner!"
    if Player1ScoreVal[0] < Player2ScoreVal[0]:
        return "Player 2 is the winner!"

def CheckBoxClosed():      
    # looks for closed boxes with empty text and changes the text to the
    # current player number and updates their score value
    ABoxFilled = 0
    for X in range(GridSizeX-1):
        for Y in range(GridSizeY-1):
            if GridSetState[GetPosByXY(X,Y,GridSizeX-1)] == 0:
                TopLineIndex = X + (Y * (GridSizeX-1))
                BottomLineIndex = X + (Y * (GridSizeX-1)) + (GridSizeX-1)
                LeftLineIndex = X + (Y * GridSizeX)
                RightLineIndex = LeftLineIndex + 1
                if HLinesSet[TopLineIndex] == 1:
                    if HLinesSet[BottomLineIndex] == 1:
                        if VLinesSet[LeftLineIndex] == 1:
                            if VLinesSet[RightLineIndex] == 1:
                                GridSetState[GetPosByXY(X,Y,GridSizeX-1)] = TurnTracker[0] + 1
                                w.itemconfig(GridState[GetPosByXY(X,Y,GridSizeX-1)],text=str(TurnTracker[0]+1))
                                ABoxFilled = 1
    if ABoxFilled == 0:
        return 0
    else:
        return 1


def UpdateGameState():
    w.itemconfig(Player1Text,text="Player 1 score - " + str(Player1ScoreVal[0]))
    w.itemconfig(Player2Text,text="Player 2 score - " + str(Player2ScoreVal[0]))
    w.itemconfig(TurnCounter,text="Number of turns - " + str(TurnCount[0]))
    if TurnTracker[0] == 0:
        w.itemconfig(PlayerTurnDisplay,text="It is Player 1's turn")
    else:
        w.itemconfig(PlayerTurnDisplay,text="It is Player 2's turn")


def UpdatePlayerScores():
    # cycles through the elements of the GridSetState, counts the
    # player scores and updates the score variables
    P1TempScore = 0
    P2TempScore = 0
    for Count in range(len(GridSetState)):
        if GridSetState[Count] == 1:
            P1TempScore = P1TempScore + 1
        if GridSetState[Count] == 2:
            P2TempScore = P2TempScore + 1
    Player1ScoreVal[0] = P1TempScore
    Player2ScoreVal[0] = P2TempScore

def CheckEndOfGame():
    # Check if the game is over i.e all boxes are filled
    EndOfGame = 1
    for Count in range(len(GridSetState)):
        if GridSetState[Count] == 0:
            EndOfGame = 0
    if EndOfGame == 1:
        return 1
    else:
        return 0
    


window = Tk()
w = Canvas(window, width=600,height=400)
w.pack()
w.create_line(14,11,27,11,fill="grey",width=2)

# Create Dots
for XDots in range(GridSizeX):
    for YDots in range(GridSizeY):
        X = (Xoffs + (GridSpacing*XDots))
        Y = (Yoffs + (GridSpacing*YDots))
        create_circle(X,Y,2,w,"Binding")

# Create Horizontal Lines
for v_lines in range(GridSizeY):
    for h_lines in range(GridSizeX-1):
        XStart = Xoffs + 4 + (GridSpacing * h_lines)
        XEnd = XStart + (GridSpacing - 8)
        YStart = Yoffs - 2  + (GridSpacing * v_lines)
        YEnd = YStart + 5
        itm = w.create_rectangle(XStart,YStart,XEnd,YEnd,fill="white",tags="Htag" + str(h_lines))
        w.tag_bind("Htag" + str(h_lines),'<ButtonPress-1>',onObjectClickH)
        HLines.append(itm)
        HLinesSet.append(0)

# Create Vertical Lines
for v_lines in range(GridSizeY-1):
    for h_lines in range(GridSizeX):
        XStart = Xoffs - 2 + (GridSpacing * h_lines)
        XEnd = XStart + 5
        YStart = Yoffs + 4  + (GridSpacing * v_lines)
        YEnd = YStart + (GridSpacing - 8)
        itm = w.create_rectangle(XStart,YStart,XEnd,YEnd,fill="white",tags="Vtag" + str(h_lines))
        w.tag_bind("Vtag" + str(h_lines),'<ButtonPress-1>',onObjectClickV)
        VLines.append(itm)
        VLinesSet.append(0)

# Create text inside grid for displaying player letter names
for v_lines in range(GridSizeY-1):
    for h_lines in range(GridSizeX-1):
        XLoc = Xoffs + (GridSpacing /2) + (GridSpacing * h_lines)
        YLoc = Yoffs + (GridSpacing /2) + (GridSpacing * v_lines)
        itm = w.create_text(XLoc,YLoc,fill="Black",text=" ",tags="Ttag")
        GridState.append(itm)
        GridSetState.append(0)


# Set game state text
XLoc = Xoffs + (GridSpacing * GridSizeX)
YLoc = Yoffs + Yoffs
TSpacing = 15
Player1Text = w.create_text(XLoc,YLoc,fill="Black",text="Player 1 Score - 0", anchor=W)
Player2Text = w.create_text(XLoc,YLoc+(TSpacing*1),fill="Black",text="Player 2 Score - 0",anchor=W)
TurnCounter = w.create_text(XLoc,YLoc+(TSpacing*2),fill="Black",text="Number of turns - 0",anchor=W)
PlayerTurnDisplay = w.create_text(XLoc,YLoc+(TSpacing*3),fill="Black",text="It is player 1's turn",anchor=W)


window.mainloop()
