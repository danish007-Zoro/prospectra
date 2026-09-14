# Prospectra

### Autonomous Company Intelligence Agent

Prospectra is a Python-based autonomous web intelligence agent that crawls public company websites, collects relevant evidence, uses an LLM to extract structured company intelligence, validates the extracted information against source pages, and produces machine-readable results.

## Overview

The agent accepts a list of company domains and autonomously:

1. Opens the company website using Playwright.

2. Discovers relevant internal pages such as About, Contact, Team, Leadership, Pricing, and company-related pages.

3. Uses an LLM to decide whether additional pages are needed.

4. Retrieves selected pages with a real browser, supporting JavaScript-rendered websites.

5. Removes unnecessary HTML content such as scripts, styles, SVGs, and other non-content elements.

6. Builds a compact evidence context for the LLM.

7. Extracts structured company intelligence using a strict Pydantic schema.

8. Verifies extracted emails and leadership information against collected page evidence.

9. Calculates a confidence score using LLM confidence, evidence verification, and page coverage.

10. Optionally enriches leadership records with publicly discoverable LinkedIn URLs.

11. Tracks LLM token usage and estimates processing cost.

12. Isolates company/page failures so one failure does not terminate the complete run.

13. Writes the final results to `output/output.json`.

## Architecture

```text
Company Domains
      |
      v
+-------------------+
|  Browser Manager  |
|    Playwright     |
+-------------------+
      |
      v
Homepage Retrieval
      |
      v
Relevant URL Discovery
      |
      v
+-------------------------+
| Autonomous Navigation   |
| LLM decides next page   |
+-------------------------+
      |
      v
Selected Web Pages
      |
      v
HTML Cleaning
      |
      v
Context Builder
      |
      v
+-------------------------+
| Structured LLM          |
| Company Extraction      |
+-------------------------+
      |
      v
Pydantic Validation
      |
      v
Evidence Verification
      |
      v
Confidence Calculation
      |
      +----------------------+
      |                      |
      v                      v
LinkedIn Enrichment     Cost Tracking
      |                      |
      +----------+-----------+
                 |
                 v
          CompanyResult
                 |
                 v
           output.json
```

## Extracted Intelligence

For each company, the agent extracts:

- **Company Overview** — concise two-sentence description.
- **Target Audience / ICP** — primary customer or user group.
- **Contact Points** — public generic/business email addresses.
- **Key Leadership / Team Members** — names, roles, source URLs, and LinkedIn URLs when discoverable.
- **Confidence Score** — final confidence between `0.0` and `1.0`.

The extraction schema uses Pydantic with strict validation and rejects unexpected fields.

## Autonomous Navigation

The agent does not rely exclusively on a fixed list of URLs.

After collecting the homepage, relevant internal links are discovered and ranked. The navigation decision-maker then evaluates the evidence collected so far and decides whether:

- `finish` — the required intelligence is sufficiently supported, or
- `visit_page` — another available page should be visited.

The decision-maker considers four required information categories:

1. Company overview
2. Target audience / ICP
3. Public contact emails
4. Key leadership / team members

The agent can therefore stop early when sufficient evidence has been collected rather than always visiting every discovered page.

## Context Preprocessing

Raw HTML is not sent directly to the LLM.

The cleaning stage removes:

- JavaScript
- CSS
- SVG elements
- `noscript` content
- unnecessary HTML structure

Useful headings, paragraphs, and list items are converted into compact text/markdown-like evidence.

The context builder prioritizes higher-value page types such as:

- About
- Contact
- Team
- Leadership
- Homepage
- Company

and applies a character budget before sending evidence to the extraction model.

## Structured LLM Extraction

The project uses the OpenAI Python SDK with an OpenAI-compatible Groq endpoint.

The extraction model is:

```text
openai/gpt-oss-20b
```

The LLM is instructed to use only the supplied website evidence and not invent missing information.

The response is validated using Pydantic before being accepted by the pipeline.

## Evidence Verification

LLM-generated contact and leadership records are checked against the collected page evidence.

For example, an extracted email is considered verified only if:

- its source page exists in the collected evidence, and
- the email appears in that page's cleaned content.

Leadership records are similarly checked for the presence of both the person's name and role on the cited source page.

## Confidence Scoring

The final confidence score combines three signals:

- LLM-provided confidence
- Evidence verification
- Website coverage

This produces a normalized score between `0.0` and `1.0`.

The purpose is to avoid relying exclusively on the LLM's own confidence estimate.

## Resilience

The agent is designed to continue operating when individual operations fail.

Handled failure categories include:

