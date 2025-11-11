# Backend Server + Upload endpoint

from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from app.data_loader import load_user_data
from app.data_cleaner import clean_dataframe, convert_numpy
from app.analysis import get_compatible_features, generate_chart
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import numpy as np
import traceback
import json
import plotly.express as px
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.get("/")
async def root():
    return {"message": "Auto-Analyzer API is running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV/Excel file and return basic dataset info.
    No cleaning is applied yet.
    """
    try:
        df, filename = await load_user_data(file)

        # Basic dataset info
        num_rows, num_columns = df.shape
        columns = df.columns.tolist()
        duplicates = int(df.duplicated().sum())
        missing_per_column = df.isna().sum().to_dict()

        # Detect outliers (optional, only report)
        numeric_cols = df.select_dtypes(include=["int", "float"]).columns
        outliers_report = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers_report[col] = int(((df[col] < lower) | (df[col] > upper)).sum())

        return {
            "filename": filename,
            "num_rows": num_rows,
            "num_columns": num_columns,
            "columns": columns,
            "duplicates": duplicates,
            "missing_values": missing_per_column,
            "outliers_detected": outliers_report,
        }

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

@app.post("/clean/")
async def apply_cleaning(file: UploadFile = File(...), remove_outliers: str = Form("False"), outlier_method: str = Form("IQR")):
    try:
        remove_outliers = remove_outliers.lower() == "true"
        df, filename = await load_user_data(file)
        clean_df, report = clean_dataframe(df, drop_outliers=remove_outliers, outlier_method=outlier_method)
        report = convert_numpy(report)
        cleaned_data = clean_df.to_dict(orient="records")
        return {
            "filename": filename,
            "cleaned_report": report,
            "cleaned_data": cleaned_data
        }
    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }

class AnalysisRequest(BaseModel):
    cleaned_data: list[Dict]
    chart_type: str

@app.post("/features/")
async def get_features(request: AnalysisRequest):
    try:
        df = pd.DataFrame(request.cleaned_data)
        features = get_compatible_features(df, request.chart_type)
        return{
            "X_axis": features["x"],
            "Y_axis": features["y"],
            "Group": features["group"]
        }
    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
    
@app.post("/analysis/")
async def generate_graph(Data: str = Form(...), chart_type: str = Form(...), X_axis: str = Form(...), Y_axis: str = Form(...), Group: str = Form(...)):
    try:
        df = pd.DataFrame(json.loads(Data)["cleanData"])
        graph = generate_chart(df, chart_type, X_axis, Y_axis, Group)
        graph_jason = graph.to_json()
        return{
            "Graph": json.loads(graph_jason)
        }
    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
