import numpy as np
import time, random


      
class Tetris:
      sPiece = np.array([
            [[0,0,1,1],
            [0,1,1,0],
            [0,0,0,0],
            [0,0,0,0]],
            [[0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [0,0,0,0]]
            ], dtype='int8')



      zPiece = np.array([
            [[0,2,2,0],
            [0,0,2,2],
            [0,0,0,0],
            [0,0,0,0]],

            [[0,0,0,2],
            [0,0,2,2],
            [0,0,2,0],
            [0,0,0,0]]
      ], dtype='int8')



      lPiece = np.array([
            [[0,0,0,0],
            [0,0,0,0],
            [3,3,3,3],
            [0,0,0,0]],

            [[3,0,0,0],
            [3,0,0,0],
            [3,0,0,0],
            [3,0,0,0]]
      ], dtype='int8') 



      oPiece = np.array([
            [[0,0,4,4],
            [0,0,4,4],
            [0,0,0,0],
            [0,0,0,0]],

            [[0,0,4,4],
            [0,0,4,4],
            [0,0,0,0],
            [0,0,0,0]]
      ], dtype='int8')



      jPiece = np.array([
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



      LPiece = np.array([

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



      tPiece = np.array([
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
      
      black = (0,0,0)
      bkgrd_black =(25, 25, 25)
      white = (254,254,254)
      bkgrd_grey = (54,54,54)
      def new_shape(self):
            return self.shape_codes[random.randint(1,7)][0]
      def __init__(self, green,red, turquoise, yellow, blue, orange, purple ):
            #Defines the color, and shape for each number
            self.shape_codes = {
                        0:(None,self.bkgrd_black),
                        1:(self.sPiece, green.copy()),
                        2:(self.zPiece,red.copy()),
                        3:(self.lPiece,turquoise.copy()),
                        4:(self.oPiece, yellow.copy()),
                        5:(self.jPiece, blue.copy()),
                        6:(self.LPiece, orange.copy()),
                        7:(self.tPiece, purple.copy())
                  }
            self.shapes = [self.new_shape(), self.new_shape(), self.new_shape(), self.new_shape()] 

      


      



      #Establishes some nesscary global varibables, like the grid and the score
      score = 0
      level = 1
      lines=0
      grid= np.zeros((20,10), dtype='int8')
      new_grid = grid.copy()
      upcoming_grid = np.zeros((10,5), dtype='int8')



      #creates original 4 shapes      
      

     




            #creates a function to trim the shape of the arrays
      def trim_shape(self, shape, rows, cols):
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




      #Checks to see if any rows are full(10 spaces are taken up) and clears the row, drops all the other pieces, and updates the v.grid
      def clear_rows(self):
            for row in range(20):
                  clear_row = True
                  for col in range(10):
                        if self.grid[row][col] == 0:
                              clear_row = False
                  if clear_row: 
                        self.score +=100
                        self.lines +=1
                        self.grid[row,:] = np.zeros((1,10), dtype='int8')
                        self.new_grid = np.zeros((20,10), dtype='int8')
                        for sub_row in range(row):
                              for col in range(10):
                                    if not self.grid[sub_row][col] == 0:
                                          self.new_grid[sub_row+1][col] = self.grid[sub_row][col]
                        for bottom_row in range(row+1, 20):
                              for col in range(10):
                                    self.new_grid[bottom_row][col] = self.grid[bottom_row][col]
                        self.grid = np.copy(self.new_grid)
            



      def rem_zero(self, shape, rows, cols):
            nrows, ncols = shape.shape
            for row in range(nrows):
                  for col in range(ncols):
                        row = nrows -row-1
                        grow = rows[0] + row
                        gcol = cols[0] + col 
                        if shape[row][col] ==0 or shape[row][col] ==10:
                              shape[row][col] = self.new_grid[grow][gcol]
            return shape     




      #Checks Collision with other pieces and if it collides with another pieces, it stops and updates the v.grid      
      def check_collision(self, shape, rows, cols ):
            nrows, ncols = shape.shape
            for row in range(nrows):
                  for col in range(ncols):
                        row = nrows -row-1
                        grow = rows[0] + row + 1
                        gcol = cols[0] + col
                        if not grow == 20 and not gcol ==10:
                              if self.grid[grow][gcol] > 0:
                                    if shape[row][col] == 0 or shape[row][col] == 10:
                                          pass
                                    else:
                                          return True
            return False



      def check_clear_space(self, shape, rows, cols):
            shape, rows, cols = self.trim_shape(shape, rows, cols)
            if rows[0]<0 or rows[1]>=20 or cols[0]<-1 or cols[1]>10:
                  return False
            elif self.check_collision( shape, rows-1, cols):
                  return False
            else:
                  return True












      def update_grid(self, shape, rows, cols):
            self.grid[rows[0]:rows[1], cols[0]:cols[1]] = shape
            self.clear_rows()
            self.new_grid = np.copy(self.grid)
            self.shapes.pop(0)
            self.shapes.append(self.new_shape())
            self.upcoming_grid = np.zeros((10,5), dtype='int8')
            self.check_top_row()



      #Keeps the shapes in bounds and if the piece touches the bottom, it stops moving
      def boundries(self, shape, rows, cols):
            if rows[1] ==20:
                  shape = self.rem_zero(shape, rows, cols)
                  self.update_grid(shape, rows, cols)
                  return True
            elif cols[1]>10:
                  cols -=1
                  return cols
            elif cols[0]< 0:
                  cols+=1 
                  return cols
            else:
                  return False




#Checks to see if the top row has any in the new v.grid, and then end the game if it does
      def check_top_row(self):
            top_row = self.new_grid[0]
            for i in top_row:
                  if i>0:
                        return True





