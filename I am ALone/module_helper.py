from operator import attrgetter
import pygame
import random
import math
import os, json

'''
    @ only absolute Path; 
'''

def load_image(title, path, expansion):

    return pygame.image.load(
        str(path)+'/'+str(title)+'.'+str(expansion) 
    )

def loadJson(absPath, mod) :

    try :
        fileDist = open_file(absPath, mod)
        return [json.loads(fileDist), fileDist]
    except :
        return {}

def open_file(file_, path='r'):
    with open(str(file_), path,
         encoding='utf-8') as file__:
        return file__

class ArgCollision:
    def __init__(self):
        self.timer = 0
        self.speed_plus_y = 0
        self.collision_types = {
                                'top': False, 'bottom': False,
                                'left': False, 'right': False
                                }

class DrawImg(ArgCollision):
    def __init__(self, img, x, y, ID, screen):
        super().__init__()

        self.img = dict(img)
        self.x = int(x)
        self.y = int(y)
        self.ID = str(ID)

        self.vector = pygame.math.Vector2()
        self.speed_list = list([0, 0].copy())
        self.flip = [False, False]
        self.rotate = 0
        self.vector.xy = 0, 0

        self.screen = screen
        self.state = 'idle'
        self.directions = {'idle': True,
                           'walking': False,
                           'jumping': False}

        self.width = int(img[self.ID].get_width())
        self.height = int(img[self.ID].get_height())
        self.scale = list([self.width, self.height].copy())

        self.rect = self.return_rect(self)
        self.rect = self.self_inflate_rect(self)

    def self_change_direction(self, self_ob):

        if bool(self_ob.speed_list[0] > 0):
            self_ob.flip[0] = False
        elif bool (self_ob.speed_list[0] < 0):
            self_ob.flip[0] = True

    def self_inflate_rect(self, self_ob, values=[0, 0]):

        return self_ob.rect.inflate(float(values[0]), float(values[1]))

    def self_change_state(self, self_ob):

        if bool(self_ob.speed_list[0] != 0):
            self_ob.directions['walking'] = True
        else:
            self_ob.directions['idle'] = True
            self_ob.directions['walking'] = False
        
        if bool(self_ob.speed_list[1] < 0):
            self_ob.directions['jumping'] = True
        else:
            self_ob.directions['idle'] = True
            self_ob.directions['jumping'] = False

        for dir_ in self_ob.directions:
            if bool(self_ob.directions[dir_]):
                self_ob.state = dir_

    def returnTransformImg(self, self_ob) :

        return pygame.transform.scale(pygame.transform.flip(pygame.transform.rotate(
            self_ob.img[self_ob.ID], self_ob.rotate), self_ob.flip[0], self_ob.flip[1]), self_ob.scale)

    def selfSettingsSurface(self, self_ob, imgSet=False) :

        if not bool(imgSet):
            try :
                targetImg = \
                    self_ob.img[self_ob.ID]
            except :
                targetImg = \
                    self.img[self.ID]
        else :
            targetImg = imgSet
        
        settingsSurf = {
            "set_colorkey" : (lambda colorKEY : \
                pygame.Surface.set_colorkey(targetImg, colorKEY)),
            "set_clip" : (lambda rectClip : \
                pygame.Surface.set_clip(targetImg, rectClip)),
        } 

        return dict(settingsSurf)

    def selfReturnClipRect(self, self_ob) :

        return pygame.Surface.get_rect(
            self_ob.img[self_ob.ID], topleft=(self_ob.x, self_ob.y))

    def return_rect(self, self_ob):

        return pygame.Rect(self_ob.x, self_ob.y, self_ob.width, self_ob.height)

    def draw_obj(self, self_ob, offset=[0, 0], area=None, sp=False):

        try :
            self.screen.blit(self.returnTransformImg(self_ob), (int(self_ob.rect.x-list(offset)[0]),
                int(self_ob.rect.y-list(offset)[1])), area=area, special_flags=sp)
        except :
            pass

def setShadowRect (selfRect, properties, offsetObj=[0, 0]) :

    try :
        pygame.draw.rect(properties[0], properties[1], pygame.Rect(
            int(selfRect.x + properties[2] - offsetObj[0]), 
            int(selfRect.y + properties[3] - offsetObj[1]), 
            selfRect.width, selfRect.height
        ))
    except :
        pass

def setShadowCircle (selfRect, properties, offsetObj=[0, 0]) :

    try :
        pygame.draw.circle(properties[0], properties[1],
            (int(selfRect.x + properties[2] - offsetObj[0]), 
             int(selfRect.y + properties[3] - offsetObj[1])), 
             selfRect.width, properties[4]
        )
    except :
        pass

