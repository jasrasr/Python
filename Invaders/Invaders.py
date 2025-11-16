import sys
import subprocess
import os
import random
import json
import shutil
from datetime import datetime

# --- Check and install pygame if missing ---
try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

pygame.init()

# --- Fullscreen Setup ---
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders - Character Select")

# --- UI Settings ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont(None, int(screen_height * 0.05))
clock = pygame.time.Clock()

scale_x = screen_width / 800
scale_y = screen_height / 600

# --- Supported Users ---
usernames = ["Jason", "Matt", "Thomas", "Cameron", "Justin", "Jimmy", "Other"]
selected_player = None
player_image = None
enemy_images = []

# ------------------------------
#        MENU SYSTEM
# ------------------------------
def show_menu():
    global selected_player
    menu_running = True
    selected_index = 0

    while menu_running:
        screen.fill(BLACK)

        title = font.render("Select Your Character", True, YELLOW)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, int(60 * scale_y)))

        for idx, name in enumerate(usernames):
            color = YELLOW if idx == selected_index else WHITE
            text = font.render(name, True, color)
            screen.blit(
                text,
                (screen_width // 2 - text.get_width() // 2, int(160 * scale_y) + idx * int(60 * scale_y))
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

# ------------------------------
#    PLAYER & ENEMY IMAGES
# ------------------------------
def load_player_and_enemies():
    global player_image, enemy_images, player_width, player_height

    base_names = ["Jason", "Matt", "Thomas", "Cameron", "Justin", "Jimmy"]

    # Determine which images are enemies vs player
    if selected_player not in base_names:
        player_file = "Other.png"
        enemy_names = base_names
    else:
        player_file = f"{selected_player}.png"
        enemy_names = [n for n in base_names if n != selected_player]

    # --- Load & Resize Player Image ---
    raw = pygame.image.load(player_file)
    max_w = int(80 * scale_x)
    max_h = int(80 * scale_y)

    ratio = min(max_w / raw.get_width(), max_h / raw.get_height())
    player_width = int(raw.get_width() * ratio)
    player_height = int(raw.get_height() * ratio)

    player_image = pygame.transform.scale(raw, (player_width, player_height))

    # --- Load & Resize Enemy Images ---
    enemy_images.clear()
    for name in enemy_names:
        path = f"{name}.png"
        if os.path.exists(path):
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (int(64 * scale_x), int(64 * scale_y)))
            enemy_images.append(img)

# ------------------------------
#    ENEMY CLASS
# ------------------------------
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, int(64 * scale_x), int(64 * scale_y))
        self.image = random.choice(enemy_images)

# ------------------------------
#    ENEMY WAVE GENERATOR
# ------------------------------
def create_enemies(level, cols=8, rows=3):
    enemies = []
    for row in range(rows):
        for col in range(cols):
            x = int(100 * scale_x) + col * (int(64 * scale_x) + int(20 * scale_x))
            y = int(50 * scale_y) + row * (int(64 * scale_y) + int(20 * scale_y))
            enemies.append(Enemy(x, y))
    return enemies

# ------------------------------
#          DRAW TEXT
# ------------------------------
def render_text(text, pos, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, pos)

# ------------------------------
#          STARTUP
# ------------------------------
show_menu()
load_player_and_enemies()

# ------------------------------
#        PLAYER STATE
# ------------------------------
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - int(10 * scale_y)
player_speed = int(6 * scale_x)

# ------------------------------
#        BULLET STATE
# ------------------------------
bullets = []
bullet_width = int(5 * scale_x)
bullet_height = int(10 * scale_y)
bullet_speed = int(7 * scale_y)

# ------------------------------
#        SCORE SYSTEM
# ------------------------------
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

# ------------------------------
#          GAME STATE
# ------------------------------
score = 0
level = 1
enemy_speed = int(2 * scale_x)
enemy_direction = 1
enemy_drop = int(20 * scale_y)
enemies = create_enemies(level)

# ------------------------------
#          GAME LOOP
# ------------------------------
running = True
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player_x + player_width // 2 - bullet_width // 2,
                    player_y,
                    bullet_width,
                    bullet_height
                )
                bullets.append(bullet)

            elif event.key == pygame.K_r:
                score_data[selected_player] = {"high_score": 0, "history": []}
                with open(score_file, "w") as f:
                    json.dump(score_data, f, indent=2)
                high_score = 0

    # --- PLAYER MOVEMENT ---
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # --- BULLET MOVEMENT ---
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # --- ENEMY MOVEMENT ---
    shift = False
    for enemy in enemies:
        enemy.rect.x += enemy_speed * enemy_direction
        if enemy.rect.right >= screen_width or enemy.rect.left <= 0:
            shift = True

    if shift:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.rect.y += enemy_drop

    # --- COLLISIONS ---
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # --- DRAW EVERYTHING ---
    screen.blit(player_image, (player_x, player_y))

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

    render_text(f"Score: {score}", (int(10 * scale_x), int(10 * scale_y)))
    render_text(f"Level: {level}", (int(10 * scale_x), int(60 * scale_y)))
    render_text(f"High Score: {high_score}", (int(10 * scale_x), int(110 * scale_y)))

    # --- Recent score history ---
    recent = score_data[selected_player]["history"][-5:]
    for i, entry in enumerate(reversed(recent)):
        label = f"{entry['score']} pts @ {entry['time']}"
        render_text(label, (int(10 * scale_x), int(160 * scale_y) + i * int(40 * scale_y)))

    # --- LEVEL COMPLETE ---
    if not enemies:
        level += 1
        bullets.clear()
        player_x = (screen_width - player_width) // 2
        enemies = create_enemies(level)
        enemy_speed += 0.5

    pygame.display.flip()
    clock.tick(60)

# ------------------------------
#      SAVE SCORE ON EXIT
# ------------------------------
score_data[selected_player]["history"].append({
    "score": score,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})

if score > score_data[selected_player]["high_score"]:
    score_data[selected_player]["high_score"] = score

with open(score_file, "w") as f:
    json.dump(score_data, f, indent=2)

pygame.quit()
sys.exit()
