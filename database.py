import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class DataArchiver:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = 'logs'
        self.data_list = []
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def save_record(self, data_dict):
        self.data_list.append(data_dict)

    def generate_comprehensive_report(self):
        if not self.data_list:
            print("No data collected.")
            return

        df = pd.DataFrame(self.data_list)
        
        # Ensure 'Gait' and 'Jerk' exist to prevent ValueErrors
        if 'Gait' not in df.columns: df['Gait'] = 0
        if 'Jerk' not in df.columns: df['Jerk'] = 0

        excel_path = os.path.join(self.log_dir, f"Session_{self.session_id}.xlsx")
        df.to_excel(excel_path, index=False)

        plt.figure(figsize=(16, 10))
        
        # A. Line Graph (Velocity)
        plt.subplot(2, 2, 1)
        sns.lineplot(data=df, x=df.index, y='Velocity', color='blue')
        plt.title("Movement Velocity")

        # B. Bar Chart (Status) - Fixed Warning
        plt.subplot(2, 2, 2)
        status_counts = df['Status'].value_counts()
        sns.barplot(x=status_counts.index, y=status_counts.values, hue=status_counts.index, palette="viridis", legend=False)
        plt.title("Scenario Distribution")
        plt.xticks(rotation=45)

        # C. Pie Chart
        plt.subplot(2, 2, 3)
        status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title("Safety Ratio")

        # D. Scatter Plot - Fixed KeyError
        plt.subplot(2, 2, 4)
        sns.scatterplot(data=df, x='Gait', y='Jerk', hue='Status', alpha=0.6)
        plt.title("Gait vs Impact Intensity")

        report_path = os.path.join(self.log_dir, f"Analytics_{self.session_id}.png")
        plt.tight_layout()
        plt.savefig(report_path)
        plt.close()
        print(f"Analytics Generated: {report_path}")
