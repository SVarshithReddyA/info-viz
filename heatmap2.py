import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Sample dataset creation (for testing)
data = {
    'School ID': np.random.choice(range(1, 11), size=100),
    'Type of Absence': np.random.choice(['Sickness'], size=100),
    'Number of Students Absent': np.random.randint(1, 10, size=100)
}
df = pd.DataFrame(data)

# Aggregate data by School ID and Type of Absence
aggregated_data = df.groupby(['School ID', 'Type of Absence'], as_index=False).sum()

# Pivot the data to create a matrix suitable for a heatmap
heatmap_data = aggregated_data.pivot(index='School ID', columns='Type of Absence', values='Number of Students Absent').fillna(0)

# Set up the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='Blues', cbar_kws={'label': 'Number of Students Absent'})

# Customize plot appearance
plt.title("Heatmap of Student Absences due to Sickness Across Schools")
plt.xlabel("Type of Absence")
plt.ylabel("School ID")
plt.yticks(rotation=0)  # Keep School ID labels horizontal

plt.show()
