# prototype: topdownpygame

2d topdown prototype created in pygame

## Features

- Super simple.
- Basic collision detection and physics:
    - Pushing objects around
    - Acceleration and velocity
- Modularity through ECS and OOP:
    - Components and Objects:
        - Player: pygame sprite with body and stats component
        - Body: the in game appreance of the gameobject
        - Stats: the in game stats of the entity 
        - Gameobjects: base class which has a basic body component and functionality
          - Walls: a simple brown entity wit customizable color and size
          - Entities: gameobjects with more functionality, such as enemies and player
            - Enemies
- Core classes:
    - Game: Main class that handles the game loop
    - Color: Helper class for creating colors
    - Style: color palette system
 easily change color of the whole game