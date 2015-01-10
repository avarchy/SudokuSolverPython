#Adithya Venkatesan
#sudoku

#

import copy
import time

def allasign(mappa):
  if mappa == None:
    return False
  for a in mappa:
    if mappa[a] < 0:
      return False
  return True

def bt(possnum, finnums):#back tracking 
  global paths

  if allasign(finnums):
    return finnums
  #heristics: 1. least number of poss cols  2. most neighbors with unfilled colors  
  curmincols = 10
  arrmincols = []
  for a in possnum:
    if len(possnum[a]) < curmincols:
      arrmincols = []
      arrmincols.append(a)
      curmincols = len(possnum[a])
    elif len(possnum[a]) == curmincols:
      arrmincols.append(a)
  
  #least num of poss cols
  
  if len(arrmincols) > 1:
    curmaxneighs = 0
    nextstate = ""
    for a in arrmincols:
      totunfilledneighs = 0
      for b in paths[a]:
	if finnums[b] == -1:
	  totunfilledneighs+=1
      if totunfilledneighs > curmaxneighs:
	curmaxneighs = totunfilledneighs
	nextstate = a
  else:
    nextstate = arrmincols[0]
  #most neighbors with unfilled colors

  #know which state to go to
  
  #backtracking
  
  for a in possnum[nextstate]:
    tpossnum = copy.deepcopy(possnum)
    tfinnums = copy.deepcopy(finnums)
    #copy stuff
    curneighs = paths[nextstate]#neighbors nextstate has
    tfinnums[nextstate] = a #sets the final color of nextstate to w/e it is
    del tpossnum[nextstate]#deletes the colors possibilites
    #takes out the possibility of that color from neighbors
    for b in curneighs:
      if tfinnums[b]!=-1:
	continue
      if a in tpossnum[b]:
	(tpossnum[b]).remove(a)
      if len(tpossnum[b]) == 0:
	return None
    x= bt(tpossnum, tfinnums)
    if allasign(x):
      return x
    
    
  return None
    
    
def outrecur():
  global paths
  global possnums
  global finnums
  return bt(possnums, finnums)
  #finish

#getting paths
paths = {}
for num in range(0,81):
  myneighbors = []
  y = int(num/9)
  x = int(num-(y*9))
  tempx = int(x)
  for a in range(0,9):
    if x+a*9 not in myneighbors:
      myneighbors.append(x+a*9)
  tempy = int(y)
  for a in range(0,9):
    if (y*9)+a not in myneighbors:
      myneighbors.append(y*9+a)
  initx = 3*int(x/3)
  inity = 3*int(y/3)
  
  for a in range(0,3):
    for b in range(0,3):
      tomaybeeadd = (initx+a)+(inity+b)*9
      if tomaybeeadd not in myneighbors:
	myneighbors.append( (initx+a)+(inity+b)*9 )
  paths[num] = myneighbors
#got all the paths

alllist = open('top95.txt','r').read().split('\n')

#multiple puzzles
for puzzle in alllist:
  if len(puzzle) < 81:#just getting rid of that annoying empty line
    continue
  tima = time.time()
  plist = list(puzzle)
  

  possnums = {}
  finnums = {}
  
  for a in range(0,81):#adding to finnums and possnums if no definite fin number
    if plist[a] == '.':
      possnums[a] = [1,2,3,4,5,6,7,8,9]
      finnums[a] = -1
    else:
      finnums[a] = int(plist[a])
  
  for a in range(0,81):
    #removing all the things that we know aren't posscols
    if not (finnums[a] == -1):
      continue
    
    for bneigh in paths[a]:
      if (finnums[bneigh]) in (possnums[a]):
	(possnums[a]).remove(finnums[bneigh])
	
  final = outrecur()
    
  puzzsol = ''
  for a in final:
    puzzsol+= (str(final[a]))
  timb = time.time()
  print puzzsol, (timb-tima)
    
      