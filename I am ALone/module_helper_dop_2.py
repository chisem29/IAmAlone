import pygame
import random
import math
import module_helper

def get_scale_img(img, scale=[1, 1]):

    return pygame.transform.scale(img, tuple(scale))

class MethodBuildLevel:
    def __init__(self, screen, list_, img_dict, typeMode="auto"):

        self.screen = screen
        self.list = list(list_)
        self.dictionary = dict(img_dict)
        self.ID = 'level'
        self.type = 'img'
        self.typeMode = str(typeMode)

    def create_level(self, self_ob, ID, app_list, str_type, offset=[0, 0], scale=[0, 0], dictImgs={}):

        for y, row in enumerate(self_ob.list):
            for x, tile in enumerate(row):
                if bool(tile == str(str_type)):

                    selectDict = dict(dictImgs if bool(dictImgs) else self_ob.dictionary)

                    propertiesSelect = {

                        False : list([selectDict[ID].get_width(),
                                 selectDict[ID].get_height()]),
                        True : list([scale[0], scale[1]])

                    }
                    
                    optionsTarget = {
                        'x' : abs((x + (max([propertiesSelect[True][0] / propertiesSelect[False][0],
                            propertiesSelect[False][0] / propertiesSelect[True][0]]))) * (propertiesSelect[False][0] - propertiesSelect[True][0])),
                        'y' : abs((y + (max([propertiesSelect[True][1] / propertiesSelect[False][1],
                            propertiesSelect[False][1] / propertiesSelect[True][1]]))) * (propertiesSelect[False][1] - propertiesSelect[True][1]))          
                    }

                    app_list.append(module_helper.Entity(selectDict, 
                        float((propertiesSelect[False][0]*x + optionsTarget['x']) ),
                         float((propertiesSelect[False][1]*y + optionsTarget['y'] )),
                         ID, self.screen, str(self.type))
                    )
                    
                    if bool(self.typeMode in ["auto"]) :
                        self.screen.blit(selectDict[ID], 
                            (float((propertiesSelect[False][0]*x - offset[0] + optionsTarget['x'] )),
                             float((propertiesSelect[False][1]*y - offset[1] + optionsTarget['y'] )))
                        )

    def self_load_text_list(self, path : str):

        self.list = load_text(path)
        return self.list

    def selfOverlapeCreate(self) :

        listTarget = []

        for y, row in enumerate(self.list):
            for x, tile in enumerate(row):
                listTarget.append(
                    [y, x]
                )
        return list(listTarget)

class SelfSound:
    def __init__(self, selfPath, properties=[0, 0, 0, 0]):

        self.selfPath = str(selfPath)
        self.soundLoad = self.selfLoadSound()
        self.ID = "sound"

        self.soundOptions = {
            "get" : self.selfGetOptions(), 
            "set" : self.selfSetOptions()
        }
        self.propertiesSound = list(properties)
        self.soundOptions['set']['volume'](self.propertiesSound[3])

    def selfLoadSound(self, pathCh='') :
        
        return pygame.mixer.Sound(
            self.selfPath or pathCh
        )

    def selfSetOptions(self) :

        return {
            "volume" : (
                lambda val: self.soundLoad.set_volume(val)
            )
        }
    
    def selfGetOptions(self) :
        
        return {
            "volume" : self.soundLoad.get_volume(),
            "len" : self.soundLoad.get_length(),
            "raw" : self.soundLoad.get_raw(),
            "numChann" : self.soundLoad.get_num_channels()
        }
    
    def selfPlaySound(self, soundProps=[0, 0, 0]) :

        try :
            self.soundLoad.play(
                (soundProps or self.propertiesSound)[0],
                (soundProps or self.propertiesSound)[1],
                (soundProps or self.propertiesSound)[2]
            )
        except :
            pass

