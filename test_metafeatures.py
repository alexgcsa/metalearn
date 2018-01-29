import json

import numpy as np

import openml
import pandas as pd

from arff2pandas import a2p


from metalearn.metafeatures.simple_metafeatures import SimpleMetafeatures
from metalearn.metafeatures.statistical_metafeatures import StatisticalMetafeatures
from metalearn.metafeatures.information_theoretic_metafeatures import InformationTheoreticMetafeatures
from metalearn.metafeatures.landmarking_metafeatures import LandmarkingMetafeatures


def import_openml_dataset(id=1):
    # get a dataset from openml using a dataset id
    dataset = openml.datasets.get_dataset(id)
    # get the metafeatures from the dataset
    omlMetafeatures = dataset.qualities
    # get X, Y, and attributes from the dataset
    X, Y, attributes = dataset.get_data(target=dataset.default_target_attribute, return_attribute_names=True)

    # create datafrom object from X,Y, and attributes
    dataframe = pd.DataFrame(X, columns=attributes)
    dataframe = dataframe.assign(target=pd.Series(Y))

    # format attributes
    for i in range(len(X[0])):
        attributes[i] = (attributes[i], str(type(X[0][i])))
        # set types of attributes (column headers) as well as the names

    return dataframe, omlMetafeatures

def compare_with_openml(dataframe,omlMetafeatures):
    # get metafeatures from dataset using our metafeatures
    print("\nopenml Metafeatures: \n",omlMetafeatures,"\n\n")
    metafeatures = extract_metafeatures(dataframe)
    print("\nOur Metafeatures: \n",metafeatures,"\n\n")

    mfDict ={}
    mfDict['EquivalentNumberOfAtts'] = 'EquivalentNumberOfFeatures', 1
    mfDict['MeanCardinalityOfNominalAttributes'] = 'MeanCardinalityOfNominalFeatures', 1
    mfDict['StdevCardinalityOfNominalAttributes'] = 'StdevCardinalityOfNominalFeatures', 1
    mfDict['MaxCardinalityOfNominalAttributes'] = 'MaxCardinalityOfNominalFeatures', 1
    mfDict['MinCardinalityOfNominalAttributes'] = 'MinCardinalityOfNominalFeatures', 1
    mfDict['MeanCardinalityOfNumericAttributes'] = 'MeanCardinalityOfNumericFeatures', 1
    mfDict['StdevCardinalityOfNumericAttributes'] = 'StdevCardinalityOfNumericFeatures', 1
    mfDict['MaxCardinalityOfNumericAttributes'] = 'MaxCardinalityOfNumericFeatures', 1
    mfDict['MinCardinalityOfNumericAttributes'] = 'MinCardinalityOfNumericFeatures', 1
    mfDict['MinorityClassPercentage'] = 'MinClassProbability', 100
    mfDict['MajorityClassPercentage'] = 'MaxClassProbability', 100
    mfDict['MaxMeansOfNumericAtts'] = 'MaxMeansOfNumericFeatures', 1
    mfDict['MaxStdevOfNumericAtts'] = 'MaxStdevOfNumericFeatures', 1
    mfDict['MaxSkewnessOfNumericAtts'] = 'MaxSkewnessOfNumericFeatures', 1
    mfDict['MaxKurtosisOfNumericAtts'] = 'MaxKurtosisOfNumericFeatures', 1
    mfDict['MinMeansOfNumericAtts'] = 'MinMeansOfNumericFeatures', 1
    mfDict['MinStdevOfNumericAtts'] = 'MinStdevOfNumericFeatures', 1
    mfDict['MinSkewnessOfNumericAtts'] = 'MinSkewnessOfNumericFeatures', 1
    mfDict['MinKurtosisOfNumericAtts'] = 'MinKurtosisOfNumericFeatures', 1
    mfDict['MeanMeansOfNumericAtts'] = 'MeanMeansOfNumericFeatures', 1
    mfDict['MeanStdevOfNumericAtts'] = 'MeanStdevOfNumericFeatures', 1
    mfDict['MeanSkewnessOfNumericAtts'] = 'MeanSkewnessOfNumericFeatures', 1
    mfDict['MeanKurtosisOfNumericAtts'] = 'MeanKurtosisOfNumericFeatures', 1
    mfDict['StdevMeansOfNumericAtts'] = 'StdevMeansOfNumericFeatures', 1
    mfDict['StdevStdevOfNumericAtts'] = 'StdevStdevOfNumericFeatures', 1
    mfDict['StdevSkewnessOfNumericAtts'] = 'StdevSkewnessOfNumericFeatures', 1
    mfDict['StdevKurtosisOfNumericAtts'] = 'StdevKurtosisOfNumericFeatures', 1
    mfDict['Quartile1MeansOfNumericAtts'] = 'Quartile1MeansOfNumericFeatures', 1
    mfDict['Quartile1StdevOfNumericAtts'] = 'Quartile1StdevOfNumericFeatures', 1
    mfDict['Quartile1SkewnessOfNumericAtts'] = 'Quartile1SkewnessOfNumericFeatures', 1
    mfDict['Quartile1KurtosisOfNumericAtts'] = 'Quartile1KurtosisOfNumericFeatures', 1
    mfDict['Quartile2MeansOfNumericAtts'] = 'Quartile2MeansOfNumericFeatures', 1
    mfDict['Quartile2StdevOfNumericAtts'] = 'Quartile2StdevOfNumericFeatures', 1
    mfDict['Quartile2SkewnessOfNumericAtts'] = 'Quartile2SkewnessOfNumericFeatures', 1
    mfDict['Quartile2KurtosisOfNumericAtts'] = 'Quartile2KurtosisOfNumericFeatures', 1
    mfDict['Quartile3MeansOfNumericAtts'] = 'Quartile3MeansOfNumericFeatures', 1
    mfDict['Quartile3StdevOfNumericAtts'] = 'Quartile3StdevOfNumericFeatures', 1
    mfDict['Quartile3SkewnessOfNumericAtts'] = 'Quartile3SkewnessOfNumericFeatures', 1
    mfDict['Quartile3KurtosisOfNumericAtts'] = 'Quartile3KurtosisOfNumericFeatures', 1
    mfDict['PercentageOfInstancesWithMissingValues'] = 'RatioOfInstancesWithMissingValues', 100
    mfDict['PercentageOfMissingValues'] = 'RatioOfMissingValues', 100
    mfDict['PercentageOfNumericFeatures'] = 'RatioOfNumericFeatures', 100
    mfDict['PercentageOfSymbolicFeatures'] = 'RatioOfNominalFeatures', 100


    sharedMf=[]
    exclusiveMf={}
    omlExclusiveMf={}
    for omlMetafeature in omlMetafeatures :
        # compare the names that are the same
        diff = 0
        if (metafeatures.get(omlMetafeature) != None):
            omlMetafeatureName = omlMetafeature
            omlMetafeatureValue = float(omlMetafeatures.get(omlMetafeature))
            metafeatureName = omlMetafeature
            metafeatureValue = float(metafeatures.get(omlMetafeature))
            diff = omlMetafeatureValue - metafeatureValue

            if (abs(diff) <= .05):
                equalString = "yes"
            else:
                equalString = "no"
            print(omlMetafeatureName + "\t" + str(omlMetafeatureValue) + "\t" + metafeatureName + "\t" + str(metafeatureValue) + "\t" + equalString)

        elif (mfDict.get(omlMetafeature) != None):
            metafeatureName, multiplier = mfDict.get(omlMetafeature)
            metafeatureValue = float(metafeatures.get(metafeatureName))
            omlMetafeatureName = omlMetafeature
            omlMetafeatureValue = float(omlMetafeatures.get(omlMetafeature))
            diff = omlMetafeatureValue - (metafeatureValue * multiplier)

            if (abs(diff) <= .05):
                equalString = "yes"
            else:
                equalString = "no"
            print(omlMetafeatureName + "\t" + str(omlMetafeatureValue) + "\t" + metafeatureName + "\t" + str(metafeatureValue) + "\t" + equalString)



        # compare the names that are different
        # if (mfDict.get(omlMetafeature) != None) :

        
        








