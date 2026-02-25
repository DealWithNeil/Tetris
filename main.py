import pygame, sys
from grid import Grid

pygame.init()

font = pygame.font.SysFont("Arial", 24)

dark_blue = (44, 44, 127)

screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game_grid = Grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_grid.rotate()
                if event.key == pygame.K_r and game_grid.game_over:
                    game_grid = Grid()
                    
            if event.key == pygame.K_LEFT:
                game_grid.move(-1)
            if event.key == pygame.K_RIGHT:
                game_grid.move(1)

    game_grid.update()

    screen.fill(dark_blue)
    game_grid.draw(screen)

    score_text = font.render(f"Score: {game_grid.score}", True, (255, 255, 255))
    screen.blit(score_text, (320, 50))

    level_text = font.render(f"Level: {game_grid.level}", True, (255, 255, 255))
    screen.blit(level_text, (320, 80))

    if game_grid.game_over:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (320, 150))

    pygame.display.update()
    clock.tick(60)