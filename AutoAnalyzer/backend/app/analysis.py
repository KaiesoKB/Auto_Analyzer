# Analyzes the df through graph generation and revealing appropriate features for graph selection

import pandas as pd
import plotly.express as px

def get_compatible_features(df, chart_type):
    numeric_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    compatible_features = {}

    if chart_type in ["Bar", "Boxplot", "Pie"]:
        cat_cols += bool_cols
    else:
        numeric_cols += bool_cols

    if chart_type == "Bar":
        compatible_features["x"] = cat_cols + date_cols
        compatible_features["y"] = numeric_cols
        compatible_features["group"] = cat_cols
    elif chart_type == "Line":
        compatible_features["x"] = numeric_cols + date_cols
        compatible_features["y"] = numeric_cols
        compatible_features["group"] = cat_cols
    elif chart_type == "Scatterplot":
        compatible_features["x"] = numeric_cols + date_cols
        compatible_features["y"] = numeric_cols
        compatible_features["group"] = cat_cols
    elif chart_type == "Histogram":
        compatible_features["x"] = numeric_cols
        compatible_features["y"] = None
        compatible_features["group"] = None
    elif chart_type == "Boxplot":
        compatible_features["x"] = cat_cols + date_cols
        compatible_features["y"] = numeric_cols
        compatible_features["group"] = cat_cols
    elif chart_type == "Heatmap":
        compatible_features["x"] = None
        compatible_features["y"] = None
        compatible_features["group"] = None
    elif chart_type == "Pairplot":
        compatible_features["x"] = None
        compatible_features["y"] = None
        compatible_features["group"] = df.columns.tolist()
    elif chart_type == "Pie":
        compatible_features["x"] = cat_cols
        compatible_features["y"] = numeric_cols
        compatible_features["group"] = None
    else:
        raise ValueError(f"Unsupport Chart Type: {chart_type}")
    
    return compatible_features
    
def generate_chart(df, chart_type, x=None, y=None, group=None):
    if chart_type == "Bar":
        fig = px.bar(df, x=x, y=y, color=group)
    elif chart_type == "Line":
        fig = px.line(df, x=x, y=y, color=group)
    elif chart_type == "Scatterplot":
        fig = px.scatter(df, x=x, y=y, color=group)
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=x, y=y, color=group)
    elif chart_type == "Boxplot":
        fig = px.box(df, x=x, y=y, color=group)
    elif chart_type == "Heatmap":
        corr = df.corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    elif chart_type == "Pairplot":
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        fig = px.scatter_matrix(df, dimensions=numeric_cols, color=group if group in df.columns else None)
    elif chart_type == "Pie":
        fig = px.pie(df, names=x, values=y, color=group)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    return fig
    
    
    


