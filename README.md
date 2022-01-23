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
        - **Body** - the in game appreance of the gameobject.
        - **Stats** - the stats of the gameobjectin game stats of the entity.
        - **Entity** - a pygame sprites with ID component and a name:
          - **Player** - a player controlled entity with a body and stats component.
          - **Gameobject** - an entity with a body component:
            - **Walls** - a simple brown gameobject that doesn't move.
            - **Actors** - gameobjects with with more functionality:
              - **Enemy** - an actor which attacks that player
    - Core classes:
        - **Game** - the main class that handles the game loop.
        - **Color** - a helper class for creating colors.
        - **Style** - color palette system that allows you to easily change color of the whole game during runtime.

## Roadmap


### spec - ECS, Collision, Physics

- [x] Game and loop
- [x] Components
  - [x] ID
  - [x] Body
  - [x] Stats
- [x] Entities
  - [x] Player
  - [x] Gameobjects
    - [x] Walls
    - [x] Actors
- [ ] Systems
  - [x] Camera
  - [x] Collision
  - [ ] Physics

### v0.1.0 - Managers

- [ ] Systems
- [ ] Scene
- [ ] Entity
- [ ] Actors
- [ ] Sound
- [ ] Save

### v0.2.0 - Procedural generation

- [ ] ECS
- [ ] Map
- [ ] Art
- [ ] Sound

### v0.3.0 - VFX

- [ ] Particle system
- [ ] Lights
- [ ] Post processing
- [ ] Shaders

### v0.x.0 - TBD...

- [ ] Menus with easy navigation
- [ ] Prefabs to allow for easily creating entire scenes/objects
- [ ] Spritesheet and atlas for animations
- [ ] Sharing and saving seeds
- [ ] Map building through external tools/files
- [ ] Parallax scrolling
- [ ] Build for Web, Mobile, PC, and Mac
- [ ] Commandline tools
- [ ] Item pickups and inventory system
- [ ] Customizable weapons
- [ ] Achievments
