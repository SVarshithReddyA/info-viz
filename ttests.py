import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Step 1: Read all correctness and response time CSV files
correctness_files = glob.glob("responses/*.csv")  # Update with your folder path
response_time_files = glob.glob("times/*.csv")  # Update with your folder path

# Initialize lists to store data
all_heatmap_response_times = []
all_scatter_response_times = []
all_heatmap_correctness = []
all_scatter_correctness = []

# Process correctness files
for file in correctness_files:
    df = pd.read_csv(file)
    
    # Separate data by visualization type
    heatmap_data = df[df['visualization_type'] == 'heatmap']
    scatter_data = df[df['visualization_type'] == 'scatter']
    
    # Collect response times
    all_heatmap_response_times.extend(heatmap_data['response_time_seconds'])
    all_scatter_response_times.extend(scatter_data['response_time_seconds'])
    
    # Collect correctness data
    all_heatmap_correctness.extend(heatmap_data['is_correct'].astype(int))  # Convert True/False to 1/0
    all_scatter_correctness.extend(scatter_data['is_correct'].astype(int))

from scipy.stats import ttest_rel

# Paired t-test for response times
t_response, p_response = ttest_rel(all_heatmap_response_times, all_scatter_response_times)
print(f"Paired T-test for Response Times: t = {t_response:.3f}, p = {p_response:.3f}")

# Paired t-test for error rates
heatmap_error_rates = [1 - x for x in all_heatmap_correctness]
scatter_error_rates = [1 - x for x in all_scatter_correctness]
t_error, p_error = ttest_rel(heatmap_error_rates, scatter_error_rates)
print(f"Paired T-test for Error Rates: t = {t_error:.3f}, p = {p_error:.3f}")


# Step 2: Bar Chart with Error Bars
# Calculate means and standard deviations
mean_heatmap_response = np.mean(all_heatmap_response_times)
std_heatmap_response = np.std(all_heatmap_response_times)
mean_scatter_response = np.mean(all_scatter_response_times)
std_scatter_response = np.std(all_scatter_response_times)

mean_heatmap_error_rate = 1 - np.mean(all_heatmap_correctness)
std_heatmap_error_rate = np.std([1 - x for x in all_heatmap_correctness])
mean_scatter_error_rate = 1 - np.mean(all_scatter_correctness)
std_scatter_error_rate = np.std([1 - x for x in all_scatter_correctness])

# Bar chart for response times
plt.figure(figsize=(8, 5))
plt.bar(['Heatmap', 'Scatter'], [mean_heatmap_response, mean_scatter_response],
        yerr=[std_heatmap_response, std_scatter_response], color=['blue', 'orange'], capsize=5)
plt.title('Average Response Time by Visualization Type')
plt.ylabel('Response Time (s)')
plt.show()

# Bar chart for error rates
plt.figure(figsize=(8, 5))
plt.bar(['Heatmap', 'Scatter'], [mean_heatmap_error_rate, mean_scatter_error_rate],
        yerr=[std_heatmap_error_rate, std_scatter_error_rate], color=['blue', 'orange'], capsize=5)
plt.title('Average Error Rate by Visualization Type')
plt.ylabel('Error Rate')
plt.show()

# Step 3: Histograms
# Histogram for response times
plt.figure(figsize=(10, 6))
plt.hist(all_heatmap_response_times, bins=10, alpha=0.7, label='Heatmap', color='blue')
plt.hist(all_scatter_response_times, bins=10, alpha=0.7, label='Scatter', color='orange')
plt.title('Response Times Distribution')
plt.xlabel('Response Time (s)')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Histogram for error rates
heatmap_error_rates = [1 - x for x in all_heatmap_correctness]
scatter_error_rates = [1 - x for x in all_scatter_correctness]

plt.figure(figsize=(10, 6))
plt.hist(heatmap_error_rates, bins=10, alpha=0.7, label='Heatmap', color='blue')
plt.hist(scatter_error_rates, bins=10, alpha=0.7, label='Scatter', color='orange')
plt.title('Error Rates Distribution')
plt.xlabel('Error Rate')
plt.ylabel('Frequency')
plt.legend()
plt.show()
