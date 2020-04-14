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


class Volcanoplot(Vis):

    def __init__(self, df: pd.DataFrame, log_fc: str, p_val: str, label_column: str, invert=False, p_val_cutoff=0.05,
                 log_fc_cuttoff=2, label_big_sig=False, colours=None, offset=0, values_to_label=None):
        super().__init__(df)
        self.log_fc = log_fc
        self.p_val = p_val
        self.p_val_cutoff = p_val_cutoff
        self.log_fc_cuttoff = log_fc_cuttoff
        self.values_to_label = values_to_label
        self.label_big_sig = label_big_sig
        self.invert = invert
        self.label_column = label_column
        self.offset = offset
        self.label = 'volcanoplot'
        self.colours = {'ns_small-neg-logFC': 'lightgrey',
                        'ns_small-pos-logFC': 'lightgrey',
                        'ns_big-neg-logFC': 'grey',
                        'ns_big-pos-logFC': 'grey',
                        'sig_small-neg-logFC': 'lightskyblue',
                        'sig_small-pos-logFC': 'salmon',
                        'sig_big-neg-logFC': 'mediumblue',
                        'sig_big-pos-logFC': 'firebrick'} if colours is None else colours

    def add_scatter_and_annotate(self, fig: plt, x: np.array, y: np.array, colour: str, idxs: np.array):
        x = x[idxs]
        y = y[idxs]
        ax = fig.scatter(x, y, c=colour, alpha=self.opacity)

        # Check if we want to annotate any of these with their gene IDs
        if self.values_to_label is not None:
            labels = self.df[self.label_column].values[idxs]
            for i, name in enumerate(labels):
                if name in self.values_to_label:
                    ax.annotate(name, (x[i], y[i]))
        return ax

    def volcanoplot(self):
        """
        For annotation styling see: https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.annotate
        Returns
        -------

        """
        # x axis has log_fc, first only plot the values < cutoff
        x = self.df[self.log_fc].values
        y = -1 * np.log10(self.df[self.p_val].values + self.offset)

        log_fc_np = self.df[self.log_fc].values
        p_val_np = self.df[self.p_val].values

        if self.invert:
            x = -1 * np.log10(self.df[self.p_val].values + self.offset)
            y = self.df[self.log_fc].values

        ns_small_pos_logfc = np.where((p_val_np > self.p_val_cutoff) & (np.abs(log_fc_np) < self.log_fc_cuttoff)
                                & (log_fc_np > 0))
        ns_big_pos_logfc = np.where((p_val_np > self.p_val_cutoff) & (np.abs(log_fc_np) >= self.log_fc_cuttoff)
                               & (log_fc_np > 0))
        sig_small_pos_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) < self.log_fc_cuttoff)
                                & (log_fc_np > 0))
        sig_big_pos_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) >= self.log_fc_cuttoff)
                                & (log_fc_np > 0))

        ns_small_neg_logfc = np.where((p_val_np > self.p_val_cutoff) & (np.abs(log_fc_np) < self.log_fc_cuttoff)
                                & (log_fc_np <= 0))
        ns_big_neg_logfc = np.where((p_val_np > self.p_val_cutoff) & (np.abs(log_fc_np) >= self.log_fc_cuttoff)
                               & (log_fc_np <= 0))
        sig_small_neg_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) < self.log_fc_cuttoff)
                                & (log_fc_np <= 0))
        sig_big_neg_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) >= self.log_fc_cuttoff)
                                & (log_fc_np <= 0))

        # Plot the points
        fig, ax = plt.subplots()

        self.add_scatter_and_annotate(ax, x, y, self.colours['ns_small-pos-logFC'], ns_small_pos_logfc)
        self.add_scatter_and_annotate(ax, x, y, self.colours['ns_big-pos-logFC'], ns_big_pos_logfc)
        self.add_scatter_and_annotate(ax, x, y, self.colours['sig_small-pos-logFC'], sig_small_pos_logfc)
        ax = self.add_scatter_and_annotate(ax, x, y, self.colours['sig_big-pos-logFC'], sig_big_pos_logfc)
        # Check if the user wants these labeled
        if self.label_big_sig:
            labels = self.df[self.label_column].values[sig_big_pos_logfc]
            for i, name in enumerate(labels):
                ax.annotate(name, (x[i], y[i]))
        # Negative
        self.add_scatter_and_annotate(ax, x, y, self.colours['ns_small-neg-logFC'], ns_small_neg_logfc)
        self.add_scatter_and_annotate(ax, x, y, self.colours['ns_big-neg-logFC'], ns_big_neg_logfc)
        self.add_scatter_and_annotate(ax, x, y, self.colours['sig_small-neg-logFC'], sig_small_neg_logfc)
        ax = self.add_scatter_and_annotate(ax, x, y, self.colours['sig_big-neg-logFC'], sig_big_neg_logfc)
        # Check if the user wants these labeled
        if self.label_big_sig:
            labels = self.df[self.label_column].values[sig_big_neg_logfc]
            for i, name in enumerate(labels):
                ax.annotate(name, (x[i], y[i]))
