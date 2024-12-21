import pygame

class Animation(object):
    def __init__(self, imageList, speed_an=0):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = speed_an
        self.scale = [self.imageList[0].get_width(),
         self.imageList[0].get_height()].copy()
        
    def update(self):
        self.animationTimer += 1
        if self.animationTimer > self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, screen, x, y, flipX, flipY,  rotate=0, special_f=False, area_=None):
        screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.transform.flip(self.imageList[self.imageIndex],
         flipX, flipY), rotate), tuple(self.scale)), (x, y), area=area_, special_flags=special_f)

class AnimationManager:
    def __init__(self, dict_values={1: 0, 2: False, 3: None}):

        self.type = str('animation')
        self.dict_values = dict(dict_values)

    def self_animation(self, self_ob, animation, offset=[0, 0]):

        if bool(self_ob.type == self.type):

            self.animation = self.self_return_animation(animation)
            
            self.animation.draw(self_ob.screen, int(self_ob.rect.x-offset[0]),
             int(self_ob.rect.y-offset[1]), self_ob.flip[0], self_ob.flip[1], 
             rotate=self.dict_values[1], special_f=self.dict_values[2], area_=self.dict_values[3])

            self.animation.update()

    def self_return_animation(self, animation):

        self.animation = animation

        return self.animation

