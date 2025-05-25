import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from source.odject.tile import Tile
from source.component.tilemap import TileMap
from source.component.camera import Camera
from source.component.aether import Aether
from source.component.window import Window

class Game:
    def __init__(self):
        # 初始化
        pygame.init()
        
        # 地图参数
        self.TILE_WIDTH = 16
        self.TILE_HEIGHT = 16
        self.MAP_WIDTH = 64
        self.MAP_HEIGHT = 64
        
        # 创建窗口
        self.window = Window()
        
        # 创建瓷砖和地图
        self._init_tiles()
        self._init_tilemap()
        
        # 创建相机
        self.camera = Camera(self.window.width, self.window.height)
        
        # 创建太空背景
        self.aether = Aether(self.window.width * 2, self.window.height * 2)
        
        # 创建时钟
        self.clock = pygame.time.Clock()

    def _init_tiles(self):
        self.grass_tile = Tile("assets/tile/grass.png", "grass")
        self.water_tile = Tile("assets/tile/water.png", "water")

    def _init_tilemap(self):
        self.tilemap = TileMap(self.MAP_WIDTH, self.MAP_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
        self.tilemap.add_tile_type(0, self.grass_tile)  # 草地
        self.tilemap.add_tile_type(1, self.water_tile)  # 水域
        self.tilemap.generate_noise_map(scale=0.1, threshold=0.4)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEWHEEL:
                self.camera.handle_mousewheel(event)
            elif event.type == pygame.VIDEORESIZE:
                self.window.handle_resize(event)
                self.camera.screen_width = self.window.width
                self.camera.screen_height = self.window.height

    def update(self):
        # 处理相机键盘输入
        self.camera.handle_keyboard()
        
        # 更新太空背景
        self.aether.update(self.camera)

    def render(self):
        # 清屏
        self.window.clear()
        
        # 绘制太空背景
        self.aether.draw(self.window.screen, self.camera)
        
        # 绘制地图
        self.tilemap.draw(self.window.screen, self.window.width, self.window.height, self.camera)
        
        # 计算并显示FPS
        fps = int(self.clock.get_fps())
        self.window.draw_fps(fps)
        
        # 更新显示
        self.window.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(120)