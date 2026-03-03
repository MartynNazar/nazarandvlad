def can_move(t, dist, walls):
    t.forward(dist)
    nx, ny = t.xcor(), t.ycor()
    if abs(nx) > 435 or abs(ny) > 335:
        t.backward(dist)
        return False
    for w in walls:
        if t.distance(w) < 26:
            t.backward(dist)
            return False
    t.backward(dist)
    return True

def build_maze(walls_list, wall_func):
    for x in [-300, 0, 300]:
        for y in range(-250, 251, 40):
            walls_list.append(wall_func(x, y))
    for y in [-150, 150]:
        for x in range(-400, 401, 40):
            if abs(x) > 50:
                walls_list.append(wall_func(x, y))