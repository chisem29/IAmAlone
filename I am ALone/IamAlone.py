import pygame, math, random, enid, parseFiles.FileParserPython, \
    module_helper_dop_2, module_helper, Functions_import, webbrowser

pygame.init(); pygame.mixer.pre_init(44100, 16, 2, 4096)

screen = pygame.display.set_mode((474, 432), pygame.DOUBLEBUF, 32)
screen.set_alpha(0)

def setSizeOf(fullPathOf : str) :

    if ("playerAsset" in fullPathOf) :
        return (30, 39)
    if ("background-head" in fullPathOf) :
        return screen.get_size()
    if ("instruction\\mouse" in fullPathOf) :
        return (12, 19)
    if ("entities" in fullPathOf) :
        return (29, 28)
    if ("stuff\\mana-coin" in fullPathOf) :
        return (12, 12)
    if ("stuff\\arrow" in fullPathOf) :
        return (7, 17)
    if ("bow" in fullPathOf) :
        return (16, 26)
    if ("artefact" in fullPathOf) :
        return (21, 21)

    return (36, 36)

def selfGetSoundProps(fullPathOf) :

    if ('gameplay' in fullPathOf) :
        return [0.6, 0, 1, 0.7]

imgList = parseFiles.FileParserPython.parseSysProperties(
    "IamAlone\\imgGame", {}, [(lambda key :
        pygame.transform.scale(pygame.image.load(key), setSizeOf(key)).convert_alpha())]
)
soundList = parseFiles.FileParserPython.parseSysProperties(
    "IamAlone\\soundsGame", {}, [(lambda key :
        module_helper_dop_2.SelfSound(key, list(selfGetSoundProps(key))))]
)

fpsGet = Functions_import.FPS(screen)
pygame.display.set_caption('I`m Alone')
pygame.display.set_icon(imgList['icon'])

