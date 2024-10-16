import numpy as np
import scipy.stats as st

def calculate_confidence_interval(data, confidence=0.95):
    # Calculate mean
    mean = np.mean(data)

    # Calculate standard deviation
    std_dev = np.std(data, ddof=1)  # Sample standard deviation

    # Sample size
    n = len(data)

    # Calculate SEM
    sem = std_dev / np.sqrt(n)

    # Calculate the 95% confidence interval using t-distribution
    t_value = st.t.ppf((1 + confidence) / 2, n - 1)  # t-value for n-1 degrees of freedom

    error = t_value * sem

    return error

import numpy as np
import matplotlib.pyplot as plt

def plot_messaging_strategies_by_topic(data_merged_subset, treatment_var, strategies, topics_dict, 
                                       calculate_confidence_interval, xlabel, filename, 
                                       x_limits=None, colors=None, markers=None):
    """
    Plots the persuasive impact of different messaging strategies across multiple topics 
    with error bars and annotations.
    
    Parameters:
    - data_merged_subset: DataFrame, the dataset containing the data.
    - treatment_var: str, the name of the variable used for grouping and calculating means and errors.
    - strategies: list of str, the list of strategies used (e.g., ['False-Targeted', 'Non-Targeted', 'Targeted']).
    - topics_dict: dict, a dictionary mapping topics to their English equivalents 
                   (e.g., {'Atomkraft': 'Nuclear Power', 'Parteiverbot': 'Party Ban', ...}).
    - calculate_confidence_interval: function, a function that calculates the confidence interval for error bars.
    - xlabel: str, the label for the x-axis.
    - filename: str, the path to save the plot as a PDF.
    - x_limits: tuple, optional, a tuple specifying the limits for the x-axis (e.g., (min, max)).
    - colors: list, optional, a list of colors to use for the topics. If None, default greyscale colors will be used.
    - markers: list, optional, a list of markers to use for each topic (e.g., ['^', 'o', 's', 'D']).
    """
    
    # Default greyscale colors if not provided
    if colors is None:
        colors = ['dimgray', 'grey', 'darkgrey', 'lightgrey']
    
    # Ensure we have enough colors
    if len(colors) < len(topics_dict):
        raise ValueError(f"Insufficient colors provided. {len(topics_dict)} topics but only {len(colors)} colors available.")
    
    # Default markers if not provided
    if markers is None:
        markers = ['^', 'o', 's', 'D']  # triangle, circle, square, rhombus
    
    # Ensure we have enough markers
    if len(markers) < len(topics_dict):
        raise ValueError(f"Insufficient markers provided. {len(topics_dict)} topics but only {len(markers)} markers available.")
    
    # Calculate means and confidence intervals for each topic and treatment group
    means = data_merged_subset.groupby(['topic', 'treatment'])[treatment_var].mean()
    errors = data_merged_subset.groupby(['topic', 'treatment'])[treatment_var].apply(calculate_confidence_interval)

    # Prepare data for each topic (from the topics_dict)
    topic_means = {topic: list(means[topic]) for topic in topics_dict.keys()}
    topic_errors = {topic: list(errors[topic]) for topic in topics_dict.keys()}

    # Calculate weighted means and confidence intervals across all topics
    overall_means = data_merged_subset.groupby('treatment')[treatment_var].mean()
    overall_errors = data_merged_subset.groupby('treatment')[treatment_var].apply(calculate_confidence_interval)

    # Create a small offset for each data point so they don't overlap
    offset = 0.125
    y_pos = np.arange(len(strategies))

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(11.5/2.54, 11.5/2.54))  # Convert cm to inches

    # Plot each topic's means with dynamically assigned colors and markers
    for i, (topic, english_topic) in enumerate(topics_dict.items()):
        ax.errorbar(topic_means[topic], y_pos + (len(topics_dict) - i - 2) * offset, 
                    xerr=topic_errors[topic], fmt=markers[i], color=colors[i], 
                    label=english_topic, capsize=0, elinewidth=1., markersize=3)

    # Plot weighted means (always in red, marker '|')
    ax.errorbar(overall_means, y_pos - (len(topics_dict) - 2) * offset, xerr=overall_errors, 
                fmt='|', color='red', label='Mean', capsize=0, elinewidth=1., markersize=5)

    # Add annotations for the data points
    for topic, means_data in topic_means.items():
        for i, (x, y) in enumerate(zip(means_data, y_pos + (len(topics_dict) - list(topics_dict.keys()).index(topic) - 2) * offset - 0.02)):
            ax.annotate(f'{x:.2f}', (x, y), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom', color=colors[list(topics_dict.keys()).index(topic)], fontsize=7)

    # Add annotations for weighted means
    for i, (x, y) in enumerate(zip(overall_means, y_pos - (len(topics_dict) - 2) * offset - 0.02)):
        ax.annotate(f'{x:.2f}', (x, y), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom', color='red', fontsize=7)

    # Customize grid, labels, and title
    ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(strategies, fontsize=8)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.tick_params(axis='x', labelsize=8)
    
    # Set x-axis limits if provided
    if x_limits is not None:
        ax.set_xlim(x_limits)
    
    # Customize legend
    ax.legend(fontsize=6.5, frameon=True, title_fontsize='7', loc='lower left', title='Topic').get_frame().set_linewidth(0.5)

    for spine in ax.spines.values():
        spine.set_linewidth(1)

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

    # Save the plot as a PDF
    fig.savefig(filename)

# Example usage:
topics_dict = {
    'Atomkraft': 'Nuclear Power',
    'Parteiverbot': 'Party Ban',
    'Schuldenbremse': 'Debt Brake',
    'Tempolimit': 'General Speed Limit'
}

# Define your colors (optional), or let the function assign default greyscale colors
colors = ['dimgray', 'grey', 'darkgrey', 'lightgrey']
# Define markers for each topic
markers = ['^', 'o', 's', 'D']  # triangle, circle, square, rhombus