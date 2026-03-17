#!/usr/bin/env python3
"""
VIOLIN V-Utilities Client.

Queries pathogen/vaccine APIs, outputs JSON-LD.

Usage:
    python client.py p_32 introduction
    python client.py --vaccine v_36 description
"""

import sys
import requests
import xml.etree.ElementTree as ET
import json
from urllib.parse import urlencode
from typing import Dict, Any, List

BASE_URL = "http://www.violinet.org/v-utilities/"


def _query_violin(endpoint: str, params: Dict[str, str]) -> Dict[str, Any] | None:
    """Core VIOLIN query helper."""
    try:
        response = requests.get(BASE_URL + endpoint, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        data = {}

        # Simple field
        if root.find("data") is not None:
            data = {"data": root.find("data").text or ""}

        # List fields
        elif root.findall("data"):
            items: List[Dict[str, str]] = []
            for item in root.findall("data"):
                item_data = {child.tag: child.text or "" for child in item}
                items.append(item_data)
            data = {"items": items}

        return data
    except requests.RequestException as e:
        print(f"API error: {e}", file=sys.stderr)
        return None
    except ET.ParseError as e:
        print(f"XML parse error: {e}", file=sys.stderr)
        return None


def query_pathogen(ptg: str, datafield: str, returntype: str = None) -> Dict[str, Any] | None:
    """Query pathogen API."""
    params = {"ptg": ptg, "datafield": datafield}
    if returntype:
        params["returntype"] = returntype
    return _query_violin("fpathogen.php", params)


def query_vaccine(vacn: str, datafield: str, returntype: str = None) -> Dict[str, Any] | None:
    """Query vaccine API."""
    params = {"vacn": vacn, "datafield": datafield}
    if returntype:
        params["returntype"] = returntype
    return _query_violin("fvaccine.php", params)


def to_jsonld(data: Dict[str, Any], source: str = "VIOLIN") -> str:
    """Convert dict to simple JSON-LD."""
    context = {
        "@context": {
            "data": "https://schema.org/text",
            "items": {"@context": {"@type": "@id"}}
        }
    }
    result = {
        "@context": context,
        "@type": "MedicalEntity",
        "source": source,
        **data
    }
    return json.dumps(result, indent=2)


def main():
    if len(sys.argv) < 3:
        print("Usage: python client.py <ptg> <datafield> [--returntype <type>]")
        print("  python client.py p_32 introduction")
        print("  python client.py p_13 vaccine")
        print("  python client.py t_727 pathogen_gene --returntype nk")
        print("")
        print("Usage: python client.py --vaccine <vacn> <datafield> [--returntype <type>]")
        print("  python client.py --vaccine v_36 description")
        print("  python client.py --vaccine n_F1%20antigen host_response --returntype vtd")
        sys.exit(1)

    if sys.argv[1] == "--vaccine":
        vacn = sys.argv[2]
        datafield = sys.argv[3]
        returntype = None
        if "--returntype" in sys.argv:
            idx = sys.argv.index("--returntype")
            returntype = sys.argv[idx + 1]
        result = query_vaccine(vacn, datafield, returntype)
    else:
        ptg = sys.argv[1]
        datafield = sys.argv[2]
        returntype = None
        if "--returntype" in sys.argv:
            idx = sys.argv.index("--returntype")
            returntype = sys.argv[idx + 1]
        result = query_pathogen(ptg, datafield, returntype)

    if result:
        jsonld = to_jsonld(result, "VIOLIN")
        print(jsonld)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
