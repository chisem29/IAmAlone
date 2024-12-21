import pygame
import random
import enid


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


def sounds_upload(sounds_list, index, key, num):

    sounds_list[index][key].play(num)


def create_position_map(_map_, self_ob, num_1, num_2, num):

        y_list = []
        x_list = []

        for y, row in enumerate(_map_):
            for x, tile in enumerate(row):
                if row.count('1') < 3 and row.count('-') == 0:
                    y_list.append(y)
                if tile == '0':
                    x_list.append(x)

        if len(self_ob.list) < num:
            self_ob.list.append(Helper(
                x_list[random.randint(0, len(x_list) - 1)] * self_ob.dx * num_1,
                y_list[random.randint(0, len(y_list) - 1)] * self_ob.dy * num_2,
                self_ob.dx,
                self_ob.dy,
                self_ob.screen,
                self_ob.list,
                self_ob.map,
                self_ob.list_animation,
                self_ob.other_rect,
            ))

        return x_list, y_list


def animation_function(self_ob, window, special_f):

    for self_ob in self_ob.list:
        if self_ob.direction == 'right':
            self_ob.list_animation[self_ob.key].draw(window, self_ob.rect.x, self_ob.rect.y, False, False, special_f)
        elif self_ob.direction == 'left':
            self_ob.list_animation[self_ob.key].draw(window, self_ob.rect.x, self_ob.rect.y, True, False, special_f)

    self_ob.list_animation[self_ob.key].update()


def moving_objects(rect, movement_obj, tiles, timer=0):

    rect.x += movement_obj[0]

    collisions_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    colls = collision_test(rect, tiles)

    for tile in colls:
        if movement_obj[0] > 0:
            rect.right = tile.left
        if movement_obj[0] < 0:
            rect.left = tile.right

    rect.y += movement_obj[1]

    colls = collision_test(rect, tiles)

    for tile in colls:
        if movement_obj[1] < 0:
            rect.top = tile.bottom
        if movement_obj[1] > 0:
            rect.bottom = tile.top

    return rect, collisions_types


class Box(object):
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.rect = pygame.Rect(self.x, self.y, self.dx, self.dy)

    def collision_and_remove(self, list_rect, other_rect, one_rect):

        for i in list_rect:
            if one_rect.colliderect(other_rect):
                list_rect.remove(i)

    def window(self,  self_rect, vector, list_b):

        list_b.append(pygame.Rect(self_rect.x+vector[0], self_rect.y+vector[1], self_rect.width, self_rect.height))


class Heart_Bar(object):
    def __init__(self, x, y, dx, dy, screen):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.rect = pygame.Rect(self.x, self.y, self.dx, self.dy)

        self.screen = screen
        self.list = []

    def window(self, window, rectangle, color, list_rect=None):

        pygame.draw.rect(window, color, rectangle.rect)

    def update_functions(self):

        self.window(self.screen, self, (115, 0, 0))


class FPS(object):
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25, bold=True)
        self.text = self.font.render(str(round(self.clock.get_fps())), True, (10, 10, 10))

        self.screen = screen

    def render(self, window):
        self.text = self.font.render(str(round(self.clock.get_fps())), True, (150, 150, 150))
        window.blit(self.text, (20, 10))

    def update(self):
        self.render(self.screen)
        self.clock.tick(45)


class Platforms(object):
    def __init__(self):

        self.list_platforms = []
        self.scroll = [0, 0]


