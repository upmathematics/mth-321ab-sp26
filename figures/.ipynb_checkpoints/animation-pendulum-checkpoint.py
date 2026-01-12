import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

# Parameters
g = 9.81      # gravity (m/s^2)
L = 1.90       # length of pendulum (m)
m = 1       # mass (kg)
c = 1       # damping coefficient (kg*m^2/s)

# Initial conditions: theta (rad), omega (rad/s)
theta0 = -np.pi / 6
omega0 = 0.0
y0 = [theta0, omega0]

# Time span
dt = 0.055
t_span = (0, 20)
t_eval = np.linspace(*t_span, int(t_span[1]/dt))

# First-order system
def damped_pendulum(t, y):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = - (g / L) * np.sin(theta) - (c / (m * L**2)) * omega
    return [dtheta_dt, domega_dt]

# Solve ODE
sol = solve_ivp(damped_pendulum, t_span, y0, t_eval=t_eval)
theta_vals = sol.y[0]

# Convert to Cartesian coordinates
x_vals = L * np.sin(theta_vals)
y_vals = -L * np.cos(theta_vals)

# Animation setup
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-2.05, 0.05)
ax.set_aspect('equal')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.axis('off')
fig.patch.set_facecolor("#FFFFFF")
#fig.patch.set_alpha(0)
fig.tight_layout(pad=0, w_pad=0, h_pad=0)

# Pendulum components
pivot = [0, 0]
rod_line, = ax.plot([], [], lw=4, color='#71706E')
bob, = ax.plot([], [], 'o', markersize=38, color='#058743')

ceiling_y = 0
ax.plot([-0.5, 0.5], [ceiling_y, ceiling_y], color='black', linewidth=4)

def init():
    rod_line.set_data([], [])
    bob.set_data([], [])
    return rod_line, bob

def update(frame):
    x = x_vals[frame]
    y = y_vals[frame]
    rod_line.set_data([pivot[0], x], [pivot[1], y])
    bob.set_data(x, y)
    return rod_line, bob

ani = FuncAnimation(fig, update, frames=len(x_vals), init_func=init, blit=True)

# Save as GIF
ani.save('pendulum.gif', writer=PillowWriter(fps=30), dpi=150)