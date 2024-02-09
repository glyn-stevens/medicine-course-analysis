from pathlib import Path

import pandas as pd

DATA_DIR = Path.cwd() / "data"


def rotation_col(rotation_num: int) -> str:
    return f"Rotation {rotation_num} location"


def main(
    region: str,
    main_city: str,
    program_type: str,
    commutatble_cities: list[str],
) -> None:
    # Column headers
    region_col = "Foundation School"
    program_type_col = "Programme Type"
    all_rotation_cols = [rotation_col(x) for x in [1, 2, 3, 4, 5, 6]]
    
    # Read data
    file_path = DATA_DIR / "foundation_programmes.csv"
    df_all = pd.read_csv(file_path)
    
    # Masks and initial filter
    mask_region = (df_all[region_col] == region)
    mask_program_type = (df_all[program_type_col] == program_type)
    df_region = df_all[mask_region & mask_program_type]
    mask_main_city = (df_region[rotation_col(1)] == main_city) | (
        df_region[rotation_col(4)] == main_city
    )
    commutatble_cities.append(main_city)
    mask_commutable = df_region[all_rotation_cols].isin(commutatble_cities).sum(axis=1) >= 5
    mask_comutable_with_main_city = (mask_main_city & mask_commutable)
    
    # Calculate stats
    region_stats = {}
    placements_in_region = len(df_region)
    region_stats[f"Region: {region}"] = placements_in_region
    region_stats[f"Rotation 1 or 4 in: {main_city}"] = mask_main_city.sum()
    region_stats[f"Rotation 1 or 4 in: {main_city}, and at least 5/6 rotations commutable"] = (
        mask_comutable_with_main_city.sum()
    )
    region_stats[f"At least 5/6 rotations commutable from: {main_city}"] = mask_commutable.sum()
    all_cities_in_region = pd.concat([df_region[col] for col in all_rotation_cols])
    uncommutable_cities = {city for city in all_cities_in_region if city not in commutatble_cities}
    
    # Print results
    print(f"Results for program type: {program_type}")
    for key, stat in region_stats.items():
        print(f"Number placements with {key}: {stat} ( = {stat/placements_in_region*100:.1f}%)")
    print(f"Cities deemed uncommutable: {uncommutable_cities}")
    print("Placement locations:")
    pd.set_option('display.max_rows', 200)
    print(df_region[mask_commutable][all_rotation_cols])


if __name__ == "__main__":
    program_type = "FP"
    region = "East of England Foundation School"
    main_city = "Cambridge"
    comutatble_cities = [
        "Bury St Edmunds",
        "Harlow",
        "Huntingdon",
        "King's Lynn",
        "Papworth Everard",
        "Papworth",
        "Papworth Hospital",
        "Stevenage",
        "CPFT",
        "Cambridgeshire and Peterborough"
    ]
    main(region, main_city, program_type, comutatble_cities)
