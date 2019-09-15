from dolfin import *
from mesh_generation import *

dash_line = '---------------------------------------------'
pin_line = '################################################'

alpha = 3
beta = 1.2

# Define boundary condition
u_D = Expression('1 + x[0]*x[0] + alpha*x[1]*x[1] + beta*t',
                 degree=2, alpha=alpha, beta=beta, t=0)

def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, u_D, boundary)

mesh_coordinates = mesh.coordinates()
print(mesh_coordinates[0][1])
print(dash_line)
print(type(mesh_coordinates))
