"""See the long note at the bottom for full explanation."""

import math
import sys
import random

#to go from tree to blob
#tree input:[(branch,branch,branch),river length, (branch,branch,branch)
#IDEA: what if can turn a string into this based on the flaps necessary for the word

#ex: [[2,1,2],1,[1],2,[1,1]] must start and end with a tuple, and alternate tuple and river.
#BUT not always. ex: undertrox's tree [[2,2],1,[1],1,[1,[1,2],1],1,[1,1]] subsublist :oca:

#this blobify function can't handle subsublists like the one above.
def blobify(tree):
    blob = []
    """
    for x in range(0,len(tree[0])-1):   #looking at the first tuple
        blob.append(tree[0][x]+tree[0][x+1])  #add the distance between branches in this cluster (tuple)
    blob.append(tree[0][-1] + tree[1]+tree[2][0])
    
    for x in range(0,len(tree[2])-1):   #looking at the first tuple
        blob.append(tree[2][x]+tree[2][x+1])  #add the distance between branches in this cluster (tuple)
    blob.append(tree[2][-1] + tree[3]+tree[4][0])
    """
    for j in range(0,math.floor(len(tree)/2)):  #this applies to all the clusters except the last
        k = j*2
        for x in range(0,len(tree[k])-1):#k refers to a cluster. x represents a branch in the cluster.
            blob.append(tree[k][x]+tree[k][x+1])  #add the distance between branches in this cluster (tuple)
        blob.append(tree[k][-1] + tree[k+1]+tree[k+2][0])  #this one jumps to the next cluster via the river
        #if it's the last cluster, don't jump river, and do the weird wrap up thing
    for x in range(0,len(tree[-1])-1):   #looking at the last cluster
        blob.append(tree[-1][x]+tree[-1][x+1])
#now to wrap back around
    final = 0
    for j in range(0,math.floor(len(tree)/2)):
        k = j*2 +1
        final = final + tree[k]  #final just counts all the rivers
    blob.append(final+tree[-1][-1]+tree[0][0])

    return blob

branchpositions =[]
branchlengths = []
def branchify(tree):
        for x in range(0,len(tree)): #take each item of the main list. either list or river. x = object in main list
            if isinstance(tree[x],list) == True: #if it's a list and does not have a list
                hassublist = False
                for y in range(0,len(tree[x])):   #check if it's a branch cluster or has rivers
                    if isinstance(tree[x][y],list) == True:
                        hassublist = True
                if hassublist == False:  #we want to add these branches (tree[x]) to branchlengths[] and record locations in branchpositions[]
                    for y in range(0,len(tree[x])):
                        branchlengths.append(tree[x][y])
                        branchpositions.append([x,y])

                if hassublist == True:
                    branchify(tree[x])





                    

successful_starting_positions = []
combinations = []
mingrid = 0
def pack(blob):
    mingrid = sum(blob)/4
    if mingrid != round(mingrid):
        mingrid = math.trunc(mingrid)
        mingrid = mingrid+1
    print("minimum grid size is " + str(mingrid)) #based on edge availability
    if mingrid<max(blob):
        mingrid = max(blob)
        print("adjusted minimum grid size is " + str(mingrid) +". This might get weird") #if one blob side is too large
    done = False
    while done == False:
        for x in range(0,len(blob)):   #x is the side (number) of the blob that we are starting with
            k = x                       #k is the side (number) of the blob that we are looking at rn
            side1 = []
            while sum(side1)<=mingrid-blob[k]:  #if side1 has room for another one
                side1.append(blob[k])
                k=k+1       #k is the length on the string that we are deciding to add or not
                if k == len(blob):      #if we've reached the end, took the last one
                    k=0        #wrap around to the begining of the blob

            side2 = []
            while sum(side2)<=mingrid-blob[k]:
                side2.append(blob[k])
                k = k+1
                if k == len(blob):  
                    k=0
            side3 = []
            while sum(side3)<=mingrid-blob[k]:
                if k == x:
                    break
                side3.append(blob[k])
                k = k+1
                if k == len(blob):  
                    k=0
            side4 = []
            while sum(side4)<=mingrid-blob[k]:
                if k == x:
                    break   #if it's already got all the sides, then it's done, don't add more
                side4.append(blob[k])
                k = k+1
                if k == len(blob):  
                    k=0
            if k == x:
                packing = side1,side2,side3,side4   #tuple, where each element is a list
                newpacking = False
                for x in range(0,len(combinations)): #this tests if the packing is new. Look at existing packings:
                    for y in range(0,4):   #look at the sides of this new packing
                        if packing[y] not in combinations[x]:   #if this side length is not in the already taken packing
                            newpacking = True
                if combinations == [] or newpacking == True: #if it's the first one or it's new
                    combinations.append(packing)      #list, where each element is a tuple, and each element of the tuple is a list
                    successful_starting_positions.append(x)
                done = True #means we found a solution; if it remains false, we increase grid size
                
        if combinations == []:
            #print("increase grid size and go back, haven't got this yet")
            mingrid = mingrid+1    
        
    combinations.append(int(mingrid))     #this is so the drawing function can easily access it
    print("practical grid size is " + str(mingrid))
    print("combinations",combinations)
    return combinations


        # 5 3 , 4 4, 2 2 4, 3 3 2, 神
        # perhaps input coordinates of trees and output coordinate of cp vertices?
        #undertrox's [4,3,5,2,6,4,4], this one does not work on default grid so +1









