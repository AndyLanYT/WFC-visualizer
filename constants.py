from math import ceil, sqrt


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MAX_FIELD_WIDTH = 550
MAX_FIELD_HEIGHT = 550

OUTPUT_SIZE = 8, 8

UP = 0, -1
DOWN = 0, 1
LEFT = -1, 0
RIGHT = 1, 0
UP_LEFT = -1, -1
UP_RIGHT = 1, -1
DOWN_LEFT = -1, 1
DOWN_RIGHT = 1, 1

DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

SHEET_TILE_WIDTH = 252
SHEET_TILE_HEIGHT = 252
SHEET_GAP = 38

TILES_COUNT = 21
TILES_COUNT_IN_ROW = ceil(sqrt(TILES_COUNT))

TILE_GAP = 1
BLOCK_GAP = min(max(70 // max(OUTPUT_SIZE), 1), 10)

TILE_WIDTH = int(((MAX_FIELD_WIDTH - BLOCK_GAP * (max(OUTPUT_SIZE) - 1)) / max(OUTPUT_SIZE) + TILE_GAP) / TILES_COUNT_IN_ROW - TILE_GAP)
TILE_HEIGHT = TILE_WIDTH

BLOCK_WIDTH = TILES_COUNT_IN_ROW * (TILE_WIDTH + TILE_GAP) - TILE_GAP
BLOCK_HEIGHT = TILES_COUNT_IN_ROW * (TILE_HEIGHT + TILE_GAP) - TILE_GAP

FIELD_WIDTH = BLOCK_WIDTH * OUTPUT_SIZE[0] + BLOCK_GAP * (OUTPUT_SIZE[0] - 1)
FIELD_HEIGHT = BLOCK_HEIGHT * OUTPUT_SIZE[1] + BLOCK_GAP * (OUTPUT_SIZE[1] - 1)

SIDE_PAD = 30
TOP_PAD = (SCREEN_HEIGHT - FIELD_HEIGHT) // 2

FPS = 60

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40

TOGGLE_WIDTH = 45
TOGGLE_HEIGHT = 20
