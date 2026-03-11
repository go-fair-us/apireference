import json
import requests


def search_seronet_studies(age_range: str = "5-50") -> dict:
    """
    Query the ImmPort SeroNet study search API.

    :param age_range: Age range string in the format "min-max" (e.g., "5-50")
    :return: Parsed JSON response as a dict
    """
    base_url = "https://immport.org/data/query/api/search/seronet/study"
    headers = {"accept": "application/json"}
    params = {"ageRange": age_range}

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    age_range = "5-50"
    print(f"Querying ImmPort SeroNet studies with ageRange={age_range}...\n")

    data = search_seronet_studies(age_range)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()