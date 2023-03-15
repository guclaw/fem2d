from anastruct import SystemElements
import pickle
import numpy as np
from anastruct.sectionbase import section_base
import matplotlib.pyplot as plt
from anastruct.material.profile import HEA
from anastruct.material.units import to_kNm2, to_kN


class Multispan_Beam():
    def __init__(self, profile: str = 'HE 200 B', uniformly_distribiuted_load: float = -50, E: float = 210e6,
                 span_number: int = 2,
                 span_length: float = 6,
                 canteliver_length: float = 2, canteliver: bool = True):
        self.system = SystemElements(figsize=(15, 5))
        self.uniformly_distribiuted_load = uniformly_distribiuted_load
        self.canteliver = canteliver
        self.canteliver_length = canteliver_length
        self.span_length = span_length
        self.profile = section_base.get_section_parameters(profile)
        self.E = E
        self.span_number = span_number
        self.EA = self.E * self.profile["Ax"]
        self.EI = self.E * self.profile["Iy"]
        self.mass = self.profile['mass']

    def geometry(self):
        # Add beams to the system.
        if self.canteliver:
            self.system.add_element([[0, 0], [self.canteliver_length, 0]], EA=self.EA, EI=self.EI)
            self.system.add_multiple_elements(
                [[self.canteliver_length, 0], [self.span_number * self.span_length + self.canteliver_length, 0]],
                self.span_number, EA=self.EA, EI=self.EI)
            self.system.add_element([[self.span_number * self.span_length + self.canteliver_length, 0],
                                     [self.span_number * self.span_length + 2 * self.canteliver_length, 0]], EA=self.EA,
                                    EI=self.EI)
            self.system.add_support_hinged(node_id=(range(1, self.span_number + 4)))
            # self.system.add_support_roll(node_id=5)

    def load(self):
        # self.system.q_load(q=self.uniformly_distribiuted_load, element_id=(1, 2))
        for el in self.system.element_map.values():
        # apply live load on elements that are horizontal
            if np.isclose(np.sin(el.angle), 0):
                self.system.q_load(
                    q=self.uniformly_distribiuted_load,
                    element_id=el.id,
                    direction='y'
                )

    def show_structure(self):
        self.system.show_structure()

    def solve(self):
        self.system.solve()
        self.system.show_results()
        # Solve
        # self.system.solve()
        # self.system.solve(geometrical_non_linear=False, discretize_kwargs=dict(n=20), max_iter=1000)

        # [ss.q_load(q=q, element_id=_) for _ in range(1, n + 3)]
        # for el in self.system.element_map.values():
        #     # apply live load on elements that are horizontal
        #     if np.isclose(np.sin(el.angle), 0):
        #         self.system.q_load(
        #             q=self.uniformly_distribiuted_load,
        #             element_id=el.id,
        #             direction='y'
        #         )

        # # Get visual results.

        # ss.add_support_hinged(node_id=1)
        # [ss.add_support_hinged(node_id=_) for _ in range(2, 4)]
        #
        # [ss.add_support_hinged(node_id=_) for _ in range(4, 7)]
        #
        # # ss.add_support_spring(node_id=2, k=k, translation=2)
        #
        # # Add loads.
        #
        # # [ss.q_load(q=q, element_id=_) for _ in range(1, n + 3)]
        # ss.q_load(q=q, element_id=1)
        # for el in ss.element_map.values():
        #     # apply live load on elements that are horizontal
        #     if np.isclose(np.sin(el.angle), 0):
        #         ss.q_load(
        #             q=q,
        #             element_id=el.id,
        #             direction='y'
        #         )
        #
        # # Solve
        # ss.solve(geometrical_non_linear=True)
        # # ss.solve(geometrical_non_linear=False, discretize_kwargs=dict(n=20), max_iter=1000)
        #
        # # Get visual results.
        # ss.show_structure(verbosity=0)
        # # ss.show_reaction_force()
        # # ss.show_axial_force()
        # # ss.show_shear_force()
        # ss.show_bending_moment()
        # ss.show_displacement()
        # deflecion = []
        # [deflecion.append(_ * 1000) for _ in ss.element_map[1].deflection]
        # # print(ss.show_displacement(values_only=True))
        # print(deflecion)
        # print(ss.element_map[1].max_deflection * 1000)


m = Multispan_Beam(profile='HE 400 B', E=200000000000000)
print(m.canteliver)
m.geometry()
m.load()
# m.show_structure()
m.solve()
