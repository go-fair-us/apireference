# ImmPort

A Python client for the [ImmPort](https://www.immport.org/) SeroNet study search API.

## References

- API docs: https://docs.immport.org/apidocumentation/
- Swagger UI: https://immport.org/data/query/swagger-ui/index.html#/

## Running the Client

The client queries the SeroNet study search endpoint and pretty-prints the JSON response.

```bash
cd code/clients/Immport
uv run immportClient.py
```

By default, it searches with `ageRange=5-50`. To use a different range, import and call `search_seronet_studies()` directly:

```python
from immportClient import search_seronet_studies
import json

data = search_seronet_studies(age_range="18-65")
print(json.dumps(data, indent=2))
```

## Equivalent curl

```bash
curl -X 'GET' \
  'https://immport.org/data/query/api/search/seronet/study?ageRange=5-50' \
  -H 'accept: application/json'
```

## Available Filter Fields

The search API supports a broad set of filters. Full field reference:

```json
{
  "term": "string",
  "fromRecord": 0,
  "pageSize": 0,
  "preTag": "string",
  "postTag": "string",
  "format": "string",
  "sortField": "string",
  "sourceFields": "string",
  "sortFieldDirection": "string",
  "returnProperties": ["string"],
  "researchFocus": ["string"],
  "reportedHealthCondition": ["string"],
  "studyType": ["string"],
  "clinicalStudyDesign": ["string"],
  "inSilicoModelType": ["string"],
  "sarsCov2VaccineType": ["string"],
  "geriatricSubjects": ["string"],
  "pediatricSubjects": ["string"],
  "pregnantSubjects": ["string"],
  "sarsCov2AntibodiesMeasured": ["string"],
  "ethnicity": ["string"],
  "race": ["string"],
  "sex": ["string"],
  "sarsCov2Symptoms": ["string"],
  "sarsCov2History": ["string"],
  "covid19DiseaseSeverity": ["string"],
  "genusAndSpecies": ["string"],
  "biosampleType": ["string"],
  "assayType": ["string"],
  "biospecimenType": ["string"],
  "biospecimenCollectionPoint": ["string"],
  "sarsCov2Antigen": ["string"],
  "virusTarget": ["string"],
  "sarsCov2Variant": ["string"],
  "ageRange": "string",
  "noOfSubjectsRange": "string",
  "dateRange": "string"
}
```


#  References

Api info at: https://docs.immport.org/apidocumentation/

See also: https://immport.org/data/query/swagger-ui/index.html#/



Filter field−


```json
{
  "term": "string",
  "fromRecord": 0,
  "pageSize": 0,
  "preTag": "string",
  "postTag": "string",
  "format": "string",
  "sortField": "string",
  "sourceFields": "string",
  "sortFieldDirection": "string",
  "returnProperties": [
    "string"
  ],
  "researchFocus": [
    "string"
  ],
  "reportedHealthCondition": [
    "string"
  ],
  "studyType": [
    "string"
  ],
  "clinicalStudyDesign": [
    "string"
  ],
  "inSilicoModelType": [
    "string"
  ],
  "sarsCov2VaccineType": [
    "string"
  ],
  "geriatricSubjects": [
    "string"
  ],
  "pediatricSubjects": [
    "string"
  ],
  "pregnantSubjects": [
    "string"
  ],
  "sarsCov2AntibodiesMeasured": [
    "string"
  ],
  "ethnicity": [
    "string"
  ],
  "race": [
    "string"
  ],
  "sex": [
    "string"
  ],
  "sarsCov2Symptoms": [
    "string"
  ],
  "sarsCov2History": [
    "string"
  ],
  "covid19DiseaseSeverity": [
    "string"
  ],
  "genusAndSpecies": [
    "string"
  ],
  "biosampleType": [
    "string"
  ],
  "assayType": [
    "string"
  ],
  "biospecimenType": [
    "string"
  ],
  "biospecimenCollectionPoint": [
    "string"
  ],
  "sarsCov2Antigen": [
    "string"
  ],
  "virusTarget": [
    "string"
  ],
  "sarsCov2Variant": [
    "string"
  ],
  "ageRange": "string",
  "noOfSubjectsRange": "string",
  "dateRange": "string"
}
```


```bash
curl -X 'GET' \
  'https://immport.org/data/query/api/search/seronet/study?ageRange=5-50' \
  -H 'accept: application/json'
```

## Studies Client

