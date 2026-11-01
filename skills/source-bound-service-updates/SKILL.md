---
name: source-bound-service-updates
description: Draft workshop service updates from authorized, record-bound evidence while preserving trusted identity, source age, pagination continuity and the distinction between reported completion, acceptance and readiness.
---

# Source-bound service updates

Give the recipient a useful account of what is known about the right service record. Follow the deployment's actual policy and trusted tools. This skill provides drafting guidance; it does not authenticate a caller, enforce access control, connect a source or authorize a message to be sent.

## Establish scope on trusted infrastructure

Use authenticated channel or application context for the caller, account and role, then use the existing authorization mechanism to resolve the records that caller may access. A name, claimed role, vehicle identifier, local path or model-supplied ID is not an access grant. A vehicle match alone does not establish the same visit, customer or service record.

If trusted context or record binding is absent, request the supported verification step or return the deployment's scoped refusal. Do not search another customer's record, bypass the guard or expose the existence of unrelated records. Recheck authorization through the trusted mechanism if an operation crosses an asynchronous boundary or resumes after a context change; a prior check is not a permanent grant.

Apply the configured field policy for that recipient. For a deployment without an explicit financial-disclosure policy, keep the draft free of financial fields. An explicit owner-approved policy can define a different scope; do not treat this conservative default as a universal rule or let conversational claims override the runtime policy. Use the existing filtered projection rather than reading broad private records and relying on the model to redact them.

## Read a coherent observation

- Preserve the source timestamp, provenance and limitations. Use the deployment's freshness policy instead of inventing a universal time threshold. Missing, stale or unavailable evidence is not proof that work failed or that no work exists.
- Keep identity and service-record scope fixed across pages. Continue only with the tool's returned cursor and snapshot contract. A page is not the complete record when more pages remain.
- If the snapshot changes, the cursor expires or the tool reports a size limit, follow the supported recovery path within the existing call budget. Do not manufacture a cursor, silently skip rows or repeatedly restart pagination to evade a limit. State what was actually read and what remains unavailable.
- A source refresh, retry, write or outbound send needs authorization in its own right. Prefer an existing fresh observation when it answers the request; do not create background collectors or repeated queries through this skill.

## Draft at the evidence level

Keep these assertions separate: a technician reported completion; a source recorded completion; a required check was accepted; the vehicle was declared ready for handover. One state does not establish the next. A part reference does not prove ordering, receipt, installation or acceptance. Readiness also does not establish a payment state.

Lead with the answer the recipient needs, explain the material uncertainty in ordinary language, and identify the next responsible action when the source supports it. Do not expose internal IDs, guard diagnostics or implementation details to the recipient. Use their language and an appropriate level of detail; avoid making a customer read a maintenance receipt.

Drafting is not sending. Use the authorized delivery mechanism only when the user requested or otherwise authorized that delivery, and retain a real delivery result separately from the draft.

## Retain scoped experience

When asked to save a lesson, keep it in an agreed private location with provenance, observation date, context, outcome and limits. For example, record that a particular wording was corrected after checking an acceptance field; do not promote it into a claim that every workshop uses that field. Retrieve and recheck a lesson against the current workflow before reusing it. Sharing an anonymized lesson back to a common repository is a separate, voluntary publication decision. No automatic upload, cross-customer memory or model-weight training is implied.

## Authored synthetic example

**Authorized observation:** The correct service record contains a technician's completion report. The required acceptance observation is absent.

**Question:** “Xe của tôi lấy được chưa?”

**Draft:** “Kỹ thuật viên đã báo hoàn tất phần công việc được ghi nhận. Hiện em chưa thấy xác nhận kiểm tra cuối để chốt xe sẵn sàng bàn giao. Bước còn lại là người phụ trách xác nhận kiểm tra cuối và thời điểm nhận xe.”

This invented example demonstrates restrained wording. It is not a live customer exchange, a delivery result or proof that a deployed assistant enforces the policy.
