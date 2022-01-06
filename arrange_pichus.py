#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Pratap Roy Choudhury (Username : prroyc), MS-DS, 2000715787]
#
# Based on skeleton code in CSCI B551, Fall 2021.
# [Reference] : Row and Column wise check code portion idea is referenced from Internet https://github.com/AjinkyaPawale/Artificial-Intelligence/tree/main/Maps

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 


#Check if the house_map in successor list has any pichu conflicts or it's one of the valid house_maps
def is_conflict(curr_house_map,pichu_loc):
    # initialise a conflict status as False, update as True if finds conflict in any direction ----
    # and return True if house_map is invalid and False if house_map is a valid
    conflict = False 
    ##################################################################### Code Idea reference start #########################################################################
    # check for any row wise conflict considering '.'/'X'/'@'/'p' states
    for rowno in range(0,len(curr_house_map)):
        flag = False # flag = False traces if there is any 'X' between any two points in the same row, hence no conflict
        for colno in range(0,len(curr_house_map[0])):
            if curr_house_map[rowno][colno] == 'p' and flag ==False:
                flag = True #reset flag = True on first pichu encounter after a valid move
            elif curr_house_map[rowno][colno] == 'p' and flag == True: # in the same row, if there is another pichu without any X/@ in between, then its a conflict 
                conflict = True
                break   
            elif curr_house_map[rowno][colno] == '.':
                continue
            elif curr_house_map[rowno][colno] in 'X@': 
                flag = False # reset flag = False on encountering a X/@ in between two moves
            

   # check for any column wise conflict considering '.'/'X'/'@'/'p' states         
    for colno in range(0,len(curr_house_map[0])):
        flag = False # flag = False traces if there is any 'X' between any two points in the same column, hence no conflict
        for rowno in range(0,len(curr_house_map)):
            if curr_house_map[rowno][colno] == 'p' and flag ==False:
                flag = True #reset flag = True on first pichu encounter after a valid move
            elif curr_house_map[rowno][colno] == 'p' and flag == True: # in the same column, if there is another pichu without any X/@ in between, then its a conflict 
                conflict = True
                break   
            elif curr_house_map[rowno][colno] == '.':
                continue
            elif curr_house_map[rowno][colno] in 'X@': 
                flag = False # reset flag = False on encountering a X/@ in between two moves
            
    ##################################################################### Code Idea Reference End #########################################################################

    # check for any diagonal wise conflict considering '.'/'X'/'@'/'p' states         
    for loc in pichu_loc: # check for each pichu's location in the house_map, if it has any conflict in any of the diagonal direction
        flag = False # flag = False traces if there is any 'X' between any two points in the diagonals, hence no conflict
        for rowno in range(0,len(curr_house_map)):
            for colno in range(0,len(curr_house_map[0])):
                if abs(loc[0]-rowno)==abs(loc[1]-colno): #check if (rowno,colno) is a diagonal position wrt each pichu's location
                    if curr_house_map[rowno][colno] == 'p' and flag ==False:
                        flag = True #reset flag = True on first pichu encounter after a valid move
                    elif curr_house_map [rowno][colno] == 'p' and flag == True: # diagonally, if there is another pichu without any X/@ in between, then its a conflict
                        conflict = True
                        break   
                    elif curr_house_map[rowno][colno] == '.':
                        continue
                    elif curr_house_map[rowno][colno] in 'X@': 
                        flag = False # reset flag = False on encountering a X/@ in between two diagonal positions
                
    # If any of the above condition(i.e row/column/diagonal) sets the conflict variable as True, then is_conflict() returns True else False(ie no conflict)         
    return conflict 



# Arrange agents on the map
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.


def solve(initial_house_map, k):

    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop()):
            pichu_loc=list() #initialise an empty pichu_loc list to store all the locations of each pichu in each of the successor house_map
            for row_i in range(len(new_house_map)):
                for col_i in range(len(new_house_map[0])):
                    if new_house_map[row_i][col_i]=="p":
                        pichu_loc.insert(0,(row_i,col_i))

            # new validation function to check conflicts
            if not is_conflict(new_house_map,pichu_loc): # conflict check that returns True if there is/are pichu conflicts---
                                                            #else return False which is a valid housemap condition
                if is_goal(new_house_map, k): # check if the current valid housemap has all the pichu without any conflict which is the goal state
                    return(new_house_map,True)
                fringe.append(new_house_map) # the valid housemap gets added in the fringe for further exploration of successor housemaps
                
    return ([],False) #if no valid house_map exists for K pichus, then return False

# Main Function
if __name__ == "__main__": 
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    if k==1: # if k equals 1 ie only one Pichu in house, then the initial house map itself will be the resultant map 
        solution = house_map, True
    else: # if more than one Pichu present, then call the solve function to arrange each Pichu without conflict
        solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")
    