class Coins(object):
    def __init__(self, x, y, dx, dy, coin_list, screen, rect, list_animation, list_sounds, map):

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.list = coin_list
        self.rect = pygame.Rect(self.x, self.y, self.dx, self.dy)
        self.player_class_ = rect

        self.vector = pygame.math.Vector2()
        self.no_change_values_of_vector = [1, 1]

        self.screen = screen
        self.map = map

        self.list_animation = list_animation
        self.key = 'coin'
        self.key_num = '2'
        self.direction = 'left'

        self.sounds_list = list_sounds
        self.flags_list = {1: pygame.BLEND_RGBA_MAX,
                           2: pygame.BLEND_ALPHA_SDL2,
                           3: pygame.BLEND_RGBA_MULT,
                           4: pygame.BLEND_RGBA_MIN}

    def window(self, self_ob, window):

        animation_function(self_ob, window, self_ob.flags_list[1])

    def generation_coins(self, class_object, post, n_x, n_y):

        for y, row in enumerate(post):
            for x, tile in enumerate(row):
                if tile == class_object.key_num:
                    class_object.list.append(Coins(
                       x*class_object.dx*n_x,
                       y*class_object.dy*n_y,
                       class_object.dx,
                       class_object.dy,
                       class_object.list,
                       class_object.screen,
                       class_object.player_class_,
                       class_object.list_animation,
                       class_object.sounds_list,
                       class_object.map))

    def gravity_objects_collisions(self, other_list, self_ob):

        for coin in self_ob.list:
            coin.vector.y += 0.1
            if coin.vector.y >= 2:
                coin.vector.y = 2
        if len(self_ob.list) == 1:
            for coin in self_ob.list:
                coin.vector.y = 0

        for coin in self_ob.list:
            for one_ob in other_list:
                if coin.rect.colliderect(one_ob):
                    coin.vector.y = 0
        for coin in self_ob.list:
            coin.rect.y += coin.vector.y

    def camera_movement_(self, self_ob, rect_vector):

        if rect_vector[0] > 0:
            for coin in self_ob.list:
                coin.vector.x = (-1 * self_ob.no_change_values_of_vector[1])
        elif rect_vector[0] < 0:
            for coin in self_ob.list:
                coin.vector.x = (1 * self_ob.no_change_values_of_vector[1])
        else:
            for coin in self_ob.list:
                coin.vector.x = 0

        for coin in self_ob.list:
            coin.rect.x += coin.vector.x

    def collision_coins(self, self_object, rect_object):

        for coin in self_object.list:
            if coin.rect.colliderect(rect_object.rect):

                self_object.list.remove(coin)
                sounds_upload(coin.sounds_list, 1, self_object.key, 0)

        if len(self_object.list) == random.randint(0, 1):
            for y, row in enumerate(self_object.map):
                for x, tile in enumerate(row):
                    if tile == self_object.key_num:
                        self_object.list.append(Coins(
                            (x * self_object.dx * 2),
                            (y * self_object.dy * 2),
                            self_object.dx,
                            self_object.dy,
                            self_object.list,
                            self_object.screen,
                            self_object.player_class_,
                            self_object.list_animation,
                            self_object.sounds_list,
                            self_object.map))

    def update(self):

        self.window(self, self.screen)
        self.collision_coins(self, self.player_class_)


