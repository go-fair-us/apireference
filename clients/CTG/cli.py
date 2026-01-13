import argparse
import requests
import json
import os
from typing import Optional, Union, Dict, Any

BASE_URL = "https://clinicaltrials.gov/api/v2"

def list_studies(query_cond: Optional[str] = None, page_size: int = 10, format: str = "json", summary: bool = False):
    params = {"pageSize": page_size, "format": format}
    if query_cond:
        params["query.cond"] = query_cond
    if summary:
        params["fields"] = "NCTId,BriefSummary"
    
    response = requests.get(f"{BASE_URL}/studies", params=params)
    response.raise_for_status()
    
    if format == "json":
        return response.json()
    else:
        return response.text

def get_study(nct_id: str, format: str = "json"):
    response = requests.get(f"{BASE_URL}/studies/{nct_id}", params={"format": format})
    response.raise_for_status()
    
    if format == "json":
        return response.json()
    else:
        return response.text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ClinicalTrials.gov API CLI")
    subparsers = parser.add_subparsers(dest="command")

    # List studies
    list_parser = subparsers.add_parser("list", help="List studies")
    list_parser.add_argument("--query-cond", help="Condition query")
    list_parser.add_argument("--page-size", type=int, default=10, help="Page size")
    list_parser.add_argument("--format", default="json", help="Output format")
    list_parser.add_argument("--summary", action="store_true", help="Fetch only NCTId and BriefSummary")
    list_parser.add_argument("--question", help="Question to ask LLM about the summaries")

    # Get study
    get_parser = subparsers.add_parser("get", help="Get a single study")
    get_parser.add_argument("nct_id", help="NCT ID")
    get_parser.add_argument("--format", default="json", help="Output format")

    args = parser.parse_args()

    if args.command == "list":
        result = list_studies(args.query_cond, args.page_size, args.format, args.summary)
        if args.question:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                print("Error: OPENROUTER_API_KEY environment variable not set.")
                exit(1)
            
            if not isinstance(result, dict):
                print("Error: --question requires JSON format and summary data.")
                exit(1)
            
            if "studies" not in result:
                print("Error: No studies found in the result.")
                exit(1)
            
            summaries = []
            for study in result["studies"]:
                protocol = study.get("protocolSection", {})
                ident = protocol.get("identificationModule", {})
                desc = protocol.get("descriptionModule", {})
                nct_id = ident.get("nctId", "Unknown")
                brief_summary = desc.get("briefSummary", "No summary")
                summaries.append(f"{nct_id}: {brief_summary}")
            
            concatenated = "\n\n".join(summaries)
            prompt = f"Here are summaries of clinical trials:\n{concatenated}\n\nQuestion: {args.question}"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "x-ai/grok-4.1-fast",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "max_tokens": 512,
                "temperature": 0.7,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "n": 1
            }
            
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            try:
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                print("LLM Response:")
                print(content)
            except requests.HTTPError as e:
                print(f"HTTP Error: {e}")
                print(response.text)
            except KeyError as e:
                print(f"Key Error in response: {e}")
                print(response.json())
            except Exception as e:
                print(f"Unexpected Error: {e}")
        else:
            if isinstance(result, dict):
                print(json.dumps(result, indent=2))
            else:
                print(result)
    elif args.command == "get":
        result = get_study(args.nct_id, args.format)
        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(result)
    else:
        parser.print_help()
