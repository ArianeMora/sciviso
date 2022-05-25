# Want to also plot the RNA, protein between S1 and S4 and also the protein from the new dataset


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
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statannot import add_stat_annotation

from sciviso import Vis


class Boxplot(Vis):
    """
    Box plot. Adds stat annotations and returns the SVG or saves it to disk.
    for stats annotations details see: https://github.com/webermarcolivier/statannot
    """

    def __init__(self, df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', box_colors=None,
                 hue=None, order=None, hue_order=None, showfliers=False, add_dots=False, add_stats=True,
                 stat_method='Mann-Whitney', box_pairs=None, figsize=(3, 3), title_font_size=12, label_font_size=8,
                 title_font_weight=700, config=None):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)
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
        self.label = 'boxplot'
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.box_colors = box_colors
        if config:
            self.load_style(config)

    def format_data_for_boxplot(self, df: pd.DataFrame, conditions: list, filter_column=None, filter_values=None):
        condition_dict = defaultdict(list)
        for column in df.columns:
            for c in conditions:
                if c in column:
                    condition_dict[c].append(column)

        # Now lets get the values
        values = []
        condition = []
        samples = []
        if filter_column is None or filter_values is None:
            for i in range(0, len(df)):
                for cond, columns in condition_dict.items():
                    for c in columns:
                        values.append(df[c].values[i])
                        condition.append(cond)
                        samples.append(c)
        else:
            i = 0
            for v in df[filter_column].values:
                if v in filter_values:
                    for cond, columns in condition_dict.items():
                        for c in columns:
                            values.append(df[c].values[i])
                            condition.append(cond)
                            samples.append(c)
                i += 1
        box_df = pd.DataFrame()
        box_df['Samples'] = samples
        box_df['Values'] = values
        box_df['Conditions'] = condition
        return box_df

    def plot(self, ax=None, legend=True):
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
        if hue_order is None and hue is not None:
            hue_order = list(set(vis_df[hue].values))
            hue_order.sort()
        if order is None:
            order = list(set(vis_df[x].values))
            order.sort()

        ax = sns.boxplot(data=vis_df, x=x, y=y, hue=hue, hue_order=hue_order, order=order, palette=self.palette,
                         showfliers=self.showfliers, ax=ax)
        if self.add_dots:
            ax = sns.swarmplot(data=vis_df, x=x, y=y, hue_order=hue_order,
                               order=order, hue=hue, dodge=True, alpha=0.3, ax=ax, palette=['black', 'black'])

        if self.add_stats:
            # Add all pairs in the order if the box pairs is none
            if box_pairs is None:
                pairs = []
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
                                test=self.stat_method, text_format='star', loc='inside', verbose=2)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', weight='bold')

        # Check if the user supplied a list of colours for the boxes:
        if self.box_colors is not None:
            for i, b in enumerate(ax.artists):
                b.set_facecolor(self.box_colors[i])

        if legend and not self.box_colors:
            plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=self.label_font_size)
        elif legend and self.box_colors:
            plt.legend(order, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,
                       fontsize=self.label_font_size)

        if legend == False:
            ax.legend([], [], frameon=False)
        ax.tick_params(labelsize=self.label_font_size)
        self.add_labels(ax=ax)
        ax.title.set_text(self.title)
        self.set_ax_params(ax=ax)
        plt.tight_layout()
        return ax