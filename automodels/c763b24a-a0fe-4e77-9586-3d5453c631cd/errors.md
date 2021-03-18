## Error for 3_Linear

Input contains NaN, infinity or a value too large for dtype('float64').
Traceback (most recent call last):
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/base_automl.py", line 970, in _fit
    trained = self.train_model(params)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/base_automl.py", line 309, in train_model
    mf.train(model_path)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/model_framework.py", line 186, in train
    self.callbacks.on_iteration_end(
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/callbacks/callback_list.py", line 23, in on_iteration_end
    cb.on_iteration_end(logs, predictions)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/callbacks/early_stopping.py", line 103, in on_iteration_end
    validation_loss = self.metric(
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/utils/metric.py", line 79, in __call__
    return self.metric(y_true, y_predicted, sample_weight=sample_weight)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/supervised/utils/metric.py", line 30, in rmse
    val = mean_squared_error(y_true, y_predicted, sample_weight=sample_weight)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/sklearn/utils/validation.py", line 63, in inner_f
    return f(*args, **kwargs)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/sklearn/metrics/_regression.py", line 335, in mean_squared_error
    y_type, y_true, y_pred, multioutput = _check_reg_targets(
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/sklearn/metrics/_regression.py", line 90, in _check_reg_targets
    y_pred = check_array(y_pred, ensure_2d=False, dtype=dtype)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/sklearn/utils/validation.py", line 63, in inner_f
    return f(*args, **kwargs)
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/sklearn/utils/validation.py", line 663, in check_array
    _assert_all_finite(array,
  File "/home/giulia/anaconda3/envs/mljar_models/lib/python3.8/site-packages/sklearn/utils/validation.py", line 103, in _assert_all_finite
    raise ValueError(
ValueError: Input contains NaN, infinity or a value too large for dtype('float64').


Please set a GitHub issue with above error message at: https://github.com/mljar/mljar-supervised/issues/new

