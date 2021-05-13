#imports modules needed
import pygame, time, random
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



#returns a new random shape(or the variable of the shape)
def new_shape():
      return shape_codes[random.randint(1,7)][0]



#creates a function to trim the shape of the arrays
def trim_shape(shape, rows, cols):
      #creates a row of zeros, finds all of the places where appears, gives an array of indexs, and then iterates through and deletes those rows
      r= np.array([0,0,0,0])
      for i in np.where(np.all(shape==r,axis=1)):
            shape = np.delete(shape, i, 0)
      

      #creates a np array of smaple row of 0(using the number of rows)
      #gives an array of indexs were that array appears, and deletes all those indexs
      c=np.zeros((1, shape.shape[0]), dtype='int8')
      for k in np.where(np.all(shape.T == c[0], axis=1)):
            shape = np.delete(shape, k, 1)
      
      
      #Updates the rows and cols to match the new shape
      dm = shape.shape
      cols[0] = cols[0] + ((cols[1]-cols[0]) - dm[1])
      rows[1] = rows[1] - ((rows[1]-rows[0]) - dm[0])
      return (shape, rows, cols)





#Checks to see if any rows are full(10 spaces are taken up) and clears the row, drops all the other pieces, and updates the grid
def clear_rows():
      global grid
      global new_grid
      global score
      cleared_rows = False
      for row in range(20):
            clear_row = True
            for col in range(10):
                  if grid[row][col] == 0:
                        clear_row = False
            if clear_row: 
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

def update_grid(shape, rows, cols):
      global new_grid
      global grid
      global shapes
      global upcoming_grid
      grid[rows[0]:rows[1], cols[0]:cols[1]] = shape
      check_top_row()
      if not clear_rows():
            new_grid = np.copy(grid)
      shapes.pop(0)
      shapes.append(new_shape())
      upcoming_grid = np.zeros((10,5), dtype='int8')



#Keeps the shapes in bounds and if the piece touches the bottom, it stops moving
def boundries(shape, rows, cols):
      if rows[1] ==20:
            rem_zero(shape, rows, cols)
            update_grid(shape, rows, cols)
            return True
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


def check_clear_space(shape, rows, cols):
      shape, rows, cols = trim_shape(shape, rows, cols)
      if rows[0]<0 or rows[1]>=20 or cols[0]<-1 or cols[1]>10:
            return False
      elif check_collision(shape, rows-1, cols):
            return False
      else:
            return True


def rem_zero(shape, rows, cols):
      global new_grid
      nrows, ncols = shape.shape
      for row in range(nrows):
            for col in range(ncols):
                  row = nrows -row-1
                  grow = rows[0] + row
                  gcol = cols[0] + col 
                  if shape[row][col] ==0:
                        shape[row][col] = new_grid[grow][gcol]
      return shape           
            



#Draws the shape that is being/can be moved
def draw_shape(shape, rows, cols, lgrid, collision = True):
      shape, rows, cols = trim_shape(shape, rows, cols)
      res = boundries(shape, rows, cols)
      res2= False
      if collision:
            res2 = check_collision(shape, rows, cols)
      shape = rem_zero(shape, rows, cols)
      if res is True:
            return True
      elif np.array_equiv(cols-1, res) or np.array_equiv(res, cols+1):
            lgrid[rows[0]:rows[1], res[0]:res[1]] = shape
            return False
      elif res2:
            update_grid(shape, rows, cols)
            return True
      else:
            lgrid[rows[0]:rows[1], cols[0]:cols[1]] = shape
            return False


def draw_grid(lgrid, dem, margin, cor):
      x,y = cor
      org_x = x
      nrows, ncols = lgrid.shape
      bsl = (dem[1] - (margin*nrows))/nrows
      for r in range(nrows):
            for c in range(ncols):
                  color = shape_codes[lgrid[r][c]][1]
                  pygame.draw.rect(win, color, (x,y, bsl, bsl), border_radius =2)
                  x += bsl+margin
            x =org_x
            y +=bsl+margin

#creates the grid onto the actual window by using the numpy array and the values
def create_screen():  
      global grid
      global upcoming_grid
      global shapes  
      x=.5
      y=0
      draw_grid(grid, (width,height), 1, (x,y))

      pygame.draw.rect(win, black, (width, 0, width_ex, height), border_radius = 2)

      score_text = game_font.render(f'Score: {score}', True, white)
      win.blit(score_text, (width ,0))
      
      upcoming_text = game_font.render(f'Upcoming', True, white)
      win.blit(upcoming_text, (width,int(height/7)))

      pygame.draw.rect(win, bkgrd_grey, (width, int(2/7 * height), width_ex, width_ex*2), border_radius = 2)
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
            over_score_text = game_font.render(f'Score: {score}', True, white)
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
      global run
      rows = np.array([0,4])
      cols = np.array([2,6])
      run = True
      rot = 0
      earlier =time.perf_counter()
      while run:   
            now = time.perf_counter()
            if now - earlier >=0.75:
                  rows +=1
                  earlier = now
            grid[:,:] = new_grid
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run=False
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                              if check_clear_space(shapes[0][rot], rows, cols-1):
                                    cols -= 1
                        if event.key == pygame.K_RIGHT:
                              if check_clear_space(shapes[0][rot], rows, cols+1):
                                    cols += 1
                        if event.key == pygame.K_UP:
                              numr, r,c = shapes[0].shape
                              if numr==1:
                                    pass
                              elif rot == numr-1:
                                    if check_clear_space(shapes[0][0], rows, cols):
                                          rot = 0
                              else:
                                    if check_clear_space(shapes[0][rot+1], rows, cols):
                                          rot += 1
                        if event.key == pygame.K_DOWN:
                              rows+=1
                              score+=1
                        if event.key == pygame.K_SPACE:
                              while not draw_shape(shapes[0][rot], rows, cols, grid):
                                    rows+=1
                                    score+=1
                                    grid= new_grid.copy()
                              rows = np.array([0,4])
                              cols = np.array([2,6])
                              rot = 0
     
            win.fill(bkgrd_grey)
            if draw_shape(shapes[0][rot], rows, cols, grid):
                  rows = np.array([0,4])
                  cols = np.array([2,6])
                  rot = 0
            create_screen()
            pygame.display.update()

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



#Defines the color, and shape for each number
shape_codes = {
            0:(None,bkgrd_black),
            1:(s, green),
            2:(z,red),
            3:(l,turquoise),
            4:(o, yellow),
            5:(j, blue),
            6:(L, orange),
            7:(t, purple)
      }



#Establishes some nesscary global varibables, like the grid and the score
score = 0
grid= np.zeros((20,10), dtype='int8')
new_grid = grid.copy()
upcoming_grid = np.zeros((10,5), dtype='int8')




#creates an intial 4 shapes to start off the game
shapes = [new_shape(), new_shape(), new_shape(), new_shape()]



#Initiates the window, sets window size and title, and calls the game loop
height = 600
width_ex = int(height* 1/4)
width = int(height* 1/2)
pygame.init()
game_font = pygame.font.Font(f"tetris/Tetris-Font/Tetris.ttf", int(0.08*width))
small_game_font=pygame.font.Font(f'tetris/Tetris-Font/Tetris.ttf', int(0.04*width))
win = pygame.display.set_mode((int(height/2 + width_ex), height))
pygame.display.set_caption("Tetris")
game_loop()
pygame.quit()