def setShadowOf(thisObj, kwargs : list) :

    returnHandler = []

    for i in range(1, 3) :
        returnHandler.append(pygame.Rect(
         int(thisObj.rect.x - kwargs[0][0] + (abs(math.cos(math.pi / i)) * 9)), int(thisObj.rect.centery - kwargs[0][1] - 7), int((thisObj.rect.width * 0.53) * i),
         int((thisObj.rect.height * 0.5) // (i / max([i, thisObj.rect.height / 30.2])) + random.choice([2.7, 10, 10.45]) / 10)))

    return returnHandler

createLevel = module_helper_dop_2.MethodBuildLevel(
    screen,  module_helper_dop_2.load_text(r"IamAlone\\mapsGame\\map1.txt"), imgList["assetBlock1"])

assetTypes = {
    "assetBlock1" : {
        "top" : "1",
        "bottom" : "2",
        "left" : "3",
        "right" : "4",
        "centerright" : "5",
        "centerleft" : "6",
        "center" : "7",
        "bottomleft" : "8",
        "bottomright" : "9"
    },
    "backgrounds" : {
        "background#" : ["B", "#"],
        "background-chunk" : "B"
    }
}

animation = {
    strAsset : {
        strTarg : enid.Animation([
            imgList[strAsset][strTarg][str(i)] for i in range(1, len(imgList[strAsset][strTarg]) + 1)
        ] + module_helper.defaultReverse([
            imgList[strAsset][strTarg][str(i)] for i in range(1, len(imgList[strAsset][strTarg]) + 1)
        ]), 5) for strTarg in ['idle', 'walking', 'dead']
    } for strAsset in ['playerAsset']
}

animationBow = {
    strTarg : enid.Animation([
        imgList['bow'][strTarg][str(i)] for i in range(1, len(imgList['bow'][strTarg]) + 1)
    ] + module_helper.defaultReverse([
        imgList['bow'][strTarg][str(i)] for i in range(1, len(imgList['bow'][strTarg]) + 1)
    ]), 5) for strTarg in ['-Active', '-noActive']
}

class Player(module_helper.Entity) :
    def __init__(self, *args):
        super().__init__(*args)

        self.properties = {
            "game" : {
                "timer" : 0,
                "render" : {
                    "background" : [
                        module_helper.RenderObj((12, 12), pygame.font.SysFont('',
                            22, True), self.screen, (210, 205, 209), ''),
                        module_helper.RenderObj((352, 12), pygame.font.SysFont('',
                            23, True), self.screen, (210, 205, 209), ''),
                        module_helper.RenderObj((175, 12), pygame.font.SysFont('',
                            22, True), self.screen, (210, 205, 209), '')],
                    "begin" : [
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            23, True), self.screen, (207, 197, 205), 'Welcome. Use a mouse as a controller'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            23, True), self.screen, (207, 197, 205), 'LMB to move, RMB to open a chest'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            15, True), self.screen, (207, 197, 205), 'RMB'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            23, True), self.screen, (207, 197, 205), 'You can collect that'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            23, True), self.screen, (207, 197, 205), 'RMB + W to attack; arrows - '),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            23, True), self.screen, (207, 197, 205), 'You didn`t open all chest and collect their loot :\n'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('',
                            23, True), self.screen, (207, 197, 205), 'You didn`t kill all enemies, try that :\n')],
                },
                "stuff" : {
                    "mana" : 0,
                    "arrow" : random.choice([9, 10])
                },
                "particles" : {
                    "self" : [[]],
                    "background" : [module_helper_dop_2.PolygonParticle(self.screen)],
                },
                "bowDt" : AsigmPlayer(animationBow, imgList['bow']['-noActive'], self.rect.x,
                    self.rect.y, '1', self.screen, 'animation', enid.AnimationManager()),
                'arrows' : [],
            },
            "outGame" : {
                "timer" : 0,
                "render" : {
                    'gameOver' : [
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('', 24, True),
                            self.screen, (207, 197, 205), 'Game Over, game is restarting!')],
                    '-noArrows' : [
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('', 24, True),
                           self.screen, (207, 197, 205), 'Sorry, you haven`t arrows :|')],
                    'win' : [
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('', 24, True),
                           self.screen, (207, 197, 205), 'Oh, congratulations, you could /_(`_`)_/'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('', 24, True),
                           self.screen, (207, 197, 205), 'Man, and thanks for your attention :>'),
                        module_helper.RenderObj((0, 0), pygame.font.SysFont('', 22, True),
                           self.screen, (207, 197, 205), 'My ItchIo : https://sensaidev.itch.io/')
                    ]},
                'particles' : {
                    'finally' : []
                }
            },
            "currentLevel" : 1,
            "valuesOf" : [False, True, 8, False, False, False],
            "spamValues" : [[False, 0], [False, 0]]
        }
        self.rect = self.self_inflate_rect(self, [0, 4])

    def selfMovementMouse(self, mouseList : list, offsetObj : list, dt : int) :

        mouseList[1].rect = pygame.Rect(
            mouseList[1].pos[0], mouseList[1].pos[1], 1, 1)

        self.angleMoveList = list((
            self.self_set_angle(mouseList[1], self.rect, [3, 3], offsetObj)
        ))

        self.speed_list = [min([round(selfAng, 3) , 5.5]) for selfAng in self.angleMoveList]

    def selfGetCurrentLevel(self) :

        return str(self.properties["currentLevel"])

    def selfUpdate(self, kwrgs : list) :

        global entities, chests, finArtefact

        try :
            self.self_animation(
                self, animation['playerAsset'][self.state], kwrgs[0])
        except :
            self.state = 'walking'
        self.self_animation(
            self, animation['playerAsset'][self.state], kwrgs[0])

        self.rect, _, _ = self.self_collision(self, kwrgs[2])
        self.properties['mouse'] = module_helper.Entity(self.img, kwrgs[1][0].pos[0]
            + kwrgs[0][0], kwrgs[1][0].pos[1] + kwrgs[0][1], self.ID, self.screen, 'img')
        selfMouseKeys = pygame.mouse.get_pressed()

        for propertyOf in dict(self.properties) :
            if bool(propertyOf in ["game", "outGame"]) :
                if bool(self.properties["valuesOf"][0]) :
                    for elementGame in self.properties[propertyOf] :
                        if bool(self.properties["valuesOf"][1]) :
                            if bool(propertyOf in ["game"]) :
                                if bool(elementGame in ["timer"]) :
                                    self.properties[propertyOf
                                        ][elementGame] += 1
                                    for indexY, targetRow in enumerate(createLevel.list) :
                                        for indexX, targetLayer in enumerate(targetRow) :
                                            if bool(targetLayer in {"P"}) :
                                                if bool(self.properties[propertyOf][elementGame] < 2) :
                                                    self.rect.x, self.rect.y = tuple([
                                                        indexX * 36, indexY * 36])
                                            if bool(targetLayer in {"S"}) :
                                                if bool(self.properties[propertyOf][elementGame] < 2) :
                                                    entities.append(EnemySlime([kwrgs[-1]], imgList["entities"]["idle"],
                                                     indexX * 36, indexY * 36, "1", self.screen, "animation", enid.AnimationManager()))
                                            if bool(targetLayer in {"B"}) :
                                                if bool(self.properties[propertyOf][elementGame] < 2) :
                                                    chests.append(Chest(imgList["chests"], indexX * 36,
                                                     indexY * 36, "-falseHandler", self.screen, "img"))
                                            if bool(targetLayer in {"A"}) :
                                                if bool(self.properties[propertyOf][elementGame] < 2) :
                                                    finArtefact.append(FinallyArtefact(imgList["artefact"], indexX * 36,
                                                     indexY * 36, "artefact", self.screen, "img"))

                                elif bool(elementGame in ["render", "particles"]) :
                                    for elemRend in  self.properties[
                                        propertyOf][elementGame] :
                                        if not bool(elementGame in ["render"]) :

                                            for ind, elemParticles in enumerate(self.properties[
                                                propertyOf][elementGame][elemRend]) :
                                                if bool(elemRend in ["self"]) :
                                                    if not bool(ind) :
                                                        if bool(random.randrange(20) in [10, 14, 3]) :
                                                            elemParticles.append([pygame.Rect(
                                                                 self.rect.centerx + random.randint(-2, 6),
                                                                 self.rect.centery + random.randint(-2, 6), 
                                                                 random.randrange(5, 10), random.randrange(5, 10)),
                                                                 [self.screen, (230, 230, 230), "glow-self", 0]])

                                                    for handlerElem in sorted(elemParticles, reverse=True) :

                                                        handlerElem[0] = pygame.Rect(handlerElem[0].x, handlerElem[0].y,
                                                            round(handlerElem[0].width), round(handlerElem[0].height))
                                                        getSelfDist = self.self_get_all_distance(self, handlerElem[0], kwrgs[0])

                                                        if bool(random.randrange(4) in [1]) :
                                                            handlerElem[0].width -= 0.01 * kwrgs[-1] * 0.1
                                                            handlerElem[0].height -= 0.01 * kwrgs[-1] * 0.1           

                                                        pygame.draw.rect(handlerElem[1][0], handlerElem[1][1], pygame.Rect(handlerElem[0].x - kwrgs[0][0],
                                                            handlerElem[0].y - kwrgs[0][1], handlerElem[0].width, handlerElem[0].height))
                                                        handlerElem[1][3] += max([handlerElem[1][3], random.random()])

                                                        if bool((handlerElem[0].width < 0.1 and handlerElem[0].height < 0.1)
                                                                or (getSelfDist[1] > 50 or getSelfDist[0] > 50)) :
                                                            elemParticles.remove(handlerElem)
                                                        handlerElem[1][0].blit(module_helper_dop_2.get_alpha_square(
                                                         handlerElem[0], list(map(lambda x : x - 20, handlerElem[1][1])), 127), 
                                                         (handlerElem[0].centerx - kwrgs[0][0], handlerElem[0].centery - kwrgs[0][1]))
                                                        
                                                        if bool(random.randrange(5) in [3, 1]) :
                                                            handlerElem[0].x += (int(2 or self.speed_list[0]) * int(random.random() + 1) - random.randint(1, 4)) * kwrgs[-1]
                                                            handlerElem[0].y += (min([int(2 or self.speed_list[1]) * int(random.random() + 1) + math.pi * handlerElem[1][3], random.randrange(3)])) * kwrgs[-1]

                                                elif bool(elemRend in ['finally']) :
                                                    pass
                                        else :

                                            for ind, backRend in enumerate(self.properties[
                                                propertyOf][elementGame][elemRend]):

                                                if bool(elemRend in ['background']) :
                                                    backRend.text = str(f"mana-coin : {self.properties[propertyOf]['stuff']['mana']}" if not bool(ind)
                                                        else f'HP : {round(self.properties["valuesOf"][2])}' if bool(ind in [1]) else f"arrows : {self.properties['game']['stuff']['arrow']}")
                                                    backRend.selfConstructShadow(
                                                        (87, 87, 87, 255), (3, 3))
                                                    backRend.self_render(backRend)

                                                    if bool(ind in [1]) :
                                                        for i in range(1, 3) :
                                                            pygame.draw.rect(self.screen, (150 - i*30, 80 - i*30, 74 - i*30), pygame.Rect(
                                                                int(backRend.pos[0] + backRend.allSize[0] + 27 + ((i-1) * 3)),
                                                                int(backRend.pos[1] + backRend.allSize[1] // 2.4 + ((i-1) * 3)), 10, 10))
                                                    backRend.font.set_underline(True)

                                                elif bool(elemRend in ["begin"]) :
                                                    backRend.pos = \
                                                        backRend.returnAlignCenter(pygame.Rect(0, 0,
                                                         self.screen.get_width(), self.screen.get_height()))
                                                    if not bool(ind) :
                                                        if bool(self.properties[propertyOf]["timer"] < 80) :
                                                            backRend.text = 'Welcome. Use a mouse as a controller' \
                                                                if not bool(self.properties['valuesOf'][5]) else 'Maybe try again ;> ?'
                                                            backRend.selfConstructShadow(
                                                                (90, 87, 89, 255), (3, 3))
                                                            backRend.self_render(backRend)
                                                            if not bool(self.properties['valuesOf'][5]) :
                                                                self.screen.blit(imgList["instruction"]["mouse"],
                                                                    (backRend.pos[0] + backRend.allSize[0] + 10,
                                                                    backRend.pos[1] + backRend.allSize[1] * 0), special_flags=pygame.BLEND_ADD)
                                                    else :
                                                        if bool(ind in [1]) :
                                                            if bool(self.properties[propertyOf]["timer"] > 100 and 
                                                                    self.properties[propertyOf]["timer"] < 190) :
                                                                if not bool(self.properties['valuesOf'][5]) :
                                                                    backRend.selfConstructShadow(
                                                                        (90, 87, 89, 255), (3, 3))
                                                                    backRend.self_render(backRend)
                                                        elif bool(ind in [3, 2]) :
                                                            for chest in chests :
                                                                chestDist = chest.self_get_all_distance(chest, self.rect, scroll)
                                                                if bool(self.properties[propertyOf]["timer"] > 100) :
                                                                    if bool(ind in [3]) :
                                                                        if not bool(self.properties[propertyOf]["stuff"]["mana"]) :
                                                                            if bool(any(chest.properties["targetLoot"])) :
                                                                                backRend.pos = backRend.returnAlignCenter(
                                                                                        pygame.Rect(0, 0, screen.get_width(), screen.get_height() + 38))
                                                                                backRend.selfConstructShadow(
                                                                                    (90, 87, 89, 255), (3, 3))
                                                                                backRend.self_render(backRend)
                                                                    else :
                                                                        if bool(kwrgs[1][1].self_collide_rect(chest)) :
                                                                            if bool(chestDist[0] < 150 and chestDist[1] < 150) :
                                                                                if not bool(chest.properties["handlerOpeningOf"]) :
                                                                                    backRend.text = 'RMB'
                                                                                else :
                                                                                    backRend.text = 'OPENED'
                                                                                backRend.pos = tuple(map(lambda x : x - 20, chest.rect.topright))
                                                                                backRend.selfConstructShadow((90, 87, 89, 255), (3, 3), kwrgs[0])
                                                                                backRend.self_render(backRend, kwrgs[0])  
                                                        elif bool(ind in [4]) :
                                                            if bool(self.properties[propertyOf]['timer'] > 200 
                                                                and self.properties[propertyOf]['timer'] < 270) :
                                                                if not bool(self.properties['valuesOf'][5]) :
                                                                    backRend.text = f'RMB + W to attack; arrows - {self.properties[propertyOf]["stuff"]["arrow"]}'
                                                                    backRend.pos = backRend.returnAlignCenter(
                                                                        pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
                                                                    backRend.selfConstructShadow((90, 87, 89, 255), (3, 3))
                                                                    backRend.self_render(backRend)
                                                        elif bool(ind in [5, 6]) :
                                                            indexOfHandler = {5 : 0, 6 : 1}
                                                            if bool(self.properties[propertyOf]['timer'] > 290) :
                                                                if bool(self.properties['spamValues'][indexOfHandler[ind]][0]) :
                                                                    if bool(self.properties['spamValues'][indexOfHandler[ind]][1] < 30) :
                                                                        backRend.pos = backRend.returnAlignCenter(
                                                                            pygame.Rect(0, 0, screen.get_width(), screen.get_height() - 40))
                                                                        backRend.selfConstructShadow((90, 87, 89, 255), (3, 3))
                                                                        backRend.self_render(backRend) 
                                                                    else :
                                                                        self.properties['spamValues'][indexOfHandler[ind]][0] = False
                                                                    self.properties['spamValues'][indexOfHandler[ind]][1] += 1
                                                                else :
                                                                    self.properties['spamValues'][indexOfHandler[ind]][1] = 0             

                                elif bool(elementGame in ["bowDt"]) :
                                    self.properties[propertyOf][elementGame].rect.x, self.properties[propertyOf
                                        ][elementGame].rect.y = self.rect.centerx - 8, self.rect.centery - 5

                                    self.properties[propertyOf][elementGame].self_animation(
                                        self.properties[propertyOf][elementGame], animationBow[
                                        self.properties[propertyOf][elementGame].state], kwrgs[0])

                                    self.properties[propertyOf][elementGame].angle = \
                                        -self.self_set_only_angle_(self.properties['mouse'], self.rect, kwrgs[0]) * (180/math.pi) 
                                    self.properties[propertyOf][elementGame].anim_manager.dict_values[1] = \
                                        self.properties[propertyOf][elementGame].angle
                                    self.properties[propertyOf][elementGame].properties['asigmAnim'] = \
                                        animationBow[self.properties[propertyOf][elementGame].state]

                                    if bool(self.properties[propertyOf][
                                        elementGame].properties['animationTargets'][0]) :
                                        if bool(self.properties[propertyOf][elementGame
                                            ].properties['asigmAnim'].imageIndex >= 4) :
                                            self.properties[propertyOf][elementGame
                                                ].properties['animationTargets'][0] = False
                                    else :
                                        self.properties[propertyOf][elementGame
                                            ].properties['asigmAnim'].imageIndex = 1
                                                            
                            self.flip[0] = True if bool(kwrgs[1][1].pos[0] 
                                - self.rect.x < 0) else False
                            self.self_change_state(self)

                            if bool(self.properties["valuesOf"][2] <= 0) :
                                self.properties["valuesOf"][1] = False
                            elif bool(not self.properties['game']['stuff']['arrow'] and len(chests) in [len(list(filter(lambda key : key.properties["handlerOpeningOf"] 
                                    and not len(list(filter(lambda key2 : key2.ID in ['arrow'], key.properties['targetLoot']))), chests)))]
                                    and (not len(entities) or len(list(filter(lambda key : key.properties['healthBar'] < 5, entities))) != 1)) :
                                self.properties['valuesOf'][3], self.properties["valuesOf"][1] = True, False

                            if bool(self.properties["valuesOf"][2] <= 3) :
                                if bool(random.randrange(10) in {2}) :
                                    self.anim_manager.dict_values[2] = pygame.BLEND_ADD
                                else :
                                    self.anim_manager.dict_values[2] = False
                            else :
                                self.anim_manager.dict_values[2] = False
                            self.properties["outGame"]["timer"] = 0
    
                        else :
                            if bool(propertyOf in ["outGame"]) :
                                if bool(elementGame in ["timer"]) :
                                    if not bool(self.properties['valuesOf'][4]) :
                                        if bool(self.properties[propertyOf
                                            ][elementGame] > 80) :
                                            self.properties['valuesOf'][2] = 8
                                            for clearData in [entities, chests, finArtefact,
                                                self.properties['game']['arrows']] :
                                                clearData.clear()
                                            self.properties['game'
                                                ]['stuff']['mana'] = 0
                                            self.properties['game'
                                                ]['stuff']['arrow'] = random.choice([9, 10])
                                            self.properties['valuesOf'][4] = False
                                            self.properties['valuesOf'][1] = True
                                    self.properties[propertyOf
                                        ][elementGame] += 1
                                    self.anim_manager.dict_values[2] = False

                                if not bool(self.properties['valuesOf'][4]) :
                                    self.state = 'dead'
                                    for backRend in self.properties[propertyOf]['render'] :
                                        if bool(backRend in ["-noArrows"]) :
                                            if bool(self.properties['valuesOf'][3]) :
                                                self.properties[propertyOf]['render'][backRend][0].pos =  \
                                                    self.properties[propertyOf]['render'][backRend][0].returnAlignCenter(
                                                        pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
                                                self.properties[propertyOf]['render'][backRend
                                                    ][0].selfConstructShadow((90, 87, 89, 255), (3, 3))
                                                self.properties[propertyOf]['render'][backRend][0].self_render(
                                                    self.properties[propertyOf]['render'][backRend][0])
                                            self.properties[propertyOf]['render'][backRend][0].font.set_underline(True)
                                        elif bool(backRend in ["gameOver"]) :
                                            self.properties[propertyOf]['render'][backRend][0].pos =  \
                                                self.properties[propertyOf]['render'][backRend][0].returnAlignCenter(
                                                    pygame.Rect(0, 0, screen.get_width(), screen.get_height() - 40))
                                            self.properties[propertyOf]['render'][backRend
                                                ][0].selfConstructShadow((90, 87, 89, 255), (3, 3))
                                            self.properties[propertyOf]['render'][backRend][0].self_render(
                                                self.properties[propertyOf]['render'][backRend][0])
                                    if bool(animation['playerAsset'][self.state].imageIndex >= 7) :
                                        animation['playerAsset'][self.state].imageIndex = 7
                                    self.properties['valuesOf'][5] = True
                                else :
                                    self.state = 'idle'
                                    for backRend in self.properties[propertyOf]['render']['win'] :
                                        if bool(self.properties[propertyOf]['render']['win'].index(backRend) in [0]) :
                                            if bool(self.properties[propertyOf]['timer'] < 55) :
                                                backRend.pos = backRend.returnAlignCenter(
                                                    pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
                                                backRend.selfConstructShadow((90, 87, 89, 255), (3, 3)); backRend.self_render(backRend)
                                        elif bool(self.properties[propertyOf]['render']['win'].index(backRend) in [1, 2]) :
                                            if bool(self.properties[propertyOf]['timer'] > 80) :
                                                if bool(self.properties[propertyOf]['render']['win'].index(backRend) in [1]) :
                                                    backRend.pos = backRend.returnAlignCenter(
                                                        pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
                                                else :
                                                    backRend.pos = backRend.returnAlignCenter(
                                                        pygame.Rect(0, 0, screen.get_width(), screen.get_height() + 80))
                                                    backRend.font.set_underline(True)
                                                    if bool(kwrgs[1][1].self_collide_rect(pygame.Rect(backRend.pos[0],
                                                        backRend.pos[1], backRend.allSize[0], backRend.allSize[1]))) :
                                                        if bool(selfMouseKeys[0]) :
                                                            webbrowser.open(str(backRend.text.replace(' ', '').split(':', 1)[1]), new=1)
       
                                                        backRend.color = (212, 166, 187)
                                                    else :
                                                        backRend.color = (220, 200, 207)
                                                backRend.selfConstructShadow((90, 87, 89, 255), (3, 3)); backRend.self_render(backRend)

                                    if bool(self.properties[propertyOf]['timer'] > 65) :
                                        self.properties['currentLevel'] = 2
                                        for indexY, targetRow in enumerate(createLevel.list) :
                                            for indexX, targetLayer in enumerate(targetRow) :
                                                if bool(targetLayer in {"P"}) :
                                                    self.rect.x, self.rect.y = tuple([
                                                        indexX * 36, indexY * 36])
                                    else :

                                        for particle in self.properties['outGame']['particles']['finally'] :

                                            pygame.draw.rect(self.screen, particle[1][0], (particle[0].x - kwrgs[0][0],
                                                particle[0].y - kwrgs[0][1], particle[0].width, particle[0].height))
                                            module_helper_dop_2.get_blit_center(self.screen, module_helper_dop_2.get_alpha_circle(particle[0].width + 5 +
                                                random.randrange(6), (205, 183, 194), 100), (particle[0].centerx - kwrgs[0][0], particle[0].centery - kwrgs[0][1]))

                                            particle[0].width -= 0.00002
                                            particle[0].height -= 0.00002

                                            if bool(particle[0].width < 1 or particle[0].height < 1) :
                                                self.properties['outGame']['particles']['finally'].remove(particle)
                                            
                                            particle[0].x += math.cos(self.rect.x + random.randrange(10)) * random.randint(3, 6)
                                            particle[0].y += math.sin(self.rect.y + random.randrange(10)) * random.randint(3, 6)

                                        pygame.draw.circle(self.screen, (195, 183, 189), (self.rect.centerx - kwrgs[0][0],
                                            self.rect.centery - kwrgs[0][1]), max([round(65 - self.properties[propertyOf]['timer'] * 2), 0]), random.randint(1, 3))

                                self.properties["game"]["timer"] = 0
                else :
                    self.screen.blit(imgList["backgrounds"
                        ]["background-head"], (0, 0))

class EnemySlime(module_helper.Entity) :
    def __init__(self, kwargs : list, *args):
        super().__init__(*args)

        self.properties = {
            str(i) : {
                "timer" : 0,
                "value" : False if not bool(i in ["default-walking"]) else True
            } for i in {"default-walking", "attack", "dead"}
        }
        self.properties["healthBar"], self.properties['removeDataOf'], \
            self.properties["copyPos"] = [5, False, (self.x, self.y)]
        self.animation = {
            strTarg : enid.Animation([
                imgList['entities'][strTarg][str(i)] for i in range(1, len(imgList['entities'][strTarg]) + 1)
                ] + module_helper.defaultReverse([
                imgList['entities'][strTarg][str(i)] for i in range(1, len(imgList['entities'][strTarg]) + 1)
            ]), 6 // kwargs[-1]) for strTarg in ['idle', 'walking', 'dead']}; self.properties['particles'] = []
        
    def selfUpdate(self, kwargs : list) :

        try :
            self.self_animation(self, 
                kwargs[0][self.state], kwargs[1])
        except :
            self.state = 'walking'
        self.self_animation(self, 
            kwargs[0][self.state], kwargs[1])

        copyDist = self.self_get_all_distance(self, pygame.Rect(self.properties['copyPos'
            ][0], self.properties['copyPos'][1], self.rect.width, self.rect.height))
        self.rect, _, _ = \
            self.self_collision(self, kwargs[2])
        
        for prop in dict(self.properties) :
            if bool(isinstance(self.properties[prop], dict)) :
                if bool(kwargs[3].properties['valuesOf'][1]) :
                    if bool(self.properties[prop]["value"]) :
                        self.properties[prop]["timer"] += 1
                        if bool(prop not in ["dead"]) :

                            self.self_change_direction(self)
                            self.self_change_state(self) 

                            if bool(prop in ["default-walking"]) :
                                if bool(copyDist[0] < 100 and copyDist[1] < 100) :
                                    self.speed_list = list([0, 0])
                                else :
                                    self.speed_list = list(self.self_set_angle(module_helper.Entity(self.img, self.properties[
                                        'copyPos'][0], self.properties['copyPos'][1], '1', self.screen, 'img'), self.rect, [1.5, 1.5]))
                            else :
                                if bool(kwargs[3].rect.colliderect(self.rect)) :
                                    if bool(random.randrange(3) in [2]) :
                                        kwargs[3].properties["valuesOf"][2] -= 0.25
                                        kwargs[3].speed_list = list(self.self_set_angle(
                                            kwargs[3], self.rect, [2, 2], kwargs[1]))
                                self.speed_list = list(self.self_set_angle(
                                    kwargs[3], self.rect, list([1.6, 1.6]), kwargs[1]))

                            for targ in kwargs[2] :
                                targDist = self.self_get_all_distance(self, targ.rect)
                                if bool(targDist[0] < 50 and targDist[1] < 50) :
                                    self.speed_list = list(self.self_set_angle(self, targ.rect, [2.5, 2.5]))
                            
                            if not bool(self.rect.x < + kwargs[1][0] + 40 or self.rect.x > self.screen.get_width() - 40 + kwargs[1][0]
                                or self.rect.y < + kwargs[1][1] + 40 or self.rect.y > self.screen.get_height() - 40 + kwargs[1][1]) :
                                selfDist = self.self_get_all_distance(self, kwargs[3].rect)
                                if bool(selfDist[0] < 218 and selfDist[1] < 218) :
                                    self.properties["attack"]["value"], self.properties[
                                        "default-walking"]["value"] = True, False     
                                else :
                                    self.properties["attack"]["value"], self.properties[
                                        "default-walking"]["value"] = False, True        
                            else :
                                selfDist = list([0, 0])
                                self.speed_list = list(self.self_set_angle(module_helper.Entity(self.img, self.properties[
                                    'copyPos'][0], self.properties['copyPos'][1], '1', self.screen, 'img'), self.rect, [1.5, 1.5]))
                                self.properties["default-walking"]["value"], self.properties[
                                    "attack"]["value"] = True, False
                        else :
                            if bool(self.properties[prop]["timer"] > 100) :
                                self.properties['removeDataOf'] = True
                            self.speed_list, self.state = list([0, 0]), 'dead'

                            if bool(kwargs[0][self.state].imageIndex > 5) :
                                kwargs[0][self.state].imageIndex = 5
                            self.properties["attack"]["value"], self.properties[
                                "default-walking"]["value"] = False, False
                        
                        self.speed_list = [sp * kwargs[4] for sp in self.speed_list]

                        for selfParticle in self.properties['particles'] :
                            
                            self.screen.blit(module_helper_dop_2.get_alpha_square(
                                selfParticle[0], list(map(lambda x : x - 20, selfParticle[1][0])), 127), 
                                (selfParticle[0].centerx - kwargs[1][0], selfParticle[0].centery - kwargs[1][1]))
                            pygame.draw.rect(self.screen, selfParticle[1][0], pygame.Rect(selfParticle[0].x - kwargs[1][0],
                                selfParticle[0].y - kwargs[1][1], selfParticle[0].width, selfParticle[0].height))
                            selfParticle[0].width -= selfParticle[1][1][0]
                            selfParticle[0].height -= selfParticle[1][1][1]
 
                            if bool(selfParticle[0].height < 1 or selfParticle[0].width < 1) :
                                self.properties['particles'].remove(selfParticle)
                            
                    else :
                        self.properties[prop]["timer"] = 0
                        if bool(prop in ["dead"]) :
                            if bool(self.properties["healthBar"] <= 0) :
                                self.properties[prop]["value"] = True
                else :
                    self.speed_list = list([0, 0])

class Chest(module_helper.Entity) :
    def __init__(self, *args) :
        super().__init__(*args)
        self.properties = {
            "handlerOpeningOf" : False,
            "targetLoot" : [],
            "particles" : {
                "opening" : []
            }, 
        }
    def selfUpdate(self, kwargs : list) :

        self.draw_obj(self, kwargs[0])

        for selfProp in list(self.properties) :
            if bool(selfProp in ["handlerOpeningOf"]) :
                self.ID = str("-falseHandler" if not bool(
                    self.properties[selfProp]) else "-trueHandler")
            elif bool(selfProp in ["particles", 'targetLoot']) :
                for asigmOf in self.properties[selfProp] :
                    if bool(selfProp in ["particles"]) :
                        if bool(isinstance(self.properties[selfProp][asigmOf], list)) :
                            for indexTarg, selfParticle in sorted(enumerate(
                                self.properties[selfProp][asigmOf]), reverse=True) :

                                if bool(asigmOf in ["opening"]) :

                                    selfParticle[0].width -= selfParticle[1][1][0] * 0.1
                                    selfParticle[0].height -= selfParticle[1][1][1] * 0.1

                                    selfParticle[0].y += selfParticle[1][1][3]
                                    selfParticle[0].x += selfParticle[1][1][2]

                                    selfParticle[1][1][3] += random.random()
                            
                                    pygame.draw.rect(self.screen, selfParticle[1][0], pygame.Rect(selfParticle[0].x - kwargs[0][0],
                                        selfParticle[0].y - kwargs[0][1], selfParticle[0].width, selfParticle[0].height))
                                    self.screen.blit(module_helper_dop_2.get_alpha_square(selfParticle[0], list(map(lambda keyHandler : keyHandler - 20,
                                        selfParticle[1][0])), 127), (selfParticle[0].centerx - kwargs[0][0], selfParticle[0].centery - kwargs[0][1]))

                                    if bool(selfParticle[0].width < 1 
                                        and selfParticle[0].height < 1) :
                                        self.properties[selfProp][asigmOf].pop(indexTarg)

                    elif bool(selfProp in ['targetLoot']) :
                        
                        asigmOf.rect, _, _ = \
                            asigmOf.self_collision(asigmOf, kwargs[1])
                        asygmMask = module_helper_dop_2.SelfMask(self.screen, (asigmOf.rect.x, asigmOf.rect.y),
                            asigmOf.img[asigmOf.ID], [(190, 190, 190), pygame.BLEND_RGB_ADD], [1, 1, [1, True, 0]])

                        if bool(kwargs[2].rect.colliderect(asigmOf.rect)) :
                            kwargs[2].properties["game"]["stuff"
                                ][str(asigmOf.ID.split('-')[0])] += 1
                            self.properties[selfProp].remove(asigmOf)

                        asigmOf.draw_obj(asigmOf, kwargs[0])
                        if bool(random.randrange(4) in [2]) :
                            asigmOf.draw_obj(asigmOf, kwargs[0], sp=pygame.BLEND_ADD)

                        if bool(kwargs[3][1].self_collide_rect(asigmOf.rect)) :
                            asigmOf.draw_obj(asigmOf, kwargs[0], sp=pygame.BLEND_ADD)
                            asygmMask.self_get_FixedOutLine(1)

class AsigmPlayer(module_helper.Entity) :
    def __init__(self, selfAnim, *args) :
        super().__init__(*args)

        self.state = '-Active'
        self.properties = {
            'asigmAnim' :  selfAnim[self.state],
            "animationTargets" : [False, 0]
        }
 
class AsigmArrow(module_helper.Entity) :
    def __init__(self, kwargs : list, *args):
        super().__init__(*args)

        self.speed_list = [sp * kwargs[1] for sp in self.self_set_angle(
            kwargs[0].properties['mouse'], self.rect, [4, 4])]
        self.rotate = kwargs[0].properties['game']['bowDt'].angle -90

        self.properties = {
            'valuesOf' : {
                "colTarget" : [False, False, False],
                'heatDamage' : 2.5
            }
        }

        self.scale = self.rect.width, self.rect.height = \
            [max([self.width - self.rotate / (180/math.pi), self.width + 2]),
             max([self.height - self.rotate / (180/math.pi), self.height + 3])]

    def selfUpdate(self, kwargs : list) :

        self.draw_obj(self, kwargs[0])
        self.self_speed_x(self), self.self_speed_y(self)

        for targ in kwargs[1] :
            if bool(abs(targ.rect.centerx - self.rect.centerx) <= 18 + self.rect.width // 2
                and abs(targ.rect.centery - self.rect.centery) <= 18 + self.rect.height // 2) :
                self.speed_list = list([0, 0]); self.properties['valuesOf']['colTarget'][2] = True
        
        for entity in kwargs[3] :
            if bool(self.rect.colliderect(entity.rect)) :
                if not bool(self.properties['valuesOf']['colTarget'][2]) :
                    entity.properties['healthBar'] -= self.properties['valuesOf']['heatDamage']
                    entity.speed_list = entity.self_set_angle(entity, kwargs[2].rect,
                        [random.randint(4, 6) + random.random() for i in range(2)], kwargs[0])
                    for i in range(random.randint(7, 11)) :
                        entity.properties['particles'].append([pygame.Rect(entity.rect.x - 2, entity.rect.y - 2, random.randint(5, 10),
                            random.randint(5, 10)), [(202 + i, 185 + i, 190 + i), [random.random() for i in range(3)]]])
                    self.properties['valuesOf']['colTarget'][1] = True

        if bool(any(self.speed_list)) :
            if not bool(self.properties['valuesOf']['colTarget'][0]) :
                kwargs[2].properties['game']['stuff']['arrow'] -= 1
            self.properties['valuesOf']['colTarget'][0] = True

class FinallyArtefact(module_helper.Entity) :
    def __init__(self, *args):
        super().__init__(*args)
        
        self.properties = {
            'targetCol' : [False],
            'particles' : []
        }; 

    def selfGetAlpha(self, kwrgs : list) :

        for i in range(1, 3) :
            module_helper_dop_2.get_blit_center(self.screen, module_helper_dop_2.get_alpha_circle(random.randint(20 + i, 25) * 0.8 * ((1 + i) * 0.6),
                (70 + i*5, 20 + i*5, 25 + i*5), 100 + i*2), (self.rect.centerx - kwrgs[0][0], self.rect.centery - kwrgs[0][1]))

    def selfUpdate(self, kwargs : list) :

        selfMask = module_helper_dop_2.SelfMask(
            self.screen, (self.rect.x - kwargs[0][0], self.rect.y - kwargs[0][1]),
            self.img[self.ID], [(17, 14, 17), pygame.BLEND_RGB_ADD], [1, 1, [1, True, 0]])
        selfDist = self.self_get_all_distance(self, kwargs[1].rect, kwargs[0])

        self.draw_obj(self, kwargs[0])
        if bool(math.sqrt(random.randrange(10)) in {3}) :
            self.draw_obj(self, kwargs[0], sp=pygame.BLEND_ADD)
        self.self_collision(self, kwargs[2])
        
        if bool(kwargs[1].rect.colliderect(self.rect)) :
            if bool(kwargs[1].properties['game']['timer'] > 290 
                and kwargs[1].properties['valuesOf'][1]) :
                self.properties['targetCol'][0] = True
        
        if bool(selfDist[0] < 230 and selfDist[1] < 230) :
            if bool(kwargs[3][1].self_collide_rect(self)) :
                self.draw_obj(self, kwargs[0], sp=pygame.BLEND_ADD)
                selfMask.self_get_FixedOutLine(1)


player = Player(imgList["playerAsset"]["idle"], 10,
    10, '1', screen, 'animation', enid.AnimationManager())        

[blockList, blockListNH, entities, chests, scroll, finArtefact] = [[], [], [], [], [0, 0], []]

while (True) :

    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
    keys = pygame.key.get_pressed()

    for event in list(pygame.event.get()) :
        if (event.type in [pygame.QUIT]) :
            exit()
        if (event.type in [pygame.MOUSEBUTTONDOWN]) :
            if bool(player.properties["valuesOf"][0] 
                and player.properties["valuesOf"][1]) :
                if (event.button in [1]) :
                    player.selfMovementMouse(
                        selfMouses, scroll, targetDT)
                elif (event.button in [3] and keys[pygame.K_w]) :
                    if bool(player.properties['game']['stuff']['arrow'] > 0) :
                        if not bool(player.properties['game']['bowDt'].properties['animationTargets'][0]) :
                            player.properties['game']['arrows'].append(
                                AsigmArrow([player, targetDT], imgList["chests"]['stuff'],
                                    player.rect.centerx, player.rect.centery, 'arrow', screen, 'img'))
                            player.properties['game']['bowDt'].properties['animationTargets'][0] = True
            player.properties["valuesOf"][0] = True
        else :
            player.speed_list = list((0, 0))
    
    screen.fill((2, 2, 2))
    fpsGet.clock.tick(120 * 1)

    targetDT = min([(min([(60 / (fpsGet.clock.get_fps() + 1)) * 0.276,
        2]) if bool(fpsGet.clock.get_fps() < 60) else 1.2), 3.5])

    if bool(player.rect.x - scroll[0] < 0):
        scroll[0] -= screen.get_size()[0]
    elif bool(player.rect.x - scroll[0] > screen.get_size()[0]) :
        scroll[0] += screen.get_size()[0]
    if bool(player.rect.y - scroll[1] < 0):
        scroll[1] -= screen.get_size()[1]
    elif bool(player.rect.y - scroll[1] > screen.get_size()[1]) :
        scroll[1] += screen.get_size()[1] 

    createLevel.list = module_helper_dop_2.load_text(
        f"IamAlone\\mapsGame\\map{player.properties['currentLevel']}.txt")
    
    selfMouses = [
        module_helper_dop_2.SelfMouse(screen, "mouse"+str(i)) for i in range(1, 3)
    ]; blockList, blockListNH = [[], []]

    for targetX in range(screen.get_width() // imgList["backgrounds"]["background"].get_width() + 1) :
        for targetY in range(screen.get_height() // imgList["backgrounds"]["background"].get_height() + 1) :
            screen.blit(imgList["backgrounds"]["background"], 
                (targetX * imgList["backgrounds"]["background"].get_width(),
                 targetY * imgList["backgrounds"]["background"].get_height()))
    
    for charA in assetTypes["backgrounds"]["background#"] :
        createLevel.create_level(createLevel, "background#",
            blockListNH, charA, scroll, [36, 36], imgList["backgrounds"])
    createLevel.create_level(createLevel, "background-chunk", blockList, 
        assetTypes["backgrounds"]["background-chunk"], scroll, [36, 36], imgList["backgrounds"])

    for targetShadows in [entities, [player], chests, finArtefact] :
        for targShadow in targetShadows :
            if bool(([entities, [player], chests, finArtefact].index(targetShadows) in [2])) :
                for lootShadow in targShadow.properties['targetLoot'] :
                    pygame.draw.rect(screen, (14, 10, 14), (lootShadow.rect.x - (lootShadow.rect.width // 1.5) - scroll[0],
                        lootShadow.rect.centery + (lootShadow.rect.height // 2) - scroll[1], lootShadow.rect.width * 2, lootShadow.rect.width * 2))
            pygame.draw.rect(screen, (14, 10, 14), (targShadow.rect.x - 7 - scroll[0], targShadow.rect.centery
                - scroll[1], targShadow.rect.width * 1.4, targShadow.rect.height // 1.4), border_radius = 4)

    for targetID in assetTypes["assetBlock1"] :
        try :
            createLevel.create_level(createLevel, targetID, blockList, 
                assetTypes["assetBlock1"][targetID], scroll, [36, 36])
        except :
            pass

    for indM, mouseS in enumerate(selfMouses) :
        mouseS.self_update_pos(scroll
            if bool(indM) else [0, 0])
        mouseS.mouse.set_system_cursor(3)

    for row in range(len([blockList, blockListNH, chests])) :
        blocksTarget = [blockList, blockListNH, chests][row]
        for column in range(len(blocksTarget)) :
            
            try :

                if bool(isinstance(blocksTarget[column], Chest)) :
                    blocksTarget[column].selfUpdate([scroll, blockList, player, selfMouses])

                targetMask = module_helper_dop_2.SelfMask(
                    screen, (blocksTarget[column].rect.x - scroll[0], blocksTarget[column].rect.y - scroll[1]),
                    blocksTarget[column].img[blocksTarget[column].ID], [(98, 34, 41), pygame.BLEND_RGB_ADD], [1, 1, [1, True, 0]])
                targetDist = blocksTarget[column].self_get_all_distance(blocksTarget[column], player.rect, scroll)

                if bool(row) :
                    if bool(selfMouses[1].self_collide_rect(blocksTarget[column])) :
                        if bool(isinstance(blocksTarget[column], Chest)) :
                            if bool(player.properties["game"]["timer"] > 100) :
                                if bool(targetDist[0] < 150 and targetDist[1] < 150) :
                                    for event in list(pygame.event.get()) :
                                        if (event.type in [pygame.MOUSEBUTTONDOWN]) :
                                            if (event.button in [3]) :
                                                if not bool(blocksTarget[column].properties["handlerOpeningOf"]) :
                                                    for i in range(random.randrange(10, 18)) :
                                                        blocksTarget[column].properties["particles"]["opening"].append(
                                                            [pygame.Rect(blocksTarget[column].rect.x + i * 2.4, blocksTarget[column].rect.y - random.randint(5, round(i * 2 // 3.5) + 5),
                                                            random.randint(6, 10), random.randint(6, 10)), [tuple((200 + j for j in range(3))), list(map(
                                                            lambda x : x * targetDT, [random.random(), random.random(), math.cos(i * math.pi / 2), -1 * random.randint(1, 4)]))]])
                                                    for a in range(random.randint(1, 4)) :
                                                        if bool(len(list(filter(lambda key : key.ID in ["arrow"], blocksTarget[column].properties["targetLoot"])))) :
                                                            targetRandomId = random.choice(["mana-coin", "arrow"])
                                                        else :
                                                            targetRandomId = 'arrow'
                                                        blocksTarget[column].properties["targetLoot"].append(module_helper.Loot(imgList["chests"]["stuff"], blocksTarget[column].rect.x + imgList["chests"]["stuff"][targetRandomId].get_width(),
                                                            blocksTarget[column].rect.y - imgList["chests"]["stuff"][targetRandomId].get_height(), targetRandomId, screen, "img", [random.randint(2, 4), -math.pi]))
                                                    blocksTarget[column].properties["handlerOpeningOf"] = True

                        blocksTarget[column].draw_obj(blocksTarget[column], scroll, sp=pygame.BLEND_ADD)
                else :
                    if bool(selfMouses[1].self_collide_rect(blocksTarget[column])) :
                        if bool(sum(targetDist) // 2 < screen.get_width() // 4) :
                            if not bool(blocksTarget[column].ID in ["background-chunk"]) :
                                screen.blit(module_helper_dop_2.get_alpha_img((120, 36, 47), blocksTarget[column].img[blocksTarget[
                                    column].ID], 90), (blocksTarget[column].rect.x - scroll[0], blocksTarget[column].rect.y - scroll[1]))
                        player.speed_list = list([0, 0])
            except :
                pass

    for entity in entities :
        entity.selfUpdate([entity.animation, scroll, blockList, player, targetDT])
        if bool(entity.properties['removeDataOf']) :
            entities.remove(entity)

    for arrow in player.properties['game']['arrows'] :
        arrow.selfUpdate([scroll, blockList, player, entities])
        if bool(arrow.properties['valuesOf']['colTarget'][1]) :
            player.properties['game']['arrows'].remove(arrow)
    
    for artefact in finArtefact :
        artefact.selfUpdate([scroll, player, blockList, selfMouses, targetDT])
        if bool(artefact.properties['targetCol'][0]) :
            if bool(not len(list(filter(lambda key : not key.properties["handlerOpeningOf"] and not len(key.properties['targetLoot']),
                 chests))) and bool(not len(entities) or not len(list(filter(lambda x : x.ID in ['walking', 'jumping'], entities))))) :
                for i in range(random.randint(20, 30)) :
                    player.properties['outGame']['particles']['finally'].append([pygame.Rect(artefact.rect.x + random.randint(-20, 20), 
                        artefact.rect.y + random.randint(-20, 20), random.randint(10, 15), random.randint(10, 15)), [tuple(map(
                        lambda x : x + random.randrange(10), (200, 167, 187))), [random.random() for ztf in range(1, 3)]]])
                player.properties["valuesOf"][1], player.properties['valuesOf'][4] = False, True
                finArtefact.remove(artefact)
            else :
                if bool(len(entities) and not player.properties['game']['stuff']['arrow']) :
                    player.properties['spamValues'][0][0] = True
                else :
                    player.properties['spamValues'][1][0] = True
                artefact.properties['targetCol'][0] = False
        else :
            artefact.properties['targetCol'][0] = False

    player.selfUpdate([scroll, selfMouses, blockList, targetDT])
    
    for artefact in finArtefact :
        artefact.selfGetAlpha([scroll])

    if bool(player.properties['valuesOf'][0]) :
        for i in range(1, 3) :
            player.properties['game']['particles']['background'][0].generation_particles(
                (4 + 2*i, 2 + 2*i, 3 + 2*i), player.properties["game" if player.properties['valuesOf'][1] else 'outGame']["timer"] * targetDT * 1.15 / math.sin(3 * math.pi
                / 2) + i, (30 if (player.properties['valuesOf'][1] or player.properties['valuesOf'][4]) else 30 + player.properties['outGame']['timer']) + i * 17)
        soundList['gameplay']['default'].selfPlaySound()

    pygame.display.flip()