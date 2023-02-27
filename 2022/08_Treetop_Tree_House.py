def load_grid(filename):
    grid = []
    with open(filename, 'r') as f:
        for row in f:
            grid.append(row.strip())
    return grid


def count_visible_trees(grid):
    visible_trees = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if is_visible(x, y, grid):
                visible_trees += 1
    return visible_trees


def is_visible_north(x, y, grid):
    height = grid[x][y]
    for i in range(x):
        if grid[i][y] >= height:
            return False
    return True


def is_visible_south(x, y, grid):
    height = grid[x][y]
    for i in range(x+1, len(grid)):
        if grid[i][y] >= height:
            return False
    return True

def is_visible_east(x, y, grid):
    height = grid[x][y]
    for j in range(y):
        if grid[x][j] >= height:
            return False
    return True


def is_visible_west(x, y, grid):
    height = grid[x][y]
    for j in range(y+1, len(grid[0])):
        if grid[x][j] >= height:
            return False
    return True


def is_visible(x, y, grid):
    visible = [is_visible_north(x, y, grid), is_visible_south(x, y, grid), is_visible_east(x, y, grid), is_visible_west(x, y, grid)]
    return sum([int(i) for i in visible]) > 0



def visibility_grid(grid):
    trees = []
    for x in range(len(grid)):
        row = []
        for y in range(len(grid[0])):
            row.append(int(is_visible(x, y, grid)))
        trees.append(row)

    return trees


def print_grid(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            print(f"{grid[x][y]:3}", end="")
        print("")


def scenic_score_north(x, y, grid):
    height = grid[x][y]
    score = 0
    i = x-1
    while i >= 0:
        score += 1
        if grid[i][y] >= height:
            break
        i -= 1
    return score


def scenic_score_south(x, y, grid):
    height = grid[x][y]
    score = 0
    i = x+1
    while i <= len(grid)-1:
        score += 1
        if grid[i][y] >= height:
            break
        i += 1
    return score


def scenic_score_east(x, y, grid):
    height = grid[x][y]
    score = 0
    j = y+1
    while j < len(grid[x]):
        score += 1
        if grid[x][j] >= height:
            break
        j += 1
    return score


def scenic_score_west(x, y, grid):
    height = grid[x][y]
    score = 0
    j = y-1
    while j >= 0:
        score += 1
        if grid[x][j] >= height:
            break
        j -= 1
    return score

def scenic_score(x, y, grid):
    return scenic_score_north(x, y, grid) * scenic_score_south(x, y, grid) * scenic_score_east(x, y, grid) * scenic_score_west(x, y, grid)


def best_scenic_score(grid):
    best_score = 0
    best_coords = [None, None]
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            score = scenic_score(x, y, grid)
            if score > best_score:
                best_score = score
                best_coords = [x, y]
    return best_score, best_coords


def score_grid(grid, score_func=scenic_score):
    scores = []
    for x in range(len(grid)):
        row = []
        for y in range(len(grid[x])):
            row.append(score_func(x, y, grid))
        scores.append(row)
    return scores


def main():
    grid = load_grid('inputs/08_input.txt')
    #grid = load_grid('inputs/08_example.txt')
    print(count_visible_trees(grid), "trees are visible from outside the forest")
    best_score, best_spot = best_scenic_score(grid)
    print(f"The best score is {best_score} at the point ({best_spot[0]}, {best_spot[1]})")

if __name__ == "__main__":
    main()