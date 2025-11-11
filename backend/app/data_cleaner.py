# Cleans uploaded file in the form of a df

import pandas as pd
import numpy as np
import re

def standardize_cols_name(df):
    df.columns = (
        df.columns
        .str.replace(u'\xa0', ' ', regex=True)
        .str.strip()
        .str.lower()
        .str.replace('[^a-zA-Z0-9_ ]', '', regex=True)
        .str.replace(' ', '_')
    )
    return df, df.columns.to_list()

def drop_duplicates(df):
    num_duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    return df,int(num_duplicate_rows)

def drop_useless_rows(df):
    num_all_null_rows = df.isnull().all(axis=1).sum()
    df = df.dropna(how='all').reset_index(drop=True)
    return df, int(num_all_null_rows)

def numeric_cols_confirm(df):
    converted_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try conversion
            converted = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
            
            # If successful (at least one valid number), apply conversion
            if converted.notna().any():
                df[col] = converted
                converted_cols.append(df[col])
    return df, list(set(converted_cols))

def drop_useless_columns(df):
    null_limit = 50
    removed_cols = []
    high_null_cols = {}

    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
            continue
         
        col_null_count = df[col].isna().sum()
        col_null_ratio = (col_null_count/len(df)) * 100
        if col_null_ratio > null_limit:
            high_null_cols[col] = col_null_ratio
            continue
    
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    removed_cols.extend(constant_cols)

    id_like_cols = [col for col in df.columns if df[col].dtype != 'float' and df[col].nunique() == len(df) and 'id' in col.lower()]
    removed_cols.extend(id_like_cols)

    high_card_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() / len(df) > 0.95 and 'date' not in col.lower()]
    removed_cols.extend(high_card_cols)
            
    df = df.drop(columns=set(removed_cols), errors='ignore')
    return df, list(set(removed_cols)), high_null_cols

def handle_missing_values(df):
    num_values_imputed = 0
    for col in df.columns:
        num_values_imputed += df[col].isna().sum()
        if df[col].dtype != "object":
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna("unknown", inplace=True)
    return df, int(num_values_imputed)

def remove_outliers_func(df, method = 'IQR'):
    outliers_count = {}
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns

    mask = pd.Series(True, index=df.index)
    for col in numeric_cols:
        if method == 'IQR':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - (1.5 * IQR)
            upper = Q3 + (1.5 * IQR)
        elif method == 'Z-Score':
            mean = df[col].mean()
            std = df[col].std()
            lower = mean - 3*std
            upper = mean + 3*std
        else:
            raise ValueError("Method must be 'IQR' or 'Z-Score'")
        
        outliers_count[col] = ((df[col] < lower) | (df[col] > upper)).sum()
        mask &= (df[col] >= lower) & (df[col] <= upper)
    
    df_filtered = df[mask].reset_index(drop=True)
    return df_filtered, outliers_count

def clean_dataframe(df, drop_outliers=False, outlier_method='IQR'):
    report = {}
    df, report['standardized_columns'] = standardize_cols_name(df)
    df, report['duplicates_removed'] = drop_duplicates(df)
    df, report['useless_rows_removed'] = drop_useless_rows(df)
    df, removed_cols, high_null_cols = drop_useless_columns(df)
    report['columns_dropped'] = removed_cols
    report['high_null_cols'] = high_null_cols

    df, report['missing_values_imputed'] = handle_missing_values(df)
    report['outliers_detected'] = {}
    if drop_outliers:
        df, report['outliers_detected'] = remove_outliers_func(df, method=outlier_method)
    else:
        report['outliers_detected'] = {}
    
    report['preview'] = df.head(10).to_dict(orient='records')
    report['num_rows'] = len(df)
    report['num_columns'] = len(df.columns)
    report['columns'] = df.columns.tolist()

    return df, report

def convert_numpy(obj):
    """Recursively convert numpy types to Python native types."""
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


# previously:
# outliers:
# rowId=0
# postal_code=0
# sales=1167
# quantity=122
# discount=817
# profit=1124