import pygame
from abc import ABC
import random
from math import ceil, sqrt, log


pygame.init()
pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MAX_FIELD_WIDTH = 550
MAX_FIELD_HEIGHT = 550

OUTPUT_SIZE = 15, 15

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

BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREY = 64, 64, 64
DARK_BLUE = 48, 32, 128
DARK_RED = 128, 0, 0
DARK_GREEN = 0, 128, 0

FONT = pygame.font.SysFont(None, 30)


class IRenderable(ABC):
    def render(self, screen, *args, **kwargs):
        pass


class IClickable(ABC):
    def check_click(self):
        pass


class Tilesheet:
    def __init__(self, filename):
        try:
            self.__sheet = pygame.image.load(filename)
        except FileNotFoundError:
            raise SystemExit(f'File {filename} does not exist')
        
        self.__tile_images = []
        for i in range(TILES_COUNT):
            x = i % 7 * (SHEET_TILE_WIDTH + SHEET_GAP)
            y = i // 7 * (SHEET_TILE_HEIGHT + SHEET_GAP)

            tile_image = self.__get_tile_image(x, y, SHEET_TILE_WIDTH, SHEET_TILE_HEIGHT)
            self.__tile_images.append(tile_image)

    def __get_tile_image(self, x, y, width, height):
        return self.__sheet.subsurface((x, y, width, height))

    @property
    def tile_images(self):
        return self.__tile_images


class Tile(IRenderable):
    COUNT = 0

    def __init__(self, image):
        self.__image = image

        image = pygame.transform.scale(image, (20, 20))
        pixelset = []
        for j in range(image.get_height()):
            pixelset.append([])
            for i in range(image.get_width()):
                pixel = image.get_at((i, j))
                pixelset[j].append(pixel)
        
        self.__pixelset = pixelset
        self.__idx = Tile.COUNT % TILES_COUNT

        Tile.COUNT += 1
    
    def edge_pixels(self, direction):
        if direction == UP:
            return self.pixelset[0]
        elif direction == DOWN:
            return self.pixelset[-1]
        elif direction == LEFT:
            return list(map(lambda x: x[0], self.__pixelset))
        elif direction == RIGHT:
            return list(map(lambda x: x[-1], self.__pixelset))
        elif direction == UP_LEFT:
            return [self.pixelset[0][0]]
        elif direction == UP_RIGHT:
            return [self.pixelset[0][-1]]
        elif direction == DOWN_LEFT:
            return [self.pixelset[-1][0]]
        elif direction == DOWN_RIGHT:
            return [self.pixelset[-1][-1]]
    
    def render(self, screen, *args, **kwargs):
        x, y, size = args

        image = pygame.transform.scale(self.__image, size)
        
        if not kwargs['is_single']:
            rect = image.get_rect(x=x, y=y)

            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos):
                surf = pygame.Surface(size, pygame.SRCALPHA)
                surf.fill((*BLACK, 128))
                
                image.blit(surf, (0, 0))
        
        screen.blit(image, (x, y))
    
    @property
    def image(self):
        return self.__image

    @property
    def pixelset(self):
        return self.__pixelset

    @property
    def idx(self):
        return self.__idx
    
    def __eq__(self, other):
        return self.pixelset == other.pixelset
    
    def __hash__(self):
        return hash(tuple(map(lambda x: tuple(x), self.pixelset)))

    def __repr__(self):
        return f'{self.idx}'


class Block(IRenderable):
    def __init__(self, tileset, x, y):
        self.__tiles = tileset
        
        self.__x = x + SIDE_PAD
        self.__y = y + TOP_PAD
    
    def set_random_tile(self, probabilities):
        self.tiles = random.choices(self.__tiles, [probabilities[tile.idx] for tile in self.__tiles])

    @property
    def tiles(self):
        return self.__tiles
    
    @tiles.setter
    def tiles(self, val):
        if isinstance(val, Tile):
            self.__tiles = [val]
        elif isinstance(val, list):
            self.__tiles = val
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def render(self, screen):
        if len(self.__tiles) == 1:
            for tile in self.__tiles:
                x = self.__x
                y = self.__y
                size = BLOCK_WIDTH, BLOCK_HEIGHT
                tile.render(screen, x, y, size, is_single=True)

        else:
            for tile in self.__tiles:
                x = self.__x + tile.idx % TILES_COUNT_IN_ROW * (TILE_WIDTH + TILE_GAP)
                y = self.__y + tile.idx // TILES_COUNT_IN_ROW * (TILE_HEIGHT + TILE_GAP)
                size = TILE_WIDTH, TILE_HEIGHT

                tile.render(screen, x, y, size, is_single=False)
    
    def __getitem__(self, key):
        for tile in self.__tiles:
            if tile.idx == key:
                return tile
    
    def __setitem__(self, key, val):
        self.__tiles[key] = val
    
    def __len__(self):
        return len(self.__tiles)
    
    def __contains__(self, key):
        if isinstance(key, Tile):
            return key in self.__tiles
        elif isinstance(key, int):
            return key in map(lambda tile: tile.idx, self.__tiles)
    
    def __eq__(self, other):
        return self.__tiles == other.tiles
    
    def __iter__(self):
        return iter(self.__tiles)

    def __repr__(self):
        return str(self.__tiles)


