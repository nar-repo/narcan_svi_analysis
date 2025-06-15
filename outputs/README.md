
## Plot Description  

The plot shows **regression coefficients and 95% confidence intervals** from an ordinary least squares (OLS) model predicting Narcan access using Social Vulnerability Index (SVI) components.  

- **X-axis:** Coefficient estimates from the OLS model. These represent how much each SVI component is associated with the log of Narcan sites per 1,000 residents.  
- **Y-axis:** Predictor variables (SVI components):
  - `RPL_THEME1`: Socioeconomic status  
  - `RPL_THEME2`: Household composition & disability  
  - `RPL_THEME3`: Minority status & language  
  - `RPL_THEME4`: Housing type & transportation  

- **Black dots:** Point estimates of the regression coefficients (β values).  
- **Horizontal lines (error bars):** 95% confidence intervals for each coefficient.  
- **Vertical dashed line at 0:** Represents no effect. If the confidence interval crosses this line, the variable’s effect is not statistically significant at the 95% level.  

---

**Interpretation:**  
- None of the SVI components show a statistically significant association with Narcan site access, as all confidence intervals cross zero.  
- The plot visually highlights the uncertainty around these estimates.
