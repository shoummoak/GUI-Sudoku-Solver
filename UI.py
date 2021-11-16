import pygame as pg
import sys
import Solver
import Button
from settings import *


# GRID GRAPHICS FUNCTIONS
def make_grid():
    y = 0
    for row in range(9):
        y += 50
        x = 0
        for col in range(9):
            x += 50
            tile = pg.Rect((x,y), (tile_size, tile_size))
            pg.draw.rect(screen, dull_purple, tile)
        
def draw_grid_lines():
    
    idx = 0 
    for width in range(50, 550, 50):
#        if else block to incorporate the thicker lines dividing the blocks
        if idx % 3 == 0:
#            vertical
            pg.draw.line(screen, yellow, (width, grid_pos), (width, grid_pos + grid_length), 5)
#            horizontal
            pg.draw.line(screen, yellow, (grid_pos, width), (grid_pos + grid_length, width), 5)             
        else:
            pg.draw.line(screen, yellow, (width, grid_pos), (width, grid_pos + grid_length), 2)
            pg.draw.line(screen, yellow, (grid_pos, width), (grid_pos + grid_length, width), 2)  
            
        idx += 1

# TILE SELECTION FUNCTIONS
    
def check_tile_selected():
    global tile_selected
    
    if (
        mouse_pos[0] < grid_pos or mouse_pos[0] > grid_pos + grid_length 
        or mouse_pos[1] <  grid_pos or mouse_pos[1] > grid_pos + grid_length
        ):
        tile_selected = None
    else:        
        row = int((mouse_pos[1] - grid_pos) / tile_size)
        col = int((mouse_pos[0] - grid_pos) / tile_size)
        tile_selected = (row, col)
        
def highlight_tile():    
    global tile_selected
    if tile_selected:
        pg.draw.rect(screen, light_purple, (tile_selected[1]*tile_size + grid_pos, tile_selected[0]*tile_size + grid_pos, tile_size, tile_size))
  
# NUMBER I/O FUNCTIONS
        
def update_grid(key):
    global grid_orig
    if tile_selected and key in [48,49,50,60,51,52,53,54,55,56,57]:
        grid_orig[tile_selected[0]][tile_selected[1]] = key-48
        grid_solved[tile_selected[0]][tile_selected[1]] = key-48
    if key == pg.K_BACKSPACE:
        grid_orig[tile_selected[0]][tile_selected[1]] = 0
        grid_solved[tile_selected[0]][tile_selected[1]] = 0              
        
def display_numbers():
    
    for y in range(9):
        for  x in range(9):
            orig_number = grid_orig[y][x]
            solved_number = grid_solved[y][x]
#            tile has not been sokved, therefore print nothing
            if orig_number == 0 and solved_number == 0:
                txt = ""
                text_obj = font.render(txt, True, yellow) 
            
#            tile has been solved therefore print in green
            elif orig_number == 0 and solved_number != 0:
                txt = str(solved_number)
                text_obj = font.render(txt, True, cyan)
                
#           tile is part of the puzzle, not a solution
            else:
                txt = str(solved_number)
                text_obj = font.render(txt, True, yellow) 
                      
            screen.blit(text_obj, (x*tile_size + grid_pos + 20, y*tile_size + grid_pos + 7))    


# BUTTON FUNCTIONS
def butt_clear_action():  
    global valid_puzzle
    if butt_clear.mouse_above_button(mouse_pos):
        valid_puzzle = True
        for idx_row, row in enumerate(grid_orig):
            for idx_col, col in enumerate(row):
                grid_orig[idx_row][idx_col] = 0
                grid_solved[idx_row][idx_col] = 0


def butt_solve_action():
    global grid_solved
    global valid_puzzle
    if butt_solve.mouse_above_button(mouse_pos):
        try:
            solved_obj = Solver.Solver(grid_orig)
        except:
            valid_puzzle = False
        else:
            valid_puzzle = True
            grid_solved = solved_obj.presentable_grid


def prompt_invalid_puzzle():
    
    if not valid_puzzle:
        orig_x = 525
        orig_y = 420
        pg.draw.rect(screen, orange, (orig_x-10, orig_y-2, 160+4, 80+4))
        pg.draw.rect(screen, dull_purple, (orig_x-8, orig_y, 160, 80))
        text_render1 = font_invalid.render("Invalid Puzzle due", True, orange)
        text_render2 = font_invalid.render("to duplication", True, orange)
        screen.blit(text_render1, (orig_x, orig_y+15))
        screen.blit(text_render2, (orig_x, orig_y+40))
    
    else:
        orig_x = 525
        orig_y = 420
        pg.draw.rect(screen, dull_purple, (orig_x-10, orig_y-2, 160+4, 80+4))        

def display_credit():
    font_credit = pg.font.SysFont("Monospace", 16)
    font_credit.set_bold(True)
    text_render = font_credit.render("by Shoummo Ahsan Khandoker", True, yellow)
    screen.blit(text_render, (10, screen_height-30))
        
        
pg.init()
clock = pg.time.Clock()


tile_selected = None
# test grids
#grid_orig = [[0,2,0,1,4,0,3,0,0],[0,0,0,8,0,3,0,5,9],[1,3,0,0,0,0,4,0,0],[0,4,0,0,5,0,0,3,0], [0,0,7,6,0,2,5,0,0],[0,8,0,0,7,0,0,9,0],[0,0,2,0,0,0,0,6,5],[4,5,0,2,0,6,0,0,0],[0,0,9,0,8,7,0,4,0]]
#grid_solved = [[0,2,0,1,4,0,3,0,0],[0,0,0,8,0,3,0,5,9],[1,3,0,0,0,0,4,0,0],[0,4,0,0,5,0,0,3,0], [0,0,7,6,0,2,5,0,0],[0,8,0,0,7,0,0,9,0],[0,0,2,0,0,0,0,6,5],[4,5,0,2,0,6,0,0,0],[0,0,9,0,8,7,0,4,0]]
grid_orig = [[0 for i in range(9)] for j in range(9)]
grid_solved = [[0 for i in range(9)] for j in range(9)]
mouse_pos = None
valid_puzzle = True
font = pg.font.SysFont("Times New Roman, Arial", tile_size-20)
font_invalid = pg.font.SysFont("Times New Roman, Arial", 20)
butt_solve = Button.Button(yellow, orange, (550, 50), 60, 30, "Solve")
butt_clear = Button.Button(yellow, orange, (550, 110), 60, 30, "Clear")


screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Sudoku Solver")


while True:
    
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
        
#        system exit
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
#        tile highlight
        if event.type == pg.MOUSEBUTTONDOWN:
            check_tile_selected()
            butt_clear_action()
            butt_solve_action()
            
#        number input
        if  event.type == pg.KEYDOWN:
            update_grid(event.key)
            
    
    screen.fill(dull_purple)
    make_grid()
    highlight_tile()
    draw_grid_lines()
    display_numbers()
    display_credit()
    
    butt_solve.render(screen)
    butt_solve.mouse_above_button(mouse_pos)
    
    butt_clear.render(screen)
    butt_clear.mouse_above_button(mouse_pos)
    
    prompt_invalid_puzzle()
    
    pg.display.update()
    clock.tick(fps)