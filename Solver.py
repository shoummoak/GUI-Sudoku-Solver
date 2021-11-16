"""
Keywords:
. grid - the entire (9,3,3) matrix of numbers
. box - each of the 9 segments of the puzzle
. triplet - a row of 3 tiles/values of a box
. tile - a single cell conatiing just 1 value
. reserveds - all numbers which can not be put into a tile
. res - short for reserveds
. potentials - all the potentials values a tile could have
. pot - short for potential

"""

import numpy as np
import PotentialContainer as pc
import sys
import errors

sys.setrecursionlimit(pow(10, 6))

class Solver:


    
    def __init__(self, puzzle):
        
        # create the grid
        
#        self.grid = np.array(puzzle).reshape(9,3,3)
        self.grid = Solver.create_calculation_grid(puzzle)
        self.row_mapper, self.col_mapper = Solver.get_reserveds_container_mappers()
        
#        initialize potentials, reserveds, and tiles_indices containers
        self.initialize_reserveds_cotainers()
        
        self.initialize_potentials_containers()
        self.tiles_indices, self.tiles_indices_pointer, self.tiles_indices_size = self.initialize_indices_of_empty_tiles()
        
        
#       find initial reserveds and containers
#        also return True if it is a valid puzzle
        self.validity = self.find_initial_reserveds() 
        
#       if puzzle is invalid raise exception
        if not self.validity:
            raise errors.InvalidPuzzleException()
            
        self.find_initial_potentials()
        
#        start solving from the first tile of the first box
        self.solve(self.tiles_indices[self.tiles_indices_pointer])
        self.presentable_grid = self.create_presentable_grid()
                        

#. one big loop to gold the two smaller forward and backward loops together
#. when a tile finds a viable potential, it propagates farther forward
#. if no viable potential found, backprop is called

    
    def solve(self, tile_indices):
        
        grid_solved = False
        while True:
            
#            forward_propagation loop
            while True:
                
                pot_found = False
                pot_found = self.forward_propagate(tile_indices)
                
    
#                f_prop has found a pot, therefore we wil propagate forward agaain    
                if pot_found:
                    self.tiles_indices_pointer += 1
                    
                    # it is guaranteed the grid will be solved when tiles_indices_pointer
                    # reaches the value of the size of the tiles_indices container
                    if self.tiles_indices_pointer == self.tiles_indices_size:
                        grid_solved = True
                        break
                    
                    tile_indices = self.tiles_indices[self.tiles_indices_pointer]
                    continue
                
#                f_prop could not find any viable solution which means a previous tile 
#                value will need to be changed
                else:
                    self.tiles_indices_pointer -= 1
                    tile_indices = self.tiles_indices[self.tiles_indices_pointer]
                    break
            
#            this 'break' breaks the big While loop, finshing the solve function
            if grid_solved:
                break
            
#            backward_propagation loop
            while True:
                new_pot_found = False
                new_pot_found = self.backward_propagate(tile_indices)
                
#                if new_pot found to be viable, break this loops, and head to f_prop loop
                if new_pot_found:
                    self.tiles_indices_pointer += 1
                    tile_indices = self.tiles_indices[self.tiles_indices_pointer]
                    break
                
#                if no viable new_pot found, continue b_prop as there will need to be:
#                a value changed on a previous tile
                else:
                    self.tiles_indices_pointer -= 1
                    tile_indices = self.tiles_indices[self.tiles_indices_pointer]
                    continue
                

#. search through all the potentials from first to last
#. if any potential viable to be a possible solution, place it AND return True
#. if not found then return False
                     
    def forward_propagate(self, tile_indices):
        
        pc = self.potentials[tile_indices]  # pc short for PotentialContainer
        for i in range(pc.size):
            
            pc.pointer = i
            pot = pc.pots[pc.pointer]
#            if this potential is valid, place it
            if self.check_viability(tile_indices, pot):
                self.set_value(pot, tile_indices)
                return True

        return False
    

#. remove the current value from all the res_containers
#. search through all the potentials from its former value to last
#. if any potential viable to be a possible solution, place it AND return True
#. if not found then return False
                    
    def backward_propagate(self, tile_indices):        
        
#        remove the old pot from the reserveds and the tile itself
        self.remove_value(self.grid[tile_indices], tile_indices)
        
