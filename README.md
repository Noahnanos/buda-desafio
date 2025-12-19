# Buda.com Crypto Portfolio API

REST API to calculate the valuation of a cryptocurrency portfolio using real-time prices from Buda.com.

## Features
- Valuation in CLP, PEN, and COP.
- Real-time price fetching from Buda.com API v2.
- Input validation using Pydantic.
- Error handling for missing markets or network issues.

## Requirements
- Python 3.9+
- Dependencies listed in `requirements.txt`

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Documentation
Interactive API docs (Swagger UI) are available at: `http://127.0.0.1:8000/docs`

### Example Request

**POST** `/api/v1/portfolio/value`

```json
{
  "portfolio": {
    "BTC": 0.5,
    "ETH": 2.0,
    "USDT": 1000
  },
  "fiat_currency": "CLP"
}
```

### Example Response

```json
{
  "total_value": 45000000.0,
  "currency": "CLP",
  "breakdown": {
    "BTC": 30000000.0,
    "ETH": 14000000.0,
    "USDT": 1000000.0
  }
}
```

## Testing

Run unit and integration tests:

```bash
pytest test_main.py -v
```
