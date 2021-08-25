import pandas as pd
import numpy as np
import os
import tensorflow as tf
import functools

####### STUDENTS FILL THIS OUT ######
#Question 3
def reduce_dimension_ndc(df, ndc_df):
    df_new = pd.merge(df, ndc_df[['NDC_Code', 'Non-proprietary Name']],how="left",left_on='ndc_code',right_on='NDC_Code')
    df_new.rename(columns={"Non-proprietary Name": "generic_drug_name"}, inplace=True)
    return df_new

#Question 4
def select_first_encounter(df):
    '''
    df: pandas dataframe, dataframe with all encounters
    return:
        - first_encounter_df: pandas dataframe, dataframe with only the first encounter for a given patient
    '''
    df=df.sort_values('encounter_id')
    first_encounter_df=df.groupby('patient_nbr').head(1)
    return first_encounter_df 


#Question 6
def patient_dataset_splitter(df, patient_key='patient_nbr'):
    '''
    df: pandas dataframe, input dataset that will be split
    patient_key: string, column that is the patient id

    return:
     - train: pandas dataframe,
     - validation: pandas dataframe,
     - test: pandas dataframe,
    '''
    key_unique=df[patient_key].unique()
    nu=len(key_unique)
    train_i=int(nu*0.6)
    test_i=int(train_i+nu*0.2)
    train=df[df[patient_key].isin(key_unique[:train_i])].reset_index(drop=True)
    test=df[df[patient_key].isin(key_unique[train_i:test_i])].reset_index(drop=True)
    validation=df[df[patient_key].isin(key_unique[test_i:])].reset_index(drop=True)
    
    #sanity check
    if any( i in list(train[patient_key]) for i in list(test[patient_key])) or any(i in list(train[patient_key]) for i in list(validation[patient_key])) or any(i in list(test[patient_key]) for i in list(validation[patient_key])):
        raise Exception('Data Leakage!!')
    if (train[patient_key].nunique()+test[patient_key].nunique()+validation[patient_key].nunique()) != df[patient_key].nunique():
        raise Exception("Number of patients don't add up ")
    print(f"Len of df: {len(df)} \nLen of train : {len(train)} \nLen of test : {len(test)}\nLen of validation : {len(validation)}")

    
    return train, validation, test
#Question 7

def create_tf_categorical_feature_cols(categorical_col_list,
                              vocab_dir='./diabetes_vocab/'):
    output_tf_list = []
    for c in categorical_col_list:
        vocab_file_path = os.path.join(vocab_dir,  c + "_vocab.txt")
        tf_categorical_feature_column = tf.feature_column.categorical_column_with_vocabulary_file(key = c, vocabulary_file = vocab_file_path, num_oov_buckets=0)       
        if c == 'primary_diagnosis_code':
            dims = 10
            cat_col = tf.feature_column.embedding_column(tf_categorical_feature_column, dimension=dims)        
        else:
            cat_col = tf.feature_column.indicator_column(tf_categorical_feature_column)      
        output_tf_list.append(cat_col)
    return output_tf_list

#Question 8
def normalize_numeric_with_zscore(col, mean, std):
    '''
    This function can be used in conjunction with the tf feature column for normalization
    '''
    return (col - mean)/std



def create_tf_numeric_feature(col, MEAN, STD, default_value=0):
    '''
    col: string, input numerical column name
    MEAN: the mean for the column in the training data
    STD: the standard deviation for the column in the training data
    default_value: the value that will be used for imputing the field

    return:
        tf_numeric_feature: tf feature column representation of the input field
    '''
    normalizer = functools.partial(normalize_numeric_with_zscore, mean=MEAN, std=STD)
    tf_numeric_feature=tf.feature_column.numeric_column(key=col, default_value = default_value, normalizer_fn=normalizer, dtype=tf.float64)
    return tf_numeric_feature

#Question 9
def get_mean_std_from_preds(diabetes_yhat):
    '''
    diabetes_yhat: TF Probability prediction object
    '''
    m = np.mean(diabetes_yhat)
    s = np.std(diabetes_yhat)
    return m, s

# Question 10
def get_student_binary_prediction(df, col):
    '''
    df: pandas dataframe prediction output dataframe
    col: str,  probability mean prediction field
    return:
        student_binary_prediction: pandas dataframe converting input to flattened numpy array and binary labels
    '''
    return student_binary_prediction
