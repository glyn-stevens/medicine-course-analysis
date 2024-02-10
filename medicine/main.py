from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class AreaDetails:
    place_to_live: str
    region: str
    main_locs: list[str]
    commutatble_locs: list[str]


CAMBRIDGE = AreaDetails(
    place_to_live="Cambridge",
    region="East of England Foundation School",
    main_locs=[
        "Cambridge",
        "Papworth Everard",
        "Papworth",
        "Papworth Hospital",
    ],
    commutatble_locs=[
        "Bury St Edmunds",
        "Harlow",
        "Huntingdon",
        "King's Lynn",
        "Stevenage",
        "CPFT",
        "Cambridgeshire and Peterborough",
    ],
)
SHEFFIELD = AreaDetails(
    place_to_live="Sheffield",
    region="Yorkshire and Humber Foundation School",
    main_locs=[
        "Sheffield S10 2JF",
        "Sheffield S10 2SF",
        "Sheffield S10 2SJ",
        "Sheffield S10 2TH",
        "Sheffield S11 9BF",
        "Sheffield S11 9NE",
        "Sheffield S12 4QN",
        "Sheffield S2 3QE",
        "Sheffield S26 4TH",
        "Sheffield S35 8QS",
        "Sheffield S5 7AU",
        "Sheffield S5 7JT",
    ],
    commutatble_locs=["Rotherham S60 2UD"],
)

SOUTH_COAST = AreaDetails(
    place_to_live="Bournemouth/Poole", region="Wessex Foundation School", main_locs=["Poole", "Bournemouth"], commutatble_locs=[]
)

DATA_DIR = Path.cwd() / "data"


def rotation_col(rotation_num: int) -> str:
    return f"Rotation {rotation_num} location"


def main(program_type: str, area: AreaDetails, print_matching_placements: bool) -> None:
    # Column headers
    region_col = "Foundation School"
    program_type_col = "Programme Type"
    all_rotation_cols = [rotation_col(x) for x in [1, 2, 3, 4, 5, 6]]

    # Read data
    file_path = DATA_DIR / "foundation_programmes.csv"
    df_all = pd.read_csv(file_path)

    # Masks and initial filter
    mask_region = df_all[region_col] == area.region
    mask_program_type = df_all[program_type_col] == program_type
    df_region = df_all[mask_region & mask_program_type]
    mask_main_city = (df_region[rotation_col(1)].isin(area.main_locs)) | (
        df_region[rotation_col(4)].isin(area.main_locs)
    )
    main_city_or_commutable = area.commutatble_locs + area.main_locs
    mask_commutable = df_region[all_rotation_cols].isin(main_city_or_commutable).sum(axis=1) >= 5
    mask_comutable_with_main_city = mask_main_city & mask_commutable

    # Calculate stats
    region_stats = {}
    num_in_region = len(df_region)
    region_stats[f"Region: {area.region}"] = num_in_region
    region_stats[f"Rotation 1 or 4 in: {area.place_to_live}"] = mask_main_city.sum()
    region_stats[
        f"Rotation 1 or 4 in: {area.place_to_live}, and at least 5/6 rotations commutable"
    ] = mask_comutable_with_main_city.sum()
    region_stats[f"At least 5/6 rotations commutable from: {area.place_to_live}"] = (
        mask_commutable.sum()
    )
    all_locations_in_region = pd.concat([df_region[col] for col in all_rotation_cols])
    uncommutable = {loc for loc in all_locations_in_region if loc not in main_city_or_commutable}
    loc_with_rotation_in_main = pd.concat(
        [df_region[mask_main_city][col] for col in all_rotation_cols]
    )
    uncommutable_with_rotation_in_main = {
        loc for loc in loc_with_rotation_in_main if loc not in main_city_or_commutable
    }

    # Print results
    print(f"Results for program type: {program_type}")
    for key, stat in region_stats.items():
        print(f"Number placements with {key}: {stat} ( = {stat/num_in_region*100:.1f}%)")
    print(f"Locations deemed uncommutable: {sorted(uncommutable)}")
    print(f"Uncommutable locs with placements in main city: {uncommutable_with_rotation_in_main}")
    if print_matching_placements:
        print("Placement locations with at least one year in main location:")
        pd.set_option("display.max_rows", 200)
        print(df_region[mask_comutable_with_main_city][all_rotation_cols])


if __name__ == "__main__":
    program_type = "FP"
    area_to_investigate = SOUTH_COAST
    main(program_type, area_to_investigate, print_matching_placements=False)
