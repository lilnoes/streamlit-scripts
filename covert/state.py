from pydantic import BaseModel
import pandas as pd


class State(BaseModel):
    df: pd.DataFrame
