import pygame

# Initialize the game
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
set_caption = pygame.display.set_caption("Physics Engine")
set_icon = pygame.display.set_icon(pygame.image.load("icon/icon.jpg"))

gravity = 0.5
wall_thickness = 10
bounce_stop = 0.3
mouse_trajectory = []


class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction
        
    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
        
    def check_gravity(self):
        if not self.selected:
            if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                (self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:
            self.y_speed = y_push
            self.x_speed = x_push
        
        return self.y_speed
    
    def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]
        
        
    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected
    

def draw_walls():
    left = pygame.draw.line(screen, "white", (0, 0), (0, 600), 20)
    right = pygame.draw.line(screen, "white", (800, 0), (800, 600), 20)
    top = pygame.draw.line(screen, "white", (0, 0), (800, 0), 20)
    bottom = pygame.draw.line(screen, "white", (0, 600), (800, 600), 20)
    wall_list = [left, right, top, bottom]
    return wall_list
    
def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
        
    return x_speed, y_speed

ball1 = Ball(50, 50, 30, "yellow", 100, .9, 0, 0, 1, 0.02)
ball2 = Ball(500, 100, 50, "purple", 100, .9, 0, 0, 2, 0.02)
balls = [ball1, ball2]

while running: 
    clock.tick(60)
    screen.fill("black")
    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos):
                    active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((-1000, -1000))
    
            
            
    
    walls = draw_walls()
    ball1.draw()
    ball1.update_pos(mouse_coords)
    ball1.y_speed = ball1.check_gravity()
    ball2.draw()
    ball2.update_pos(mouse_coords)
    ball2.y_speed = ball2.check_gravity()
            
            
            
            
            
            
    pygame.display.flip()        
        
    

        
            

    
    
    

    

    
