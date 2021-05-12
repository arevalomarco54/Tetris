#imports modules needed
import pygame
import time, random
from pygame.constants import K_RIGHT, K_SPACE
import numpy as np




#Establishes variables that hold the size and shape of the pieces in numpy arrays
s= np.array([
      [[0,0,1,1],
       [0,1,1,0],
       [0,0,0,0],
       [0,0,0,0]],
      [[0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [0,0,0,0]]
      ], dtype='int8')



z = np.array([
      [[0,2,2,0],
       [0,0,2,2],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,0,2],
       [0,0,2,2],
       [0,0,2,0],
       [0,0,0,0]]
], dtype='int8')



l = np.array([
      [[0,0,0,0],
       [0,0,0,0],
       [3,3,3,3],
       [0,0,0,0]],

      [[3,0,0,0],
       [3,0,0,0],
       [3,0,0,0],
       [3,0,0,0]]
], dtype='int8') 



o = np.array([
      [[0,0,4,4],
       [0,0,4,4],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,4,4],
      [0,0,4,4],
      [0,0,0,0],
      [0,0,0,0]]
], dtype='int8')



j = np.array([
      [[0,5,0,0],
       [0,5,5,5],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,5,5],
       [0,0,5,0],
       [0,0,5,0],
       [0,0,0,0]],

      [[0,5,5,5],
       [0,0,0,5],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,0,5],
       [0,0,0,5],
       [0,0,5,5],
       [0,0,0,0]]
], dtype='int8')



L = np.array([

      [[0,0,0,6],
       [0,6,6,6],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,6,6],
       [0,0,0,6],
       [0,0,0,6],
       [0,0,0,0]],

      [[0,6,6,6],
       [0,6,0,0],
       [0,0,0,0],
       [0,0,0,0]],

       [[0,0,6,0],
       [0,0,6,0],
       [0,0,6,6],
       [0,0,0,0]]
], dtype='int8')



t = np.array([
      [[0,7,7,7],
       [0,0,7,0],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,7,0],
       [0,0,7,7],
       [0,0,7,0],
       [0,0,0,0]],

      [[0,0,7,0],
       [0,7,7,7],
       [0,0,0,0],
       [0,0,0,0]],

      [[0,0,0,7],
       [0,0,7,7],
       [0,0,0,7],
       [0,0,0,0]]
], dtype='int8')





#assigns each number a shape, meaning if the randomly the number 1 is picked, it will be the s shape
def int_to_shape(int):
      if int == 1:
            return s
      if int ==2:
            return z
      if int == 3:
            return l
      if int == 4:
            return o
      if int == 5:
            return j
      if int == 6:
            return L
      if int == 7:
            return t




#returns a new random shape(or the variable of the shape)
def new_shape():
      return int_to_shape(random.randint(1,7))



#creates an intial 4 shapes to start off the game
shapes = [new_shape(), new_shape(), new_shape(), new_shape()]



#creates a function to trim the shape of the arrays
def trim_shape(shape):
      """#creates a row of zeros, finds all of the places where appears, gives an array of indexs, and then iterates through and deletes those rows
      r= np.array([0,0,0,0])
      result_r = np.where(np.all(shape==r,axis=1))
      for i in result_r:
            shape = np.delete(shape, i, 0)
      
      #creates a np array of smaple row of 0(using the number of rows)
      #gives an array of indexs were that array appears, and deletes all those indexs
      c=np.zeros((1, shape.shape[0]), dtype='int8')
      result_c = np.where(np.all(shape.T == c[0], axis=1))
      for k in result_c:
            shape = np.delete(shape, k, 1)
      return shape"""
      #Iterates through all the rows and deletes any that are all 0's
      for r in shape:
            num_rows, _ = shape.shape
            del_r = True
            
            for i in r:
                  if not i ==0:
                        del_r = False
            #finds the index of the row that needs to be delete
            if del_r:
                  result = 0
                  for i in range(num_rows):
                        if np.array_equiv(shape[i],r):
                              result = i
                  shape = np.delete(shape, result, 0)
            
      #Iterates through all the columns and deletes any that are all 0's
      for c in shape.T:
            num_rows, num_cols = shape.shape
            del_c = True
            for k in c:
                  if not k == 0:
                        del_c = False
            if del_c:
                  result =0
                  for i in range(num_cols):
                        if np.array_equiv(shape[:,i],c):
                              result = i
                  shape = np.delete(shape, result, 1)
      return shape




