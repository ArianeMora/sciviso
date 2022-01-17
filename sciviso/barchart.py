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

from sciviso import Vis


class Barchart(Vis):

    def __init__(self, df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', hue=None, order=None,
                 hue_order=None, figsize=(3, 3), title_font_size=12, label_font_size=8, title_font_weight=700,
                 errwidth=0, linewidth=1, edgecolor="k", config={}):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)
        super().__init__(df)
        self.df = df
        self.x = x
        self.y = y
        self.title = title
        self.hue = hue
        self.order = order
        self.hue_order = hue_order
        self.label = 'barchart'
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.errwidth = errwidth if config.get('errwidth') is None else config.get('errwidth')
        self.linewidth = linewidth if config.get('linewidth') is None else config.get('linewidth')
        self.edgecolor = edgecolor if config.get('edgecolor') is None else config.get('edgecolor')
        if config:
            self.load_style(config)

    def plot(self):
        x, y, hue_order, order, hue = self.x, self.y, self.hue_order, self.order, self.hue
        # First lets check whether we were passed lists or strings for our y and x arrays
        if not isinstance(x, str) and not isinstance(y, str):
            vis_df = pd.DataFrame()
            vis_df['x'] = x
            vis_df['y'] = y
            x = 'x'
            y = 'y'
            if hue is not None:
                vis_df['colour'] = hue
                hue = 'colour'
            if order is None:
                order = list(set(vis_df['x'].values))
                order.sort()
        else:
            vis_df = self.df
        # set the orders
        if hue_order is None and hue is not None:
            hue_order = list(set(vis_df[hue].values))
            hue_order.sort()
        if order is None:
            order = list(set(vis_df[x].values))
            order.sort()

        ax = sns.barplot(data=vis_df, x=x, y=y, hue=hue, hue_order=hue_order, order=order, palette=self.palette,
                         edgecolor=self.edgecolor, linewidth=self.linewidth, errwidth=self.errwidth)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.tick_params(labelsize=self.label_font_size)
        self.add_labels()
        self.set_ax_params(ax)
        plt.tight_layout()
        return ax