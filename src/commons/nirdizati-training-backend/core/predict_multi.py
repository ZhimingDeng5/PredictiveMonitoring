import pickle
import sys

import pandas as pd


def predict_multi(test_file, pickle_model, save_loc):

    # read in pickle file with predictive model and metadata
    with open(pickle_model, 'rb') as f:
        pipelines = pickle.load(f)
        bucketer = pickle.load(f)
        dataset_manager = pickle.load(f)

    # detailed_results_file = "%s-results.csv" % save_loc

    ##### MAIN PART ######

    dtypes = {col: "str" for col in dataset_manager.dynamic_cat_cols + dataset_manager.static_cat_cols +
            [dataset_manager.case_id_col, dataset_manager.timestamp_col]}
    for col in dataset_manager.dynamic_num_cols + dataset_manager.static_num_cols:
        dtypes[col] = "float"

    # if dataset_manager.mode == "regr":
    #     dtypes[dataset_manager.label_col] = "float"  # if regression, target value is float
    # else:
    #     dtypes[dataset_manager.label_col] = "str"  # if classification, preserve and do not interpret dtype of label

    test = pd.read_csv(test_file, sep=",|;", dtype=dtypes, engine="python")
    #test = test.drop(label_col, axis = 1)
    test[dataset_manager.timestamp_col] = pd.to_datetime(test[dataset_manager.timestamp_col], dayfirst=True)

    # get bucket for each test case
    bucket_assignments_test = bucketer.predict(test)

    detailed_results = pd.DataFrame()

    # use appropriate classifier for each bucket of test cases
    for bucket in set(bucket_assignments_test):
        relevant_cases_bucket = dataset_manager.get_indexes(test)[bucket_assignments_test == bucket]
        dt_test_bucket = dataset_manager.get_relevant_data_by_indexes(test, relevant_cases_bucket)

        if len(relevant_cases_bucket) == 0:
            continue

        elif bucket not in pipelines:
            sys.exit("No matching model has been trained!")

        else:
            # make actual predictions
            preds_bucket = pipelines[bucket].predict_proba(dt_test_bucket)
            unfiltered_preds_bucket = preds_bucket

        if preds_bucket.ndim == 1:
            preds_bucket = preds_bucket.clip(min=0)  # if remaining time is predicted to be negative, make it zero
        else: # classification
            preds_bucket = preds_bucket.idxmax(axis=1)

        case_ids = list(dt_test_bucket.groupby(dataset_manager.case_id_col).first().index)
        current_results = pd.DataFrame({dataset_manager.case_id_col: case_ids, dataset_manager.label_col: preds_bucket})
        if dataset_manager.label_col == "remtime":  # remaining time - output predicted completion time instead
            last_timestamps = test.groupby(dataset_manager.case_id_col)[dataset_manager.timestamp_col].apply(lambda x: x.max())
            last_timestamps = pd.DataFrame({dataset_manager.case_id_col: last_timestamps.index, 'last-timestamp': last_timestamps.values})
            current_results = pd.merge(current_results, last_timestamps, on=dataset_manager.case_id_col)
            # current_results['predicted-completion'] = pd.to_datetime(current_results['last-timestamp']) + pd.to_timedelta(current_results['remtime'].round(), unit='s')
            current_results['predicted-completion'] = pd.to_datetime(current_results['last-timestamp']) + pd.to_timedelta(current_results['remtime'], unit='d')
            current_results['predicted-completion'] = current_results['predicted-completion'].map(lambda t: t.strftime('%Y-%m-%d %H:%M'))
            # current_results = current_results.drop(["last-timestamp", "remtime"], axis=1)
        else: # label - append probability
            current_results['probability'] = unfiltered_preds_bucket.max(axis = 1)

        detailed_results = pd.concat([detailed_results, current_results])

    # aggregate data collection
    aggregate_results = {}

    start_timestamps = test.groupby(dataset_manager.case_id_col)[dataset_manager.timestamp_col].min()
    end_timestamps = test.groupby(dataset_manager.case_id_col)[dataset_manager.timestamp_col].max()
    case_durations = end_timestamps - start_timestamps

    # log statistics
    aggregate_results['Total cases'] = len(detailed_results)
    if dataset_manager.label_col == "remtime":
        aggregate_results['Running cases'] = len(detailed_results[detailed_results['remtime'] > 0.01])
        aggregate_results['Completed cases'] = aggregate_results['Total cases'] - aggregate_results['Running cases']
        detailed_results = detailed_results.drop(["last-timestamp", "remtime"], axis=1)
    if 'case:variant' in test.columns:
        aggregate_results['Case variants'] = test['case:variant'].max()
    elif 'Variant index' in test.columns:
        aggregate_results['Case variants'] = test['Variant index'].max()
    aggregate_results['Average case length'] = test.groupby(dataset_manager.case_id_col)[dataset_manager.case_id_col].count().mean()
    aggregate_results['Completed events'] = len(test)
    aggregate_results['Activities'] = test['Activity'].nunique()

    # temporal statistics
    aggregate_results['Start of log'] = str(test[dataset_manager.timestamp_col].min())
    aggregate_results['End of log'] = str(test[dataset_manager.timestamp_col].max())

    aggregate_results['Min. case duration'] = str(case_durations.min())
    aggregate_results['Median case duration'] = str(case_durations.median())
    aggregate_results['Average case duration'] = str(case_durations.mean())
    aggregate_results['Max. case duration'] = str(case_durations.max())
    # print(aggregate_results)

    # detailed_results.to_csv(detailed_results_file, sep=",", index=False)
    return detailed_results, aggregate_results
