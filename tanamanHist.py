import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math as math
from scipy.stats import gaussian_kde

# Sesuaikan dengan lokasi file 
file_path = "Produksi Tanaman Biofarmaka Menurut Jenis Tanaman di Provinsi DKI Jakarta, 2024.csv"

data = pd.read_csv(file_path)

data.columns = ['Tanaman', 'Produksi']

data = data.dropna(subset=['Tanaman', 'Produksi'])
data = data[~data['Tanaman'].str.contains('Catatan', case=False, na=False)]
data = data[~data['Tanaman'].str.contains('Angka', case=False, na=False)]
data['Produksi'] = pd.to_numeric(data['Produksi'], errors='coerce')
data = data.dropna(subset=['Produksi'])

values = data['Produksi'].to_numpy()

bins = np.arange(0, 6000, 500)

mean_produksi = data['Produksi'].mean()
median_produksi = data['Produksi'].median()
modus_produksi = data['Produksi'].mode()[0]
variance_produksi = data['Produksi'].var(ddof=0)
stddeviasi_produksi = math.sqrt(variance_produksi)

print(f"Mean   : {mean_produksi:.2f}")
print(f"Median : {median_produksi:.2f}")
print(f"Modus  : {modus_produksi}")
print(f"Variance : {variance_produksi:.2f}")
print(f"Standar Deviasi : {stddeviasi_produksi:.2f}")

plt.hist(values, bins=bins, color='lightyellow', edgecolor='black')

counts, bin_edges = np.histogram(values, bins=bins)

kde = gaussian_kde(values)
bin_width = bins[1] - bins[0]
x_grid = np.linspace(min(values), max(values), 1000)
kde_density = kde(x_grid)

kde_frequency = kde_density * len(values) * bin_width

max_hist_height = np.max(counts)

max_kde_height = np.max(kde_frequency)

if max_kde_height > 0:
    scale_factor = max_hist_height / max_kde_height
    kde_frequency_scaled = kde_frequency * scale_factor
else:
    kde_frequency_scaled = kde_frequency

plt.plot(x_grid, kde_frequency_scaled, color="blue", linewidth=2, label="Kurva (KDE)")


plt.axvline(mean_produksi, color='red', linestyle='--', label='Mean')
plt.axvline(median_produksi, color='green', linestyle='--', label='Median')
plt.axvline(modus_produksi, color='orange', linestyle='--', label='Mode')

plt.title("Distribusi Produksi Tanaman Biofarmaka DKI Jakarta (2024)")
plt.xlabel("Produksi (kg)")
plt.ylabel("Frekuensi")

plt.xticks(np.arange(0, values.max() + 1000, 1000))
plt.tick_params(axis='x', rotation=45)
plt.legend()
plt.show()
