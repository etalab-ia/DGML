# Summary of Ensemble

[<< Go back](../README.md)


## Ensemble structure
| Model                   |   Weight |
|:------------------------|---------:|
| 2_DecisionTree          |        1 |
| 4_Default_Xgboost       |        2 |
| 5_Default_NeuralNetwork |        1 |
| 6_Default_RandomForest  |        1 |

### Metric details
|           |         0 |     1 |         2 |         3 |         4 |   accuracy |   macro avg |   weighted avg |   logloss |
|:----------|----------:|------:|----------:|----------:|----------:|-----------:|------------:|---------------:|----------:|
| precision |  0.904762 |  0.48 |  0.607143 |  0.459459 |  0.555556 |   0.605714 |    0.601384 |       0.617634 |  0.758586 |
| recall    |  0.808511 |  0.48 |  0.586207 |  0.5      |  0.666667 |   0.605714 |    0.608277 |       0.605714 |  0.758586 |
| f1-score  |  0.853933 |  0.48 |  0.596491 |  0.478873 |  0.606061 |   0.605714 |    0.603072 |       0.610318 |  0.758586 |
| support   | 47        | 50    | 29        | 34        | 15        |   0.605714 |  175        |     175        |  0.758586 |


## Confusion matrix
|              |   Predicted as 0 |   Predicted as 1 |   Predicted as 2 |   Predicted as 3 |   Predicted as 4 |
|:-------------|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|
| Labeled as 0 |               38 |                4 |                0 |                5 |                0 |
| Labeled as 1 |                0 |               24 |                3 |               15 |                8 |
| Labeled as 2 |                3 |                9 |               17 |                0 |                0 |
| Labeled as 3 |                0 |                9 |                8 |               17 |                0 |
| Labeled as 4 |                1 |                4 |                0 |                0 |               10 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
