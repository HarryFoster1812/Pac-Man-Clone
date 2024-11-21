from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage
from src.objects.ghosts.ghost_state import GhostState


# Pink
class Pinky(Ghost):
    def __init__(self, start_pos, maze, pacman):
        super(Pinky, self).__init__(start_pos, maze, pacman)
        self.image = GameImage(
            "assets/Ghosts/Pink/Pink",
            load_ghost_variations=True)  # need to fill this out
        self.scatter_cell = [2, 0]
        self.colour = "pink"
        self.direction = [0, 1]
        self.next_direction = [0, 1]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell
        self.state = GhostState.IN_GHOST_HOUSE
        self.ghost_house_target = start_pos

    def reset(self, level, maze, startpos):
        super().reset(level, maze, startpos)

        parent = self.image.parent
        id = self.image.id
        self.image = GameImage(
            "assets/Ghosts/Pink/Pink",
            load_ghost_variations=True)  # need to fill this out
        self.image.id = id
        self.image.parent = parent

        self.direction = [0, 1]
        self.next_direction = [0, 1]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell

    def calculateTarget(self):
        match(self.state):
            case GhostState.CHASE:
                pacman_loc = self.pacman.current_cell[:]
                pacman_dir = self.pacman.direction[:]
                pacman_dir = [component * 2 for component in pacman_dir]
                if pacman_dir == [0, -2]:
                    # this is to implement the original bug that was present in
                    # the original game
                    pacman_dir = [-2, -2]
                self.target = pacman_loc
                self.target[0] += pacman_dir[0]
                self.target[1] += pacman_dir[1]

            case GhostState.SCATTER:
                self.target = self.scatter_cell
            case GhostState.FRIGHTENED:
                self.target = self.current_cell
