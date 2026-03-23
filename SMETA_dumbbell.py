import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# =========================================================
# SMETA-LIKE DUMBBELL PARTICLE FIELD
# Interactive Atman  = copper-sulphate blue side
# Memory Atman       = yellow side
# Mixed local states + tracked particle X
# =========================================================

np.random.seed(7)

# -------------------------
# PARAMETERS
# -------------------------
N = 90                    # 120 works too, but 90 is cleaner for patch animation
dt = 0.55
fr = 0.972

# field dynamics
G = 0.42                  # attraction
R = 0.78                  # repulsion
F = 0.16                  # freedom / noise
O = 0.18                  # oneness to center
A_pulse = 0.34            # tangential dance pulse

# memory field B
alpha = 0.028
lam = 0.020
Bmax = 3.2
beta = 0.10               # memory recollection

# domain
xmin, xmax = 0, 100
ymin, ymax = 0, 100
cx, cy = 50, 50

# dumbbell geometry
bond_len_max = 2.1
r_blue_base = 0.75
r_yellow_base = 0.70

# cycle: ACTIVE -> STEADY -> DISSOLVE -> FREE-YELLOW -> REBIND
active_len = 120
steady_len = 110
dissolve_len = 90
free_len = 75
rebind_len = 95
cycle_len = active_len + steady_len + dissolve_len + free_len + rebind_len

# selected tracked particle
track_idx = 8

# -------------------------
# INITIAL STATE
# -------------------------
x = np.random.rand(N) * 100
y = np.random.rand(N) * 100
vx = np.random.randn(N) * 0.35
vy = np.random.randn(N) * 0.35

B = np.zeros(N)

# per-particle asynchronous cycle offsets
cycle_offset = np.random.randint(0, cycle_len, size=N)

# orientation state for dumbbells
theta = np.random.rand(N) * 2 * np.pi

# store previous B to detect rising/waning
B_prev = B.copy()

# -------------------------
# COLOR PALETTE
# -------------------------
BG = "#071018"
PANEL = "#0d1724"
GRID = "#122130"
WHITE = "#ecf3ff"
MUTED = "#a9b9cc"

# copper sulphate blue
BLUE_RGB = np.array([0.16, 0.55, 0.94])

# warm yellow
YELLOW_RGB = np.array([1.00, 0.85, 0.18])

BOND_RGB = np.array([0.72, 0.78, 0.88])

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def smoothstep(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)

def get_local_cycle_state(frame, idx):
    """
    Returns per-particle local morph targets:
    blue_presence: 0..1   (interactive side exists or dissolved)
    yellow_boost : 0..1   (memory side enlarged)
    bond_presence: 0..1   (connection line visible)
    local_state   : label
    """
    t = (frame + cycle_offset[idx]) % cycle_len

    # 1) ACTIVE: blue strong, dancing/striking, yellow builds
    if t < active_len:
        u = t / active_len
        blue_presence = 1.0
        yellow_boost = 0.25 + 0.55 * smoothstep(u)
        bond_presence = 1.0
        local_state = "ACTIVE"

    # 2) STEADY: yellow enlarged, dumbbell balanced
    elif t < active_len + steady_len:
        u = (t - active_len) / steady_len
        blue_presence = 0.92 - 0.10 * smoothstep(u)
        yellow_boost = 0.82 + 0.10 * smoothstep(u)
        bond_presence = 1.0
        local_state = "STEADY"

    # 3) DISSOLVE: blue shrinks, yellow still present
    elif t < active_len + steady_len + dissolve_len:
        u = (t - active_len - steady_len) / dissolve_len
        blue_presence = 1.0 - smoothstep(u)
        yellow_boost = 0.88 - 0.15 * smoothstep(u)
        bond_presence = 1.0 - 0.7 * smoothstep(u)
        local_state = "DISSOLVING"

    # 4) FREE-YELLOW: blue absent, yellow free
    elif t < active_len + steady_len + dissolve_len + free_len:
        u = (t - active_len - steady_len - dissolve_len) / free_len
        blue_presence = 0.0
        yellow_boost = 0.68 - 0.18 * smoothstep(u)
        bond_presence = 0.0
        local_state = "FREE-YELLOW"

    # 5) REBIND: blue returns and binds again
    else:
        u = (t - active_len - steady_len - dissolve_len - free_len) / rebind_len
        blue_presence = smoothstep(u)
        yellow_boost = 0.48 + 0.18 * smoothstep(u)
        bond_presence = smoothstep(u)
        local_state = "REBINDING"

    return blue_presence, yellow_boost, bond_presence, local_state

