#Het spel:
class SnakeGame:
    def _init_(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((WIDTH, HEIGHT + 60))
        pygame.display.set_caption("Snake")
        self.clock   = pygame.time.Clock()
        self.font_lg = pygame.font.SysFont("couriernew", 36, bold=True)
        self.font_md = pygame.font.SysFont("couriernew", 18)
        self.font_sm = pygame.font.SysFont("couriernew", 13)
        self.reset()

    def reset(self):
        self.snake      = [SnakeSegment(10, 10, is_head=True),
                           SnakeSegment(9,  10),
                           SnakeSegment(8,  10)]
        self.direction  = (1, 0)
        self.next_dir   = (1, 0)
        self.score      = 0
        self.speed      = INIT_SPEED
        self.tick_timer = 0
        self.phase      = "start"   # start | spelen | dood
        self.food       = self._spawn_food()

    # ETEN SPAWNEN: random positie vinden die niet bezet is door de slang
    def _occupied(self):
        return {(s.x, s.y) for s in self.snake}

    def _spawn_food(self):
        occupied = self._occupied()
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in occupied:
                return Food(x, y)

    # iNPUT: richting veranderen, maar geen 180° omkeer toetsaan
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.phase in ("start", "dead"):
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset()
                        self.phase = "playing"
                    return

                # Richting invoer — geen 180° omkeer toestaan
                dx, dy = self.direction
                if event.key in (pygame.K_UP, pygame.K_w) and dy == 0:
                    self.next_dir = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and dy == 0:
                    self.next_dir = (0,  1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and dx == 0:
                    self.next_dir = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and dx == 0:
                    self.next_dir = (1,  0)