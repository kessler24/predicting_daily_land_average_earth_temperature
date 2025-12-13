## [1.1.0] - 2025-12-12
### Feedback Addressed by Ojasv
- Updated QMD file to address reviewer feedback regarding model evaluation and documentation.
- Explicitly documented hyperparameters for SVR (`C=100`, `gamma=0.1`, `epsilon=0.01`) and Random Forest (`n_estimators=200`).
- Clarified the rationale for including R² as an error metric and added explanation of negative R² values.
- Expanded the modeling section to include kernel choice for SVR, model configurations, and whether defaults or tuned hyperparameters were used.
- Added discussion of model limitations, including extrapolation risks, assumptions about trend continuation, and the limitation of using only year as a feature.

### Feedback Addressed by Jacob
- Original Issues Raised: https://github.com/UBC-MDS/data-analysis-review-2025/issues/18#issuecomment-3634810044 https://github.com/UBC-MDS/data-analysis-review-2025/issues/18#issuecomment-3639818869
- Relevant commits of changes: https://github.com/kessler24/predicting_daily_land_average_earth_temperature/commit/3f5f3ee7ab927a93a3b3a44ff5e07a91b111f3cb https://github.com/kessler24/predicting_daily_land_average_earth_temperature/commit/3f5f3ee7ab927a93a3b3a44ff5e07a91b111f3cb
- Fixed the filename outputs and handling for the abstract_eda.py script and added error handling for defensive programming.
- Added informative filename suffixes indicating the type of plot and and table while giving the user the ability to choose the filename prefix
- Update .qmd to reflect new naming convention compatible with Makefile and full analysis

### Feedback Addressed by Daisy
- Original Issues Raised: https://github.com/UBC-MDS/data-analysis-review-2025/issues/18#issuecomment-3639818869
- Relevant commits of changes: https://github.com/kessler24/predicting_daily_land_average_earth_temperature/commit/74a8d950760c43601a3febf40e8415c6be921912
- Addressed limitations of the model with only year, month and day as the feature and implementation beyond the dataset for a further future.

- Original Issues Raised: https://github.com/UBC-MDS/data-analysis-review-2025/issues/18#issuecomment-3634618262
- Relevant commits of changes: https://github.com/kessler24/predicting_daily_land_average_earth_temperature/commit/31bb74cfeba108f9b13f7e4fe9f30a1f9ee53cfa
- Changed script name for better naming conventions
