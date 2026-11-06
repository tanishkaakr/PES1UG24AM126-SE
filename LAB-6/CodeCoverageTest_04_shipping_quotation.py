import pytest
from shipping_quote import process_shipments, monitor_container_pressures

# --- LINE COVERAGE TESTS FOR process_shipments ---

def test_invalid_input_types():
    with pytest.raises(ValueError, match="Invalid shipments list or handling fee"):
        process_shipments("not a list", 10.0)
    with pytest.raises(ValueError, match="Invalid shipments list or handling fee"):
        process_shipments([], -5.0)

def test_unapproved_manifest():
    shipments = [{"manifest_approved": False}]
    result = process_shipments(shipments, 10.0)
    assert result == {"total_quote": 0.0, "status": "NO_CARGO"}

def test_air_mode_heavy_weight_express():
    shipments = [{
        "manifest_approved": True,
        "mode": "air",
        "is_fragile": False,
        "express_priority": True,
        "packages": [{"weight_kg": 40, "is_hazmat": False}]
    }]
    # handling_fee = 20.0
    # package cost = 40 * (12.0 * 1.5) = 720.0
    # shipment_cost = 740.0 * 1.25 = 925.0
    result = process_shipments(shipments, 20.0)
    assert result == {"total_quote": 925.0, "status": "CLEARED"}

def test_invalid_mode():
    shipments = [{
        "manifest_approved": True,
        "mode": "sea",
        "packages": [{"weight_kg": 10, "is_hazmat": False}]
    }]
    result = process_shipments(shipments, 10.0)
    assert result == {"total_quote": 0.0, "status": "NO_CARGO"}

def test_invalid_weight_and_hazmat_non_fragile():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": False,
        "packages": [
            {"weight_kg": -1, "is_hazmat": False},
            {"weight_kg": 10, "is_hazmat": True}
        ]
    }]
    # handling_fee = 10.0 + 50.0 = 60.0
    result = process_shipments(shipments, 10.0)
    assert result == {"total_quote": 60.0, "status": "CLEARED"}

def test_hazmat_and_fragile_break():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": True,
        "packages": [{"weight_kg": 10, "is_hazmat": True}]
    }]
    # fragile + hazmat resets shipment_cost to 0.0
    result = process_shipments(shipments, 10.0)
    assert result == {"total_quote": 0.0, "status": "NO_CARGO"}

def test_flagged_review_status():
    shipments = [
        {"manifest_approved": True, "mode": "invalid"},
        {"manifest_approved": True, "mode": "invalid"},
        {"manifest_approved": True, "mode": "invalid"},
        {"manifest_approved": True, "mode": "invalid"}
    ]
    result = process_shipments(shipments, 10.0)
    assert result["status"] == "FLAGGED_REVIEW"


# --- LINE COVERAGE TESTS FOR monitor_container_pressures ---

def test_pressures_no_data():
    assert monitor_container_pressures([]) == "NO_DATA"

def test_pressures_leak_detected():
    logs = [[15.0, 13.0, 12.0]]
    assert monitor_container_pressures(logs) == "LEAK_DETECTED"

def test_pressures_stable():
    logs = [[15.0, 13.0, 15.0]]
    assert monitor_container_pressures(logs) == "STABLE"