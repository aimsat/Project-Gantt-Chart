
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

# Data
data = {
    'Task': ['Project Planning and Requirements Gathering', 'Database Design and Setup', 'User Authentication',
             'Product Management', 'Promotional Offers Management', 'Refund Processing',
             'Checkout and Order Processing', 'UI Design', 'Cart and Promotion Logic',
             'Admin Panel', 'Testing and Bug Fixing', 'Deployment', 'Documentation and Final Review'],
    'Start Date': ['23/05/2024', '25/05/2024', '26/05/2024', '27/05/2024', '30/05/2024',
                   '31/05/2024', '31/05/2024', '2/06/2024', '2/06/2024', '2/06/2024',
                   '3/06/2024', '3/06/2024', '4/06/2024'],
    'End Date': ['25/05/2024', '26/05/2024', '27/05/2024', '29/05/2024', '31/05/2024',
                 '2/06/2024', '2/06/2024', '2/06/2024', '2/06/2024', '3/06/2024',
                 '3/06/2024', '4/06/2024', '4/06/2024']
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert date columns to datetime
df['Start Date'] = pd.to_datetime(df['Start Date'], format='%d/%m/%Y')
df['End Date'] = pd.to_datetime(df['End Date'], format='%d/%m/%Y')

# Calculate duration
df['Duration'] = (df['End Date'] - df['Start Date']).dt.days + 1

# Apply a professional style
plt.style.use('seaborn-darkgrid')

# Create the Gantt chart
fig, ax = plt.subplots(figsize=(14, 8))

# Define colors for tasks
colors = plt.cm.tab20(range(len(df)))

# Plot each task with its color
for idx, (row, color) in enumerate(zip(df.iterrows(), colors)):
    _, row = row
    ax.broken_barh([(mdates.date2num(row['Start Date']), row['Duration'])],
                   (len(df) - idx - 1, 0.8), facecolors=color)  # Adjusted y position for reversed order

# Highlight parallel activities
parallel_tasks = [7, 8, 9]  # Indexes of UI Design, Cart and Promotion Logic, and Admin Panel

for idx in parallel_tasks:
    task_start = mdates.date2num(df['Start Date'][idx])
    task_end = mdates.date2num(df['End Date'][idx])
    ax.broken_barh([(task_start, task_end - task_start)],
                   (len(df) - idx - 1, 0.8), facecolors='lightblue', edgecolor='black', linewidth=1.2, alpha=0.3)

# Draw dashed lines to indicate parallelism
for idx in parallel_tasks:
    task_start = mdates.date2num(df['Start Date'][idx])
    task_end = mdates.date2num(df['End Date'][idx])
    ax.plot([task_start, task_end], [len(df) - idx - 1 + 0.4, len(df) - idx - 1 + 0.4], 'k--', lw=1.5, alpha=0.7)

# Set x-axis limits to ensure no gap and start from 23/05/2024
start_date = df['Start Date'].min()  # Start from the earliest task start date
end_date = df['End Date'].max() + pd.Timedelta(days=1)
ax.set_xlim([mdates.date2num(start_date), mdates.date2num(end_date)])

# Set y-axis labels and formatting
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['Task'][::-1], fontsize=10)  # Reversed task order

# Create a secondary x-axis at the top
ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())  # Sync x-axis limits
ax_top.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax_top.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
ax_top.tick_params(axis='x', rotation=45, labelsize=10)
ax_top.set_xlabel('Date', fontsize=12)
ax_top.xaxis.set_ticks_position('top')  # Move ticks to the top
ax_top.xaxis.set_label_position('top')  # Set x-axis label position to the top

# Remove bottom x-axis ticks and labels
ax.set_xticks([])
ax.set_xticklabels([])

# Set y-axis label and title fonts
plt.xlabel('Date', fontsize=12)
plt.ylabel('Task', fontsize=12)
plt.title('Project Gantt Chart', fontsize=14)

# Add activity legend below the chart
legend_elements = [plt.Line2D([0], [0], color=color, lw=4, label=task) for task, color in zip(df['Task'], colors)]

# Add a legend for highlighted activities
highlight_legend = [plt.Line2D([0], [0], color='lightblue', lw=4, label='Parallel Activities')]

# Adjust layout to make room for legend
fig.tight_layout(rect=[0, 0.1, 1, 1])  # Make extra room at the bottom

# Add legend below the chart
fig.legend(handles=legend_elements + highlight_legend, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=10)

plt.show()