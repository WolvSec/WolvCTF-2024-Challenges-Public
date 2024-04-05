#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIDE  26
#define MAZEW 3 * SIDE
#define MAZEH 4 * SIDE

char maze[MAZEH][MAZEW] = 
{
  "..........................#---###-#-------##########..........................",
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
  "..........................#####-####--##########-###.........................."
  };

unsigned int total_moves;

typedef enum Dir { UP, DOWN, NORTH, SOUTH, EAST, WEST } Dir;

/*   cube faces
 *      Ba
 *   L  T  R
 *      F
 *      Bo
 */

typedef enum Face { TOP, BOT, BACK, FRONT, RIGHT, LEFT } Face;
char* fnames[] = {"top", "bot", "back", "front", "right", "left"};

typedef enum Rot { U, D, L, R } Rot;

struct orientation {
  Dir x;
  Dir y;
  Dir z;
} cube_orienter;

struct loc {
  unsigned int row;
  unsigned int col;
} player_loc;

void init_maze() {
  cube_orienter.x = EAST;
  cube_orienter.y = NORTH;
  cube_orienter.z = UP;
  player_loc.row = 39;
  player_loc.col = 38;
  total_moves = 0;
}

bool has_axis(Dir d) {
  return (cube_orienter.x == d
       || cube_orienter.y == d
       || cube_orienter.z == d);
} 

void update_dirU(Dir *d) {
  switch (*d) {
    case UP:
      *d = NORTH;
      break;
    case DOWN:
      *d = SOUTH;
      break;
    case NORTH:
      *d = DOWN;
      break;
    case SOUTH:
      *d = UP;
      break;
    default:
      break;
  }
}

void update_dirD(Dir *d) {
  switch (*d) {
    case UP:
      *d = SOUTH;
      break;
    case DOWN:
      *d = NORTH;
      break;
    case NORTH:
      *d = UP;
      break;
    case SOUTH:
      *d = DOWN;
      break;
    default:
      break;
  }
}

void update_dirL(Dir *d) {
  switch (*d) {
    case UP:
      *d = WEST;
      break;
    case DOWN:
      *d = EAST;
      break;
    case EAST:
      *d = UP;
      break;
    case WEST:
      *d = DOWN;
      break;
    default:
      break;
  }
}

void update_dirR(Dir *d) {
  switch (*d) {
    case UP:
      *d = EAST;
      break;
    case DOWN:
      *d = WEST;
      break;
    case EAST:
      *d = DOWN;
      break;
    case WEST:
      *d = UP;
      break;
    default:
      break;
  }
}

void rotate(Rot r) {
  if (r == D)  {
    update_dirU(&(cube_orienter.x));
    update_dirU(&(cube_orienter.y));
    update_dirU(&(cube_orienter.z));
  } else if (r == U) {
    update_dirD(&(cube_orienter.x));
    update_dirD(&(cube_orienter.y));
    update_dirD(&(cube_orienter.z));
  } else if (r == R) {
    update_dirL(&(cube_orienter.x));
    update_dirL(&(cube_orienter.y));
    update_dirL(&(cube_orienter.z));
  } else if (r == L) {
    update_dirR(&(cube_orienter.x));
    update_dirR(&(cube_orienter.y));
    update_dirR(&(cube_orienter.z));
  } else exit(-1);

}

Face face_of(int row, int col) {
  if (row < SIDE) { return BACK; }
  else if (row < SIDE*2 && row >= SIDE && col < SIDE) { return LEFT; }
  else if (row < SIDE*2 && row >= SIDE && col >= SIDE && col < SIDE*2) { return TOP; }
  else if (row < SIDE*2 && row >= SIDE && col >= SIDE*2) { return RIGHT; }
  else if (row >= SIDE*2 && row < SIDE*3) { return FRONT; }
  else if (row >= SIDE*3) { return BOT; }
  else { exit(0); }
}

Face top_face() {
  if (cube_orienter.x == UP) {return RIGHT;}
  else if (cube_orienter.x == DOWN) {return LEFT;}
  else if (cube_orienter.y == UP) {return BACK;}
  else if (cube_orienter.y == DOWN) {return FRONT;}
  else if (cube_orienter.z == UP) {return TOP;}
  else if (cube_orienter.z == DOWN) {return BOT;}
  else exit(-1);
}

