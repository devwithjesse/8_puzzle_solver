import heapq
from utils.puzzle_utils import neighbors, is_goal

# heuristics map will be imported by UI
def heuristic_misplaced(state, goal):
    return sum(1 for a,b in zip(state, goal) if a!=0 and a!=b)

def heuristic_manhattan(state, goal):
    # index positions
    def pos(index):
        return (index//3, index%3)
    goal_positions = {val: i for i,val in enumerate(goal)}
    total = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        gi = goal_positions[val]
        r1,c1 = pos(i)
        r2,c2 = pos(gi)
        total += abs(r1-r2)+abs(c1-c2)
    return total

heuristics_map = {
    'misplaced': heuristic_misplaced,
    'manhattan': heuristic_manhattan
}

def a_star(start, goal, heuristic):
    # A* returns path and moves list, or None if no solution
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {start: None}
    move_from_parent = {start: None}
    gscore = {start: 0}

    while open_set:
        f, g, current = heapq.heappop(open_set)
        if is_goal(current, goal):
            # reconstruct path
            path = []
            moves = []
            cur = current
            while cur is not None:
                path.append(cur)
                moves.append(move_from_parent[cur])
                cur = came_from[cur]
            path.reverse(); moves.reverse()
            return path, [m for m in moves[1:]]
        for ns, mv in neighbors(current):
            tentative_g = gscore[current] + 1
            if ns not in gscore or tentative_g < gscore[ns]:
                gscore[ns] = tentative_g
                came_from[ns] = current
                move_from_parent[ns] = mv
                fscore = tentative_g + heuristic(ns, goal)
                heapq.heappush(open_set, (fscore, tentative_g, ns))
    return None

def uniform_cost_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    move_from_parent = {start: None}
    gscore = {start: 0}

    while open_set:
        cost, current = heapq.heappop(open_set)

        if is_goal(current, goal):
            path, moves = [], []
            cur = current
            while cur is not None:
                path.append(cur)
                moves.append(move_from_parent[cur])
                cur = came_from[cur]
            return path[::-1], [m for m in moves[::-1][1:]]
        
        for ns, mv in neighbors(current):
            tentative_g = gscore[current] + 1
            if ns not in gscore or tentative_g < gscore[ns]:
                gscore[ns] = tentative_g
                came_from[ns] = current
                move_from_parent[ns] = mv
                heapq.heappush(open_set, (tentative_g, ns))
    return None

def greedy_best_first_search(start, goal, heuristic):
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    move_from_parent = {start: None}
    visited = set()

    while open_set:
        h, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if is_goal(current, goal):
            path, moves = [], []
            cur = current
            while cur is not None:
                path.append(cur)
                moves.append(move_from_parent[cur])
                cur = came_from[cur]
            return path[::-1], [m for m in moves[::-1][1:]]
        
        for ns, mv in neighbors(current):
            if ns not in visited:
                came_from[ns] = current
                move_from_parent[ns] = mv
                heapq.heappush(open_set, (heuristic(ns, goal), ns))

    return None

def weighted_a_star(start, goal, heuristic, weight=1.5):
    open_set = []
    heapq.heappush(open_set, (weight * heuristic(start, goal), 0, start))
    came_from = {start: None}
    move_from_parent = {start: None}
    gscore = {start: 0}

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if is_goal(current, goal):
            path, moves = [], []
            cur = current
            while cur is not None:
                path.append(cur)
                moves.append(move_from_parent[cur])
                cur = came_from[cur]
            return path[::-1], [m for m in moves[::-1][1:]]

        for ns, mv in neighbors(current):
            tentative_g = gscore[current] + 1
            if ns not in gscore or tentative_g < gscore[ns]:
                gscore[ns] = tentative_g
                came_from[ns] = current
                move_from_parent[ns] = mv
                fscore = tentative_g + weight * heuristic(ns, goal)
                heapq.heappush(open_set, (fscore, tentative_g, ns))

    return None
