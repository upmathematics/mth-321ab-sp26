import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

# Physical parameters
m = 1       # mass (kg)
k = 4       # spring constant (N/m)
c = 0       # damping coefficient (Ns/m)

# Initial conditions: x1 = position, x2 = velocity
x0 = [1.0, 0.0]  # initial displacement and velocity

# Time span
dt = 0.05
t_span = (0, 20)
t_eval = np.linspace(*t_span, int(t_span[1]/dt))

# First-order system
def spring_mass_damped(t, x):
    x1, x2 = x
    dx1dt = x2
    dx2dt = -(k/m)*x1 - (c/m)*x2
    return [dx1dt, dx2dt]

# Solve ODE
sol = solve_ivp(spring_mass_damped, t_span, x0, t_eval=t_eval)

# Extract position
positions = sol.y[0]

# Animation setup
fig, ax = plt.subplots(figsize=(9, 1.5))
ax.set_xlim(-1.51, 1.51)
ax.set_ylim(-0.01, 0.51)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.axis('off')
fig.patch.set_facecolor("#FFFFFF")
#fig.patch.set_alpha(0)
fig.tight_layout(pad=0, w_pad=0, h_pad=0)

# Wall and floor
ax.plot([-1.5, -1.5], [0, 1], color='black', linewidth=4)
floor_y = 0
ax.plot([-1.5, 1.5], [floor_y, floor_y], color='black', linewidth=4)

# Mass block
mass_width = 0.5
mass_height = 0.5
mass = Rectangle((0, floor_y), mass_width, mass_height, fc='#058743')
ax.add_patch(mass)

# Spring line
spring_line, = ax.plot([], [], color='#71706E', lw=3)

def draw_spring(x0, x1, coils=20, amplitude=0.05):
    x = np.linspace(x0, x1, coils * 20)
    y = amplitude * np.sin(np.linspace(0, coils * np.pi, coils * 20)) + floor_y + mass_height / 2
    return x, y

def init():
    spring_line.set_data([], [])
    mass.set_xy((positions[0] - mass_width/2, floor_y))
    return spring_line, mass

def update(frame):      
    x = positions[frame]
    spring_x, spring_y = draw_spring(-1.5, x-(mass_width/2))
    spring_line.set_data(spring_x, spring_y)
    mass.set_xy((x - mass_width/2, floor_y))
    return spring_line, mass

ani = FuncAnimation(fig, update, frames=len(positions), init_func=init, blit=True)

# Save as GIF
ani.save('horizontal-spring-mass/'+'hsm-undamped-c0-k4.gif', writer=PillowWriter(fps=30), dpi=150)