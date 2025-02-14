from noeud import Noeud
from noeud import generer_configurations
import csv

def print_tree(root, indent= 0, depth=1):
    print(root.str_with_indent(indent))
    print()
    if depth > 1:
        for succ in root.get_successors():
            print_tree(succ, indent + 4, depth - 1)
    

def minimax(node, depth, us='X'):
    if depth == 0 or node.is_terminal():
        return (node.eval(us), None)
    if node.player_to_move == us:
        maxEval = -1000
        best_move = None
        for child in node.get_successors():
            eval, _ = minimax(child, depth - 1, us)
            if eval > maxEval:
                maxEval = eval
                best_move = child            
        return (maxEval, best_move)                
    else:
        minEval = 1000
        best_move = None
        for child in node.get_successors():
            eval, _ = minimax(child, depth - 1, us)
            if eval < minEval:
                minEval = eval
                best_move = child
        return (minEval, best_move)
   

def alphabeta(node, depth, alpha, beta, us='X'):
    if depth == 0 or node.is_terminal():
        return (node.eval(us), None)
    if node.player_to_move == us:
        maxEval = -1000
        best_move = None
        for child in node.get_successors():
            eval, _ = alphabeta(child, depth - 1, alpha, beta, us)
            if eval > maxEval:
                maxEval = eval
                best_move = child
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return (maxEval, best_move)
    else:
        minEval = 1000
        best_move = None
        for child in node.get_successors():
            eval, _ = alphabeta(child, depth - 1, alpha, beta, us)
            if eval < minEval:
                minEval = eval
                best_move = child
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (minEval, best_move)

# Sauvegarde dans un fichier CSV
def sauvegarder_csv(fichier, configurations):
    with open(fichier, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "Label"])
        writer.writerows(configurations)


def main():
    nd = Noeud()
    # print("node tree with depth 4")
    # print_tree(nd, depth=4)

    # Génération les 500 configurations gagnantes et 500 perdantes
    configs_gagnantes = generer_configurations(500, gagnant=True)
    configs_perdantes = generer_configurations(500, gagnant=False)
    dataset = configs_gagnantes + configs_perdantes

    # Sauvegarde des fichiers
    sauvegarder_csv("dataset.csv", dataset)

    print("Configurations enregistrées avec succès !")

    # print("minimax")
    # print(minimax(nd, 1000))
    # print("alphabeta")
    # print(alphabeta(nd, 1000, -1000, 1000))


    
if __name__ == "__main__":
    main()
