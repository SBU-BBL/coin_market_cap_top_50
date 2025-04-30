import matplotlib.pyplot as plt
import numpy as np

# Labels for sentiment classes
labels = ['Bearish (-1)', 'Neutral (0)', 'Bullish (1)']

# Metric values from your chart
precision = [0.27, 0.54, 0.40]
recall =    [0.83, 0.22, 0.07]
f1_score =  [0.41, 0.32, 0.12]

x = np.arange(len(labels))  # label locations
width = 0.25  # width of the bars

fig, ax = plt.subplots(figsize=(8, 6))
bars1 = ax.bar(x - width, precision, width, label='Precision', color='#FDB813')
bars2 = ax.bar(x, recall, width, label='Recall', color='#FF6F1E')
bars3 = ax.bar(x + width, f1_score, width, label='F1 Score', color='#EF3E6B')

# Add value labels on top
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

# Customization
ax.set_ylabel('Score')
ax.set_title('Model Performance by Sentiment Class')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.set_ylim(0, 1.05)
plt.tight_layout()
plt.show()
