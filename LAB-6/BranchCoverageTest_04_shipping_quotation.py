import pytest
from shipping_quote import process_shipments, monitor_container_pressures

# --- BRANCH COVERAGE TESTS FOR process_shipments ---

def test_branch_validation_combinations():
    # True for valid list, True for negative handling fee -> raises
    with pytest.raises(ValueError):
        process_shipments([], -1.0)
    # False for list check -> raises
    with pytest.raises(ValueError):
        process_shipments("invalid", 5.0)

def test_branch_manifest_approved_toggle():
    shipments = [
        {"manifest_approved": False},
        {"manifest_approved": True, "mode": "ground", "packages": [{"weight_kg": 5, "is_hazmat": False}]}
    ]
    result = process_shipments(shipments, 10.0)
    assert result == {"total_quote": 30.0, "status": "CLEARED"}

def test_branch_transport_modes():
    # Air mode
    s_air = [{"manifest_approved": True, "mode": "air", "packages": [{"weight_kg": 10, "is_hazmat": False}]}]
    assert process_shipments(s_air, 0.0)["total_quote"] == 120.0
    
    # Ground mode
    s_ground = [{"manifest_approved": True, "mode": "ground", "packages": [{"weight_kg": 10, "is_hazmat": False}]}]
    assert process_shipments(s_ground, 0.0)["total_quote"] == 40.0
    
    # Unknown mode (else branch)
    s_unknown = [{"manifest_approved": True, "mode": "express_air"}]
    assert process_shipments(s_unknown, 0.0)["status"] == "NO_CARGO"

def test_branch_package_weight_and_hazmat():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": False,
        "packages": [
            {"weight_kg": 0, "is_hazmat": False},       # weight <= 0 True
            {"weight_kg": 10, "is_hazmat": True},      # hazmat True, is_fragile False
            {"weight_kg": 40, "is_hazmat": False},     # weight > 30 True
            {"weight_kg": 20, "is_hazmat": False}      # weight > 30 False (standard weight)
        ]
    }]
    # handling_fee = 10.0
    # pkg 1: skipped (rejected)
    # pkg 2: +50.0
    # pkg 3: +40 * (4.0 * 1.5) = +240.0
    # pkg 4: +20 * 4.0 = +80.0
    # total = 380.0
    result = process_shipments(shipments, 10.0)
    assert result["total_quote"] == 380.0

def test_branch_hazmat_fragile_break():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "is_fragile": True,
        "packages": [{"weight_kg": 10, "is_hazmat": True}]
    }]
    assert process_shipments(shipments, 10.0)["total_quote"] == 0.0

def test_branch_express_priority_toggle():
    shipment_express = [{
        "manifest_approved": True,
        "mode": "ground",
        "express_priority": True,
        "packages": [{"weight_kg": 10, "is_hazmat": False}]
    }]
    # (10 + 40) * 1.25 = 62.5
    assert process_shipments(shipment_express, 10.0)["total_quote"] == 62.5

def test_branch_rejected_parcels_thresholds():
    # Exactly 3 rejected parcels -> status CLEARED
    shipments_3 = [
        {"manifest_approved": True, "mode": "unknown"},
        {"manifest_approved": True, "mode": "unknown"},
        {"manifest_approved": True, "mode": "unknown"},
        {"manifest_approved": True, "mode": "ground", "packages": [{"weight_kg": 10, "is_hazmat": False}]}
    ]
    assert process_shipments(shipments_3, 0.0)["status"] == "CLEARED"

    # 4 rejected parcels (> 3) -> status FLAGGED_REVIEW
    shipments_4 = shipments_3 + [{"manifest_approved": True, "mode": "unknown"}]
    assert process_shipments(shipments_4, 0.0)["status"] == "FLAGGED_REVIEW"


# --- BRANCH COVERAGE TESTS FOR monitor_container_pressures ---

def test_branch_pressure_logs():
    # Empty pressure logs
    assert monitor_container_pressures([]) == "NO_DATA"

    # Leak detected branch: 2 consecutive values < 14.0
    assert monitor_container_pressures([[13.0, 12.0]]) == "LEAK_DETECTED"

    # Reset streak branch: single low value followed by normal value
    assert monitor_container_pressures([[13.0, 15.0, 13.0]]) == "STABLE"