class Particle(object):
    def __init__(self, x, y, ID, screen, color, width, height):
        
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.copy_rect = self.rect.copy()

        self.ID = ID
        self.screen = screen
        self.vector = pygame.math.Vector2()
        self.color = color

    def delete_object(self, self_list):

        for self_ in list(self_list):
            if self_.rect.y < self_.screen.get_height()-0.5*self_.rect.height:
                self_list.remove(self_)
        
    def draw(self, self_ob):

        pygame.draw.rect(self_ob.screen, self_ob.color, self_ob.rect)

    def spawn(self, self_list):

        for i in range(random.randint(5, 10)):
            list(self_list).append(Particle(random.randint(0, self.screen.get_width()), random.randint(self.screen.get_height()-2*self.rect.height,
             self.screen.get_height()+3*self.rect.height), self.ID, self.screen, self.color, self.copy_rect.width, self.copy_rect.height))

    def update_vector(self, self_list):

        for self_ in list(self_list):
            self_.vector.y = random.randint(-3, -1)

        for self_ in list(self_list):
            self_.rect.y += self_.vector.y
            
class Entity(DrawImg):
    def __init__(self, img, x, y, ID, screen, type, animation_manager=False):
        super().__init__(img, x, y, ID, screen)

        self.type = str(type)
        self.num = 0
        self.anim_manager = animation_manager

    def collision_test(self, self_rect, tiles):
        collisions = []
        for tile in tiles:
            if self_rect.colliderect(tile.rect):
                collisions.append(tile)
        return collisions

    def self_collision(self, self_ob, tiles, motion=[0, 0]):

        types_collisions = {'top': False,
                            'bottom': False, 
                            'left': False,
                            'right': False}

        try :

            target_rect = self_ob.rect

            self_ob.self_speed_x(self_ob)
            self_collisions = self_ob.collision_test(self_ob.rect, tiles)

        except Exception :

            target_rect = self_ob
            target_rect.x += motion[0]

        for tile in self_collisions:
            
            if self_ob.speed_list[0] < 0:
                target_rect.left = tile.rect.right
                types_collisions['left'] = True
            elif self_ob.speed_list[0] > 0:
                target_rect.right = tile.rect.left
                types_collisions['right'] = True

        types_collisions = {'top': False,
                            'bottom': False,
                            'left': False,
                            'right': False}

        try :

            target_rect = self_ob.rect

            self_ob.self_speed_y(self_ob)
            self_collisions = self_ob.collision_test(self_ob.rect, tiles)

        except Exception :
            
            target_rect = self_ob
            target_rect.y += motion[1]

        for tile in self_collisions:
            
            if self_ob.speed_list[1] < 0:
                target_rect.top = tile.rect.bottom
                types_collisions['top'] = True

                try :
                    self_ob.speed_list[1] = 0
                except Exception :
                    motion[1] = 0

            elif self_ob.speed_list[1] > 0:
                target_rect.bottom = tile.rect.top
                types_collisions['bottom'] = True

                try :
                    self_ob.speed_list[1] = 0
                except Exception :
                    motion[1] = 0

        return target_rect, types_collisions, self_collisions

    def self_speed_x(self, self_ob):
        self_ob.rect.x += int(self_ob.speed_list[0])
        
    def self_speed_y(self, self_ob):
        self_ob.rect.y += int(self_ob.speed_list[1])

    def self_get_angle_y(self, self_ob, target_rect, target_motion, target_motion_copy, scroll=[0, 0]):

        if int(self_ob.rect.y-scroll[1]) < int(target_rect.y-scroll[1]):
            target_motion[1] = -abs(target_motion_copy[1])
        elif int(self_ob.rect.y-scroll[1]) > int(target_rect.y-scroll[1]):
            target_motion[1] = abs(target_motion_copy[1])
        else:
            target_motion[1] = 0

        return list(target_motion)

    def self_get_angle_x(self, self_ob, target_rect, target_motion=[0, 0], target_motion_copy=[0, 0], scroll=[0, 0]):

        if int(self_ob.rect.x-scroll[0]) < int(target_rect.x-scroll[0]):
            target_motion[0] = -abs(target_motion_copy[0])
        elif int(self_ob.rect.x-scroll[0]) > int(target_rect.x-scroll[0]):
            target_motion[0] = abs(target_motion_copy[0])
        else:
            target_motion[0] = 0

        return list(target_motion)

    def self_set_angle(self, self_ob, target_rect, target_motion=[0, 0], scroll=[0, 0]):

        self_angle = self.self_set_only_angle_(self_ob, target_rect, scroll)

        return list((math.cos(self_angle)*target_motion[0],  math.sin(self_angle)*target_motion[1]))

    def self_set_only_angle_(self, self_ob, target_rect, scroll=[0, 0]):

        self_angle = math.atan2(int(self_ob.rect.y-scroll[1])-int(target_rect.y-scroll[1]),
                                int(self_ob.rect.x-scroll[0])-int(target_rect.x-scroll[0]))

        return self_angle

    def self_get_distance_x(self, self_ob, target_rect, scroll=[0, 0]):

        return abs(self_ob.rect.centerx+scroll[0]-target_rect.centerx-scroll[0])

    def self_get_distance_y(self, self_ob, target_rect, scroll=[0, 0]):

        return abs(self_ob.rect.centery+scroll[1]-target_rect.centery-scroll[1])

    def self_get_all_distance(self, self_ob, target_rect, scroll=[0, 0]):

        return list((self.self_get_distance_x(self_ob, target_rect, scroll),
                    self.self_get_distance_y(self_ob, target_rect, scroll)))
    
    def self_animation(self, self_ob, animation, offset=[0, 0]):

        if bool(self_ob.anim_manager):
            
            self_ob.anim_manager.self_animation(self_ob, animation, offset)

        else:

            self_ob.draw_obj(self_ob, offset)

