import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.x = 0  # 相机X偏移
        self.y = 0  # 相机Y偏移
        self.zoom = 3.0  # 缩放比例
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.move_speed = 1  # 移动速度
        self.zoom_speed = 0.1  # 缩放速度
        self.min_zoom = 0.1  # 最小缩放
        self.max_zoom = 10.0  # 最大缩放
        self.velocity_x = 0  # X方向速度
        self.velocity_y = 0  # Y方向速度
        self.friction = 0.9  # 摩擦系数
        
    def handle_keyboard(self):
        """处理键盘输入"""
        keys = pygame.key.get_pressed()
        # WASD 和方向键控制
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y += self.move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y -= self.move_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x += self.move_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x -= self.move_speed
            
        # 应用摩擦力和更新位置
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # 如果速度很小，直接设为0
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0
        if abs(self.velocity_y) < 0.1:
            self.velocity_y = 0
            
        # 更新位置
        self.x += self.velocity_x
        self.y += self.velocity_y
            
    def handle_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        # 获取鼠标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 计算鼠标位置相对于世界坐标的位置
        world_x = (mouse_x - self.x) / self.zoom
        world_y = (mouse_y - self.y) / self.zoom
        
        # 保存旧的缩放值
        old_zoom = self.zoom
        
        # 更新缩放
        if event.y > 0:  # 向上滚动
            self.zoom = min(self.zoom + self.zoom_speed, self.max_zoom)
        else:  # 向下滚动
            self.zoom = max(self.zoom - self.zoom_speed, self.min_zoom)
            
        # 计算新的相机位置，保持鼠标指向的世界坐标不变
        self.x = mouse_x - world_x * self.zoom
        self.y = mouse_y - world_y * self.zoom
                    
    def apply(self, x, y):
        """应用相机变换到坐标"""
        # 应用缩放
        scaled_x = x * self.zoom
        scaled_y = y * self.zoom
        
        # 应用偏移
        return scaled_x + self.x, scaled_y + self.y
        
    def get_zoom(self):
        """获取当前缩放比例"""
        return self.zoom