class Index:
    def __init__(self, tileset):
        self.__rules = {}
        for tile in tileset:
            self.__rules[tile.idx] = {}
            
            for direction in DIRECTIONS:
                self.__rules[tile.idx][direction] = []
                
                for neighbor in tileset:
                    if self.__is_similar(tile, neighbor, direction):
                        self.__rules[tile.idx][direction].append(neighbor.idx)
    
    def __is_similar(self, tile, neighbor, direction, k=0.8):
        opposite_direction = -direction[0], -direction[1]
        
        tile_pixels = tile.edge_pixels(direction)
        neighbor_pixels = neighbor.edge_pixels(opposite_direction)

        lst = list(map(lambda idx: tile_pixels[idx] == neighbor_pixels[idx], range(len(tile_pixels))))

        return lst.count(True) / len(lst) >= k
    
    def is_possible_neighbor(self, tile, neighbor, direction):
        return neighbor.idx in self.__rules[tile.idx][direction]


class WaveFunction(IRenderable):
    def __init__(self, tile_images):
        self.size = OUTPUT_SIZE
        
        self.__coeffs = []
        for i in range(self.size[1]):
            self.__coeffs.append([])
            for j in range(self.size[0]):
                tileset = list(map(Tile, tile_images))

                x = j * (BLOCK_WIDTH + BLOCK_GAP)
                y = i * (BLOCK_HEIGHT + BLOCK_GAP)
                
                block = Block(tileset, x, y)
                self.__coeffs[i].append(block)
        
        self.__tileset = list(map(Tile, tile_images))
        self.probabilities = {tile.idx: 1 / len(tileset) for tile in tileset}
        self.index = Index(tileset)
        self.__stack = []
    
    def __entropy(self, pos):
        if len(self.block_at_pos(pos)) == 1:
            return 0
        
        return -sum([self.probabilities[tile.idx] * log(self.probabilities[tile.idx], 2) for tile in self.__tileset if tile is not None]) - random.uniform(0, 0.1)
    
    def __min_entropy_pos(self):
        min_entropy = None
        pos = None

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                entropy = self.__entropy((x, y))

                if entropy != 0 and (min_entropy is None or min_entropy > entropy):
                    min_entropy = entropy
                    pos = x, y
        
        return pos
    
    def __valid_directions(self, pos):
        x, y = pos

        directions = []
        if x == 0:
            directions += [RIGHT]

            if y == 0:
                directions += [DOWN, DOWN_RIGHT]
            elif y == self.size[1] - 1:
                directions += [UP, UP_RIGHT]
            else:
                directions += [DOWN, DOWN_RIGHT, UP, UP_RIGHT]
        elif x == self.size[0] - 1:
            directions += [LEFT]

            if y == 0:
                directions += [DOWN, DOWN_LEFT]
            elif y == self.size[1] - 1:
                directions += [UP, UP_LEFT]
            else:
                directions += [DOWN, DOWN_LEFT, UP, UP_LEFT]
        else:
            directions += [LEFT, RIGHT]

            if y == 0:
                directions += [DOWN, DOWN_LEFT, DOWN_RIGHT]
            elif y == self.size[1] - 1:
                directions += [UP, UP_LEFT, UP_RIGHT]
            else:
                directions += [DOWN, DOWN_LEFT, DOWN_RIGHT, UP, UP_LEFT, UP_RIGHT]

        return directions
    
    def is_collapsed(self):
        for row in self.__coeffs:
            for block in row:
                if len(block) > 1:
                    return False
        
        return True
    
    def block_at_pos(self, pos):
        col, row = pos
        return self.__coeffs[row][col]
    
    def __observe(self):
        pos = self.__min_entropy_pos()
        if pos is None:
            return
        
        block = self.block_at_pos(pos)
        block.set_random_tile(self.probabilities)

        self.add_to_stack(pos)
    
    def propagate(self):
        while len(self.__stack) != 0:
            pos = self.__stack.pop()
            block = self.block_at_pos(pos)

            for direction in self.__valid_directions(pos):
                adjacent_pos = pos[0] + direction[0], pos[1] + direction[1]
                adjacent_block = self.block_at_pos(adjacent_pos)

                is_changed = False
                for neighbor in adjacent_block.tiles[:]:
                    if len(adjacent_block) == 1:
                        break
                    
                    if True not in [self.index.is_possible_neighbor(tile, neighbor, direction) for tile in block]:
                        adjacent_block.tiles.remove(neighbor)
                        is_changed = True

                        yield

                if is_changed:
                    self.add_to_stack(adjacent_pos)

    def add_to_stack(self, pos):
        self.__stack.append(pos)
    
    def collapse(self):
        while not self.is_collapsed():
            propagate_gen = self.propagate()
            propagation = True
            
            while propagation:
                try:
                    next(propagate_gen)
                    yield
                except StopIteration:
                    propagation = False

            self.__observe()
            yield
    
    def render(self, screen, *args, **kwargs):
        for row in self.__coeffs:
            for block in row:
                block.render(screen)
            
    def renovate(self):
        tile_images = list(map(lambda tile: tile.image, self.__tileset))
        
        self.__coeffs = []
        for i in range(self.size[1]):
            self.__coeffs.append([])
            for j in range(self.size[0]):
                tileset = list(map(Tile, tile_images))

                x = j * (BLOCK_WIDTH + BLOCK_GAP)
                y = i * (BLOCK_HEIGHT + BLOCK_GAP)
                
                block = Block(tileset, x, y)
                self.__coeffs[i].append(block)

    @property
    def coeffs(self):
        return self.__coeffs