class SelfCircle:
    def __init__(self, screen, pos, ID, color, size):
        self.pos = tuple(pos)
        self.size = size
        self.screen = screen
        self.scroll = [0, 0]
        self.color = tuple(color)
        self.type = 'drawobj'
        self.ID = ID
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def self_draw_obj(self, self_ob, offset=[0, 0], count=0):
        
        pygame.draw.circle(self_ob.screen, self_ob.color, 
            (int(self_ob.rect.x-offset[0]), int(self_ob.rect.y-offset[1])), self_ob.rect.width, count)

    def self_move_x(self, self_ob):
        self_ob.rect.x += self_ob.scroll[0]

    def self_move_y(self, self_ob):
        self_ob.rect.y += self_ob.scroll[1]

class CameraObj:
    def __init__(self, screen, values=[0, 0, 0]):

        self.type = 'camera'
        self.screen = screen
        self.offset = [0, 0]

        self.values = list(
            values
        )
        
    def scrolling_offset_obj_x(self, self_obj, offset=[0, 0]):

        offset[0] -= int(list(offset)[0]-self_obj.rect.x+int(
            self.screen.get_width()//2)-self.values[0])
        return offset

    def scrolling_offset_obj_y(self, self_obj, offset=[0, 0]):

        offset[1] -= int(list(offset)[1]-self_obj.rect.y+int(
            self.screen.get_height()//2)-self.values[1])
        return offset

    def scrolling_offset_obj_all(self, self_obj, offset=[0, 0]):

        offset = self.scrolling_offset_obj_x(self_obj, offset)
        offset = self.scrolling_offset_obj_y(self_obj, offset)

        return list(offset)

def load_text(path, methodSplit='\n'):

    file_ = open(path, 'r')
    data = file_.read()
    file_.close()
    data = data.replace(" ", "").split(methodSplit)

    game_map = []
    for row in list(data):
        game_map.append(list(row))
    return game_map

def get_alpha_rect(fog_surf, value, pos, screen, sp=pygame.BLEND_RGBA_SUB):

    fog_surf.set_alpha(value)
    fog_surf.set_colorkey((0, 0, 0))
    screen.blit(fog_surf, pos, special_flags=sp)

def typeNormolise(typeOF) :

    return str(typeOF)[1+str(typeOF).index("'"):][:-2]

class DefaultIterable :
    def __init__(self, typeItter) :
                        
        self.typeProperties = list(self.returnTypes(typeItter))

    def returnTypes(self, iterabelPrototype) :

        return [
            typeNormolise(type(iterabelPrototype)), iterabelPrototype
        ]
      
    def selfRecursIter(self, iterableSelf, setProperties=[], setPropertiesIt=[]) :

        selectTypeItter = {
            "dict" : (lambda valueLet, itterOf : (itterOf[str(valueLet)])),
            "list" : (lambda valueLet, itterOf : valueLet),
        }
        if bool(
            self.typeProperties[0] in str(type(iterableSelf))
        ) :

            for objLet in iterableSelf :
                if bool(
                    self.typeProperties[0] in str(type(selectTypeItter[
                        self.typeProperties[0]](objLet, iterableSelf)))
                ) : 
                    setPropertiesIt.append(iterableSelf)

                    self.selfRecursIter(selectTypeItter[self.typeProperties[0]
                        ](objLet, iterableSelf), setProperties, setPropertiesIt)
                else : 
                    setProperties.append([selectTypeItter[self.typeProperties[0]
                        ](objLet, iterableSelf), iterableSelf, objLet])

        return [setProperties, setPropertiesIt]
    
    def selfConstructFromDict(self, iterDict, dictFolder={}, lambdaFolder=[]) :

        for osDir in dict(iterDict) :

            dictFolder[osDir] = (iterDict[osDir] if not lambdaFolder else lambdaFolder[0](osDir, iterDict)) \
                 if not bool(isinstance(osDir, dict)) else dict({})

            try :
                self.selfDictRecurs(
                    iterDict[osDir], dictFolder[osDir], lambdaFolder)
            except : 
                pass

        return dictFolder

class MegaParticle:
    def __init__(self, list_, screen, frame, size_pop):

        self.type = 'drawobj'
        self.ID = 'particle'
        self.list = list_
        self.screen = screen
        self.frame = list(frame)
        self.size_pop = list(size_pop)
        
    def generation_particles(self, width_height, pos, color=(0, 0, 0)):


        parallax = random.random()
    
        self.list.append([[pos[0], pos[1]+self.frame[1]*parallax], parallax, width_height, random.random()*2+1])

        for i, p in sorted(enumerate(self.list), reverse=True):
            size = p[2]
            p[2] -= self.size_pop[1]
            p[0][1] -= p[3]
            if size < 1:
                self.screen.set_at((int(p[0][0]), int(p[0][1]+self.frame[1]*p[1])), color)
            else:
                r = pygame.Rect(p[0][0]+self.frame[0], p[0][1]+self.frame[1]*p[1], int(p[2]), int(p[2]))
                pygame.draw.rect(self.screen, color, r)
            if size < 0:
                self.list.pop(i)

class ParticleObj:
    def __init__(self, screen, frame, pos, size_pop, color, size):

        self.ID = 'particle'
        self.type  = 'drawobj'
        self.screen = screen
        self.frame = list(frame)
        self.pos = list(pos)
        self.color = tuple(color)
        self.size = list(size)
        self.size_pop = list(size_pop)

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.random_constat, self.randomSlice = random.randint(20, 30)/30, [random.random() // 2 for i in range(1, 3)]

    def self_draw_obj(self, offset=[0, 0]):

        self.rect = pygame.Rect(self.pos[0]+self.frame[0]-offset[0], self.pos[1]+self.frame[1]-offset[1],
         self.size[0]-self.size_pop[0], self.size[1]-self.size_pop[1])
        pygame.draw.rect(self.screen, self.color, self.rect)

        return self.rect

    def self_frame_x(self):
        self.rect.x += self.frame[0]
    def self_frame_y(self):
        self.rect.y += self.frame[1]

class NormalEntity(module_helper.ArgCollision):
    def __init__(self, pos, image, divClass,
         screen, propsImg={}, typeOf="img") :

        self.pos = tuple(pos)
        self.image = image
        self.divClass = str(divClass)
        self.screen = screen
        self.motionObj = [0, 0]
        self.propertiesImg = \
            self.selfReturnPropertiesImg(propsImg)
        self.rect = self.selfReturnRectClip()
        self.type = str(typeOf)

    def selfDraw(self, offsetObj=[0, 0], sp=False, area=None) :

        self.screen.blit(self.image, (int(self.rect.x-list(offsetObj)[0]),
            int(self.rect.y-list(offsetObj)[1])), special_flags=sp , area=area)

    def selfAnimation(self, offsetObj=[0, 0], animationMan=None) :

        try :
            self.animationAd.self_animation(
                self, animationMan, offsetObj)
        except :
            # если нет attr : self.animationAd у object
            self.selfDraw(offsetObj)

    def selfReturnPropertiesImg(self, props) :

        try :
            return {
                str(keyGet) : props[keyGet] for keyGet in props
            }
        except :
            pass

    def selfReturnRect(self) : 

        return pygame.Surface.get_rect(
            self.image, topleft=self.pos)

class SelfMouse:
    def __init__(self, screen, ID):

        self.screen = screen
        self.mouse = pygame.mouse
        self.pos = tuple(self.mouse.get_pos())
        self.ID = str(ID)

        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], 1, 1)
    
    def self_update_pos(self, offset=[0, 0]):

        self.mouse = pygame.mouse
        self.pos = tuple([
            self.mouse.get_pos()[0]+offset[0],
            self.mouse.get_pos()[1]+offset[1]])

    def self_collide_rect(self, targetrect):

        try :
            targetObj = targetrect.rect
        except :
            targetObj = targetrect
        collidevalue = False

        if bool(targetObj.collidepoint(
            int(self.pos[0]), int(self.pos[1])
        )):
            collidevalue = True

        return bool(collidevalue)

class SelfRect:
    def __init__(self, pos, size, color, screen, ID):

        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.scroll = [0, 0]
        self.rect = pygame.Rect(self.pos[0], 
         self.pos[1], self.size[0], self.size[1])
        self.ID = ID
        self.screen = screen

    def self_draw(self, offset=[0, 0]):

        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.rect.x-int(offset[0]), 
         self.rect.y-int(offset[1]), self.rect.width, self.rect.height))

    def self_scroll_x(self):

        self.rect.x += self.scroll[0]

    def self_scroll_y(self):

        self.rect.y += self.scroll[1]

class SelfMask:
    def __init__(self, screen, pos, img, colorvals=[(0, 0, 0, 255),
         False], maskvals=[1, 1, [1, True, 1]]):

        self.pos = tuple(pos)
        self.img = img
        self.screen = screen

        self.colorvals= list(
            (colorvals)
        )

        self.maskval = list(
            (maskvals)
        )

        self.mask = pygame.mask.from_surface(
            self.img, self.maskval[1]
        )
        self.outlines = [(p[0] + self.pos[0], p[1] + self.pos[1])
             for p in self.mask.outline(self.maskval[0])]

    def self_get_FixedOutLine(self, targetSize : int) :

        pygame.draw.lines(self.screen, tuple(self.colorvals[0]),
             False, list(self.outlines), int(targetSize))

    def self_get_outline(self, colorkey=(0, 0, 0, 255)):

        maskout = self.mask.outline(self.maskval[0])
        mask_surf = pygame.Surface(tuple(
            self.img.get_size()), flags=self.colorvals[1])

        for outM in maskout :
            if bool(self.maskval[2][1]) :
                mask_surf.set_at(outM, (self.colorvals[0]))
            else:
                if bool(outM[1] < self.maskval[2][2]) :
                    mask_surf.set_at(outM, (self.colorvals[0]))

        mask_surf.set_colorkey((tuple(colorkey)))
        self.screen.blit(mask_surf, tuple(self.pos), special_flags=self.colorvals[1])

    def selfFromToSurf(self, properties=[None, 127, (0, 0, 0, 255),
            [None, None, (0, 0, 0, 255), (0, 0, 0, 255)]]) :

        '''
            getting toSurface and defaultMaskClass 
                : list[object], __len__ : 2;
        '''

        try :
    
            return [
                pygame.mask.from_surface(
                    properties[0], properties[1]),
                pygame.mask.from_surface(
                    properties[0], properties[1]).to_surface(
                        setsurface=properties[3][0], 
                        unsetsurface=properties[3][1],
                        setcolor=properties[3][2],
                        unsetcolor=properties[3][3])
            ]
            
        except :
            pass

class SelfPhisicRotateObj(module_helper.Entity):
    def __init__(self, *args):
        super().__init__(*args)

        self.random_constat = float(
            (random.randint(30, 50) // 10)
        )
        self.rotation_list = [0, 0]

    def self_get_phisic(self, self_ob, rotateval):
        
        self_ob.rotate = float(min(list(rotateval)) * self_ob.random_constat)//2

    def self_get_true_phisic(self, self_ob, properties) :

        if bool(
            len(properties) and any(properties)
        ) :

            if bool(
                abs(self_ob.rotate) < properties[0]
                or abs(self_ob.rotate) < math.sqrt(abs(
                    min([properties[0] // 2, self.random_constat 
                    * random.randint(3, 5)], default=self.random_constat)))
            ) :

                return self.self_get_phisic(self_ob, properties) 

            self_ob.rotate += -self.random_constat * min(
                 map(lambda propVal : propVal *random.random(),
                  [math.sqrt(random.random()) for i in range(1, 6)])
            ) - 0.1
            return

class PolygonParticle:
    def __init__(self, screen):
        self.type = 'drawobj'
        self.ID = 'particle'
        self.screen = screen
    def generation_particles(self, color, time_, num):

        points = [[0, num]]

        points += [[self.screen.get_width()/25*(i+2)+math.cos((time_+i*120)*2/math.pi)*8, num+(num/5)+math.sin((time_+i*10)/10)*4] for i in range(random.randint(22, 33))]
        points += [[self.screen.get_width(), math.pi*num+(num/10)], [self.screen.get_width(), 0], [0, 0]]

        fog_surf = pygame.Surface((self.screen.get_width(), num+20))
        pygame.draw.polygon(fog_surf, color, points)
        
        get_alpha_rect(fog_surf, 150, (0, 0), self.screen, pygame.BLEND_RGBA_SUB)

        self.screen.blit(pygame.transform.flip(fog_surf, False, True), (0, self.screen.get_height()-(num+20)))
        self.screen.blit(pygame.transform.flip(fog_surf, False, True), (0, self.screen.get_height()-(num+20)))

        side_fog = pygame.transform.scale(pygame.transform.rotate(fog_surf, 90), (num+20, self.screen.get_height()))
        self.screen.blit(pygame.transform.flip(side_fog, False, True), (0, 0))
        self.screen.blit(pygame.transform.flip(side_fog, True, False), (self.screen.get_width()-(num+20), 0))

def get_conver_img(img, color):
    img.convert()
    img.set_colorkey(color)

def get_alpha_circle(size, color, alpha):

    circle_surf = pygame.Surface((int(abs(size*2)+2), int(abs(size*2)+2)))
    pygame.draw.circle(circle_surf, color, (size+1, size+1), size+1)

    circle_surf.set_alpha(alpha)
    circle_surf.set_colorkey((0, 0, 0))

    return circle_surf

def get_alpha_square(target_rect, color, alpha) :

    targ_surf = pygame.Surface(
        (int(abs(target_rect.width * 2)),
         int(abs(target_rect.height * 2))))
    pygame.draw.rect(targ_surf, color, pygame.Rect(0,
         0, target_rect.width, target_rect.height))

    targ_surf.set_alpha(alpha)
    targ_surf.set_colorkey((0, 0, 0))

    return targ_surf

def get_alpha_img(color, img, alpha) :

    targSurf = pygame.Surface(img.get_size(),
         pygame.SRCALPHA).convert_alpha()
    targSurf.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    targSurf.set_alpha(alpha)
    targSurf.set_colorkey((0, 0, 0))
    
    targSurf.fill((130, 47, 36))

    return targSurf

def get_blit_center(target_surf, screen, loc):

    target_surf.blit(screen, (loc[0]-screen.get_width()//2,
     loc[1]-screen.get_height()//2), special_flags=pygame.BLEND_RGBA_ADD)

def particle_update(particles, screen, frame, size, alpha=0, scroll=[0, 0], color=[0, 0, 0]):

    for i, particle in sorted(enumerate(particles), reverse=True):

        particle.size_pop[1] += size[1]
        particle.size_pop[0] += size[0]
        particle_rect = particle.self_draw_obj(scroll)

        if particle_rect.width < 0 and particle_rect.height < 0:
            particles.pop(i)

        if particle.ID == 'particle':
            get_blit_center(screen, get_alpha_circle(particle.size[0]-particle.size_pop[0]//2,
            (color[0]+particle.size_pop[1]*1, color[1]+particle.size_pop[1]*1, color[2]+particle.size_pop[1]*1),
             alpha), (particle_rect.x, particle_rect.y))

        particle.frame[1] += frame[1]
        particle.frame[0] += frame[0]