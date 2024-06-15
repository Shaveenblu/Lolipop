#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random, time, webbrowser, os, entities
from datetime import datetime
from copy import deepcopy
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
import os
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(32)
pygame.display.set_caption('Ninja')
global WINDOWWIDTH, WINDOWHEIGHT
global screen
WINDOWWIDTH = 600
WINDOWHEIGHT = 400
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.RESIZABLE)
Display = pygame.Surface((300,200))



    
def load_img(path):
    img = pygame.image.load(path).convert()
    #make all the white part of the image transparent
    img.set_colorkey((255,255,255))
    return img

# Colors ----------------------------------------------------- #
SKY = (255,192,203)
# Images ----------------------------------------------------- #
tile_list = os.listdir('data/images/tiles')
tile_database = {}
for tile in tile_list:
    if tile != 'Thumbs.db':
        img = pygame.image.load('data/images/tiles/' + tile).convert()
        img.set_colorkey((255,255,255))
        tile_database[tile] = img.copy()

ninja_run = entities.animation([[0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2]],'data/images/ninja/run/',['loop'])
ninja_run_key = ninja_run.start(0,0)
ninja_wall = load_img('data/images/ninja/wall_stick.png')
ninja_eat = load_img('data/images/ninja/eat.png')
ninja_jump = load_img('data/images/ninja/jump.png')
ninja_stand = load_img('data/images/ninja/standing.png')
bomb_img = load_img('data/images/bomb.png')
lollipop_img = load_img('data/images/lollipop_win.png')
textbox_img = load_img('data/images/text_box.png')
textbox_img_2 = load_img('data/images/text_box_2.png')
textbox_img.set_alpha(200)
invisibility_icon = load_img('data/images/invisibility_icon.png')
bomb_icon = load_img('data/images/bomb_icon.png')
jump_animation = entities.animation([[0,2],[1,1],[2,2],[3,1],[4,2],[5,1],[6,2],[7,1],[8,2],[9,1]],'data/images/animations/jump/',[])
wall_jump_animation = entities.animation([[0,2],[1,1],[2,2],[3,1],[4,2],[5,1],[6,2],[7,1],[8,2],[9,1]],'data/images/animations/wall_jump/',[])
turn_animation = entities.animation([[0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],[8,2]],'data/images/animations/turn/',[])
cloud_0_img = load_img('data/images/cloud_0.png')
cloud_1_img = load_img('data/images/cloud_1.png')
cloud_2_img = load_img('data/images/cloud_2.png')
cloud_3_img = load_img('data/images/cloud_3.png')
cloud_index = {'cloud_0':cloud_0_img, 'cloud_1':cloud_1_img, 'cloud_2':cloud_2_img, 'cloud_3':cloud_3_img}
ready_img = load_img('data/images/icon_ready.png')



# Text ------------------------------------------------------- #
def GenerateFont(FontImage,FontSpacingMain,TileSize,TileSizeY,color):
    FontSpacing = deepcopy(FontSpacingMain)
    FontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"']
    FontImage = pygame.image.load(FontImage).convert()
    NewSurf = pygame.Surface((FontImage.get_width(),FontImage.get_height())).convert()
    NewSurf.fill(color)
    FontImage.set_colorkey((0,0,0))
    NewSurf.blit(FontImage,(0,0))
    FontImage = NewSurf.copy()
    FontImage.set_colorkey((255,255,255))
    num = 0
    for char in FontOrder:
        FontImage.set_clip(pygame.Rect(((TileSize+1)*num),0,TileSize,TileSizeY))
        CharacterImage = FontImage.subsurface(FontImage.get_clip())
        FontSpacing[char].append(CharacterImage)
        num += 1
    FontSpacing['Height'] = TileSizeY
    return FontSpacing
def ShowText(Text,X,Y,Spacing,WidthLimit,Font,surface,overflow='normal'):
    Text += ' '
    OriginalX = X
    OriginalY = Y
    CurrentWord = ''
    if overflow == 'normal':
        for char in Text:
            if char not in [' ','\n']:
                try:
                    Image = Font[str(char)][1]
                    CurrentWord += str(char)
                except KeyError:
                    pass
            else:
                WordTotal = 0
                for char2 in CurrentWord:
                    WordTotal += Font[char2][0]
                    WordTotal += Spacing
                if WordTotal+X-OriginalX > WidthLimit:
                    X = OriginalX
                    Y += Font['Height']
                for char2 in CurrentWord:
                    Image = Font[str(char2)][1]
                    surface.blit(Image,(X,Y))
                    X += Font[char2][0]
                    X += Spacing
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                else:
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X,Y
    if overflow == 'cut all':
        for char in Text:
            if char not in [' ','\n']:
                try:
                    Image = Font[str(char)][1]
                    surface.blit(Image,(X,Y))
                    X += Font[str(char)][0]
                    X += Spacing
                except KeyError:
                    pass
            else:
                if char == ' ':
                    X += Font['A'][0]
                    X += Spacing
                if char == '\n':
                    X = OriginalX
                    Y += Font['Height']
                CurrentWord = ''
            if X-OriginalX > WidthLimit:
                X = OriginalX
                Y += Font['Height']
        return X,Y

global Font_0
font_dat = {'A':[3],'B':[3],'C':[3],'D':[3],'E':[3],'F':[3],'G':[3],'H':[3],'I':[3],'J':[3],'K':[3],'L':[3],'M':[5],'N':[3],'O':[3],'P':[3],'Q':[3],'R':[3],'S':[3],'T':[3],'U':[3],'V':[3],'W':[5],'X':[3],'Y':[3],'Z':[3],
          'a':[3],'b':[3],'c':[3],'d':[3],'e':[3],'f':[3],'g':[3],'h':[3],'i':[1],'j':[2],'k':[3],'l':[3],'m':[5],'n':[3],'o':[3],'p':[3],'q':[3],'r':[2],'s':[3],'t':[3],'u':[3],'v':[3],'w':[5],'x':[3],'y':[3],'z':[3],
          '.':[1],'-':[3],',':[2],':':[1],'+':[3],'\'':[1],'!':[1],'?':[3],
          '0':[3],'1':[3],'2':[3],'3':[3],'4':[3],'5':[3],'6':[3],'7':[3],'8':[3],'9':[3],
          '(':[2],')':[2],'/':[3],'_':[5],'=':[3],'\\':[3],'[':[2],']':[2],'*':[3],'"':[3]}
