from fastapi import FastAPI
from models import PortfolioRequest, PortfolioValue
from services import BudaService

app = FastAPI(
    title="Buda.com Portfolio Valuator",
    description="API to calculate the value of a crypto portfolio using Buda.com market prices.",
    version="1.0.0"
)

@app.post("/api/v1/portfolio/value", response_model=PortfolioValue)
async def calculate_portfolio(request: PortfolioRequest):
    """
    Calculate the total value of a cryptocurrency portfolio in a specific fiat currency.
    """
    fiat = request.fiat_currency.upper()
    
    total_value, breakdown = BudaService.calculate_portfolio_value(request.portfolio, fiat)
    
    return PortfolioValue(
        total_value=total_value,
        currency=fiat,
        breakdown=breakdown
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Buda.com Portfolio API. Visit /docs for documentation."}