#        search for a viable solution between the old value and the last pot
        pc = self.potentials[tile_indices]
        for i in range(pc.pointer+1, pc.size):
            
            pc.pointer = i
            pot = pc.pots[pc.pointer]
            if self.check_viability(tile_indices, pot):
                self.set_value(pot, tile_indices)
                return True  
        
        return False
            
              
    def remove_value(self, pot, tile_indices):
        
        self.grid[tile_indices] = 0
        self.res_boxes[tile_indices[0]].remove(pot)
        self.res_rows[self.row_mapper[tile_indices]].remove(pot)
        self.res_cols[self.col_mapper[tile_indices]].remove(pot)
        
        
    def set_value(self, pot, tile_indices):
        
        self.grid[tile_indices] = pot
        self.res_boxes[tile_indices[0]].append(pot)
        self.res_rows[self.row_mapper[tile_indices]].append(pot)
        self.res_cols[self.col_mapper[tile_indices]].append(pot)
    
    
    def get_next_tile_indices(tile_indices_old):
        
        idx_bo, idx_tr, idx_ti = tile_indices_old
        if idx_ti == 2:
            if idx_tr == 2:
                return (idx_bo+1, 0, 0)
            else:
                return (idx_bo, idx_tr+1, 0)
        else:
            return (idx_bo, idx_tr, idx_ti+1)
        
        
    def get_prev_tile_indices(tile_indices_old):
        
        idx_bo, idx_tr, idx_ti = tile_indices_old
        if idx_ti == 0:
            if idx_tr == 0:
                return (idx_bo-1, 2, 2)
            else:
                return (idx_bo, idx_tr-1, 2)
        else:
            return (idx_bo, idx_tr, idx_ti-1)
        
    

    def check_viability(self, tile_indices, pot):
        
        idx_bo, idx_tr, idx_ti = tile_indices

        if pot in self.res_boxes[idx_bo]:
            return False
        
        elif pot in self.res_rows[self.row_mapper[tile_indices]]:
            return False
        
        elif pot in self.res_cols[self.col_mapper[tile_indices]]:
            return False
        
        else:
            return True
         
             
    
#   maps every tile/cell of the puzzle to its respective reserved row, col, and box 
    def get_reserveds_container_mappers():
        
        row_mapper = np.zeros((9,3,3), dtype = np.int32)
        row_mapper[0:3] = np.array([[0,0,0], [1,1,1], [2,2,2]])
        row_mapper[3:6] = np.array([[3,3,3], [4,4,4], [5,5,5]])
        row_mapper[6:9] = np.array([[6,6,6], [7,7,7], [8,8,8]])
        
        col_mapper = np.zeros((9,3,3), dtype = np.int32)
        template = np.array([[0]*9,[1]*9,[2]*9,[3]*9,[4]*9,[5]*9,[6]*9,[7]*9,[8]*9], dtype = np.int32).T
        col_mapper[0], col_mapper[3], col_mapper[6] = template[0:3, 0:3]
        col_mapper[1], col_mapper[4], col_mapper[7] = template[0:3, 3:6]
        col_mapper[2], col_mapper[5], col_mapper[8] = template[0:3, 6:9]
        
        return row_mapper, col_mapper
     

#    find the first sets of potentials of the tiles 
    def find_initial_potentials(self):
        
        row_mapper, col_mapper = Solver.get_reserveds_container_mappers()
        
        for idx_bo, box in enumerate(self.grid):
            for idx_tr, triplet in enumerate(box):
                for idx_ti, tile in enumerate(triplet):      
                    
                    if tile != 0: continue
                    for num in range(1,10):
                        if (
                            num not in self.res_boxes[idx_bo] 
                            and num not in self.res_rows[row_mapper[idx_bo, idx_tr, idx_ti]] 
                            and num not in self.res_cols[col_mapper[idx_bo, idx_tr, idx_ti]]
                            ):
                                self.potentials[(idx_bo, idx_tr, idx_ti)].append(num)

        for idx_bo, box in enumerate(self.grid):
            for idx_tr, triplet in enumerate(box):
                for idx_ti, tile in enumerate(triplet):
                    
                    self.potentials[(idx_bo, idx_tr, idx_ti)] = pc.PotentialContainer(self.potentials[(idx_bo, idx_tr, idx_ti)])
                    
    
#   fills in the reserveds containers
    def find_initial_reserveds(self):
        
        row_mapper, col_mapper = Solver.get_reserveds_container_mappers()
        duplicate_found = False
        
        for idx_bo, box in enumerate(self.grid):
            for idx_tr, triplet in enumerate(box):
                for idx_ti, tile in enumerate(triplet):
                                       
                    if tile == 0:
                        continue
                    else:
                        if tile in self.res_boxes[idx_bo] or tile in self.res_rows[row_mapper[idx_bo,idx_tr,idx_ti]] or tile in self.res_cols[col_mapper[idx_bo,idx_tr,idx_ti]]:
                            duplicate_found = True
                        self.res_boxes[idx_bo].append(tile)                        
                        self.res_rows[row_mapper[idx_bo,idx_tr,idx_ti]].append(tile)                        
                        self.res_cols[col_mapper[idx_bo,idx_tr,idx_ti]].append(tile)
        
