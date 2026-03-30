import requests
import sys
import json

def get_dataset(dataset_id):
    """
    Retrieves a dataset from the Provisium demo API.

    Args:
        dataset_id: The ID of the dataset to retrieve.

    Returns:
        The dataset as a JSON object, or None if an error occurs.
    """
    url = f"http://127.0.0.1:8080/id/dataset/{dataset_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <dataset_id>", file=sys.stderr)
        sys.exit(1)

    dataset_id = sys.argv[1]
    dataset = get_dataset(dataset_id)

    if dataset:
        print(json.dumps(dataset, indent=2))
