# Public showcase architecture

The published site is a static application: HTML, CSS, ES modules, an invented CSV and two selected excerpts from stored controlled training conversations. It has no backend, database connection, model provider, analytics, cookies or local-storage persistence.

## Data path

`showcase.mjs` renders authored scenarios. Its service example calls `serviceContext()` with a synthetic record and the selected role, vehicle/customer identity and observation age. The result selects an authored response. It is **not** an LLM call.

`report.html` reads the bundled sample or an explicitly selected local CSV. `engine.mjs` parses at most 1 MB / 1,000 rows and evaluates exact declared fields. User text is rendered with DOM `textContent`; reference strings are not turned into active links. Text export contains the imported text, so treat exported files as potentially sensitive if you use your own data.

The sample clock is fixed. Local imports use the user's current time. The CSV checker uses a 48-hour freshness threshold; the separate synthetic Linh example uses a 600-second observation gate. These are different examples, not interchangeable policies.

## What stays outside

Private integrations, messaging accounts, provider credentials, workshop datasets, private manuals, model prompts and deployment bundles are absent. The approved Q&A excerpt module contains only the selected controlled-exercise text and editorial translations. Full transcripts, account metadata and internal session identifiers remain private. Rendered Q&A images are labeled as rendered excerpts, not platform screenshots or independently verified message delivery.

In a real integration, authentication, authorization, customer binding, version/queue checks and source validation belong on trusted infrastructure. Do not promote this client-side demonstration to production by merely connecting a database or adding an API key.

## Hosting

The site can run on any static host. This project's GitHub Pages publication uses the `docs/` directory on `main`; there is no application build or package download. GitHub's own hosting infrastructure is outside the application's no-analytics claim.
