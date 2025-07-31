## Painter
This is a game project. In the game, your goal is to paint the whole floor.

It was originally made for a college assignment. 
The code I handed in for that assignment is on the 'assignment-version' branch,
the newest released version is on the main branch.
You can download a Windows executable of either version from the 'releases' section.
Other branches are current work-in-progress.

### Instructions
Move by pressing the arrow keys. You'll leave paint behind you as you go. 

However, the paint is wet, and you can't cross it until it's dry. You'll paint the floor in one go, and it will dry after you're done. 

If you paint yourself into a corner, don't lose hope! Crossing the edge of the floor will wrap you round to the opposite side.
You can utilise that to reach areas enclosed by paint, and find your own way to paint everything.

In menus, press the number key beside the option you want.

If you get stuck, you can:
- undo by pressing backspace
- press escape or control

By pressing escape or control, you can choose to start again, or paint a different floor instead.

### The level editor
You can also make your own floors to paint! In the level editor, you left-click to paint a cell, and right-click to set the starting position.
Your floors will be grouped into a floorpack. If you'd like everyone to play your floorpack, consider making a pull request with the corresponding file from your resources/floors directory.

### To try the game...
- You can visit [https://halfoftwobiscuits.github.io/painter/]
- On Windows, you can download an executable version from the 'releases' area on the right of the page.
- On any platform, you can clone this repository, and execute run_game.py, run_editor.py, or run_game_or_editor.py with Python.

### Mouse and keyboard controls
The game was originally designed with the keyboard in mind, and the level editor with the mouse.
However, I've tried to make them both accessible with either.

In the game, you can move by clicking an adjacent square to go to.
In the editor, you can press the arrow keys to make a cursor appear. You can then move the cursor with the arrow keys, press space to paint the square which the cursor is over, and press shift to move the painter to that square.

A full list of controls is in CONTROLS.md for reference.

Any feedback about the controls, or other accessibility feedback, is welcome.

#### Ideas for future development...
- On starting a level, display which number it is and how many are left to go.

- Aesthetic options when creating levels:
  - Add the ability to change the colour of the paint.
  - Right click the painter's starting position to change the direction the graphic initially faces.
  - Allow giving individual floors a name, not just floorpacks. This would also make it easier to keep track of what you're doing when re-ordering them.

- My logic for determining the pixel dimensions of the grid could be made more space-efficient to allow bigger levels.
  - This also might make it easier to tell what's on the grid and what isn't.

- The level re-ordering menu might be more intuitive if you dragged the levels into place with the mouse.

- In the editor, maybe merge the 'Save' and 'Exit' options into a 'Save and Exit' option? Personally, I like being able to fiddle with a level without necessarily saving the result into the game. But maybe this is a niche preference.

- Areas that can be painted, but don't have to be, because there's going to be furniture on top.

- Challenges to encourage finding alternative solutions to a level, such as: 'Wrap round the edge twice', 'Don't wrap round the edge', or 'Move left first'.
  - This might work just as supplementary material outside the game.
  - If it was a restriction ingame, the grid lines could change colour to indicate you should or shouldn't wrap round.
  - There could be a challenge for every distinct way to paint a floor, not just ones that the creator deems less obvious.
  - The cleanest way to implement this might be specific positions to end the level on. Presumably, most alternate solutions end in a different square: that's why I didn't require a certain end position all the time.

- Linux and MacOS executable version(s).
  - In the level editor, an option that swaps the effects of the left and right mouse button, so that MacOS users can reposition the painter using the mouse.

### Attribution
- Made using pygame-ce [https://pypi.org/project/pygame-ce/].
- Level data stored using YAML and PyYAML [https://pypi.org/project/PyYAML/]
- Web build(s) created with Pygbag [https://github.com/pygame-web/pygbag]
- Executable build(s) created with pyinstaller [https://pypi.org/project/pyinstaller/].