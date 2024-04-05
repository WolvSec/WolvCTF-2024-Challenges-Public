from pwn import *

# side length of a cube face
side = 26

# cube
maze = ["..........................#---###-#-------##########..........................",
        "..........................###-###-#########------#--..........................",
        "..........................#-----#-----------######-#..........................",
        "..........................--###-####-###-#------##-#..........................",
        "..........................#-#--------#-#-###-#-##--#..........................",
        "..........................#-##########-###-###-##-##..........................",
        "..........................---------------#-#-#------..........................",
        "..........................########-#####-#-#-#######..........................",
        "..........................##-----#-#----------------..........................",
        "..........................---###-#-#####-########-##..........................",
        "..........................####---#-----#-#---##-#---..........................",
        "..........................-----#-#-###-#-#-#-##-####..........................",
        "..........................-#####-#-#-#-#-#-#----##--..........................",
        "..........................-#-------#---#-#-##-#-##-#..........................",
        "..........................-#-##################-##-#..........................",
        "..........................##-#------------------##-#..........................",
        "..........................##-##########-##########-#..........................",
        "..........................##---#----------##-#---#-#..........................",
        "..........................####-#-####-###-#----###-#..........................",
        "..........................---#-#-####--##-#-##-----#..........................",
        "..........................##-#-#-#####-##---########..........................",
        "..........................##-#-#-##----###-##------#..........................",
        "..........................-----#-#####-#-#-#--####--..........................",
        "..........................####-#-#-----#-#-#-#######..........................",
        "..........................---------###-#-#-#-----#--..........................",
        "..........................####-#######-#-#-#-#-#-#-#..........................",
        "###-----###--######-##-#-##----#-------#-#-#-#-#-#-##-#-#########-###-########",
        "###-########-#------##-#-##-####-#-###-#-#-#---#-#----#---###-----------------",
        "--#--------#-#####--##-#--###----#-#-###-#-###-#-####-###-####################",
        "#-#-#-####-#-#-#---###-##-#---####----##-#-#####-#-#--#-#-#--------------#----",
        "#-###-######-#-#####-#--#-#####-#######--------###---##-#-#-###-###-####-###-#",
        "#-----#-----------##-##-#-#----------##-#####-------###-#-###-###-#-##--------",
        "##########-#-#-##-##-##-#-#####-####----#-#-#########---#-##---------#####-###",
        "------####-#-#-##-#---#-#---#-----#######----#-----##-#-#-####-####-###-------",
        "#####-#----#-#------###-###-#-###-#----##-######-###--#-#-####-#-##-#-####-#-#",
        "#-----#-##-#-########-#---#-#-###-####---------#-#---##-#-#----#------#-#--#-#",
        "#-###-#--#-#-#---#----#-###-#-#------#-######-##-#####--#-#-##-#-####-#-#-##-#",
        "#-#-####-#-#-#-#-#-#-##-----#-#-######-----#--##-----#-##---##-#-#-####-###--#",
        "---------#-#---#-#-#-####-###-#-##-#-#####-#-#######-#-#######-###------#-#-##",
        "###-######-#####-###---##-#-#-#-#--#-#---#-#---------#-------------##-#-#-#-#-",
        "#-#-#------#-----#-###----#-#-#-#-##-###-#-#-#######-#-################-#-#-#-",
        "#-#-#-####-#####-#-----####-#-#-#--#-#-#-###---#-----#-#--##----------#-------",
        "#-###-#--------#-#-###-#----#---##-----------#-#-#####-##----##########-#-##-#",
        "#-----#-######-#---#-#-#-##-######-###########-#--------####-#----------#-##-#",
        "##-####-#-##-#-###-#-#---##-------##-#------##-########-#----#-#-##-##-##-##-#",
        "-#----#-#-#----#-#-#---########-#----#-####-##----------##-###-#-##-##-#--##-#",
        "---####-#-##-#-#-#-#-####----#######-#-##-#-##-##-########-#---#-#####-#-#-#-#",
        "##-#----#--###-#-#-###-##-##---###--------####-##-##-----#-#-###---#-#-#-#-#--",
        "---#-####------#-#--------#--#---####-#-#----#-##----###-#-#-#####-#-#-###-###",
        "####-####-####---##########-####----#-#-#-##-#######-#-#-#-#----##-#-#-----###",
        "#-------#----#-###------#############-###-##-#-----#---#-#-######------###-###",
        "#######-######-#---####-###-----------#-#-##-#-###-#####-#--------########-###",
        "..........................#-###########-####-#-#---#..........................",
        "..........................#-##-#######---------#####..........................",
        "..........................----------###-######-----#..........................",
        "..........................######-##-###-#----#######..........................",
        "..........................-----#--#---#---##-#------..........................",
        "..........................###-###-###-#-####-#-#####..........................",
        "..........................#--------######-####-#----..........................",
        "..........................#-#########------#---#-###..........................",
        "..........................###---------####-#####-#-#..........................",
        "..........................-###############-#####-#-#..........................",
        "..........................-##--------------------#-#..........................",
        "..........................-#########-#####-#######-#..........................",
        "..........................##-----###-#---#-#--------..........................",
        "..........................---#-###-###-#-#-#-#######..........................",
        "..........................####-#-----#-#-#-#-#-----#..........................",
        "..........................#----#-###-#-#-#-#-#-###-#..........................",
        "..........................#-####-#---#-#---#-#-#-#--..........................",
        "..........................#-#----#-###-#####-#-#-#-#..........................",
        "..........................--#-####---------#---#-#-#..........................",
        "..........................#-#----##-######-#####-#-#..........................",
        "..........................#-####-#--#------------#--..........................",
        "..........................#------#-###############-#..........................",
        "..........................--######-#---------------#..........................",
        "..........................###--------###-#-#########..........................",
        "..........................-#######-#-#---#-#--------..........................",
        "..........................-----#-#-###-###-#####-#-#..........................",
        "..........................-#-#-#-#-#-----#-#-----#-#..........................",
        "..........................##-#-#-#-#######-#-#####-#..........................",
        "..........................##--##-#---------------###..........................",
        "..........................###-#--#-#########-###-#--..........................",
        "..........................#-#-#-##---------#---#-#-#..........................",
        "..........................#---#-##-#-#-#-#####-#-#-#..........................",
        "..........................###-#-#--#-#-#-------#----..........................",
        "..........................#-#-#-#-##-#-#############..........................",
        "..........................----#-##########---------#..........................",
        "..........................#-#-#----------#-#######--..........................",
        "..........................#-#-####-#####-#-#-##----#..........................",
        "..........................#-#-#----#---#-----#--####..........................",
        "..........................#-###-####-#-#-###-#-##---..........................",
        "..........................------#-##-###---#-#-####-..........................",
        "..........................#######-##-----#-#-#-#----..........................",
        "..........................------#-#-####-#####-#-###..........................",
        "..........................#-#-#-#---#----------#-###..........................",
        "..........................#-#-----##################..........................",
        "..........................#-#-###----------#-#-----#..........................",
        "..........................#-#-#-#-########-#-#-#-###..........................",
        "..........................#-#-#-###------------#-#--..........................",
        "..........................#-###-##########-###-#---#..........................",
        "..........................#-------------#--#-#-#####..........................",
        "..........................#-######-#########-----#-#..........................",
        "..........................#-----#-----#------###---#..........................",
        "..........................#####-####--##########-###.........................."]

