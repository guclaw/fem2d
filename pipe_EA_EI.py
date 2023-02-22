import math

def hollow_circle_properties(**kwargs):
    d1 = kwargs.get("d1", 0.4)
    th = kwargs.get("th", 0.01)
    E = kwargs.get("E", 210e9)

    gamma = kwargs.get("gamma", 10000)
    sw = kwargs.get("sw", False)
    d_int = d1 - 2*th
    A = math.pi * ((0.5*d1)**2 - (0.5*d_int)**2)
    I=(math.pi/4)*((d1/2)**4-(d_int/2)**4)
    EA = E * A
    EI = E * I
    if sw:
        g = A * gamma
    else:
        g = 0
    section_name = f"RO {d1*1000}x{th*1000}"
    return section_name, EA, EI, g