class Button(IRenderable, IClickable):
    def __init__(self, text, pos, width=BUTTON_WIDTH, height=BUTTON_HEIGHT):
        self.__is_pressed = False

        elevation = int(0.14 * height)
        self.__elevation = elevation
        self.__dynamic_elevation = elevation
        self.__y = pos[1]

        self.__bottom_rect = pygame.Rect(pos, (width, height + elevation))
        self.__bottom_color = BLACK

        self.__top_rect = pygame.Rect(pos, (width, height))
        self.__top_color = DARK_BLUE

        self.__text_surf = FONT.render(text, True, WHITE)
        self.__text_rect = self.__text_surf.get_rect(center=self.__top_rect.center)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.__top_rect.collidepoint(mouse_pos):
            self.__top_color = DARK_RED
            
            if pygame.mouse.get_pressed()[0]:
                self.__is_pressed = True
                self.__dynamic_elevation = 0
            else:
                if self.__is_pressed:
                    self.__is_pressed = False
                    self.__dynamic_elevation = self.__elevation
                    
                    return True
        else:
            self.__top_color = DARK_BLUE
            self.__dynamic_elevation = self.__elevation

    def render(self, screen, *args, **kwargs):
        self.__top_rect.y = self.__y - self.__dynamic_elevation
        self.__text_rect.center = self.__top_rect.center

        self.__bottom_rect.y = self.__top_rect.y
        self.__bottom_rect.height = self.__top_rect.height + self.__dynamic_elevation

        pygame.draw.rect(screen, self.__bottom_color, self.__bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.__top_color, self.__top_rect, border_radius=12)
        screen.blit(self.__text_surf, self.__text_rect)


