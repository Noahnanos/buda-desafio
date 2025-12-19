from typing import Dict
from pydantic import BaseModel, Field

class PortfolioRequest(BaseModel):
    portafolio: Dict[str, float] = Field(
        ...,
        description="Dictionary of cryptocurrencies and their amounts (e.g., {'BTC': 0.5, 'ETH': 2.0})",
        json_schema_extra={"example": {"BTC": 0.5, "ETH": 2.0, "USDT": 1000}}
    )
    fiat_currency: str = Field(
        ...,
        description="Target fiat currency (CLP, PEN, COP)",
        pattern="^((?i)CLP|PEN|COP)$", 
        json_schema_extra={"example": "CLP"}
    )

class PortfolioValue(BaseModel):
    total_value: float
    currency: str
    breakdown: Dict[str, float] = Field(description="Value of each asset in the target fiat currency")
