import numpy as np

def find_closest_element(input_list, mouse_position):
    closest_element = min(input_list, key=lambda element: min(np.linalg.norm(np.array(point) - np.array(mouse_position)) 
                            for point in element[0]))
    return closest_element

# Your input list with inhomogeneous structure
input_list = [
    [[[222, 8], [600, 8], [600, 34], [222, 34]], 'Neither CUDA nor MPS are available'],
    [[256, 54], [581, 54], [581, 84], [256, 84], 'GNarrator is now running  You'],
    [[153, 131], [175, 131], [175, 151], [153, 151], 'M'],
    [[0, 472], [350, 472], [350, 498], [0, 498], ') 0 8> Git Graph GIST [Create Profile]']
]

mouse_position = np.array((1000, 1000))

closest_element = find_closest_element(input_list, mouse_position)
print(closest_element)
