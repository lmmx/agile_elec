from agile_elec.loader import load_agile_data


def main():
    df = load_agile_data()
    print(df)
