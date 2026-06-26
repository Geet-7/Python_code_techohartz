import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Slide 143: Line Chart
fig, ax = plt.subplots(figsize=(8, 5))
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]
ax.plot(x, y, marker='o', color='#2563eb', linewidth=2, markersize=6)
ax.set_title('Square Numbers', fontsize=14, fontweight='bold')
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig('chart_line.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# Slide 144: Bar Chart
fig, ax = plt.subplots(figsize=(8, 5))
fruits = ['Apple', 'Banana', 'Cherry']
quantities = [23, 17, 35]
colors = ['#dc2626', '#facc15', '#f472b6']
ax.bar(fruits, quantities, color=colors, edgecolor='white')
ax.set_title('Fruit Quantities', fontsize=14, fontweight='bold')
ax.set_xlabel('Fruit', fontsize=12)
ax.set_ylabel('Quantity', fontsize=12)
fig.tight_layout()
fig.savefig('chart_bar.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# Slide 145: Pie Chart
fig, ax = plt.subplots(figsize=(8, 5))
sizes = [30, 20, 25, 25]
labels = ['A', 'B', 'C', 'D']
colors = ['#2563eb', '#059669', '#d97706', '#7c3aed']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax.set_title('Distribution', fontsize=14, fontweight='bold')
fig.tight_layout()
fig.savefig('chart_pie.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# Slide 146: Subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot([1, 2, 3], [1, 4, 9], marker='o', color='#2563eb')
axes[0, 0].set_title('Line Chart')
axes[0, 1].bar(['A', 'B'], [3, 7], color=['#059669', '#d97706'])
axes[0, 1].set_title('Bar Chart')
axes[1, 0].scatter([1, 2, 3], [1, 4, 9], color='#7c3aed', s=100)
axes[1, 0].set_title('Scatter Plot')
axes[1, 1].pie([30, 70], labels=['A', 'B'], colors=['#dc2626', '#2563eb'])
axes[1, 1].set_title('Pie Chart')
plt.tight_layout()
fig.savefig('chart_subplots.png', dpi=150, bbox_inches='tight')
plt.close(fig)

print("Chart images generated successfully!")
