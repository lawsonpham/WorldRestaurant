import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
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

# Game states
MENU = "menu"
GAME = "game"
INFO = "info"

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Ingredient:
    def __init__(self, name, x, y, color, size=60):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        
        # Draw ingredient icon/text
        text = font.render(self.name[:4], True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

class Order:
    def __init__(self, dish_name, required_ingredients, fun_fact):
        self.dish_name = dish_name
        self.required_ingredients = required_ingredients
        self.fun_fact = fun_fact
        self.added_ingredients = []
        
    def add_ingredient(self, ingredient_name):
        if ingredient_name not in self.added_ingredients:
            self.added_ingredients.append(ingredient_name)
            
    def is_complete(self):
        return set(self.added_ingredients) == set(self.required_ingredients)
    
    def is_correct(self):
        return set(self.added_ingredients) == set(self.required_ingredients)

class VietnameseRestaurantGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nhà Hàng Việt Nam - Vietnamese Restaurant")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = MENU
        self.score = 0
        self.orders_completed = 0
        
        # Dishes database
        self.dishes = {
            "Phở": {
                "ingredients": ["Noodles", "Broth", "Beef", "Herbs", "Lime"],
                "fact": "Phở originated in Northern Vietnam in the early 20th century.\nThe name 'phở' comes from the French dish 'pot-au-feu'.\nIt's typically eaten for breakfast but enjoyed any time of day!"
            },
            "Bánh Mì": {
                "ingredients": ["Bread", "Pâté", "Pork", "Pickle", "Cilantro"],
                "fact": "Bánh Mì is a fusion of French and Vietnamese cuisine.\nThe crispy baguette was introduced during French colonization.\nIt's been called the world's best sandwich by many food critics!"
            },
            "Bún Chả": {
                "ingredients": ["Noodles", "Pork", "Fish Sauce", "Herbs", "Pickle"],
                "fact": "Bún Chả is a Hanoi specialty dish.\nPresident Obama and Anthony Bourdain famously ate it together.\nThe grilled pork is served with a sweet-sour dipping sauce!"
            },
            "Gỏi Cuốn": {
                "ingredients": ["Rice Paper", "Shrimp", "Pork", "Herbs", "Noodles"],
                "fact": "Gỏi Cuốn means 'salad rolls' in Vietnamese.\nThey're also called 'summer rolls' and served fresh, not fried.\nEach roll is wrapped by hand and dipped in peanut sauce!"
            }
        }
        
        self.current_order = None
        self.ingredients = []
        self.bowl_rect = pygame.Rect(700, 400, 250, 250)
        self.show_fact = False
        self.fact_timer = 0
        
        # Buttons
        self.start_button = Button(350, 300, 300, 80, "Start Cooking!", GREEN, DARK_GREEN)
        self.menu_button = Button(400, 550, 200, 60, "Main Menu", LIGHT_BROWN, BROWN)
        self.next_button = Button(400, 550, 200, 60, "Next Order", GREEN, DARK_GREEN)
        
    def create_new_order(self):
        dish_name = random.choice(list(self.dishes.keys()))
        dish_data = self.dishes[dish_name]
        self.current_order = Order(dish_name, dish_data["ingredients"], dish_data["fact"])
        
        # Create ingredient buttons
        self.ingredients = []
        all_possible_ingredients = ["Noodles", "Broth", "Beef", "Pork", "Shrimp", 
                                   "Herbs", "Lime", "Pickle", "Cilantro", "Fish Sauce",
                                   "Rice Paper", "Bread", "Pâté"]
        
        # Shuffle and pick ingredients (including required ones)
        available = dish_data["ingredients"] + random.sample(
            [i for i in all_possible_ingredients if i not in dish_data["ingredients"]], 
            min(3, len(all_possible_ingredients) - len(dish_data["ingredients"]))
        )
        random.shuffle(available)
        
        colors = [RED, GREEN, BROWN, YELLOW, DARK_GREEN, LIGHT_BROWN]
        
        for i, ingredient in enumerate(available):
            x = 50 + (i % 4) * 90
            y = 400 + (i // 4) * 90
            color = colors[i % len(colors)]
            self.ingredients.append(Ingredient(ingredient, x, y, color))
        
        self.show_fact = False
        
    def draw_menu(self):
        self.screen.fill(CREAM)
        
        # Title
        title = self.title_font.render("Nhà Hàng Việt Nam", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Vietnamese Restaurant Game", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        instructions = [
            "Welcome to our Vietnamese restaurant!",
            "Drag ingredients to the bowl to prepare dishes.",
            "Learn fun facts about Vietnamese cuisine!",
            "Complete orders to earn points!"
        ]
        
        for i, line in enumerate(instructions):
            text = self.small_font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 220 + i * 30))
            self.screen.blit(text, text_rect)
        
        # Start button
        self.start_button.draw(self.screen, self.font)
        
        # Credits
        credits = self.small_font.render("Celebrating Vietnamese Culture Through Food", True, DARK_GREEN)
        credits_rect = credits.get_rect(center=(SCREEN_WIDTH // 2, 650))
        self.screen.blit(credits, credits_rect)
        
    def draw_game(self):
        self.screen.fill(LIGHT_BLUE)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        orders_text = self.small_font.render(f"Orders: {self.orders_completed}", True, BLACK)
        self.screen.blit(orders_text, (20, 60))
        
        # Draw current order
        if self.current_order:
            order_text = self.title_font.render(f"Make: {self.current_order.dish_name}", True, RED)
            self.screen.blit(order_text, (300, 20))
            
            required_text = self.small_font.render("Ingredients needed:", True, BLACK)
            self.screen.blit(required_text, (300, 90))
            
            for i, ingredient in enumerate(self.current_order.required_ingredients):
                check = "✓" if ingredient in self.current_order.added_ingredients else "○"
                ing_text = self.small_font.render(f"{check} {ingredient}", True, DARK_GREEN if ingredient in self.current_order.added_ingredients else BLACK)
                self.screen.blit(ing_text, (320, 120 + i * 30))
        
        # Draw bowl
        pygame.draw.ellipse(self.screen, WHITE, self.bowl_rect)
        pygame.draw.ellipse(self.screen, BLACK, self.bowl_rect, 3)
        bowl_label = self.font.render("Bowl", True, BLACK)
        self.screen.blit(bowl_label, (self.bowl_rect.centerx - 30, self.bowl_rect.centery - 15))
        
        # Draw ingredients
        for ingredient in self.ingredients:
            ingredient.draw(self.screen, self.small_font)
        
        # Instructions
        inst_text = self.small_font.render("Drag ingredients to the bowl!", True, BLACK)
        self.screen.blit(inst_text, (50, 350))
        
        # Show completion message or fact
        if self.show_fact:
            # Draw fact box
            fact_box = pygame.Rect(150, 200, 700, 300)
            pygame.draw.rect(self.screen, CREAM, fact_box, border_radius=15)
            pygame.draw.rect(self.screen, RED, fact_box, 5, border_radius=15)
            
            # Title
            if self.current_order.is_correct():
                title = self.title_font.render("Perfect! 🎉", True, GREEN)
                self.screen.blit(title, (fact_box.centerx - 100, fact_box.y + 20))
            else:
                title = self.title_font.render("Not quite right!", True, RED)
                self.screen.blit(title, (fact_box.centerx - 150, fact_box.y + 20))
            
            # Fun fact
            fact_title = self.font.render("Fun Fact:", True, RED)
            self.screen.blit(fact_title, (fact_box.x + 20, fact_box.y + 90))
            
            # Split fact into lines
            lines = self.current_order.fun_fact.split('\n')
            for i, line in enumerate(lines):
                fact_text = self.small_font.render(line, True, BLACK)
                self.screen.blit(fact_text, (fact_box.x + 20, fact_box.y + 130 + i * 30))
            
            # Next button
            self.next_button.draw(self.screen, self.font)
        
    def handle_menu_events(self, event):
        if self.start_button.handle_event(event):
            self.state = GAME
            self.create_new_order()
            
    def handle_game_events(self, event):
        if self.show_fact:
            if self.next_button.handle_event(event):
                self.create_new_order()
        else:
            for ingredient in self.ingredients:
                ingredient.handle_event(event)
                
                # Check if ingredient is dropped in bowl
                if event.type == pygame.MOUSEBUTTONUP:
                    if ingredient.rect.colliderect(self.bowl_rect):
                        self.current_order.add_ingredient(ingredient.name)
                        self.ingredients.remove(ingredient)
                        
                        # Check if order is complete
                        if len(self.current_order.added_ingredients) == len(self.current_order.required_ingredients):
                            self.show_fact = True
                            if self.current_order.is_correct():
                                self.score += 100
                                self.orders_completed += 1
                            else:
                                self.score += 20
                        break
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if self.state == MENU:
                    self.handle_menu_events(event)
                elif self.state == GAME:
                    self.handle_game_events(event)
            
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
