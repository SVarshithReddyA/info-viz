import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample dataset creation (for testing)
data = {
    'School ID': np.random.choice(range(1, 11), size=100),
    'Month': np.random.choice(['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'], size=100),
    'Type of Absence': np.random.choice(['Sickness'], size=100),
    'Number of Students Absent': np.random.randint(1, 10, size=100)
}
df = pd.DataFrame(data)

# Aggregate data by School ID, Month, and Type of Absence
aggregated_data = df.groupby(['School ID', 'Month', 'Type of Absence'], as_index=False).sum()

# Define the order of months for plotting
month_order = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
aggregated_data['Month'] = pd.Categorical(aggregated_data['Month'], categories=month_order, ordered=True)
aggregated_data = aggregated_data.sort_values('Month')

# Set up plot
plt.figure(figsize=(14, 8))

# Scatter plot with Month on x-axis, Number of Students Absent on y-axis, and color for each School ID
for school_id in aggregated_data['School ID'].unique():
    school_data = aggregated_data[aggregated_data['School ID'] == school_id]
    plt.scatter(school_data['Month'], school_data['Number of Students Absent'], alpha=0.6, s=100, label=f"School {school_id}")

# Customize plot appearance
plt.title("Monthly Student Absences due to Sickness Across Schools (Sep to Aug)")
plt.xlabel("Month")
plt.ylabel("Number of Students Absent")
plt.grid(True, linestyle='--', alpha=0.6)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add legend for school IDs
plt.legend(title="School ID", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()
