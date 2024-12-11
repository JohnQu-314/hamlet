import pygame
from pygame.locals import *
import sys
from dialogue import dialogue_lines
from dialogue import fortinbras_dialogue

# Initialize Pygame
pygame.init()

# Game settings
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hamlet Castle Adventure")

claudius_img = pygame.image.load('static/claudius.png')  # Replace with the correct path to your image
hamlet_img = pygame.image.load('static/hamlet.png')      # Replace with the correct path to your image
rosen_img = pygame.image.load('static/rosen.png')
captain_img = pygame.image.load('static/captain.png')

claudius_img = pygame.transform.scale(claudius_img, (100, 200))  # Resize to 100x100 pixels
hamlet_img = pygame.transform.scale(hamlet_img, (200, 200)) 
rosen_img = pygame.transform.scale(rosen_img, (200, 200)) 
captain_img = pygame.transform.scale(captain_img, (300, 300)) 

claudius_img2 = pygame.transform.scale(claudius_img, (75, 150))  # Resize to 100x100 pixels
rosen_img2 = pygame.transform.scale(rosen_img, (150, 200)) 

claudiusyap = False


# Add a lives variable
lives = 3  # Player starts with 5 lives

# Font for displaying lives
font = pygame.font.Font(None, 36)

# Function to display lives
def draw_lives(surface, lives):
    text = font.render(f"Lives: {lives}", True, WHITE)
    surface.blit(text, (screen_width - 150, 20))  # Top-right corner

# Colors
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

# Load images
grass_image = pygame.image.load("static/grass.png")
grass_tile_size = grass_image.get_width()  # Assuming the image is square