Font_0 = GenerateFont('data/fonts/small_font.png',deepcopy(font_dat),5,8,(218,219,224))
Font_1 = GenerateFont('data/fonts/small_font.png',deepcopy(font_dat),5,8,(24,24,35))
# Functions -------------------------------------------------- #
global collision_types
collision_types = ['grass','dirt','grass_right','grass_left','grass_top','dirt_left','dirt_right','dirt_middle','dirt_bottom','dirt_bottom_left','dirt_bottom_right','dirt_bottom_middle',
                   'brick','brick_bottom','brick_bottom_middle','brick_center','brick_left','brick_left_bottom','brick_left_middle','brick_middle','brick_right','brick_right_bottom','brick_right_middle','brick_top']
global decor_list
decor_list = ['crate','crates','crates_2','tree','tree_0','tree_1','tree_2','tree_3','tree_4','tree_5','thin_tree','weapon_stand','pillar','torch_r','torch_l','support_right','support_left','potted_plant','sugar_cane']

def get_rates(point_1, point_2):
    x_dif = point_2[0]-point_1[0]
    y_dif = point_2[1]-point_1[1]
    try:
        rate_x = x_dif / (abs(x_dif) + abs(y_dif))
    except ZeroDivisionError:
        rate_x = 0
    try:
        rate_y = y_dif / (abs(x_dif) + abs(y_dif))
    except ZeroDivisionError:
        rate_y = 0
    return rate_x, rate_y

def get_spotlight_points(start,target):
    rates = get_rates(start,target)
    points = [start]
    x = target[0] + rates[1] * 4
    y = target[1] - rates[0] * 4
    points.append([x,y])
    points.append([target[0]+rates[0]*3,target[1]+rates[1]*3])
    x = target[0] - rates[1] * 4
    y = target[1] + rates[0] * 4
    points.append([x,y])
    return points

def frames_to_time(frames):
    seconds = frames / 40
    seconds = round(seconds,2)
    minutes = (seconds - (seconds % 60)) / 60
    seconds = round(seconds % 60,2)
    seconds = str(seconds)
    if float(seconds) < 10:
        seconds = '0' + seconds
    if len(seconds[seconds.find('.')+1:]) < 2:
        seconds += '0'
    minutes = str(int(minutes))
    if int(minutes) < 10:
        minutes = '0' + minutes
    time_str = minutes + ':' + seconds
    return time_str

def normalize(num,amount):
    if abs(num) < amount:
        num = 0
    elif num < 0:
        num += amount
    elif num > 0:
        num -= amount
    return num

def cap(num,amount):
    if num > amount:
        num = amount
    if num < -amount:
        num = -amount
    return num

def maximum(num,amount):
    if num > amount:
        num = amount
    return num

def minimum(num,amount):
    if num < amount:
        num = amount
    return num

def Text2List(Text,Divider,intmode=False):
    List = []
    Current = ''
    for char in Text:
        if char != Divider:
            Current += char
        else:
            if intmode == True:
                try:
                    List.append(int(Current))
                except:
                    List.append(Current)
            else:
                List.append(Current)
            Current = ''
    return List

def nearby_tiles(x,y,tiles):
    x_loc = int(round(x/32,0))
    y_loc = int(round(y/32,0))
    tile_list = []
    for y in range(3):
        for x in range(3):
            loc = str(x_loc+x-1) + ';' + str(y_loc+y-1)
            if loc in tiles:
                for tile in tiles[loc][0]:
                    if tile[:-4] in collision_types:
                        tile_list.append([tiles[loc][1]*32,tiles[loc][2]*32,32,32])
                        break
    return tile_list

def load_map(name):
    file = open('data/maps/' + name + '.txt','r')
    map_data = file.read()
    file.close()
    tiles = Text2List(map_data,'=')
    items = []
    decor = []
    item_list = ['lollipop.png','human.png','camera_down_left.png','camera_down_right.png','camera_down.png','grasshopper.png']
    n = 0
    for tile in tiles:
        tiles[n] = Text2List(tile,';',True)
        n += 1
    for tile in tiles:
        tile[0] = Text2List(tile[0],'+')
    tile_map = {}
    spawn = [0,0]
    # left, top, right, bottom
    edges = [99999,99999,-99999,-99999]
    for tile in tiles:
        delete = []
        n = 0
        for img in tile[0]:
            if img in item_list:
                delete.append(n)
                items.append([img, tile[1]*32, tile[2]*32, random.randint(0,6)-3])
            if img[:-4] in decor_list:
                delete.append(n)
                decor.append([img, tile[1]*32, tile[2]*32])
            if img == 'spawn.png':
                delete.append(n)
                spawn = [tile[1]*32+12,tile[2]*32+17]
            n += 1
        delete.sort(reverse=True)
        for img in delete:
            tile[0].pop(img)
        if tile[0] != []:
            tile_map[str(tile[1]) + ';' + str(tile[2])] = tile
        if tile[2]*32 > edges[3]:
            edges[3] = tile[2]*32
        if tile[2]*32 < edges[1]:
            edges[1] = tile[2]*32
        if tile[1]*32 > edges[2]:
            edges[2] = tile[1]*32
        if tile[1]*32 < edges[0]:
            edges[0] = tile[1]*32
    return tile_map, items, decor, spawn, edges

