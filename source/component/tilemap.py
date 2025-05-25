import pygame
import random
from opensimplex import OpenSimplex
from source.odject.tile import Tile

class TileMap:
    def __init__(self, width, height, tile_width, tile_height):
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.iso_width = tile_width
        self.iso_height = tile_height // 2
        self.tiles = {}
        self.map_data = [[0 for _ in range(width)] for _ in range(height)]
        self.noise_generator = OpenSimplex(seed=random.randint(0, 1000000))
        
    def add_tile_type(self, tile_id, tile):
        """添加新的瓷砖类型"""
        self.tiles[tile_id] = tile
        
    def set_tile(self, x, y, tile_id):
        """设置指定位置的瓷砖"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map_data[y][x] = tile_id
            
    def get_tile(self, x, y):
        """获取指定位置的瓷砖ID"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map_data[y][x]
        return None
        
    def generate_noise_map(self, scale=0.1, threshold=0.0):
        """使用柏林噪声生成地图"""
        for y in range(self.height):
            for x in range(self.width):
                # 生成噪声值
                noise_value = self.noise_generator.noise2(x * scale, y * scale)
                # 将噪声值映射到0-1范围
                noise_value = (noise_value + 1) / 2
                
                # 根据阈值设置瓦片类型
                if noise_value > threshold:
                    self.map_data[y][x] = 0  # 草地
                else:
                    self.map_data[y][x] = 1  # 水域
        
    def tile_to_iso(self, x, y, screen_width, screen_height):
        """将地图坐标转换为等距屏幕坐标"""
        # 计算地图的总宽度和高度（以等距单位）
        map_width_iso = (self.width + self.height) * self.iso_width // 2
        map_height_iso = (self.width + self.height) * self.iso_height // 2
        
        # 计算偏移量，使地图居中
        offset_x = (screen_width - map_width_iso) // 2
        offset_y = (screen_height - map_height_iso) // 2
        
        # 计算等距坐标
        screen_x = (x - y) * self.iso_width // 2 + offset_x
        screen_y = (x + y) * self.iso_height // 2 + offset_y
        
        return screen_x, screen_y
        
    def draw(self, screen, screen_width, screen_height, camera=None):
        """绘制整个地图"""
        if not camera:
            return
            
        # 获取相机位置和缩放
        zoom = camera.get_zoom()
        camera_x, camera_y = camera.x, camera.y
        
        # 计算可见区域的范围
        # 考虑缩放和相机位置，计算需要绘制的瓦片范围
        visible_start_x = max(0, int((camera_x / zoom - screen_width) / self.iso_width))
        visible_end_x = min(self.width, int((camera_x / zoom + screen_width * 2) / self.iso_width))
        visible_start_y = max(0, int((camera_y / zoom - screen_height) / self.iso_height))
        visible_end_y = min(self.height, int((camera_y / zoom + screen_height * 2) / self.iso_height))
        
        # 只绘制可见区域的瓦片
        for y in range(visible_start_y, visible_end_y):
            for x in range(visible_start_x, visible_end_x):
                tile_id = self.map_data[y][x]
                if tile_id in self.tiles:
                    tile = self.tiles[tile_id]
                    tile.update()  # 自动更新动画帧
                    screen_x, screen_y = self.tile_to_iso(x, y, screen_width, screen_height)
                    
                    # 计算地图中心点（不应用缩放）
                    center_x = (self.width - 1) * self.iso_width // 2
                    center_y = (self.height - 1) * self.iso_height // 2
                    
                    # 调整坐标，使地图中心与相机中心对齐
                    screen_x = screen_x - center_x + screen_width // 2
                    screen_y = screen_y - center_y + screen_height // 2
                    
                    # 应用相机变换（包括缩放）
                    screen_x, screen_y = camera.apply(screen_x, screen_y)
                    
                    # 检查是否在屏幕范围内
                    if -self.tile_width <= screen_x <= screen_width + self.tile_width and \
                       -self.tile_height <= screen_y <= screen_height + self.tile_height:
                        # 直接用tile的draw方法，传递zoom参数
                        tile.draw(screen, screen_x, screen_y, zoom)
