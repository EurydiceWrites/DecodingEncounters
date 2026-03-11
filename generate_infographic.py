import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Connect to DB and fetch the actual motif frequencies
conn = sqlite3.connect('ufo_matrix.db')

query = """
SELECT SUBSTR(m.current_family_header, 1, 1) as Category_Letter, 
       m.current_family_header,
       COUNT(e.Motif_Code) as Occurrence_Count
FROM Encounter_Events e
JOIN Motif_Dictionary m ON e.Motif_Code = m.motif_number
GROUP BY Category_Letter, m.current_family_header
ORDER BY Occurrence_Count DESC
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Clean up headers
def clean_header(h):
    h = h.split('--')[-1].replace('.', '').title()
    if h == 'The Beings': return 'Beings (Entities)'
    if h == 'The Ufo': return 'The UFO (Craft)'
    if h == 'The Otherworld': return 'Otherworld Journey'
    if h == 'Theorhany': return 'Theophany'
    if h == 'Messases': return 'Messages'
    return h.strip()

df['Clean_Category'] = df['current_family_header'].apply(clean_header)

# Data for plot
categories = df['Clean_Category'].tolist()
counts = df['Occurrence_Count'].tolist()

# Setup Dark Mode Style
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

fig.patch.set_facecolor('#0f111a')
ax.set_facecolor('#0f111a')

# Create a gradient color map for the bars
colors = sns.color_palette("mako", len(categories))
bars = ax.barh(categories, counts, color=colors, height=0.6, edgecolor='#1a1f2e', linewidth=1)

# Invert Y axis so the highest is at the top
ax.invert_yaxis()

# Add glowing data labels
for bar, count in zip(bars, counts):
    ax.text(bar.get_width() + 15, bar.get_y() + bar.get_height()/2, 
            f'{count:,}', 
            va='center', ha='left', color='#00d2ff', fontsize=12, fontweight='bold', alpha=0.9)

# Formatting
ax.set_title("THE ARCHITECTURE OF THE PHENOMENON\nRecorded Occurrences by Bullard's Sequential Motifs", 
             fontsize=18, color='#ffffff', fontweight='bold', pad=25, loc='left')

ax.set_xlabel("Total Logged Events (n=4,364)", fontsize=11, color='#a0a8b9', labelpad=15)
ax.tick_params(axis='y', colors='#e2e8f0', labelsize=12)
ax.tick_params(axis='x', colors='#a0a8b9', labelsize=10)

# Remove borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#2a324b')
ax.spines['bottom'].set_color('#2a324b')

# Add subtle grid
ax.xaxis.grid(True, linestyle='--', alpha=0.2, color='#ffffff')

# Add footer
fig.text(0.12, 0.03, "Source: Thomas E. Bullard (1987) | Processed via UFO Matrix AI Pipeline", 
         fontsize=9, color='#718096', style='italic')

plt.tight_layout()
plt.subplots_adjust(bottom=0.1)

output_path = "ufo_architecture_infographic.png"
plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
print(f"Infographic saved to {output_path}")
