import random

MOVES = [
    (1,0,0), (-1,0,0),
    (0,1,0), (0,-1,0),
    (0,0,1), (0,0,-1)
]

def generate_fold(sequence, max_attempts=100):
    for _ in range(max_attempts):
        positions = [(0,0,0)]
        occupied = set(positions)

        valid = True

        for _ in sequence[1:]:
            x,y,z = positions[-1]
            random.shuffle(MOVES)

            placed = False
            for dx,dy,dz in MOVES:
                new_pos = (x+dx, y+dy, z+dz)

                if new_pos not in occupied:
                    positions.append(new_pos)
                    occupied.add(new_pos)
                    placed = True
                    break

            if not placed:
                valid = False
                break

        if valid:
            return positions

    return [(i,0,0) for i in range(len(sequence))]