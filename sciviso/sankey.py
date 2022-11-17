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

import pandas as pd
import plotly.graph_objects as go

from sciviso import Vis


class Sankeyplot(Vis):

    def __init__(self, df: pd.DataFrame, title='', figsize=(3, 3), colours=None, config={}):
        super().__init__(df, figsize=figsize)
        super().__init__(df)
        self.df = df
        self.title = title
        self.label = 'sankey'
        self.colours = colours if colours is not None else ['#AAC7E2', '#FFC107', '#016957', '#9785C0',
               '#D09139', '#338A03', '#FF69A1', '#5930B1', '#FFE884', '#35B567', '#1E88E5',
               '#ACAD60', '#A2FFB4', '#B68F5', '#854A9C']
        if config:
            self.load_style(config)

    def plot(self, colour_col=None, columns=None):
        """

        :param colour_col: the colour column will be the column by which the values are annotated.
        :param columns: has to be ordered as in the very left one in the list is on the LHS while the one on the RHS is
        the last in the snakey plot: default is to use all columns
        :return:
        """
        # Use by default the last column as colour
        colour_col = colour_col if colour_col else self.df.columns[-1]
        labels = {}
        i = 0
        columns = columns if columns else self.df.columns
        for c in columns:
            for v in self.df[c].values:
                if labels.get(f'{c} {v}') is None:
                    labels[f'{c} {v}'] = i
                    i += 1
        # Now we want to do the source to target
        source = []
        target = []
        value = []
        colours = []
        colour_column = self.df[colour_col].values
        cmap = {}
        i = 0
        for c in colour_column:
            cmap[c] = self.colours[i]
            i += 1
            if i == len(self.colours):
                i = 0

        for i, c in enumerate(columns):
            if i + 1 < len(columns):
                # Basically we want to go through each and say the column0 is the source and the next value is the
                # target
                source_values = self.df[c].values
                target_values = self.df[columns[i + 1]].values
                for j, s in enumerate(source_values):
                    value.append(1)
                    source.append(labels.get(f'{c} {s}'))
                    target.append(labels.get(f'{columns[i + 1]} {target_values[j]}'))
                    colours.append(cmap.get(colour_column[j]))

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=list(labels.keys()),
                color='white'
            ),
            link=dict(
                source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
                target=target,
                value=value,
                color=colours
            ))])

        fig.update_layout(title_text=self.title, font_size=self.title_font_size)
        fig.show()