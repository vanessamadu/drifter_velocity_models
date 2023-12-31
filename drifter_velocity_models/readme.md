# Model Class

## Class Functions
- Residuals: Returns the residuals between an array of predictions and associated observations.

## Loss Functions
- RMSE: Root mean square error over every velocity component prediction made by the model: $$\sqrt{\frac{1}{2N}\sum_{i=1}^N\sum_{j=1}^2 (\mathbf{u}^{(j)}-\hat{\mathbf{u}^{(j)}})^2}$$ where $\mathbf{u} = (u,v)$ is the predicted drifter velocity and $\hat{\mathbf{u}}$ is the observed drifter velocity. 