def load_arff(infile_path):
    f = open(infile_path)
    dataframe = a2p.load(f)
    column_name = [name for name in list(dataframe.columns) if 'class@' in name][0]
    dataframe = dataframe.rename(index=str, columns={column_name: 'target'})
    return dataframe

def extract_metafeatures(dataframe):
    metafeatures = {}
    features_df = SimpleMetafeatures().compute(dataframe)
    for feature in features_df.columns:
        metafeatures[feature] = features_df[feature].as_matrix()[0]
    features_df = StatisticalMetafeatures().compute(dataframe)
    for feature in features_df.columns:
        metafeatures[feature] = features_df[feature].as_matrix()[0]
    features_df = InformationTheoreticMetafeatures().compute(dataframe)
    for feature in features_df.columns:
        metafeatures[feature] = features_df[feature].as_matrix()[0]
    features_df = LandmarkingMetafeatures().compute(dataframe)
    for feature in features_df.columns:
        metafeatures[feature] = features_df[feature].as_matrix()[0]
    return metafeatures

def main():
    for filename in ["./data/iris.arff", "./data/38_sick_train_data.csv"]:
    # for filename in ["./data/38_sick_train_data.csv"]:
    # for filename in ["./data/iris.arff"]:
        ext = filename.split(".")[-1]
        if ext == "arff":
            dataframe = load_arff(filename)
        elif ext == "csv":
            dataframe = pd.read_csv(filename)
            dataframe.rename(columns={"Class": "target"}, inplace=True)
        else:
            raise ValueError("file type '{}' not implemented")

        if "d3mIndex" in dataframe.columns:
            dataframe.drop(columns="d3mIndex", inplace=True)

        metafeatures = extract_metafeatures(dataframe)

        print(json.dumps(metafeatures, sort_keys=True, indent=4))
    print("tests finished")

if __name__ == "__main__":
    # print(compute_metafeatures("./iris.arff"))
    print("\n\n\n")
    dataframe, omlMetafeatures = import_openml_dataset()
    compare_with_openml(dataframe,omlMetafeatures)
    main()

