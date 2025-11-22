from PIL import Image, ImageDraw
import os

# Create an authentic Vietnamese restaurant background
def create_restaurant_background():
    width = 1200
    height = 800

    # Create base image
    img = Image.new('RGB', (width, height), (245, 235, 220))

    draw = ImageDraw.Draw(img)

    # ===================================================================
    # LAYER 1: FAR BACKGROUND - Walls and architectural elements
    # ===================================================================

    # Upper wall - cream/beige with warmth
    for y in range(0, 200):
        ratio = y / 200
        r = int(238 - (10 * ratio))
        g = int(228 - (8 * ratio))
        b = int(210 - (5 * ratio))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Wooden wall paneling - horizontal planks
    wood_dark = (139, 90, 43)
    wood_light = (180, 130, 80)
    wood_medium = (160, 110, 65)

    # Vertical wooden beams
    beam_positions = [100, 300, 500, 700, 900, 1100]
    for beam_x in beam_positions:
        # Main beam
        draw.rectangle([beam_x - 8, 0, beam_x + 8, 200], fill=wood_dark)
        # Highlight
        draw.rectangle([beam_x - 6, 0, beam_x - 4, 200], fill=wood_medium)

    # Horizontal wood trim
    draw.rectangle([0, 190, width, 205], fill=wood_dark)
    draw.rectangle([0, 192, width, 198], fill=wood_light)

    # ===================================================================
    # DECORATIVE ELEMENTS - Lanterns and plants
    # ===================================================================

    # Red paper lanterns
    def draw_lantern(x, y, size=30):
        lantern_red = (220, 20, 60)
        lantern_gold = (255, 215, 0)

        # Hanging cord
        draw.line([(x, y - 20), (x, y)], fill=wood_dark, width=2)

        # Top cap
        draw.ellipse([x - size//3, y - 5, x + size//3, y + 5], fill=lantern_gold)

        # Main body - rounded
        draw.ellipse([x - size, y, x + size, y + size*2], fill=lantern_red)

        # Gold bands
        for band_y in [y + size//3, y + size, y + size*1.6]:
            draw.rectangle([x - size - 2, band_y - 3, x + size + 2, band_y + 1], fill=lantern_gold)

        # Bottom tassel
        draw.line([(x, y + size*2), (x, y + size*2 + 15)], fill=lantern_gold, width=3)
        # Tassel fringe
        for offset in [-6, -3, 0, 3, 6]:
            draw.line([(x, y + size*2 + 15), (x + offset, y + size*2 + 22)], fill=lantern_gold, width=2)

    # Place lanterns
    draw_lantern(200, 30, 25)
    draw_lantern(600, 40, 30)
    draw_lantern(1000, 35, 28)

    # Bamboo plants in corners
    def draw_bamboo_plant(x, y):
        bamboo_green = (106, 168, 79)
        bamboo_stalk = (120, 140, 90)
        pot_color = (139, 90, 43)

        # Pot
        draw.ellipse([x - 30, y + 80, x + 30, y + 100], fill=pot_color)
        draw.rectangle([x - 28, y + 60, x + 28, y + 90], fill=pot_color)

        # Bamboo stalks
        for stalk_offset in [-15, 0, 15]:
            stalk_x = x + stalk_offset
            # Main stalk
            draw.rectangle([stalk_x - 3, y, stalk_x + 3, y + 85], fill=bamboo_stalk)

            # Segments
            for seg_y in [y + 20, y + 40, y + 60]:
                draw.line([(stalk_x - 4, seg_y), (stalk_x + 4, seg_y)], fill=bamboo_green, width=2)

            # Leaves
            for leaf_y in [y + 10, y + 25, y + 45]:
                # Left leaves
                draw.ellipse([stalk_x - 20, leaf_y - 8, stalk_x - 5, leaf_y + 8], fill=bamboo_green)
                # Right leaves
                draw.ellipse([stalk_x + 5, leaf_y - 8, stalk_x + 20, leaf_y + 8], fill=bamboo_green)

    # Place bamboo plants
    draw_bamboo_plant(70, 50)
    draw_bamboo_plant(1130, 50)

    # ===================================================================
    # LAYER 2: FLOOR - Wooden planks with texture
    # ===================================================================

    floor_start_y = 200

    # Base floor color - warm wood
    floor_base = (160, 120, 80)
    draw.rectangle([0, floor_start_y, width, height], fill=floor_base)

    # Wooden plank effect - horizontal boards
    plank_colors = [
        (155, 115, 75),
        (165, 125, 85),
        (160, 120, 80),
        (158, 118, 78),
    ]

    plank_height = 40
    y_pos = floor_start_y
    color_idx = 0

    while y_pos < height:
        plank_color = plank_colors[color_idx % len(plank_colors)]
        draw.rectangle([0, y_pos, width, y_pos + plank_height], fill=plank_color)

        # Wood grain effect
        for grain_y in range(y_pos, min(y_pos + plank_height, height), 8):
            grain_lightness = color_idx % 2
            grain_color = tuple(max(0, c - 10 + grain_lightness * 5) for c in plank_color)
            draw.line([(0, grain_y), (width, grain_y)], fill=grain_color, width=1)

        # Plank separators
        separator_color = (120, 85, 50)
        draw.line([(0, y_pos + plank_height - 1), (width, y_pos + plank_height - 1)],
                 fill=separator_color, width=2)

        y_pos += plank_height
        color_idx += 1

    # Vertical plank joints (random)
    import random
    random.seed(42)  # For consistency
    for plank_y in range(floor_start_y, height, plank_height):
        num_joints = random.randint(3, 6)
        for _ in range(num_joints):
            joint_x = random.randint(50, width - 50)
            draw.line([(joint_x, plank_y), (joint_x, plank_y + plank_height)],
                     fill=(120, 85, 50), width=3)

    # ===================================================================
    # LAYER 3: COOKING/PREP AREA - Lighter floor section
    # ===================================================================

    # Left side cooking area - lighter tile floor
    cooking_area_width = 520
    tile_color_1 = (220, 210, 195)
    tile_color_2 = (210, 200, 185)

    # Create tiled pattern
    tile_size = 40
    for tile_y in range(floor_start_y, height, tile_size):
        for tile_x in range(0, cooking_area_width, tile_size):
            # Checkerboard pattern
            if ((tile_x // tile_size) + (tile_y // tile_size)) % 2 == 0:
                color = tile_color_1
            else:
                color = tile_color_2

            draw.rectangle([tile_x, tile_y, tile_x + tile_size, tile_y + tile_size], fill=color)

            # Tile grout lines
            draw.rectangle([tile_x, tile_y, tile_x + tile_size, tile_y + 2], fill=(180, 170, 160))
            draw.rectangle([tile_x, tile_y, tile_x + 2, tile_y + tile_size], fill=(180, 170, 160))

    # Border between cooking area and dining area
    border_x = cooking_area_width
    draw.rectangle([border_x - 3, floor_start_y, border_x + 3, height], fill=wood_dark)
    draw.rectangle([border_x - 1, floor_start_y, border_x + 1, height], fill=(255, 215, 0))

    # ===================================================================
    # DECORATIVE FLOOR ELEMENTS
    # ===================================================================

    # Woven mat or rug in customer area
    def draw_decorative_mat(x, y, w, h):
        mat_color = (180, 100, 80)
        mat_border = (220, 50, 50)

        # Mat base
        draw.rectangle([x, y, x + w, y + h], fill=mat_color)

        # Border pattern
        draw.rectangle([x, y, x + w, y + 8], fill=mat_border)
        draw.rectangle([x, y + h - 8, x + w, y + h], fill=mat_border)

        # Woven pattern
        for pattern_y in range(y + 12, y + h - 12, 8):
            for pattern_x in range(x + 8, x + w - 8, 16):
                draw.rectangle([pattern_x, pattern_y, pattern_x + 8, pattern_y + 4],
                             fill=(160, 90, 70))

    # Place decorative mats under customer areas
    draw_decorative_mat(870, 140, 280, 180)
    draw_decorative_mat(870, 340, 280, 180)
    draw_decorative_mat(870, 540, 280, 180)

    # ===================================================================
    # WINDOW WITH STREET VIEW
    # ===================================================================

    def draw_window(x, y, w, h):
        # Window frame
        frame_color = wood_dark
        glass_color = (200, 230, 255, 200)  # Light blue tint

        # Outer frame
        draw.rectangle([x, y, x + w, y + h], fill=frame_color)

        # Glass panes
        pane_margin = 12
        center_div = w // 2

        # Left pane
        draw.rectangle([x + pane_margin, y + pane_margin,
                       x + center_div - 3, y + h - pane_margin], fill=(220, 240, 255))

        # Right pane
        draw.rectangle([x + center_div + 3, y + pane_margin,
                       x + w - pane_margin, y + h - pane_margin], fill=(220, 240, 255))

        # Cross frame
        draw.rectangle([x + center_div - 4, y, x + center_div + 4, y + h], fill=frame_color)
        draw.rectangle([x, y + h//2 - 4, x + w, y + h//2 + 4], fill=frame_color)

        # Hints of plants outside
        plant_green = (100, 150, 100)
        for plant_x in [x + 30, x + w - 40]:
            draw.ellipse([plant_x, y + h - 40, plant_x + 25, y + h - 15], fill=plant_green)

    # Windows on back wall
    draw_window(400, 30, 120, 140)
    draw_window(800, 40, 100, 120)

    # ===================================================================
    # WALL DECORATIONS
    # ===================================================================

    # Framed artwork/calligraphy
    def draw_frame(x, y, w, h):
        frame_wood = (100, 60, 30)
        art_bg = (250, 245, 235)

        # Frame
        draw.rectangle([x, y, x + w, y + h], fill=frame_wood)

        # Art inside
        draw.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], fill=art_bg)

        # Simple decorative strokes (abstract calligraphy)
        stroke_color = (40, 40, 40)
        for i in range(3):
            stroke_x = x + 20 + i * 20
            draw.line([(stroke_x, y + 20), (stroke_x + 10, y + h - 20)],
                     fill=stroke_color, width=4)

    # Place frames
    draw_frame(150, 60, 80, 100)
    draw_frame(950, 70, 70, 90)

    # ===================================================================
    # SUBTLE ATMOSPHERIC EFFECTS
    # ===================================================================

    # Add subtle texture overlay for depth
    import random
    random.seed(100)
    for _ in range(500):
        px = random.randint(0, width)
        py = random.randint(floor_start_y, height)
        brightness_adj = random.randint(-5, 5)

        # Get current pixel color (approximation)
        current_color = img.getpixel((px, py))
        new_color = tuple(max(0, min(255, c + brightness_adj)) for c in current_color)
        draw.point((px, py), fill=new_color)

    # Save the background
    img.save("resources/sprites/restaurant_background.png")
    print("Created restaurant_background.png")
    print("Authentic Vietnamese restaurant atmosphere complete!")

if __name__ == "__main__":
    os.makedirs("resources/sprites", exist_ok=True)
    create_restaurant_background()
