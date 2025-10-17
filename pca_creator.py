import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
import os
from adjustText import adjust_text

# Load Data and Metadata

sample_names = [
    '22307_Enteropogon_ramosus',
    '22336_Triodia_basedowii',
    '22339_Triodia_melvillei',
    '22343_Triodia_longiceps',
    '22346_Triodia_brizoides',
    '22349_Triodia_wiseana',
    '33696_Triodia_sp',
    '33709_Triodia_wiseana',
    '33740_Triodia_brizoides',
    '33757_Triodia_sp',
    '33763_Triodia_longiceps'
]

# Load the genotype data from your local file.
genotype_data_path = 'pca_genotypes.tsv'
if not os.path.exists(genotype_data_path):
    print(f"ERROR: The file '{genotype_data_path}' was not found in this directory.")
    exit()

genotype_df = pd.read_csv(genotype_data_path, header=None, sep='\t')

if genotype_df.shape[1] > len(sample_names):
    genotype_df = genotype_df.iloc[:, :-1]

# Transpose the DataFrame so that samples are rows and SNPs are columns
genotype_df = genotype_df.T
genotype_df.columns = [f'SNP_{i+1}' for i in range(genotype_df.shape[1])]
genotype_df['Sample_ID'] = sample_names

# Prepare Data for PCA

# Extract species name from the Sample_ID to color the plot
genotype_df['Species'] = genotype_df['Sample_ID'].apply(lambda x: '_'.join(x.split('_')[1:]))

# Handle non-numeric values and fill missing data with the mode
features = genotype_df.drop(['Sample_ID', 'Species'], axis=1)
features = features.apply(pd.to_numeric, errors='coerce')
features = features.fillna(features.mode().iloc[0])

metadata = genotype_df[['Sample_ID', 'Species']]

# Perform PCA

pca = PCA(n_components=2)
principal_components = pca.fit_transform(features)
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
pc1_variance = pca.explained_variance_ratio_[0] * 100
pc2_variance = pca.explained_variance_ratio_[1] * 100
final_df = pd.concat([pca_df, metadata.reset_index(drop=True)], axis=1)


plt.figure(figsize=(14, 10))
sns.set_style("whitegrid")

# Define unique markers (shapes) for each species
unique_species = final_df['Species'].unique()
markers = ['o', 's', '^', 'D', 'P', 'X', '*']
species_marker_map = dict(zip(unique_species, markers[:len(unique_species)]))

# Create the plot by iterating through each species to assign unique markers
for species, group in final_df.groupby('Species'):
    plt.scatter(
        group['PC1'],
        group['PC2'],
        s=200,
        alpha=0.8,
        edgecolor='black',
        marker=species_marker_map.get(species, 'o'),
        label=species
    )
    
    
    if len(group) > 2:
        sns.kdeplot(
            data=group,
            x='PC1',
            y='PC2',
            alpha=0.5,
            fill=True
        )


texts = []
for i, row in final_df.iterrows():
    label_id = row['Sample_ID'].split('_')[0]
    texts.append(plt.text(row['PC1'], row['PC2'], label_id, fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="-", color='black', lw=0.5))


plt.title('PCA of Triodia Chloroplast SNPs', fontsize=18)
plt.xlabel(f'Principal Component 1 ({pc1_variance:.2f}%)', fontsize=14)
plt.ylabel(f'Principal Component 2 ({pc2_variance:.2f}%)', fontsize=14)
plt.legend(title='Species', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.tight_layout()
plt.savefig('triodia_pca_plot_final.png', dpi=300, bbox_inches='tight')

print("Success! Final PCA plot saved as 'triodia_pca_plot_final.png'")