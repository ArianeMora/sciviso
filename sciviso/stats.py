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

import io
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
from textwrap import wrap

from sciutil import SciUtil, SciException

assumption_dict = {
    'ttest_1samp': {
        'Short': 'Calculate the T-test for one group scores against an EXPECTED mean (popmean). [2]',
        'Long': 'This is a test for the null hypothesis that the expected value (mean) of a sample of independent observations a is equal to the given population mean, popmean.[2]',
        'Null Hypothesis': 'The null hypothesis is that the mean of the group is Greater/Less/Equal to the mean of the Null Hypothesis (popmean)',
        'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html#scipy.stats.ttest_1samp',
        'Assumptions': {'normality': True,
                        'num_groups': 1,
                        'alternative': ['two-sided', 'less', 'greater'],
                        'min_sample_size': 3,
                        },
        'Data': {'normality': None,
                 'equal-variance': None,
                 }
    },
    'ttest_ind': {'Name': 'Independent t-test',
                  'Short': 'Calculate the T-test for the means of two independent samples of scores. [2]',
                  'Long': 'Where subjects in both groups are independent of each other (persons in first group are different from those in second group), and the parameters are normally distributed and continuous, the unpaired t-test is used. [1]',
                  'Null Hypothesis': 'The null hypothesis is that the two groups have the same mean.',
                  'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html#scipy.stats.ttest_ind',
                  'Assumptions': {'paired': False,
                                  'normality': True,
                                  'equal-variance': True,
                                  'num_groups': 2,
                                  'alternative': ['two-sided', 'less', 'greater'],
                                  'min_sample_size': 3},
                  'Data': {'normality': None,
                           'equal-variance': None,
                           }
                  },
    'ttest_welch': {'Name': 'Welches t-test',
                    'Short': 'Calculate the Welchs T-test for the means of two independent samples of scores. [2]',
                    'Long': 'Where subjects in both groups are independent of each other (persons in first group are different from those in second group), and the parameters are normally distributed and continuous, the unpaired t-test is used. [1]',
                    'Null Hypothesis': 'The null hypothesis is that the two groups have the same mean.',
                    'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html#scipy.stats.ttest_ind',
                    'Assumptions': {'paired': False,
                                    'normality': True,
                                    'equal-variance': False,  # Same as t-test but with different variance
                                    'num_groups': 2,
                                    'alternative': ['two-sided', 'less', 'greater'],
                                    'min_sample_size': 3},  # Two-sided, less or greater are the options.
                    'Data': {'normality': None,
                             'equal-variance': None,
                             }
                    },
    'ttest_rel': {'Name': 'Paired t-test',
                  'Short': 'Calculate the T-test for the means of two DEPENDENT samples of scores. [2]',
                  'Long': 'The paired t-test is used for normally distributed continuous parameters in two paired groups. [1]',
                  'Null Hypothesis': 'The null hypothesis is that the two groups have the same mean.',
                  'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html#scipy.stats.ttest_rel',
                  'Assumptions': {'paired': True,
                                  'normality': True,
                                  'equal-variance': True,
                                  'num_groups': 2,
                                  'alternative': ['two-sided', 'less', 'greater'],
                                  'min_sample_size': 3},
                  'Data': {'normality': None,
                           'equal-variance': None,
                           }
                  },
    'mannwhitneyu': {'Name': 'Mann-Whitney U-test',
                     'Short': 'The Mann-Whitney U test is a nonparametric test of the null hypothesis that the distribution underlying sample x is the same as the distribution underlying sample y. It is often used as a test of difference in location between distributions.',
                     'Long': 'The Mann–Whitney U test (also known as the Wilcoxon rank sum test) can be used for the comparison of a non-normally distributed, but at least ordinally scaled, parameter in two unpaired samples.[1]',
                     'Null Hypothesis': 'The null hypothesis is that the two groups have the same mean.',
                     'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html#scipy.stats.mannwhitneyu',
                     'Assumptions': {'paired': True,
                                     'normality': False,
                                     'equal-variance': False,
                                     'num_groups': 2,
                                     'alternative': ['two-sided', 'less', 'greater'],
                                     'min_sample_size': 3},
                     'Data': {'normality': None,
                              'equal-variance': None,
                              }
                     },
    'wilcoxon': {'Name': 'Wilcoxon signed rank test',
                 'Short': 'The Wilcoxon signed-rank test tests the null hypothesis that two related paired samples come from the same distribution. In particular, it tests whether the distribution of the differences x - y is symmetric about zero. It is a non-parametric version of the paired T-test.[2]',
                 'Long': 'The Wilcoxon signed rank test can be used for the comparison of two paired samples of non-normally distributed parameters, but on a scale that is at least ordinal.[5] Alternatively, the sign test should be used when the two values are only distinguished on a binary scale—e.g., improvement versus deterioration. If more than matched paired samples are being compared, the Friedman test can be used as a generalization of the sign test. [1]',
                 'Null Hypothesis': 'The null hypothesis is that the two groups have the same mean.',
                 'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html#scipy.stats.wilcoxon',
                 'Assumptions': {'paired': False,
                                 'normality': False,
                                 'equal-variance': False,
                                 'num_groups': 2,
                                 'alternative': ['two-sided', 'less', 'greater'],
                                 'min_sample_size': 3},
                 'Data': {'normality': None,
                          'equal-variance': None,
                          }
                 },
    'kruskal': {'Name': 'Kruskal-Wallis H-test',
                'Long': 'The Kruskal-Wallis H-test tests the null hypothesis that the population median of all of the groups are equal. It is a non-parametric version of ANOVA. The test works on 2 or more independent samples, which may have different sizes. Note that rejecting the null hypothesis does not indicate which of the groups differs. Post hoc comparisons between groups are required to determine which groups are different. [2]',
                'Short': 'Compute the Kruskal-Wallis H-test for independent samples. [2] e.g. non-parametric one-way ANOVA',
                'Null Hypothesis': 'The null hypothesis is that the population median of all of the groups are equal.',
                'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html#scipy.stats.kruskal',
                'Assumptions': {'paired': False,
                                'normality': False,
                                'equal-variance': False,
                                'num_groups': None,  # Can be more than 2
                                'alternative': ['two-sided', 'less', 'greater'],
                                'min_sample_size': 5},
                'Data': {'normality': None,
                         'equal-variance': None,
                         },
                'Notes': [
                    'Due to the assumption that H has a chi square distribution, the number of samples in each group must not be too small. A typical rule is that each sample must have at least 5 measurements. [2]']
                },
    'anova': {'Name': 'one way ANOVA',
              'Long': 'If a comparison is to be made of a normally distributed continuous parameter in more than two groups, analysis of variance (ANOVA) can be used. One example would be a study with three or more treatment arms. ANOVA is a generalization of the unpaired t-test. ANOVA only informs whether the groups differ, but does not say which groups differ. This requires methods of multiple testing.[3] [1]',
              'Short': 'The one-way ANOVA tests the null hypothesis that two or more groups have the same population mean. The test is applied to samples from two or more groups, possibly with differing sizes. [2]',
              'Null Hypothesis': 'The null hypothesis is that two or more groups have the same population mean.',
              'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html#scipy.stats.f_oneway',
              'Assumptions': {'paired': None,
                              'normality': True,
                              'equal-variance': True,  # homoscedasticity
                              'num_groups': None,  # Can be more than 2
                              'alternative': None,
                              'min_sample_size': 3},
              'Data': {'normality': None,
                       'equal-variance': None,
                       },
              },
    'tukeyhsd': {'Name': 'Tukey’s honestly significant difference (HSD)',
                 'Long': 'The test statistic, which is computed for every possible pairing of samples, is simply the difference between the sample means. For each pair, the p-value is the probability under the null hypothesis (and other assumptions; see notes) of observing such an extreme value of the statistic, considering that many pairwise comparisons are being performed. Confidence intervals for the difference between each pair of means are also available. [2]',
                 'Short': 'Tukey’s honestly significant difference (HSD) test performs pairwise comparison of means for a set of samples. Whereas ANOVA (e.g. f_oneway) assesses whether the true means underlying each sample are identical, Tukey’s HSD is a post hoc test used to compare the mean of each sample to the mean of each other sample. [2]',
                 'Null Hypothesis': 'The null hypothesis is that the distributions underlying the samples all have the same mean',
                 'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.tukey_hsd.html#scipy.stats.tukey_hsd',
                 'Assumptions': {'paired': None,
                                 'normality': True,
                                 'equal-variance': True,  # homoscedasticity
                                 'num_groups': None,  # Can be more than 2
                                 'alternative': None,
                                 'min_sample_size': 3},
                 'Data': {'normality': None,
                          'equal-variance': None,
                          },
                 'Notes': ['The observations are independent within and among groups. [2]',
                           'The observations within each group are normally distributed. [2]',
                           'The distributions from which the samples are drawn have the same finite variance.[2]']
                 },
    'levene': {'Name': 'Levene test for equal variances',
               'Long': "Levene's test ( Levene 1960) is used to test if k samples have equal variances. Equal variances across samples is called homogeneity of variance. Some statistical tests, for example the analysis of variance, assume that variances are equal across groups or samples. The Levene test can be used to verify that assumption. https://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm",
               'Short': 'The Levene test tests the null hypothesis that all input samples are from populations with equal variances. Levene’s test is an alternative to Bartlett’s test bartlett in the case where there are significant deviations from normality. [2]',
               'Null Hypothesis': 'The null hypothesis is that samples have the same variance.',
               'Link': 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.levene.html#scipy.stats.levene',
               'Assumptions': {'paired': None,
                               'normality': None,
                               'equal-variance': None,  # homoscedasticity
                               'num_groups': None,  # Can be more than 2
                               'alternative': None,
                               'min_sample_size': 3},
               'Data': {'normality': None,
                        'equal-variance': None,
                        }
               },
}

class VisException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


class Vis:

    """

    #font.serif      : DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman,
    New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L,
    Times New Roman, Times, Palatino, Charter, serif
#font.sans-serif : DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif,

 Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif

    """

    def __init__(self):
        pass

    def perform_stats(self):
        print(None)

    def get_assumptions(self, stat_name: str):


        references = ['[1] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2996580/', '[2] https://docs.scipy.org/doc/scipy/reference/stats.html#statistical-tests']

    def output_assumptions(self, test_name: str):
        # assumption rows: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2996580/
        assumptions = [f'Assumptions:',
                       f'1: {}']


    def write_stats_file(self):
        print(None)