#Checks to see if any rows are full(10 spaces are taken up) and clears the row, drops all the other pieces, and updates the grid
def clear_rows():
      global grid
      global new_grid
      cleared_rows = False
      for row in range(20):
            clear_row = True
            for col in range(10):
                  if grid[row][col] == 0:
                        clear_row = False
            if clear_row:
                  global score
                  score =score +100
                  grid[row,:] = np.zeros((1,10), dtype='int8')
                  new_grid = np.zeros((20,10), dtype='int8')
                  for sub_row in range(row):
                        for col in range(10):
                              if not grid[sub_row][col] == 0:
                                    new_grid[sub_row+1][col] = grid[sub_row][col]
                  for bottom_row in range(row+1, 20):
                        for col in range(10):
                              new_grid[bottom_row][col] = grid[bottom_row][col]
                  grid = new_grid.copy()
      
      return cleared_rows

def new_grid1(shape, rows, cols):
      global new_grid
      global grid
      global shapes
      global upcoming_grid
      grid[rows[0]:rows[1], cols[0]:cols[1]] = shape
      check_top_row()
      res= clear_rows()
      if not res:
            new_grid = np.copy(grid)
      shapes.pop(0)
      shapes.append(new_shape())
      upcoming_grid = np.zeros((10,5), dtype='int8')



#Keeps the shapes in bounds and if the piece touches the bottom, it stops moving
def boundries(shape, rows, cols):
      if rows[1] ==20:
            rem_zero(shape, rows, cols)
            new_grid1(shape, rows, cols)
            return 'bottom'
      elif cols[1]>10:
            cols -=1
            return cols
      elif cols[0]< 0:
            cols+=1 
            return cols
      else:
            return False

      
 
#Checks Collision with other pieces and if it collides with another pieces, it stops and updates the grid      
def check_collision(shape, rows, cols ):
      nrows, ncols = shape.shape
      for row in range(nrows):
            for col in range(ncols):
                  row = nrows -row-1
                  grow = rows[0] + row + 1
                  gcol = cols[0] + col
                  if not grow == 20 and not gcol ==10:
                        if grid[grow][gcol] > 0:
                              if shape[row][col] == 0:
                                    pass
                              else:
                                    return True
      return False


def check_rotation(shape, rows, cols):
      shape = trim_shape(shape)
      dm = shape.shape
      cols[0] = cols[0] + ((cols[1]-cols[0]) - dm[1])
      rows[1] = rows[1] - ((rows[1]-rows[0]) - dm[0])
      if rows[0]<0 or rows[1]>=20 or cols[0]<-1 or cols[1]>10:
            return False
      elif check_collision(shape, rows-1, cols):
            return False
      else:
            return True

def check_side(shape, rows, cols):
      shape = trim_shape(shape)
      dm = shape.shape
      cols[0] = cols[0] + ((cols[1]-cols[0]) - dm[1])
      rows[1] = rows[1] - ((rows[1]-rows[0]) - dm[0])
      if check_collision(shape, rows-1, cols):
            return False
      else:
            return True

def rem_zero(shape, rows, cols):
      nrows, ncols = shape.shape
      for row in range(nrows):
            for col in range(ncols):
                  row = nrows -row-1
                  grow = rows[0] + row
                  gcol = cols[0] + col 
                  global new_grid
                  if shape[row][col] ==0:
                        shape[row][col] = new_grid[grow][gcol]

      return shape           
            



