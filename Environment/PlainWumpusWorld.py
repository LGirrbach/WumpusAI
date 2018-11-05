from itertools import compress


class PlainWumpusWorld:

    EXIT_POSITION = (0, 0)

    def __init__(self, n=4):
        self.__N = n

        self._fields = tuple([(x, y) for y in range(n) for x in range(n)])
        self._fields_without_start = tuple([(x, y) for y in range(n) for x in range(n)
                                            if (x, y) != self.EXIT_POSITION])

        self.actions = ("forward", "turnright", "turnleft", "grab", "shoot", "climb")
        self.direction_list = ('N', 'E', 'S', 'W')

        self._direction_forward_transformations = {
            'N': lambda x, y: (x-1, y),
            'S': lambda x, y: (x+1, y),
            'E': lambda x, y: (x, y+1),
            'W': lambda x, y: (x, y-1)
        }

    def forward_field(self, coordinates_field, direction):
        x_field, y_field = coordinates_field
        x_next, y_next = self._direction_forward_transformations[direction](x_field, y_field)
        if x_next >= self.__N or y_next >= self.__N:
            return coordinates_field
        elif x_next < 0 or y_next < 0:
            return coordinates_field
        else:
            return x_next, y_next

    def neighbours(self, coordinates_field):
        x_field, y_field = coordinates_field
        nbs = list(compress(
            [(x_field - 1, y_field), (x_field + 1, y_field), (x_field, y_field - 1),
             (x_field, y_field + 1)],
            [x_field > 0, x_field < self.__N - 1, y_field > 0, y_field < self.__N - 1]
        ))
        """"
        Equivalent:
        nbs = []
        if x_field > 0:
            nbs.append((x_field - 1, y_field))
        if x_field < self.N - 1:
            nbs.append((x_field + 1, y_field))
        if y_field > 0:
            nbs.append((x_field, y_field - 1))
        if y_field < self.N - 1:
            nbs.append((x_field, y_field + 1))
        """
        return nbs

    def get_fields_without_start(self):
        return self._fields_without_start[:]

    def get_fields(self):
        return self._fields[:]

    def get_n(self):
        return self.__N

    def get_direction_forward_transformations(self):
        return self._direction_forward_transformations

    directionForwardTransformations = property(get_direction_forward_transformations)
    fieldsWithoutStart =  property(get_fields_without_start)
    allFields = property(get_fields)
    N = property(get_n)




