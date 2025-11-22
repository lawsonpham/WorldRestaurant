from PIL import Image, ImageDraw, ImageFont
import os

# Create a vibrant Vietnamese-themed start screen
def create_start_screen():
    # Screen dimensions
    width = 1200
    height = 800

    # Create base image
    img = Image.new('RGB', (width, height), (255, 253, 208))  # Cream background
    draw = ImageDraw.Draw(img)

    # Background gradient - warm tones
    for y in range(height):
        # Gradient from warm cream to light terracotta
        ratio = y / height
        r = int(255 - (30 * ratio))
        g = int(253 - (90 * ratio))
        b = int(208 - (78 * ratio))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add rice paper texture pattern (subtle dots)
    for i in range(0, width, 15):
        for j in range(0, height, 15):
            if (i + j) % 30 == 0:
                draw.ellipse([i, j, i+2, j+2], fill=(240, 235, 200, 128))

    # Decorative border - bamboo green frame
    border_color = (87, 121, 76)  # Bamboo green
    draw.rectangle([20, 20, width-20, height-20], outline=border_color, width=8)
    draw.rectangle([30, 30, width-30, height-30], outline=(180, 150, 100), width=3)

    # Corner decorations - lotus flowers
    def draw_lotus(x, y, size):
        # Lotus petals
        petal_color = (255, 182, 193)
        for angle in range(0, 360, 45):
            import math
            px = x + int(size * math.cos(math.radians(angle)))
            py = y + int(size * math.sin(math.radians(angle)))
            draw.ellipse([px-15, py-20, px+15, py+20], fill=petal_color, outline=(220, 100, 120), width=2)
        # Center
        draw.ellipse([x-12, y-12, x+12, y+12], fill=(255, 215, 0), outline=(200, 170, 50), width=2)

    # Draw lotus flowers in corners
    draw_lotus(80, 80, 35)
    draw_lotus(width-80, 80, 35)
    draw_lotus(80, height-80, 35)
    draw_lotus(width-80, height-80, 35)

    # Draw bamboo leaves accent
    def draw_bamboo_leaf(x, y):
        leaf_color = (106, 168, 79)
        points = [(x, y), (x+40, y+10), (x+35, y+25), (x, y+15), (x-35, y+25), (x-40, y+10)]
        draw.polygon(points, fill=leaf_color, outline=(70, 120, 50), width=2)
        draw.line([(x, y+15), (x, y-5)], fill=(70, 120, 50), width=3)

    # Bamboo leaves near title area
    draw_bamboo_leaf(150, 120)
    draw_bamboo_leaf(width-150, 120)

    # Traditional lantern decorations
    def draw_lantern(x, y):
        # Red lantern
        lantern_red = (220, 20, 60)
        lantern_gold = (255, 215, 0)

        # Top cap
        draw.ellipse([x-25, y-5, x+25, y+10], fill=lantern_gold, outline=(200, 170, 0), width=2)
        # Main body
        draw.ellipse([x-30, y+5, x+30, y+70], fill=lantern_red, outline=(180, 10, 40), width=3)
        # Horizontal gold bands
        for band_y in [y+20, y+40, y+55]:
            draw.rectangle([x-32, band_y-2, x+32, band_y+2], fill=lantern_gold)
        # Bottom tassel
        draw.line([(x, y+70), (x, y+85)], fill=lantern_gold, width=3)
        for i in range(-8, 9, 4):
            draw.line([(x, y+85), (x+i, y+95)], fill=lantern_gold, width=2)

    # Lanterns on sides
    draw_lantern(220, 200)
    draw_lantern(width-220, 200)

    # Food illustrations in background (simplified)

    # Pho bowl (left side)
    def draw_pho_bowl(x, y):
        # Bowl
        draw.ellipse([x-50, y+20, x+50, y+40], fill=(240, 240, 245), outline=(180, 180, 190), width=3)
        draw.arc([x-55, y-15, x+55, y+45], 0, 180, fill=(200, 200, 210), width=35)
        # Broth
        draw.ellipse([x-45, y-5, x+45, y+15], fill=(160, 100, 50))
        # Noodles
        for i in range(-30, 35, 8):
            draw.arc([x+i-8, y-8, x+i+8, y+8], 180, 360, fill=(240, 230, 200), width=3)
        # Herbs on top
        draw.ellipse([x-15, y-5, x-5, y+5], fill=(34, 139, 34))
        draw.ellipse([x+5, y-5, x+15, y+5], fill=(34, 139, 34))
        # Steam
        for sx in [x-20, x, x+20]:
            draw.line([(sx, y-20), (sx-3, y-35)], fill=(220, 220, 230), width=2)
            draw.line([(sx, y-20), (sx+3, y-35)], fill=(220, 220, 230), width=2)

    draw_pho_bowl(200, 350)

    # Banh mi (right side)
    def draw_banh_mi(x, y):
        # Bread
        draw.ellipse([x-60, y-20, x+60, y+20], fill=(210, 180, 140), outline=(160, 130, 90), width=3)
        # Crust texture lines
        for i in range(-50, 55, 15):
            draw.line([(x+i-5, y-18), (x+i+5, y-15)], fill=(180, 150, 110), width=2)
        # Filling visible
        draw.rectangle([x-55, y-8, x+55, y+8], fill=(200, 150, 100))
        # Vegetables
        draw.rectangle([x-50, y-5, x+50, y-2], fill=(34, 139, 34))  # Herbs
        draw.rectangle([x-50, y+2, x+50, y+5], fill=(255, 100, 100))  # Pickles/peppers

    draw_banh_mi(width-200, 350)

    # Spring rolls (bottom)
    def draw_spring_roll(x, y):
        # Rice paper wrapper
        draw.ellipse([x-40, y-15, x+40, y+15], fill=(255, 250, 240), outline=(220, 210, 200), width=2)
        # Filling visible through wrapper
        draw.rectangle([x-30, y-8, x+30, y+8], fill=(255, 182, 193, 180))
        # Shrimp tint
        draw.ellipse([x-15, y-6, x+15, y+6], fill=(255, 140, 140, 150))
        # Herbs
        draw.line([(x-20, y-4), (x+20, y-4)], fill=(34, 139, 34, 180), width=2)

    draw_spring_roll(width//2 - 100, 650)
    draw_spring_roll(width//2 + 100, 650)

    # Coffee drip illustration
    def draw_coffee_drip(x, y):
        # Drip filter (phin)
        draw.rectangle([x-25, y-30, x+25, y-15], fill=(150, 150, 160), outline=(100, 100, 110), width=2)
        draw.rectangle([x-22, y-15, x+22, y-10], fill=(120, 120, 130))
        # Coffee drops
        for dy in [0, 10, 20]:
            draw.ellipse([x-3, y+dy, x+3, y+dy+8], fill=(101, 67, 33))
        # Glass below
        draw.rectangle([x-20, y+30, x+20, y+60], fill=(240, 240, 245, 200), outline=(180, 180, 190), width=2)
        # Coffee in glass
        draw.rectangle([x-18, y+45, x+18, y+58], fill=(101, 67, 33))
        # Condensed milk layer
        draw.rectangle([x-18, y+55, x+18, y+58], fill=(255, 250, 230))

    draw_coffee_drip(width//2, 520)

    # Title panel with transparency effect
    panel_height = 140
    panel_y = 100
    # Dark overlay for title
    overlay = Image.new('RGBA', (width-200, panel_height), (139, 90, 43, 230))
    img_rgba = img.convert('RGBA')
    img_rgba.paste(overlay, (100, panel_y), overlay)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Title text (will be drawn in the actual game with custom font)
    # Drawing decorative frame for where title will go
    title_frame_color = (255, 215, 0)
    draw.rectangle([110, panel_y+10, width-110, panel_y+panel_height-10],
                   outline=title_frame_color, width=4)

    # Instruction panel
    instr_y = 270
    instr_height = 340
    instruction_panel = Image.new('RGBA', (700, instr_height), (255, 255, 255, 220))
    img_rgba = img.convert('RGBA')
    img_rgba.paste(instruction_panel, (250, instr_y), instruction_panel)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Frame for instructions
    draw.rectangle([255, instr_y+5, 945, instr_y+instr_height-5],
                   outline=(139, 90, 43), width=3)

    # Decorative elements around instruction panel
    # Chopsticks
    def draw_chopsticks(x, y, angle_offset=0):
        stick_color = (139, 90, 43)
        import math
        # Two chopsticks
        for offset in [-8, 8]:
            x1 = x + offset
            y1 = y
            x2 = x1 + int(100 * math.cos(math.radians(angle_offset)))
            y2 = y1 + int(100 * math.sin(math.radians(angle_offset)))
            draw.line([(x1, y1), (x2, y2)], fill=stick_color, width=4)
            # Decorative tip
            draw.line([(x1, y1), (x1-2, y1-10)], fill=(200, 50, 50), width=3)

    draw_chopsticks(220, 300, 45)
    draw_chopsticks(980, 300, 135)

    # Chili peppers accent
    def draw_chili(x, y):
        # Red chili
        draw.ellipse([x-4, y, x+4, y+35], fill=(220, 20, 60), outline=(180, 10, 40), width=2)
        # Stem
        draw.line([(x, y), (x-3, y-8)], fill=(34, 139, 34), width=3)

    draw_chili(240, 580)
    draw_chili(960, 580)

    # Herb sprigs (cilantro/mint)
    def draw_herb_sprig(x, y):
        stem_color = (50, 120, 50)
        leaf_color = (106, 168, 79)
        # Stem
        draw.line([(x, y+30), (x, y)], fill=stem_color, width=3)
        # Leaves
        for leaf_y in [y+5, y+12, y+19, y+26]:
            draw.ellipse([x-8, leaf_y-4, x-2, leaf_y+4], fill=leaf_color, outline=stem_color, width=1)
            draw.ellipse([x+2, leaf_y-4, x+8, leaf_y+4], fill=leaf_color, outline=stem_color, width=1)

    draw_herb_sprig(950, 540)
    draw_herb_sprig(250, 540)

    # "Press SPACE to Start" button area - wooden sign style
    button_y = 720
    # Wooden plaque background
    wood_color = (139, 90, 43)
    draw.rectangle([400, button_y-35, 800, button_y+35], fill=wood_color, outline=(100, 60, 20), width=4)
    # Wood grain effect
    for i in range(410, 790, 20):
        draw.line([(i, button_y-30), (i+15, button_y+30)], fill=(120, 75, 35), width=2)

    # Border decoration on sign
    draw.rectangle([410, button_y-30, 790, button_y+30], outline=(255, 215, 0), width=3)

    # Save the background
    img.save("resources/sprites/start_screen_bg.png")
    print("Created start_screen_bg.png")

    # Create a version with just the title area clear for text overlay
    # This will be the actual background used in-game
    print("Vietnamese Restaurant Start Screen created successfully!")

if __name__ == "__main__":
    os.makedirs("resources/sprites", exist_ok=True)
    create_start_screen()
