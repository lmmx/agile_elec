import polars as pl


def calculate_over_threshold_pct(df: pl.DataFrame, threshold: float = 26.0) -> float:
    """Calculate percentage of time price goes over threshold."""
    total_rows = df.height
    over_threshold = df.filter(pl.col("r") > threshold).height
    return (over_threshold / total_rows) * 100


def calculate_savings_counterfactual(
    df: pl.DataFrame,
    annual_kwh: float = 5000.0,
    threshold: float = 26.0,
    summer_multiplier: float = 2.0,
) -> dict:
    """Calculate savings if usage outside expensive hours was offset.

    Returns dict with savings analysis.
    """
    # Parse datetime
    df = df.with_columns(
        pl.col("dt").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ").alias("datetime")
    )

    # Add month for summer detection (Jun-Aug = 6,7,8)
    df = df.with_columns(pl.col("datetime").dt.month().alias("month"))

    # Classify high vs low price periods
    df = df.with_columns((pl.col("r") > threshold).alias("is_expensive"))

    # Calculate average prices (in pence)
    avg_expensive = df.filter(pl.col("is_expensive")).select(pl.col("r").mean()).item()
    avg_cheap = df.filter(~pl.col("is_expensive")).select(pl.col("r").mean()).item()

    # Calculate hours in each category
    total_hours = df.height * 0.5  # Each row is 30 min
    expensive_hours = df.filter(pl.col("is_expensive")).height * 0.5
    cheap_hours = total_hours - expensive_hours

    # Simple model: distribute usage proportionally to available hours
    kwh_per_hour = annual_kwh / total_hours

    # Current cost (proportional distribution) - convert pence to pounds
    current_cost_expensive = (expensive_hours * kwh_per_hour * avg_expensive) / 100
    current_cost_cheap = (cheap_hours * kwh_per_hour * avg_cheap) / 100
    current_total = current_cost_expensive + current_cost_cheap

    # Optimized: shift all usage to cheap hours - convert pence to pounds
    optimized_cost = (annual_kwh * avg_cheap) / 100

    savings = current_total - optimized_cost

    return {
        "current_cost_gbp": current_total,
        "optimized_cost_gbp": optimized_cost,
        "savings_gbp": savings,
        "savings_pct": (savings / current_total) * 100,
        "avg_expensive_price": avg_expensive,
        "avg_cheap_price": avg_cheap,
        "pct_time_expensive": (expensive_hours / total_hours) * 100,
    }
