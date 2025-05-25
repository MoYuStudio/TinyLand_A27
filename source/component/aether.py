import pygame
import random
import math

class Star:
    def __init__(self, x, y, size, brightness, speed):
        self.x = x
        self.y = y
        self.size = size
        self.brightness = brightness
        self.speed = speed
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.twinkle_direction = 1
        self.current_brightness = brightness
        self.distance = math.sqrt(x*x + y*y)  # 到原点的距离
        self.angle = math.atan2(y, x)  # 与x轴的夹角

    def update(self, camera):
        # 星星闪烁效果
        self.current_brightness += self.twinkle_speed * self.twinkle_direction
        if self.current_brightness >= self.brightness:
            self.current_brightness = self.brightness
            self.twinkle_direction = -1
        elif self.current_brightness <= self.brightness * 0.5:
            self.current_brightness = self.brightness * 0.5
            self.twinkle_direction = 1
            
        # 根据距离计算视差效果
        parallax_factor = 1.0 - (self.distance / 10000)  # 距离越远，移动越慢
        if parallax_factor < 0.05:  # 降低最小视差因子
            parallax_factor = 0.05
            
        # 更新位置（进一步降低移动速度）
        self.x -= camera.x * parallax_factor * self.speed * 0.05  # 从0.1降到0.05
        self.y -= camera.y * parallax_factor * self.speed * 0.05  # 从0.1降到0.05

    def draw(self, screen, camera):
        # 应用相机变换
        screen_x, screen_y = camera.apply(self.x, self.y)
        
        # 检查是否在屏幕范围内
        if -self.size <= screen_x <= screen.get_width() + self.size and \
           -self.size <= screen_y <= screen.get_height() + self.size:
            # 确保亮度值在有效范围内
            brightness = min(255, max(0, int(self.current_brightness)))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.size)

class Aether:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        self.view_distance = 1500  # 视距
        self.min_star_distance = 50  # 星星之间的最小距离
        self.update_counter = 0  # 更新计数器
        self.generate_stars(100)  # 初始星星数量
        
    def is_valid_position(self, x, y):
        """检查新星星的位置是否合适"""
        for star in self.stars:
            distance = math.sqrt((x - star.x)**2 + (y - star.y)**2)
            if distance < self.min_star_distance:
                return False
        return True
        
    def generate_stars(self, count):
        """生成随机星星"""
        attempts = 0
        max_attempts = count * 3  # 最大尝试次数
        
        while len(self.stars) < count and attempts < max_attempts:
            # 使用极坐标生成星星，确保均匀分布
            distance = random.uniform(0, self.view_distance)
            angle = random.uniform(0, 2 * math.pi)
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            
            # 检查位置是否合适
            if self.is_valid_position(x, y):
                # 根据距离计算大小和亮度
                size_factor = 1.0 - (distance / self.view_distance)
                # 减小星星大小
                size = random.uniform(0.2, 0.6) * (1 + size_factor * 0.3)
                brightness = min(255, int(random.randint(100, 255) * (1 + size_factor * 0.5)))
                # 进一步降低移动速度
                speed = random.uniform(0.02, 0.05) * (1 + size_factor)  # 从0.05-0.1降到0.02-0.05
                
                self.stars.append(Star(x, y, size, brightness, speed))
            
            attempts += 1
            
    def update(self, camera):
        """更新所有星星的状态"""
        # 每4帧更新一次星星位置
        self.update_counter = (self.update_counter + 1) % 4
        if self.update_counter == 0:
            # 更新现有星星
            for star in self.stars:
                star.update(camera)
                
            # 检查是否需要生成新的星星
            visible_stars = sum(1 for star in self.stars 
                              if -star.size <= camera.apply(star.x, star.y)[0] <= self.width + star.size and 
                                 -star.size <= camera.apply(star.x, star.y)[1] <= self.height + star.size)
            
            # 如果可见星星太少，生成新的星星
            if visible_stars < 50:
                self.generate_stars(20)
                
            # 移除太远的星星
            self.stars = [star for star in self.stars 
                         if abs(star.x) < self.view_distance * 1.5 and 
                            abs(star.y) < self.view_distance * 1.5]
            
    def draw(self, screen, camera):
        """绘制所有星星"""
        for star in self.stars:
            star.draw(screen, camera)
