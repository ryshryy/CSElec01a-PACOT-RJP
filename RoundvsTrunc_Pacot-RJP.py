from decimal import Decimal, getcontext, ROUND_HALF_UP
import matplotlib.pyplot as plt
import numpy as np

# 1. Decimal precision & π
# Setting precision high enough to handle 100+ decimal places
getcontext().prec = 150 

PI_FULL = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513"
)

# 2. Truncate and Round functions
def truncate_pi(pi, decimals):
    factor = Decimal(10) ** decimals
    return (pi * factor // 1) / factor

def round_pi(pi, decimals):
    return pi.quantize(
        Decimal(f"1.{'0'*decimals}"),
        rounding=ROUND_HALF_UP
    )

# 3. Cylinder volume
r = Decimal("2")
h = Decimal("10")

def volume(pi):
    return pi * r**2 * h

# True volume based on our high-precision Pi
V_true = volume(PI_FULL)

# Decimal points to check
decimals_list = [20, 40, 60, 100]

# Lists to store data for plotting
delta_trunc_list = []
delta_round_list = []

print(f"TRUE VOLUME: {V_true}\n")
print("Formula: V = π * r^2 * h")
print(f"Given: r = {r}, h = {h}\n")

for d in decimals_list:
    # Get truncated and rounded pi at this decimal
    pi_t = truncate_pi(PI_FULL, d)
    pi_r = round_pi(PI_FULL, d)

    # Compute volume using each
    V_t = volume(pi_t)
    V_r = volume(pi_r)

     # Differences
    delta_trunc = abs(V_t - V_true)
    delta_round = abs(V_r - V_true)

    delta_trunc_list.append(float(delta_trunc))
    delta_round_list.append(float(delta_round))
    
        # Determine which is closer
    if delta_trunc < delta_round:
        remark = "Truncation is closer to true volume"
    elif delta_round < delta_trunc:
        remark = "Rounding is closer to true volume"
    else:
        remark = "Truncation and Rounding are equally close"

    print(f"--- {d} DECIMAL PLACES ---")
    print("Truncated π :", pi_t)
    print("Rounded π   :", pi_r)
    print("Truncated Volume :", V_t)
    print("Rounded Volume   :", V_r)
    print("Δ (Trunc vs True):", abs(V_t - V_true))
    print("Δ (Round vs True):", abs(V_r - V_true))
    print("Δ (Round vs Trunc):", abs(V_r - V_t))
    print("Remarks:", remark)
    print()
    

# 4. Visualization
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(decimals_list))
width = 0.35

# Plotting bars
rects1 = ax.bar(x - width/2, delta_trunc_list, width, label='Truncation Error', color='#3498db', alpha=0.85, edgecolor='black')
rects2 = ax.bar(x + width/2, delta_round_list, width, label='Rounding Error', color='#e74c3c', alpha=0.85, edgecolor='black')

# Using log scale for the Y-axis to see the tiny differences
ax.set_yscale('log')

# Adding 'r' before strings to avoid SyntaxWarnings with LaTeX symbols
ax.set_xticks(x)
ax.set_xticklabels(decimals_list)
ax.set_xlabel(r'Decimal Places of $\pi$', fontsize=12, fontweight='bold')
ax.set_ylabel(r'Absolute Error ($\Delta$)', fontsize=12, fontweight='bold')
ax.set_title(r'Precision Impact: Truncation vs. Rounding of $\pi$ in Volume Calculations', fontsize=14, pad=20, fontweight='bold')

ax.legend(frameon=True, facecolor='white', shadow=True)
ax.grid(True, which="both", ls="-", alpha=0.2)

# Helper function to add scientific notation labels above bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        if height > 0:
            ax.annotate(f'{height:.1e}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 5), 
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=45)

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.show()