def defaultReverse(targetList) :

    targetList.reverse()
    return targetList

class Loot(Entity):
    def __init__(self, *args, velocity=[0, 0]):
        super().__init__(*args)

        self.velocity = velocity
        self.speed_list = velocity

    def self_collection(self, other_ob, self_list):

        bool_val = False

        for i, self_obj in enumerate(self_list):
            if self_obj.rect.colliderect(other_ob.rect):
                bool_val = True
                self_list.pop(i)

        return other_ob, bool_val

    def update(self, self_ob, num):
        self_ob.speed_list[1] = min(self_ob.speed_list[1]+random.random(), int(num))
        if self_ob.speed_list[1] < 0:
            self_ob.speed_list[1] *= -1

class RenderObj:
    def __init__(self, pos, font, screen, color, text):
        self.pos = list(pos)
        self.font = font
        self.screen = screen
        self.color = tuple(color)
        self.text = text
        self.vals = [
            True, False]
        self.allSize = tuple(
            self.font.size(self.text))

    def returnAlignCenter(self, targRect) :

        try :

            return tuple([
                targRect.centerx-self.allSize[0]//2,
                targRect.centery-self.allSize[1]//2,
            ])

        except :

            pass

    def selfConstructShadow(self, setColor=(0, 0, 0), topLeft=(0, 0), offset=[0, 0]) :

        if bool(any(topLeft)) :
            shadowOF = RenderObj((self.pos[0] + topLeft[0], self.pos[1] 
             + topLeft[1]), self.font, self.screen, setColor, self.text)
            if not bool(topLeft[1] > self.allSize[1] 
                 and topLeft[0] > self.allSize[0]) :
                shadowOF.self_render(shadowOF, offset)
        
        return shadowOF

    def self_render(self, self_ob, offset=[0, 0]):

       self_surface_render = self_ob.font.render(str(self_ob.text), bool(self_ob.vals[0]), self_ob.color)
       self_ob.screen.blit(self_surface_render, (int(self_ob.pos[0]-offset[0]), int(self_ob.pos[1]-offset[1])))

    def self_join_text(self, self_ob, symbol):

        self_ob.text.join(symbol)
        return str(self_ob.text)

    def self_remake_text(self, self_ob, other_text):

        self_ob.text = str(other_text)
        return str(self_ob.text)
    
        
class MapCircle(object):
    def __init__(self, radius, pos, color, screen, size):
        self.radius = radius
        self.pos = pos
        self.color = color
        self.screen = screen
        self.size = size

    def draw(self, self_ob):

        pygame.draw.circle(self_ob.screen, self_ob.color, self_ob.pos, self_ob.radius, self_ob.size)

     
class DefaultList(object):
    def __init__(self):
        self.list = self.return_list(self)

    def return_list(self, self_ob):
        return []
        
