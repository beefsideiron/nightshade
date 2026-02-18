"""
Validation script for testing SunPredict predictions.

Runs test cases to verify the prediction logic is working correctly.
"""

import json
from datetime import datetime
from src.main import predict_sunlight_loss
import sys


def run_validation():
    """Run all validation test cases."""
    # Load test cases
    with open("data/validation_cases.json", "r") as f:
        test_data = json.load(f)

    test_cases = test_data["test_cases"]
    passed = 0
    failed = 0

    print("\n" + "=" * 70)
    print("SUNPREDICT VALIDATION TEST SUITE")
    print("=" * 70 + "\n")

    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"  Location: {test_case['latitude']}, {test_case['longitude']}")
        print(f"  Elevation: {test_case['elevation']}m")
        print(f"  Date: {test_case['date']}")
        print(f"  Notes: {test_case['notes']}")

        try:
            # Parse date
            date = datetime.strptime(test_case["date"], "%Y-%m-%d")

            # Run prediction
            result = predict_sunlight_loss(
                test_case["latitude"],
                test_case["longitude"],
                test_case["elevation"],
                date,
                test_case["terrain_file"],
            )

            # Check result
            if result["has_sunlight"] == test_case["expected_has_sunlight"]:
                print(f"  ✓ PASSED")
                if result["has_sunlight"]:
                    print(
                        f"    Sunlight lost at: {format_time(datetime.fromisoformat(result['last_direct_sunlight']))}"
                    )
                else:
                    print(f"    No sunlight on this date (as expected)")
                passed += 1
            else:
                print(f"  ✗ FAILED")
                print(
                    f"    Expected has_sunlight={test_case['expected_has_sunlight']}, "
                    f"got {result['has_sunlight']}"
                )
                failed += 1

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1

        print()

    # Summary
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70 + "\n")

    return failed == 0


def format_time(dt: datetime) -> str:
    """Format datetime as HH:MM."""
    if dt is None:
        return "N/A"
    return dt.strftime("%H:%M")


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
