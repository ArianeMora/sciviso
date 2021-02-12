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
from adjustText import adjust_text

from sciviso import Vis


class Volcanoplot(Vis):

    def __init__(self, df: pd.DataFrame, log_fc: str, p_val: str, label_column: str, title='',
                 xlabel='', ylabel='', invert=False, p_val_cutoff=0.05,
                 log_fc_cuttoff=2, label_big_sig=False, colours=None, offset=None,
                 text_colours=None, values_to_label=None, max_labels=20, values_colours=None):
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
                        'sig_small-neg-logFC': '#2970b1',
                        'sig_small-pos-logFC': '#d6604c',
                        'sig_big-neg-logFC': '#0a3568',
                        'sig_big-pos-logFC': '#6f0220'} if colours is None else colours
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.max_labels = max_labels
        self.values_colours = values_colours or {}
        self.text_colours = text_colours or {}

    def add_scatter_and_annotate(self, fig: plt, x_all: np.array, y_all: np.array,
                                 colour: str, idxs: np.array, annotate=False):
        x = x_all[idxs]
        y = y_all[idxs]
        ax = fig.scatter(x, y, c=colour, alpha=self.opacity, s=20)

        # Check if we want to annotate any of these with their gene IDs

        if self.values_to_label is not None:
            texts = []
            labels = self.df[self.label_column].values[idxs]
            for i, name in enumerate(labels):
                if name in self.values_to_label:
                    lbl_bg = self.values_colours.get(name)
                    color = self.text_colours.get(name)
                    texts.append(fig.text(x[i], y[i], name, color=color, fontsize=6,
                                          bbox=dict(fc=lbl_bg, alpha=1.0)))
            adjust_text(texts, force_text=2.0)
        # Check if the user wants these labeled
        if self.label_big_sig and annotate:
            # If they do have a limit on the number of ones we show (i.e. we don't want 10000 gene names...)
            max_values = -1 * self.max_labels
            if len(y) < self.max_labels:
                max_values = -1 * (len(y) - 1)
            most_sig_idxs = np.argpartition(y, max_values)[max_values:]
            labels = self.df[self.label_column].values[idxs][most_sig_idxs]
            x = x[most_sig_idxs]
            y = y[most_sig_idxs]
            # We only label the ones with the max log fc
            for i, name in enumerate(labels):
                fig.annotate(name, (x[i], y[i]),
                             xytext=(0, 10),
                             textcoords='offset points', ha='center', va='bottom',
                             bbox=dict(boxstyle='round,pad=0.5',
                                       fc='white', alpha=0.2)
                             )
        return ax

    def plot(self):
        """
        For annotation styling see: https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.annotate
        Returns
        -------

        """
        # if offset is not given, make the offset the smallest value in the dataset
        if not self.offset:
            vals = self.df[self.p_val].values
            self.offset = np.min(vals[np.nonzero(vals)])
            self.u.warn_p(['No offset was provided, setting offset to be smallest value recorded in dataset: ',
                           self.offset])

        # x axis has log_fc, first only plot the values < cutoff
        x = self.df[self.log_fc].values
        y = -1 * np.log10(self.df[self.p_val].values + self.offset)

        log_fc_np = self.df[self.log_fc].values
        p_val_np = self.df[self.p_val].values

        if self.invert:
            x = -1 * np.log10(self.df[self.p_val].values + self.offset)
            y = self.df[self.log_fc].values
        sig_small_pos_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) < self.log_fc_cuttoff)
                                       & (log_fc_np > 0))
        sig_big_pos_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) >= self.log_fc_cuttoff)
                                     & (log_fc_np > 0))

        sig_small_neg_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) < self.log_fc_cuttoff)
                                       & (log_fc_np <= 0))
        sig_big_neg_logfc = np.where((p_val_np <= self.p_val_cutoff) & (np.abs(log_fc_np) >= self.log_fc_cuttoff)
                                     & (log_fc_np <= 0))

        # Plot the points
        fig, ax = plt.subplots(figsize=(3, 3))
        self.add_scatter_and_annotate(ax, x, y, self.colours['sig_small-pos-logFC'], sig_small_pos_logfc)
        self.add_scatter_and_annotate(ax, x, y, self.colours['sig_big-pos-logFC'], sig_big_pos_logfc, annotate=True)

        # Negative
        self.add_scatter_and_annotate(ax, x, y, self.colours['sig_small-neg-logFC'], sig_small_neg_logfc)
        self.add_scatter_and_annotate(ax, x, y, self.colours['sig_big-neg-logFC'], sig_big_neg_logfc, annotate=True)
        self.add_labels()
        ax.tick_params(labelsize=6)

        return ax
