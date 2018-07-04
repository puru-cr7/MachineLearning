'''
Created on Jul 3, 2018

@author: Purnendu Rath (puru_cr7)
'''

from matplotlib import rc 
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

from bayesianoptimisation.bsopti import bayesian_optimisation 
from bayesianoptimisation.plotters import plot_iteration 
import numpy as np


def sample_loss(params):
    val = cross_val_score(SVC(C=10 ** params[0], gamma=10 ** params[1], random_state=12345),
                           X=data, y=target, scoring='roc_auc', cv=3).mean()
    print(params)
    print(val)
    return val


data, target = make_classification(n_samples=2500,
                                   n_features=45,
                                   n_informative=15,
                                   n_redundant=5)
  
lambdas = np.linspace(1, -4, 25)
gammas = np.linspace(1, -4, 20)
# # We need the cartesian combination of these two vectors
# param_grid = np.array([[C, gamma] for gamma in gammas for C in lambdas])
# real_loss = [sample_loss(params) for params in param_grid]
# # The maximum is at:
# param_grid[np.array(real_loss).argmax(), :]
# rc('text', usetex=True)
#  
# C, G = np.meshgrid(lambdas, gammas)
#  
# plt.figure()
# cp = plt.contourf(C, G, np.array(real_loss).reshape(C.shape))
# plt.colorbar(cp)
#  
# plt.title('Filled contours plot of loss function $\mathcal{L}$($\gamma$, $C$)')
# plt.xlabel('$C$')
# plt.ylabel('$\gamma')
#  
# # plt.savefig('/Users/thomashuijskens/Personal/bsopti-optimisation/figures/real_loss_contour.png', bbox_inches='tight')
# plt.show()

bounds = np.array([[-4, 1], [-4, 1]])

xp, yp = bayesian_optimisation(n_iters=20,
                               sample_loss=sample_loss,
                               bounds=bounds,
                               n_pre_samples=1,
                               random_search=100000)
indx = np.argmax(yp)
print()
print('Best score found is ', yp[indx])
print('Best settings are found are ', xp[indx])

rc('text', usetex=False)
plot_iteration(lambdas, xp, yp, first_iter=0, second_param_grid=gammas, optimum=[0.58333333, -2.15789474], filepath='../results/bayesianoptimisation')

