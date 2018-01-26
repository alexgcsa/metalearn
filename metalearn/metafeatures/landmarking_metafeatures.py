import time
import numpy as np

from .metafeatures_base import MetafeaturesBase

from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, cohen_kappa_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

'''

Compute Landmarking meta-features according to Reif et al. 2012.
The accuracy values of the following simple learners are used: 
Naive Bayes, Linear Discriminant Analysis, One-Nearest Neighbor, 
Decision Node, Random Node.

'''

class LandmarkingMetafeatures(MetafeaturesBase):

    def __init__(self):
        
        function_dict = {
            'NaiveBayesErrRate': self._get_naive_bayes,
            'NaiveBayesKappa': self._get_naive_bayes,
            'kNN1NErrRate': self._get_knn_1,
            'kNN1NKappa': self._get_knn_1,
            'DecisionStumpErrRate': self._get_decision_stump,
            'DecisionStumpKappa': self._get_decision_stump
        }

        dependencies_dict = {
            'NaiveBayesErrRate': [],
            'NaiveBayesKappa': [],
            'kNN1NErrRate': [],
            'kNN1NKappa': [],
            'DecisionStumpErrRate': [],
            'DecisionStumpKappa': []
        }

        super().__init__(function_dict, dependencies_dict)

    def _run_pipeline(self, X, Y, estimator, label):        
        pipe = Pipeline([('Imputer', preprocessing.Imputer(missing_values='NaN', strategy='mean', axis=0)),
                         ('classifiers', estimator)])
        accuracy_scorer = make_scorer(accuracy_score)
        kappa_scorer = make_scorer(cohen_kappa_score)
        scores = cross_validate(pipe, X.as_matrix(), Y.as_matrix(), 
            cv=10, n_jobs=-1, scoring={'accuracy': accuracy_scorer, 'kappa': kappa_scorer})
        err_rate = 1. - np.mean(scores['test_accuracy'])
        kappa = np.mean(scores['test_kappa'])

        return {
            label + 'ErrRate': err_rate,
            label + 'Kappa': kappa
        }

    def _get_naive_bayes(self, X, Y):
        values_dict = self._run_pipeline(X, Y, GaussianNB(), 'NaiveBayes')
        return {
            'NaiveBayesErrRate': values_dict['NaiveBayesErrRate'],
            'NaiveBayesKappa': values_dict['NaiveBayesKappa']
        }

    def _get_knn_1(self, X, Y):
        values_dict = self._run_pipeline(X, Y, KNeighborsClassifier(n_neighbors = 1), 'kNN1N')
        return {
            'kNN1NErrRate': values_dict['kNN1NErrRate'],
            'kNN1NKappa': values_dict['kNN1NKappa']
        }

    def _get_decision_stump(self, X, Y):
        values_dict = self._run_pipeline(X, Y, DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=1, random_state=0), 'DecisionStump')
        return {
            'DecisionStumpErrRate': values_dict['DecisionStumpErrRate'],
            'DecisionStumpKappa': values_dict['DecisionStumpKappa']
        }

    def get_landmarking_metafeatures(attributes, data, X, Y):
        metafeatures = {}                
        metafeatures['linear_discriminant_analysis'], metafeatures['linear_discriminant_analysis_time'] = pipeline(X, Y, LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto'))         
        metafeatures['decision_node'], metafeatures['decision_node_time']= pipeline(X, Y, DecisionTreeClassifier(criterion='entropy', splitter='best', 
                                                                                                                 max_depth=1, random_state=0)) 
        metafeatures['random_node'], metafeatures['random_node_time'] = pipeline(X, Y, DecisionTreeClassifier(criterion='entropy', splitter='random',
                                                                                                              max_depth=1, random_state=0))        
        return metafeatures