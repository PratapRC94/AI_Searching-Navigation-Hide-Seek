# Part 1: Navigation

A certain autonomous agent likes to fly around the house and interrupt video recordings at the most inopportune moments.
Suppose that a house consists of a grid of N x M cells, represented like this:

```
....XXX
.XXX...
....X..
.X.X...
.X.X.X.
pX...X@
```

As you can see, the map consists of N lines (in this case, 6) and M columns (in this case, 7). Each cell of the house is marked with one of four symbols: 
* p - represents the agent's current location
* X - represents a wall through which the agent cannot pass
* . - represents open space over which the agent can fly
* @ - represents my location (presumably with video recording in progress)

Our goal is to write a program that finds the shortest path between the agent and me. The agent can move one square at a time in any of the four principal compass directions, and the program should find the shortest distance between the two points and then output a string of letters (L, R, D, and U for left, right, down, and up) indicating that solution. The program should take a single command line argument, which is the name of the file containing the map file.
For example:

```
prroyc@silo:~/prroyc-a0$ python3 route_pichu.py map1.txt
Shhhh... quiet while I navigate!
Here's the solution I found:
16 UUURRDDDRRUURRDD
```

You can assume that there is always exactly one p and one @ in the map file. If there is no solution, your program should display path length -1 and not display a path.

## Solution

The goal of this problem is to find the shortest path between the agent “p” and goal “@”. It will return the number of steps taken and all the moves in U/D/L/R directions.

A skeleton program route_pichu.py was already given. Unfortunately, the program does not work very well; it will probably enter in an infinite loop and you'll have to press CONTROL-C to kill it. Nevertheless, the code is a good starting point.

1. **What is the set of valid states?** - *The valid states are those moves which are indicated as '.' and 'p' is placed in that move.*
2. **The successor function?** - *It identifies all the next states of house map from the current location of 'p' considering the valid index of N x M grid*
3. **The cost function?** - *Here cost is the number of steps/moves that 'p' takes to reach each valid location and ended up arriving at '@'*
4. **The goal state definition, and the initial state?** - *The Goal state is when the next valid move of 'p' finds '@'. The initial state is the starting configuration of the house map with 'p' placed in any of the grid point.*
5. **Why does the program often fail to find a solution?** - *The skeleton program was falling in an infinite loop in its while condition in the **search()** function since it was revisiting the already visited moves continuously.*

To run the program correctly and more efficiently, the **search(house_map)** function has been modified in the skeleton code and **get_direction(child_move, parent_move)** function has been defined to find the directional moves taken by 'p' from initial state to goal state.

### Algorithm

* **pichu_loc** - *Starting location of 'p' in the initial state*
* **fringe** - *A **queue** FRINGE that contains all the valid move location, current distance from initial state(ie the cost till the current state) and current route travelled from the initial state. It is a list of tuples where each tuple has the above 3 informations and the tuples are poped out in FIFO manner.*
* **visited** - *a list to store all the visited moves to keep track of it so that 'p' doesn't step into the already visited move.*
* **curr_move** - *current location of 'p' that has been removed from FRINGE*
* **curr_dist** - *cost incured till the curr_move location*
* **curr_route** - *directional route travelled by 'p' till curr_move location from initial state*

### Algorithm : search(house_map)

```
1. pichu_loc <- initial_move
2. Initialise route = '', visited =[]
3. INSERT((pichu_loc,0,route), fringe)
4. Repeat:
6.  curr_move, curr_dist, curr_route <- REMOVE(fringe)
7.  INSERT(curr_move, visited)
8.  For every valid move s' in SUCC(curr_move):
9.    If s' not in visited:
10.     IF GOAL?(s') then find path(call get_direction), return curr_dist+1 and curr_route
11.     INSERT((s',curr_dist+1,curr_route+get_direction(s',curr_move)), fringe)
12. If empty(FRINGE) then return -1
```

### Algorithm : get_direction(child_move, parent_move)

```
1. If child_move.Row = parent_move.Row:
2.   If child_move.Col = parent_move.Col + 1 ? then return 'R' else return 'L'
3. If child_move.Row = parent_move.Row + 1 ? then return 'D' else return 'U'
```

**Sample Output**

```
Initial state: 
....XXX
.X.X...
.X..X..
.X.X...
.X.X.X.
pX...X@

Shhhh... quiet while I navigate!
Here's the solution I found:
20 UUUUURRDDDDDRRUURRDD
```


# Part 2: Hide-and-seek

Suppose that instead of a single agent as in Part 1 (Navigation), you have adopted k agents. The problem is that these agents do not like one another, which means that they have to be positioned such that no two agents can see one another. Write a program called arrange_pichus.py that takes the filename of a map in the same format as Part 1 as well as a single parameter specifying the number k of agents that you have. You can assume k >= 1. Assume two agents can see each other if they are on either the same row, column, or diagonal of the map, and there are no walls between them. An agent can only be positioned on empty squares (marked with .). It's okay if agents see you (@), and you obscure the view between agents, as if you were a wall. Your program should output a new version of the map, but with the agents' locations marked with p. Note that exactly one p will already be fixed in the input map file. If there is no solution, your program should just display False. 
Here's an example on the same sample output on the same map as in Part 1:

