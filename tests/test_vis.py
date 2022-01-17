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

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import shutil
import tempfile
import unittest

from sciviso import Barchart, Boxplot, Heatmap, Histogram, Scatterplot, Violinplot, Volcanoplot, Line


class TestVis(unittest.TestCase):

    def setUp(self):
        # Flag to set data to be local so we don't have to download them repeatedly. ToDo: Remove when publishing.
        self.local = True
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(THIS_DIR, 'data/')
        if self.local:
            self.tmp_dir = os.path.join(THIS_DIR, 'data/tmp/')
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
            os.mkdir(self.tmp_dir)
        else:
            self.tmp_dir = tempfile.mkdtemp(prefix='scidatannotate_tmp_')
        # Lets use a simple dataframe e.g. the iris dataset
        self.df = pd.read_csv(self.data_dir + 'iris.csv')
        self.x = 'sepal_width'
        self.y = 'petal_width'
        self.numeric_cols = ['sepal_width', 'sepal_length', 'petal_length', 'petal_width']
        self.label = 'label'

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_barchart(self):
        barchart = Barchart(self.df, self.label, self.y)
        barchart.plot()
        plt.show()

    def test_histpgram(self):
        histogram = Histogram(self.df, self.y, fit_norm=True, plot_rug=True)
        histogram.plot()
        plt.show()

        histogram = Histogram(self.df, self.y, fit_norm=False, plot_rug=True)
        histogram.plot()
        plt.show()

    def test_boxplot(self):
        boxplot = Boxplot(self.df, self.label, self.y)
        boxplot.plot()
        plt.show()

        # Example showing formatting data for plots
        df = boxplot.format_data_for_boxplot(self.df, ["sepal_length", "sepal_width"], "label",
                                             ["Iris-setosa", "Iris-virginica"])
        boxplot = Boxplot(df, "Conditions", "Values", box_colors=['pink', 'orange'], add_dots=True)
        boxplot.plot()
        plt.savefig('fig.svg')
        plt.show()

    def test_heatmap(self):
        labels = self.df['sepal_width'].values.astype(int)
        lut = dict(zip(set(labels), sns.color_palette("coolwarm", len(set(labels)))))
        row_colors = pd.DataFrame(labels)[0].map(lut)

        # Create additional row_colors here
        labels = self.df['sepal_length'].values.astype(int)
        lut = dict(zip(set(labels), sns.color_palette("coolwarm", len(set(labels)))))
        row_colors2 = pd.DataFrame(labels)[0].map(lut)
        annot = self.df[self.numeric_cols].values
        heatmap = Heatmap(self.df, self.numeric_cols, self.label, 'Xlabel', 'Ylabel', annot=True,
                          row_colours=[row_colors, row_colors2], rows_to_colour=['sepal_length'],
                          linewidths=0.5, x_tick_labels=0)
        heatmap.plot(linecolor="none")
        heatmap.save_png([self.data_dir, "heatmap"])
        plt.show()
        heatmap.plot_hm(linecolor="none")
        plt.show()
        df = self.df
        labels = df['label'].values
        lut = dict(zip(set(labels), sns.color_palette("pastel", len(set(labels)))))
        row_colors = pd.DataFrame(labels)[0].map(lut)
        df['label_2'] = labels + '_2'

        # Create additional row_colors here based on the values of one column as an example
        labels = df['sepal_length'].values.astype(int)
        lut = dict(zip(set(labels), sns.color_palette("Greens", len(set(labels)))))
        row_colors2 = pd.DataFrame(labels)[0].map(lut)
        heatmap = Heatmap(df,
                          chart_columns=['sepal_width', 'sepal_length', 'petal_length', 'petal_width'],
                          row_index='label', row_colours=[row_colors, row_colors2], rows_to_colour=['label', 'label_2'],
                          y_tick_labels=10,  # How many skips before a tick on the RHS looks neater
                          figsize=(5, 5))
        heatmap.plot(linecolor="none")
        plt.show()


    def test_scatterplot(self):
        scatterplot = Scatterplot(self.df, self.x, self.y, 'sepal_length', 'Xlabel', 'Ylabel',
                                  points_to_annotate=['Iris-setosa'],
                                  annotation_label=self.label, colour=self.df[self.x].values)
        scatterplot.plot()
        plt.show()

        scatterplot = Scatterplot(self.df, self.x, self.y, 'sepal_length', 'Xlabel', 'Ylabel', z='sepal_length',
                                  points_to_annotate=['Iris-setosa'],
                                  annotation_label=self.label, colour=self.df[self.x].values)
        scatterplot.plot()
        plt.show()

    def test_violinplot(self):
        violinplot = Violinplot(self.df, self.label, self.y, 'Xlabel', 'Ylabel', add_dots=True)
        violinplot.plot()
        plt.show()

    def test_volcanoplot(self):
        self.df = pd.read_csv(self.data_dir + 'volcano.csv')

        volcanoplot = Volcanoplot(self.df, 'logfc', 'padj', 'external_gene_name', 'A Title', 'Xlabel', 'Ylabel',
                                  label_big_sig=True, )
        volcanoplot.plot()
        plt.show()

    def test_line(self):
        line = Line(self.df, 'title', 'Xlabel', 'Ylabel')
        idxs = np.where(self.df['label'] == 'Iris-setosa')[0]
        labels = ['length', 'width']
        cols = [['sepal_length', 'petal_length'], ['sepal_width', 'petal_width']]

        line.plot_line_grps(idxs, labels, cols)
        plt.show()
