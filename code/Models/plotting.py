import pickle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
mpl.rcParams['xtick.labelsize'] = 12

def plot_hypopt():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    name = 'rf_cvresults'
    cv_res = pickle.load(open("hpopt/{}.p".format(name), "rb"))

    # Make data.
    X = [param['max_features'] for param in cv_res['params']]
    Y = [param['max_depth'] for param in cv_res['params']]
    # X, Y = np.meshgrid(X, Y)
    Z = -cv_res['mean_test_score']
    fig = plt.figure(1, figsize=(7, 5))
    ax = fig.gca(projection='3d')

    # Plot the surface.
    surf = ax.plot_trisurf(X, Y, Z, cmap=plt.cm.CMRmap)

    # Customize the z axis.
    fs = 15
    ax.set_xlabel('Max Features', fontsize=fs,)
    ax.set_ylabel('Max Depth', fontsize=fs)
    ax.set_zlabel('MAE', fontsize=fs, labelpad=10)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.00f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # plt.savefig("../../figures/{}.pdf".format(name))
    # plt.savefig("../../figures/{}.png".format(name))
    plt.show()

    return None


def plot_featimps():
    fi_data = np.loadtxt('featimp/featimps_uniq.txt', delimiter=',', dtype=str)

    feature_names = fi_data[:, 0]
    y_pos = np.arange(len(feature_names))
    names = ['Linear Regression', 'GBT', 'RF']
    for i, name in enumerate(names):
        fig = plt.figure(i)
        fis = map(float, fi_data[:, i+1])
        width = 0.8
        plt.bar(y_pos, fis, align='center', alpha=0.5, width=width)
        if i == 2:
            plt.xticks(y_pos, feature_names, rotation='vertical')
        else:
            plt.xticks(y_pos, [], rotation='vertical')
        plt.ylim(0, 1)
        plt.ylabel('Feature Importance', fontsize=12)
        plt.title('Feature importances - {}'.format(name))
        plt.show()


if __name__ == '__main__':
    # plot_hypopt()
    plot_featimps()