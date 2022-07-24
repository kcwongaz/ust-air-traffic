import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------- #
dstr = "20170101_0000-20171231_2359"

datadir = f"/home/kc/Research/air_traffic/data/loops"
savedir = f"/home/kc/Research/air_traffic/figures/2022-05-12"

# [loop_len, loop_len_seq, loop_total, loop_count]
var = "loop_count"

separated = False
areas = ("NE", "SE", "W")
colors = ("blue", "green", "red")

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
if separated:
    data = {}
    for a in areas:
        data[a] = np.loadtxt(f"{datadir}/{var}_{a}_{dstr}.txt")

    fig, ax = plt.subplots()

    for i, a in enumerate(areas):
        # if a != "W":
        #     continue
        ax.hist(data[a]/60, bins=30, color=colors[i], density=True, alpha=0.5)

    plt.show()

else:
    data = []
    for a in areas:
        data.extend(np.loadtxt(f"{datadir}/{var}_{a}_{dstr}.txt"))

    data = np.array(data)

    fig, ax = plt.subplots()
    ax.hist(data, bins=np.arange(0.5, 5.5, 1),
            color="slategray", rwidth=0.7)

    ax.set_title("Distribution of Loop Count (2017)", fontsize=16)
    ax.set_xlabel("Number of Loop", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    ax.set_xticks(range(1, 5))

    plt.tight_layout()
    plt.savefig(f"{savedir}/hist_{var}.png", dpi=300)
    plt.show()
