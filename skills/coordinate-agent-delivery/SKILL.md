---
name: coordinate-agent-delivery
description: Coordinate a requested multi-agent delivery with scoped assignments, parallel independent work, verifiable artifacts, review and correction, and separate integration and runtime acceptance.
---

# Coordinate agent delivery

Use this when the user wants work shared among assistants or agents. Keep responsibility for the requested outcome with the coordinator. Delegation is useful only when the recipient has the necessary context, access and a task that can be accepted independently. Do not create agents, sessions, fees or access grants merely because this skill is loaded.

## Assign work that can be checked

Start from the existing backlog, current artifacts and active assignments. Closed jobs are historical evidence; do not replay them as pending work. A new request can create a new scoped task without reopening or duplicating a completed deployment.

For each assignment, provide a stable task ID, objective, input version, permitted sources, output location, writer, reviewer, acceptance condition and relevant limits. Specify what the recipient can actually see; a local path is not a transferred file, and a repository link does not start a job. Include enough context to explain the larger user goal and the dependencies, without exporting unrelated private material.

Choose roles to fit the available agents. One useful split is: the coordinator owns host investigation, integration and release; a coding agent implements a defined code package; a workflow reviewer checks the business interpretation and communication. These are example responsibilities, not permanent authority attached to a model name. Explicit user authorization and actual tool permissions remain controlling.

## Parallelize independent work

Give each writable package one writer at a time. Run independent implementation, documentation and review preparation concurrently when their inputs and outputs are separable. Reviewers should return findings or a separate patch rather than changing the writer's files concurrently. Sequence dependent integration and deployment after the inputs are accepted. Do not make the user shuttle every artifact between agents when an authorized delivery route already exists.

Track distinct states in the existing tracker: prepared, sent, acknowledged, in progress, submitted, reviewed, accepted, integrated and runtime verified. A draft assignment file is not sent; a sent prompt or repository comment is not an acknowledgment or proof that an agent is running. Record the actual receipt or supported status. If delivery is uncertain, inspect that task's status before sending again. A blocked task should not stop independent work.

## Close the delivery loop

Receive the exact commit or content hashes, changed-file scope, checks actually run and limitations. Compare them against the assigned base and concurrent changes. Review the resulting behavior and business meaning, not just the test count. Ask for a correction tied to a concrete finding, then review the corrected artifact rather than accepting an earlier revision by implication.

Integrate only the accepted scope with the deployment's backup, rollback and authorization requirements. Check that the intended runtime actually loaded the intended artifact. A file on disk, successful build or active plugin registration is narrower evidence than a real authorized end-user result. Keep these levels separate in the acceptance record; do not substitute a paid model probe or outbound test message for missing natural-use evidence without authorization.

For a task that adds or changes an MCP adapter, read [MCP boundaries](references/mcp-boundaries.md) before defining its contract or accepting its integration. Other tasks do not need that reference.

Leave a continuation point with the accepted version, work still open, known evidence gaps, next responsible party and rollback condition. Report meaningful completion, failure or required action. Do not repeat unchanged pending status or claim continuous monitoring without an existing mechanism that actually runs.

## Authored synthetic example

A user requests a reusable service-update workflow. The coordinator gives the coding agent a new adapter package, asks a separate reviewer to examine the wording and record boundaries, and drafts installation instructions independently. The reviewer finds that “technician reported done” was presented as handover acceptance. The writer corrects that interpretation and submits a new artifact version. The coordinator accepts the corrected package, checks native loading, and records end-user behavior as unreviewed until a permitted observation exists.

This invented example illustrates ownership and evidence states. It does not show that any external agent was dispatched or that a system was deployed.