class Entity(object):
    def __init__(self, x, y, dx, dy, list, screen, player_class, other_list, list_animation, map):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.rect = pygame.Rect(self.x, self.y, self.dx, self.dy-5)
        self.list = list
        self.vector = pygame.math.Vector2()
        self.vector.xy = random.choice([-1, 1]), 2
        self.number_enemy = 0

        self.screen = screen
        self.map = map
        self.player_class_ = player_class
        self.other_list = other_list
        self.type_collisions = {'W': False, 'S': False, 'A': False, 'D': False}

        self.key = 'enemy'
        self.key_num = '3'
        self.direction = 'right'
        self.state = 'idle'
        self.list_animation = list_animation
        self.list_flags = {1: pygame.BLEND_ALPHA_SDL2,
                           2: pygame.BLEND_RGBA_ADD}

        self.x_m = round(self.other_list[0].width//self.rect.width)
        self.y_m = round(self.other_list[0].height//self.rect.height)

    def spawn_and_generation_enemies(self,entity_class):

        for y, row in enumerate(entity_class.map):
            for x, tile in enumerate(row):
                if tile == entity_class.key_num:
                    entity_class.list.append(Entity(
                        x * entity_class.dx * entity_class.x_m,
                        y * entity_class.dy * entity_class.y_m,
                        entity_class.dx,
                        entity_class.dy,
                        entity_class.list,
                        entity_class.screen,
                        entity_class.player_class_,
                        entity_class.other_list,
                        entity_class.list_animation,
                        entity_class.map)

                                       )

    def movement_entity(self, e_list):

        for index, e in enumerate(e_list):

            if index % 2 == 0:
                if e.rect.x >= random.randint(300, 440):
                    e.vector.x = -1
                    e.direction = 'left'
                elif e.rect.x <= random.randint(30, 100):
                    e.vector.x = 1
                    e.direction = 'right'
            else:
                if e.rect.x >= random.randint(400, 540):
                    e.vector.x = -1
                    e.direction = 'left'
                elif e.rect.x <= random.randint(30, 50):
                    e.vector.x = 1
                    e.direction = 'right'

        for e in e_list:
            if e.type_collisions['S'] is True:
                e.rect.x += e.vector.x

    def collisions_object(self, self_object):

        last = pygame.time.get_ticks()

        for entity in self_object.list:
            if self_object.player_class_.rect.colliderect(pygame.Rect(random.randint(entity.rect.x-20, entity.rect.x+20),
                                                                      random.randint(entity.rect.y-20, entity.rect.y+20),
                                                                      entity.rect.width,
                                                                      entity.rect.height)):

                entity.number_enemy += 1
                self_object.list.remove(entity)

                entity.list.append(Entity(
                    entity.x,
                    entity.y,
                    entity.dx,
                    entity.dy,
                    entity.list,
                    entity.screen,
                    entity.player_class_,
                    entity.other_list,
                    entity.list_animation,
                    entity.map
                ))

    def gravity_list_objects(self, self_list, other_list):

        for self_ob in self_list:
            for other_ob in other_list:
                if self_ob.rect.colliderect(other_ob):
                    self_ob.vector.y = 0
                    self_ob.type_collisions['S'] = True

        for self_ob in self_list:
            self_ob.rect.y += self_ob.vector.y

    def window(self, self_ob):

        animation_function(self_ob, self_ob.screen, self_ob.list_flags[1])

    def return_spawn(self, self_ob):

        if len(self_ob.list) == self_ob.number_enemy*(len(self_ob.list)-1):
            self_ob.list.clear()
            self_ob.map.reverse()
            self_ob.spawn_and_generation_enemies(self_ob.map, self_ob, self_ob.x_m, self_ob.y_m)

    def update(self):
        self.movement_entity(self.list)
        self.window(self)
        self.return_spawn(self)
        self.gravity_list_objects(self.list, self.other_list)


class Create_Level(object):
    def __init__(self, self_list):

        self.list = self_list
        self.vector = pygame.math.Vector2(0, 0)

    def create_level_function(self, tiles, list_rect_f, image, number, num, num_2):

        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == number:
                    list_rect_f.append(
                        pygame.Rect(x * image.get_width() * num, y * image.get_height() * num_2,
                                    image.get_width(), image.get_height()))

    def update(self, window, self_list, image):

        for ob in self_list:
            window.blit(image, (ob.x, ob.y))

    def scroll_camera(self, other_ob, self_list):

        if other_ob.vector[0] > 0:
            self.vector.x = (-1*other_ob.vector[0])
        elif other_ob.vector[0] < 0:
            self.vector.x = (-1*other_ob.vector[0])
        else:
            self.vector.x = 0

        if other_ob.vector[1] > 0:
            self.vector.y = (-1*other_ob.vector[1])
        elif other_ob.vector[1] < 0:
            self.vector.y = (-1*other_ob.vector[1])
        else:
            self.vector.y = 0

        for self_ in self_list:
            self_.x += self.vector.x
            self_.y += self.vector.y


class Render_Font_Score(object):
    def __init__(self, x, y, dx_and_dy, screen, number, str_num, font_bold, str_text, color):
        self.x = x
        self.y = y
        self.dx_and_dy = dx_and_dy

        self.screen = screen
        self.number_mes = number

        self.str_num = str_num
        self.str_text = str_text
        self.font_bold = font_bold
        self.color = color

    def self_rendering(self, type_number, window, number_mes, str_text, type_font, color):

        if type_number == '1':
            font = pygame.font.SysFont(type_font, self.dx_and_dy, bold=True)
            render = font.render(str(str_text)+str(number_mes), True, color)
            window.blit(render, (self.x, self.y))
        else:
            pass

    def message_number(self, number=None):

        self.number_mes += 1

    def update_all_functions(self):

        self.self_rendering(self.str_num, self.screen, self.number_mes, self.str_text, self.font_bold, self.color)


class Image_Window(object):

    def __init__(self, self_list, screen):

        self.list = self_list
        self.screen = screen

    def self_rendering_image(self, self_list, index, pos_x, pos_y, window):

        window.blit(self_list[index], (pos_x, pos_y))
        #эта функция не расспространяется на анимации спрайтов


class Helper(object):
    def __init__(self, x, y, dx, dy, screen, _list_, _map_, list_animation, other_ob):

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.rect = pygame.Rect(self.x, self.y, self.dx, self.dy)
        self.other_rect = other_ob
        self.vector = pygame.math.Vector2()
        self.vector.xy = 0, 0

        self.screen = screen
        self.list = _list_
        self.map = _map_

        self.index = '5'
        self.key = 'helper'
        self.direction = 'right'
        self.list_animation = list_animation

        self.list_flags = {1: pygame.BLEND_RGBA_SUB,
                           2: pygame.BLEND_RGBA_MAX,
                           3: pygame.BLEND_ALPHA_SDL2,
                           4: pygame.BLEND_RGBA_ADD
                           }

        self.x_m = round(self.other_rect.width/self.rect.width, 1)
        self.y_m = round(self.other_rect.height/self.rect.height, 2)

    def create_position_map(self, self_ob):

        create_position_map(self_ob.map, self_ob, self_ob.x_m, self_ob.y_m, random.randint(1, 2))

    def update_change_map(self, self_ob):

        self_ob.create_position_map(self_ob)

    def set_mode_window(self, self_ob):

        animation_function(self_ob, self_ob.screen, self_ob.list_flags[4])

    def update_all_functions(self):

        self.create_position_map(self)
        self.set_mode_window(self)


class Ghost(object):
    def __init__(self, x, y, dx, dy, other_rect, screen, animation_list, sounds_list, list):

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.rect = pygame.Rect(self.x, self.y, self.dx, self.dy)
        self.list = list
        self.other_rect = other_rect

        self.screen = screen

        self.vector = pygame.math.Vector2(0, 0)
        self.vector.xy = 0, 0
        self.no_change_values_of_vector = [1, 1]

        self.key = 'ghost'
        self.direction = 'right'

        self.list_animation = animation_list
        self.sounds_list = sounds_list
        self.flags_list = {1: pygame.BLEND_MAX,
                           2: pygame.BLEND_ALPHA_SDL2}

    def set_mode_window(self, self_ob):

        animation_function(self_ob, self_ob.screen, self_ob.flags_list[2])

    def generation_objects(self, self_object):

        if len(self_object.list) <= 1:
            self_object.list.append(
                Ghost(self_object.x + random.randint(0+random.randint(40, 50), self_object.screen.get_width()-random.randint(40, 50)),
                      self_object.y + random.randint(0+random.randint(40, 50), self_object.screen.get_height()-random.randint(40, 50)),
                      self_object.dx,
                      self_object.dy,
                      self_object.other_rect,
                      self_object.screen,
                      self_object.list_animation,
                      self_object.sounds_list,
                      self_object.list
                )
            )

    def collisions_object(self, self_object):

        for self_ob in self_object.list:
            if self_object.other_rect.rect.colliderect(pygame.Rect(random.randint(self_ob.rect.x-20, self_ob.rect.x+20),
                                                                   random.randint(self_ob.rect.y-20, self_ob.rect.y+20),
                                                                   self_ob.rect.width,
                                                                   self_ob.rect.height)):

                self_object.list.remove(self_ob)
                self_object.generation_objects(self_object)

    def vector_and_position_change(self, self_object):

        for self_ob in self_object.list:
            if self_ob.rect.x < self_ob.other_rect.rect.x+random.randint(0, 20):
                self_ob.vector.x = (1 * self_object.no_change_values_of_vector[0])
            elif self_ob.rect.x > self_ob.other_rect.rect.x-random.randint(0, 20):
                self_ob.vector.x = (-1 * self_object.no_change_values_of_vector[0])
            else:
                self_ob.vector.x = 0

        for self_ob in self_object.list:
            if self_ob.rect.y < self_ob.other_rect.rect.y+random.randint(0, 20):
                self_ob.vector.y = (1 * self_object.no_change_values_of_vector[1])
            elif self_ob.rect.y > self_ob.other_rect.rect.y-random.randint(0, 20):
                self_ob.vector.y = (-1 * self_object.no_change_values_of_vector[1])
            else:
                self_ob.vector.y = 0

        self_object.position_object_updtate(self_object)

        return self_object

    def position_object_updtate(self, self_object):

        for self_ob in self_object.list:
            self_ob.rect.y += self_ob.vector.y
        for self_ob in self_object.list:
            self_ob.rect.x += self_ob.vector.x

    def update_all_functions(self):

        self.set_mode_window(self)
        self.vector_and_position_change(self)
        self.generation_objects(self)