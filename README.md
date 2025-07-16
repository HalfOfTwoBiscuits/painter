## Painter
This is a game project. In the game, your goal is to paint the whole floor. 
It was originally made for a college assignment. 
The code I handed in for that assignment is on the 'main' branch,
and the newest version with extra features is on the 'further-work-after-handin' branch.
You can download a Windows executable of either version from the 'releases' section.

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

#### The level editor
You can also make your own floors to paint! In the level editor, you left-click to paint a cell, and right-click to set the starting position.
Your floors will be grouped into a floorpack. If you'd like everyone to play your floorpack, consider making a pull request with the corresponding file from your resources/floors directory.

### To try the game...
- On Windows, you can download the executable version from the 'releases' area on the right of the page.
- On any platform, you can clone this repository, and execute run_game.py, run_editor.py, or run_game_or_editor.py with Python.

#### Ideas for future development...
- On starting a level, display which number it is and how many are left to go.

- Add a 'Test' shortcut in the editor to help you test levels as you create them.
  - Add a 'Check Possible' button that tells you if the floor is possible to paint or not.

- Aesthetic options when creating levels:
  - Add the ability to change the colour of the paint.
  - Right click the painter's starting position to change the direction the graphic initially faces.
  - Allow giving individual floors a name, not just floorpacks. This would also make it easier to keep track of what you're doing when re-ordering them.

- Enforce a minimum and maximum size for a floor.
  - My logic for determining the pixel dimensions of the grid could be made more space-efficient to allow bigger levels.
  - This also might make it easier to tell what's on the grid and what isn't.

- Improve the usability of the input fields in the editor.
  - Increase contrast, and make them more aesthetically consistent with the rest of the menus.
  - Start with the cursor in the first field.
  - Allow keyboard navigation between the fields.
  - Allow pressing keys to submit or cancel.

- The level re-ordering menu might be more intuitive if you dragged the levels into place with the mouse.

- In the editor, maybe merge the 'Save' and 'Exit' options into a 'Save and Exit' option? Personally, I like being able to fiddle with a level without necessarily saving the result into the game. But maybe this is a niche preference.

- Areas that can be painted, but don't have to be, because there's going to be furniture on top.

- Challenges to encourage finding alternative solutions to a level, such as: 'Wrap round the edge twice', 'Don't wrap round the edge', or 'Move left first'.
  - This might work just as supplementary material outside the game.
  - If it was a restriction ingame, the grid lines could change colour to indicate you should or shouldn't wrap round.
  - Maybe the cleanest way is to represent all challenges by a position that you have to end the level in. Most alternative solutions would involve ending in a different cell.
  - There could be a challenge for every distinct way to paint a floor, not just ones that the creator deems less obvious.

- Linux and MacOS executable version(s).
  - In the level editor, an option that swaps the effects of the left and right mouse button, so that MacOS users can use all the features without a right click.

- A web build. I was unsucessful in creating one with pygbag, and I'm unclear what the issue is, so maybe I'll ask?
  - pygbag would also allow me to create a mobile build, though the controls would probably need a rework to allow that.

### Attribution
Made using pygame-ce [https://pypi.org/project/pygame-ce/].
Level data stored using YAML and PyYAML [https://pypi.org/project/PyYAML/]
I attempted to create a web build with pygbag,
following [https://pygame-web.github.io/wiki/publishing/github.io/],
but it doesn't currently work.
Executable build(s) created with pyinstaller [https://pypi.org/project/pyinstaller/].