def face_of(row, col):
    if row < side:
        return "back"
    elif row < side*2 and row >= side and col < side:
        return "left"
    elif row < side*2 and row >= side and col >= side and col < side*2:
        return "top"
    elif row < side*2 and row >= side and col >= side*2:
        return "right"
    elif row >= side*2 and row < side*3:
        return "front"
    elif row >= side*3:
        return "bot"
    else:
        return "bad"

# adjust the position to wrap around the faces of the cube
def fix_pos(row, col):
    nrow = row
    ncol = col
    if row == -1:
        nrow = (side*4)-1
        ncol = col
    elif col == -1:
        nrow = (side*4)-(row-side+1)
        ncol = side
    elif row == side*4:
        nrow = 0
        ncol = col
    elif col == side*3:
        nrow = (side*4)-(row-side+1)
        ncol = (side*2)-1
    elif row < side and col == side-1:
        nrow = side
        ncol = row
    elif row < side and col == side*2:
        nrow = side
        ncol = (side*3)-(row+1)
    elif row == side-1 and col < side:
        nrow = col
        ncol = side
    elif row == side-1 and col >= side*2:
        nrow = (side*3)-(col+1)
        ncol = (side*2)-1
    elif row == side*2 and col < side:
        nrow = (side*3)-(col+1)
        ncol = side
    elif row == side*2 and col >= side*2:
        nrow = col
        ncol = (side*2)-1
    elif row >= side*2 and row < side*3 and col == side-1:
        nrow = (side*2)-1
        ncol = (side-1)-(row-(side*2))
    elif row >= side*2 and row < side*3 and col == side*2:
        nrow = (side*2)-1
        ncol = row
    elif row >= side*3 and col == side-1:
        nrow = side+((side*4)-(row+1))
        ncol = 0
    elif row >= side*3 and col == side*2:
        nrow = side+((side*4)-(row+1))
        ncol = (side*3)-1
    return (nrow, ncol)