```
prroyc@silo:~/prroyc-a0$ python3 arrange_pichus.py map1.txt 5

Looking for solution...

Here's what we found:
.p..XXX
.XXX...
....X..
.X.X...
.XpX.Xp
pX..pX@
```

## Solution

The goal of this problem is to find a valid house map accomodating all the k agents without any conflict. A conflict is when two agents can see each other either horizontally, vertically or diagonally without any wall(X) or me(@) between them.

A skeleton program was already given which is saved as arrange_pichus_skeleton.py. But it's not fully working; the configurations it finds often allow agents to see one another, and it can be quite slow. We need to fix the code so that it works, and then try to make it run as quickly as possible.

1. **What is the set of valid states?** - *The valid states are those house maps which has k agents placed and there is no conflict.*
2. **The successor function?** - *It identifies all the possible configuration of housemaps with k=2,3,4...n*
3. **The cost function?** - *Here cost is ignored as one agent is added in the house map one by one satisfying the non conflicting conditions with another agent(p).*
4. **The goal state definition, and the initial state?** - *The goal state is when the house map has all the k agents(p) placed without any conflicting condition. The initial state is the starting configuration of the house map with only 1 agent 'p' placed in any of the grid point.*

To run the program correctly and more efficiently, the **solve(initial_house_map, k)** function has been modified in the skeleton code and **is_conflict(curr_house_map,pichu_loc)** function has been defined to check if the house_map in successor maps list has any agent conflicts or it's one of the valid house_maps.

### Algorithm

* **pichu_loc** - *all the location of each agent 'p' in every successor housemaps*
* **fringe** - *A **list** FRINGE that contains the initial state housemap and subsequently all the valid house maps from the successor states. It is a list of lists where each list again are the house map configuration and they are poped out in LIFO manner as the search abstraction used here is depth first search.*

### Algorithm : solve(initial_house_map, k)

```
1. If k=1? then return initial_house_map and True, else call solve()
2. INSERT(initial_house_map, fringe)
3. Repeat:
4   For every s' in SUCC(REMOVE(fringe)):
5.    Initialise pichu_loc = []
6.    INSERT((p.row,p.col), pichu_loc) for every p in s'
7.    If Not is_conflict(s', pichu_loc):
8.      If GOAL(s',k)? then return s' and True
9.      INSERT(s',fringe)
10. If empty(fringe) then return False
```

### Algorithm : is_conflict(curr_house_map,pichu_loc)

```
1. Initialise conflict = False
2. For each row in s': # row wise conflict check
3.   Set flag = False
4.   For each col in s':
5.    If s'[row][col] = p and flag = False, then set flag = True
6.    If s'[row][col] = p and flag = True, then set conflict = True and break
7.    If s'[row][col] = '.' then continue
8.    If s'[row][col] = X or @, then set flag = False
9. For each col in s': # column wise conflict check
10.  set flag = False
11.  For each row in s':
12.   If s'[row][col] = p and flag = False, then set flag = True
13.   If s'[row][col] = p and flag = True, then set conflict = True and break
14.   If s'[row][col] = '.' then continue
15.   If s'[row][col] = X or @, then set flag = False
16. For each loc in pichu_loc list from s': # diagonal conflict check
17.   set flag = False
18.   For each row in s':
19.     For each col in s':
20.       If |loc[0]-row| = |loc[1]-col|: # check if (row,col) index is diagonal to loc
21.         If s'[row][col] = p and flag = False, then set flag = True
22.         If s'[row][col] = p and flag = True, then set conflict = True and break
23.         If s'[row][col] = '.' then continue
24.         If s'[row][col] = X or @, then set flag = False
25. Return conflict
```

**Sample Output**

```
prroyc@silo:~/prroyc-a0$ python3 arrange_pichus.py map2.txt 7
Starting from initial board:
....XXX
.X.X...
.X..X..
.X.X...
.X.X.X.
pX...X@

Looking for solution...

Here's what we found:
...pXXX
.X.X.p.
.X.pX..
.X.X...
.XpX.Xp
pX..pX@
```
### Algorithm Improvment Area:

There is always a limiting k=i for k=1,2..n,i<=n depending on the house grid size after which there won't be any valid house map exist without any confliction between k agents and as k increases, it will keep return False. But the process to get False in that case will be tedious as it will explore all the successor house map states with k agents.

So, a checking condition can be put on the very first k = i when it return False, and break out of the loop, so that for any k = i+1,i+2...n agents, the house map is not needed to be checked for validity and the program returns False as a result.
