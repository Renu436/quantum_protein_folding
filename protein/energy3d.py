def compute_energy(sequence, positions):
    energy = 0
    pos_map = {pos:i for i,pos in enumerate(positions)}

    for i,(x,y,z) in enumerate(positions):
        if sequence[i] != 'H':
            continue

        neighbors = [
            (x+1,y,z),(x-1,y,z),
            (x,y+1,z),(x,y-1,z),
            (x,y,z+1),(x,y,z-1)
        ]

        for n in neighbors:
            if n in pos_map:
                j = pos_map[n]

                if abs(i-j) > 1 and sequence[j] == 'H':
                    energy -= 1

    return energy // 2