# Separate heuristics module (optional)
def misplaced(state, goal):
    return sum(1 for a,b in zip(state, goal) if a!=0 and a!=b)

def manhattan(state, goal):
    def pos(idx): return (idx//3, idx%3)
    goal_pos = {val:i for i,val in enumerate(goal)}
    total = 0
    for i,val in enumerate(state):
        if val==0: continue
        gi = goal_pos[val]
        r1,c1 = pos(i); r2,c2 = pos(gi)
        total += abs(r1-r2) + abs(c1-c2)
    return total
