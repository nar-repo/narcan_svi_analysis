# Narcan Distribution and Social Vulnerability Index (SVI) Analysis in Minnesota

## Project Overview

This project analyzes the relationship between the availability of Narcan (naloxone) distribution sites and social vulnerability across census tracts in **Minnesota**. The Social Vulnerability Index (SVI), developed by the CDC/ATSDR, measures community vulnerability based on socioeconomic status, household composition, minority status, and housing/transportation.

The goal is to assess whether higher social vulnerability is associated with greater access to Narcan, a life-saving medication used to reverse opioid overdoses, **within the state of Minnesota**.

---

## Data Sources

- **Narcan Site Locations:** Distribution site data collected for Minnesota (JSON format from the public-facing map on KnowTheDangers.com’s Naloxone Finder).
- **Social Vulnerability Index (SVI):** CDC/ATSDR 2020 SVI data by census tract (CDC/ATSDR SVI 2022 (SVI2022) is based on data from the 2020 U.S. Census and American Community Survey 2016–2020 5-year estimates).
- **Census Tract Boundaries:** U.S. Census Bureau TIGER/Line shapefiles (census tract boundaries for the state of Minnesota based on the 2020 U.S. Census).

---

## Methods

1. Performed a geospatial join to link Minnesota-based Narcan sites with census tracts.
2. Calculated Narcan site availability rates per 1,000 residents (`narcan_per_1000`).
3. Applied a log transformation (`log(x + 1)`) to address skewness in Narcan distribution data.
4. Conducted statistical analysis including:
   - Pearson correlation between SVI and Narcan availability.
   - Ordinary Least Squares (OLS) regression modeling using overall SVI and individual SVI themes (`RPL_THEME1` to `RPL_THEME4`).

---

## Key Findings

- The correlation between overall SVI and Narcan availability was very weak and not statistically significant.
- The OLS regression model had very low explanatory power (R² = 0.006).
- Among the four SVI subthemes:
  - **Household Composition (RPL_THEME2)** was significantly and negatively associated with Narcan availability.
  - **Minority Status & Language (RPL_THEME3)** showed a significant positive association.
  - **Socioeconomic Status (RPL_THEME1)** and **Housing/Transportation (RPL_THEME4)** were not statistically significant.
- These results suggest that SVI alone is not a strong predictor of Narcan site distribution in Minnesota.

---

## Interpretation and Implications

The model highlights potential equity concerns:

- **Fewer Narcan sites** in tracts with high household vulnerability (e.g., elderly, disabled, single-parent households) could suggest underserved populations.
- **Greater access** in minority-dense areas might reflect targeted public health outreach or resource allocation in urban regions.

However, the weak model fit implies that **other factors**, such as opioid overdose prevalence, public health infrastructure, and policy interventions, may be stronger drivers of Narcan site distribution.

---

## Repository Structure

- `data/` - Raw and processed datasets.
- `scripts/` - Data preparation and analysis scripts (Python).
- `outputs/` -  a plot for visual analysis and a CSV file containing data suitable for various visualizations in PowerBI.
- `README.md` - Project overview and technical documentation.

---

## Skills Demonstrated

- Spatial data joining and geographic analysis (with GeoPandas and shapefiles)
- Regression modeling and diagnostics using `statsmodels`
- Data transformation and visualization
- Interpretation of weak models and clear communication of limitations
- Public health data analysis

---

