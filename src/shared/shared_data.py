import os
import yaml

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.abspath(WORKING_DIR + "/../../assets/")
CARDS_DIR = os.path.abspath(ASSET_DIR + "/cards/")
BACKGROUND_DIR = os.path.abspath(ASSET_DIR + "/backgrounds/")
UI_DIR = os.path.abspath(ASSET_DIR + "/ui/")
USER_SETTINGS_PATH = os.path.abspath(WORKING_DIR + "/../../usersettings.yml")

with open(os.path.abspath(WORKING_DIR + "/../../appsettings.yml"), 'r') as app_file:
    appsettings = yaml.safe_load(app_file)

LOCAL = appsettings["local"]
DEBUG = appsettings["debug"]
WIN_WIDTH = appsettings["window"]["width"]
WIN_HEIGHT = appsettings["window"]["width"]
CENTER = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
FPS = appsettings["window"]["fps"]
BUTTON_WIDTH = appsettings["buttons"]["classic"]["width"]
BUTTON_HEIGHT = appsettings["buttons"]["classic"]["height"]
IMAGE_BUTTON_WIDTH = appsettings["buttons"]["images"]["width"]
IMAGE_BUTTON_HEIGHT = appsettings["buttons"]["images"]["height"]
GAMES = appsettings["games"]
FONT_FAMILY = appsettings["font"]["family"]
FONT_SIZE = appsettings["font"]["size"]
BACKGROUND_COUNT = appsettings["backgrounds"]["count"]
BACKGROUND_ROUTE = appsettings["backgrounds"]["route"]
BACKGROUND_EXTENSION = appsettings["backgrounds"]["extension"]
CARD_TYPES = appsettings["cards"]["types"]
CARD_SUITS = appsettings["cards"]["suits"]
CARD_BACKS = appsettings["cards"]["backs"]
CARD_WIDTH = appsettings["cards"]["width"]
CARD_HEIGHT = appsettings["cards"]["height"]
CARD_SPACING = appsettings["cards"]["spacing"]
CARD_ROUTE = appsettings["cards"]["route"]
CARD_EXTENSION = appsettings["cards"]["extension"]
UI_ELEMENTS = appsettings["ui"]["elements"]
UI_ROUTE = appsettings["ui"]["route"]
UI_EXTENSION = appsettings["ui"]["extension"]
ARROW_SIZE = appsettings["ui"]["arrow_size"]
BLINK_SPEED = appsettings["animation"]["blink_speed"]
OUTLINE_WIDTH = 3
HOST = "45.33.32.168"
if LOCAL:
    HOST = "localhost"
PORT = 13058
ADDR = (HOST, PORT)
END = str.encode("EOF")

RESET = 0
GAME_OVER = 1
NEW_GAME = 2
PLAY = 3

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (100, 100, 100)
BUTTON = (200, 200, 200)
OUTLINE = (255, 255, 0)
