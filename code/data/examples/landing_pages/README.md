# Example Dataset Landing Pages

**These are fictitious example datasets for demonstration purposes only. All data, identifiers, and organizations are fake.**

## Overview

This directory contains 6 example HTML dataset landing pages with embedded schema.org JSON-LD metadata. Each page demonstrates the standard approach of embedding structured data using `<script type="application/ld+json">` in the HTML head.

## Files

| Dataset Type | HTML Page | JSON-LD |
|--------------|-----------|---------|
| Influenza A genome sequences | `dataset-genomics-001.html` | `dataset-genomics-001.jsonld` |
| Malaria vaccine clinical trial | `dataset-clinical-002.html` | `dataset-clinical-002.jsonld` |
| TB chest X-ray images for ML | `dataset-imaging-003.html` | `dataset-imaging-003.jsonld` |
| Dengue seroprevalence survey | `dataset-survey-004.html` | `dataset-survey-004.jsonld` |
| HIV proteomics data | `dataset-proteomics-005.html` | `dataset-proteomics-005.jsonld` |
| Mosquito surveillance network | `dataset-vector-006.html` | `dataset-vector-006.jsonld` |

## Viewing Locally

Use Python's built-in HTTP server to view the pages in a browser:

```bash
cd code/data/examples/landing_pages
python -m http.server 8000
```

Then open http://localhost:8000/ in your browser.

## Validation

You can validate the JSON-LD using:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