#Draws the shape that is being/can be moved
def draw_shape(shape1, rows, cols, ngrid, collision = True):
      shape = trim_shape(shape1)
      dm = shape.shape
      cols[0] = cols[0] + ((cols[1]-cols[0]) - dm[1])
      rows[1] = rows[1] - ((rows[1]-rows[0]) - dm[0])
      res = boundries(shape, rows, cols)
      res2= False
      if collision:
            res2 = check_collision(shape, rows, cols)
      shape = rem_zero(shape, rows, cols)
      if res == 'bottom':
            return True
      elif np.array_equiv(cols-1, res) or np.array_equiv(res, cols+1):
            ngrid[rows[0]:rows[1], res[0]:res[1]] = shape
            return False
      elif res2:
            new_grid1(shape, rows, cols)
            return True
      else:
            ngrid[rows[0]:rows[1], cols[0]:cols[1]] = shape
            return False


def draw_grid(sgrid, dem, margin, cor):
      x,y = cor
      org_x = x
      width, length = dem
      nrows, ncols = sgrid.shape
      bsl = (length - (margin*nrows))/nrows
      for r in range(nrows):
            for c in range(ncols):
                  color = bkgrd_black
                  if sgrid[r,c] == 1:
                        color = green
                  if sgrid[r,c] == 2:
                        color = red
                  if sgrid[r,c] == 3:
                        color = turquoise
                  if sgrid[r,c] == 4:
                        color = yellow
                  if sgrid[r,c] == 5:
                        color = blue
                  if sgrid[r,c] == 6:
                        color = orange
                  if sgrid[r,c] == 7:
                        color = purple
                  pygame.draw.rect(win, color, (x,y, bsl, bsl), border_radius =2)
                  x += bsl+margin
            x =org_x
            y +=bsl+margin

#creates the grid onto the actual window by using the numpy array and the values
def create_screen():    
      x=.5
      y=0
      global grid
      global shapes
      draw_grid(grid, (width,height), 1, (x,y))

      pygame.draw.rect(win, black, (width, 0, width_ex, height), border_radius = 2)
      
      score_text = game_font.render(f'Score:{score}', True, white)
      win.blit(score_text, (int(width+ .05*width),0))
      
      upcoming_text = game_font.render(f'Upcoming', True, white)
      win.blit(upcoming_text, (int(width+ .05*width),int(height/7)))
      pygame.draw.rect(win, bkgrd_grey, (width, int(2/7 * height), width_ex, width_ex*2), border_radius = 2)
      global upcoming_grid
      lrows = np.array([0,4])
      lcols= np.array([0,4])
      for i in range(1,len(shapes)):
            
            draw_shape(shapes[i][0],lrows, lcols, upcoming_grid, collision = False)
            lrows +=3

      draw_grid(upcoming_grid, (width_ex,int(width_ex*2)), 0.75, (width,int(2/7 * height)))

      


#Checks to see if the top row has any in the new grid, and then end the game if it does
def check_top_row():
      global new_grid
      top_row = new_grid[0]
      for i in top_row:
            if i>0:
                  game_over()
                  break



