import pygame
import sys
import random
import math
from music_manager import MusicManager

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 90, 43)
LIGHT_BROWN = (205, 133, 63)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
CREAM = (255, 253, 208)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

# Game states
MENU = "menu"
GAME = "game"

class Player:
    def __init__(self, x, y, sprite_path=None):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 90
        self.speed = 5
        self.color = ORANGE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.held_ingredient = None
        self.held_ingredient_sprite = None
        self.sprite = None
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            except:
                self.sprite = None
        
    def move(self, keys):
        old_x, old_y = self.x, self.y
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
        
                
    def draw(self, screen, font):
        if self.sprite:
            # Draw sprite
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            # Fallback to simple shapes
            # Body
            pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
            # Head
            pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.y - 10), 15)
            # Eyes
            pygame.draw.circle(screen, BLACK, (self.rect.centerx - 5, self.rect.y - 10), 3)
            pygame.draw.circle(screen, BLACK, (self.rect.centerx + 5, self.rect.y - 10), 3)

        # Show held ingredient
        if self.held_ingredient:
            if self.held_ingredient_sprite:
                # Draw downscaled ingredient sprite
                sprite_size = 30
                sprite_x = self.rect.centerx - sprite_size // 2
                sprite_y = self.rect.y - 40
                screen.blit(self.held_ingredient_sprite, (sprite_x, sprite_y))
                # Add a small border/background
                pygame.draw.rect(screen, WHITE, (sprite_x - 2, sprite_y - 2, sprite_size + 4, sprite_size + 4), 2)
            else:
                # Fallback to text display
                text = font.render(self.held_ingredient[:4], True, WHITE)
                pygame.draw.circle(screen, GREEN, (self.rect.centerx, self.rect.y - 35), 15)
                text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 35))
                screen.blit(text, text_rect)

class IngredientStation:
    def __init__(self, x, y, ingredient_name, color, sprite_path=None):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 80
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.ingredient_name = ingredient_name
        self.color = color
        self.sprite = None
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            except:
                self.sprite = None
        
    def draw(self, screen, font):
        if self.sprite:
            # Draw sprite
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
            # Draw border
            pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        else:
            # Fallback to colored rectangles
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)
            text = font.render(self.ingredient_name[:6], True, WHITE)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
        
    def is_player_near(self, player):
        return self.rect.colliderect(player.rect.inflate(20, 20))

