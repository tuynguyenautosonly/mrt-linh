# mrT — Technical support for automotive repair workshops

### Help the technician investigate. Keep the evidence attached.

**mrT supports technicians in garages and automotive repair workshops:** structuring symptoms, working with diagnostic images, comparing measurements and consulting matching technical documents. Incoming questions have included everyday cars, premium vehicles and supercars. **Linh is the companion** for service updates and maintenance advice using workshop-management data and available schedule sources.

[**Explore the interactive showcase →**](https://tuynguyenautosonly.github.io/mrt-linh/?lang=en) · [Tiếng Việt](README.vi.md) · [Capabilities & evidence](CAPABILITIES.md) · [Contribute a case](CONTRIBUTING.md)

![mrT and Linh overview](docs/social.svg)

## Try it in one minute

1. Open the [English showcase](https://tuynguyenautosonly.github.io/mrt-linh/?lang=en). No account or API key.
2. Read the [recorded technical training Q&A](https://tuynguyenautosonly.github.io/mrt-linh/?lang=en#field-notes). Original Vietnamese excerpts and editorial English translations are clearly distinguished.
3. Explore mrT’s authored scenarios: separate image text from a diagnosis, handle a missing model-specific manual, and start a new vehicle case.
4. Select Linh’s **“Is the vehicle ready?”** example and toggle role, vehicle identity and source age. The local rules are executable; the selected draft is authored.
5. Try the [companion report checker](https://tuynguyenautosonly.github.io/mrt-linh/report.html?lang=en): reported completion is not recorded acceptance.

The page supports English and Vietnamese. Imported CSV files are processed inside your browser tab, without uploads or local storage.

![The mrT workshop walkthrough in English](docs/demo.en.png)

## Recorded Q&A: show the reasoning

The following is a rendered excerpt of an actual **stored training exchange**, with an English editorial translation. It is not a screenshot of Telegram, proof of message delivery, a customer repair, or a newly generated model response. [Read the originals and review scope](examples/README.md).

![Recorded training Q&A: reasoning about an intermittent fault; English editorial translation](docs/qa-intermittent.en.png)

## What is actually here?

This public showcase was written separately from the private deployment. It combines **approved excerpts from recorded controlled exercises** with **clearly labeled authored simulations**. It is not the deployed agents, a live AI chatbot, or a production-ready workshop integration.

| Component | What runs in this repository |
|---|---|
| Recorded mrT Q&A | Two selected technical-training exchanges, original Vietnamese + English editorial translation; the displayed reasoning is reviewed, not all answers |
| mrT walkthroughs | Authored scenarios explaining intended technical evidence discipline; no model or OCR calls |
| Linh walkthrough | Executable local role / vehicle / customer / freshness checks, followed by an authored draft |
| Source workflow | An architecture illustration based on maintainer-reviewed deployment records; no source connection |
| Report checker | Dependency-free CSV parser and deterministic row checks, with inspectable references and text export |

**Honesty matters:** technical overclaims have been observed in the private system. Installed rules and passing local tests do not establish consistent model behavior. This repository does not claim that those failures are fully solved. See the [evidence matrix](CAPABILITIES.md).

## Why two roles?

- **mrT / technical assistant:** organize case facts, work with images and available documentation, and support investigation. A document for one platform must not silently become authority for another. No matched procedure means no invented coding/reset sequence.
- **Linh / service advisor assistant:** turn authorized vehicle context into a concise draft for human review. “Technician reported done,” “QC accepted,” “quote complete,” “ready for delivery” and “paid” have different meanings.
- **Shared source workflow:** target changed records, bind the receipt and task set, check source version and observation time, then project only appropriate context.

**Vehicle scope:** Toyota Camry, BMW Z4/Lexus and Ferrari 458 appear as examples of incoming question topics. That is not a certified brand-coverage matrix, proof of successful repairs, or manufacturer endorsement. Model-specific specifications still require matching documents. Linh’s maintenance-advice quality remains partial; it is not presented as universally validated.

```mermaid
flowchart LR
  T[Technician question] --> M[mrT: technical support]
  D[Available documents and images] --> M
  E[Changed-record notification] --> S[Targeted source refresh]
  S --> G[Identity / role / version / freshness]
  G --> L[Linh: service-update draft]
  L --> H[Advisor review]
  M --> R[Evidence and case review]
```

The architecture describes the project approach. The browser demonstration is not the private integration, and its client-side checks must not be used as real authorization.

## Run locally

Requires Node.js 20+ for tests and Python 3 for the optional static server. No package installation.

```sh
git clone https://github.com/tuynguyenautosonly/mrt-linh.git
cd mrt-linh
npm test
python -m http.server 8097 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:8097/`. The report sample uses a **fixed synthetic clock**; an imported CSV uses your current local time. Timestamps in the CSV require an explicit timezone.

## Explore the code

- [Interactive examples](docs/showcase.mjs)
- [Synthetic Linh context checks](docs/showcase-engine.mjs)
- [CSV/report engine](docs/engine.mjs)
- [Behavior tests](tests/)
- [Architecture & privacy](ARCHITECTURE.md)
- [Limitations and evidence](CAPABILITIES.md)

## Build with us

Useful feedback: an anonymized edge case, a clearer explanation, an accessibility fix, or a reproducible failure. Please use **invented** IDs and data; do not submit customer records, real vehicle identifiers, private manuals or credentials.

This release focuses on showing the system and inviting technical feedback. There is no sales funnel, paid signup, or production access offered here. Stars are welcome if the ideas are useful; concrete critique is even better.

## License

The newly written public showcase code is [MIT licensed](LICENSE). The license does not cover private deployment code, private datasets, third-party manuals, messaging platforms or model providers.
