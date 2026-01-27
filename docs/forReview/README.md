#  NIAID API Training Hub
### From Data Consumers to API Architects

Welcome to the **National Institute of Allergy and Infectious Diseases (NIAID)** API Training Resource. Whether you are here to learn how to download your first dataset via Python or you are building the next generation of NIAID data services, this repository provides the roadmap and tools you need.

---

##  Choose Your Learning Path
Select the persona that best describes your current goal:

### 🟢 The Discoverer (New User)
* **Profile:** You want to access NIAID data but have never used an API before.
* **Focus:** Understanding "What is an API?", using browser-based tools, and reading documentation.
* **Featured Resource:** [Getting Started with the Discovery Portal API](./01-Foundations/readme.md)

### 🟡 The Integrator (Power User/Data Scientist)
* **Profile:** You use Python, R, or Bash to automate data retrieval for research.
* **Focus:** Authentication, pagination, rate limits, and JSON parsing.
* **Featured Resource:** [Jupyter Notebook: Querying TB Portals via API](./02-Intermediates/python-requests.ipynb)

### 🔵 The Provider (Developer/Architect)
* **Profile:** You are building or maintaining a service that shares NIAID data.
* **Focus:** RESTful design, OpenAPI specifications, and FAIR data principles.
* **Featured Resource:** [NIAID API Design & Security Standards](./03-Providers/design-principles.md)

---

##  NIAID API Showcase
We use real NIAID endpoints to teach these concepts. Explore the diverse ecosystem:

| API Service | Best For | Technical Complexity |
| :--- | :--- | :--- |
| **NIAID Discovery Portal** | Searching across datasets | ⭐ (Introductory) |
| **TB Portals API** | Clinical and Genomic data | ⭐⭐ (Intermediate) |
| **ImmPort** | Immunology studies | ⭐⭐⭐ (Advanced) |
| **AccessClinicalData** | Controlled-access clinical trials | 🔐 (Security-focused) |

---

##  Quick Start: Your First "Call"
You don't need code to see an API in action. Copy and paste this URL into your browser to see the latest **Influenza** research metadata from the NIAID Discovery Portal:

`https://api.data.niaid.nih.gov/v1/query?q=influenza&size=1`

> [!TIP]
> **What are you looking at?** That text is **JSON**. It is the universal language of APIs. It is structured so that both humans and computers can read it.

---

##  Repository Structure
* `01-Foundations/`: Definitions, analogies, and no-code tools (Postman, Swagger).
* `02-Intermediates/`: Python/R scripts, handling API keys, and data cleaning.
* `03-Providers/`: Best practices for building APIs that meet NIH data sharing policies.
* `examples/`: Boilerplate code snippets for NIAID services.

---

## Contributing
Are you an NIAID developer with an API you'd like to feature? Please see [CONTRIBUTING.md](CONTRIBUTING.md) to add your service to our showcase.

---
*Maintained by the NIAID Training Group. This resource is for educational purposes within the NIH ecosystem.*
