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
if _name_ == "_main_":
    SnakeGame().run()
