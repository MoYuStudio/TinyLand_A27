import pygame
import os

class Tile:
    def __init__(self, image_path, tile_type="grass", animated=False, frame_count=1, frame_duration=10):
        self.type = tile_type
        self.animated = animated
        self.frame_count = frame_count
        self.frame_duration = frame_duration  # 每帧持续的tick数
        self.current_frame = 0
        self.tick = 0
        self.scale_cache = {}  # 缓存不同缩放下的帧

        if animated and frame_count > 1:
            # 加载多帧图片，命名如 water_1.png, water_2.png ...
            base, ext = os.path.splitext(image_path)
            self.frames = [
                pygame.image.load(f"{base}_{i+1}{ext}").convert_alpha()
                for i in range(frame_count)
            ]
            self.image = self.frames[0]
        else:
            if not os.path.exists(image_path):
                base, ext = os.path.splitext(image_path)
                alt_path = f"{base}_1{ext}"
                self.image = pygame.image.load(alt_path).convert_alpha()
            else:
                self.image = pygame.image.load(image_path).convert_alpha()
            self.frames = [self.image]

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        if self.animated and self.frame_count > 1:
            self.tick += 1
            if self.tick >= self.frame_duration:
                self.tick = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count
                self.image = self.frames[self.current_frame]

    def get_scaled_image(self, zoom):
        # 四舍五入到小数点后2位，避免浮点误差导致缓存失效
        zoom_key = round(zoom, 2)
        if (self.current_frame, zoom_key) in self.scale_cache:
            return self.scale_cache[(self.current_frame, zoom_key)]
        img = self.frames[self.current_frame]
        scaled = pygame.transform.scale(img, (int(self.width * zoom_key), int(self.height * zoom_key)))
        self.scale_cache[(self.current_frame, zoom_key)] = scaled
        return scaled

    def draw(self, screen, x, y, zoom=1.0):
        """在指定位置绘制瓷砖"""
        screen.blit(self.get_scaled_image(zoom), (x, y))
        
    def get_size(self):
        """获取瓷砖尺寸"""
        return self.width, self.height
