import pygame
import random
import sys

GRID_SIZE   = 20
CELL_SIZE   = 28
WIDTH       = GRID_SIZE * CELL_SIZE
HEIGHT      = GRID_SIZE * CELL_SIZE
FPS         = 60
INIT_SPEED  = 8   

# Kleuren
BG          = (26,  26,  46)
GRID_COLOR  = (255, 255, 255, 10)
HEAD_COLOR  = (74,  222, 128)
BODY_COLOR  = (34,  197, 94)
FOOD_COLOR  = (248, 113, 113)
TEXT_COLOR  = (255, 255, 255)
DIM_COLOR   = (150, 150, 150)
OVERLAY     = (15,  15,  26,  210)


# ── Unit base class (polymorphism) ─────────────────────────
class Unit:
    """Basisklasse voor alle speeleenheden."""
    def __init__(self, x, y, color):
        self.x     = x
        self.y     = y
        self.color = color

    def draw(self, surface):
        raise NotImplementedError

    def get_rect(self):
        return pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)


class SnakeSegment(Unit):
    """Één segment van het slangenlichaam."""
    def __init__(self, x, y, is_head=False):
        color = HEAD_COLOR if is_head else BODY_COLOR
        super().__init__(x, y, color)
        self.is_head = is_head

    def draw(self, surface):
        r = self.get_rect().inflate(-2, -2)
        pygame.draw.rect(surface, self.color, r, border_radius=4)


class Food(Unit):
    """Het eten dat de slang opeet."""
    def __init__(self, x, y):
        super().__init__(x, y, FOOD_COLOR)

    def draw(self, surface):
        cx = self.x * CELL_SIZE + CELL_SIZE // 2
        cy = self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(surface, self.color, (cx, cy), CELL_SIZE // 2 - 3)


#Het spel:
class SnakeGame:
    def __init__(self):
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

    # ETEN SPAWNEN: willekeurige positie vinden die niet bezet is door de slang
    def _occupied(self):
        return {(s.x, s.y) for s in self.snake}

    def _spawn_food(self):
        occupied = self._occupied()
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in occupied:
                return Food(x, y)

    # iNPUT: richting veranderen, maar geen 180° omkeer toestaan
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

    # DYNAMIEK van het spel: slang bewegen, botsingen detecteren, eten spawnen
    def update(self, dt):
        if self.phase != "playing":
            return

        self.tick_timer += dt
        if self.tick_timer < 1.0 / self.speed:
            return
        self.tick_timer = 0

        self.direction = self.next_dir
        dx, dy = self.direction
        head   = self.snake[0]
        nx     = head.x + dx
        ny     = head.y + dy

        # Botsing met de muur. Game Over
        if nx < 0 or nx >= GRID_SIZE or ny < 0 or ny >= GRID_SIZE:
            self.phase = "dead"
            return

        # Botsing met zichzelf. Game Over
        if (nx, ny) in self._occupied():
            self.phase = "dead"
            return

        # Beweeg: nieuwe kop invoegen, kleuren bijwerken
        self.snake.insert(0, SnakeSegment(nx, ny, is_head=True))
        self.snake[1].is_head = False
        self.snake[1].color   = BODY_COLOR

        # Eten opeten
        if nx == self.food.x and ny == self.food.y:
            self.score += 10
            self.speed  = min(18, INIT_SPEED + self.score // 30)
            self.food   = self._spawn_food()
        else:
            self.snake.pop()

    # Uiterlijk: grid, slang, eten en score. 
    def draw(self):
        self.screen.fill(BG)
        self._draw_grid()
        self._draw_hud()

        
        self.food.draw(self.screen)
        for seg in reversed(self.snake):
            seg.draw(self.screen)

        
        if self.phase == "start":
            self._draw_overlay("SNAKE",
                               ["rode punt is eten en zorgt dat de slang langer wordt",
                                "Pijltjestoetsen of WASD om te bewegen",
                                "",
                                "DRUK OP SPATIE OF ENTER"],
                               HEAD_COLOR)
        elif self.phase == "dead":
            self._draw_overlay("GAME OVER",
                               [f"Score: {self.score}",
                                "",
                                "DRUK OP SPATIE OM OPNIEUW TE SPELEN"],
                               FOOD_COLOR)

        pygame.display.flip()

    def _draw_grid(self):
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(s, (255, 255, 255, 8),
                             (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
            pygame.draw.line(s, (255, 255, 255, 8),
                             (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        self.screen.blit(s, (0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255, 30),
                         (0, 0, WIDTH, HEIGHT), 1)

    def _draw_hud(self):
        #  bar onder het speelruimte 
        hud_y = HEIGHT + 10
        score_txt = self.font_md.render(f"SCORE  {self.score}", True, TEXT_COLOR)
        best_txt  = self.font_sm.render(f"LENGTE  {len(self.snake)}", True, DIM_COLOR)
        speed_txt = self.font_sm.render(f"SNELHEID  {self.speed}", True, DIM_COLOR)
        self.screen.blit(score_txt, (10, hud_y))
        self.screen.blit(best_txt,  (WIDTH // 2 - 40, hud_y + 4))
        self.screen.blit(speed_txt, (WIDTH - 90, hud_y + 4))

    def _draw_overlay(self, title, lines, title_color):
        # Transparant overlay over speelveld
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 15, 26, 200))
        self.screen.blit(overlay, (0, 0))

        # Titelregel
        title_surf = self.font_lg.render(title, True, title_color)
        tx = WIDTH // 2 - title_surf.get_width() // 2
        self.screen.blit(title_surf, (tx, HEIGHT // 2 - 80))

        # Tekstregels
        for i, line in enumerate(lines):
            color = TEXT_COLOR if line and not line.startswith("DRUK") else DIM_COLOR
            surf  = self.font_md.render(line, True, color)
            x     = WIDTH // 2 - surf.get_width() // 2
            self.screen.blit(surf, (x, HEIGHT // 2 - 20 + i * 28))

    # Hoofd While loop
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()


#Begin het spel
if __name__ == "__main__":
    SnakeGame().run()
