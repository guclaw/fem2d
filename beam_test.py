from anastruct import SystemElements
import pickle
import numpy as np
from anastruct.sectionbase import section_base
param = section_base.get_section_parameters("HE 450 B")
import matplotlib.pyplot as plt

# Data

E = 205*10**6

l = 6 # m
q = -100

EI = param['Iy'] * E


ss = SystemElements(figsize=(15, 5))

# Add beams to the system.
ss.add_element(location=[[0, 0], [l, 0]], EI=EI)
print(ss.element_map[1].EI)

# Add a fixed support at start and end
ss.add_support_hinged(node_id=1)
ss.add_support_roll(node_id=2)

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


# Solve
ss.solve()
# ss.solve(geometrical_non_linear=False, discretize_kwargs=dict(n=20), max_iter=1000)

# Get visual results.
# ss.show_structure()
# ss.show_reaction_force()
# ss.show_axial_force()
# ss.show_shear_force()
# ss.show_bending_moment()
# ss.show_displacement(factor=100)
deflecion = []
[deflecion.append(_ * 1000) for _ in ss.element_map[1].deflection]
# print(ss.show_displacement(values_only=True))
print(deflecion)
print(ss.element_map[1].max_deflection*1000)