struct loc check(int row, int col) {
  int nrow = 0;
  int ncol = 0;
  if(row == -1) {
    //printf("back to bot\n");
    nrow = (SIDE*4)-1;
    ncol = col;
  } else if (col == -1) {
    //printf("left to bot\n");
    nrow = (SIDE*4)-(row-SIDE+1);
    ncol = SIDE;
  } else if (row == SIDE*4) {
    //printf("bot to back\n");
    nrow = 0;
    ncol = col;
  } else if (col == SIDE*3) {
    //printf("right to bot\n");
    nrow = (SIDE*4)-(row-SIDE+1);
    ncol = (SIDE*2)-1;
  } else if (row < SIDE && col == SIDE-1) {
    //printf("back to left\n");
    nrow = SIDE;
    ncol = row;
  } else if (row < SIDE && col == SIDE*2) {
    //printf("back to right\n");
    nrow = SIDE;
    ncol = (SIDE*3)-(row+1);
  } else if (row == SIDE-1 && col < SIDE) {
    //printf("left to back\n");
    nrow = col;
    ncol = SIDE;
  } else if (row == SIDE-1 && col >= SIDE*2) {
    //printf("right to back\n");
    nrow = (SIDE*3)-(col+1);
    ncol = (SIDE*2)-1;
  } else if (row == SIDE*2 && col < SIDE) {
    //printf("left to front\n");
    nrow = (SIDE*3)-(col+1);
    ncol = SIDE;
  } else if (row == SIDE*2 && col >= SIDE*2) {
    //printf("right to front\n");
    nrow = col;
    ncol = (SIDE*2)-1;
  } else if (row >= SIDE*2 && row < SIDE*3 && col == SIDE-1) {
    //printf("front to left\n");
    nrow = (SIDE*2)-1;
    ncol = (SIDE-1)-(row-(SIDE*2));
  } else if (row >= SIDE*2 && row < SIDE*3 && col == SIDE*2) {
    //printf("front to right\n");
    nrow = (SIDE*2)-1;
    ncol = row;
  } else if (row >= SIDE*3 && col == SIDE-1) {
    //printf("bot to left\n");
    nrow = SIDE+((SIDE*4)-(row+1));
    ncol = 0;
  } else if (row >= SIDE*3 && col == SIDE*2) {
    //printf("bot to right\n");
    nrow = SIDE+((SIDE*4)-(row+1));
    ncol = (SIDE*3)-1;
  } else {
    nrow = row;
    ncol = col;
  }
  struct loc ret;
  ret.row = nrow;
  ret.col = ncol;
  return ret;
}

void move(Rot r) {
  Dir d = NORTH;
  int target_row = 0;
  int target_col = 0;
  switch (top_face()) {
    case LEFT:
    case RIGHT:
      d = cube_orienter.y;
      break;
    case TOP:
    case BOT:
    case FRONT:
    case BACK:
      switch (cube_orienter.x) {
        case EAST:
          d = NORTH;
          break;
        case SOUTH:
          d = EAST;
          break;
        case WEST:
          d = SOUTH;
          break;
        case NORTH:
          d = WEST;
          break;
        default:
          exit(0);
      }
      break;
    default:
      exit(0);
  }
  switch (r) {
    case U:
      switch (d) {
        case NORTH:
          target_row = player_loc.row-1;
          target_col = player_loc.col;
          break;
        case SOUTH:
          target_row = player_loc.row+1;
          target_col = player_loc.col;
          break;
        case EAST:
          target_row = player_loc.row;
          target_col = player_loc.col-1;
          break;
        case WEST:
          target_row = player_loc.row;
          target_col = player_loc.col+1;
          break;
        default:
          exit(0);
      }
      break;
    case D:
      switch (d) {
        case NORTH:
          target_row = player_loc.row+1;
          target_col = player_loc.col;
          break;
        case SOUTH:
          target_row = player_loc.row-1;
          target_col = player_loc.col;
          break;
        case EAST:
          target_row = player_loc.row;
          target_col = player_loc.col+1;
          break;
        case WEST:
          target_row = player_loc.row;
          target_col = player_loc.col-1;
          break;
        default:
          exit(0);
      }
      break;
    case L:
      switch (d) {
        case NORTH:
          target_row = player_loc.row;
          target_col = player_loc.col-1;
          break;
        case SOUTH:
          target_row = player_loc.row;
          target_col = player_loc.col+1;
          break;
        case EAST:
          target_row = player_loc.row+1;
          target_col = player_loc.col;
          break;
        case WEST:
          target_row = player_loc.row-1;
          target_col = player_loc.col;
          break;
        default:
          exit(0);
      }
      break;
    case R:
      switch (d) {
        case NORTH:
          target_row = player_loc.row;
          target_col = player_loc.col+1;
          break;
        case SOUTH:
          target_row = player_loc.row;
          target_col = player_loc.col-1;
          break;
        case EAST:
          target_row = player_loc.row-1;
          target_col = player_loc.col;
          break;
        case WEST:
          target_row = player_loc.row+1;
          target_col = player_loc.col;
          break;
        default:
          exit(0);
      }
      break;
    default:
      exit(0);
  }
  struct loc resolved = check(target_row, target_col);
  //printf("%d, %d  to  ", player_loc.row, player_loc.col);
  //printf("%d, %d\n", resolved.row, resolved.col);
  if(maze[resolved.row][resolved.col] != '-') {
    return;
  }
  ++total_moves;
  if(face_of(player_loc.row, player_loc.col) != face_of(resolved.row ,resolved.col)) {
    maze[player_loc.row][player_loc.col] = '-';
    player_loc.row = resolved.row;
    player_loc.col = resolved.col;
    maze[player_loc.row][player_loc.col] = '*';
    rotate(r);
  } else if(target_row == player_loc.row) {
    struct loc turn1 = check(resolved.row+1, resolved.col);
    struct loc turn2 = check(resolved.row-1, resolved.col);
    maze[player_loc.row][player_loc.col] = '-';
    player_loc.row = resolved.row;
    player_loc.col = resolved.col;
    maze[player_loc.row][player_loc.col] = '*';
    if (maze[turn1.row][turn1.col] != '-' && maze[turn2.row][turn2.col] != '-') {
      move(r);
    } 
  } else if(target_col == player_loc.col) {
    struct loc turn1 = check(resolved.row, resolved.col+1);
    struct loc turn2 = check(resolved.row, resolved.col-1);
    maze[player_loc.row][player_loc.col] = '-';
    player_loc.row = resolved.row;
    player_loc.col = resolved.col;
    maze[player_loc.row][player_loc.col] = '*';
    if (maze[turn1.row][turn1.col] != '-' && maze[turn2.row][turn2.col] != '-') {
      move(r);
    }
  } else {
    exit(0);
  }
  
}

