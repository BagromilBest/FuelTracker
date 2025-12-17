from fastapi import HTTPException


def calculate_ride_data(dist, cons, fuel):
    """
    Core business logic for ride calculation.
    Returns tuple (dist, cons, fuel) rounded to 2 decimals.
    """

    # Helper to round
    def r(val):
        return round(val, 2)

    # Check which are present
    has_d = dist is not None
    has_c = cons is not None
    has_f = fuel is not None

    count = sum([has_d, has_c, has_f])

    if count < 2:
        raise HTTPException(status_code=400, detail="At least two of Distance, Consumption, or Fuel must be provided.")

    final_d = dist
    final_c = cons
    final_f = fuel

    if count == 3:
        # Validate consistency
        expected_f = (dist * cons) / 100.0
        if abs(fuel - expected_f) > 0.1:
            raise HTTPException(status_code=400,
                                detail=f"Inconsistent data. Based on Dist ({dist}) and Cons ({cons}), Fuel should be approx {r(expected_f)}, but got {fuel}.")

    elif not has_f:
        # Calculate Fuel
        final_f = (dist * cons) / 100.0

    elif not has_d:
        # Calculate Distance: d = (f * 100) / c
        final_d = (fuel * 100.0) / cons

    elif not has_c:
        # Calculate Consumption: c = (f * 100) / d
        if dist == 0:
            raise HTTPException(status_code=400, detail="Distance cannot be zero when calculating consumption.")
        final_c = (fuel * 100.0) / dist

    return r(final_d), r(final_c), r(final_f)