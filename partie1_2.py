import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 600, 600
FPS = 60
RADIUS = 15  # Taille des points d'intersection

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fanorontelo")

# Définition des intersections
INTERSECTIONS = [(100, 100), (300, 100), (500, 100),
                 (100, 300), (300, 300), (500, 300),
                 (100, 500), (300, 500), (500, 500)]

board = {pos: None for pos in INTERSECTIONS}
player_to_move = 'O'
pieces = {'X': [], 'O': []}
placement_phase = True
selected_piece = None


# Fonction pour dessiner le plateau avec intersections
def draw_board():
    screen.fill(WHITE)

    # Dessiner les lignes du plateau
    pygame.draw.line(screen, BLACK, INTERSECTIONS[0], INTERSECTIONS[2], 5)
    pygame.draw.line(screen, BLACK, INTERSECTIONS[3], INTERSECTIONS[5], 5)
    pygame.draw.line(screen, BLACK, INTERSECTIONS[6], INTERSECTIONS[8], 5)

    pygame.draw.line(screen, BLACK, INTERSECTIONS[0], INTERSECTIONS[6], 5)
    pygame.draw.line(screen, BLACK, INTERSECTIONS[1], INTERSECTIONS[7], 5)
    pygame.draw.line(screen, BLACK, INTERSECTIONS[2], INTERSECTIONS[8], 5)

    pygame.draw.line(screen, BLACK, INTERSECTIONS[0], INTERSECTIONS[8], 5)
    pygame.draw.line(screen, BLACK, INTERSECTIONS[2], INTERSECTIONS[6], 5)

    # Dessiner les points d'intersection
    for pos in INTERSECTIONS:
        pygame.draw.circle(screen, BLACK, pos, RADIUS)

    # Dessiner les pièces
    for pos, piece in board.items():
        if piece:
            color = RED if piece == 'X' else BLUE
            pygame.draw.circle(screen, color, pos, RADIUS + 10)

    pygame.display.flip()


# Fonction pour détecter l'intersection la plus proche d'un clic
def get_nearest_intersection(pos):
    x, y = pos
    for inter in INTERSECTIONS:
        if abs(inter[0] - x) < 50 and abs(inter[1] - y) < 50:
            return inter
    return None


def handle_click(pos):
    global player_to_move, placement_phase, selected_piece
    nearest = get_nearest_intersection(pos)

    if nearest is None:
        return  # Clic hors des intersections

    if placement_phase:
        # Phase de placement
        if board[nearest] is None:  # Vérifier que l'intersection est vide
            board[nearest] = player_to_move
            pieces[player_to_move].append(nearest)

            # Vérifier si la phase de placement est terminée
            if len(pieces['X']) == 3 and len(pieces['O']) == 3:
                placement_phase = False

            # Alterner entre les joueurs après chaque placement
            player_to_move = 'X' if player_to_move == 'O' else 'O'
    else:
        # Phase de déplacement
        if selected_piece:
            # Vérifier si la destination est vide et adjacente à la pièce sélectionnée
            print(board)
            if board[nearest] is None and is_adjacent(selected_piece, nearest) and get_successor(selected_piece, nearest):

                move_piece(selected_piece, nearest)
                selected_piece = None
            else:
                selected_piece = None
        elif board[nearest] == player_to_move:
            # Sélectionner une pièce si c'est la pièce du joueur
            selected_piece = nearest

def is_adjacent(pos1, pos2):
    return abs(pos1[0] - pos2[0]) == 200 or abs(pos1[1] - pos2[1]) == 200

def get_successor(pos,end):
    if (pos[0] == 100 and pos[1] == 100):
        return (end[0] == 100 and end[1] == 300) or (end[0] == 300 and end[1] == 100) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 100 and pos[1] == 300):
        return (end[0] == 100 and end[1] == 100) or (end[0] == 100 and end[1] == 500) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 100 and pos[1] == 500):
        return (end[0] == 100 and end[1] == 300) or (end[0] == 300 and end[1] == 500) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 300 and pos[1] == 100):
        return (end[0] == 100 and end[1] == 100) or (end[0] == 500 and end[1] == 100) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 300 and pos[1] == 300):
        return 1

    if (pos[0] == 300 and pos[1] == 500):
        return (end[0] == 100 and end[1] == 500) or (end[0] == 500 and end[1] == 500) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 500 and pos[1] == 100):
        return (end[0] == 300 and end[1] == 100) or (end[0] == 500 and end[1] == 300) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 500 and pos[1] == 300):
        return (end[0] == 500 and end[1] == 100) or (end[0] == 500 and end[1] == 500) or (end[0] == 300 and end[1] == 300)

    if (pos[0] == 500 and pos[1] == 500):
        return (end[0] == 300 and end[1] == 500) or (end[0] == 500 and end[1] == 300) or (end[0] == 300 and end[1] == 300)

# Déplacer une pièce avec animation
def move_piece(start, end):
    global player_to_move
    board[end] = board[start]
    board[start] = None
    pieces[player_to_move].remove(start)
    pieces[player_to_move].append(end)
    player_to_move = 'X'

def check_winner():
    winning_lines = [
        [(100, 100), (300, 100), (500, 100)],
        [(100, 300), (300, 300), (500, 300)],
        [(100, 500), (300, 500), (500, 500)],
        [(100, 100), (100, 300), (100, 500)],
        [(300, 100), (300, 300), (300, 500)],
        [(500, 100), (500, 300), (500, 500)],
        [(100, 100), (300, 300), (500, 500)],
        [(500, 100), (300, 300), (100, 500)],
    ]

    for line in winning_lines:
        values = [board[pos] for pos in line]
        if values == ['X', 'X', 'X']:
            return 'X'
        if values == ['O', 'O', 'O']:
            return 'O'
    return None


