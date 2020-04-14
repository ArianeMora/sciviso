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


class Scatterplot(Vis):

    def __init__(self, df: pd.DataFrame, x: object, y: object, title='', colour=None, points_to_annotate=None,
                 annotation_label=None, add_correlation=False, correlation='Spearman'):
        super().__init__(df)
        self.x = x
        self.y = y
        self.title = title
        self.colour = colour
        self.points_to_annotate = points_to_annotate
        self.annotation_label = annotation_label
        self.add_correlation = add_correlation
        self.correlation = correlation

    def annotate(self, ax: plt.axes, x: np.array, y: np.array, labels: np.array) -> plt.axes:
        for i, name in enumerate(labels):
            if name in self.points_to_annotate:
                ax.annotate(name, (x[i], y[i]))

        return ax

    def plot(self):
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
        ax.scatter(vis_df[x].values, vis_df[y].values, c=self.colour, alpha=self.opacity)

        # Check if we need to annotate anything
        if self.points_to_annotate is not None:
            self.check_columns([self.annotation_label])
            self.annotate(ax, vis_df[x].values, vis_df[y].values, self.df[self.annotation_label].values)
