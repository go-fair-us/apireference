
import argparse
import json
import requests
import pandas as pd
from typing import List, Optional


def search_studies(
    term: str = "influenza vaccine",
    from_record: int = 0,
    page_size: int = 10,
    pre_tag: str = "<em>",
    post_tag: str = "</em>",
    sort_field_direction: str = "asc",
    condition_or_disease: Optional[List[str]] = None,
) -> dict:
    """
    Search ImmPort studies (no authentication required).

    Equivalent curl:
        curl -X GET 'https://immport.org/data/query/api/search/study?term=%20influenza%20vaccine
            &fromRecord=0&pageSize=10&preTag=%3Cem%3E&postTag=%3C%2Fem%3E
            &format=json&sortFieldDirection=asc&conditionOrDisease=asthma%2CCOVID-19'
            -H 'accept: application/json'
    """
    if condition_or_disease is None:
        condition_or_disease = ["asthma", "COVID-19"]

    url = "https://immport.org/data/query/api/search/study"
    headers = {"accept": "application/json"}
    params = {
        "term": term,
        "fromRecord": from_record,
        "pageSize": page_size,
        "preTag": pre_tag,
        "postTag": post_tag,
        "format": "json",
        "sortFieldDirection": sort_field_direction,
        "conditionOrDisease": ",".join(condition_or_disease),
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def to_dataframe(data: dict) -> pd.DataFrame:
    """Flatten the hits[].`_source` records into a DataFrame."""
    hits = data.get("hits", {}).get("hits", [])
    records = [hit["_source"] for hit in hits if "_source" in hit]
    return pd.DataFrame(records)


def main():
    parser = argparse.ArgumentParser(description="Search ImmPort studies and export results.")
    parser.add_argument("--term", default="influenza vaccine", help="Search term (default: 'influenza vaccine')")
    parser.add_argument(
        "--condition",
        nargs="+",
        default=["asthma", "COVID-19"],
        metavar="CONDITION",
        help="One or more conditions/diseases to filter by (default: asthma 'COVID-19')",
    )
    parser.add_argument("--page-size", type=int, default=10, help="Number of results to return (default: 10)")
    parser.add_argument("--from-record", type=int, default=0, help="Offset for pagination (default: 0)")
    parser.add_argument("--output", default=None, metavar="FILE.parquet", help="Save results to a Parquet file")
    args = parser.parse_args()

    print(f"Searching for: '{args.term}' | conditions: {args.condition}\n")
    data = search_studies(
        term=args.term,
        from_record=args.from_record,
        page_size=args.page_size,
        condition_or_disease=args.condition,
    )

    df = to_dataframe(data)
    print(f"Got {len(df)} results with {len(df.columns)} columns.")
    print(df.to_string(max_cols=6, max_rows=10))

    if args.output:
        df.to_parquet(args.output, index=False)
        print(f"\n✅ Saved to {args.output}")


if __name__ == "__main__":
    main()