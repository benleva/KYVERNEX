# M6 Scope Lock — Minimum Shippable Plugin

Status: `FROZEN`
Target product line: `1.2.0`
Applies to: `M6 — KYVERNEX Plugin Runtime`

## 1. Single objective

M6 exists to deliver one installable and testable KYVERNEX plugin that an in-process Python host can initialize, call once through the governed execution path, inspect and shut down.

The required end-to-end path is:

```text
Python host -> KyvernexPluginRuntime -> governed request decision -> bounded in-process adapter -> structured response
```

M6 is complete when this path works from a clean installation and is covered by green tests and a smoke example.

## 2. Required deliverables

Only these deliverables are required:

1. frozen plugin contract;
2. deterministic lifecycle runtime;
3. structured request, response and error envelopes;
4. immutable fail-closed configuration;
5. one reference in-process adapter wrapping a host-supplied Python callable;
6. focused security and lifecycle integration tests;
7. one minimal installable example and one package entry point;
8. clean build, clean installation and smoke verification;
9. prerelease evidence for the `1.2.0` line.

## 3. M6-W004 hard limit

M6-W004 may implement only one reference adapter with these properties:

- wraps one explicitly supplied Python callable;
- exposes only explicitly declared capabilities;
- performs no network, filesystem, subprocess, repository or publication operation by itself;
- reads no environment variable;
- discovers no plugins dynamically;
- makes no governance or authorization decision;
- invokes the callable only after the runtime has authorized the request;
- returns a JSON-serializable result or a governed adapter error;
- provides a simple health state;
- supports idempotent shutdown.

No second adapter is permitted inside M6.

## 4. Explicitly out of scope

The following are not part of M6 and MUST NOT be added while completing it:

- remote, HTTP, WebSocket or RPC adapters;
- adapters for ChatGPT, browsers, IDEs, CMS platforms or third-party products;
- plugin marketplace, discovery, registry or dynamic loading;
- background workers, queues, schedulers or distributed execution;
- database persistence;
- graphical interface or management dashboard;
- authentication service, user management or billing;
- secret vault implementation;
- container orchestration or sandbox platform;
- arbitrary filesystem, network or subprocess execution;
- GitHub mutation, repository automation or release publication from the plugin;
- multiple programming-language SDKs;
- independent implementation or conformance certification;
- performance optimization beyond preventing obvious unbounded behavior;
- new strategic-roadmap milestones.

These ideas require a future separately authorized milestone.

## 5. Change-control rule

No new M6 capability may be introduced unless it is strictly necessary to make the single required end-to-end path installable, executable or verifiable.

A proposed change is rejected when any answer below is `no`:

1. Is it required for the single Python in-process plugin path?
2. Is it required by the frozen M6 contract?
3. Can it be completed without adding a new external system or adapter type?
4. Does it preserve fail-closed authority?
5. Does it move M6 measurably closer to clean-install smoke verification?

## 6. Stop rule

After M6-W004, work proceeds directly to focused integration tests, the minimal example, complete verification and prerelease evidence. No feature-expansion work item may be inserted between them.
