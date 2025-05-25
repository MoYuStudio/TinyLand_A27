import pygame
import os

class Window:
    def __init__(self, width=1280, height=720, title="TinyLand"):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None
        self.font = None
        self.initialize()

    def initialize(self):
        # 设置窗口
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)

        # 设置窗口图标
        icon = pygame.image.load("assets/tile/grass.png")
        pygame.display.set_icon(icon)

        # 创建字体对象
        self.font = pygame.font.Font("assets/font/kenney_pixel.ttf", 36)

    def handle_resize(self, event):
        self.width, self.height = event.w, event.h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        return self.width, self.height

    def draw_fps(self, fps):
        fps_text = self.font.render(f"FPS: {fps}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

    def clear(self):
        self.screen.fill((0, 0, 0))

    def update(self):
        pygame.display.flip()
