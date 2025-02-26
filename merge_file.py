import pandas as pd
import os

# Thư mục chứa các file CSV
csv_folder = "data/k59"
output_file = "merged_data_k59.csv"

csv_files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]

df_list = [pd.read_csv(os.path.join(csv_folder, file), delimiter=';') for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv(output_file, index=False, sep=';')

print(f"✅ Gộp {len(csv_files)} file CSV thành công vào {output_file}")