#shows game over screen and resets the game                  
def game_over():
      global grid
      global score
      global run
      global new_grid 
      global shapes  
      global upcoming_grid                     
      grid = np.zeros((20,10), dtype='int8')
      upcoming_grid = np.zeros((10,5), dtype='int8')
      shapes = [new_shape(), new_shape(), new_shape(), new_shape()]
      new_grid = grid.copy()
      wait =True
      while wait:
            mouse = pygame.mouse.get_pos()
            win.fill(bkgrd_grey)
            create_screen()
            quit_button_pos = (int(width* 1/5), int(height * 3/4),50,25)
            restart_button_pos = (int(width * 3/5),int(height *3/4),50,25)
            pygame.draw.rect(win, black, (int(width/10), int(height/10), int(width * 4/5), int(height*4/5)), border_radius = 4)
            pygame.draw.rect(win, red, quit_button_pos, border_radius = 2)
            pygame.draw.rect(win, purple, restart_button_pos, border_radius = 2 )
            game_over_text = game_font.render("Game Over!!!", True, white)
            over_score_text = game_font.render(f'Score:{score}', True, white)
            quit_text = small_game_font.render('Quit', True, white)
            restart_text = small_game_font.render('Restart', True, white)
            win.blit(game_over_text, (int(width * 1/5), int(height *1/5)))
            win.blit(over_score_text, (int(width *1/5), int(height * 2/5)))
            win.blit(quit_text, (quit_button_pos[0],quit_button_pos[1]))
            win.blit(restart_text, (restart_button_pos[0],restart_button_pos[1]))

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run=False
                        wait = False
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                              wait = False
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button_pos[0] <= mouse[0] <= quit_button_pos[0]+quit_button_pos[2] and quit_button_pos[1] <= mouse[1] <= quit_button_pos[1]+quit_button_pos[3]:
                              wait = False
                              run = False
                        if restart_button_pos[0] <= mouse[0] <= restart_button_pos[0]+restart_button_pos[2] and restart_button_pos[1] <= mouse[1] <= restart_button_pos[1]+restart_button_pos[3]:
                              wait = False
            pygame.display.update()
      score = 0
      


#defines the game loop, the function that runs over and over until the play loses
def game_loop():
      global grid
      global score
      global g_rows
      global g_cols
      g_rows = np.array([0,4])
      g_cols = np.array([2,6])
      global run
      run = True
      rot = 0
      earlier =time.perf_counter()
      while run:   
            now = time.perf_counter()
            if now - earlier >=0.75:
                  g_rows +=1
                  earlier = now
            grid[:,:] = new_grid
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run=False
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                              if check_side(shapes[0][rot], g_rows, g_cols-1):
                                    g_cols -= 1
                        if event.key == pygame.K_RIGHT:
                              if check_side(shapes[0][rot], g_rows, g_cols+1):
                                    g_cols += 1
                        if event.key == pygame.K_UP:
                              numr, r,c = shapes[0].shape
                              if numr==1:
                                    pass
                              elif rot == numr-1:
                                    if check_rotation(shapes[0][0], g_rows, g_cols):
                                          rot = 0
                              else:
                                    if check_rotation(shapes[0][rot+1], g_rows, g_cols):
                                          rot += 1
                        if event.key == pygame.K_DOWN:
                              g_rows+=1
                              score+=1
                        if event.key == pygame.K_SPACE:
                              while not draw_shape(shapes[0][rot], g_rows, g_cols, grid):
                                    g_rows+=1
                                    score+=1
                                    grid= new_grid.copy()
                              g_rows = np.array([0,4])
                              g_cols = np.array([2,6])
                              rot = 0
     
            win.fill(bkgrd_grey)
            if draw_shape(shapes[0][rot], g_rows, g_cols, grid):
                  g_rows = np.array([0,4])
                  g_cols = np.array([2,6])
                  rot = 0
            create_screen()
            pygame.display.update()


""""
******TO DO******


"""



#Defines tuples for the color of the pieces and background
black = (0,0,0)
bkgrd_black =(25, 25, 25)
white = (254,254,254)
turquoise =(175,238,238)
purple = (177, 156, 217)
orange = (255,140,0)
yellow = (255,255,0)
green = (0,254,0)
blue = (0,0,254)
red=(254,0,0)
bkgrd_grey = (54,54,54)



#Establishes some nesscary global varibables, like the grid and the score
score = 0
grid= np.zeros((20,10), dtype='int8')
new_grid = grid.copy()
upcoming_grid = np.zeros((10,5), dtype='int8')




#Initiates the window, sets window size and title, and calls the game loop
height = 500
width_ex = int(height/5)
width = int(height/2)
pygame.init()
game_font = pygame.font.Font(f"New_Tegomin/NewTegomin-Regular.ttf", int(0.04*height))
small_game_font=pygame.font.Font(f'New_Tegomin/NewTegomin-Regular.ttf', int(0.02*height))
win = pygame.display.set_mode((int(height/2 + width_ex), height))
pygame.display.set_caption("Tetris")
game_loop()
pygame.quit()