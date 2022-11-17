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

from sciviso import Barchart, Boxplot, Heatmap, Histogram, Scatterplot, Violinplot, Volcanoplot, Line, \
    Emapplot, Sankeyplot


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

    def test_sankey(self):
        df = pd.read_csv('data/RegGrps2-old-new-diff.csv')
        df = pd.read_csv('data/SiRCle_r1.csv')
        # https://plotly.com/python/sankey-diagram/
        # Convert into the source target, value and the labels
        # Labels are each one in the groups
        df = df[df['Regulation_Grouping_2'] != 'None']
        sk = Sankeyplot(df)
        fig = sk.plot(columns=['Methylation', 'RNA', 'Protein', 'Regulation_Grouping_2'], colour_col='Protein')
        fig.show()

    def test_histogram(self):
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
        row_colors2 = pd.DataFrame(labels)[0].map(lut).values
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

    def test_emapplot(self):
        df = pd.read_csv('data/emapexample.csv')
        eplot = Emapplot(df, config={'figsize': (3, 3)})
        eplot.build_graph()
        plt.savefig('fig.svg')
        plt.show()

        rcm_labels = ["MDS", "MDS_TMDE", "MDE", "MDE_TMDS", "TMDE", "TMDS", "TPDE", "TPDE_TMDS", "TPDS", "TPDS_TMDE"]
        r = 'MDE_TMDS'
        fig_dir= '/Users/ariane/Documents/code/sircle_meth/figures/sircle/'
        files = os.listdir(fig_dir)  # ClusterGoSummary_MDE_TMDS_matched-island.csv
        cluster_files = [c for c in files if 'ClusterGoSummary' in c]
        cluster_files
        for c in cluster_files:
            for test_title in ['matched', 'tvn']:
                if f'y_{r}_{test_title}' in c:
                    print(c)
                    try:
                        title = r + ' ' + c.split('_')[-1].split('.')[0]
                        df = pd.read_csv(f'{fig_dir}{c}')
                        df.sort_values('p.adjust')
                        df = df.head(n=20)
                        eplot = Emapplot(df, config={'figsize': (3, 3)})
                        eplot.build_graph()
                        plt.title(title)
                        plt.gca().set_clip_on = False
                        plt.savefig(f'{fig_dir}{title.replace(" ", "-")}.png', bbox_inches='tight')
                        plt.show()
                    except:
                        print(c)