def line_collide(start, end, tiles):
    x = start[0]
    y = start[1]
    dis_x = end[0]-start[0]
    dis_y = end[1]-start[1]
    rate_x = dis_x / (abs(dis_x) + abs(dis_y))
    rate_y = dis_y / (abs(dis_x) + abs(dis_y))
    hit = False
    while True:
        x += rate_x * 3
        y += rate_y * 3
        if abs(end[0] - x) <= 8:
            if abs(end[1] - y) <= 8:
                break
        target = str(int(round(x/32,0))) + ';' + str(int(round(y/32,0)))
        if target in tiles:
            for img in tiles[target][0]:
                if img[:-4] in collision_types:
                    hit = True
                    break
    return hit

def gen_clouds(edges):
    cloud_list = ['cloud_0','cloud_1','cloud_2','cloud_3']
    x = edges[0]
    y = edges[1]
    x -= 320
    y -= 320
    size_x = edges[2]-edges[0]
    size_y = edges[3]-edges[1]
    size_x += 640
    size_y += 640
    area = size_x * size_y
    clouds = []
    for depth in range(3):
        depth = 4-depth
        for i in range(int(area/(1024*90))):
            clouds.append([random.choice(cloud_list),random.randint(x,x+size_x)/depth,random.randint(y,y+size_y)/depth,depth])
    return clouds

# Title Screen ----------------------------------------------- #
global run_type
run_type = 'classic' # classic, segmented speedrun, one-shot speedrun
global map_set
map_set = 'standard' # standard
def find(l,target):
    loc = 0
    for item in l:
        if item == target:
            break
        loc += 1
    if loc == len(l):
        loc = -1
    return loc
def title_screen():
    global run_type, map_set, screen, WINDOWWIDTH, WINDOWHEIGHT
    map_sets = ['standard']
    run_types = ['classic', 'segmented speedrun', 'one-shot speedrun']
    map_sets_index = find(map_sets,map_set)
    run_types_index = find(run_types,run_type)

    menu_options = ['Lollipop', '', 'Play', 'Level Set: ' + map_set, 'Rules: ' + run_type, 'Exit']
    pointer = 2
    in_menu = True
    hit_zero = False
    resolutions = [[300,200],[600,400],[900,600],[1200,800]]
    resolution_index = find(resolutions,[WINDOWWIDTH,WINDOWHEIGHT])
    if resolution_index == -1:
        resolution_index = 0
    while in_menu:
        Display.fill((0,0,0))
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                WINDOWWIDTH = event.size[0]
                WINDOWHEIGHT = event.size[1]
                screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.RESIZABLE)
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    pointer += 1
                    if pointer == len(menu_options):
                        pointer = 2
                if event.key == K_UP:
                    pointer -= 1
                    if pointer == 1:
                        pointer = len(menu_options)-1
                if event.key == K_RETURN:
                    selection = menu_options[pointer]
                    if selection == '- Exit':
                        pygame.quit()
                        sys.exit()
                    if selection == '- Play':
                        in_menu = False
                    if selection == '- Level Set: ' + map_set:
                        map_sets_index += 1
                        if map_sets_index == len(map_sets):
                            map_sets_index = 0
                        map_set = map_sets[map_sets_index]
                    if selection == '- Rules: ' + run_type:
                        run_types_index += 1
                        if run_types_index == len(run_types):
                            run_types_index = 0
                        run_type = run_types[run_types_index]
                    if selection == '- Resolution: ' + str(resolutions[resolution_index][0]) + 'x' + str(resolutions[resolution_index][1]):
                        resolution_index += 1
                        if resolution_index == len(resolutions):
                            resolution_index = 0
                        WINDOWWIDTH = resolutions[resolution_index][0]
                        WINDOWHEIGHT = resolutions[resolution_index][1]
                        screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.RESIZABLE)
                    
        menu_options = ['Lollipop', '', 'Play', 'Level Set: ' + map_set, 'Rules: ' + run_type, 'Resolution: ' + str(resolutions[resolution_index][0]) + 'x' + str(resolutions[resolution_index][1]), 'Exit']
        menu_options[pointer] = '- ' + menu_options[pointer]
        y = 0
        for option in menu_options:
            ShowText(option,4,4+y*12,1,245,Font_0,Display,overflow='normal')
            y += 1
        if WINDOWWIDTH > 900:
            ShowText('Need high perfomance CPU',110,64,1,245,Font_0,Display,overflow='normal')
        ratio = WINDOWWIDTH/WINDOWHEIGHT
        if ratio < 1.5:
            width = WINDOWWIDTH
            height = WINDOWWIDTH/1.5
        else:
            height = WINDOWHEIGHT
            width = WINDOWHEIGHT*1.5
        screen.blit(pygame.transform.scale(Display,(int(width),int(height))),(0,0))
        pygame.display.update()
        mainClock.tick(40)
title_screen()

