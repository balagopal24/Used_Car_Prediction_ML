# from pydantic import BaseModel
# from typing import Optional


# class CarFeatures(BaseModel):
#     brand: str
#     fuel: str
#     transmission: str
#     owner: str
#     seller_type: Optional[str] = "Individual"
#     year: int
#     km_driven: int
#     engine_cc: Optional[float] = None
#     mileage_kmpl: Optional[float] = None
#     seats: Optional[int] = 5


# class PredictionResponse(BaseModel):
#     predicted_price: float
#     model_version: str = "v1-linear-regression"


# class ListingOut(BaseModel):
#     id: int
#     brand: Optional[str]
#     model: Optional[str]
#     year: Optional[int]
#     km_driven: Optional[int]
#     fuel_type: Optional[str]
#     price_actual: Optional[float]
#     price_predicted: Optional[float]
#     ingested_at: str

from pydantic import BaseModel
from typing import Optional


class CarFeatures(BaseModel):
    brand: str
    fuel: str
    transmission: str
    seller_type: Optional[str] = "Individual"
    year: int
    km_driven: int
    engine_cc: Optional[float] = None
    mileage_kmpl: Optional[float] = None
    seats: Optional[int] = 5


class PredictionResponse(BaseModel):
    predicted_price: float
    model_version: str = "v1-linear-regression"


class ListingOut(BaseModel):
    id: int
    brand: Optional[str]
    model: Optional[str]
    year: Optional[int]
    km_driven: Optional[int]
    fuel_type: Optional[str]
    price_actual: Optional[float]
    price_predicted: Optional[float]
    ingested_at: str