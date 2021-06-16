#imports modules needed
import pygame, time, random
import numpy as np
import backbone as bc


#Initiates the window
pygame.init()



# colors/images
red = pygame.image.load(f'Sprites/red.png')
blue = pygame.image.load(f'Sprites/blue.png')
green = pygame.image.load(f'Sprites/green.png')
orange = pygame.image.load(f'Sprites/orange.png')
purple = pygame.image.load(f'Sprites/purple.png')
yellow = pygame.image.load(f'Sprites/yellow.png')
turquoise = pygame.image.load(f'Sprites/light_blue.png')
tetris = bc.Tetris(green, red, turquoise, yellow, blue, orange, purple)


#Draws the shape that is being/can be moved
def draw_shape(shape, rows, cols, lgrid, collision = True):
      shape, rows, cols = tetris.trim_shape(shape, rows, cols)
      res = tetris.boundries(shape, rows, cols)
      res2= False
      if collision:
            res2 = tetris.check_collision(shape, rows, cols)
      shape = tetris.rem_zero(shape, rows, cols)
      if np.array_equiv(cols-1, res) or np.array_equiv(res, cols+1):
            cols =  res
      if res is True:
            return True
      elif res2:
            tetris.update_grid(shape, rows, cols)
            return True
      else:
            lrows = rows.copy()
            nshape = shape.copy() +10 
            if lgrid is tetris.grid:
                  local_bottom = lrows[1] == 20
                  local_collided = tetris.check_collision(nshape, lrows, cols)
                  while not local_bottom and not local_collided:
                        lrows+=1
                        local_bottom = lrows[1] == 20
                        local_collided = tetris.check_collision(nshape, lrows, cols)
                  nshape = tetris.rem_zero(nshape, lrows, cols)
                  tetris.grid[lrows[0]:lrows[1], cols[0]:cols[1]] = nshape
            lgrid[rows[0]:rows[1], cols[0]:cols[1]] = shape
            return False


def draw_grid(lgrid, dem, margin, cor):
      x,y = cor
      org_x = x
      nrows, ncols = lgrid.shape
      bsl = int((dem[1] - (margin*nrows))/nrows)
      for r in range(nrows):
            for c in range(ncols):
                  yes= False
                  if lgrid[r][c]>10:
                        pygame.draw.rect(win, tetris.bkgrd_grey, (x,y, bsl, bsl), border_radius =2)
                        img = tetris.shape_codes[lgrid[r][c]-10][1]
                        yes= True
                  if lgrid[r][c] == 0 or lgrid[r][c]-10 == 0:
                        color = tetris.shape_codes[0][1]
                        pygame.draw.rect(win, color, (x,y, bsl, bsl), border_radius =2)
                  else:
                        
                        if yes is True:
                              img=pygame.transform.scale(img, (bsl, bsl))
                              win.blit(img, (x,y), None, pygame.BLEND_RGBA_MIN)
                        else:
                              img = tetris.shape_codes[lgrid[r][c]][1]
                              img=pygame.transform.scale(img, (bsl, bsl))
                              win.blit(img, (x,y))
                  x += bsl+margin
            x =org_x
            y +=bsl+margin

#creates the tetris.grid onto the actual window by using the numpy array and the values
def create_screen():  
      global shapes  
      x=.5
      y=0
      draw_grid(tetris.grid, (width,height), 1, (x,y))

      pygame.draw.rect(win, tetris.black, (width, 0, width_ex, height), border_radius = 2)

      score_text = game_font.render(f'Score:', True, tetris.white)
      score_score = game_font.render(f'{tetris.score}', True, tetris.white)
      win.blit(score_text, (width ,0))
      win.blit(score_score, (width, height*0.05))

      level_text = game_font.render(f'Level: {level}', True, tetris.white)
      win.blit(level_text, (width ,(int(2/7*height)+width_ex*2)))

      lines_text = game_font.render(f'Lines: {tetris.lines}', True, tetris.white)
      win.blit(lines_text, (width ,(int(2/7*height)+width_ex*2 +height*0.05)))
      
      upcoming_text = game_font.render(f'Upcoming', True, tetris.white)
      win.blit(upcoming_text, (width,int(height/7)))

      pygame.draw.rect(win, tetris.bkgrd_grey, (width, int(2/7 * height), width_ex, width_ex*2), border_radius = 2)
      lrows = np.array([0,4])
      lcols= np.array([0,4])
      for i in range(1,len(tetris.shapes)):
            
            draw_shape(tetris.shapes[i][0],lrows, lcols, tetris.upcoming_grid, collision = False)
            lrows +=3

      draw_grid(tetris.upcoming_grid, (width_ex,int(width_ex*2)), 1, (width,int(2/7 * height)))

      






