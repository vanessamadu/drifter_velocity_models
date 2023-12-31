# Model Class

## Class Functions
- Residuals: Returns the residuals between an array of predictions and associated observations.

## Error Metrics
- RMSE: Root mean square error over every velocity component prediction made by the model: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2 (\mathbf{u}^{(i)}_j-\hat{\mathbf{u}}^{(i)}_j)^2}$$ where $\mathbf{u} = (u,v)$ is the predicted drifter velocity and $\hat{\mathbf{u}}$ is the observed drifter velocity. 
- RMS of Residual Speed and Residual Direction: Returns the root mean square (rms) of the speed and rms of the direction of the velocity residuals: $$\sqrt{\frac{1}{N} \sum_{i=1}^{N}\|u-u\|^{2}}, \quad \sqrt{\frac{1}{N}\sum_{i=1}^N\left[\arctan{\frac{v}{u}}\right]^2}$$

### Uncertainty Quantification
- Standard Error of the Velocity Residuals: Returns the standard deviation of the residuals: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2\left(\varepsilon^{(i)}_j-\bar{\varepsilon}_j\right)^2}$$