# world-of-rectangles

## Implemented features

1. Double click to add new rectangle
2. Drag and drop rectangle to move it
3. Click the port, then drag the line and drop it to another port to create connection
4. Color of the rectangle is chosen randomly from fixed colors list
5. Rectangles can not overlap each other - they stay in the last available position
6. Rectangles can not be moved outside of game field
7. Rectangle can not be added if there is not enough space for it
8. Links and ports positions are updated when rectangle is being moved
9. Double click location is the center of created rectangle.
10. Rectangle can be dragged by any of its points
11. Window will not be resized if some of the rectangles block the way
12. Added documentation
13. Added tests

## Installation

1. Install Python3
2. Clone the game files to a new folder
3. Run `python -m pip install .` from the folder to build project and install dependencies
4. Run `pytest` from the folder to run tests
5. Move to `src` folder run `cd src`
6. Run `python Main.py` from the `src` folder to start the Application
