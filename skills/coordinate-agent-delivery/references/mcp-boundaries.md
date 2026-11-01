# Reviewing an MCP boundary

Use this reference for an MCP adapter assignment or integration review. MCP is a tool protocol, not an identity provider, access grant, source of business truth or proof of model understanding. Preserve the deployment's actual policies rather than importing another installation's limits.

## Define the consumer contract

Identify the caller, permitted operations and fields, source and freshness meaning, output limits, pagination/snapshot contract, cancellation behavior, call budget and failure states. Separate a read from a write, and tool availability from permission to use it. Keep private integrations and credentials out of a public example; synthetic fixtures should be labeled as such.

Take agent, channel, account, caller identity and role from trusted runtime context and the existing authorization mechanism. Do not accept them as model-selected arguments. Validate input and output shapes, but do not treat schema validation as authorization. Use the existing scoped projection and record binding; an adapter must not silently broaden the data visible to its consumer.

An authorization or invocation check performed before an asynchronous operation may no longer be current afterward. Recheck through the trusted mechanism at the operation boundary before backend access or disclosure when the context could have changed. Preserve cancellation and existing revocation semantics. Do not create an independent role database or let a cached successful result outlive its authorization context.

## Preserve operation meaning

- Apply the real deployment's field and financial-disclosure rules and call budget. A skill statement does not enforce these controls; identify where trusted code does.
- Preserve the returned snapshot and cursor continuity. Distinguish incomplete pagination, size limits, stale evidence, unavailable evidence and an empty valid result. Do not fabricate continuation tokens or silently truncate business facts.
- Coalesce identical in-flight reads only when the contract permits it and the identity, record scope, snapshot and cancellation context are compatible. Do not share results across authorization scopes or turn this into persistent caching without an explicit contract.
- Do not coalesce writes just because their arguments match. A write needs its own operation semantics and authorization; any idempotency behavior must be designed and verified separately.
- Keep existing source ownership and scheduling. Adding an adapter does not authorize a new collector, source refresh, plugin installation, grant or background retry loop.

## Accept the integration in layers

Use an isolated staging package for review and relevant positive, negative, revocation and cancellation checks. Pin the exact artifact that was reviewed and compare it with the actual target before applying changes. Do not overwrite concurrent work.

Verify native registration or capture against the intended artifact, then retain the distinction between native activation, an authorized tool result, source coverage and natural model behavior. Test fixtures establish their named contract cases; they do not prove complete production privacy or general model reliability.

Observe existing natural source cycles when those cycles provide the needed integration evidence. If a source or artifact no longer matches its approved binding, fail closed for the affected operation and require a scoped review. A timeout alone does not prove version drift. Missing health metadata does not prove failure, and healthy transport does not prove permission or complete data coverage. Do not automatically adopt a new identity, fetch a replacement asset or repin a changed artifact to make a check pass.

Keep a concrete rollback path and the evidence needed to decide whether to use it. Rollback instructions are not authorization to restart a healthy service or undo unrelated data changes.