from tkinter import *
bp_packing = Tk()
canvas = Canvas(bp_packing,width=700,height=700)
#canvas.pack()

#canvas.create_rectangle(100,600,600,100,outline = "black", width = 2)

def grid(size):
    step = 500/size
    for x in range(1,size):
        canvas.create_line(100+x*step, 100, 100+x*step, 600, width = 0.5, fill = "gray")    #vertical line
        canvas.create_line(100,100+x*step, 600, 100+x*step, width = 0.5, fill = "gray")    #horizontal line
s=0
def drawgrid(blob,tree,C):  #blob will be packed, then used for markings and grid. tree is needed for square packing
    canvas.pack()
    canvas.create_rectangle(100,600,600,100,outline = "black", width = 2)
    combinations = pack(blob)
    mingrid = combinations[-1]
    grid(mingrid)

    #now to draw the red marks, first unpack the combinations list
    packing1 = combinations[C]
    packing1side1 = packing1[0]  #is a list of the distances along this side
    packing1side2 = packing1[1]
    packing1side3 = packing1[2]
    packing1side4 = packing1[3]

    s = 0
    s = successful_starting_positions[0]#################################change the 0 here for next solution#####################################
    def drawtopmarks(): #side 1
        s = successful_starting_positions[0]
        spot1 = 100 #we add to this variable so the marks build off the previous
        #print(packing1side1)
        for x in range(0,len(packing1side1)+1): #make sure you draw all the vertex marks. +1 gets the last one
            radius = branchlengths[s]*(500/mingrid) ########################
            canvas.create_line(spot1,100,spot1,85, width = 3, fill = "red") #mark
            canvas.create_rectangle(spot1-radius,100-radius,spot1+radius,100+radius,width=2,outline="blue") #square pack
            canvas.create_line(spot1-radius,100-radius,spot1+radius,100+radius,width = 2, fill = "red") #ridge
            canvas.create_line(spot1+radius,100-radius,spot1-radius,100+radius,width = 2, fill = "red") #ridge
            s = s+1
 #when you make the mark, draw the square too. use successful_starting_positions to find radii
            if x in range(0,len(packing1side1)):
                spot1 = spot1+ (500/mingrid)*packing1side1[x]
            

#Keep increasing s everytime you jump, but it will be a pain to try to keep in sync.
    #perhaps sync up at the start of every side?
    #keep increasing s; but if you get to a river in the tree list, s = s+1
                
    def drawrightmarks(): #side2
        s = successful_starting_positions[0]+len(packing1side1)
        spot2 = 100
        for x in range(0,len(packing1side2)+1):
            radius = branchlengths[s]*(500/mingrid) ########################
            canvas.create_line(600,spot2,615,spot2, width = 3, fill = "red")
            if x>0:
                canvas.create_rectangle(600-radius,spot2-radius,600+radius,spot2+radius,width=2,outline="blue") #square pack
                canvas.create_line(600-radius,spot2-radius,600+radius,spot2+radius,width = 2, fill = "red") #ridge
                canvas.create_line(600+radius,spot2-radius,600-radius,spot2+radius,width = 2, fill = "red") #ridge
            s = s+1
            if x in range(0,len(packing1side2)):
                spot2 = spot2+ (500/mingrid)*packing1side2[x]
            
    def drawbottommarks(): #side3
        s = successful_starting_positions[0]+len(packing1side1)+len(packing1side2)
        spot3 = 600
        for x in range(0,len(packing1side3)+1):
            radius = branchlengths[s]*(500/mingrid) ########################
            canvas.create_line(spot3, 600, spot3, 615, width = 3, fill = "red")
            if x>0:
                canvas.create_rectangle(spot3-radius,600-radius,spot3+radius,600+radius,width=2,outline="blue") #square pack
                canvas.create_line(spot3-radius,600-radius,spot3+radius,600+radius,width = 2, fill = "red") #ridge
                canvas.create_line(spot3+radius,600-radius,spot3-radius,600+radius,width = 2, fill = "red") #ridge
            s = s+1
            if x in range(0,len(packing1side3)):
                spot3 = spot3-(500/mingrid)*packing1side3[x]
                
    def drawleftmarks(): #side4
        s = successful_starting_positions[0]+len(packing1side1)+len(packing1side2)+len(packing1side3)        
        spot4 = 600
        for x in range(0,len(packing1side4)):
            radius = branchlengths[s]*(500/mingrid) ########################
            canvas.create_line(100,spot4,85,spot4, width = 3, fill = "red")
            if x>0:
                canvas.create_rectangle(100-radius,spot4-radius,100+radius,spot4+radius,width=2,outline="blue") #square pack
                canvas.create_line(100-radius,spot4-radius,100+radius,spot4+radius,width = 2, fill = "red") #ridge
                canvas.create_line(100+radius,spot4-radius,100-radius,spot4+radius,width = 2, fill = "red") #ridge
            s = s+1
            if x in range(0,len(packing1side4)):
                spot4 = spot4- (500/mingrid)*packing1side4[x]
                
    drawtopmarks()
    drawrightmarks()
    drawbottommarks()
    drawleftmarks()
    #canvas.create_text(350,650,text="solution "+str(1)+" of "+str(len(combinations)-1))

    print("successful starting positions", successful_starting_positions)

