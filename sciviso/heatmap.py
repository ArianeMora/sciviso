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


class Heatmap(Vis):

    def __init__(self, df: pd.DataFrame, chart_columns: list, row_index: str, title='', xlabel='', ylabel='',
                 cluster_rows=True, cluster_cols=True, row_colours=None, col_colours=None, vmin=None, vmax=None,
                 linewidths=0.5, x_tick_labels=1,
                 figsize=(3, 3), title_font_size=8, label_font_size=6, title_font_weight=700, cmap='RdBu_r',
                 config={}):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)
        self.chart_columns = chart_columns
        self.row_index = row_index
        self.title = title
        self.cluster_rows = cluster_rows
        self.cluster_cols = cluster_cols
        self.col_colours = col_colours
        self.row_colours = row_colours
        self.vmin = vmin
        self.vmax = vmax
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.cmap_str = cmap
        self.x_tick_labels = x_tick_labels
        self.linewidths = linewidths
        if config:
            self.load_style(config)

    def plot(self, ax=None, linecolor="black"):
        self.check_args_in_columns([self.chart_columns, [self.row_index]])
        df_dists = pd.DataFrame(self.df[self.chart_columns].values)
        df_dists.columns = self.chart_columns
        df_dists.index = self.df[self.row_index].values
        if ax:
            ax = sns.clustermap(df_dists, col_cluster=self.cluster_cols, figsize=self.figsize, row_cluster=self.cluster_rows,
                                col_colors=self.col_colours, ax=ax,
                                row_colors=self.row_colours, cmap=self.cmap_str, vmax=self.vmax, vmin=self.vmin,
                                yticklabels=1, xticklabels=self.x_tick_labels, linewidths=self.linewidths, linecolor=linecolor)
        else:
            ax = sns.clustermap(df_dists, col_cluster=self.cluster_cols, figsize=self.figsize, row_cluster=self.cluster_rows,
                                col_colors=self.col_colours,
                                row_colors=self.row_colours, cmap=self.cmap_str, vmax=self.vmax, vmin=self.vmin,
                                yticklabels=1, xticklabels=self.x_tick_labels, linewidths=self.linewidths, linecolor=linecolor)
        plt.title(self.title)
        plt.setp(ax.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
        plt.setp(ax.ax_heatmap.xaxis.get_majorticklabels(), rotation=45, horizontalalignment='right')
        ax.ax_heatmap.tick_params(labelsize=self.label_font_size)
        self.add_labels(title=False, x=False)
        ax.fig.suptitle(self.title, fontsize=self.title_font_size, fontweight=self.title_font_weight)
        ax.ax_heatmap.set_xticklabels(ax.ax_heatmap.get_xmajorticklabels(), fontsize=self.label_font_size)
        self.set_ax_params(ax.ax_heatmap)
        return ax

    def plot_hm(self, ax=None, linecolor="black"):
        self.check_args_in_columns([self.chart_columns, [self.row_index]])
        df_dists = pd.DataFrame(self.df[self.chart_columns].values)
        df_dists.columns = self.chart_columns
        df_dists.index = self.df[self.row_index].values
        if ax:
            ax = sns.heatmap(df_dists,
                             ax=ax, cmap=self.cmap_str, vmax=self.vmax, vmin=self.vmin,
                             yticklabels=1, xticklabels=self.x_tick_labels, linewidths=self.linewidths,
                             linecolor=linecolor)
        else:
            ax = sns.heatmap(df_dists, cmap=self.cmap_str, vmax=self.vmax, vmin=self.vmin,
                             yticklabels=1, xticklabels=self.x_tick_labels, linewidths=self.linewidths,
                             linecolor=linecolor)
        plt.title(self.title)
        plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, horizontalalignment='right')
        ax.tick_params(labelsize=self.label_font_size)
        self.add_labels(title=False, x=False)
        ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=self.label_font_size)
        self.set_ax_params(ax)
        #plt.colorbar(ax=ax, shrink=0.3, aspect=3, orientation='horizontal')
        return ax