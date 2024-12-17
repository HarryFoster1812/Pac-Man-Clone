# Diff Details

Date : 2024-11-21 13:04:01

Directory /home/harryfoster/git/comp16321-labs_r49769hf

Total : 68 files,  627 codes, 41 comments, 181 blanks, all 849 lines

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 2 | 0 | 1 | 3 |
| [game_solution.py](/game_solution.py) | Python | 517 | 79 | 177 | 773 |
| [src/animate.py](/src/animate.py) | Python | 63 | 6 | 24 | 93 |
| [src/game.py](/src/game.py) | Python | 240 | 61 | 95 | 396 |
| [src/gameImage.py](/src/gameImage.py) | Python | 83 | 4 | 20 | 107 |
| [src/leaderboard.json](/src/leaderboard.json) | JSON | 1 | 0 | 0 | 1 |
| [src/leaderboard.py](/src/leaderboard.py) | Python | 25 | 0 | 9 | 34 |
| [src/maze.py](/src/maze.py) | Python | 192 | 5 | 45 | 242 |
| [src/objects/consumable/apple.py](/src/objects/consumable/apple.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/bell.py](/src/objects/consumable/bell.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/cherry.py](/src/objects/consumable/cherry.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/consumable.py](/src/objects/consumable/consumable.py) | Python | 7 | 0 | 1 | 8 |
| [src/objects/consumable/dot.py](/src/objects/consumable/dot.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/energizer.py](/src/objects/consumable/energizer.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/galaxian.py](/src/objects/consumable/galaxian.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/grapes.py](/src/objects/consumable/grapes.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/key.py](/src/objects/consumable/key.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/peach.py](/src/objects/consumable/peach.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/consumable/strawberry.py](/src/objects/consumable/strawberry.py) | Python | 0 | 0 | 1 | 1 |
| [src/objects/ghosts/Blinky.py](/src/objects/ghosts/Blinky.py) | Python | 33 | 1 | 6 | 40 |
| [src/objects/ghosts/Clyde.py](/src/objects/ghosts/Clyde.py) | Python | 38 | 1 | 7 | 46 |
| [src/objects/ghosts/Ghost.py](/src/objects/ghosts/Ghost.py) | Python | 285 | 57 | 92 | 434 |
| [src/objects/ghosts/Inky.py](/src/objects/ghosts/Inky.py) | Python | 35 | 2 | 7 | 44 |
| [src/objects/ghosts/Pinky.py](/src/objects/ghosts/Pinky.py) | Python | 41 | 1 | 7 | 49 |
| [src/objects/ghosts/ghost_state.py](/src/objects/ghosts/ghost_state.py) | Python | 11 | 0 | 2 | 13 |
| [src/objects/map_objects/moveable.py](/src/objects/map_objects/moveable.py) | Python | 21 | 0 | 6 | 27 |
| [src/objects/map_objects/wall.py](/src/objects/map_objects/wall.py) | Python | 6 | 0 | 2 | 8 |
| [src/objects/pacman.py](/src/objects/pacman.py) | Python | 123 | 16 | 40 | 179 |
| [src/player.py](/src/player.py) | Python | 6 | 0 | 1 | 7 |
| [src/settings.py](/src/settings.py) | Python | 34 | 7 | 15 | 56 |
| [util temp programs/fontTest.py](/util%20temp%20programs/fontTest.py) | Python | 32 | 0 | 9 | 41 |
| [util temp programs/gifTest.py](/util%20temp%20programs/gifTest.py) | Python | 30 | 0 | 15 | 45 |
| [util temp programs/pickleTest.py](/util%20temp%20programs/pickleTest.py) | Python | 11 | 0 | 4 | 15 |
| [util temp programs/scaleTest.py](/util%20temp%20programs/scaleTest.py) | Python | 14 | 5 | 6 | 25 |
| [util temp programs/testKeys.py](/util%20temp%20programs/testKeys.py) | Python | 20 | 0 | 5 | 25 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/README.md](//home/r49769hf/git/comp16321-labs_r49769hf/README.md) | Markdown | -2 | 0 | -1 | -3 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/fontTest.py](//home/r49769hf/git/comp16321-labs_r49769hf/fontTest.py) | Python | -32 | 0 | -9 | -41 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/game_solution.py](//home/r49769hf/git/comp16321-labs_r49769hf/game_solution.py) | Python | -242 | -46 | -102 | -390 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/gifTest.py](//home/r49769hf/git/comp16321-labs_r49769hf/gifTest.py) | Python | -30 | 0 | -15 | -45 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/scaleTest.py](//home/r49769hf/git/comp16321-labs_r49769hf/scaleTest.py) | Python | -14 | -5 | -6 | -25 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/animate.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/animate.py) | Python | -61 | -6 | -23 | -90 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/game.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/game.py) | Python | -115 | -60 | -50 | -225 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/gameImage.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/gameImage.py) | Python | -72 | -4 | -18 | -94 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/leaderboard.json](//home/r49769hf/git/comp16321-labs_r49769hf/src/leaderboard.json) | JSON | -1 | 0 | 0 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/leaderboard.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/leaderboard.py) | Python | -16 | 0 | -7 | -23 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/maze.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/maze.py) | Python | -96 | -5 | -33 | -134 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/apple.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/apple.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/bell.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/bell.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/cherry.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/cherry.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/consumable.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/consumable.py) | Python | -7 | 0 | -1 | -8 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/dot.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/dot.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/energizer.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/energizer.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/galaxian.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/galaxian.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/grapes.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/grapes.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/key.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/key.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/peach.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/peach.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/strawberry.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/consumable/strawberry.py) | Python | 0 | 0 | -1 | -1 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Blinky.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Blinky.py) | Python | -21 | -1 | -2 | -24 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Clyde.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Clyde.py) | Python | -26 | -1 | -3 | -30 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Ghost.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Ghost.py) | Python | -282 | -51 | -84 | -417 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Inky.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Inky.py) | Python | -22 | -2 | -3 | -27 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Pinky.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/ghosts/Pinky.py) | Python | -32 | -1 | -4 | -37 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/map_objects/moveable.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/map_objects/moveable.py) | Python | -21 | 0 | -6 | -27 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/map_objects/powerup.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/map_objects/powerup.py) | Python | -8 | -1 | -2 | -11 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/map_objects/wall.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/map_objects/wall.py) | Python | -4 | 0 | -1 | -5 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/objects/pacman.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/objects/pacman.py) | Python | -101 | -14 | -31 | -146 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/src/settings.py](//home/r49769hf/git/comp16321-labs_r49769hf/src/settings.py) | Python | -18 | -7 | -9 | -34 |
| [/home/r49769hf/git/comp16321-labs_r49769hf/testKeys.py](//home/r49769hf/git/comp16321-labs_r49769hf/testKeys.py) | Python | -20 | 0 | -5 | -25 |

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details