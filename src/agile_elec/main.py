from agile_elec.loader import load_agile_data
from agile_elec.analysis import (
    calculate_over_threshold_pct,
    calculate_savings_counterfactual,
)


def format_gbp(amount: float) -> str:
    """Format amount as GBP with commas and pound sign."""
    return f"£{amount:,.2f}"


def main():
    df = load_agile_data()

    # Input parameters
    annual_kwh = 5000.0
    threshold = 26.0

    print("Simulation Parameters:")
    print(f"  Annual consumption: {annual_kwh:,.0f} kWh")
    print(f"  Price threshold: {threshold}p")
    print(f"  Data period: {df.height} half-hour periods")
    print()

    pct_over_26 = calculate_over_threshold_pct(df, threshold=threshold)
    print(f"Percentage of time over {threshold}p: {pct_over_26:.2f}%")

    savings = calculate_savings_counterfactual(
        df, annual_kwh=annual_kwh, threshold=threshold
    )
    print("\nSavings Analysis:")
    print(f"  Current cost: {format_gbp(savings['current_cost_gbp'])}")
    print(f"  Optimized cost: {format_gbp(savings['optimized_cost_gbp'])}")
    print(
        f"  Savings: {format_gbp(savings['savings_gbp'])} ({savings['savings_pct']:.2f}%)"
    )
    print(f"  Avg expensive price: {savings['avg_expensive_price']:.2f}p")
    print(f"  Avg cheap price: {savings['avg_cheap_price']:.2f}p")
    print(f"  Time expensive: {savings['pct_time_expensive']:.2f}%")
