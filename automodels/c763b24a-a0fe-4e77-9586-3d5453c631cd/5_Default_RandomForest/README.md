# Summary of 5_Default_RandomForest

[<< Go back](../README.md)


## Random Forest
- **criterion**: mse
- **max_features**: 0.9
- **min_samples_split**: 30
- **max_depth**: 4
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True

## Optimized metric
rmse

## Training time

7.0 seconds

### Metric details:
| Metric   |    Score |
|:---------|---------:|
| MAE      | 0.288797 |
| MSE      | 0.150648 |
| RMSE     | 0.388133 |
| R2       | 0.442504 |



## Learning curves
![Learning curves](learning_curves.png)

## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)

## SHAP Importance
![SHAP Importance](shap_importance.png)

## SHAP Dependence plots

### Dependence (Fold 1)
![SHAP Dependence from Fold 1](learner_fold_0_shap_dependence.png)

## SHAP Decision plots

### Top-10 Worst decisions (Fold 1)
![SHAP worst decisions from fold 1](learner_fold_0_shap_worst_decisions.png)
### Top-10 Best decisions (Fold 1)
![SHAP best decisions from fold 1](learner_fold_0_shap_best_decisions.png)

[<< Go back](../README.md)