class CookingStation:
    def __init__(self, x, y, station_type, sprite_path=None):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.station_type = station_type  # "prep", "cook", "serve"
        self.ingredients = []
        self.cooking = False
        self.cook_timer = 0
        self.cook_time = 180  # 3 seconds at 60 FPS
        self.sprite = None
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            except:
                self.sprite = None
        
    def add_ingredient(self, ingredient):
        if len(self.ingredients) < 5:
            self.ingredients.append(ingredient)
            return True
        return False
        
    def start_cooking(self):
        if self.ingredients and not self.cooking:
            self.cooking = True
            self.cook_timer = 0
            
    def update(self):
        if self.cooking:
            self.cook_timer += 1
            if self.cook_timer >= self.cook_time:
                self.cooking = False
                return True  # Cooking complete
        return False
        
    def clear(self):
        self.ingredients = []
        self.cooking = False
        self.cook_timer = 0
        
    def draw(self, screen, font, small_font):
        # Station background
        if self.station_type == "prep":
            color = LIGHT_BROWN
            label = "PREP"
        elif self.station_type == "cook":
            color = RED
            label = "COOK"
        else:
            color = GREEN
            label = "SERVE"

        if self.sprite:
            # Draw sprite
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
            # Draw label on top
            text = font.render(label, True, WHITE)
            text_bg = pygame.Surface((text.get_width() + 6, text.get_height() + 2))
            text_bg.fill(BLACK)
            text_bg.set_alpha(180)
            screen.blit(text_bg, (self.rect.x + 8, self.rect.y + 3))
            screen.blit(text, (self.rect.x + 10, self.rect.y + 5))
        else:
            # Fallback to colored rectangles
            pygame.draw.rect(screen, color, self.rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)

            # Label
            text = font.render(label, True, WHITE)
            screen.blit(text, (self.rect.x + 10, self.rect.y + 5))
        
        # Show ingredients
        for i, ing in enumerate(self.ingredients):
            ing_text = small_font.render(ing[:4], True, BLACK)
            screen.blit(ing_text, (self.rect.x + 10 + (i % 3) * 30, self.rect.y + 35 + (i // 3) * 20))
        
        # Cooking progress
        if self.cooking:
            progress = self.cook_timer / self.cook_time
            bar_width = self.width - 20
            pygame.draw.rect(screen, WHITE, (self.rect.x + 10, self.rect.bottom - 20, bar_width, 10))
            pygame.draw.rect(screen, YELLOW, (self.rect.x + 10, self.rect.bottom - 20, bar_width * progress, 10))
            
    def is_player_near(self, player):
        return self.rect.colliderect(player.rect.inflate(20, 20))

class Customer:
    def __init__(self, name, color, order, x, y, sprite_path=None):
        self.name = name
        self.color = color
        self.order = order  # List of required ingredients
        self.x = x
        self.y = y
        self.patience = 100.0
        self.max_patience = 100.0
        self.served = False
        self.leaving = False
        self.rect = pygame.Rect(x, y, 60, 80)
        self.sprite = None
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (60, 80))
            except:
                self.sprite = None
        
    def update(self):
        if not self.served and not self.leaving:
            self.patience -= 0.05
            if self.patience <= 0:
                self.leaving = True
                
    def draw(self, screen, font, small_font):
        # Customer body
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            # Fallback to simple shapes
            pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
            pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.y - 10), 15)

            # Eyes
            pygame.draw.circle(screen, BLACK, (self.rect.centerx - 5, self.rect.y - 10), 3)
            pygame.draw.circle(screen, BLACK, (self.rect.centerx + 5, self.rect.y - 10), 3)
        
        # Name
        name_text = small_font.render(self.name, True, BLACK)
        screen.blit(name_text, (self.rect.x, self.rect.bottom + 5))
        
        # Order bubble
        bubble_x = self.rect.right + 10
        bubble_y = self.rect.y
        bubble_width = 150
        bubble_height = 100
        
        pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)
        
        # Order text
        order_text = small_font.render("Wants:", True, BLACK)
        screen.blit(order_text, (bubble_x + 5, bubble_y + 5))
        
        for i, ingredient in enumerate(self.order):
            ing_text = small_font.render(f"• {ingredient[:6]}", True, DARK_GREEN)
            screen.blit(ing_text, (bubble_x + 5, bubble_y + 30 + i * 20))
        
        # Patience bar
        bar_width = 100
        patience_percent = self.patience / self.max_patience
        bar_color = GREEN if patience_percent > 0.5 else YELLOW if patience_percent > 0.25 else RED
        
        pygame.draw.rect(screen, GRAY, (bubble_x - 100, bubble_y + bubble_height, bar_width, 15))
        pygame.draw.rect(screen, bar_color, (bubble_x - 100, bubble_y + bubble_height, bar_width * patience_percent, 15))

class VietnameseRestaurantGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nhà Hàng Việt Nam - Vietnamese Restaurant")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)

        # --- MUSIC SETUP ---
        self.music_manager = MusicManager() # <--- Add this
        self.music_manager.start_music()    # <--- Add this

        # Load start screen background
        self.start_screen_bg = None
        try:
            self.start_screen_bg = pygame.image.load("resources/sprites/start_screen_bg.png")
            self.start_screen_bg = pygame.transform.scale(self.start_screen_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.start_screen_bg = None

        # FIXED: Load restaurant background
        self.restaurant_bg = None
        try:
            self.restaurant_bg = pygame.image.load("resources/sprites/restaurant_background.png")
            self.restaurant_bg = pygame.transform.scale(self.restaurant_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.restaurant_bg = None

        # Game state
        self.state = MENU
        self.score = 0
        self.orders_completed = 0
        
        # Player
        self.player = Player(400, 400, "resources/sprites/guy-sprite.png")

        # Sprite mapping for ingredients
        sprite_map = {
            "Noodles": "resources/sprites/noodles.png",
            "Broth": "resources/sprites/cooking_pho_pot.png",
            "Beef": "resources/sprites/raw_beef.png",
            "Pork": "resources/sprites/chicken_slices.png",  # Using chicken as substitute
            "Shrimp": "resources/sprites/shrimp.png",
            "Herbs": "resources/sprites/basil.png",
            "Lime": "resources/sprites/lime_wedges.png",
            "Jalapeno": "resources/sprites/sliced_jalapeno.png",
            "Cilantro": "resources/sprites/cilantro.png",
            "Rice Paper": "resources/sprites/fresh_spring_rolls.png",
            "Bread": "resources/sprites/banh_mi_sandwich.png",
            "Fish Sauce": "resources/sprites/fish_sauce.png",
        }

        # Ingredient stations
        self.ingredient_stations = [
            IngredientStation(50, 300, "Noodles", YELLOW, sprite_map.get("Noodles")),
            IngredientStation(150, 300, "Broth", BROWN, sprite_map.get("Broth")),
            IngredientStation(250, 300, "Beef", RED, sprite_map.get("Beef")),
            IngredientStation(350, 300, "Pork", LIGHT_BROWN, sprite_map.get("Pork")),
            IngredientStation(50, 400, "Shrimp", ORANGE, sprite_map.get("Shrimp")),
            IngredientStation(150, 400, "Herbs", GREEN, sprite_map.get("Herbs")),
            IngredientStation(250, 400, "Lime", DARK_GREEN, sprite_map.get("Lime")),
            IngredientStation(350, 400, "Jalapeno", YELLOW, sprite_map.get("Jalapeno")),
            IngredientStation(50, 500, "Cilantro", GREEN, sprite_map.get("Cilantro")),
            IngredientStation(150, 500, "Rice Paper", WHITE, sprite_map.get("Rice Paper")),
            IngredientStation(250, 500, "Bread", LIGHT_BROWN, sprite_map.get("Bread")),
            IngredientStation(350, 500, "Fish Sauce", BROWN, sprite_map.get("Fish Sauce")),
        ]
        
        # Cooking stations
        self.prep_station = CookingStation(50, 650, "prep", "resources/sprites/prep_station.png")
        self.cook_station = CookingStation(200, 650, "cook", "resources/sprites/cook_station.png")
        self.serve_station = CookingStation(350, 650, "serve", "resources/sprites/serve_station.png")
        
        # Customers
        self.customers = []
        self.customer_spawn_timer = 0
        self.customer_spawn_delay = 600  # 5 seconds
        
        # Dishes
        self.dishes = {
            "Phở": ["Noodles", "Broth", "Beef", "Herbs", "Lime"],
            "Bánh Mì": ["Bread", "Pork", "Jalapeno", "Cilantro"],
            "Bún Chả": ["Noodles", "Pork", "Fish Sauce", "Herbs"],
            "Gỏi Cuốn": ["Rice Paper", "Shrimp", "Herbs", "Noodles"],
        }
        
        
        # UI message
        self.message = ""
        self.message_timer = 0
        
    def spawn_customer(self):
        # FIXED: Enforce maximum 3 customers
        if len(self.customers) >= 3:
            return

        names = ["Minh", "Linh", "Hùng", "Mai", "Tuấn", "Hoa"]
        colors = [RED, GREEN, LIGHT_BLUE, YELLOW, ORANGE]
        sprites = [
            "resources/sprites/customer1.png",
            "resources/sprites/customer2.png",
            "resources/sprites/customer3.png",
            "resources/sprites/customer4.png",
            "resources/sprites/customer5.png",
            "resources/sprites/customer6.png"
        ]

        name = random.choice(names)
        color = random.choice(colors)
        sprite = random.choice(sprites)
        dish_name = random.choice(list(self.dishes.keys()))
        order = self.dishes[dish_name]

        # FIXED: Define distinct spawn positions to prevent overlap
        spawn_positions = [
            (900, 150),   # Position 1 (top)
            (900, 350),   # Position 2 (middle)
            (900, 550)    # Position 3 (bottom)
        ]

        # Get occupied positions
        occupied_positions = set()
        for customer in self.customers:
            occupied_positions.add((customer.x, customer.y))

        # Find available position
        available_positions = [pos for pos in spawn_positions if pos not in occupied_positions]

        if not available_positions:
            return  # No available positions

        # FIXED: Use first available position
        x, y = available_positions[0]

        customer = Customer(name, color, order, x, y, sprite)
        self.customers.append(customer)
            
    def check_order_match(self, ingredients, customer_order):
        return set(ingredients) == set(customer_order)
        
    def show_message(self, text):
        self.message = text
        self.message_timer = 120  # 2 seconds
        
    def draw_menu(self):
        # Draw background image or fallback
        if self.start_screen_bg:
            self.screen.blit(self.start_screen_bg, (0, 0))
        else:
            self.screen.fill(CREAM)

        # Title - positioned in the decorative title area
        title = self.title_font.render("Nhà Hàng Việt Nam", True, (255, 215, 0))
        title_shadow = self.title_font.render("Nhà Hàng Việt Nam", True, (139, 90, 43))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        # Shadow effect
        self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title, title_rect)

        subtitle = self.font.render("Vietnamese Restaurant Game", True, (255, 255, 255))
        subtitle_shadow = self.font.render("Vietnamese Restaurant Game", True, (100, 60, 20))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_shadow, (subtitle_rect.x + 2, subtitle_rect.y + 2))
        self.screen.blit(subtitle, subtitle_rect)

        # Instructions - positioned in the white instruction panel
        instructions = [
            ("CONTROLS:", True),
            ("WASD or Arrow Keys - Move", False),
            ("SPACE - Pick up ingredient / Add to station / Start cooking", False),
            ("", False),
            ("HOW TO PLAY:", True),
            ("1. Check what customers want (right side)", False),
            ("2. Walk to ingredient stations and press SPACE to pick up", False),
            ("3. Bring ingredients to PREP station and add them", False),
            ("4. Move dish to COOK station and start cooking", False),
            ("5. When done, take to SERVE station and serve customers!", False),
            ("", False),
            ("Keep customers happy before their patience runs out!", False),
        ]

        y_offset = 290
        for line, is_header in instructions:
            if is_header:
                text = self.font.render(line, True, (220, 20, 60))  # Red for headers
            else:
                text = self.small_font.render(line, True, (60, 40, 20))  # Brown for text
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25 if not is_header else 30

        # "Press SPACE to Start" - positioned on the wooden sign
        start_text = self.title_font.render("Press SPACE to Start!", True, (255, 215, 0))
        start_shadow = self.title_font.render("Press SPACE to Start!", True, (80, 50, 20))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 720))
        self.screen.blit(start_shadow, (start_rect.x + 2, start_rect.y + 2))
        self.screen.blit(start_text, start_rect)
        
    def draw_game(self):
        # FIXED: Draw authentic Vietnamese restaurant background
        if self.restaurant_bg:
            self.screen.blit(self.restaurant_bg, (0, 0))
        else:
            # Fallback to original
            self.screen.fill(LIGHT_BLUE)
            # Draw floor
            pygame.draw.rect(self.screen, CREAM, (0, 200, 500, 550))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        orders_text = self.small_font.render(f"Orders: {self.orders_completed}", True, BLACK)
        self.screen.blit(orders_text, (20, 60))
        
        # Draw ingredient stations
        for station in self.ingredient_stations:
            station.draw(self.screen, self.small_font)
        
        # Draw cooking stations
        self.prep_station.draw(self.screen, self.font, self.small_font)
        self.cook_station.draw(self.screen, self.font, self.small_font)
        self.serve_station.draw(self.screen, self.font, self.small_font)
        
        # Draw customers
        for customer in self.customers:
            customer.draw(self.screen, self.font, self.small_font)
        
        # Draw player
        self.player.draw(self.screen, self.small_font)
        
        # Draw controls hint
        controls = self.small_font.render("WASD: Move | SPACE: Interact", True, BLACK)
        self.screen.blit(controls, (20, 100))
        
        # Draw interaction hints
        if self.prep_station.is_player_near(self.player):
            hint = self.small_font.render("[SPACE] Add ingredient / Move to cook", True, WHITE)
            pygame.draw.rect(self.screen, BLACK, (self.prep_station.rect.x, self.prep_station.rect.y - 25, 300, 20))
            self.screen.blit(hint, (self.prep_station.rect.x + 5, self.prep_station.rect.y - 23))
            
        if self.cook_station.is_player_near(self.player):
            hint = self.small_font.render("[SPACE] Start cooking / Move to serve", True, WHITE)
            pygame.draw.rect(self.screen, BLACK, (self.cook_station.rect.x, self.cook_station.rect.y - 25, 300, 20))
            self.screen.blit(hint, (self.cook_station.rect.x + 5, self.cook_station.rect.y - 23))
            
        if self.serve_station.is_player_near(self.player):
            hint = self.small_font.render("[SPACE] Serve to customer", True, WHITE)
            pygame.draw.rect(self.screen, BLACK, (self.serve_station.rect.x, self.serve_station.rect.y - 25, 250, 20))
            self.screen.blit(hint, (self.serve_station.rect.x + 5, self.serve_station.rect.y - 23))
        
        for station in self.ingredient_stations:
            if station.is_player_near(self.player) and not self.player.held_ingredient:
                hint = self.small_font.render(f"[SPACE] Pick up", True, WHITE)
                pygame.draw.rect(self.screen, BLACK, (station.rect.x, station.rect.y - 25, 150, 20))
                self.screen.blit(hint, (station.rect.x + 5, station.rect.y - 23))
        
        # Draw message
        if self.message_timer > 0:
            message_surface = self.font.render(self.message, True, WHITE)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
            pygame.draw.rect(self.screen, BLACK, message_rect.inflate(20, 10), border_radius=10)
            self.screen.blit(message_surface, message_rect)
            self.message_timer -= 1
        
    def handle_interaction(self):
        # Pick up ingredient
        for station in self.ingredient_stations:
            if station.is_player_near(self.player) and not self.player.held_ingredient:
                self.player.held_ingredient = station.ingredient_name
                # Set the downscaled sprite
                if station.sprite:
                    try:
                        self.player.held_ingredient_sprite = pygame.transform.scale(station.sprite, (30, 30))
                    except:
                        self.player.held_ingredient_sprite = None
                else:
                    self.player.held_ingredient_sprite = None
                self.show_message(f"Picked up {station.ingredient_name}!")
                return
        
        # Interact with prep station
        if self.prep_station.is_player_near(self.player):
            if self.player.held_ingredient:
                self.prep_station.add_ingredient(self.player.held_ingredient)
                self.show_message(f"Added {self.player.held_ingredient} to prep!")
                self.player.held_ingredient = None
                self.player.held_ingredient_sprite = None
            elif self.prep_station.ingredients and not self.cook_station.ingredients:
                # Move to cook station
                self.cook_station.ingredients = self.prep_station.ingredients[:]
                self.prep_station.clear()
                self.show_message("Moved to cook station!")
            return
        
        # Interact with cook station
        if self.cook_station.is_player_near(self.player):
            if not self.cook_station.cooking and self.cook_station.ingredients:
                self.cook_station.start_cooking()
                self.show_message("Started cooking!")
            elif not self.cook_station.cooking and not self.cook_station.ingredients:
                self.show_message("Station is empty!")
            elif self.cook_station.cooking:
                self.show_message("Still cooking...")
            return
        
        # Interact with serve station
        if self.serve_station.is_player_near(self.player):
            if self.serve_station.ingredients:
                # Try to serve to a customer
                for customer in self.customers[:]:
                    if not customer.leaving and not customer.served:
                        if self.check_order_match(self.serve_station.ingredients, customer.order):
                            # Correct order!
                            patience_bonus = int(customer.patience)
                            self.score += 100 + patience_bonus
                            self.orders_completed += 1
                            self.customers.remove(customer)
                            self.serve_station.clear()
                            self.show_message(f"Perfect! +{100 + patience_bonus} points!")
                            return
                        else:
                            # Wrong order
                            self.show_message("Wrong order for this customer!")
                            return
                self.show_message("No matching customer order!")
            else:
                self.show_message("Serve station is empty!")
            return
    
    def run(self):
        while self.running:
            # Check music
            self.music_manager.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.state == MENU:
                            self.state = GAME
                            self.spawn_customer()
                        elif self.state == GAME:
                            self.handle_interaction()
            
            if self.state == GAME:
                # Update player movement
                keys = pygame.key.get_pressed()
                self.player.move(keys)
                
                # Update cooking
                if self.cook_station.update():
                    # Cooking done, move to serve station
                    if not self.serve_station.ingredients:
                        self.serve_station.ingredients = self.cook_station.ingredients[:]
                        self.cook_station.clear()
                        self.show_message("Dish ready to serve!")
                
                # Update customers
                for customer in self.customers[:]:
                    customer.update()
                    if customer.leaving:
                        self.customers.remove(customer)
                        self.show_message("Customer left! :(")
                
                # Spawn new customers
                self.customer_spawn_timer += 1
                if self.customer_spawn_timer >= self.customer_spawn_delay:
                    self.spawn_customer()
                    self.customer_spawn_timer = 0
            
            # Draw
            if self.state == MENU:
                self.draw_menu()
            elif self.state == GAME:
                self.draw_game()
                
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = VietnameseRestaurantGame()
    game.run()