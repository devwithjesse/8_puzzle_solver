from collections import deque
from utils.puzzle_utils import neighbors, is_goal

def bfs(start, goal):
    # start, goal: tuples of length 9
    if start == goal:
        return [start], []

    frontier = deque([start])
    parent = {start: None}
    move_from_parent = {start: None}

    while frontier:
        state = frontier.popleft()
        if is_goal(state, goal):
            # reconstruct path
            path = []
            moves = []
            cur = state
            while cur is not None:
                path.append(cur)
                moves.append(move_from_parent[cur])
                cur = parent[cur]
            path.reverse()
            moves.reverse()
            # first move is None (start) - chop it for moves list
            return path, [m for m in moves[1:]]
        for ns, mv in neighbors(state):
            if ns not in parent:
                parent[ns] = state
                move_from_parent[ns] = mv
                frontier.append(ns)
    return None

def dfs(start, goal, max_depth=1000):
    stack = [(start, 0)]
    parent = {start : None}
    move_from_parent = {start : None}

    while stack:
        state, depth = stack.pop()
        if is_goal(state, goal):
            path, moves = [], []
            cur = state

            while cur is not None:
                path.append(cur)
                moves.append(move_from_parent[cur])
                cur = parent[cur]
            return path[::-1], [m for m in moves[::-1][1:]]
        
        if depth < max_depth:
            for ns, mv in neighbors(state):
                if ns not in parent:
                    parent[ns] = state
                    move_from_parent[ns] = mv
                    stack.append((ns, depth + 1))
    return None


def dls(start, goal, limit):
    def recursive_dls(state, goal, limit, parent, move_from_parent):
        if is_goal(state, goal):
            return [state], [move_from_parent[state]]
        elif limit == 0:
            return "cutoff"
        else:
            cutoff_occured = False
            for ns, mv in neighbors(state):
                if ns not in parent:
                    parent[ns] = state
                    move_from_parent[ns] = mv
                    result = recursive_dls(ns, goal, limit - 1, parent, move_from_parent)
                    if result == "cutoff":
                        cutoff_occured = True
                    elif result is not None:
                        path, moves = result
                        path.insert(0, state)
                        moves.insert(0, mv)
                        return path, moves
            return "cutoff" if cutoff_occured else None
        
    parent = {start : None}
    move_from_parent = {start : None}
    result = recursive_dls(start, goal, limit, parent, move_from_parent)

    if isinstance(result, tuple):
        path, moves = result
        return path, [m for m in moves[1:]] if len(moves) > 1 else []
    
    return None

def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        result = dls(start, goal, depth)
        if result is not None:
            return result
    return None

def bidirectional_search(start, goal):
    if start == goal:
        return [start], []

    frontier_start = deque([start])
    frontier_goal = deque([goal])

    parent_start = {start: None}
    parent_goal = {goal: None}
    
    move_from_start = {start: None}
    move_from_goal = {goal: None}

    while frontier_start and frontier_goal:
        # Expand forward frontier
        state_fwd = frontier_start.popleft()
        for ns, mv in neighbors(state_fwd):
            if ns not in parent_start:
                parent_start[ns] = state_fwd
                move_from_start[ns] = mv
                frontier_start.append(ns)
                if ns in parent_goal:
                    # Meeting point found
                    return reconstruct_bidirectional_path(ns, parent_start, parent_goal, move_from_start, move_from_goal)

        # Expand backward frontier
        state_bwd = frontier_goal.popleft()
        for ns, mv in neighbors(state_bwd):
            if ns not in parent_goal:
                parent_goal[ns] = state_bwd
                move_from_goal[ns] = mv
                frontier_goal.append(ns)
                if ns in parent_start:
                    return reconstruct_bidirectional_path(ns, parent_start, parent_goal, move_from_start, move_from_goal)

    return None


def reconstruct_bidirectional_path(meeting_state, parent_start, parent_goal, move_from_start, move_from_goal):
    # Reconstruct forward path
    path_start, moves_start = [], []
    cur = meeting_state
    while cur is not None:
        path_start.append(cur)
        moves_start.append(move_from_start[cur])
        cur = parent_start[cur]
    path_start.reverse()
    moves_start.reverse()

    # Reconstruct backward path
    path_goal, moves_goal = [], []
    cur = meeting_state
    while cur is not None:
        path_goal.append(cur)
        moves_goal.append(move_from_goal[cur])
        cur = parent_goal[cur]

    # Combine both halves (excluding duplicate meeting point)
    full_path = path_start + path_goal[1:]
    full_moves = [m for m in moves_start[1:] + moves_goal[:-1] if m]

    return full_path, full_moves
