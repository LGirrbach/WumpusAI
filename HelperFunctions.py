def symbol(symb, *indices):
    assert isinstance(symb, str)
    for index in indices:
        symb += str(index)
    return symb

def neighbour_symbols(symb, coords_neighbours):
    return [symb + str(x_neighbour) + str(y_neighbour) for x_neighbour, y_neighbour in coords_neighbours]


def direction_transformation_plan(direction1, direction2):
    directions = ['N', 'W', 'S', 'E']
    if any(direction not in directions for direction in (direction1, direction2)):
        raise TypeError
    if direction1 == direction2:
        return []
    transformation_process = [direction1, direction2]
    if abs(directions.index(direction1)-directions.index(direction2)) == 2:
        index_direction1 = directions.index(direction1)
        transformation_process.insert(1, directions[(index_direction1+1)%len(directions)])
    direction_transformation_agenda = []
    for number_direction, direction in enumerate(transformation_process[:-1]):
        index_direction = directions.index(direction)
        if transformation_process[number_direction+1] == directions[(index_direction+1)%4]:
            direction_transformation_agenda.append('turnleft')
        else:
            direction_transformation_agenda.append('turnright')
    return direction_transformation_agenda

def distance(coords_field1, coords_field2):
    return abs(coords_field1[0]-coords_field2[0]) + abs(coords_field1[1]-coords_field2[1])