- DNS failures
- HTTP errors
- Page timeouts
- Browser errors
- LLM errors
- JSON/validation errors
- Unexpected errors

A failed page is isolated from the navigation loop, while a failed company is isolated from the remaining companies in the batch.

## LinkedIn Enrichment

As a bonus capability, leadership members without a LinkedIn URL can be enriched using an external search query.

The search is restricted to LinkedIn profile URLs and validates returned search evidence against the person's name before accepting a result.

## Cost Tracking

LLM usage is collected for both:

- navigation decision calls
- structured extraction calls

The agent reports:

- input tokens
- output tokens
- total tokens
- estimated LLM cost

This makes the pipeline's LLM usage measurable.

## Project Structure

```text
software-brio-ai-agent/
│
├── src/
│   ├── agent.py
│   ├── browser.py
│   ├── cleaner.py
│   ├── confidence.py
│   ├── context_builder.py
│   ├── cost_tracker.py
│   ├── decision.py
│   ├── errors.py
│   ├── extractor.py
│   ├── linkedin.py
│   ├── main.py
│   ├── navigation.py
│   ├── schemas.py
│   └── scraper.py
│
├── output/
│   └── output.json
│
├── test_agent.py
├── test_context.py
├── test_cost_tracker.py
├── test_errors.py
├── test_navigation.py
├── test_result.py
├── test_schema.py
├── test_scraper.py
├── test_validator.py
│
├── agent_check.py
├── all_domains_check.py
├── browser_check.py
├── context_check.py
├── encoding_check.py
├── extractor_check.py
├── links_check.py
├── scraper_check.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The `*_check.py` files are manual/integration checks and are intentionally separate from the automated unit-test suite.

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd software-brio-ai-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the Playwright browser

```bash
playwright install chromium
```

### 5. Configure the API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit `.env` to Git.

## Running the Agent

The test domains are configured in:

```text
src/main.py
```

The current evaluation domains are:

- `https://postman.com`
- `https://supabase.com`
- `https://vapi.ai`

Run the complete pipeline with:

```bash
python -m src.main
```

The final structured results are written to:

```text
output/output.json
```

## Running Tests

The automated test suite is intentionally designed to run without making external browser or LLM calls.

The current test suite contains **37 automated tests, all passing**.

```text
37 passed
```

Run the test suite with:

```bash
python -m pytest
```

The test suite covers:

- Pydantic schema validation
- Result validation
- Contact verification
- Leadership verification
- Error classification
- Navigation state management
- Navigation target validation
- Navigation context limits
- Context size limits
- Scraper URL discovery and classification
- Cost calculation
- Company failure isolation
- Page-level navigation failure handling

## Manual Integration Checks

The repository also contains manual checks for components that require real external services.

Examples:

```bash
python browser_check.py
python scraper_check.py
python context_check.py
python extractor_check.py
python agent_check.py
```

These are separate from the normal pytest suite because they may use real websites, Playwright, or the LLM API.

## Sample Output

A sample result is available in:

```text
output/output.json
```

The output follows the `CompanyResult` structure and records either successful intelligence or a structured processing error for each domain.

## Design Decisions

### Why Playwright?

Company websites frequently use JavaScript-rendered content. Playwright provides a real browser environment instead of relying only on static HTTP requests.

### Why preprocess HTML?

Raw HTML contains a large amount of information that is irrelevant to company intelligence, including scripts, styles, SVGs, and presentation markup. Cleaning reduces unnecessary context before sending information to the LLM.

### Why use structured output?

Free-form LLM responses are difficult to reliably consume programmatically. A strict Pydantic schema provides predictable fields and validation.

### Why verify LLM output?

The LLM can make mistakes even when given good evidence. Checking extracted claims against the collected source pages adds an independent verification layer.

### Why use a custom navigation loop?

The assignment requires agentic behavior, but a lightweight custom loop is sufficient for this task. It keeps the navigation logic understandable and avoids introducing a framework before it is necessary.

### Why separate unit and integration tests?

Unit tests should be fast, deterministic, and independent of external services. Browser and LLM behavior is tested separately through manual/integration checks.

## Limitations

- Some websites may block automated browsers or require additional anti-bot handling.
- Website structures vary significantly, so relevant-page discovery is heuristic.
- Public LinkedIn search results may be incomplete or unavailable.
- Confidence scoring is a heuristic rather than a calibrated probability.
- The agent only uses publicly accessible web information collected during the run.

## Technologies

- Python 3.11
- Playwright
- BeautifulSoup
- Pydantic
- OpenAI Python SDK
- Groq
- DDGS
- pytest