import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

# Constants
g = 9.81            # gravity (m/s^2)
v_x = 1           # horizontal velocity (m/s)
restitution = 0.9   # bounce damping factor
dt = 0.06           # time step for animation
total_time = 20     # total simulation time

# Initial conditions: [y, v_y]
y0 = 5.0
vy0 = 0.0
state = [y0, vy0]
t = 0.0

# ODE function for vertical motion
def vertical_ode(t, y):
    return [y[1], -g]

# Set up plot
fig, ax = plt.subplots(figsize=(9, 3))
ball, = plt.plot([], [], 'o', markersize=32, color='#058743')
ax.set_xlim(-0.4, v_x * total_time + 0.6)
ax.set_ylim(-0.6, y0 + 0.6)
#ax.set_aspect('equal')
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.axis('off')
fig.patch.set_facecolor("#FFFFFF")
#fig.patch.set_alpha(0)
fig.tight_layout(pad=0, w_pad=0, h_pad=0)

# floor
floor_y = -0.6
ax.plot([-0.4, v_x * total_time + 0.6], [floor_y, floor_y], color='black', linewidth=9)

# Animation update function
positions = []

def update(frame):
    global state, t
    # Integrate vertical motion
    sol = solve_ivp(vertical_ode, [0, dt], state, t_eval=[dt])
    y, vy = sol.y[:, -1]

    # Bounce condition
    if y <= 0 and vy < 0:
        vy = -vy * restitution
        y = 0

    state = [y, vy]
    t += dt

    # Update horizontal position
    x = v_x * t
    ball.set_data(x, y)
    return ball,

# Run animation
ani = FuncAnimation(fig, update, frames=int(total_time / dt), interval=dt*1000, blit=True)

ani.save('bouncing-ball.gif', writer=PillowWriter(fps=30), dpi=150)