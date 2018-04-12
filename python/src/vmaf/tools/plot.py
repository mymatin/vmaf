from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm, gamma

__copyright__ = "Copyright 2016-2018, Netflix, Inc."
__license__ = "Apache, Version 2.0"


def get_cdf(x, num_bins=100):
    x = np.array(x)
    counts, bin_edges = np.histogram(x, bins=num_bins)
    cdf = np.cumsum(counts)
    cdf = cdf / float(cdf[-1]) # normalize
    bin_edges = bin_edges[1:] # make size
    return cdf, bin_edges


def get_pdf(data, num_bins=20):
    pdf, bin_edges = np.histogram(data, density=True, bins=num_bins)
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2
    return pdf, bin_centres


def plot_distribution(plot_type, df, key, slice_name, slices, colors=None, ax=None):
    if colors is None:
        colors = [None for _ in slices]
    for slice, color in zip(slices, colors):
        if isinstance(slice, (list, tuple)):
            data = df.loc[df[slice_name].isin(slice)][key].tolist()
        else:
            data = df.loc[df[slice_name] == slice][key].tolist()
        if plot_type == 'cdf':
            ys, xs = get_cdf(data)
            plt.ylabel('CDF')
        elif plot_type == 'pdf':
            ys, xs = get_pdf(data)
            plt.ylabel('PDF')
        else:
            assert False, "Unknown plot type: {}".format(plot_type)
        if ax:
            ax.plot(xs, ys, label="{}".format(str(slice)), color=color)
            ax.grid(which='major')
        else:
            plt.plot(xs, ys, label="{}".format(str(slice)), color=color)
            plt.grid(which='major')

def plot_distribution_fit(plot_type, df, key, slice_name, slices, colors=None, ax=None, distribution_type='gamma', collate_data=True):

    if colors is None:
        colors = [None for _ in slices]
    if collate_data:
        data = []
        for slice in slices:
            if isinstance(slice, (list, tuple)):
                data += df.loc[df[slice_name].isin(slice)][key].tolist()
            else:
                data += df.loc[df[slice_name] == slice][key].tolist()
        _plot_distribution_fit(ax, data, distribution_type, plot_type, "", colors[0])

    else:
        for slice, color in zip(slices, colors):
            if isinstance(slice, (list, tuple)):
                data = df.loc[df[slice_name].isin(slice)][key].tolist()
            else:
                data = df.loc[df[slice_name] == slice][key].tolist()
            _plot_distribution_fit(ax, data, distribution_type, plot_type, slice, color)


def _plot_distribution_fit(ax, data, distribution_type, plot_type, tag, color):

    if distribution_type == 'norm':
        distribution_fcn = norm
    elif distribution_type == 'gamma':
        distribution_fcn = gamma
    else:
        assert False, 'Currently only support norm and gamma distribution fit.'

    xmin = min(data)
    xmax = max(data)
    xs = np.linspace(xmin, xmax)

    params = distribution_fcn.fit(data)
    if plot_type == 'cdf':
        ys = distribution_fcn.cdf(xs, *params)
        plt.ylabel('CDF')
    elif plot_type == 'pdf':
        ys = distribution_fcn.pdf(xs, *params)
        plt.ylabel('PDF')
    else:
        assert False, "Unknown plot type: {}".format(plot_type)
    label = "{tag} {dis_name} fit {param}".format(
        tag=tag, dis_name=distribution_fcn.name,
        param=', '.join(map(lambda p: "{:.4f}".format(p), params)))

    if ax:
        ax.plot(xs, ys, label=label, color=color)
        ax.grid(which='major')
    else:
        plt.plot(xs, ys, label=label, color=color)
        plt.grid(which='major')