#ifdef DEBUG
void print_maze() {
  for (int row = 0; row < MAZEH; row++) {
    for (int col = 0; col < MAZEW; col++) {
      printf("%c", maze[row][col]);
    }
    printf("\n");
  }
}

void inc(int *x) { ++(*x); }
void dec(int *x) { --(*x); }

void print_face(Face f) {
  int row_offset = SIDE;
  int col_offset = SIDE;
  int rstart;
  int cstart;
  bool rowwise = true;
  void (*rfn) (int*);
  void (*cfn) (int*);
  switch (f) {
    case BOT:
      row_offset *= 3;
      if (cube_orienter.x == EAST) {
        rstart = row_offset;
        cstart = col_offset;
        rfn = inc;
        cfn = inc;
      } else if (cube_orienter.x == WEST) {
        rstart = row_offset+SIDE-1;
        cstart = col_offset+SIDE-1;
        rfn = dec;
        cfn = dec;
      } else if (cube_orienter.x == NORTH) {
        rowwise = false;
        rstart = row_offset;
        cstart = col_offset+SIDE-1;
        rfn = inc;
        cfn = dec;
      } else if (cube_orienter.x == SOUTH) {
        rowwise = false;
        rstart = row_offset+SIDE-1;
        cstart = col_offset;
        rfn = dec;
        cfn = inc;
      } 
      break;
    case FRONT:
      row_offset *= 2;
      if (cube_orienter.x == EAST) {
        rstart = row_offset;
        cstart = col_offset;
        rfn = inc;
        cfn = inc;
      } else if (cube_orienter.x == WEST) {
        rstart = row_offset+SIDE-1;
        cstart = col_offset+SIDE-1;
        rfn = dec;
        cfn = dec;
      } else if (cube_orienter.x == NORTH) {
        rowwise = false;
        rstart = row_offset;
        cstart = col_offset+SIDE-1;
        rfn = inc;
        cfn = dec;
      } else if (cube_orienter.x == SOUTH) {
        rowwise = false;
        rstart = row_offset+SIDE-1;
        cstart = col_offset;
        rfn = dec;
        cfn = inc;
      } 

      break;
    case BACK:
      row_offset = 0;
      if (cube_orienter.x == EAST) {
        rstart = row_offset;
        cstart = col_offset;
        rfn = inc;
        cfn = inc;
      } else if (cube_orienter.x == WEST) {
        rstart = row_offset+SIDE-1;
        cstart = col_offset+SIDE-1;
        rfn = dec;
        cfn = dec;
      } else if (cube_orienter.x == NORTH) {
        rowwise = false;
        rstart = row_offset;
        cstart = col_offset+SIDE-1;
        rfn = inc;
        cfn = dec;
      } else if (cube_orienter.x == SOUTH) {
        rowwise = false;
        rstart = row_offset+SIDE-1;
        cstart = col_offset;
        rfn = dec;
        cfn = inc;
      } 
      break;
    case LEFT:
      col_offset = 0;
      if (cube_orienter.y == NORTH) {
        rstart = row_offset;
        cstart = col_offset;
        rfn = inc;
        cfn = inc;
      } else if (cube_orienter.y == SOUTH) {
        rstart = row_offset+SIDE-1;
        cstart = col_offset+SIDE-1;
        rfn = dec;
        cfn = dec;
      } else if (cube_orienter.y == WEST) {
        rowwise = false;
        rstart = row_offset;
        cstart = col_offset+SIDE-1;
        rfn = inc;
        cfn = dec;
      } else if (cube_orienter.y == EAST) {
        rowwise = false;
        rstart = row_offset+SIDE-1;
        cstart = col_offset;
        rfn = dec;
        cfn = inc;
      } 
      break;
    case RIGHT:
      col_offset *= 2;
      if (cube_orienter.y == NORTH) {
        rstart = row_offset;
        cstart = col_offset;
        rfn = inc;
        cfn = inc;
      } else if (cube_orienter.y == SOUTH) {
        rstart = row_offset+SIDE-1;
        cstart = col_offset+SIDE-1;
        rfn = dec;
        cfn = dec;
      } else if (cube_orienter.y == WEST) {
        rowwise = false;
        rstart = row_offset;
        cstart = col_offset+SIDE-1;
        rfn = inc;
        cfn = dec;
      } else if (cube_orienter.y == EAST) {
        rowwise = false;
        rstart = row_offset+SIDE-1;
        cstart = col_offset;
        rfn = dec;
        cfn = inc;
      } 
      break;
    default:
      if (cube_orienter.x == EAST) {
        rstart = row_offset;
        cstart = col_offset;
        rfn = inc;
        cfn = inc;
      } else if (cube_orienter.x == WEST) {
        rstart = row_offset+SIDE-1;
        cstart = col_offset+SIDE-1;
        rfn = dec;
        cfn = dec;
      } else if (cube_orienter.x == NORTH) {
        rowwise = false;
        rstart = row_offset;
        cstart = col_offset+SIDE-1;
        rfn = inc;
        cfn = dec;
      } else if (cube_orienter.x == SOUTH) {
        rowwise = false;
        rstart = row_offset+SIDE-1;
        cstart = col_offset;
        rfn = dec;
        cfn = inc;
      } 
      break;
  }
  if (rowwise) {
    for (int row = rstart; row < rstart+SIDE && row > rstart-SIDE; rfn(&row)) {
      for (int col = cstart; col < cstart+SIDE && col > cstart-SIDE; cfn(&col)) {
        printf("%c", maze[row][col]);
      }
      printf("\n");
    }
  } else {
    for (int col = cstart; col < cstart+SIDE && col > cstart-SIDE; cfn(&col)) {
      for (int row = rstart; row < rstart+SIDE && row > rstart-SIDE; rfn(&row)) {
        printf("%c", maze[row][col]);
      }
      printf("\n");
    }
  }
}
#endif

