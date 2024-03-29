from dolfin import *
import numpy as np

dash_line = '---------------------------------------------'
pin_line = '################################################'

alpha = 3
beta = 1.2
T = 2.0            # final time
num_steps = 10     # number of time steps
dt = T / num_steps # time step size


################################################
# Create mesh and define function space
nx = ny = 8
mesh = UnitSquareMesh(nx, ny)
V = FunctionSpace(mesh, 'P', 1)

mesh_plate = File('mesh.pvd')
mesh_plate << mesh

################################################

################################################
# Define boundary condition
u_D = Expression('1 + x[0]*x[0] + alpha*x[1]*x[1] + beta*t',
                 degree=2, alpha=alpha, beta=beta, t=0)

def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, u_D, boundary)
################################################

################################################
# Define initial value
u_n = interpolate(u_D, V)
# or
# u_n = project(u_D, V)
################################################

################################################
# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(beta - 2 - 2*alpha)
# class dolfin.functions.constant.Constant(value, cell=None, name=None)
# Create constant-valued function with given value.


F = u*v*dx + dt*dot(grad(u), grad(v))*dx - (u_n + dt*f)*v*dx
a, L = lhs(F), rhs(F)
# This way of formulation is more convenient for more
# complicated problems
################################################




# Time-stepping
u = Function(V)
t = 0
for n in range(num_steps):

    # Update current time
    t += dt
    u_D.t = t

    # Compute solution
    solve(a == L, u, bc)

    # Plot solution
    plot(u)

    # Compute error at vertices
    u_e = interpolate(u_D, V)
    error = np.abs(u_e.vector().array() - u.vector().array()).max()
    print('t = %.2f: error = %.3g' % (t, error))

    solv = u.vector()
    print(solv.array())

    solv = u_e.vector()
    print(solv.array())

    # Update previous solution
    u_n.assign(u)

# Hold plot
interactive()

vtkfile = File('solution.pvd')
vtkfile << (u, t)
