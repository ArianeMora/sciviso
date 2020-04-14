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
from statannot import add_stat_annotation

from sciviso import Vis


class Boxplot(Vis):
    """
    Box plot. Adds stat annotations and returns the SVG or saves it to disk.
    """
    def __init__(self, df: pd.DataFrame, x: object, y: object, title='', hue=None, order=None, hue_order=None,
                    showfliers=False, add_dots=False, add_stats=True, stat_method='Mann-Whitney', box_pairs=None):
        super().__init__(df)
        self.df = df
        self.x = x
        self.y = y
        self.title = title
        self.hue = hue
        self.order = order
        self.hue_order = hue_order
        self.showfliers = showfliers
        self.add_dots = add_dots
        self.add_stats = add_stats
        self.stat_method = stat_method
        self.box_pairs = box_pairs

    def boxplot(self):
        x, y, hue_order, order, hue, box_pairs = self.x, self.y, self.hue_order, self.order, self.hue, self.box_pairs
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
        if hue_order is None:
            hue_order = list(set(vis_df[hue].values))
            hue_order.sort()
        if order is None:
            order = list(set(vis_df[x].values))
            order.sort()

        ax = sns.boxplot(data=vis_df, x=x, y=y, hue=hue, hue_order=hue_order, order=order, palette=self.palette,
                         showfliers=self.showfliers)
        if self.add_dots:
            ax = sns.stripplot(data=vis_df, x=x, y=y, hue_order=hue_order, order=order, color='.2')
        if self.add_stats:
            # Add all pairs in the order if the box pairs is none
            if box_pairs is None:
                box_pairs = []
                for i in order:
                    for j in order:
                        if i != j:
                            box_pairs.append((i, j))
            # Add stats annotation
            add_stat_annotation(ax, data=vis_df, x=x, y=y, order=order,
                                box_pairs=[box_pairs],
                                test=self.stat_method, text_format='star', loc='inside', verbose=2)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.title(self.title)

    def get_boxplot_str(self) -> str:
        self.boxplot()
        return self.return_svg()

    def save_boxplot(self, label_lst: list) -> None:

        label_lst = self.check_label(label_lst, 'boxplot')
        self.boxplot()
        self.save_svg(label_lst)
