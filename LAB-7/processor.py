import json
import math

def calculate_dimensional_weight(dimensions_str):
    if not isinstance(dimensions_str, str):
        raise ValueError("Dimensions must be a string")

    dims = dimensions_str.strip().split('x')
    if len(dims) != 3:
        raise ValueError("Dimensions must be in LxWxH format")

    try:
        length = float(dims[0])
        width = float(dims[1])
        height = float(dims[2])
    except ValueError as exc:
        raise ValueError("Dimensions must contain valid numbers") from exc

    if not (math.isfinite(length) and math.isfinite(width) and math.isfinite(height)):
        raise ValueError("Dimensions must be finite numbers")

    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Dimensions must be positive")

    return round((length * width * height) / 5000.0, 2)


def format_tracking_label(raw_code):
    if not isinstance(raw_code, str):
        raise ValueError("Tracking code must be a string")

    code = raw_code.strip()
    if len(code) < 2 or not code[0].isalpha() or not code[0].isascii():
        raise ValueError("Tracking code must start with an ASCII letter")

    num_part = code[1:]
    if not (num_part.isdigit() and num_part.isascii()):
        raise ValueError("Tracking number portion must contain only ASCII digits")

    prefix = code[0].upper()
    tracking_num = int(num_part)
    return f"{prefix}-{tracking_num:06d}"


def parse_package_manifest(json_payload):
    if not isinstance(json_payload, str):
        raise ValueError("Manifest payload must be a JSON string")

    try:
        data = json.loads(json_payload)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON payload") from exc

    if not isinstance(data, dict) or "weight" not in data:
        raise ValueError("Manifest JSON must be an object containing 'weight'")

    raw_weight = data["weight"]
    if isinstance(raw_weight, bool) or raw_weight is None:
        raise ValueError("Weight must be a numeric value")

    try:
        weight = float(raw_weight)
    except (TypeError, ValueError) as exc:
        raise ValueError("Weight must be convertible to float") from exc

    if not math.isfinite(weight) or weight <= 0:
        raise ValueError("Weight must be a finite positive number")

    return weight


def main():
    print("==== Running calculate_dimensional_weight ====")
    dims_input = input("Enter dimensions LxWxH in cm (e.g. 20x30x10): ")
    dim_weight = calculate_dimensional_weight(dims_input)
    print("Dimensional Weight (kg):", dim_weight)

    print("\n==== Running format_tracking_label ====")
    code_input = input("Enter raw code (e.g. E123): ")
    label = format_tracking_label(code_input)
    print("Formatted Label:", label)

    print("\n==== Running parse_package_manifest ====")
    json_input = input('Enter manifest JSON (e.g. {"weight": 12.5}): ')
    weight = parse_package_manifest(json_input)
    print("Manifest Weight:", weight)


if __name__ == "__main__":
    main()