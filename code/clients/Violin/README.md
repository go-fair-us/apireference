# Violin Client

# NOTE:  Violin Service is broken.  This code is only for other demonstration purposes. 


VIOLIN (Vaccine Investigation and Online Information Network) API client.

Queries V-Utilities APIs:
- Pathogen: http://www.violinet.org/v-utilities/fpathogen.php
- Vaccine: http://www.violinet.org/v-utilities/fvaccine.php

Returns JSON-LD (XML parsed).

## Installation

```bash
uv sync  # From project root
cd code/clients/Violin
uv run python client.py --help
```

## Usage

### Pathogen Queries
```bash
# Introduction for pathogen ID 32
uv run python client.py p_32 introduction

# Vaccines for pathogen 13
uv run python client.py p_13 vaccine

# Genes (name + DNA seq) for taxonomy 727
uv run python client.py t_727 pathogen_gene --returntype nk

# By name (URL-encoded)
uv run python client.py "n_Haemophilus%20influenzae" vaccine
```

### Vaccine Queries
```bash
# Description for vaccine 36
uv run python client.py --vaccine v_36 description

# Host responses (vaccine+time+desc)
uv run python client.py --vaccine v_36 host_response --returntype vtd

# By name
uv run python client.py --vaccine "n_F1%20antigen" preparation
```

**Example Pathogens**: `p_32`, `p_13`, `p_31`, `n_Haemophilus influenzae`, `t_727`, `t_1773`  
**Example Vaccines**: `v_36`, `n_F1 antigen`

## Data Fields
- `introduction`, `pathogenesis`, `disease_name`, `vaccine`, `pathogen_gene`, `host_gene`, `reference`
- Full list + `returntype` codes: https://violinet.org/v-utilities/index.php

## Output
JSON-LD with `@context` (schema.org), e.g.:
```json
{
  "@context": {...},
  "@type": "MedicalEntity",
  "source": "VIOLIN",
  "items": [...]
}
```

## References
* https://violinet.org/v-utilities/index.php
* Schemas: [fpathogen.xsd](v-utilities_doc.pdf)