# Player setup
player_width = 20
player_height = 20
player_speed = 1
player = pygame.Rect(screen_width // 2, screen_height // 2, player_width, player_height)
player_img = pygame.image.load('static/rosen.png')
player_img = pygame.transform.scale(player_img, (100, 100)) 

# Maps
castle_map_size = 1200
outdoor_map_size = 2300

# Door and Castle setup
door = pygame.Rect(castle_map_size // 2 - 50, castle_map_size - 20, 100, 20)  # Black door
castledoor = pygame.Rect(outdoor_map_size // 2 - 250 , outdoor_map_size // 2 - 0, 100, 20)
castle = pygame.Rect(outdoor_map_size // 2 - 400, outdoor_map_size // 2 - 400, 400, 400)  # Brown castle (center-left of outdoor map)

# Claudius setup
claudius_position = (castle_map_size // 2 - 25, castle_map_size // 2 - 25)  # Center of the castle
claudius_size = 40
claudius = pygame.Rect(*claudius_position, claudius_size, claudius_size)

rosen_position = (castle_map_size // 2 + 10, castle_map_size // 2 - 25)  # Center of the castle
rosen_size = 40
rosen = pygame.Rect(*rosen_position, rosen_size, rosen_size)

fortinbras_position = (outdoor_map_size - 100, outdoor_map_size // 2 - 25)  # Center of the castle
fortinbras_size = 30
fortinbras = pygame.Rect(*fortinbras_position, fortinbras_size, fortinbras_size)

current_dialogue_index = 0
in_cutscene = False
inyap = False

# Game state
current_map = "castle"  # "castle" or "outdoor"
camera = pygame.Rect(0, 0, screen_width, screen_height)  # Camera tracks player


#castle = pygame.Rect(outdoor_map_size // 2 - 800, outdoor_map_size // 2 - 800, 400, 400)  # Brown castle (center-left of outdoor map)

# Function to constrain the player to the map boundaries
def constrain_player(player, map_size):
    if player.left < 0:
        player.left = 0
    if player.right > map_size:
        player.right = map_size
    if player.top < 0:
        player.top = 0
    if player.bottom > map_size:
        player.bottom = map_size
    # Define the bounds of the castle (adjust values as per your map dimensions)
    castle_bounds = pygame.Rect(
        (outdoor_map_size // 2 - 400),  # x position
        (outdoor_map_size // 2 - 400),        # y position
        400,                                  # width of the castle area
        400                                   # height of the castle area
    )

# Function to draw a tiled grass background
def draw_tiled_grass(surface, camera, map_size):
    start_x = max(0, camera.x // grass_tile_size * grass_tile_size)
    start_y = max(0, camera.y // grass_tile_size * grass_tile_size)
    end_x = min(map_size, (camera.x + screen_width) // grass_tile_size * grass_tile_size + grass_tile_size)
    end_y = min(map_size, (camera.y + screen_height) // grass_tile_size * grass_tile_size + grass_tile_size)
    
    for x in range(start_x, end_x, grass_tile_size):
        for y in range(start_y, end_y, grass_tile_size):
            surface.blit(grass_image, (x - camera.x, y - camera.y))

# Function to draw dialogue
def draw_dialogue(dialogue, index):
    if index < len(dialogue):
        line = dialogue[index]
        dfont = pygame.font.SysFont('times new roman', 18)
        text_surface = dfont.render(f"{line['character']}: {line['text']}", True, WHITE)
        screen.blit(text_surface, (50, screen_height - 100))
        if line['choices']:
            for i, choice in enumerate(line['choices']):
                choice_surface = dfont.render(f"{i+1}. {choice['text']}", True, YELLOW)
                screen.blit(choice_surface, (50, screen_height - 200 + i * 30))
        if line["character"] == "Claudius":
            # Display Claudius' image in the bottom-right corner
            screen.blit(claudius_img, (screen.get_width() - claudius_img.get_width() - 20, screen.get_height() - claudius_img.get_height() - 150))
        elif line["character"] == "Hamlet":
            # Display Hamlet's image in the bottom-right corner
            screen.blit(hamlet_img, (screen.get_width() - hamlet_img.get_width() - 20, screen.get_height() - hamlet_img.get_height() - 150))
        elif line["character"] == "Rosencrantz":
            # Display Hamlet's image in the bottom-right corner
            screen.blit(rosen_img, (screen.get_width() - rosen_img.get_width() - 20, screen.get_height() - hamlet_img.get_height() - 150))
        elif line["character"] == "Captain":
            # Display Hamlet's image in the bottom-right corner
            screen.blit(captain_img, (screen.get_width() - captain_img.get_width() - 20, screen.get_height() - captain_img.get_height() - 150))

        

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if in_cutscene:

                line = dialogue_lines[current_dialogue_index]
                if line['choices']:
                    if event.key in (K_1, K_2):
                        choice_index = event.key - K_1
                        
                        if not line['choices'][choice_index]['correct']:  # Check if choice is incorrect
                            lives -= 1  # Deduct a life
                        
                        current_dialogue_index += 1
                elif event.key == K_SPACE:
                    current_dialogue_index += 1
                    if current_dialogue_index >= len(dialogue_lines):
                        in_cutscene = False
                        current_dialogue_index = 0


        if event.type == QUIT:
                    running = False
        if event.type == KEYDOWN:
                    if inyap:
                        line = fortinbras_dialogue[current_dialogue_index]
                        if line['choices']:
                            if event.key in (K_1, K_2):
                                choice_index = event.key - K_1
                                if not line['choices'][choice_index]['correct']:  # Check if choice is incorrect
                                    lives -= 1  # Deduct a life    
                                current_dialogue_index += 1

                        elif event.key == K_SPACE:
                            current_dialogue_index += 1
                            if current_dialogue_index >= len(fortinbras_dialogue):
                                inyap = False
                                current_dialogue_index = 0

    keys = pygame.key.get_pressed()
    if not in_cutscene and not inyap:
        if keys[K_LEFT]:
            player.x -= player_speed
        if keys[K_RIGHT]:
            player.x += player_speed
        if keys[K_UP]:
            player.y -= player_speed
        if keys[K_DOWN]:
            player.y += player_speed

    if player.colliderect(castle) :
        if keys[K_LEFT]:
            player.x += player_speed
        if keys[K_RIGHT]:
            player.x -= player_speed
        if keys[K_UP]:
            player.y += player_speed
        if keys[K_DOWN]:
            player.y -= player_speed

    # Check map transitions
    if current_map == "castle" and player.colliderect(door):
        current_map = "outdoor"
        player.y = castle.y + castle.height + 100
        player.x = castle.x + castle.width // 2 - player.width // 2

    elif current_map == "outdoor" and player.colliderect(castledoor):
        current_map = "castle"
        player.x = castle_map_size // 2
        player.y = castle_map_size - 150

    # Claudius interaction
    if current_map == "castle" and not in_cutscene and (player.colliderect(claudius) or player.colliderect(rosen)):
            in_cutscene = True
            current_dialogue_index = 0
            claudiusyap = True

            player.y = castle.y // 2+ castle.height -100
            player.x = castle.x - player.width // 2 - 150



    if current_map == "outdoor" and not inyap and player.colliderect(fortinbras): #and claudiusyap:
            inyap = True
            current_dialogue_index = 0

            player.y = outdoor_map_size // 2 + 50
            player.x = outdoor_map_size - 100
        


    # Constrain player
    if current_map == "castle":
        constrain_player(player, castle_map_size)
    elif current_map == "outdoor":
        constrain_player(player, outdoor_map_size)

    # Update camera
    camera.center = player.center

    # Draw map
    screen.fill(BLACK)
    if current_map == "castle":
        pygame.draw.rect(screen, BROWN, (0 - camera.x, 0 - camera.y, castle_map_size, castle_map_size))
        pygame.draw.rect(screen, BLACK, door.move(-camera.x, -camera.y))
        pygame.draw.rect(screen, BLUE, claudius.move(-camera.x, -camera.y))  # Draw Claudius
        pygame.draw.rect(screen, PURPLE, rosen.move(-camera.x, -camera.y))  # Draw Rosencrantz

        screen.blit(claudius_img2, (castle_map_size // 2 - 45 - camera.x, castle_map_size // 2 - 75 - camera.y))
        screen.blit(rosen_img2, (castle_map_size // 2 - 30 - camera.x, castle_map_size // 2 - 75 - camera.y))
    elif current_map == "outdoor":
        draw_tiled_grass(screen, camera, outdoor_map_size)
        pygame.draw.rect(screen, BLACK, castledoor.move(-camera.x, -camera.y))
        pygame.draw.rect(screen, BROWN, castle.move(-camera.x, -camera.y))
        pygame.draw.rect(screen, BROWN, fortinbras.move(-camera.x, -camera.y))

    draw_lives(screen, lives)

    # Draw player
    pygame.draw.rect(screen, RED, player.move(-camera.x, -camera.y))

    # Draw cutscene if active
    if in_cutscene:
        draw_dialogue(dialogue_lines, current_dialogue_index)

    if inyap:
        draw_dialogue(fortinbras_dialogue, current_dialogue_index)
        

    if lives == 0:
        screen.fill(BLACK)
        dfont = pygame.font.SysFont('times new roman', 18)
        defont = pygame.font.SysFont('times new roman', 36)

        game_over_text = defont.render("You Died", True, RED)
        game_over_text2 = dfont.render("You have selected too many wrong answers. ", True, WHITE)
        game_over_text3 = dfont.render("In an alternate universe, Laertes gets his revenge by stabbing", True, WHITE)
        game_over_text4 = dfont.render("you while having you drink poison juice.", True, WHITE)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
        screen.blit(game_over_text2, (screen_width // 2 - game_over_text.get_width() // 2 - 100, screen_height // 2 + 40))
        screen.blit(game_over_text3, (screen_width // 2 - game_over_text.get_width() // 2 - 160, screen_height // 2 + 60))
        screen.blit(game_over_text4, (screen_width // 2 - game_over_text.get_width() // 2 - 90, screen_height // 2 + 80))
    pygame.display.update()
    

pygame.quit()


