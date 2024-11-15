import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Parameters
NUM_SCHOOLS = 10
MONTHS_IN_YEAR = 12
WEEKS_IN_MONTH = 1  # Approximate weeks per month
ABSENCE_REASONS = ['Illness', 'Vacation', 'Other']

# Generate random data for absences with different reasons
def generate_data():
    data = {}
    for reason in ABSENCE_REASONS:
        data[reason] = np.random.randint(0, 10, size=(NUM_SCHOOLS, MONTHS_IN_YEAR * WEEKS_IN_MONTH))
    return data

# Display heatmap with enhancements
def show_heatmap(data):
    # Set a more accessible color palette
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))

    absences_total = sum(data.values())  # Total absences across reasons

    # Use a diverging colormap that's accessible for colorblind individuals
    heatmap = ax.imshow(absences_total, cmap="coolwarm", aspect="auto")

    # Add a color bar with better labels
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label("Number of Absences", fontsize=12)

    # Adjust x-ticks and labels to represent months
    months_labels = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    month_ticks = [i * WEEKS_IN_MONTH for i in range(MONTHS_IN_YEAR)]
    ax.set_xticks(month_ticks)
    ax.set_xticklabels(months_labels, rotation=45, ha="right", fontsize=12)

    # Adjust y-ticks to represent schools
    ax.set_yticks(range(NUM_SCHOOLS))
    ax.set_yticklabels([f"School {i+1}" for i in range(NUM_SCHOOLS)], fontsize=12)

    # Add labels and title with enhanced accessibility
    ax.set_xlabel("Month", fontsize=14)
    ax.set_ylabel("School", fontsize=14)
    ax.set_title("Heatmap of Pupil Absences Over the School Year", fontsize=16, fontweight='bold')

    # Add gridlines for better readability
    ax.grid(False)
    
    # Display the heatmap
    plt.tight_layout()  # Ensures everything fits without overlap
    plt.show()

# Run experiment
def run_experiment():
    data = generate_data()  # Generate random data for absences
    show_heatmap(data)  # Display the heatmap

run_experiment()
