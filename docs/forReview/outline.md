#  NIAID API Training: Repository Structure & Strategy

Creating a training resource for a diverse audience (from newcomers to providers) within the NIH NIAID
ecosystem requires a **layered curriculum**. Since this will be hosted in a GitHub repository, 
you can leverage **Markdown** for documentation, **Jupyter Notebooks** for 
interactive examples, and **GitHub Pages** .

---

## 📁 Proposed Repository Structure

```text
├── README.md                 # Welcome, high-level overview, and "Choose Your Path"
├── 01-Foundations/           # For Everyone (The "User" level)
│   ├── what-is-an-api.md     # Non-technical analogies (The "Waiter" or "Receptionist")
│   ├── reading-docs.md       # How to use Swagger/OpenAPI (using NIAID Discovery API)
│   └── tools-no-code.md      # Using Postman or Web Interfaces
├── 02-Intermediates/         # For Power Users & Data Scientists
│   ├── python-requests.ipynb # Fetching NIAID data with Python
│   ├── auth-and-limits.ipynb # Handling API keys and rate limits
│   └── case-study-tb.md      # Example: TB Portals Data API
├── 03-Providers/             # For Developers & Architects
│   ├── design-principles.md  # RESTful design for biomedical data
│   ├── documenting-api.md    # Writing OpenAPI specs for NIH compliance
│   └── security-fair.md      # Implementing FAIR principles and OAuth2
└── examples/                 # Ready-to-run code snippets

```

---

## Targeted Training Content

### 1. For the Newcomer (The "Consumer")

Start with a relatable analogy and move immediately to a "Quick Win" using the **NIAID Data Discovery Portal API**.

* **The Concept:** Explain that an API is like a **Librarian**. You don't walk into the stacks yourself (the database); you give the Librarian a specific request (the API call), and they bring you the book (the JSON response).
* **The Tool:** Introduce **Swagger UI**.
* *Hands-on:* Point them to [api.data.niaid.nih.gov](https://api.data.niaid.nih.gov/).
* *Exercise:* Have them use the `/query` endpoint in the browser to search for "Malaria" and see the raw data returned.



### 2. For the Experienced User (The "Data Scientist")

Transition from browser-based tools to programmatic access. Use the **TB Portals Data API** as a sophisticated example.

* **Example Case Study:** Programmatic access to Tuberculosis datasets.
* **Technical Skill:** Parsing JSON and handling pagination.
* **Sample Python Snippet:**

```python
import requests

# Accessing NIAID Discovery Portal
base_url = "https://api.data.niaid.nih.gov/v1/query"
params = {'q': 'influenza', 'size': 5}
response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Found {data['total']} records.")

```



### 3. For the API Provider (The "Architect")

Focus on **Standards** and **FAIR (Findable, Accessible, Interoperable, Reusable) Principles**.

* **Design for NIAID:** Emphasize using the **OpenAPI Specification (OAS)**. Since NIAID works with heterogeneous data, explain the importance of **Metadata Schemas**.
* **The Challenge:** How to handle **Controlled Access Data**. Use the **AccessClinicalData@NIAID** platform as a reference for how APIs must handle Data Use Agreements (DUA) and authentication (OAuth2/OpenID Connect).
* **Best Practices:**
* Versioning (e.g., `/v1/`, `/v2/`).
* Naming conventions (nouns, not verbs: `/datasets` instead of `/getDatasets`).



---

## NIAID Specific Examples to Feature

| Resource | Role in Training | Why it works |
| --- | --- | --- |
| **Discovery Portal API** | **Basic User** | Publicly accessible, no key required, great Swagger UI. |
| **TB Portals API** | **Power User** | Demonstrates complex queries and domain-specific data (genomics/imaging). |
| **ImmPort / ImmSpace** | **Advanced/Provider** | Showcases high-level data integration and strict metadata standards. |
| **AccessClinicalData** | **Provider** | Focuses on security, controlled access, and HIPAA/PII considerations. |

---

**Would you like me to help you draft the intermediate Python tutorial for the `02-Intermediates/` folder next?**
