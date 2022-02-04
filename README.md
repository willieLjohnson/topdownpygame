# core: topdownpygame

The core mechanics of a topdown 2d game created with pygame.

## Goal

- [ ] Easy to use ECS.
- [ ] Importable into any project 'import topdowncore'
- [ ] Main functionality from a single import.
- [ ] Visual FX of near production quality 2d indie game with a debug mode that shows the underlying progammer art.
- [ ] Ingame debug commands through simple ui textfield.
- [ ] Procedural generation.
- [ ] Fully featured demo.

## Features

- Super simple.
- Basic collision detection and physics:
    - Pushing objects around.
    - Acceleration and velocity.
- Modularity through ECS and OOP:
    - Components and Objects:
        - **Body** - the in game appreance of the entity.
        - **Stats** - the stats of the entityin game stats of the entity.
        - **Object** - a pygame sprites with ID component and a name:
          - **Player** - a player controlled entity with a body and stats component.
          - **entity** - an entity with a body component:
            - **Walls** - a simple brown entity that doesn't move.
            - **Actors** - entities with with more functionality:
              - **Enemy** - an actor which attacks that player
    - Core classes:
        - **Game** - the main class that handles the game loop.
        - **Color** - a helper class for creating colors.
        - **Style** - color palette system that allows you to easily change color of the whole game during runtime.

