from hypothesis import given, strategies as st
import pytest
from processor import calculate_dimensional_weight, format_tracking_label, parse_package_manifest

@given(st.text() | st.none())
def test_calculate_dimensional_weight_no_crash(s):
    try:
        result = calculate_dimensional_weight(s)
        assert isinstance(result, float)
        assert result > 0
    except ValueError:
        pass

@given(st.text() | st.none())
def test_format_tracking_label_safe(s):
    try:
        result = format_tracking_label(s)
        assert isinstance(result, str)
        assert "-" in result
    except ValueError:
        pass

@given(st.text() | st.none())
def test_parse_package_manifest_safe(s):
    try:
        result = parse_package_manifest(s)
        assert isinstance(result, float)
        assert result > 0
    except ValueError:
        pass