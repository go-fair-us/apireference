# Data.gov review

## alt title:  Data.gov, how do you annoy me, let me count the ways


### Landing page
Let's look at the catalog entry:

https://catalog-beta.data.gov/dataset/etp-covid-19-contracts?from_hint=eyJxIjoiY292aWQiLCJzb3J0IjoicmVsZXZhbmNlIn0%3D

Pulled up in the browser the look is OK.

Sadly, there is no structured metadata with this page:  [validation call](https://validator.schema.org/#url=https%3A%2F%2Fcatalog-beta.data.gov%2Fdataset%2Fetp-covid-19-contracts%3Ffrom_hint%3DeyJxIjoiY292aWQiLCJzb3J0IjoicmVsZXZhbmNlIn0%253D)

So right away any machine action on this entry is not happening easily.  There are links on the page to the metadata is harvested.  That could have been linked in the landing page in a machine resolvable manner, but wasn't.  

### Metadata

OK, Let's look at it.  We assume this is the metadata they got from https://data.ca.gov/.  Oh, it's California, go figure.

https://catalog-beta.data.gov/harvest_record/664051e8-826b-4cea-a2a3-787c49b21eb7/raw

OK, so it's the metadata they harvested, but they host.  Fine(ish).  

That metadata is included at the bottom of this page in the appendix.   It is not good (and that is kind).

* There is no context, so right off it's basically semantically mute and can't be used in any structured manner like a graph
* it can be blindly index in CKAN, which is what they do.
* They attempt to express ontology links with prefix values.  This is just wrong without a context, but at least they tried.   However, there is such a mix of vocabularies.  DCAT, VCARD, ORG.  Of these I can appreciate DCAT, but schema.org would scope all of these and align better with current best practices like Croissant and SOSO, etc.
* There is also NO DEFAULT vocabulary.  So the terms like "fn:" just hang there with absolutely ZERO context, meaning, understanding, etc.  
* summary, this data graph is WORTHLESS.  

### APIs

If we wanted to use the APIs, we might visit  https://api.data.gov/.  Which is a bit overwhelming.  

What we likely want is: https://api.data.gov/docs/developer-manual/.  This is better but while it says you need an API key, never bothers to provide link to where that key is. 

Oh look...  here it is: https://open.gsa.gov/api/datadotgov/.  That was obvious.   





### Appendix
```json
{
  "@type": "dcat:Dataset",
  "accessLevel": "public",
  "contactPoint": {
    "@type": "vcard:Contact",
    "fn": "Employment Training Panel, Data Analytics Unit",
    "hasEmail": "mailto:kelsey.oehrke@etp.ca.gov"
  },
  "description": "ETP contracts affected by COVID-19 who fall in one of the Governor declared essential industries. The dataset includes data in 3 different ETP COVID-19 programs: (1) ETP COVID-19 Response (2) ETP COVID-19 Pilot and (3) ETP RESPOND COVID",
  "distribution": [
    {
      "@type": "dcat:Distribution",
      "describedBy": "https://data.ca.gov/api/action/datastore_search?resource_id=1e1054dc-b863-4ba7-b8d6-2c03e647c6c2&limit=0",
      "describedByType": "application/json",
      "description": "Contractors who have requested modifications to their ETP contract or record keeping requirements due to the impact of COVID-19, or received expedited processing because they fall in one of the Governor declared essential industries.",
      "downloadURL": "https://data.ca.gov/dataset/b4162b8b-30cf-4f29-a55f-1bea50b097d2/resource/1e1054dc-b863-4ba7-b8d6-2c03e647c6c2/download/response-csv.csv",
      "format": "CSV",
      "mediaType": "text/csv",
      "title": "ETP COVID-19 Response Contracts"
    },
    {
      "@type": "dcat:Distribution",
      "describedBy": "https://data.ca.gov/api/action/datastore_search?resource_id=56c987fb-46d5-45d6-bd1a-f11133823fc3&limit=0",
      "describedByType": "application/json",
      "description": "The Rapid Employment Strategies On Natural Disasters (RESPOND) Program expands on our program for use on all natural disasters (including viral outbreaks)",
      "downloadURL": "https://data.ca.gov/dataset/b4162b8b-30cf-4f29-a55f-1bea50b097d2/resource/56c987fb-46d5-45d6-bd1a-f11133823fc3/download/respond-csv.csv",
      "format": "CSV",
      "mediaType": "text/csv",
      "title": "ETP RESPOND COVID Contracts"
    },
    {
      "@type": "dcat:Distribution",
      "describedBy": "https://data.ca.gov/api/action/datastore_search?resource_id=fe8b9dac-ff89-4b4b-9b04-d0c5c7cfde61&limit=0",
      "describedByType": "application/json",
      "description": "Contracts developed under ETP’s COVID-19 Pilot program which seeks to support training in essential businesses in healthcare and food supply chain.",
      "downloadURL": "https://data.ca.gov/dataset/b4162b8b-30cf-4f29-a55f-1bea50b097d2/resource/fe8b9dac-ff89-4b4b-9b04-d0c5c7cfde61/download/pilot-csv.csv",
      "format": "CSV",
      "mediaType": "text/csv",
      "title": "ETP COVID-19 Pilot Contracts"
    }
  ],
  "identifier": "b4162b8b-30cf-4f29-a55f-1bea50b097d2",
  "issued": "2020-12-28T17:57:48.789475",
  "keyword": [
    "covid",
    "covid-19",
    "employment training panel",
    "etp"
  ],
  "license": "http://www.opendefinition.org/licenses/cc-zero",
  "modified": "2021-08-30T17:21:17.859362",
  "publisher": {
    "@type": "org:Organization",
    "name": "California Employment Training Panel"
  },
  "theme": [
    "COVID-19"
  ],
  "title": "ETP COVID-19 Contracts"
}
```