int main(int argc, char **argv) {
  init_maze();
  char in[32];
  int xarr[20] = { 48, 134, 5, 236, 220, 149, 210, 101, 77, 220, 111, 68, 23, 186, 105, 81, 156, 66, 48, 0 };
  printf("flag: ");
  scanf("%31s", in);
  if(strncmp(in, "wctf{", 5)) {
    printf("No, not that, I need a FLAG.\n");
    exit(0);
  }
  for (int i = 0; i < 20; ++i) {
    in[i+5] = (in[i+5] ^ xarr[i]);
  }
  int i = 5;
  while (in[i] != '}' && in[i] != 0) {
    char op = in[i];
    for (int j = 0; j < 4; ++j) {
      //printf("%d, %d\n", player_loc.row, player_loc.col);
      switch ((op >> (j*2)) & 3) {
        case 0:
          #ifdef DEBUG
          printf("Down\n");
          #endif
          move(D);
          break;
        case 1:
          #ifdef DEBUG
          printf("Up\n");
          #endif
          move(U);
          break;
        case 2:
          #ifdef DEBUG
          printf("Left\n");
          #endif
          move(L);
          break;
        case 3:
          #ifdef DEBUG
          printf("Right\n");
          #endif
          move(R);
          break;
        default:
          exit(0);
      }
      #ifdef DEBUG
      print_face(top_face());
      #endif
      if(player_loc.row == 90 && player_loc.col == 38) { break; }
    }
    ++i;
  }
  #ifdef DEBUG
  print_maze();
  printf("moves: %d\n", total_moves);
  #endif
  if(player_loc.row == 90 && player_loc.col == 38 && total_moves == 223) {
    printf("Success.\n");
  } else {
    printf("better luck next time\n");
  }
  return 0;
}
