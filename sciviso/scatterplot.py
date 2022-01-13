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
from mpl_toolkits.mplot3d import Axes3D

from sciviso import Vis


class Scatterplot(Vis):

    def __init__(self, df: pd.DataFrame, x: object, y: object, title='', xlabel='', ylabel='', colour=None, z=None,
                 zlabel=None, add_legend=True,
                 points_to_annotate=None, annotation_label=None, add_correlation=False, correlation='Spearman',
                 figsize=(3, 3), title_font_size=12, label_font_size=8, title_font_weight=700, s=30, config={},
                 color_col=None):
        super().__init__(df, figsize=figsize, title_font_size=title_font_size, label_font_size=label_font_size,
                         title_font_weight=title_font_weight)

        self.x = x
        self.y = y
        self.z = z
        self.title = title
        self.colour = colour
        self.points_to_annotate = points_to_annotate
        self.annotation_label = annotation_label
        self.add_correlation = add_correlation
        self.correlation = correlation
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.add_legend = add_legend
        self.zlabel = zlabel
        self.color_col = color_col
        self.s = s if config.get('s') is None else s
        if config:
            self.load_style(config)

    def annotate(self, ax: plt.axes, x: np.array, y: np.array, labels: np.array) -> plt.axes:
        """
        https://stackoverflow.com/questions/5147112/how-to-put-individual-tags-for-a-scatter-plot for more details
        Parameters
        ----------
        ax
        x
        y
        labels

        Returns
        -------

        """
        for i, name in enumerate(labels):
            if name in self.points_to_annotate:
                ax.annotate(name, (x[i], y[i]),
                            xytext=(-5, 10),
                            textcoords='offset points', ha='center', va='bottom',
                            bbox=dict(boxstyle='round,pad=0.5',
                                      fc='white', alpha=0.2)
                            )

        return ax

    def annotate3D(self, ax: plt.axes, x: np.array, y: np.array, z: np.array, labels: np.array) -> plt.axes:

        for i, name in enumerate(labels):
            if name in self.points_to_annotate:
                ax.text3D(x[i], y[i], z[i], name, size=12, zorder=1)
        return ax

    def plot2D(self):
        x, y = self.x, self.y
        if not isinstance(x, str) and not isinstance(y, str):
            vis_df = pd.DataFrame()
            vis_df['x'] = x
            vis_df['y'] = y
            x = 'x'
            y = 'y'
        else:
            vis_df = self.df
        if self.colour is None:
            self.colour = self.default_colour

        # Plot the points

        fig, ax = plt.subplots()
        # Check if we have a colour col
        color_col = self.color_col
        if color_col:
            colors = list(set(vis_df[color_col].values))
            ci = 0
            for c in colors:
                c_df = vis_df[vis_df[color_col] == c]
                scatter = ax.scatter(c_df[x].values, c_df[y].values, c=self.palette[ci], alpha=self.opacity,
                                     s=self.s, vmin=self.vmin, vmax=self.vmax, label=c)
                ci += 1
                if ci >= len(self.palette):
                    ci = 0
        else:
            scatter = ax.scatter(vis_df[x].values, vis_df[y].values, c=self.colour, alpha=self.opacity,
                                 cmap=self.cmap_str,
                                 s=self.s, vmin=self.vmin, vmax=self.vmax)

        # Check if we need to annotate anything
        if self.points_to_annotate is not None:
            self.check_columns([self.annotation_label])
            self.annotate(ax, vis_df[x].values, vis_df[y].values, self.df[self.annotation_label].values)

        self.add_labels()
        if self.add_legend and self.color_col:
            plt.colorbar(scatter, shrink=0.2, aspect=3)
        elif self.color_col:
            plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        ax.tick_params(labelsize=self.label_font_size)
        self.set_ax_params(ax)
        return ax

    def plot3D(self):
        x, y, z = self.x, self.y, self.z
        if not isinstance(x, str) and not isinstance(y, str):
            vis_df = pd.DataFrame()
            vis_df['x'] = x
            vis_df['y'] = y
            vis_df['z'] = z
            x = 'x'
            y = 'y'
            z = 'z'
        else:
            vis_df = self.df
        if self.colour is None:
            self.colour = self.default_colour

        # Plot the points
        fig = plt.figure()
        ax = Axes3D(fig)
        # Check if we have a colour col
        color_col = self.color_col
        if color_col:
            colors = list(set(vis_df[color_col].values))
            ci = 0
            for c in colors:
                c_df = vis_df[vis_df[color_col] == c]
                scatter = ax.scatter(c_df[x].values, c_df[y].values, c_df[z].values,
                                     c=self.palette[ci], alpha=self.opacity,
                                     s=self.s, vmin=self.vmin, vmax=self.vmax, label=c)
                ci += 1
                if ci >= len(self.palette):
                    ci = 0
        else:
            scatter = ax.scatter(vis_df[x].values, vis_df[y].values, vis_df[z].values, s=self.s,
                                 c=self.colour, alpha=self.opacity, cmap=self.cmap_str,
                                 vmin=self.vmin, vmax=self.vmax)
        # remove fill
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        # Check if we need to annotate anything
        if self.points_to_annotate is not None:
            self.check_columns([self.annotation_label])
            self.annotate3D(ax, vis_df[x].values, vis_df[y].values, vis_df[z].values,
                            self.df[self.annotation_label].values)

        self.add_labels()
        if isinstance(self.colour, str):
            # continue
            e = ''
        elif self.add_legend and not self.color_col:
            plt.colorbar(scatter, shrink=0.2, aspect=3)
        elif self.color_col:
            plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        ax.tick_params(labelsize=self.label_font_size)
        self.set_ax_params(ax)

        return ax

    def plot_groups_2D(self, grp_labels: list, grp_idxs: list, grp_colours=None, plt_bg=True, max_bg=600,
                       linewidth=1.0, alpha_highlight=0.8, alpha_bg=0.5):
        """ Allows pre-specified groups to be plot, user passes in an ordered list of group_labels,
        that match group_idxs. Optionally also passes the group colours. """
        if not grp_colours:
            grp_colours = self.palette

        fig, ax = plt.subplots()

        x = self.df[self.x].values
        y = self.df[self.y].values
        labels = []
        if plt_bg:
            if max_bg > len(x):
                max_bg = len(x)
            rand_idxs = np.random.choice(range(0, len(self.df), 1), max_bg)
            ax.scatter(x[rand_idxs], y[rand_idxs], c='lightgrey', alpha=alpha_bg,
                       vmin=self.vmin, vmax=self.vmax)
            labels = ['None']

        g_i = 0
        c_i = 0
        for g in grp_idxs:
            ax.scatter(x[g], y[g], s=self.s, c=grp_colours[c_i],
                       label=grp_labels[g_i],
                       edgecolors='k', linewidth=linewidth,
                       alpha=alpha_highlight,
                       vmin=self.vmin, vmax=self.vmax)
            labels.append(grp_labels[g_i])
            c_i += 1
            if c_i == len(grp_colours):
                c_i = 0
            g_i += 1
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=self.label_font_size)
        ax.tick_params(labelsize=self.label_font_size)
        self.set_ax_params(ax)
        plt.title(self.title)
        plt.tight_layout()
        return ax

    def plot_groups_3D(self, grp_labels: list, grp_idxs: list, grp_colours=None, plt_bg=True, max_bg=600,
                       s=70, linewidth=1.0, alpha_highlight=0.8, alpha_bg=0.5):
        """ Allows pre-specified groups to be plot, user passes in an ordered list of group_labels,
        that match group_idxs. Optionally also passes the group colours. """
        if not grp_colours:
            grp_colours = self.palette
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = self.df[self.x].values
        y = self.df[self.y].values
        z = self.df[self.z].values
        labels = []
        if plt_bg:
            rand_idxs = np.random.choice(range(0, len(self.df), 1), max_bg)
            ax.scatter(x[rand_idxs], y[rand_idxs], z[rand_idxs], c='lightgrey',
                       alpha=alpha_bg, s=self.s, vmin=self.vmin, vmax=self.vmax)
            labels = ['None']

        g_i = 0
        c_i = 0
        for g in grp_idxs:
            ax.scatter(x[g], y[g], z[g], s=self.s, c=grp_colours[c_i],
                       label=grp_labels[g_i],
                       edgecolors='k', linewidth=linewidth,
                       alpha=alpha_highlight,
                       vmin=self.vmin, vmax=self.vmax)
            labels.append(grp_labels[g_i])
            c_i += 1
            if c_i == len(grp_colours):
                c_i = 0
            g_i += 1
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=self.label_font_size)
        ax.tick_params(labelsize=self.label_font_size)
        self.set_ax_params(ax)
        # remove fill
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        plt.title(self.title)
        plt.tight_layout()
        return ax

    def plot(self):
        if self.z is None:
            return self.plot2D()
        else:
            return self.plot3D()
