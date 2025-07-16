| Metadata Element Describing the Digital Object | Metadata Element Description | Default Format for Metadata Value |
|---|---|---|
| type | Identifies the type of digital object. | IRI to type (e.g., "dataset", "software application", "image") |
| identifier | A globally unique, persistent, machine-resolvable identifier (GUPRI) assigned to the digital object | Resolvable DOI* |
| name | Descriptive title or name of the digital object. | Free text |
| description | A description of the digital object. | Free text |
| dateCreated | The date on which the digital object was created, or the item was added to a data repository. | Date (ISO 8601) |
| author** | Person or organization responsible for the creation of the digital object. | ORCID* |
| funder** | Organization(s) that provided funding for the digital object. | ROR* |
| grant** | Grant or contract number(s) associated with the digital object. | Alphanumeric string |
| measurementTechnique** | Technique(s) or technologies used in a digital object's measurement, if applicable. | NCIT* |
| distribution** | Link(s) to the downloadable distribution of the digital object. This refers specifically to the direct link(s) to the bit stream or file(s) themselves. | IRI (URL) |
| citation** | A citation or reference to another creative work related to the digital object. | IRI (URL) |
| infectiousAgent** | Infectious agent(s) involved in the digital object. | NCBITaxon* |
| host** | Host organism(s) associated with the digital object. | NCBITaxon* |
| healthCondition** | The health condition related to the digital object. | MONDO* |
| conditionsOfAccess | The condition(s) under which the digital object can be accessed, including data use agreements or limitations. | IRI (URL) to resources describing conditions of access, such as "open," "registered," "controlled," etc. |
| license | License(s) under which the digital object is distributed. | SPDX License Identifier* or IRI to a license document if not listed in SPDX. |
| spatialCoverage** | The geographic area covered by the digital object. | Country Code (ISO 3166) * |
| temporalCoverage** | The time period covered by the digital object. | Date range (ISO 8601 for start/end) |
