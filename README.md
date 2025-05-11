## Painter
This is a game project for a college assignment. In the game, your goal is to paint the whole floor. 

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

### To try the game...
- On Windows, you can download the executable version from the 'releases' area on the right of the page.
- On any platform, you can clone this repository and execute main_offline.py with Python.
#### In future...
- I plan to create Linux executable version(s).
- I was unsucessful in creating a web build with pygbag, and I'm unclear what the issue is, but hope to resolve it.
  - pygbag would also allow me to create a mobile build, though the controls would probably need a rework to allow that.

### Ideas to make the game more interesting
- Some areas can be painted, but don't have to be,
  - because those bits of the floor are going to have furniture on top
- Move freely around the area, no grid
  - would that make it more annoying, because you could miss tiny bits?
  - It would definitely be more complex to program.
- Limit on the number of times you can cross the edge of the floor
  - indicated by the grid edge lines turning red.

### Attribution
Made using pygame-ce [https://pypi.org/project/pygame-ce/].
Level data stored using YAML and PyYAML [https://pypi.org/project/PyYAML/]
I attempted to create a web build with pygbag,
following [https://pygame-web.github.io/wiki/publishing/github.io/],
but it doesn't currently work.
Executable build(s) created with pyinstaller [https://pypi.org/project/pyinstaller/].