class SelfLIst(object):
    def __init__(self, list, ID, screen, img):

        self.list = list 
        self.img = img
        self.ID = ID
        self.screen = screen

        self.other_list = self.return_list(self)
        self.drops_list = self.return_list(self)
        self.timer_list = self.return_list(self)
        self.stuck_height = [(self.screen.get_height()//self.img[self.ID].get_height())-1
        for i in range((self.screen.get_width()//self.img[self.ID].get_width()-1))]

        self.stuck_height[0] -= 1

        self.set_timer = [0, 0]
        self.game_timer = [0, 0]

    def return_list(self, self_ob):

        return []

    def self_objects_spawn(self, self_ob, key):

        self_ob.game_timer[0] += float(0.01*random.randint(3, 8))
        self_ob.game_timer[1] += float(0.01*random.randint(3, 6))

        self_ob.set_timer[1] += 1
    
        if key == self_ob.ID:
            if self_ob.game_timer[0] > random.choice([3, 4]):

                self_ob.game_timer[0] = 0

                if self_ob.set_timer[1] > 5:
                    self_ob.set_timer[1] = 0

                minimum = min(self_ob.stuck_height)
                options = self_ob.return_list(self_ob)

                for i, stuck in sorted(enumerate(self_ob.stuck_height), reverse=True):
                    offset = stuck - minimum
                    for j in range(int(offset**0.7)+1):
                        options.append(i)

                self_ob.other_list.append(DrawImg(self_ob.img, self_ob.img[self_ob.ID].get_width()*(math.floor(random.choice(list(options))+1)), 
                (math.floor(-self_ob.set_timer[1]*self_ob.img[self_ob.ID].get_height()*3)), self_ob.ID, self_ob.screen))
                           
        elif key == 'box':
            for self_obj in self_ob.other_list:
                if self_obj.ID == self_ob.ID:
                    if self_ob.game_timer[1] > random.randint(23, 27):

                        self_ob.other_list.append(DrawImg(self_ob.img, self_obj.rect.x, 
                        self_obj.rect.y-self_ob.img[key].get_height(), key, self_ob.screen))

                        self_ob.game_timer[1] = 0
            
    def self_objects_collision_remove(self, self_ob):

        for other_obj in self_ob.other_list:
            other_obj.rect.y += other_obj.speed_list[1]
        for self_obj in self_ob.list:
            self_obj.rect.y += self_obj.speed_list[1]

        for self_obj in self_ob.list:
            if self_obj.rect.y > self_ob.screen.get_height()+(self_ob.img[self_ob.ID].get_height()*1):
                self_ob.list.remove(self_obj)
        
        for self_obj in self_ob.list:
            for self_obj_y in self_ob.other_list:
                if self_obj_y.rect.colliderect(self_obj.rect):
                    if self_obj_y.speed_list[1] > 0:
                        self_obj_y.rect.bottom = self_obj.rect.top
                        if self_obj.ID != self_ob.ID:
                            try:
                                self_ob.list.remove(self_obj)
                            except ValueError:
                                pass
                            self_obj_y.speed_list[1] = 40
                        else:
                            self_obj_y.speed_list[1] = 0
                    
        for other_obj in self_ob.other_list:
            if other_obj.speed_list[1] == 0:
                self_ob.list.append(other_obj)
                self_ob.other_list.remove(other_obj)
        
    def self_objects_movement(self, self_ob):

        height = self_ob.screen.get_height()//self_ob.img[self_ob.ID].get_height()
        width = self_ob.screen.get_width()//self_ob.img[self_ob.ID].get_width()
        self_drops_list = self_ob.drops_list.copy()

        img_height = lambda :math.floor(int(self_ob.img[self_ob.ID].get_height()))

        for self_obj in set(self_ob.other_list):
            self_obj.speed_list[1] = 5
        for self_obj in self_ob.list:  
            if self_obj.rect.y == img_height()*(height-2) and self_obj.ID == self_ob.ID:
                self_drops_list.append(self_obj)
        for self_obj in set(self_ob.list):  
            if len(set(self_drops_list)) > 0:
                if len(set(self_drops_list)) >= width:
                    self_obj.speed_list[1] = self_obj.rect.height
                elif self_drops_list[-1].rect.y >= img_height():
                    self_obj.speed_list[1] = 0

        return self_drops_list, height, width

    def self_update_spawn(self, self_ob):

        self_drops_list, height, width = self_ob.self_objects_movement(self_ob)
        if len(set(self_drops_list)) >= int(width):
            self_ob.list.append(DrawImg(self_ob.img, 0, -self_ob.img[self_ob.ID].get_height(), self_ob.ID, self_ob.screen))
            self_ob.list.append(DrawImg(self_ob.img, (width-1)*self_ob.img[self_ob.ID].get_width(), -self_ob.img[self_ob.ID].get_height(),
             self_ob.ID, self_ob.screen))
            
    def update(self):
        self.self_objects_spawn(self, self.ID)
        self.self_objects_spawn(self, 'box')
        self.self_objects_movement(self)
        self.self_objects_collision_remove(self)
        self.self_update_spawn(self)
        
