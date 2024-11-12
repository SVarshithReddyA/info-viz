import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample dataset creation (for testing)
data = {
    'School ID': np.random.choice(range(1, 11), size=100),
    'Type of Absence': np.random.choice(['Sickness'], size=100),
    'Number of Students Absent': np.random.randint(1, 10, size=100)
}
df = pd.DataFrame(data)

# Aggregate data by School ID and Type of Absence
aggregated_data = df.groupby(['School ID', 'Type of Absence'], as_index=False).sum()

# Set up plot
plt.figure(figsize=(12, 8))

# Scatter plot with School ID on x-axis and Number of Students Absent on y-axis
plt.scatter(aggregated_data['School ID'], aggregated_data['Number of Students Absent'],
            color='blue', alpha=0.6, label="Sickness", s=100)

# Customize plot appearance
plt.title("Number of Students Absent due to Sickness Across Schools")
plt.xlabel("School ID")
plt.ylabel("Number of Students Absent")
plt.grid(True, linestyle='--', alpha=0.6)

# Set School ID as custom tick labels
plt.xticks(ticks=aggregated_data['School ID'].unique(), labels=[f"School {int(sid)}" for sid in aggregated_data['School ID'].unique()])

# Add legend
plt.legend(title="Type of Absence")

plt.show()
