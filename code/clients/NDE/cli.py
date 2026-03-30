"""
NIAID Data Ecosystem (NDE) API Client

A command-line interface for querying the NDE Hub API at api.data.niaid.nih.gov.
The NDE Hub aggregates metadata from 50+ biomedical data repositories.
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

import requests

BASE_URL = "https://api.data.niaid.nih.gov/v1"


def query(
    q: str,
    size: int = 10,
    from_: int = 0,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    facets: Optional[List[str]] = None,
    facet_size: int = 10,
    fetch_all: bool = False,
    scroll_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Query the NDE API.

    Args:
        q: Query string (Elasticsearch query syntax)
        size: Number of results to return (max 1000)
        from_: Starting offset for pagination
        fields: List of fields to return (default: all)
        sort: Sort order (e.g., "dateModified:desc")
        facets: List of fields to aggregate/facet on
        facet_size: Number of facet buckets to return
        fetch_all: If True, use scroll API for all results
        scroll_id: Scroll ID for pagination with fetch_all

    Returns:
        API response as dictionary
    """
    params: Dict[str, Any] = {"q": q, "size": size}

    if from_ > 0:
        params["from"] = from_

    if fields:
        params["_source"] = ",".join(fields)

    if sort:
        params["sort"] = sort

    if facets:
        params["aggs"] = ",".join(facets)
        params["facet_size"] = facet_size

    if fetch_all:
        params["fetch_all"] = "true"

    if scroll_id:
        params["scroll_id"] = scroll_id

    try:
        response = requests.get(f"{BASE_URL}/query", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying API: {e}", file=sys.stderr)
        sys.exit(1)


def fetch_all_results(
    q: str,
    fields: Optional[List[str]] = None,
    max_results: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch all results using scroll API.

    Args:
        q: Query string
        fields: List of fields to return
        max_results: Maximum number of results to fetch (None for all)

    Returns:
        List of all matching documents
    """
    all_hits: List[Dict[str, Any]] = []
    scroll_id = None

    while True:
        result = query(
            q=q,
            fields=fields,
            fetch_all=True,
            scroll_id=scroll_id,
            size=1000,
        )

        hits = result.get("hits", [])
        if not hits:
            break

        all_hits.extend(hits)
        scroll_id = result.get("_scroll_id")

        if max_results and len(all_hits) >= max_results:
            all_hits = all_hits[:max_results]
            break

        if not scroll_id:
            break

    return all_hits


def get_metadata() -> Dict[str, Any]:
    """Get API metadata including source information."""
    try:
        response = requests.get(f"{BASE_URL}/metadata")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}", file=sys.stderr)
        sys.exit(1)


def get_fields() -> Dict[str, Any]:
    """Get available fields in the API."""
    try:
        response = requests.get(f"{BASE_URL}/metadata/fields")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fields: {e}", file=sys.stderr)
        sys.exit(1)


def get_document(doc_id: str) -> Dict[str, Any]:
    """
    Get a single document by ID.

    Args:
        doc_id: Document identifier

    Returns:
        Document data
    """
    try:
        response = requests.get(f"{BASE_URL}/dataset/{doc_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching document: {e}", file=sys.stderr)
        sys.exit(1)


def format_hit(hit: Dict[str, Any], verbose: bool = False) -> str:
    """Format a single hit for display."""
    lines = []
    name = hit.get("name", "Untitled")
    doc_id = hit.get("_id", "unknown")
    source = hit.get("includedInDataCatalog", {})
    if isinstance(source, dict):
        source_name = source.get("name", "Unknown source")
    elif isinstance(source, list) and source:
        source_name = source[0].get("name", "Unknown source")
    else:
        source_name = "Unknown source"

    lines.append(f"[{doc_id}] {name}")
    lines.append(f"  Source: {source_name}")

    if verbose:
        description = hit.get("description", "")
        if description:
            desc_preview = (
                description[:200] + "..." if len(description) > 200 else description
            )
            lines.append(f"  Description: {desc_preview}")

        url = hit.get("url", "")
        if url:
            lines.append(f"  URL: {url}")

        has_api = hit.get("hasAPI", False)
        if has_api:
            lines.append("  Has API: Yes")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="NIAID Data Ecosystem (NDE) API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for datasets with APIs
  %(prog)s query "hasAPI:true" --size 5

  # Search for COVID-related datasets
  %(prog)s query "COVID-19" --size 10 --verbose

  # Get facets for infectious agents
  %(prog)s query "*" --facets infectiousAgent.name --facet-size 20

  # Fetch all datasets with APIs
  %(prog)s query "hasAPI:true" --fetch-all --output results.json

  # Get specific document
  %(prog)s get nde-zenodo-14299481

  # List available data sources
  %(prog)s metadata --sources
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Query command
    query_parser = subparsers.add_parser("query", help="Search the NDE database")
    query_parser.add_argument("q", help="Query string (Elasticsearch syntax)")
    query_parser.add_argument(
        "--size", type=int, default=10, help="Number of results (default: 10)"
    )
    query_parser.add_argument(
        "--from", dest="from_", type=int, default=0, help="Starting offset"
    )
    query_parser.add_argument(
        "--fields", help="Comma-separated list of fields to return"
    )
    query_parser.add_argument("--sort", help="Sort order (e.g., 'dateModified:desc')")
    query_parser.add_argument(
        "--facets", help="Comma-separated list of fields to facet on"
    )
    query_parser.add_argument(
        "--facet-size", type=int, default=10, help="Number of facet buckets"
    )
    query_parser.add_argument(
        "--fetch-all", action="store_true", help="Fetch all results (scroll)"
    )
    query_parser.add_argument(
        "--max-results", type=int, help="Max results when using --fetch-all"
    )
    query_parser.add_argument("--output", "-o", help="Output file (JSON)")
    query_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    query_parser.add_argument(
        "--raw", action="store_true", help="Output raw JSON response"
    )

    # Get command
    get_parser = subparsers.add_parser("get", help="Get a specific document by ID")
    get_parser.add_argument("doc_id", help="Document ID")
    get_parser.add_argument("--raw", action="store_true", help="Output raw JSON")

    # Metadata command
    meta_parser = subparsers.add_parser("metadata", help="Get API metadata")
    meta_parser.add_argument("--sources", action="store_true", help="List data sources")
    meta_parser.add_argument("--raw", action="store_true", help="Output raw JSON")

    # Fields command
    fields_parser = subparsers.add_parser("fields", help="List available fields")
    fields_parser.add_argument("--search", help="Search for specific field")
    fields_parser.add_argument("--raw", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.command == "query":
        fields_list = args.fields.split(",") if args.fields else None
        facets_list = args.facets.split(",") if args.facets else None

        if args.fetch_all:
            hits = fetch_all_results(
                q=args.q,
                fields=fields_list,
                max_results=args.max_results,
            )
            result = {"total": len(hits), "hits": hits}
        else:
            result = query(
                q=args.q,
                size=args.size,
                from_=args.from_,
                fields=fields_list,
                sort=args.sort,
                facets=facets_list,
                facet_size=args.facet_size,
            )

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {args.output}")
        elif args.raw:
            print(json.dumps(result, indent=2))
        else:
            total = result.get("total", 0)
            hits = result.get("hits", [])
            print(f"Found {total} results\n")

            for hit in hits:
                print(format_hit(hit, verbose=args.verbose))
                print()

            # Show facets if requested
            facets_result = result.get("facets", {})
            if facets_result:
                print("--- Facets ---")
                for field, data in facets_result.items():
                    print(f"\n{field}:")
                    terms = data.get("terms", [])
                    for term in terms:
                        print(
                            f"  {term.get('term', 'unknown')}: {term.get('count', 0)}"
                        )

    elif args.command == "get":
        result = get_document(args.doc_id)
        if args.raw:
            print(json.dumps(result, indent=2))
        else:
            print(f"Name: {result.get('name', 'Untitled')}")
            print(f"ID: {result.get('_id', 'unknown')}")
            print(f"Type: {result.get('@type', 'unknown')}")
            print(f"URL: {result.get('url', 'N/A')}")
            print(f"Description: {result.get('description', 'N/A')[:500]}")

    elif args.command == "metadata":
        result = get_metadata()
        if args.raw:
            print(json.dumps(result, indent=2))
        elif args.sources:
            sources = result.get("src", {})
            print(f"Data Sources ({len(sources)} total):\n")
            for name, info in sorted(sources.items()):
                stats = info.get("stats", {})
                count = stats.get("total", "unknown")
                print(f"  {name}: {count} records")
        else:
            build = result.get("build_version", "unknown")
            build_date = result.get("build_date", "unknown")
            sources = result.get("src", {})
            print(f"Build Version: {build}")
            print(f"Build Date: {build_date}")
            print(f"Data Sources: {len(sources)}")

    elif args.command == "fields":
        result = get_fields()
        if args.raw:
            print(json.dumps(result, indent=2))
        else:
            search_term = args.search.lower() if args.search else None
            for field_name in sorted(result.keys()):
                if search_term and search_term not in field_name.lower():
                    continue
                print(field_name)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
