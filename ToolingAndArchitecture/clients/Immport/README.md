# ImmPort

#  References

Api info at: https://docs.immport.org/apidocumentation/

See also: https://immport.org/data/query/swagger-ui/index.html#/



Filter field

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