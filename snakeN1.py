import pygame
import random

# Initialiser Pygame
pygame.init()

# Définir les couleurs
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Définir les dimensions de la fenêtre
dis_width = 800
dis_height = 600

# Le score seuil
score_threshold = 10 

# Créer la fenêtre
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game mach02')

# Définir les variables du jeu
clock = pygame.time.Clock()
snake_block = 10
snake_speed_level1 = 5  # Vitesse réduite pour le niveau 1
snake_speed_level2 = 10
snake_speed_level3 = 15   

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    """
    Affiche le serpent sur l'écran.
    :param snake_block: Taille d'un segment du serpent.
    :param snake_list: Liste des positions des segments du serpent.
    """
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displacement=0):
    """
    Affiche un message à l'écran.
    :param msg: Le message à afficher.
    :param color: La couleur du texte.
    :param y_displacement: Le déplacement en y du message.
    """
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displacement])

def your_score(score):
    """
    Affiche le score actuel du joueur.
    :param score: Le score à afficher.
    """
    value = score_font.render("Votre score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def gameLoop(level):
    """
    Fonction principale du jeu, gère la boucle de jeu pour un niveau donné.
    :param level: Le niveau actuel du jeu.
    """
    game_over = False
    game_close = False

    # Position initiale du serpent
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Variables de changement de direction
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Position initiale de la nourriture
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Définir la vitesse du serpent en fonction du niveau
    if level == 1:
        snake_speed = snake_speed_level1
    elif level == 2:
        snake_speed = snake_speed_level2
    else:
        snake_speed = snake_speed_level3

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("Vous avez perdu!", red, -50)
            your_score(Length_of_snake - 1)
            draw_button("Réessayer", 150, 500, 150, 50, green, blue, lambda: gameLoop(level))
            draw_button("Quitter", 500, 500, 100, 50, red, red, quit_game)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)
        draw_button("Quitter", 650, 550, 100, 50, red, red, quit_game)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    if level == 1 and not game_over:
        message("Niveau 1 terminé! Pressez E pour continuer", green)
        draw_button("Quitter", 350, 500, 100, 50, red, red, quit_game)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        waiting = False
                        gameLoop(2)
                    if event.key == pygame.K_q:
                        waiting = False
                        game_over = True
                if event.type == pygame.QUIT:
                    waiting = False
                    game_over = True

    pygame.quit()
    quit()

def draw_button(msg, x, y, w, h, ic, ac, action=None):
    """
    Dessine un bouton sur l'écran et vérifie les clics de souris.
    :param msg: Le texte sur le bouton.
    :param x: La coordonnée x du bouton.
    :param y: La coordonnée y du bouton.
    :param w: La largeur du bouton.
    :param h: La hauteur du bouton.
    :param ic: La couleur initiale du bouton.
    :param ac: La couleur du bouton lorsqu'il est cliqué.
    :param action: L'action à exécuter lorsque le bouton est cliqué.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    dis.blit(text_surf, text_rect)

def text_objects(text, font):
    """
    Crée des objets de texte pour l'affichage.
    :param text: Le texte à afficher.
    :param font: La police du texte.
    """
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def quit_game():
    """
    Quitte le jeu.
    """
    pygame.quit()
    quit()

def main_menu():
    """
    Affiche le menu principal pour permettre au joueur de choisir le niveau.
    """
    menu = True
    while menu:
        dis.fill(white)
        message("Bienvenue! Choisissez un niveau:", black, -100)
        draw_button("Niveau 1", 350, 200, 100, 50, green, blue, lambda: gameLoop(1))
        draw_button("Niveau 2", 350, 300, 100, 50, green, blue, lambda: gameLoop(2))
        draw_button("Niveau 3", 350, 400, 100, 50, green, blue, lambda: gameLoop(3))
        draw_button("Quitter", 350, 500, 100, 50, red, red, quit_game)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
                quit()

# Lancer le menu principal
main_menu()
