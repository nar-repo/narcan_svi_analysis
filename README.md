# Narcan Distribution and Social Vulnerability Index (SVI) Analysis

## Project Overview

This project analyzes the relationship between the availability of Narcan (naloxone) distribution sites and social vulnerability across U.S. census tracts. The Social Vulnerability Index (SVI), developed by the CDC/ATSDR, measures community vulnerability based on socioeconomic status, household composition, minority status, and housing/transportation.

The goal is to assess whether higher social vulnerability is associated with greater access to Narcan, a life-saving medication used to reverse opioid overdoses.

---

## Data Sources

- **Narcan Site Locations:** Data on Narcan distribution sites (source details to be added).
- **Social Vulnerability Index (SVI):** CDC/ATSDR SVI data by census tract.
- **Census Tract Boundaries:** US Census Bureau TIGER/Line shapefiles.

---

## Methods

1. Performed a geospatial join to link Narcan sites with census tracts.
2. Calculated Narcan site availability rates per 1,000 residents (`narcan_per_1000`).
3. Applied a log transformation (log(x + 1)) to address skewness in Narcan distribution data.
4. Conducted statistical analysis including:
   - Pearson correlation between SVI and Narcan availability.
   - Ordinary Least Squares (OLS) regression modeling with overall SVI and individual SVI themes (`RPL_THEME1` to `RPL_THEME4`).

---

## Key Findings

- The correlation between overall SVI and Narcan availability was very weak and not statistically significant.
- The OLS regression model showed very low explanatory power (R² = 0.006).
- Among SVI themes:
  - **Household Composition (RPL_THEME2)** was negatively associated with Narcan availability.
  - **Minority Status & Language (RPL_THEME3)** showed a positive association.
  - Other themes were not significant predictors.
- These results suggest that social vulnerability alone does not strongly predict Narcan site distribution.

---

## Model Limitations

- **Residual Distribution Issues:** The model residuals exhibit severe positive skewness (Skew = 12.38) and high kurtosis (178.79), indicating non-normality and presence of extreme outliers.
- **Autocorrelation:** Durbin-Watson statistic (1.275) signals positive autocorrelation, violating the independence assumption.
- **Multicollinearity:** Condition number (409) suggests multicollinearity among predictors, weakening individual coefficient reliability.
- **Data Constraints:** Narcan site data may be incomplete or outdated, and this analysis does not account for overdose rates or other contextual factors.

Because of these issues, statistical significance should be interpreted cautiously, and the model’s practical utility is limited.

---

## Interpretation and Implications

The findings highlight potential gaps in Narcan access, especially in areas with vulnerable household compositions (e.g., elderly, disabled, single-parent families). Conversely, minority-dense areas may receive relatively more Narcan resources, possibly due to targeted public health efforts.

However, the weak model fit and assumption violations suggest that other factors, such as local policies, overdose prevalence, or outreach programs, likely play a larger role in Narcan distribution patterns.

---

## Next Steps

- Incorporate spatial modeling techniques to address spatial autocorrelation (e.g., Moran’s I, Geographically Weighted Regression).
- Explore additional variables such as overdose rates, emergency medical service data, and policy indicators.
- Investigate temporal trends and longitudinal changes in Narcan distribution.
- Use non-linear or machine learning models to capture complex relationships.

---

## Repository Structure

- `data/` — Raw and processed datasets.
- `scripts/` — Data processing and analysis SQL scripts and Python notebooks.
- `outputs/` — Tables, charts, and model results.
- `README.md` — Project overview and documentation.

---

## Skills Demonstrated

- Geospatial data integration and analysis
- Statistical modeling and regression diagnostics
- Handling of skewed and non-normal data distributions
- Critical interpretation of model limitations
- Data storytelling and reporting

---

## Contact

For questions or collaboration, please contact [Your Name] at [your email].

---

*This project was completed as part of a data analysis portfolio to demonstrate applied skills in SQL, Python, spatial analysis, and statistical modeling.*
