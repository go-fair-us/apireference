# CLI Examples

## About
This document has some example CLI commands, mostly in curl.  They demonstrate some of the public
APIs that are available for use.  

## Nominatim: GeoCoding: Address to Coodinates


```bash
> curl -X GET "https://nominatim.openstreetmap.org/search?format=json&q=Berlin%20Germany&limit=1" | jq

[
  {
    "place_id": 134131805,
    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
    "osm_type": "relation",
    "osm_id": 62422,
    "lat": "52.5173885",
    "lon": "13.3951309",
    "class": "boundary",
    "type": "administrative",
    "place_rank": 8,
    "importance": 0.8522196536088086,
    "addresstype": "city",
    "name": "Berlin",
    "display_name": "Berlin, Deutschland",
    "boundingbox": [
      "52.3382448",
      "52.6755087",
      "13.0883450",
      "13.7611609"
    ]
  }
]     
```
