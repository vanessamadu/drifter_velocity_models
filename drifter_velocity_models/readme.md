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
- Residuals: Returns the residuals between an array of predictions and associated observations.

## Error Metrics
- RMSE: Root mean square error over every velocity component prediction made by the model: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2 (\mathbf{u}^{(i)}_j-\hat{\mathbf{u}}^{(i)}_j)^2}$$ where $\mathbf{u} = (u,v)$ is the predicted drifter velocity and $\hat{\mathbf{u}}$ is the observed drifter velocity. 
- RMS of Residual Speed and Residual Direction: Returns the root mean square (rms) of the speed and rms of the direction of the velocity residuals: $$\sqrt{\frac{1}{N} \sum_{i=1}^{N}\|u-\hat{u}\|^{2}}, \quad \sqrt{\frac{1}{N}\sum_{i=1}^N\left[\arctan{\frac{v-\hat{v}}{u-\hat{u}}}\right]^2}$$

### Uncertainty Quantification
- Standard Error of the Velocity Residuals: Returns the standard deviation of the residuals: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2\left(\varepsilon^{(i)}_j-\bar{\varepsilon}_j\right)^2}$$
- Standard Deviation of the Residual Speed and Residual Direction: Does what it says on the tin:
$$\sqrt{\frac{1}{N}\sum_{i=1}^N (\|\mathbf{\varepsilon}^{(i)}\|-\overline{\|{\mathbf{\varepsilon}} \|})^2},\quad \sqrt{\frac{1}{N}\sum_{i=1}^N (\|\mathbf{\theta_\varepsilon}^{(i)}\|-\overline{\|{\mathbf{\theta}} \|})^2}$$ where $\varepsilon$ is the matrix of $N$ velocity residuals, and $\theta_\varepsilon$ is the vector of angular residuals (deviations between predicted and observed direction).