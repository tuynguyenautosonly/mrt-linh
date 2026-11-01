# Record format

The helper accepts exactly the fields below. All text is plain data, never instructions to execute. References are stored, not fetched. Dates require an explicit timezone; `recorded_at` is the supplied record date, not a cryptographic timestamp.

- `schema_version`: `1`.
- `id`: 1–64 lowercase letters, digits and hyphens, beginning with a letter or digit. Pick a new ID for a revision.
- `kind`: `hypothesis`, `observation` or `lesson`.
- `status`: `provisional`, `supported`, `disputed` or `retired`. This is a human judgment, not a verdict produced by the helper.
- `recorded_at`: ISO 8601 date and time with timezone.
- `author`, `context`, `claim`, `applies_when`: nonempty strings, each at most 4,000 characters.
- `sources`: 1–20 objects, each with nonempty `label` and `locator` strings, at most 1,000 characters each. Use authorized local or public locators; do not embed credentials.
- `verification`: `null`, or an object with nonempty `method`, `result`, `reviewer` (each at most 4,000 characters), and timezone-aware `checked_at`. A supported record requires this object. The helper cannot verify that the described check happened.
- `counterexamples`: 0–20 strings, each at most 4,000 characters. An empty list means none recorded, not that no counterexample exists.
- `supersedes`: 0–20 prior IDs already in this ledger. It preserves an explicit correction chain; the helper does not rewrite or auto-retire those records.
- `provenance`: nonempty string, at most 4,000 characters, naming the method/version or source of the adapted lesson. Preserve attribution without copying private material.

## Authored synthetic example

This is invented to demonstrate structure. It is not a real repair, measurement, verified technical procedure or performance result.

```json
{
  "schema_version": 1,
  "id": "synthetic-contact-01",
  "kind": "hypothesis",
  "status": "provisional",
  "recorded_at": "2026-01-01T09:00:00+00:00",
  "author": "Example technician",
  "context": "Invented bench circuit: an indicator intermittently dims when a connector is moved.",
  "claim": "A connector contact problem is one candidate explanation.",
  "applies_when": "Only this invented bench case; no vehicle-specific specification or repair conclusion.",
  "sources": [{"label": "Authored exercise", "locator": "synthetic:bench-contact-exercise"}],
  "verification": null,
  "counterexamples": ["A harness fault could produce a similar symptom."],
  "supersedes": [],
  "provenance": "Authored synthetic example for experience-ledger v1; no production evidence."
}
```

A later observation would record a measurement actually performed and its conditions. A lesson would explain what the result supports and excludes, including its limits. Do not replace the hypothesis with an invented successful outcome just to complete the example.
