def generate_animation(sequence):
    positions = [(0,0,0)]
    frames = [positions.copy()]

    moves = [(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]

    for i in range(1, len(sequence)):
        x,y,z = positions[-1]
        dx,dy,dz = moves[i % len(moves)]

        new_pos = (x+dx, y+dy, z+dz)
        positions.append(new_pos)

        frames.append(positions.copy())

    return frames