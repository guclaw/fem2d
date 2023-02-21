from anastruct import SystemElements

# Data
l0 = 2  # m
l = 4  # m
number_of_pipes = 2
n = number_of_pipes + 1

q = -50
l_pipe = 6

hinge_offset = -3

steelprofile = 'IPE 300'

ss = SystemElements(figsize=(15, 5))

# Add beams to the system.
ss.add_element(location=[[0, 0], [l0, 0]])
if n == 1:
    ss.add_element(location=[[l0, 0], [l0+l, 0]])
else:
    ss.add_multiple_elements([[l0, 0], [l0 + l * n, 0]], n)
ss.add_element(location=[[l0 + (n * l), 0], [2 * l0 + (n * l), 0]])

# Add a fixed support at start and end
ss.add_support_hinged(node_id=1)
ss.add_support_hinged(node_id=n + 3)

# Add loads.
[ss.q_load(q=q, element_id=_) for _ in range(1, n + 3)]

# skew elements
ss.add_truss_element(location=[[l0, 0], [0, -l0]])
ss.add_support_hinged(node_id=4 + n)

ss.add_truss_element(location=[[n * l + l0, 0], [n * l + 2 * l0, -l0]])
ss.add_support_hinged(node_id=n + 5)

# vertical elements
for _ in range(1, n):
    print(_)
    ss.add_truss_element(location=[[l0 + l * _, 0], [l0 + l * _, -l_pipe]])
    ss.add_support_hinged(node_id=number_of_pipes+6+_)

# Solve
ss.solve()

# Get visual results.
ss.show_structure()
# ss.show_reaction_force()
ss.show_axial_force()
# ss.show_shear_force()
ss.show_bending_moment()
ss.show_displacement()