#shows game over screen and resets the game                  
def game_over():
      global run            
      tetris.grid = np.zeros((20,10), dtype='int8')
      tetris.upcoming_grid = np.zeros((10,5), dtype='int8')
      tetris.shapes = [tetris.new_shape(), tetris.new_shape(), tetris.new_shape(), tetris.new_shape()]
      tetris.new_grid = tetris.grid.copy()
      wait =True
      while wait:
            mouse = pygame.mouse.get_pos()
            win.fill(tetris.bkgrd_grey)
            create_screen()
            quit_button_pos = (int(width* 1/5), int(height * 3/4),50,25)
            restart_button_pos = (int(width * 3/5),int(height *3/4),50,25)
            pygame.draw.rect(win, tetris.black, (int(width/10), int(height/10), int(width * 4/5), int(height*4/5)), border_radius = 4)
            pygame.draw.rect(win, tetris.bkgrd_black, quit_button_pos, border_radius = 2)
            pygame.draw.rect(win, tetris.bkgrd_black, restart_button_pos, border_radius = 2 )
            game_over_text = game_font.render("Game Over!!!", True, tetris.white)
            over_score_text = game_font.render(f'Score: {tetris.score}', True, tetris.white)
            quit_text = small_game_font.render('Quit', True, tetris.white)
            restart_text = small_game_font.render('Restart', True, tetris.white)
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
      tetris.score = 0
      


#defines the game loop, the function that runs over and over until the play loses
def game_loop():
      global run
      global level
      rows = np.array([0,4])
      cols = np.array([2,6])
      run = True
      rot = 0
      earlier =time.perf_counter()
      while run:   
            now = time.perf_counter()
            level = int(tetris.lines/10 + 1)
            if now - earlier >=0.80 - (level*0.05):
                  rows +=1
                  earlier = now
            tetris.grid[:,:] = tetris.new_grid
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run=False
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                              if tetris.check_clear_space(tetris.shapes[0][rot], rows, cols-1):
                                    cols -= 1
                        if event.key == pygame.K_RIGHT:
                              if tetris.check_clear_space(tetris.shapes[0][rot], rows, cols+1):
                                    cols += 1
                        if event.key == pygame.K_UP:
                              numr, r,c = tetris.shapes[0].shape
                              if numr==1:
                                    pass
                              elif rot == numr-1:
                                    if tetris.check_clear_space(tetris.shapes[0][0], rows, cols):
                                          rot = 0
                              else:
                                    if tetris.check_clear_space(tetris.shapes[0][rot+1], rows, cols):
                                          rot += 1
                        if event.key == pygame.K_DOWN:
                              rows+=1
                              tetris.score+=1
                        if event.key == pygame.K_SPACE:
                              while not draw_shape(tetris.shapes[0][rot], rows, cols, tetris.grid):
                                    rows+=1
                                    tetris.score+=1
                                    tetris.grid= tetris.new_grid.copy()
                              rows = np.array([0,4])
                              cols = np.array([2,6])
                              rot = 0
            
            win.fill(tetris.bkgrd_grey)
            if draw_shape(tetris.shapes[0][rot], rows, cols, tetris.grid):
                  rows = np.array([0,4])
                  cols = np.array([2,6])
                  rot = 0
            create_screen()
            pygame.display.update()






#defines fonts and dm
height = 600
width_ex = int(height* 1/5)
width = int(height* 1/2)
game_font = pygame.font.Font(f"Recursive/static/Recursive/Recursive-SemiBold.ttf", int(0.075*width))
small_game_font=pygame.font.Font(f'Recursive/static/Recursive/Recursive-SemiBold.ttf', int(0.04*width))
win = pygame.display.set_mode((int(width + width_ex), height))



#sets window size and title, and calls the game loop
pygame.display.set_caption("Tetris")
game_loop()
pygame.quit()