# Audio ------------------------------------------------------ #
poof_sound = pygame.mixer.Sound('data/SFX/poof.wav')
bomb_sound = pygame.mixer.Sound('data/SFX/bomb_poof.wav')
click_sound = pygame.mixer.Sound('data/SFX/click.wav')
slide_sound = pygame.mixer.Sound('data/SFX/slide.wav')
eat_sound = pygame.mixer.Sound('data/SFX/eat.wav')
bounce_sound = pygame.mixer.Sound('data/SFX/bounce.wav')
jump_sound = pygame.mixer.Sound('data/SFX/jump.wav')
grass_0_sound = pygame.mixer.Sound('data/SFX/grass_0.wav')
grass_1_sound = pygame.mixer.Sound('data/SFX/grass_1.wav')
stone_0_sound = pygame.mixer.Sound('data/SFX/stone_0.wav')
stone_1_sound = pygame.mixer.Sound('data/SFX/stone_1.wav')
poof_sound = pygame.mixer.Sound('data/SFX/poof.wav')
ambience_sound = pygame.mixer.Sound('data/SFX/ambience.wav')
music = pygame.mixer.Sound('data/music/main.wav')
music.set_volume(0.15)
slide_channel = pygame.mixer.Channel(31)
slide_sound.set_volume(0.15)
bomb_sound.set_volume(0.4)
jump_sound.set_volume(0.3)
stone_0_sound.set_volume(0.3)
stone_1_sound.set_volume(0.3)
click_sound.set_volume(0.3)
VOs = {}
VO_list = ['hey','huh_1','huh_2','I_cant_see_him','stop','umm','what','what_are_you_doing','where_did_he_go','hehe','you_cant_see_me','Im_gone','oh_no','stop_staring','dont_look']
for sound in VO_list:
    VOs[sound] = pygame.mixer.Sound('data/vo/' + sound + '.wav')
# Variables -------------------------------------------------- #
ninja_gravity = 0
ninja_slide = 0
right = False
left = False
ninja_direction = 'r'
ninja_ground_timer = 0
global scroll_x, scroll_y
scroll_x = 0
scroll_y = 0
right_cooldown = 0
left_cooldown = 0
wait_to_jump = 0
invisibility_timer = 0
opacity = 255
bombs = []
particles = []
health = 300
invisible_areas = []
win = 0
lose = 0
loss_message = ''
loss_messages = ['Great, you\'ve made a scene.','You\'ve drawn too much attention.','He\'s staring at you...','*INTERNAL SCREAMING*']
fade = 0
bomb_cooldown = 0
jump_name = 'UP'
arrow_keys_name = 'arrow keys'
x_name = 'X'
c_name = 'C'

wall_jump_count = 0


text_box = ['Use the ' + arrow_keys_name + ' to move.',160]
level_text = {'standard':{1:'Use the ' + arrow_keys_name + ' to move.',2:'Use ' + jump_name + ' to jump.',3:'Use ' + jump_name + ' to wall jump. Just hold one direction and press jump when between walls.',4:'Practice some more jumping.',5:'Don\'t let people stare at you for too long.',6:'Use ' + x_name + ' to go invisible so people don\'t stare at you.',7:'This looks tricky...',8:'Surround people in smoke using ' + c_name + ' so you go unseen.',
                          9:'What a lovely pit.',10:'Scrrraaaaaaaaape...',11:'Where\'s the lollipop?',12:'Sugar.',13:'All I wanted was a lollipop...',14:'Hey look! Another hole...',15:'This seems familiar.',16:'Almost sated.'}}


particle_animations = []

stick_tilt = 0
a_button = 0
l_trigger = 0
r_trigger = 0

ambience_sound.play(-1)
slide_channel.play(slide_sound,-1)
music.play(-1)

current_level = 1



level, items, decor, spawn, edges = load_map(map_set + '/level_' + str(current_level))
clouds = gen_clouds(edges)
void = edges[3]+32
ninja = entities.entity(spawn[0],spawn[1],8,15)

speedrun_score = 0 # for one-shot speedrun
speedrun_scores = [] # for segmented speedrun

cam_time = 0
cam_mode = None