#       returns True if puzzle's valid else False                
        return not duplicate_found


#   creates the containers to hold the reserved/forbitdden 
#   numbers across rows, cols, and boxes    
    def initialize_reserveds_cotainers(self):
        
        self.res_boxes = []
        self.res_rows = []
        self.res_cols = []
        
        for i in range(9):
            self.res_boxes.append([])
            self.res_cols.append([])
            self.res_rows.append([])
            
        
#    maps each tile to its respective potentials container
    def initialize_potentials_containers(self):
          
        self.potentials = {}
          
        for idx_bo, box in enumerate(self.grid):
            for idx_tr, triplet in enumerate(box):
                for idx_ti, tile in enumerate(triplet):
                    self.potentials[(idx_bo, idx_tr, idx_ti)] = []
                    
    def initialize_indices_of_empty_tiles(self):
        
        tiles_indices = []
        for idx_bo, box in enumerate(self.grid):
            for idx_tr, triplet in enumerate(box):
                for idx_ti, tile in enumerate(triplet):
                    tile_indices = (idx_bo, idx_tr, idx_ti)
                    if self.grid[tile_indices] == 0:
                        tiles_indices.append(tile_indices)
                        
        return tiles_indices, 0, len(tiles_indices)

    def create_calculation_grid(values):
        
        grid = []
        values = np.array(values)
        
        grid.append(values[:3, :3])
        grid.append(values[:3, 3:6])
        grid.append(values[:3, 6:9])
        grid.append(values[3:6, :3])
        grid.append(values[3:6, 3:6])
        grid.append(values[3:6, 6:9])
        grid.append(values[6:9, :3])
        grid.append(values[6:9, 3:6])
        grid.append(values[6:9, 6:9])
        
        return np.array(grid)
    
    
    def create_presentable_grid(self):  
        
        p_grid = []
        
        p_grid.append(self.grid[:3, 0, :])
        p_grid.append(self.grid[:3, 1, :])
        p_grid.append(self.grid[:3, 2, :])
        p_grid.append(self.grid[3:6, 0, :])
        p_grid.append(self.grid[3:6, 1, :])
        p_grid.append(self.grid[3:6, 2, :])
        p_grid.append(self.grid[6:9, 0, :])
        p_grid.append(self.grid[6:9, 1, :])
        p_grid.append(self.grid[6:9, 2, :])
        
        return np.array(p_grid).reshape(9,9).tolist()
    
    
    # Utility functions
    
    def print_grid(self):
        print("Grid:")
        for idx_triplet in range(3):
            print(self.grid[0:3, idx_triplet].reshape(9))
        print()
        for idx_triplet in range(3):
            print(self.grid[3:6, idx_triplet].reshape(9))
        print()
        for idx_triplet in range(3):
            print(self.grid[6:9, idx_triplet].reshape(9))
            
            
    def print_potentials(self):
        print("Tile Potentials:")
        for idx_bo, box in enumerate(self.grid):
            for idx_tr, triplet in enumerate(box):
                for idx_ti, tile in enumerate(triplet):
                    print("pots of tile ({}-{}-{}): {}".format(idx_bo, idx_tr, idx_ti, self.potentials[(idx_bo, idx_tr, idx_ti)]))
                   
        
    def print_res_boxes(self):
        print("res_boxes")
        for box in self.res_boxes:
            print("[", end = "")
            for reserved in box:
                print(" {}".format(reserved), end = "")
            print("]")
    
    
    def print_res_rows(self):
        print("res_rows")
        for row in self.res_rows:
            print("[", end = "")
            for reserved in row:
                print(" {}".format(reserved), end = "")
            print("]")
    
    
    def print_res_cols(self):
        print("res_cols")
        for col in self.res_cols:
            print("[", end = "")
            for reserved in col:
                print(" {}".format(reserved), end = "")
            print("]")
    
                        
    def print_line():
        print("\n--------------------------------------------------------------\n")                
                    
                    
                    
                    
                    
# test                   
#a = [[2,2,0,1,4,0,3,0,0],[0,0,0,8,0,3,0,5,9],[1,3,0,0,0,0,4,0,0],[0,4,0,0,5,0,0,3,0], [0,0,7,6,0,2,5,0,0],[0,8,0,0,7,0,0,9,0],[0,0,2,0,0,0,0,6,5],[4,5,0,2,0,6,0,0,0],[0,0,9,0,8,7,0,4,0]]                    
#a = Solver(a)
#a.print_grid()                
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    