# for tracking current orientation of the cube.
# current_direction is the input move direction to move towards the lowest row of the current face.

def input_dir(face_dir):
    global current_direction
    if current_direction == 'u':
        return face_dir
    elif current_direction == 'd':
        if face_dir == 'u':
            return 'd'
        elif face_dir == 'd':
            return 'u'
        elif face_dir == 'l':
            return 'r'
        elif face_dir == 'r':
            return 'l'
    elif current_direction == 'l':
        if face_dir == 'u':
            return 'l'
        elif face_dir == 'd':
            return 'r'
        elif face_dir == 'l':
            return 'd'
        elif face_dir == 'r':
            return 'u'
    elif current_direction == 'r':
        if face_dir == 'u':
            return 'r'
        elif face_dir == 'd':
            return 'l'
        elif face_dir == 'l':
            return 'u'
        elif face_dir == 'r':
            return 'd'

# for rotating the cube when the current face changes.
def update_dir(old_face, new_face):
    global current_direction
    if old_face == "back":
        if new_face == "left":
            if current_direction == 'u':
                current_direction = 'r'
            elif current_direction == 'd':
                current_direction = 'l'
            elif current_direction == 'l':
                current_direction = 'u'
            elif current_direction == 'r':
                current_direction = 'd'
        elif new_face == "right":
            if current_direction == 'u':
                current_direction = 'l'
            elif current_direction == 'd':
                current_direction = 'r'
            elif current_direction == 'l':
                current_direction = 'd'
            elif current_direction == 'r':
                current_direction = 'u'
    elif old_face == "left":
        if new_face == "front":
            if current_direction == 'u':
                current_direction = 'r'
            elif current_direction == 'd':
                current_direction = 'l'
            elif current_direction == 'l':
                current_direction = 'u'
            elif current_direction == 'r':
                current_direction = 'd'
        elif new_face == "back":
            if current_direction == 'u':
                current_direction = 'l'
            elif current_direction == 'd':
                current_direction = 'r'
            elif current_direction == 'l':
                current_direction = 'd'
            elif current_direction == 'r':
                current_direction = 'u'
        elif new_face == "bot":
            if current_direction == 'u':
                current_direction = 'd'
            elif current_direction == 'd':
                current_direction = 'u'
            elif current_direction == 'l':
                current_direction = 'r'
            elif current_direction == 'r':
                current_direction = 'd'
    elif old_face == "right":
        if new_face == "front":
            if current_direction == 'u':
                current_direction = 'l'
            elif current_direction == 'd':
                current_direction = 'r'
            elif current_direction == 'l':
                current_direction = 'd'
            elif current_direction == 'r':
                current_direction = 'u'
        elif new_face == "back":
            if current_direction == 'u':
                current_direction = 'r'
            elif current_direction == 'd':
                current_direction = 'l'
            elif current_direction == 'l':
                current_direction = 'u'
            elif current_direction == 'r':
                current_direction = 'd'
        elif new_face == "bot":
            if current_direction == 'u':
                current_direction = 'd'
            elif current_direction == 'd':
                current_direction = 'u'
            elif current_direction == 'l':
                current_direction = 'r'
            elif current_direction == 'r':
                current_direction = 'd'
    elif old_face == "front":
        if new_face == "left":
            if current_direction == 'u':
                current_direction = 'l'
            elif current_direction == 'd':
                current_direction = 'r'
            elif current_direction == 'l':
                current_direction = 'd'
            elif current_direction == 'r':
                current_direction = 'u'
        elif new_face == "right":
            if current_direction == 'u':
                current_direction = 'r'
            elif current_direction == 'd':
                current_direction = 'l'
            elif current_direction == 'l':
                current_direction = 'u'
            elif current_direction == 'r':
                current_direction = 'd'
    elif old_face == "bot":
        if new_face == "left" or new_face == "right":
            if current_direction == 'u':
                current_direction = 'd'
            elif current_direction == 'd':
                current_direction = 'u'
            elif current_direction == 'l':
                current_direction = 'r'
            elif current_direction == 'r':
                current_direction = 'd'

