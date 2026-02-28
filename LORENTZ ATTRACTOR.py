import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patheffects as pe
from mpl_toolkits.mplot3d import Axes3D

# ───────────────── LORENZ SYSTEM ─────────────────
sigma, rho, beta = 10, 28, 8/3
dt = 0.005

def lorenz_step(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dx*dt, y + dy*dt, z + dz*dt

# ───────────────── MULTIPLE STARTS ─────────────────
N_STEPS = 8000

STARTS = [
    (0.1, 0.0, 0.0),
    (0.1, 0.01, 0.0),
    (-0.1, 0.0, 0.0),
    (0.0, 0.1, 0.0),
    (0.0, -0.1, 0.0),
]

COLORS = ['#00f5ff', '#ff00ff', '#ff6b9d', '#ffd93d', '#4ecdc4']

trails = []
for sx, sy, sz in STARTS:
    xs, ys, zs = [sx], [sy], [sz]
    x, y, z = sx, sy, sz
    for _ in range(N_STEPS):
        x, y, z = lorenz_step(x, y, z)
        xs.append(x); ys.append(y); zs.append(z)
    trails.append((np.array(xs), np.array(ys), np.array(zs)))

# ───────────────── FIGURE ─────────────────
plt.style.use('dark_background')
fig = plt.figure(figsize=(12,9), facecolor='#000005')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#000005')

ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.set_xlim(-25,25)
ax.set_ylim(-35,35)
ax.set_zlim(0,55)

# ───────────────── TITLE ─────────────────
fig.text(
    0.5,0.95,
    "🦋 LORENZ ATTRACTOR · CHAOS THEORY",
    ha='center',
    fontsize=16,
    color='#00f5ff',
    fontfamily='monospace',
    path_effects=[pe.withStroke(linewidth=6,
    foreground='#001122')]
)

# ───────────────── GLOW LINES ─────────────────
lines=[]
dots=[]

for color in COLORS:

    glow1, = ax.plot([],[],[],
                     color=color,
                     linewidth=6,
                     alpha=0.05)

    glow2, = ax.plot([],[],[],
                     color=color,
                     linewidth=3,
                     alpha=0.15)

    line, = ax.plot([],[],[],
                    color=color,
                    linewidth=1.2,
                    alpha=0.9)

    dot, = ax.plot([],[],[],
                   'o',
                   color=color,
                   markersize=6,
                   markeredgecolor='white',
                   markeredgewidth=0.3)

    lines.append((glow1,glow2,line))
    dots.append(dot)

# ───────────────── COUNTER ─────────────────
counter_text = fig.text(
    0.98,0.02,'',
    ha='right',
    fontsize=8,
    color='#334',
    fontfamily='monospace'
)

TAIL=1500
STEP=20

# ───────────────── ANIMATION ─────────────────
def animate(frame):

    end=min(TAIL+frame*STEP,N_STEPS)
    start=max(0,end-TAIL)

    # breathing camera motion
    ax.view_init(
        elev=25+5*np.sin(frame*0.02),
        azim=frame*0.45
    )

    for i,((g1,g2,line),dot) in enumerate(zip(lines,dots)):

        xs,ys,zs=trails[i]

        xe=xs[start:end]
        ye=ys[start:end]
        ze=zs[start:end]

        g1.set_data(xe,ye)
        g1.set_3d_properties(ze)

        g2.set_data(xe,ye)
        g2.set_3d_properties(ze)

        line.set_data(xe,ye)
        line.set_3d_properties(ze)

        if len(xe)>0:
            dot.set_data([xe[-1]],[ye[-1]])
            dot.set_3d_properties([ze[-1]])

            # pulse particle
            dot.set_markersize(
                5+2*np.sin(frame*0.3)
            )

    pct=int(100*end/N_STEPS)
    counter_text.set_text(
        f'Points: {end:,} | {pct}%'
    )

    return []

ani=animation.FuncAnimation(
    fig,
    animate,
    frames=(N_STEPS-TAIL)//STEP+1,
    interval=25,
    repeat=True
)

fig.text(
    0.98,0.005,
    "Python · NumPy · Matplotlib",
    ha='right',
    fontsize=7,
    color='#111122',
    fontfamily='monospace'
)

plt.tight_layout()
plt.show()
