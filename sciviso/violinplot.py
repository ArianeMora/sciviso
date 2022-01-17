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

class Violinplot(Vis):

    def __init__(self, df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', hue=None, order=None,
                 hue_order=None, showfliers=False, add_dots=False, add_stats=False, stat_method='Mann-Whitney',
                 figsize=(3, 3), title_font_size=12, box_pairs=None,
                 label_font_size=8, title_font_weight=700, config=None):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)
        self.df = df
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.hue = hue
        self.order = order
        self.hue_order = hue_order
        self.showfliers = showfliers
        self.add_dots = add_dots
        self.add_stats = add_stats
        self.stat_method = stat_method
        self.box_pairs = box_pairs
        if config:
            self.load_style(config)

    def plot(self):
        x, y, hue, order, hue_order, box_pairs = self.x, self.y, self.hue, self.order, self.hue_order, self.box_pairs
        if not isinstance(self.x, str) and not isinstance(self.y, str):
            vis_df = pd.DataFrame()
            vis_df['x'] = x
            vis_df['y'] = y
            x = 'x'
            y = 'y'
            if self.hue is not None:
                vis_df['colour'] = self.hue
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

        ax = sns.violinplot(data=vis_df, x=x, y=y, hue=hue, hue_order=hue_order, order=order, palette=self.palette,
                            showfliers=self.showfliers)
        if self.add_dots:
            ax = sns.stripplot(data=vis_df, x=x, y=y, hue_order=hue_order, order=order, alpha=0.9, s=1, color='.2')
        if self.add_stats:
            # Add all pairs in the order if the box pairs is none

            pairs = []
            if box_pairs is None:
                box_pairs = []
                for i in order:
                    for j in order:
                        if i != j:
                            # Ensure we don't get duplicates
                            pair = f'{i}{j}' if i < j else f'{j}{i}'
                            if pair not in pairs:
                                box_pairs.append((i, j))
                                pairs.append(pair)
            # Add stats annotation

            add_stat_annotation(ax, data=vis_df, x=x, y=y, order=order,
                                box_pairs=box_pairs,
                                test=self.stat_method, text_format='star', loc='inside', verbose=2,
                                pvalue_thresholds=[[1e-4, "****"], [1e-3, "***"], [1e-2, "**"], [0.05, "*"]])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.tick_params(labelsize=self.label_font_size)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=self.label_font_size)
        self.add_labels()
        self.set_ax_params(ax)
        plt.tight_layout()
        return ax