FPS = 60
TILESIZE = 96
WIDTH = 3648
HEIGTH = 3200
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'images/game_font.ttf'
UI_FONT_SIZE = 30

COVERAGE_COLOR = '#338236'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
 
TEXT_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'


HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

weapons_info = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic':'images/weapons/sword/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'images/weapons/axe/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic':'images/weapons/sai/full.png'}
    }

magic_info = {
    'flame' : {'strength': 5, 'cost': 20, 'graphic': 'images/magic/flame/fire.png'},
    'heal' : {'strength': 20, 'cost': 10, 'graphic': 'images/magic/heal/heal.png'}
    }

enemy_info = {
    'demons': {'health': 100, 'exp': 15, 'damage': 20, 'attack_type': 'slash', 'attack_sound':'images/weapons/sword/full.png', 'speed': 3, 'resistence': 3, 'attack_radius': 80, 'notice_radius': 360},
    'wraths': {'health': 100, 'exp': 15, 'damage': 20, 'attack_type': 'slash', 'attack_sound':'images/weapons/sword/full.png', 'speed': 3, 'resistence': 3, 'attack_radius': 80, 'notice_radius': 360},
    'beasts': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw', 'attack_sound':'images/weapons/sword/full.png', 'speed': 2, 'resistence': 3, 'attack_radius': 50, 'notice_radius': 300},
    }

HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 20,
    'obstacles': -140
    }
