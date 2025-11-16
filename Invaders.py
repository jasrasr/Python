
import sys
import subprocess
import os

# Check and install pygame if not already installed
try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

import random

pygame.init()

# Fullscreen mode
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders - Choose Your Player")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, int(screen_height * 0.05))

scale_x = screen_width / 800
scale_y = screen_height / 600

# Player data
usernames = ["Jason", "Matt", "Thomas", "Cameron", "Justin", "Jimmy", "Other"]
selected_player = None
player_image = None
enemy_images = []

def show_menu():
    global selected_player
    menu_running = True
    selected_index = 0

    while menu_running:
        screen.fill(BLACK)
        for idx, name in enumerate(usernames):
            color = YELLOW if idx == selected_index else WHITE
            text = font.render(name, True, color)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, int(150 * scale_y) + idx * int(60 * scale_y)))

        pygame.display.flip()

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_index = (selected_index - 1) % len(usernames)
        elif event.key == pygame.K_DOWN:
            selected_index = (selected_index + 1) % len(usernames)
        elif event.key == pygame.K_RETURN:
            selected_player = usernames[selected_index]
            menu_running = False
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

                
# --- Save score data ---
score_data[selected_player]["history"].append({
    "score": score,
    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
})

if score > score_data[selected_player]["high_score"]:
    score_data[selected_player]["high_score"] = score

with open(score_file, "w") as f:
    json.dump(score_data, f, indent=2)

pygame.quit()
sys.exit()

                    
# --- Save score data ---
score_data[selected_player]["history"].append({"score": score, "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
if score > score_data[selected_player]["high_score"]:
    score_data[selected_player]["high_score"] = score
with open(score_file, "w") as f:
    json.dump(score_data, f, indent=2)

pygame.quit()

                    sys.exit()

# --- Load player/enemy images based on selected user and enforce image size ---
def load_player_and_enemies():
    global player_image, enemy_images

    base_names = ["Jason", "Matt", "Thomas", "Cameron", "Justin", "Jimmy"]
    if selected_player not in base_names:
        player_file = "Other.png"
        enemy_names = base_names
    else:
        player_file = f"{selected_player}.png"
        enemy_names = [name for name in base_names if name != selected_player]

    # Load player image
    raw = pygame.image.load(player_file)
    player_width = int(64 * scale_x)
    player_height = int(40 * scale_y)
    player_image = pygame.transform.scale(raw, (player_width, player_height))

    # Load enemy images
    enemy_images = []
    for name in enemy_names:
        try:
            raw = pygame.image.load(f"{name}.png")
            scaled = pygame.transform.scale(raw, (int(64 * scale_x), int(64 * scale_y)))
            enemy_images.append(scaled)
        except:
            pass  # skip if missing

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, int(64 * scale_x), int(64 * scale_y))
        self.image = random.choice(enemy_images)

def render_text(text, pos, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, pos)

# Run menu and setup
show_menu()
load_player_and_enemies()

# --- GAME LOGIC ---

# Initialize game state
player_width = int(64 * scale_x)
player_height = int(40 * scale_y)
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - int(10 * scale_y)
player_speed = int(6 * scale_x)

bullet_width = int(5 * scale_x)
bullet_height = int(10 * scale_y)
bullet_speed = int(7 * scale_y)
bullets = []

enemy_width = int(64 * scale_x)
enemy_height = int(64 * scale_y)
enemy_direction = 1
enemy_drop = int(20 * scale_y)

score = 0
level = 1

def create_enemies(level, cols=8, rows=3):
    enemies = []
    for row in range(rows):
        for col in range(cols):
            x = int(100 * scale_x) + col * (enemy_width + int(20 * scale_x))
            y = int(50 * scale_y) + row * (enemy_height + int(20 * scale_y))
            enemies.append(Enemy(x, y))
    return enemies

enemies = create_enemies(level)
enemy_speed = int(2 * scale_x) + level * 0.5



# --- Load or initialize score history ---
import json
import shutil
from datetime import datetime

score_file = "score_history.json"
backup_file = "score_history_backup.json"
score_data = {}
if os.path.exists(score_file):
    try:
        with open(score_file, "r") as f:
            score_data = json.load(f)
        shutil.copy(score_file, backup_file)
    except:
        score_data = {}

if selected_player not in score_data:
    score_data[selected_player] = {"high_score": 0, "history": []}
high_score = score_data[selected_player]["high_score"]

# Check for reset (press R key)
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        score_data[selected_player] = {"high_score": 0, "history": []}
        with open(score_file, "w") as f:
            json.dump(score_data, f, indent=2)
        high_score = 0

import json
score_file = "score_history.json"
score_data = {}
if os.path.exists(score_file):
    try:
        with open(score_file, "r") as f:
            score_data = json.load(f)
    except:
        score_data = {}

if selected_player not in score_data:
    score_data[selected_player] = {"high_score": 0, "history": []}
high_score = score_data[selected_player]["high_score"]

running = True
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height)
            bullets.append(bullet)

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    shift = False
    for enemy in enemies:
        enemy.rect.x += enemy_speed * enemy_direction
        if enemy.rect.right >= screen_width or enemy.rect.left <= 0:
            shift = True

    if shift:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.rect.y += enemy_drop

    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Draw everything
    screen.blit(player_image, (player_x, player_y))
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

    render_text(f"Score: {score}", (int(10 * scale_x), int(10 * scale_y)))
    render_text(f"Level: {level}", (int(10 * scale_x), int(60 * scale_y)))

    if not enemies:
        level += 1
        bullets.clear()
        player_x = (screen_width - player_width) // 2
        enemies = create_enemies(level)
        enemy_speed = int(2 * scale_x) + level * 0.5

    pygame.display.flip()
    clock.tick(60)


# --- Save score data ---
score_data[selected_player]["history"].append({"score": score, "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
if score > score_data[selected_player]["high_score"]:
    score_data[selected_player]["high_score"] = score
with open(score_file, "w") as f:
    json.dump(score_data, f, indent=2)

pygame.quit()

