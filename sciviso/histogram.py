###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import norm

from sciviso import Vis


class Histogram(Vis):

    def __init__(self, df: pd.DataFrame, x: object, title='', xlabel='', ylabel='', colour=None, normalise=False, fit_norm=False,
                 plot_rug=False, plot_kde=False, plot_hist=True, bins=20, min_x=None, max_x=None, min_y=None, max_y=None,
                 figsize=(3, 3), title_font_size=12, label_font_size=8, title_font_weight=700, config={}):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)
        self.df = df
        self.x = x
        self.title = title
        self.bins = bins
        self.normalise = normalise
        self.colour = colour if colour is not None else "black"
        self.fit_norm = fit_norm
        self.plot_rug = plot_rug
        self.plot_kde = plot_kde
        self.plot_hist = plot_hist
        self.label = 'histogram'
        self.xlabel = xlabel
        self.ylabel = f'{ylabel} Frequency' if self.normalise is False and self.plot_kde is False and fit_norm is False else f'{ylabel} Normalised Frequency'
        self.min_x = min_x
        self.min_y = min_y
        self.max_y = max_y
        self.max_x = max_x
        if config:
            self.load_style(config)

    def plot(self):
        x = self.x
        # First lets check whether we were passed lists or strings for our y and x arrays
        if not isinstance(x, str):
            vis_df = pd.DataFrame()
            vis_df['x'] = x
            x = 'x'
        else:
            vis_df = self.df
        # set the orders
        values = vis_df[x].values
        if self.fit_norm:
            ax = sns.distplot(values, fit=norm, kde=self.plot_kde, rug=self.plot_rug, hist=self.plot_hist,
                              norm_hist=self.normalise, bins=self.bins)
        else:
            ax = sns.distplot(values, kde=self.plot_kde, rug=self.plot_rug, hist=self.plot_hist,
                              norm_hist=self.normalise, bins=self.bins, color=self.colour)
        self.add_labels()
        self.apply_limits('x', self.max_x, self.min_x)
        self.apply_limits('y', self.max_y, self.min_y)

        self.set_ax_params(ax)
        plt.tight_layout()
        return ax