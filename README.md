# Vietnamese Restaurant Game 🍜

A fun cooking game celebrating Vietnamese culture through food! Similar to Papa's Pizzeria, players prepare authentic Vietnamese dishes and learn interesting facts about each one.

## How to Run

1. **Install Python** (if you don't have it): Download from [python.org](https://python.org)

2. **Install Pygame**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python vietnamese_restaurant.py
   ```

## How to Play

1. **Start the game** - Click "Start Cooking!" on the main menu
2. **Read the order** - See which Vietnamese dish is requested
3. **Check ingredients** - Review the list of required ingredients
4. **Drag ingredients** - Drag and drop the correct ingredients into the bowl
5. **Learn facts** - After completing each order, learn fun facts about the dish!
6. **Earn points** - Get 100 points for perfect orders, 20 points for attempts

## Current Dishes

The game includes four authentic Vietnamese dishes:

1. **Phở** - The iconic Vietnamese noodle soup
2. **Bánh Mì** - Vietnamese sandwich with French influence
3. **Bún Chả** - Grilled pork with noodles (Obama's favorite!)
4. **Gỏi Cuốn** - Fresh spring rolls

## Customization Ideas

### Adding More Dishes

To add new dishes, edit the `self.dishes` dictionary around line 110:

```python
"New Dish Name": {
    "ingredients": ["Ingredient1", "Ingredient2", "Ingredient3"],
    "fact": "Fun fact about this dish!\nYou can add multiple lines."
}
```

### Adding More Ingredients

Update the `all_possible_ingredients` list around line 181 to include new ingredients.

### Changing Colors

Modify the color constants at the top of the file (lines 15-24) to match your preferences.

### Adjusting Difficulty

- Make it easier: Reduce the number of wrong ingredients shown
- Make it harder: Add more similar ingredients or time limits

## Features to Add

Here are some ideas for expanding the game:

### Easy Additions:
- **Timer**: Add a countdown for each order
- **Lives**: Give players 3 chances before game over
- **Sound effects**: Add cooking sounds and music
- **More dishes**: Add Cơm Tấm, Cao Lầu, Chả Cá, etc.

### Medium Additions:
- **Cooking steps**: Add multiple stages (prep, cook, serve)
- **Customer patience**: Visual indicator of waiting time
- **Achievements**: Unlock badges for completing certain tasks
- **High score**: Save and display best scores

### Advanced Additions:
- **Multiple stations**: Like Papa's Pizzeria (order station, cooking station, serving station)
- **Upgrades**: Buy better equipment with earned points
- **Story mode**: Progress through different restaurants
- **Multiplayer**: Compete with friends for high scores

## GitHub Setup

### Creating a Repository

1. **Create a GitHub account** at [github.com](https://github.com)

2. **Install Git**:
   - Windows: Download from [git-scm.com](https://git-scm.com)
   - Mac: `brew install git` or download from git-scm.com
   - Linux: `sudo apt install git`

3. **Configure Git**:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

4. **Create a new repository** on GitHub:
   - Click the "+" icon → "New repository"
   - Name it: `vietnamese-restaurant-game`
   - Add description: "A cooking game celebrating Vietnamese culture"
   - Choose "Public" and check "Add a README"
   - Click "Create repository"

5. **Upload your game**:
   ```bash
   # Navigate to your game folder
   cd path/to/your/game
   
   # Initialize git
   git init
   
   # Add files
   git add vietnamese_restaurant.py
   git add README.md
   
   # Commit
   git commit -m "Initial commit: Vietnamese restaurant game"
   
   # Connect to GitHub (replace USERNAME and REPO_NAME)
   git remote add origin https://github.com/USERNAME/REPO_NAME.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### Working with Your Team

**Cloning the repository** (for team members):
```bash
git clone https://github.com/USERNAME/vietnamese-restaurant-game.git
cd vietnamese-restaurant-game
```

**Making changes**:
```bash
# Pull latest changes first
git pull

# Make your changes to the code...

# Check what changed
git status

# Add your changes
git add .

# Commit with a descriptive message
git commit -m "Added Cao Lau dish and improved graphics"

# Push to GitHub
git push
```

**Creating branches** (for testing new features):
```bash
# Create and switch to a new branch
git checkout -b add-timer-feature

# Make changes...

# Commit changes
git add .
git commit -m "Added countdown timer for orders"

# Push branch to GitHub
git push -u origin add-timer-feature

# On GitHub, create a Pull Request to merge into main
```

## Project Structure Suggestion

```
vietnamese-restaurant-game/
│
├── vietnamese_restaurant.py    # Main game file
├── README.md                    # This file
├── requirements.txt             # Python dependencies
│
├── assets/                      # Future: images and sounds
│   ├── images/
│   └── sounds/
│
└── docs/                        # Future: documentation
    ├── dishes.md               # Information about dishes
    └── development.md          # Development notes
```

## Contributing

If working with a team, consider these practices:

1. **Use descriptive commit messages**: "Added timer feature" not "update"
2. **Create branches for features**: Keep main branch stable
3. **Test before pushing**: Make sure the game runs
4. **Document your changes**: Update README when adding features
5. **Communicate**: Let teammates know what you're working on

## Vietnamese Cultural Resources

To add more authentic content:

- Research Vietnamese cuisine history
- Learn about regional differences (North vs South Vietnam)
- Understand traditional cooking methods
- Include cultural context in fun facts
- Consult with family members or Vietnamese community

## License

This is an educational project celebrating Vietnamese culture. Feel free to modify and share!

---

**Made with ❤️ to celebrate Vietnamese culture and food**

🍜 Chúc ngon miệng! (Enjoy your meal!)
