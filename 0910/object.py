import random as rd


def distance(player, treasure):
    return abs(player[0] - treasure[0]) + abs(player[1] - treasure[1])


def visualize(grid_size, position):
    ls = [['*' for _ in range(grid_size)] for _ in range(grid_size)]
    ls[position[0]][position[1]] = 'P'
    for row in ls:
        print(*row)


def move(direction, player):
    if direction == "N":
        if player[0] > 0:
            player[0] -= 1
        else:
            print("Illegal move! Can't move further North.")
    elif direction == "S":
        if player[0] < grid_size - 1:
            player[0] += 1
        else:
            print("Illegal move! Can't move further South.")
    elif direction == "E":
        if player[1] < grid_size - 1:
            player[1] += 1
        else:
            print("Illegal move! Can't move further East.")
    elif direction == "W":
        if player[1] > 0:
            player[1] -= 1
        else:
            print("Illegal move! Can't move further West.")
    else:
        print("Invalid direction! Use N, S, E, W only.")


if __name__ == '__main__':
    grid_size = 5
    player_pos = [rd.randint(0, grid_size - 1), rd.randint(0, grid_size - 1)]
    treasure_pos = [rd.randint(0, grid_size - 1), rd.randint(0, grid_size - 1)]

    initial_distance = distance(player_pos, treasure_pos)
    print(f"Starting position of the player: {player_pos}")
    visualize(grid_size, player_pos)
    print(f"Initial distance to the treasure: {initial_distance}\n")

    max_moves = 10
    moves_made = 0

    while True:
        direction = input("Enter move (N, S, E, W): ").upper()

        move(direction, player_pos)
        visualize(grid_size, player_pos)

        new_distance = distance(player_pos, treasure_pos)
        moves_made += 1

        if player_pos == treasure_pos:
            print(f"Congratulations! You found the treasure at {treasure_pos} in {moves_made} moves!")
            break
        elif new_distance < initial_distance:
            print(f"You're getting closer! Distance to treasure: {new_distance}\n")
        else:
            print(f"You're moving farther! Distance to treasure: {new_distance}\n")

        initial_distance = new_distance

        # If the player has used all moves
        if moves_made == max_moves:
            print(f"No more moves left. You lost! The treasure was at {treasure_pos}.")
            break
