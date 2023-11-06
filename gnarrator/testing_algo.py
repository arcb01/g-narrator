import numpy as np

def find_closest_element(input_list, mouse_position):
    closest_element = None
    closest_distance = float('inf')

    for element in input_list:
        points = element[0]
        label = element[1]

        for point in points:
            distance = np.linalg.norm(np.array(point) - np.array(mouse_position))

            if distance < closest_distance:
                closest_distance = distance
                closest_element = element

    return closest_element

# Your input list with inhomogeneous structure
input_list = [
    [[[222, 8], [600, 8], [600, 34], [222, 34]], 'Neither CUDA nor MPS are available'],
    [[256, 54], [581, 54], [581, 84], [256, 84], 'GNarrator is now running  You'],
    [[153, 131], [175, 131], [175, 151], [153, 151], 'M'],
    [[0, 472], [350, 472], [350, 498], [0, 498], ') 0 8> Git Graph GIST [Create Profile]']
]

mouse_position = (1000, 1000)

closest_element = find_closest_element(input_list, mouse_position)
print(closest_element)