def handle_ia_move():
    global player_to_move
    if player_to_move == 'X':  # S'assurer que c'est bien le tour de l'IA
        best_move = find_best_move(board)  # Trouver le meilleur coup pour l'IA

        # Vérifier si l'IA a une pièce à déplacer vers la meilleure position
        piece_to_move = None
        for piece in pieces['X']:  # Vérifier toutes les pièces de l'IA
            if is_adjacent(piece, best_move):  # Si la pièce est déjà adjacent à la meilleure position
                piece_to_move = piece
                break  # L'IA a trouvé la pièce à déplacer

        if piece_to_move:
            # Déplacer la pièce de l'IA
            move_piece(piece_to_move, best_move)

        # Alterner entre les joueurs
        player_to_move = 'O'

def handle_ia_placement():
    global player_to_move, placement_phase

    if len(pieces['X']) < 3:  # L'IA ne doit pas placer plus de 3 pièces
        available_positions = [pos for pos in INTERSECTIONS if board[pos] is None]
        if available_positions:
            move = random.choice(available_positions)  # Sélectionner un mouvement au hasard
            board[move] = 'X'  # Le coup de l'IA
            pieces['X'].append(move)  # Ajouter la pièce de l'IA

            # Vérifier si la phase de placement est terminée
            if len(pieces['X']) == 3 and len(pieces['O']) == 3:
                placement_phase = False  # Fin de la phase de placement

            # Alterner entre les joueurs après chaque placement
            player_to_move = 'O' if player_to_move == 'X' else 'X'

def evaluate(board):
    # Définition des lignes gagnantes possibles sur votre plateau
    winning_lines = [
        [(100, 100), (300, 100), (500, 100)],
        [(100, 300), (300, 300), (500, 300)],
        [(100, 500), (300, 500), (500, 500)],
        [(100, 100), (100, 300), (100, 500)],
        [(300, 100), (300, 300), (300, 500)],
        [(500, 100), (500, 300), (500, 500)],
        [(100, 100), (300, 300), (500, 500)],
        [(500, 100), (300, 300), (100, 500)],
    ]

    # Vérifier si l'un des joueurs a gagné
    for line in winning_lines:
        values = [board[pos] for pos in line]
        if values == ['X', 'X', 'X']:  # L'IA gagne
            return 1
        if values == ['O', 'O', 'O']:  # L'utilisateur gagne
            return -1
    return 0  # Match nul ou état en cours

def get_possible_moves(board, player):
    possible_moves = []
    for intersection in INTERSECTIONS:
        if board[intersection] is None:  # Vérifier si l'intersection est vide
            new_board = board.copy()  # Copier l'état actuel du plateau
            new_board[intersection] = player  # Ajouter le coup du joueur
            possible_moves.append((new_board, intersection))
    return possible_moves

def minimax(board, depth, maximizing_player):
    score = evaluate(board)  # Évaluer l'état actuel
    if score == 1 or score == -1:  # Si un gagnant est trouvé
        return score
    if depth == 0:  # Limite de profondeur pour ne pas faire trop de calculs
        return 0

    if maximizing_player:  # C'est le tour de l'IA
        best = -float('inf')
        for new_board, move in get_possible_moves(board, 'X'):
            best = max(best, minimax(new_board, depth - 1, False))  # Tour de l'utilisateur
        return best
    else:  # C'est le tour de l'utilisateur
        best = float('inf')
        for new_board, move in get_possible_moves(board, 'O'):
            best = min(best, minimax(new_board, depth - 1, True))  # Tour de l'IA
        return best

def find_best_move(board):
    best_move = None
    best_value = -float('inf')

    for new_board, move in get_possible_moves(board, 'X'):
        move_value = minimax(new_board, 3, False)  # Profondeur 3 pour l'IA
        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move
GREEN = (0, 255, 0)  # Définir la couleur verte

def draw_text(text, font, color, surface, x, y):
    """Affiche du texte à la position (x, y) sur la surface donnée."""

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def display_end_message(winner):
    font = pygame.font.Font(None, 74)
    if winner == 'X':
        message = "Vous avez perdu!"
    elif winner == 'O':
        message = "Vous avez gagné!"
    else:
        message = "Match nul!"

    draw_text(message, font, GREEN, screen, WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if placement_phase:
                if player_to_move == 'O':  # L'utilisateur fait son coup pendant la phase de placement
                    handle_click(pygame.mouse.get_pos())
                elif player_to_move == 'X':  # L'IA joue pendant la phase de placement
                    handle_ia_placement()
            else:
                # Après la phase de placement, l'utilisateur ou l'IA peuvent déplacer leurs pièces
                if player_to_move == 'O':
                    handle_click(pygame.mouse.get_pos())  # L'utilisateur fait son mouvement
                elif player_to_move == 'X':
                    handle_ia_move()  # L'IA fait son mouvement

    draw_board()  # Dessiner le plateau à chaque itération

    # Vérifier la fin de la partie
    winner = check_winner()
    if winner:
        display_end_message(winner)
        pygame.display.flip()  # Met à jour l'écran
        pygame.time.wait(3000)  # Attendre 3 secondes avant de quitter ou recommencer
        pygame.quit()
        sys.exit()