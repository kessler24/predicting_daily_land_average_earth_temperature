## [1.1.0] - 2025-12-12
### Feedback Addressed by Ojasv
- Updated QMD file to address reviewer feedback regarding model evaluation and documentation.
- Explicitly documented hyperparameters for SVR (`C=100`, `gamma=0.1`, `epsilon=0.01`) and Random Forest (`n_estimators=200`).
- Clarified the rationale for including R² as an error metric and added explanation of negative R² values.
- Expanded the modeling section to include kernel choice for SVR, model configurations, and whether defaults or tuned hyperparameters were used.
- Added discussion of model limitations, including extrapolation risks, assumptions about trend continuation, and the limitation of using only year as a feature.
