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
import numpy as np

from sciviso import Vis


class Line(Vis):

    def __init__(self, df: pd.DataFrame, title='', xlabel='', ylabel='', colour=None, figsize=(3, 3),
                 title_font_size=12, label_font_size=8, title_font_weight=700, config={}):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)
        super().__init__(df)
        self.title = title
        self.colour = colour
        self.xlabel = xlabel
        self.ylabel = ylabel
        if config:
            self.load_style(config)

    def plot_line_grps(self, idxs, axis_labels, axis_columns, labels_lst=None, title='', plt_mean=True, colours=None,
                      dot_colours=None, ylim=None, alpha_bg=0.1, alpha_highlight=0.8, linewidth_bg=0.5,
                      linewidth_highlight=3.0, scatter_linewidth=2.0):
        """ Plot means of line groups with optional alternative dot colours. """
        fig, ax = plt.subplots()
        axis_values = []
        if not labels_lst:
            labels_lst = axis_labels
        if not colours:
            colours = self.palette
        if not dot_colours:
            dot_colours = self.palette

        for c in axis_columns:
            axis_values.append(self.df[c].values)

        c_i = 0
        values_lst = []
        axis_x = range(0, len(axis_labels))
        for v in axis_values:
            value_lst = []
            for i in idxs:
                plt.plot(axis_x, v[i], alpha=alpha_bg,
                         c=colours[c_i], linewidth=linewidth_bg, zorder=1)
                value_lst.append(np.array(v[i]))
            c_i += 1
            if c_i == len(colours):
                c_i = 0
            values_lst.append(value_lst)

        c_i = 0
        if plt_mean:
            for v in values_lst:
                plt.plot(axis_x, np.mean(np.array(v), axis=0),
                         alpha=alpha_highlight, linewidth=linewidth_highlight, c=colours[c_i], zorder=1)
                plt.scatter(axis_x, np.mean(np.array(v), axis=0), facecolors='none', linewidth=scatter_linewidth,
                            edgecolors=dot_colours[c_i], alpha=alpha_highlight, zorder=2)

                c_i += 1

        plt.xticks(np.arange(len(axis_labels)))
        if ylim:
            plt.ylim(0, ylim)

        ax.set_xticklabels(axis_labels, rotation=45, ha='right')
        plt.title(title)
        ax.tick_params(labelsize=self.label_font_size)
        ax.legend(labels_lst, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=self.label_font_size)
        self.set_ax_params(ax)
        return ax