class Toggle(IRenderable, IClickable):
    def __init__(self, pos, width=TOGGLE_WIDTH, height=TOGGLE_HEIGHT):
        self.__is_pressed = False
        self.__status = True

        self.__bottom_rect = pygame.Rect(pos, (width, height))

        top_height = int(0.9 * height)
        top_width = top_height
        top_y = pos[1] + (height - top_height) // 2
        self.__top_rect = pygame.Rect((pos[0], top_y), (top_width, top_height))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.__bottom_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.__is_pressed = True
            else:
                if self.__is_pressed:
                    self.__is_pressed = False
                    self.__status = not self.__status

                    return True
    
    def render(self, screen, *args, **kwargs):
        pygame.draw.rect(screen, BLACK, self.__bottom_rect, border_radius=self.__bottom_rect.height // 2)
        
        if self.__status:
            self.__top_rect.x = self.__bottom_rect.x + self.__bottom_rect.width - self.__top_rect.width - (self.__bottom_rect.height - self.__top_rect.height) // 2
            pygame.draw.rect(screen, DARK_GREEN, self.__top_rect, border_radius=self.__top_rect.height // 2)
        else:
            self.__top_rect.x = self.__bottom_rect.x + (self.__bottom_rect.height - self.__top_rect.height) // 2
            pygame.draw.rect(screen, DARK_RED, self.__top_rect, border_radius=self.__top_rect.height // 2)


class Visualizer:
    def __init__(self):
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('WFC visualizer')
        
        self.__clock = pygame.time.Clock()

        tilesheet = Tilesheet('smth/assets/tileset1.png')
        self.__wave_function = WaveFunction(tilesheet.tile_images)

        self.__collapse_button = Button('Collapse', (595, 150))
        self.__renovate_button = Button('Renovate', (595, 210))
        self.__save_button = Button('Save', (595, 270))
        self.__propagation_toggle = Toggle((595, 330))

        self.__to_propagate = True
        self.__start = False

        self.__runner = True

    def get_col_row_idx(self, mouse_pos):
        col, row, idx = None, None, None

        mouse_x, mouse_y = mouse_pos
        if SIDE_PAD <= mouse_x <= SIDE_PAD + FIELD_WIDTH and TOP_PAD <= mouse_y <= TOP_PAD + FIELD_HEIGHT:
            col = (mouse_x - SIDE_PAD) // (BLOCK_WIDTH + BLOCK_GAP)
            row = (mouse_y - TOP_PAD) // (BLOCK_HEIGHT + BLOCK_GAP)

            block = self.__wave_function.coeffs[row][col]
            if block.x <= mouse_x <= block.x + BLOCK_WIDTH and block.y <= mouse_y <= block.y + BLOCK_HEIGHT:
                x = (mouse_x - SIDE_PAD) % (BLOCK_WIDTH + BLOCK_GAP) // (TILE_WIDTH + TILE_GAP)
                y = (mouse_y - TOP_PAD) % (BLOCK_HEIGHT + BLOCK_GAP) // (TILE_HEIGHT + TILE_GAP)

                idx = y * TILES_COUNT_IN_ROW + x

        return col, row, idx
    
    def check_clicked_tile(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()

            col, row, idx = self.get_col_row_idx(mouse_pos)
            if idx is not None:
                block = self.__wave_function.coeffs[row][col]

                if len(block) != 1 and idx in block:
                    tile = block[idx]
                    block.tiles = tile
                    self.__wave_function.add_to_stack((col, row))
                    
                    return self.__to_propagate
    
    def image(self):
        image = pygame.Surface((SHEET_TILE_WIDTH * OUTPUT_SIZE[0], SHEET_TILE_HEIGHT * OUTPUT_SIZE[1]))

        for i, row in enumerate(self.__wave_function.coeffs):
            for j, block in enumerate(row):
                image.blit(block.tiles[0].image, (SHEET_TILE_WIDTH * j, SHEET_TILE_HEIGHT * i))

        return image
    
    def save_image(self, filename):
        image = self.image()
        pygame.image.save(image, f'{filename}.png')
    
    def render(self):
        self.__screen.fill(DARK_GREY)
        self.__wave_function.render(self.__screen)
        self.__collapse_button.render(self.__screen)
        self.__renovate_button.render(self.__screen)
        self.__save_button.render(self.__screen)
        self.__propagation_toggle.render(self.__screen)
        
        pygame.display.flip()

    def run(self):
        while self.__runner:
            # self.__clock.tick(FPS)

            if self.__start:
                try:
                    next(collapse_gen)
                except StopIteration:
                    self.__start = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__runner = False
                
                elif event.type == pygame.KEYDOWN and not self.__start:
                    if event.key == pygame.K_c:
                        collapse_gen = self.__wave_function.collapse()
                        self.__start = True
                    
                    elif event.key == pygame.K_r:
                        self.__wave_function.renovate()
                    
                    elif event.key == pygame.K_p:
                        self.__to_propagate = not self.__to_propagate
            
            if not self.__start:
                if self.check_clicked_tile():
                    collapse_gen = self.__wave_function.propagate()
                    self.__start = True

                if self.__collapse_button.check_click():
                    collapse_gen = self.__wave_function.collapse()
                    self.__start = True

                if self.__renovate_button.check_click():
                    self.__wave_function.renovate()

                if self.__wave_function.is_collapsed() and self.__save_button.check_click():
                    self.save_image(input('filename: '))
                
                if self.__propagation_toggle.check_click():
                    self.__to_propagate = not self.__to_propagate

            self.render()

        pygame.quit()


Visualizer().run()