def compute_metrics(x, y, vx, vy, B):
    dx = x - cx
    dy = y - cy
    r = np.sqrt(dx**2 + dy**2) + 1e-9

    mean_radius = np.mean(r)
    vr = np.mean((vx * dx + vy * dy) / r)
    radial_std = np.std(r)
    coherence = 1.0 / (1.0 + radial_std)
    central_density = np.mean(r < 20)
    kinetic = np.mean(vx**2 + vy**2)
    mean_B = np.mean(B)

    return {
        "mean_radius": mean_radius,
        "vr": vr,
        "coherence": coherence,
        "central_density": central_density,
        "kinetic": kinetic,
        "mean_B": mean_B,
    }

def dominant_global_phase(local_states):
    labels = ["ACTIVE", "STEADY", "DISSOLVING", "FREE-YELLOW", "REBINDING"]
    counts = {k: 0 for k in labels}
    for s in local_states:
        counts[s] += 1
    dom = max(counts, key=counts.get)
    frac = counts[dom] / len(local_states)
    return dom, counts, frac

# -------------------------
# FIGURE
# -------------------------
fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")

for spine in ax.spines.values():
    spine.set_color(GRID)

ax.tick_params(colors=MUTED, labelsize=9)
ax.grid(color=GRID, alpha=0.22, linewidth=0.7)

title_text = ax.text(
    0.5, 1.02,
    "SMETA Dumbbell Field: Blue = Interactive Ātman | Yellow = Memory Ātman",
    transform=ax.transAxes,
    ha="center", va="bottom",
    color=WHITE, fontsize=12, fontweight="bold"
)

phase_text = ax.text(
    0.02, 0.98, "",
    transform=ax.transAxes,
    ha="left", va="top",
    color=WHITE, fontsize=14, fontweight="bold"
)

metric_text = ax.text(
    0.02, 0.90, "",
    transform=ax.transAxes,
    ha="left", va="top",
    color=MUTED, fontsize=9, family="monospace"
)

track_text = ax.text(
    0.72, 0.98, "",
    transform=ax.transAxes,
    ha="left", va="top",
    color=WHITE, fontsize=11
)

legend_text = ax.text(
    0.5, -0.06,
    "Blue end leads interaction/dance. Yellow end stores memory. "
    "Blue fades in dissolution; yellow remains in free-memory phase.",
    transform=ax.transAxes,
    ha="center", va="top",
    color=MUTED, fontsize=9
)

# particle artists
bond_lines = []
yellow_patches = []
blue_patches = []
track_label_artist = ax.text(0, 0, "X", color="white", fontsize=11, fontweight="bold")

for _ in range(N):
    line = Line2D([], [], lw=1.3, color=BOND_RGB, alpha=0.75)
    ax.add_line(line)
    bond_lines.append(line)

    cy_patch = Circle((0, 0), radius=0.5, facecolor=YELLOW_RGB, edgecolor="none", alpha=0.95)
    cb_patch = Circle((0, 0), radius=0.5, facecolor=BLUE_RGB, edgecolor="none", alpha=0.95)

    ax.add_patch(cy_patch)
    ax.add_patch(cb_patch)

    yellow_patches.append(cy_patch)
    blue_patches.append(cb_patch)