# initialize second mattrix to track single step moves to any position
single_moves_to_pos = []
for mrow in maze:
    init_row = []
    for c in mrow:
        if c == '.':
            init_row.append(-1)
        elif c == '#':
            init_row.append(-2)
        elif c == '-':
            init_row.append(10000)
    if len(init_row) != len(mrow):
        print("bad maze")
        exit()
    single_moves_to_pos.append(init_row)

# find number of single step moves to any position from starting location
check = [ (39, 38) ]
single_moves_to_pos[39][38] = 0
while check != []:
    pos = check[0]
    check = check[1:]
    current_moves = single_moves_to_pos[pos[0]][pos[1]]
    u = single_moves_to_pos[fix_pos(pos[0]-1, pos[1])[0]][fix_pos(pos[0]-1, pos[1])[1]]
    d = single_moves_to_pos[fix_pos(pos[0]+1, pos[1])[0]][fix_pos(pos[0]+1, pos[1])[1]]
    l = single_moves_to_pos[fix_pos(pos[0], pos[1]-1)[0]][fix_pos(pos[0], pos[1]-1)[1]]
    r = single_moves_to_pos[fix_pos(pos[0], pos[1]+1)[0]][fix_pos(pos[0], pos[1]+1)[1]]

    if u >= 0 and u > current_moves:
        single_moves_to_pos[fix_pos(pos[0]-1, pos[1])[0]][fix_pos(pos[0]-1, pos[1])[1]] = current_moves+1
        check.append(fix_pos(pos[0]-1, pos[1]))
    if d >= 0 and d > current_moves:
        single_moves_to_pos[fix_pos(pos[0]+1, pos[1])[0]][fix_pos(pos[0]+1, pos[1])[1]] = current_moves+1
        check.append(fix_pos(pos[0]+1, pos[1]))
    if l >= 0 and l > current_moves:
        single_moves_to_pos[fix_pos(pos[0], pos[1]-1)[0]][fix_pos(pos[0], pos[1]-1)[1]] = current_moves+1
        check.append(fix_pos(pos[0], pos[1]-1))
    if r >= 0 and r > current_moves:
        single_moves_to_pos[fix_pos(pos[0], pos[1]+1)[0]][fix_pos(pos[0], pos[1]+1)[1]] = current_moves+1
        check.append(fix_pos(pos[0], pos[1]+1))