text_box = [level_text[map_set][current_level],160]
# FPS -------------------------------------------------------- #
FPS = 80
TrueFPSCount = 0
TrueFPS = 0
fpsOn = False
PrevNow = 0
frame_num = 0
# Loop ------------------------------------------------------- #
while True:
    # FPS ---------------------------------------------------- #
    frame_num += 1
    NewSec = False
    TrueFPSCount += 1
    now = datetime.now()
    now = now.second
    if PrevNow != now:
        PrevNow = now
        NewSec = True
        TrueFPS = TrueFPSCount
        TrueFPSCount = 0
        TrueFPS = str(TrueFPS)
    # Background --------------------------------------------- #
    Display.fill(SKY)

    m_x = int((ninja.x-(scroll_x+150))/10)
    m_y = int((ninja.y-(scroll_y+100))/10)
    scroll_x += m_x
    scroll_y += m_y

    stare_map = pygame.Surface((300,200))
    stare_map.fill((24,24,35))
    stares = []

    if cam_mode == 'd':
        scroll_y += int(cam_time/2)
    if cam_mode == 'dr':
        scroll_y += int(cam_time/3)
        scroll_x += int(cam_time/7)
    if cam_mode == 'dl':
        scroll_y += int(cam_time/3)
        scroll_x -= int(cam_time/7)

    end_level = 8
    if map_set == 'standard':
        end_level = 17

    # Clouds ------------------------------------------------- #
    for cloud in clouds:
        Display.blit(cloud_index[cloud[0]],(cloud[1]-scroll_x/cloud[3],cloud[2]-scroll_y/cloud[3]))
    
    # Decor -------------------------------------------------- #
    for thing in decor:
        if abs(thing[1]-(scroll_x+150)) < 200:
            if abs(thing[2]-(scroll_y+150)) < 200:
                if thing[0] == 'torch_r.png':
                    for i in range(random.randint(1,2)):
                        particles.append([thing[1]+26,thing[2]+14,(random.randint(0,20)-20)/20,(random.randint(0,10)-10)/10,random.choice([(225,176,62),(214,78,78)]),True,random.randint(10,20),random.randint(1,2),'spark'])
                if thing[0] == 'torch_l.png':
                    for i in range(random.randint(1,2)):
                        particles.append([thing[1]+6,thing[2]+14,(random.randint(0,20))/20,(random.randint(0,10)-10)/10,random.choice([(225,176,62),(214,78,78)]),True,random.randint(10,20),random.randint(1,2),'spark'])
        Display.blit(tile_database[thing[0]],(thing[1]-scroll_x,thing[2]-scroll_y))

    # Particle Animations ------------------------------------ #
    for animation in particle_animations:
        try:
            animation[1].play(animation[0],Display,animation[2],True,[-scroll_x,-scroll_y])
        except KeyError:
            particle_animations.remove(animation)
    
    # Items -------------------------------------------------- #
    cam_mode = None
    
    ninja_visible = True
    
    if opacity != 255:
        ninja_visible = False
    
    for r in invisible_areas:
        if ninja.obj.rect.colliderect(r):
            ninja_visible = False

    if (win > 0) or (lose > 0):
        ninja_visible = False
    
    stared_at = False
    for item in items:
        if item[0] == 'lollipop.png':
            item[3] += 0.125
            if item[3] > 3:
                item[3] = -3
            if item[3] > 0:
                y_change = item[3]
            else:
                y_change = -item[3]
            itemR = pygame.Rect(item[1]+14,item[2]+11,5,10)
            if ninja.obj.rect.colliderect(itemR):
                win = 160
                ninja_slide = 0
                items.remove(item)
                eat_sound.play()
            width = tile_database[item[0]].get_width()
            height = tile_database[item[0]].get_height()
            Display.blit(tile_database[item[0]],(item[1]-scroll_x+(16-int(width/2)),item[2]-scroll_y+(16-int(height/2)-round(y_change,0))))
        elif item[0] == 'grasshopper.png':
            if len(item) == 4:
                item.append(0) # effect timer
            itemR = pygame.Rect(item[1],item[2],32,32)
            if ninja.obj.rect.colliderect(itemR):
                if item[4] == 0:
                    item[4] = 1
            if item[4] != 0:
                item[1] += 4
                item[2] -= 4-int(item[4]/2)
                item[4] += 1
                if item[4] > 18:
                    items.remove(item)
                img = tile_database[item[0]].copy()
                if item[4] > 8:
                    img = tile_database['grasshopper_falling.png'].copy()
                if item[4] > 14:
                    img.set_alpha(255-(item[4]-14)*50)
                Display.blit(img,(item[1]-scroll_x,item[2]-scroll_y+13))
        elif item[0][:6] == 'camera':
            itemR = pygame.Rect(item[1]+4,item[2],25,32)
            if ninja.obj.rect.colliderect(itemR):
                cam_time += 2
                if cam_time > 20:
                    cam_time = 20
                if item[0] == 'camera_down.png':
                    cam_mode = 'd'
                if item[0] == 'camera_down_right.png':
                    cam_mode = 'dr'
                if item[0] == 'camera_down_left.png':
                    cam_mode = 'dl'
        elif item[0] == 'human.png':
            if len(item) == 4:
                item.append(False)
                item.append(False)
            can_see = True
            itemR = pygame.Rect(item[1]+12,item[2]+7,7,17)
            for r in invisible_areas:
                if r.colliderect(itemR):
                    can_see = False
                    if item[5] == True:
                        VOs[random.choice(['huh_1','huh_2','I_cant_see_him','umm','what','where_did_he_go'])].play()
                        
                    item[5] = False
            if can_see == True:
                item[5] = True
            if can_see == True:
                if ninja_visible == True:
                    if line_collide([item[1]+6,item[2]+10], [ninja.x,ninja.y-4], level) == False:
                        stares.append([item[1]+16,item[2]+16])
                        stared_at = True
                        if item[4] == False:
                            item[4] = True
                            VOs[random.choice(['huh_1','huh_2','hey','umm','stop','what_are_you_doing'])].play()
                            
                    else:
                        item[4] = False
                else:
                    item[4] = False
            else:
                item[4] = False
            width = tile_database[item[0]].get_width()
            height = tile_database[item[0]].get_height()
            img = tile_database[item[0]].copy()
            if item[1] > ninja.x:
                img = pygame.transform.flip(img, True, False)
            Display.blit(img,(item[1]-scroll_x+(16-int(width/2)),item[2]-scroll_y+15))
                    
    invisible_areas = []
    
    if stared_at == True:
        health -= 2
        if health < 150:
            health = 150
            lose = 160
            loss_message = random.choice(loss_messages)
            VOs[random.choice(['oh_no','stop_staring','dont_look'])].play()
    else:
        health += 2
        if health > 300:
            health = 300

    if ninja.y > void:
        if lose == 0:
            lose = 160
            loss_message = 'Why have you fallen?'

    if invisibility_timer == 160:
        VOs[random.choice(['hehe','you_cant_see_me','Im_gone'])].play()
    # Ninja -------------------------------------------------- #
    if cam_time > 0:
        cam_time -= 1
    
    if wait_to_jump != 0:
        if air == False:
            ninja_gravity = -4.1
            wait_to_jump = 0
            jump_sound.play()
            particle_animations.append([jump_animation.start(ninja.x,ninja.y-1),jump_animation,False])
        elif wall == True:
            ninja_gravity = -2.7
            slide_channel.pause()
            if ninja_slide > 0:
                ninja_direction = 'l'
                ninja_slide = -13
                right_cooldown = 16
                particle_animations.append([wall_jump_animation.start(ninja.x-8,ninja.y+2),wall_jump_animation,False])
            else:
                ninja_direction = 'r'
                ninja_slide = 13
                left_cooldown = 16
                particle_animations.append([wall_jump_animation.start(ninja.x,ninja.y+2),wall_jump_animation,True])
            wait_to_jump = 0
            jump_sound.play()
            wall_jump_count += 1
            if wall_jump_count == 1:
                if ninja_ground_timer < 35:
                        if ninja_direction == 'r':
                            left_cooldown = 3
                            ninja_slide = 2
                        else:
                            right_cooldown = 3
                            ninja_slide = -2

    if invisibility_timer > 0:
        invisibility_timer -= 1
        if invisibility_timer > 170:
            opacity -= 15
            if opacity < 100:
                opacity = 100
        if invisibility_timer <= 130:
            opacity += 15
            if opacity > 255:
                opacity = 255

    right_cooldown = normalize(right_cooldown,1)
    left_cooldown = normalize(left_cooldown,1)
    if (win == 0) and (lose == 0):
        if right_cooldown == 0:
            if right == True:
                ninja_slide += 0.5
                ninja_direction = 'r'
                if air == True:
                    ninja_slide -= 0.125
        if left_cooldown == 0:
            if left == True:
                ninja_slide -= 0.5
                ninja_direction = 'l'
                if air == True:
                    ninja_slide += 0.125

    ninja_slide = normalize(ninja_slide,0.25)
    ninja_slide = cap(ninja_slide,4)
    
    ninja_movement = [ninja_slide,ninja_gravity]
    ninja_gravity += 0.25
    if ninja_gravity > 5:
        ninja_gravity = 5
    
    ninja_collisions = ninja.move(ninja_movement,nearby_tiles(ninja.x,ninja.y,level))

    try:
        tile_type = level[str(int((ninja.x+22)/32)) + ';' + str(int((ninja.y+22)/32))][0][0]
    except:
        tile_type = None
    
    air = True
    wall = False
    running = False

    ninja_ground_timer += 1
    
    if ninja_collisions['bottom'] == True:
        ninja_ground_timer = 0
        ninja_gravity = 0.75
    if ninja_ground_timer < 6:
        air = False
        wall_jump_count = 0
    if win != 0:
        ninja_img = ninja_eat
    elif (ninja_collisions['right'] == True) and (ninja_ground_timer >= 3):
        ninja_gravity = maximum(ninja_gravity,1.5)
        ninja_img = ninja_wall
        wall = True
        if right == True:
            ninja_slide = 0.875
    elif (ninja_collisions['left'] == True) and (ninja_ground_timer >= 3):
        ninja_gravity = maximum(ninja_gravity,1.5)
        ninja_img = pygame.transform.flip(ninja_wall,True,False)
        wall = True
        if left == True:
            ninja_slide = -0.875
    elif air == True:
        if ninja_direction == 'r':
            ninja_img = ninja_jump
        else:
            ninja_img = pygame.transform.flip(ninja_jump,True,False)
    elif ninja_movement[0] == 0:
        if ninja_direction == 'r':
            ninja_img = ninja_stand
        else:
            ninja_img = pygame.transform.flip(ninja_stand,True,False)
    else:
        running = True
        ninja.update_animation(ninja_run,ninja_run_key)
        if ninja_direction == 'r':
            ninja_run.play(ninja_run_key,Display,False,True,[-4-scroll_x,-3-scroll_y],opacity)
        else:
            ninja_run.play(ninja_run_key,Display,True,True,[-4-scroll_x,-3-scroll_y],opacity)
    if running == False:
        ninja_run.reset(ninja_run_key)
        ninja_img.set_alpha(opacity)
        Display.blit(ninja_img,(ninja.x-4-scroll_x,ninja.y-3-scroll_y))
    elif random.randint(1,5) == 1:
        if tile_type != None:
            if (tile_type[:5] == 'grass') or (tile_type[:4] == 'dirt'):
                random.choice([grass_0_sound,grass_1_sound]).play()
                if ninja_direction == 'r':
                    for i in range(4):
                        particles.append([ninja.x+8,ninja.y+14,(random.randint(0,20))/20,(random.randint(10,25)-25)/10,random.choice([(51,120,115),(106,183,115)]),True,random.randint(10,20),1,'spark'])
                else:
                    for i in range(4):
                        particles.append([ninja.x+8,ninja.y+14,(random.randint(0,20)-20)/20,(random.randint(10,25)-25)/10,random.choice([(51,120,115),(106,183,115)]),True,random.randint(10,20),1,'spark'])
    if wall == False:
        slide_channel.pause()
    elif ninja_gravity > 0:
        slide_channel.unpause()
        
    # Bombs -------------------------------------------------- #
    for bomb in bombs:
        obj = entities.PhysicsObject(bomb[0],bomb[1],3,3)
        collisions = obj.Move([bomb[2],bomb[3]],nearby_tiles(bomb[0],bomb[1],level))
        if (collisions['left'] == True) or (collisions['right'] == True):
            bomb[2] = -bomb[2]
            bounce_sound.play()
        if collisions['bottom'] == True:
            bomb[3] = int(-bomb[3] * 0.3)
            bomb[2] = normalize(bomb[2],1)
        if collisions['top'] == True:
            bomb[3] = -bomb[3]
            bounce_sound.play()
        bomb[0] = obj.x
        bomb[1] = obj.y
        bomb[4] -= 1
        bomb[2] = normalize(bomb[2],0.05)
        bomb[3] += 0.25
        if bomb[3] > 4:
            bomb[3] = 4
        if bomb[4] <= 0:
            bombs.remove(bomb)
        if bomb[4] == 200:
            bomb_sound.play()
        if bomb[4] <= 200:
            invisible_areas.append(pygame.Rect(bomb[0]-30,bomb[1]-30,63,33))
            for i in range(random.randint(2,3)):
                size = random.randint(1,24)
                # x, y, x momentum, y momentum, color, physics, duration, size, type
                particles.append([bomb[0]+random.randint(0,3),bomb[1]+random.randint(0,3)-int(size/2),random.randint(0,4)-2,random.randint(1,3)-3,random.choice([(222,208,184),(230,222,208),(206,184,138)]),True,random.randint(5,30),size,'smoke'])
        Display.blit(bomb_img,(bomb[0]-scroll_x,bomb[1]-scroll_y))

    # Particles ---------------------------------------------- #
    for particle in particles:
        if particle[5] == False:
            particle[0] += particle[2]
            particle[1] += particle[3]
        else:
            obj = entities.PhysicsObject(particle[0],particle[1],1,1)
            collisions = obj.Move([particle[2],particle[3]],nearby_tiles(particle[0],particle[1],level))
            particle[0] = obj.x
            particle[1] = obj.y
        if particle[8] == 'smoke':
            particle[2] = normalize(particle[2],0.05)
            particle[3] += 0.2
            if random.randint(1,2) == 1:
                particle[7] -= 1
                particle[6] += 5
            if particle[7] < 1:
                particle[7] = 1
                particle[6] -= 10
        if particle[8] == 'poof':
            particle[3] = normalize(particle[3],0.005)
            particle[2] = normalize(particle[2],0.005)
            particle[3] -= 0.005
        if particle[8] == 'spark':
            particle[3] = normalize(particle[3],0.02)
            particle[2] = normalize(particle[2],0.02)
            particle[3] += 0.15
        if particle[3] > 3:
            particle[3] = 3
        s = pygame.Surface((particle[7],particle[7]))
        s.fill(particle[4])
        Display.blit(s,(particle[0]-scroll_x-int(particle[7]/2),particle[1]-scroll_y-int(particle[7]/2)))
        particle[6] -= 1
        if particle[6] < 0:
            particles.remove(particle)
        elif particle[5] == True:
            if collisions['bottom'] == True:
                particles.remove(particle)

    # Tiles -------------------------------------------------- #
    visible_tiles = []
    for y in range(9):
        for x in range(12):
            target_x = x-1 + int(scroll_x/32)
            target_y = y-1 + int(scroll_y/32)
            target = str(target_x) + ';' + str(target_y)
            if target in level:
                visible_tiles.append(level[target])
    for tile in visible_tiles:
        for img in tile[0]:
            if img[:5] != 'grass':
                Display.blit(tile_database[img],(tile[1]*32-scroll_x,tile[2]*32-scroll_y))
            else:
                Display.blit(tile_database[img],(tile[1]*32-scroll_x,tile[2]*32-5-scroll_y))


    

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            WINDOWWIDTH = event.size[0]
            WINDOWHEIGHT = event.size[1]
            screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.RESIZABLE)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                title_screen()
                current_level = 1
  
                if run_type == 'classic':
                        pass
                level, items, decor, spawn, edges = load_map(map_set + '/level_' + str(current_level))
                clouds = gen_clouds(edges)
                void = edges[3]+32
                text_box = [level_text[map_set][current_level],160]
                ninja = entities.entity(spawn[0],spawn[1],8,15)
                bombs = []
                particles = []
                speedrun_score = 0
                speedrun_scores = []
            if (win == 0) and (lose == 0):
                if event.key == K_RIGHT:
                    right = True
                    if ninja_direction == 'l':
                        left = False
                        particle_animations.append([turn_animation.start(ninja.x-4,ninja.y-1),turn_animation,True])
                if event.key == K_LEFT:
                    left = True
                    if ninja_direction == 'r':
                        right = False
                        particle_animations.append([turn_animation.start(ninja.x-4,ninja.y-1),turn_animation,False])
            if event.key == K_UP:
                if (win == 0) and (lose == 0):
                    wait_to_jump = 5
            if event.key == K_x:
                if (win == 0) and (lose == 0):
                    if invisibility_timer == 0:
                        invisibility_timer = 180
                        poof_sound.play()
                        for item in items:
                            if item[0] == 'human.png':
                                if item[4] == True:
                                    VOs[random.choice(['huh_1','huh_2','I_cant_see_him','umm','what','where_did_he_go'])].play()
                                    
                        for i in range(40):
                            size = random.randint(1,4)
                            particles.append([ninja.x+random.randint(0,8),ninja.y+random.randint(0,15)-int(size/2),(random.randint(0,20)-10)/20,(random.randint(0,10)-10)/10,(132,136,155),True,random.randint(20,40),size,'poof'])
                    else:
                        click_sound.play()
            if event.key == K_c:
                if (win == 0) and (lose == 0):
                    if bomb_cooldown == 0:
                        bomb_cooldown = 60
                        if ninja_direction == 'r':
                            bombs.append([ninja.x+4,ninja.y+4,5,-2,240])
                        else:
                            bombs.append([ninja.x+4,ninja.y+4,-5,-2,240])
                    else:
                        click_sound.play()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False

    wait_to_jump = normalize(wait_to_jump,1)

    # Update ------------------------------------------------- #
    update_frame = False
    if int(TrueFPS) > 33:
        update_frame = True
    elif int(TrueFPS) > 25:
        if frame_num % 2 == 0:
            update_frame = True
    elif int(TrueFPS) > 15:
        if frame_num % 4 == 0:
            update_frame = True

    if update_frame == True:    
        display_copy = pygame.transform.scale(Display,(health,int(round(health * (2/3),0))))
        display_copy = pygame.transform.scale(display_copy,(300,200))
        Display = display_copy.copy()

    # Stares ------------------------------------------------- #
    if update_frame == True: 
        for stare in stares:
            pygame.draw.polygon(stare_map,(255,0,255),get_spotlight_points([stare[0]-scroll_x,stare[1]-scroll_y],[ninja.x+4-scroll_x,ninja.y+4-scroll_y]))
        stare_map.set_colorkey((255,0,255))
        stare_map.set_alpha(150-int(health/2))
        if health < 290:
            Display.blit(stare_map,(0,0))
    
    # GUI ---------------------------------------------------- #
    if win > 0:
        win -= 1
        Display.blit(lollipop_img,(78,48-minimum(win-155.2,0)*10))
        Display.blit(textbox_img,(114+minimum(win-141.4,0)*10,44))
        ShowText('Hunted',126+minimum(win-141.4,0)*10,49,1,300,Font_0,Display,overflow='normal')
        ShowText('Level completed.',123+minimum(win-141.4,0)*10,58,1,300,Font_0,Display,overflow='normal')
        if win == 100:
            win = 26
        if win == 25:
            fade = 100
        if win == 1:
            current_level += 1
            if run_type == 'classic':

                pass
            if current_level != end_level:
                level, items, decor, spawn, edges = load_map(map_set + '/level_' + str(current_level))
                clouds = gen_clouds(edges)
                void = edges[3]+32
                text_box = [level_text[map_set][current_level],160]
                ninja = entities.entity(spawn[0],spawn[1],8,15)
                bombs = []
                particles = []
            elif run_type == 'classic':

                pass
            if run_type == 'segmented speedrun':
                speedrun_scores.append(speedrun_score)
                speedrun_score = 0
    if lose > 0:
        lose -= 1
        #Display.blit(lollipop_img,(78,48-minimum(lose-155.2,0)*10))
        Display.blit(textbox_img,(114+minimum(lose-141.4,0)*10,44))
        ShowText(loss_message,126+minimum(lose-141.4,0)*10,49,1,300,Font_0,Display,overflow='normal')
        ShowText('You\'ve failed.',123+minimum(lose-141.4,0)*10,58,1,300,Font_0,Display,overflow='normal')
        if lose == 1:
            level, items, decor, spawn, edges = load_map(map_set + '/level_' + str(current_level))
            clouds = gen_clouds(edges)
            void = edges[3]+32
            text_box = [level_text[map_set][current_level],160]
            ninja = entities.entity(spawn[0],spawn[1]-2,8,15)
            bombs = []
            particles = []
            ninja_gravity = -1
            if run_type == 'segmented speedrun':
                speedrun_score = 0
        if lose == 100:
            lose = 26
        if lose == 25:
            fade = 100
    if text_box[1] > 0:
        if text_box[1] > 150:
            y = 10-(text_box[1]-150)
        elif text_box[1] < 10:
            y = text_box[1]
        else:
            y = 10
        text_box[1] -= 1
        Display.blit(textbox_img_2,(45,200-y*3))
        ShowText(text_box[0],49,204-y*3,1,204,Font_0,Display,overflow='normal')
    Display.blit(bomb_icon,(2,2))
    Display.blit(invisibility_icon,(2,22))
    if bomb_cooldown == 0:
        Display.blit(ready_img,(2,2))
    if invisibility_timer == 0:
        Display.blit(ready_img,(2,22))
    height = int((invisibility_timer/180)*16)
    cooldown_img_2 = pygame.Surface((16,height))
    cooldown_img_2.set_alpha(210)
    Display.blit(cooldown_img_2,(3,23+(16-height)))
    if bomb_cooldown > 0:
        bomb_cooldown -= 1
    height = int((bomb_cooldown/60)*16)
    cooldown_img = pygame.Surface((16,height))
    cooldown_img.set_alpha(210)
    Display.blit(cooldown_img,(3,3+(16-height)))

    if run_type == 'one-shot speedrun':
        speedrun_score += 1
        ShowText('frames: ' + str(speedrun_score),40,4,1,211,Font_1,Display,overflow='normal')
        ShowText('approx. time: ' + frames_to_time(speedrun_score),40,16,1,211,Font_1,Display,overflow='normal')
    elif run_type == 'segmented speedrun':
        speedrun_score += 1
        ShowText('frames: ' + str(sum(speedrun_scores)+speedrun_score),40,4,1,211,Font_1,Display,overflow='normal')
        ShowText('approx. time: ' + frames_to_time(sum(speedrun_scores)+speedrun_score),40,16,1,211,Font_1,Display,overflow='normal')
    # Fade --------------------------------------------------- #
    if update_frame == True: 
        black = pygame.Surface((300,200))
        if fade > 50:
            black.set_alpha(int((100-fade)*5.1))
        elif fade != 0:
            black.set_alpha(int(fade*5.1))
        if fade != 0:
            fade -= 2
            Display.blit(black,(0,0))
    # Update ------------------------------------------------- #
    if update_frame == True:
        screen.fill((24,24,35))
        ratio = WINDOWWIDTH/WINDOWHEIGHT
        height_center = 0
        width_center = 0
        if ratio < 1.5:
            width = WINDOWWIDTH
            height = WINDOWWIDTH/1.5
            height_center = int((WINDOWHEIGHT-height)/2)
        else:
            height = WINDOWHEIGHT
            width = WINDOWHEIGHT*1.5
            width_center = int((WINDOWWIDTH-width)/2)
        screen.blit(pygame.transform.scale(Display,(int(width),int(height))),(width_center,height_center))
        pygame.display.update()
    mainClock.tick(40)

    if current_level == end_level:
        break

while True:
    Display.fill((24,24,35))
    Display.blit(lollipop_img,(260,150))
    extra = ''
    if run_type == 'segmented speedrun':
        extra = '\nSegmented Speedrun\nframe count: ' + str(sum(speedrun_scores))
        extra += '\napprox. time: ' + frames_to_time(sum(speedrun_scores))
    if run_type == 'one-shot speedrun':
        extra = '\nOne-Shot Speedrun\nframe count: ' + str(speedrun_score)
        extra += '\napprox. time: ' + frames_to_time(speedrun_score)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    ratio = WINDOWWIDTH/WINDOWHEIGHT
    height_center = 0
    width_center = 0
    if ratio < 1.5:
        width = WINDOWWIDTH
        height = WINDOWWIDTH/1.5
        height_center = int((WINDOWHEIGHT-height)/2)
    else:
        height = WINDOWHEIGHT
        width = WINDOWHEIGHT*1.5
        width_center = int((WINDOWWIDTH-width)/2)
    screen.blit(pygame.transform.scale(Display,(int(width),int(height))),(width_center,height_center))
    pygame.display.update()
    mainClock.tick(40)
    
    