# -------------------------
# UPDATE FUNCTION
# -------------------------
def update(frame):
    global x, y, vx, vy, B, B_prev, theta

    # -----------------------------------
    # pairwise field on particle centers
    # -----------------------------------
    fx = np.zeros(N)
    fy = np.zeros(N)

    for i in range(N):
        dx = x - x[i]
        dy = y - y[i]
        dist2 = dx * dx + dy * dy + 1e-6
        dist = np.sqrt(dist2)

        mask = np.ones(N, dtype=bool)
        mask[i] = False

        fx[i] += np.sum(G * dx[mask] / (dist2[mask] + 8.0))
        fy[i] += np.sum(G * dy[mask] / (dist2[mask] + 8.0))

        fx[i] += np.sum(-R * dx[mask] / (dist2[mask] + 0.55)**1.16)
        fy[i] += np.sum(-R * dy[mask] / (dist2[mask] + 0.55)**1.16)

    # -----------------------------------
    # center pull
    # -----------------------------------
    dx0 = cx - x
    dy0 = cy - y
    r0 = np.sqrt(dx0**2 + dy0**2) + 1e-9

    fx += O * dx0 / r0
    fy += O * dy0 / r0

    # -----------------------------------
    # tangential pulse ("dance")
    # -----------------------------------
    tx = -dy0 / r0
    ty = dx0 / r0
    pulse = A_pulse * np.sin(2 * np.pi * frame / 85.0)
    fx += pulse * tx
    fy += pulse * ty

    # -----------------------------------
    # local cycle influence
    # -----------------------------------
    local_states = []
    blue_presence_arr = np.zeros(N)
    yellow_boost_arr = np.zeros(N)
    bond_presence_arr = np.zeros(N)

    for i in range(N):
        blue_p, y_boost, bond_p, state = get_local_cycle_state(frame, i)
        blue_presence_arr[i] = blue_p
        yellow_boost_arr[i] = y_boost
        bond_presence_arr[i] = bond_p
        local_states.append(state)

    # ACTIVE particles prefer peripheral/tangential striking
    active_strength = (np.array([1.0 if s == "ACTIVE" else 0.0 for s in local_states])
                       * blue_presence_arr)
    fx += 0.55 * active_strength * tx + 0.20 * active_strength * (x - cx) / r0
    fy += 0.55 * active_strength * ty + 0.20 * active_strength * (y - cy) / r0

    # FREE-YELLOW particles drift more softly, less bound
    free_strength = np.array([1.0 if s == "FREE-YELLOW" else 0.0 for s in local_states])
    fx += 0.04 * free_strength * np.random.randn(N)
    fy += 0.04 * free_strength * np.random.randn(N)

    # REBINDING particles are gently recollected by memory
    rebind_strength = np.array([1.0 if s == "REBINDING" else 0.0 for s in local_states])
    fx += beta * rebind_strength * (cx - x) / r0 * (0.3 + B / (Bmax + 1e-9))
    fy += beta * rebind_strength * (cy - y) / r0 * (0.3 + B / (Bmax + 1e-9))

    # DISSOLVING particles move outward a bit
    dissolve_strength = np.array([1.0 if s == "DISSOLVING" else 0.0 for s in local_states])
    fx += 0.28 * dissolve_strength * (x - cx) / r0
    fy += 0.28 * dissolve_strength * (y - cy) / r0

    # freedom
    fx += F * np.random.randn(N)
    fy += F * np.random.randn(N)

    # -----------------------------------
    # memory B dynamics
    # blue-active interaction helps yellow memory grow
    # -----------------------------------
    interaction_input = np.sqrt(fx**2 + fy**2)

    # blue side striking periphery enhances yellow side
    drive = interaction_input * (0.45 + 0.55 * blue_presence_arr)
    dB = alpha * drive * (1 - B / Bmax) - lam * B

    # in FREE-YELLOW phase memory decays more gently
    dB += 0.006 * free_strength

    B += dt * dB
    B = np.clip(B, 0, Bmax)

    # memory stabilizes velocity
    damp = 0.022 + 0.020 * (B / (Bmax + 1e-9))
    vx += dt * (fx - damp * vx)
    vy += dt * (fy - damp * vy)

    vx *= fr
    vy *= fr

    x += dt * vx
    y += dt * vy

    # reflective boundaries
    hit_left = x < xmin
    hit_right = x > xmax
    hit_bottom = y < ymin
    hit_top = y > ymax

    vx[hit_left | hit_right] *= -0.88
    vy[hit_bottom | hit_top] *= -0.88

    x = np.clip(x, xmin, xmax)
    y = np.clip(y, ymin, ymax)

    # -----------------------------------
    # update dumbbell orientation
    # blue end tends to point along motion / outward-interaction
    # yellow stays opposite
    # -----------------------------------
    vel_theta = np.arctan2(vy, vx + 1e-12)
    rad_theta = np.arctan2(y - cy, x - cx + 1e-12)

    # ACTIVE: more tangential/outward
    preferred = 0.65 * vel_theta + 0.35 * (rad_theta + 0.35*np.sin(frame/20.0))
    theta = 0.86 * theta + 0.14 * preferred

    # -----------------------------------
    # visuals
    # -----------------------------------
    artists = []

    for i in range(N):
        blue_p = blue_presence_arr[i]
        y_boost = yellow_boost_arr[i]
        bond_p = bond_presence_arr[i]

        # size rules
        yellow_r = r_yellow_base + 1.25 * (B[i] / (Bmax + 1e-9)) + 0.90 * y_boost
        blue_r = (r_blue_base + 0.55 * blue_p + 0.16 * np.sqrt(vx[i]**2 + vy[i]**2)) * blue_p

        # bond length shrinks when blue dissolves
        L = bond_len_max * (0.20 + 0.80 * bond_p) * (0.35 + 0.65 * max(blue_p, 0.12))

        ux = np.cos(theta[i])
        uy = np.sin(theta[i])

        # blue end leads, yellow trails
        xb = x[i] + 0.5 * L * ux
        yb = y[i] + 0.5 * L * uy
        xy = x[i] - 0.5 * L * ux
        yy = y[i] - 0.5 * L * uy

        # if blue nearly absent -> yellow sits at center, blue hidden
        if blue_p < 0.05:
            xb, yb = x[i], y[i]
            xy, yy = x[i], y[i]

        # bond line
        bond_lines[i].set_data([xy, xb], [yy, yb])
        bond_lines[i].set_alpha(0.15 + 0.65 * bond_p)
        bond_lines[i].set_color(BOND_RGB * (0.85 + 0.15 * (B[i] / (Bmax + 1e-9))))

        # yellow memory patch
        yellow_color = np.clip(YELLOW_RGB * (0.85 + 0.22 * (B[i] / (Bmax + 1e-9))), 0, 1)
        yellow_patches[i].center = (xy, yy)
        yellow_patches[i].radius = yellow_r
        yellow_patches[i].set_facecolor(yellow_color)
        yellow_patches[i].set_alpha(0.88)

        # blue interactive patch
        blue_color = np.clip(BLUE_RGB * (0.80 + 0.20 * blue_p), 0, 1)
        blue_patches[i].center = (xb, yb)
        blue_patches[i].radius = max(0.001, blue_r)
        blue_patches[i].set_facecolor(blue_color)
        blue_patches[i].set_alpha(0.10 + 0.85 * blue_p)

        artists.extend([bond_lines[i], yellow_patches[i], blue_patches[i]])

    # tracked particle X
    blue_p = blue_presence_arr[track_idx]
    y_boost = yellow_boost_arr[track_idx]
    bond_p = bond_presence_arr[track_idx]
    state_x = local_states[track_idx]

    ux = np.cos(theta[track_idx])
    uy = np.sin(theta[track_idx])
    Lx = bond_len_max * (0.20 + 0.80 * bond_p) * (0.35 + 0.65 * max(blue_p, 0.12))
    xt = x[track_idx]
    yt = y[track_idx]

    track_label_artist.set_position((xt + 2.4, yt + 2.1))

    # -----------------------------------
    # text panel
    # -----------------------------------
    metrics = compute_metrics(x, y, vx, vy, B)
    global_phase, counts, frac = dominant_global_phase(local_states)

    phase_text.set_text(f"DOMINANT PHASE: {global_phase}   ({frac*100:.1f}% particles)")
    metric_text.set_text(
        f"mean_radius   = {metrics['mean_radius']:.2f}\n"
        f"radial_flow   = {metrics['vr']:.3f}\n"
        f"coherence     = {metrics['coherence']:.3f}\n"
        f"central_frac  = {metrics['central_density']:.3f}\n"
        f"memory_B      = {metrics['mean_B']:.3f}\n"
        f"ACTIVE        = {counts['ACTIVE']:>3d}\n"
        f"STEADY        = {counts['STEADY']:>3d}\n"
        f"DISSOLVING    = {counts['DISSOLVING']:>3d}\n"
        f"FREE-YELLOW   = {counts['FREE-YELLOW']:>3d}\n"
        f"REBINDING     = {counts['REBINDING']:>3d}"
    )

    dB_track = B[track_idx] - B_prev[track_idx]
    trend = "rising" if dB_track > 0.002 else ("waning" if dB_track < -0.002 else "steady")

    track_text.set_text(
        f"Tracked X\n"
        f"state   = {state_x}\n"
        f"B(X)    = {B[track_idx]:.2f}\n"
        f"trend   = {trend}\n"
        f"blue    = {blue_p:.2f}"
    )

    B_prev[:] = B
    artists.extend([phase_text, metric_text, title_text, track_text, legend_text, track_label_artist])
    return artists

# -------------------------
# ANIMATION
# -------------------------
ani = FuncAnimation(fig, update, frames=2200, interval=40, blit=False)
plt.show()
