from pathlib import Path

import polars as pl
import polars_genson  # noqa: F401


def load_agile_data():
    """Load agile electricity data from JSON file."""
    # Get path to data file (2 directories up from this file)
    data_path = (
        Path(__file__).parent.parent.parent / "data" / "agile_electricity_london.json"
    )

    # Read JSON as single column
    with open(data_path) as f:
        json_str = f.read()

    df = pl.DataFrame({"data": [json_str]})

    # Use genson to normalize and decode the JSON with root wrapping
    result = (
        df.genson.normalise_json("data", wrap_root="data", decode=True, unnest=True)
        .explode("data")
        .unnest("data")
    )

    return result
