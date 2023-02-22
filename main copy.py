from anastruct import SystemElements
import pickle
import numpy as np


# Data
l0 = 2  # m
l = 6 # m
number_of_pipes = 2
n = number_of_pipes + 1

q = -41
l_pipe = 6

steelsection="HE 220 B"


ss = SystemElements(figsize=(15, 5))

# Add beams to the system.
ss.add_element(location=[[0, 0], [l0, 0]], steelsection=steelsection)
if n == 1:
    ss.add_element(location=[[l0, 0], [l0+l, 0]], steelsection=steelsection)
else:
    ss.add_multiple_elements([[l0, 0], [l0 + l * n, 0]], n, steelsection=steelsection)
ss.add_element(location=[[l0 + (n * l), 0], [2 * l0 + (n * l), 0]], steelsection=steelsection)

# Add a fixed support at start and end
ss.add_support_hinged(node_id=1)
ss.add_support_hinged(node_id=n + 3)

# Add loads.
# [ss.q_load(q=q, element_id=_) for _ in range(1, n + 3)]
for el in ss.element_map.values():
    # apply live load on elements that are horizontal
    if np.isclose(np.sin(el.angle), 0):
        ss.q_load(
            q=q,
            element_id=el.id,
            direction='y'
        )





# skew elements
ss.add_element(location=[[l0, 0], [0, -l0]], steelsection=steelsection, spring={1: 0})
ss.add_support_hinged(node_id=4 + n)

ss.add_element(location=[[n * l + l0, 0], [n * l + 2 * l0, -l0]], steelsection=steelsection, spring={1: 0})
ss.add_support_hinged(node_id=n + 5)

# vertical elements
for _ in range(1, n):
    print(_)
    ss.add_element(location=[[l0 + l * _, 0], [l0 + l * _, -l_pipe]], d1=0.3556, th=0.008, spring={1: 0})
    ss.add_support_hinged(node_id=number_of_pipes+6+_)

# Solve
# ss.solve()
ss.solve(geometrical_non_linear=False, discretize_kwargs=dict(n=20), max_iter=1000)

# Get visual results.
# ss.show_structure()
# ss.show_reaction_force()
# ss.show_axial_force()
# ss.show_shear_force()
# ss.show_bending_moment()
ss.show_displacement()
# for x in range(1, 10):
#     print(f'section: {ss.element_map[x].section_name}')
#     print(f'EA: {ss.element_map[x].EA}')

# # save
# with open('my_structure.pkl', 'wb') as f:
#     pickle.dump(ss, f)


max = [ss.element_map[4].deflection]
print(max)