# follow optimal path in reverse and mark each position in the maze
opt = single_moves_to_pos[90][38]
check = [ (90, 38) ]
while check != []:
    pos = check[0]
    check = check[1:]
    current_moves = single_moves_to_pos[pos[0]][pos[1]]
    if c == 0:
        break
    u = single_moves_to_pos[fix_pos(pos[0]-1, pos[1])[0]][fix_pos(pos[0]-1, pos[1])[1]]
    d = single_moves_to_pos[fix_pos(pos[0]+1, pos[1])[0]][fix_pos(pos[0]+1, pos[1])[1]]
    l = single_moves_to_pos[fix_pos(pos[0], pos[1]-1)[0]][fix_pos(pos[0], pos[1]-1)[1]]
    r = single_moves_to_pos[fix_pos(pos[0], pos[1]+1)[0]][fix_pos(pos[0], pos[1]+1)[1]]

    if u == current_moves-1:
        single_moves_to_pos[pos[0]][pos[1]] = -3
        check.append(fix_pos(pos[0]-1, pos[1]))
    if d == current_moves-1:
        single_moves_to_pos[pos[0]][pos[1]] = -3
        check.append(fix_pos(pos[0]+1, pos[1]))
    if l == current_moves-1:
        single_moves_to_pos[pos[0]][pos[1]] = -3
        check.append(fix_pos(pos[0], pos[1]-1))
    if r == current_moves-1:
        single_moves_to_pos[pos[0]][pos[1]] = -3
        check.append(fix_pos(pos[0], pos[1]+1))

# print out maze with optimal path(s)
for row in single_moves_to_pos:
    for c in row:
        if c == -1:
            print('.', end='')
        elif c == -2:
            print('#', end='')
        elif c == -3:
            print('+', end='')
        elif c >= 10000:
            print('-', end='')
        elif c >= -1 and c < 10000:
            print(' ', end='')
    print()
print("Maze solved in " + str(opt) + " single moves")