def coverup(C):
    canvas.create_rectangle(0,0,710,99,fill = "white",width = 0)
    canvas.create_rectangle(0,601,710,710, fill = "white",width = 0)
    canvas.create_rectangle(0,0,99,710,fill = "white",width = 0)
    canvas.create_rectangle(601,0,710,710,fill = "white",width = 0)
    canvas.create_rectangle(100,100,600,600,width = 2)
    canvas.create_text(350,33,text="solution "+str(C+1)+" of "+str(len(combinations)-1))
    canvas.create_text(350,66,text="grid size: " + str(combinations[-1]))

#1 tree -> 2 string -> 3 blob -> 4 square vertices -> 5 flaps -> 6 rivers (->7 cp)
    #5 and 6 require 1. 6 may not be possible (maybe make human do it)

#5: have it draw squares centered around the marks, would be easier and clearer than ridge creases
#nitpicky: maybe choose colors other than red and blue for the marks. maybe cyan for the packing

#keep a track of which starting point of the blob we are, so we can connect it back to the tree. line 61.
    #ex: if we started at blob position 0, we know that we are starting at tree[0][0], and tree[0][0] tells us the radius of the square

#6 use the move thing to move the squares around
    
#new feature for later: draw lines to highlight where you have freedom/wasted edge
#another feature: have it draw all the combinations. Also make it not have to
                #reload the program everytime

def treepacking(tree):   #combines blobify (tree -> blob) and drawgrid (blob -> packing)
    print("tree:",tree)
    blob = blobify(tree)
    print("blob: ",blob)
    branchify(tree)
    print("branch positions:", branchpositions)
    print("branch lengths:", branchlengths)
    drawgrid(blob,tree,0) #the 0 means first solution only. Soon, we can loop to show all solutions
    coverup(0)
    #drawgrid(blob,tree,1)

#treepacking([[random.randrange(1,5),random.randrange(3,7),random.randrange(1,5)],random.randrange(1,5),[random.randrange(1,6),random.randrange(1,6)],random.randrange(1,5),[random.randrange(4,9)]])

"""
OVERALL EXPLANATION
1. tree
2. string figure (skipped)
3. blob
4. packed square that tracks vertices
5. the square and vertices on the edge, but with the square packing

1. The tree is input numerically by writing out a list of lists. rivers are integers
    on their own, are not in a list (kinda. it's complicated)
2. skip straight to 3
3. the blob figure is made by blobify(tree) and caluclates the distances between the
    tips of branches as paths along the tree. It is circular, so to speak.
4. The minimum grid size is calculated based off the blob figure. The program
    tries to inscribe a square of the given grid size into the blob figure.
    If it doesn't work, the program increases the grid size and tries again. There
    may be multiple solutions.
5. the vertices are marked based on the packing along the 4 sides, then a square and
    ridge creases are drawn around the vertex with "radius" being the flap length for
    that vertex. If there are wasted edges, the flaps on that edge might be able to shift.


STILL NEEDS TO BE DONE
=========
show multiple solutions: open a new canvas, but all of them called canvas. etc need the name of the new canvas.
    that or have a button to switch between them. canvas.update() and clear the thing
better blobifier. is locations necessary though? (actually, probably yeah for blob to work)
fix the situations that print "this might get weird". example: treepacking([[1,1],2,[3,1]]). This one has empty lists
fix overlapping squares. ex [[4, 6, 1], 1, [3, 4], 3, [6]]
"""
