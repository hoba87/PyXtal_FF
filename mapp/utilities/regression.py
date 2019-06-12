import sys
sys.path.append("..")

from models.model import LossFunction

class gRegressor:
    """This class consists of global optimization methods.

    Parameters
    ----------
    method: str
        Type of optimization scheme.
    user_kwargs: dict
        Keywords for the optimization scheme.
    """
    def __init__(self, method='DifferentialEvolution', user_kwargs=None):
        if method == 'DifferentialEvolution':
            from scipy.optimize import differential_evolution as optimizer
            kwargs = {'strategy': 'best1bin',
                      'maxiter': 1000,
                      'popsize': 30,
                      'tol': 0.0001}
        elif method == 'BasinHopping':
            from scipy.optimize import basinhopping as optimizer
            kwargs = {'niter': 100,
                      'T': 1.0}
        else:
            msg = "The method is not implemented yet."
            raise NotImplementedError(msg)

        if user_kwargs is not None:
            kwargs.update(user_kwargs)
        
        self.optimizer = optimizer
        self.kwargs = kwargs


    def regress(self, model, bounds):
        """Run the optimization scheme here.
        
        Parameters
        ----------
        model: class
            Class representing the machine learning model.
        bounds: List of tuples
            The tuples describe the min and max values for the global 
            searching algorithm.
        
        Returns
        -------
        List
            List of the optimized parameters and loss value.
        """
        self.bounds = bounds
        
        f = LossFunction(model)
        regression = self.optimizer(f.glossfunction, self.bounds, **self.kwargs)

        return [regression.x, regression.fun]


class lRegressor:
    """This class contains local optimization methods.

    Parameters
    ----------
    method: str
        Type of minimization scheme, e.g.: 'BFGS'.
    user_kwargs: dict
        The arguments of the optimization function are passed by the dict 
        keywords.
    """
    def __init__(self, method='BFGS', user_kwargs=None):
        if method == 'BFGS':
            from scipy.optimize import minimize as optimizer
            kwargs = {'method': 'BFGS',
                      'options': {'gtol': 1e-15, }}
        else:
            msg = "The method is not implemented yet."
            raise NotImplementedError(msg)
        
        if user_kwargs is not None:
            kwargs.update(user_kwargs)

        self.optimizer = optimizer
        self.kwargs = kwargs


    def regress(self, model):
        """
        Run the optimization scheme here.

        Parameters
        ----------
        model: object
            Class representing the regression model.

        Returns
        -------
        List
            List of the optimized parameters and loss value.
        """
        self.kwargs.update({'jac': True,
                            'args': (True,)})

        parameters0 = model.vector.copy()
        
        f = LossFunction(model)
        regression = self.optimizer(f.llossfunction, parameters0, **self.kwargs)

        return [regression.x, regression.fun]