# follow path forward through maze again to get input moves.
# input moves will do as many single moves as possible until the 
# current cube face changes or there are multiple legal next moves.
# input moves are also reletive to the current cube orientation.
# orientation changes when the current face changes and the cube rotates
input_moves = []
current_direction = 'u'
check = [ (39, 38) ]
while check != []:
    pos = check[0]
    check = check[1:]
    u = single_moves_to_pos[fix_pos(pos[0]-1, pos[1])[0]][fix_pos(pos[0]-1, pos[1])[1]]
    d = single_moves_to_pos[fix_pos(pos[0]+1, pos[1])[0]][fix_pos(pos[0]+1, pos[1])[1]]
    l = single_moves_to_pos[fix_pos(pos[0], pos[1]-1)[0]][fix_pos(pos[0], pos[1]-1)[1]]
    r = single_moves_to_pos[fix_pos(pos[0], pos[1]+1)[0]][fix_pos(pos[0], pos[1]+1)[1]]

    if u == -3:
        input_moves.append(input_dir('u'))
        current_face = face_of(pos[0], pos[1])
        npos = fix_pos(pos[0]-1, pos[1])
        turn1 = fix_pos(npos[0], npos[1]-1)
        turn2 = fix_pos(npos[0], npos[1]+1)
        while single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face == face_of(npos[0], npos[1]):
            pos = npos
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
            if not (maze[turn1[0]][turn1[1]] == '#' and maze[turn2[0]][turn2[1]] == '#'):
                break
            npos = fix_pos(pos[0]-1, pos[1])
            turn1 = fix_pos(npos[0], npos[1]-1)
            turn2 = fix_pos(npos[0], npos[1]+1)
        if single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face != face_of(npos[0], npos[1]):
            pos = npos
            update_dir(current_face, face_of(pos[0], pos[1]))
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
        check.append(pos)
    elif d == -3:
        input_moves.append(input_dir('d'))
        current_face = face_of(pos[0], pos[1])
        npos = fix_pos(pos[0]+1, pos[1])
        turn1 = fix_pos(npos[0], npos[1]-1)
        turn2 = fix_pos(npos[0], npos[1]+1)
        while single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face == face_of(npos[0], npos[1]):
            pos = npos
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
            if not (maze[turn1[0]][turn1[1]] == '#' and maze[turn2[0]][turn2[1]] == '#'):
                break
            npos = fix_pos(pos[0]+1, pos[1])
            turn1 = fix_pos(npos[0], npos[1]-1)
            turn2 = fix_pos(npos[0], npos[1]+1)
        if single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face != face_of(npos[0], npos[1]):
            pos = fix_pos(pos[0]+1, pos[1])
            update_dir(current_face, face_of(pos[0], pos[1]))
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
        check.append(pos)
    elif l == -3:
        input_moves.append(input_dir('l'))
        current_face = face_of(pos[0], pos[1])
        npos = fix_pos(pos[0], pos[1]-1)
        turn1 = fix_pos(npos[0]-1, npos[1])
        turn2 = fix_pos(npos[0]+1, npos[1])
        while single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face == face_of(npos[0], npos[1]):
            pos = fix_pos(pos[0], pos[1]-1)
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
            if not (maze[turn1[0]][turn1[1]] == '#' and maze[turn2[0]][turn2[1]] == '#'):
                break
            npos = fix_pos(pos[0], pos[1]-1)
            turn1 = fix_pos(npos[0]-1, npos[1])
            turn2 = fix_pos(npos[0]+1, npos[1])
        if single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face != face_of(npos[0], npos[1]):
            pos = fix_pos(pos[0], pos[1]-1)
            update_dir(current_face, face_of(pos[0], pos[1]))
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
        check.append(pos)
    elif r == -3:
        input_moves.append(input_dir('r'))
        current_face = face_of(pos[0], pos[1])
        npos = fix_pos(pos[0], pos[1]+1)
        turn1 = fix_pos(npos[0]-1, npos[1])
        turn2 = fix_pos(npos[0]+1, npos[1])
        while single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face == face_of(npos[0], npos[1]):
            pos = npos
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
            if not (maze[turn1[0]][turn1[1]] == '#' and maze[turn2[0]][turn2[1]] == '#'):
                break
            npos = fix_pos(pos[0], pos[1]+1)
            turn1 = fix_pos(npos[0]-1, npos[1])
            turn2 = fix_pos(npos[0]+1, npos[1])
        if single_moves_to_pos[npos[0]][npos[1]] == -3 and current_face != face_of(npos[0], npos[1]):
            pos = npos 
            update_dir(current_face, face_of(pos[0], pos[1]))
            current_face = face_of(pos[0], pos[1])
            single_moves_to_pos[pos[0]][pos[1]] = -4
        check.append(pos)

#print(input_moves)
binary = process("./maize")

# xor key from main
xor = [48, 134, 5, 236, 220, 149, 210, 101, 77, 220, 111, 68, 23, 186, 105, 81, 156, 66, 48, 0]
flag = "wctf{"

for i, d in enumerate(xor):
    dir_byte = 0
    for j in range(0, 4):
        if input_moves[(i*4)+j] == 'd':
            dir_byte = dir_byte | (0 << (2*j))
        if input_moves[(i*4)+j] == 'u':
            dir_byte = dir_byte | (1 << (2*j))
        if input_moves[(i*4)+j] == 'l':
            dir_byte = dir_byte | (2 << (2*j))
        if input_moves[(i*4)+j] == 'r':
            dir_byte = dir_byte | (3 << (2*j))
    flag += chr(d ^ dir_byte)
flag += "}\n"

binary.sendline(bytes(flag, 'ascii'))
print(flag)
print(binary.recvall())
