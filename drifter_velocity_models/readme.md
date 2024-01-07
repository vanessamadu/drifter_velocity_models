# Model Objects

## Model Attributes
- `loss_type` (str): The label of the loss function to be used (`rmse`,`rms_s_d`)
- `uncertainty_type` (str): The label of the uncertainty function to be used (`sre`, `sr_s_d`)
- `model_type` (str): The label for the type of model (`bathtub`,`sbr`,`fixedcurrent`,`lr`,`ngboost_pr`)
- `training_data` (DataFrame): Data used for training
- `test_data` (DataFrame): Data used for testing
- `trained_distribution` (array[`scipy.multivariate_normal`]): For Probabilistic Regression Models - Array of multivariate normal distributions with parameters specified from the training data according to the learned model for the probability distribution parameters.
- `test_distribution` (array[`scipy.multivariate_normal`]): For Probabilistic Regression Models - Array of multivariate normal distributions with parameters specified from the test data according to the learned model for the probability distribution parameters.

### Model Properties without Setters
These are properties that are designed not to be changed manually.
- `loss_function` (func): appropriate loss function according to `loss_type`.
- `uncertainty_function` (func): appropriate uncertainty function according to `uncertainty_type`.

## Model Instance Methods
- `loss`: returns the test or train loss as appropriate.

## Class Functions
- `to_degrees`: Converts angles from radians to degrees
- `to_cm_per_second`: Converts measurements with units m/s to cm/s
- `residuals`: Returns the residuals between an array of predictions and associated observations.

## Error Metrics
- RMSE (`rmse`): Root mean square error over every velocity component prediction made by the model: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2 (\mathbf{u}^{(i)}_j-\hat{\mathbf{u}}^{(i)}_j)^2}$$ where $\mathbf{u} = (u,v)$ is the predicted drifter velocity and $\hat{\mathbf{u}}$ is the observed drifter velocity. 
- RMS of Residual Speed and Residual Direction (`rms_residual_speed_and_direction`): Returns the root mean square (rms) of the speed and rms of the direction of the velocity residuals: $$\sqrt{\frac{1}{N} \sum_{i=1}^{N}\|u-\hat{u}\|^{2}}, \quad \sqrt{\frac{1}{N}\sum_{i=1}^N\left[\arctan{\frac{v-\hat{v}}{u-\hat{u}}}\right]^2}$$

### Uncertainty Quantification
- Standard Error of the Velocity Residuals (`standard_error_of_residuals`): Returns the standard deviation of the residuals: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2\left(\varepsilon^{(i)}_j-\bar{\varepsilon}_j\right)^2}$$
- Standard Deviation of the Residual Speed and Residual Direction (`std_residual_speed_and_direction`): Does what it says on the tin:
$$\sqrt{\frac{1}{N}\sum_{i=1}^N (\|\mathbf{\varepsilon}^{(i)}\|-\overline{\|{\mathbf{\varepsilon}} \|})^2},\quad \sqrt{\frac{1}{N}\sum_{i=1}^N (\|\mathbf{\theta_\varepsilon}^{(i)}\|-\overline{\|{\mathbf{\theta}} \|})^2}$$ where $\varepsilon$ is the matrix of $N$ velocity residuals, and $\theta_\varepsilon$ is the vector of angular residuals (deviations between predicted and observed direction).

# Model Sub-Types
## BathtubModel Objects
Benchmark Model - Predicts all velocities to be zero at all positions and for all times.
### BathtubModel Attributes
- Inherits all attributes and methods from the `Model` class.
- `model_type` is `'bathtub'`.
- `model_function` is defined by a static method, `bathtub`, where `bathtub(lon,lat) = [0,0]` for all longitudes and latitudes.

## SBRModel Objects
Benchmark Model: Predicts velocities according to a steady solid body rotation model: $\mathbf{u} = (-f_0 \text{lat}, f_0 \text{lon})$ where $f_0$ is the Coriolis parameter at $30^\circ \text{N}$.
### SBRModel Attributes
- Inherits all attributes and methods from the `Model` class.
- `model_type` is `'sbr'`.
- `f_0` (float) takes `7.27e-5` as default.
- `model_functiom` is defined by a static method, `sbr`, where `sbr(lon,lat) = [-f0*lat, f0*lon]`.

## FixedCurrentModel Objects
Benchmark Model: Predicts all drifter velocities to be the average velocity across the drifter data.
### FixedCurrentModel Attributes
- Inherits all attributes and methods from the `Model` class.
- `model_type` is `fixedcurrent`.
- `av_drifter_velocity` (array) initialised as `None` but populated with the average drifter velocity over all the (training) data.
- `model_function` is defined by a static method that returns the average drifter velocity which is passing into it via the `av_drifter_velocity` after it is initially calculated.

## LinearRegressionModel Objects
Predicts velocities according to a linear regression model.
### LinearRegressionModel Attributes
- Inherits all attributes and methods from the `Model` class.
- `model_type` is `'lr'`.
- `covariate_labels` (array): List of covariate labels to be used as model covariates.
- `param_estimate` (array): Least squares parameter estimate.
- `model_function` is defined by the static method `lr`. 
#### LinearRegressionModel Properties without Setters
These are properties that are designed not to be changed manually.
- `design` (array): Returns the design matrix associated with the training data.
### LinearRegressionModel (Instance) Methods
-`calculate_param_estimate` (func): Returns the least squares parameter estimate associated with the training data.

