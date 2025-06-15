import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from scipy.stats import pearsonr
import statsmodels.formula.api as smf
import statsmodels.api as sm 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt




#load Narcan site data
narcan_df = pd.read_csv(r"C:/Users/Nari/narcan_svi_analysis/data/raw/narcan_sites_mn.csv")

narcan_df = narcan_df.rename(columns={"latitude": "lat", "longitude": "lon"})

#drop rows without coordinates
narcan_df = narcan_df.dropna(subset=['lat', 'lon'])

#convert to GeoDataFrame
narcan_gdf = gpd.GeoDataFrame(
    narcan_df,
    geometry=gpd.points_from_xy(narcan_df['lon'], narcan_df['lat']),
    crs="EPSG:4326"
)

#load census tract shapefile for Minnesota
tracts_gdf = gpd.read_file(r"data/shapefiles/tl_2020_27_tract.shp")

#rename GEOID to FIPS for merging with svi file
tracts_gdf = tracts_gdf.rename(columns={"GEOID": "FIPS"})

#load SVI data
svi_df = pd.read_csv(r"data/raw/minnesota_svi_2022.csv")


#convert both to string before merge
tracts_gdf['FIPS'] = tracts_gdf['FIPS'].astype(str)
svi_df['FIPS'] = svi_df['FIPS'].astype(str)

svi_df = svi_df.rename(columns={'RPL_THEMES': 'SVI'})
#merge SVI into census tracts GeoDataFrame
tracts_gdf = tracts_gdf.merge(
    svi_df[['FIPS', 'SVI', 'E_TOTPOP', 'RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']],
    on='FIPS',
    how='left'
)

#spatial join Narcan points to tracts
narcan_gdf = narcan_gdf.to_crs(tracts_gdf.crs)

narcan_tracts = gpd.sjoin(narcan_gdf, tracts_gdf, how="left", predicate='within')

#count how many Narcan sites are in each census tract
narcan_counts = narcan_tracts.groupby('FIPS').size().reset_index(name='narcan_site_count')

#merge counts into tracts data, now shape file has narcan site counts for each tract
tracts_gdf = tracts_gdf.merge(narcan_counts, on='FIPS', how='left')

#fill NaN values with 0 for tracts with no Narcan sites
tracts_gdf['narcan_site_count'] = tracts_gdf['narcan_site_count'].fillna(0)

#calculate Narcan sites per 1000 residents
#tracts_gdf['narcan_per_1000'] = tracts_gdf['narcan_site_count'] / tracts_gdf['E_TOTPOP'] * 1000
tracts_gdf['narcan_per_1000'] = tracts_gdf['narcan_site_count'] / tracts_gdf['E_TOTPOP'].replace(0, np.nan) * 1000
#log transformation
tracts_gdf['narcan_per_1000_log'] = np.log1p(tracts_gdf['narcan_per_1000'])

#drop rows with missing or infinite values in required columns
filtered = tracts_gdf[['SVI', 'narcan_per_1000_log']].replace([np.inf, -np.inf], np.nan).dropna()


tracts_gdf = tracts_gdf.replace([np.inf, -np.inf], np.nan).dropna(subset=['narcan_per_1000_log', 'RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4'])

# Prepare independent variables
X = tracts_gdf[['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']]
X = sm.add_constant(X)  # add intercept
y = tracts_gdf['narcan_per_1000_log']

#fit model
model = sm.OLS(y, X).fit()

#output results
print(model.summary())

#extract coefficients and confidence intervals
coefs = model.params
conf = model.conf_int()
conf.columns = ['lower_bound', 'upper_bound']
conf['coef'] = coefs
conf = conf.reset_index()
conf = conf.rename(columns={'index': 'Variable'})

#remove intercept (optional)
conf = conf[conf['Variable'] != 'const']

#plot
plt.figure(figsize=(8, 6))
sns.pointplot(data=conf, x='coef', y='Variable', join=False, color='black')
plt.errorbar(conf['coef'], conf['Variable'], 
             xerr=[conf['coef'] - conf['lower_bound'], conf['upper_bound'] - conf['coef']], 
             fmt='o', color='black', capsize=4)

plt.axvline(0, color='gray', linestyle='--')
plt.title('Regression Coefficients: Predicting Narcan Access')
plt.xlabel('Coefficient Estimate (Log Narcan Sites per 1000 Residents)')
plt.ylabel('SVI Component')
plt.grid(True)
plt.tight_layout()

plt.savefig(r"C:/Users/Nari/narcan_svi_analysis/outputs/ols_coefficients_plot.png", dpi=300)
plt.show()
