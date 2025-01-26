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


class Countplot(Vis):

    def __init__(self, df: pd.DataFrame, x=None, y=None, title='', xlabel='', ylabel='', colour=None, hue=None,
                 min_x=None, max_x=None, min_y=None, max_y=None,
                 figsize=(3, 3), config={}):
        super().__init__(df, figsize=figsize)
        self.df = df
        self.x = x
        self.y = y
        self.title = title
        self.hue = hue
        self.colour = colour if colour is not None else "black"
        self.label = 'countplot'
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.min_x = min_x
        self.min_y = min_y
        self.max_y = max_y
        self.max_x = max_x
        if config:
            self.load_style(config)

    def plot(self):
        x = self.x
        y = self.y
        # First lets check whether we were passed lists or strings for our y and x arrays
        if x is not None:
            ax = sns.countplot(data=self.df, x=x, hue=self.hue, palette=self.palette, order =self.df[x].value_counts().index)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', weight='bold')
        elif y is not None:
            ax = sns.countplot(data=self.df, y=y, hue=self.hue, palette=self.palette)
        self.add_labels()
        self.apply_limits('x', self.max_x, self.min_x)
        self.apply_limits('y', self.max_y, self.min_y)

        self.set_ax_params(ax)
        plt.tight_layout()
        return ax