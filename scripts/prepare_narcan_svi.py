import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from scipy.stats import pearsonr
import statsmodels.formula.api as smf
import statsmodels.api as sm 
import numpy as np




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
tracts_gdf = tracts_gdf.merge(svi_df[['FIPS', 'SVI', 'E_TOTPOP']], on='FIPS')


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
tracts_gdf['narcan_per_1000_log'] = np.log1p(tracts_gdf['narcan_per_1000'])

# Drop rows with missing or infinite values in required columns
filtered = tracts_gdf[['SVI', 'narcan_per_1000_log']].replace([np.inf, -np.inf], np.nan).dropna()



#avoid division by zero
tracts_gdf.loc[tracts_gdf['E_TOTPOP'] == 0, 'narcan_per_1000'] = 0


#Pearson correlation 
#r, p = pearsonr(tracts_gdf['SVI'], tracts_gdf['narcan_per_1000'])
r, p = pearsonr(filtered['SVI'], filtered['narcan_per_1000_log'])
print(f"Pearson correlation: r = {r:.2f}, p-value = {p:.4f}")

 #OLS linear regression analysis as Narcan acess as the dependent variable and
 #SVI as the independent variable
X = sm.add_constant(tracts_gdf['SVI']) 
y = tracts_gdf['narcan_per_1000'] 
#model = sm.OLS(y, X).fit()
#model = smf.ols('narcan_per_1000_log ~ SVI', data=filtered).fit()
print(model.summary())
print(f"Using {len(filtered)} rows after dropping NaNs/infs.")

#export cleaned data for Power BI
#tracts_gdf[['FIPS', 'SVI', 'narcan_site_count', 'narcan_per_1000']].to_csv("data/processed/mn_svi_narcan.csv", index=False)
