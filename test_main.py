from fastapi.testclient import TestClient
from main import app
from services import BudaService
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Buda.com Portafolio API. Visit /docs for documentation."}

def test_calculate_portafolio_integration():
    """
    Integration test mocking the external Buda API call to avoid network dependency during test.
    """
    mock_response_btc = {
        "ticker": {
            "last_price": ["50000000.0", "CLP"]
        }
    }
    mock_response_eth = {
        "ticker": {
            "last_price": ["3000000.0", "CLP"]
        }
    }

    def side_effect(url, timeout=5):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        
        if "btc-clp" in url:
            mock_resp.json.return_value = mock_response_btc
        elif "eth-clp" in url:
            mock_resp.json.return_value = mock_response_eth
        else:
            mock_resp.raise_for_status.side_effect = Exception("Not Found")
            
        return mock_resp

    with patch('requests.get', side_effect=side_effect):
        payload = {
            "portafolio": {
                "BTC": 0.5,
                "ETH": 2.0
            },
            "fiat_currency": "CLP"
        }
        response = client.post("/api/v1/portafolio/value", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        expected_total = 31000000.0
        assert data["total_value"] == expected_total
        assert data["currency"] == "CLP"
        assert data["breakdown"]["BTC"] == 25000000.0
        assert data["breakdown"]["ETH"] == 6000000.0

def test_invalid_fiat_validation():
    payload = {
        "portfolio": {"BTC": 1},
        "fiat_currency": "INVALID"
    }
    response = client.post("/api/v1/portafolio/value", json=payload)
    assert response.status_code == 422  

def test_service_market_not_found():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Network Error")
        
        price = BudaService.get_market_price("UNKNOWN", "CLP")
        assert price == 0.0
