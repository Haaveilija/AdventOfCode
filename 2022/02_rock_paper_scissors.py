def win_strat_A(p1, p2):
    # note: you are p2
    if p1 == p2:
        return 3 # draw
    elif (p1 - p2) % 3 == 1:
        return 0 # p1 wins
    elif (p1 - p2) % 3 == 2:
        return 6 # p2 wins
    else:
        print("wut?",(p1-p2)%3)

def convert_abc_to_nums(abc):
    # 0 = rock, 1 = paper, 2 = scissors
    relations = {
        'A' : 0,
        'B' : 1,
        'C' : 2,
        'X' : 0,
        'Y' : 1,
        'Z' : 2
    }
    if abc in relations:
        return relations[abc]
    

def rps_points_strat_A(p2):
    relations = {
        0 : 1,
        1 : 2,
        2 : 3
    }
    return relations[p2]


def points_from_strategy_A(filename):
    points = 0
    with open(filename, 'r') as file:
        for row in file:
            plays = row.rstrip().split(' ')
            # A = rock, B = paper, C = scissors
            # X = rock, Y = paper, Z = scissors
            win_points = win_strat_A(convert_abc_to_nums(plays[0]), convert_abc_to_nums(plays[1]))
            rps_points = rps_points_strat_A(convert_abc_to_nums(plays[1]))
            points += win_points + rps_points

    return points

def points_from_strategy_B(filename):
    points = 0
    with open(filename, 'r') as file:
        for row in file:
            plays = row.rstrip().split(' ')
            # A = rock, B = paper, C = scissors
            # X = lose, Y = draw, Z = win
            your_move = calculate_move(convert_abc_to_nums(plays[0]), plays[1])
            win_points = win_points_from_move(plays[1])
            rps_points = rps_points_strat_A(your_move)
            points += win_points + rps_points
    return points

def win_points_from_move(result):
    relations = {
        'X' : 0,
        'Y' : 3,
        'Z' : 6
    }
    return relations[result]

def calculate_move(p1, p2):
    relations = {
        'X' : -1,
        'Y' : 0,
        'Z' : 1
    }
    return (p1 + relations[p2]) % 3


def main():
    filename = "inputs/02_input.txt"
    points_A = points_from_strategy_A(filename)
    print(points_A)
    points_B = points_from_strategy_B(filename)
    print(points_B)


if __name__ == "__main__":
    main()