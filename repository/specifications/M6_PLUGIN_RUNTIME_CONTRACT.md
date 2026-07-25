# M6 KYVERNEX Plugin Runtime Contract

Specification ID: `KYVERNEX-M6-PLUGIN-CONTRACT`
Version: `1.0.0`
Target product line: `1.2.0`
Status: `FROZEN`
Stable dependency: `KYVERNEX 1.1.0`

## 1. Purpose

This specification defines the host-facing KYVERNEX plugin contract. It freezes identity metadata, lifecycle behavior, request and response envelopes, governed errors, configuration, host adapters, governance integration, authority boundaries, audit evidence and compatibility rules before runtime implementation.

The plugin is a bounded integration layer over the existing ARGUS, KPM, KGO and KEX capabilities. It is not an independent implementation and it is not a conformance-certification system.

## 2. Normative language

`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` and `MAY` are normative.

The runtime MUST fail closed whenever configuration, lifecycle state, authority, compatibility, request validity or authorization is ambiguous.

## 3. Plugin identity

Every runtime instance MUST expose:

- `plugin_id`: constant `kyvernex.plugin.runtime`;
- `plugin_api_version`: semantic version of this contract, initially `1.0.0`;
- `kyvernex_version`: installed KYVERNEX package version;
- `instance_id`: host-supplied or generated opaque identifier;
- `capabilities`: explicit immutable list negotiated during initialization;
- `state`: one lifecycle state defined below.

Identity metadata MUST NOT claim capabilities that are absent or disabled.

## 4. Lifecycle

### 4.1 States

The only valid runtime states are:

- `CREATED`: object exists but is not initialized;
- `INITIALIZED`: configuration and adapter are accepted;
- `READY`: initialization validation completed successfully;
- `EXECUTING`: one governed request is being processed;
- `DEGRADED`: runtime remains inspectable but execution is blocked;
- `SHUTDOWN`: terminal state.

### 4.2 Operations

The public lifecycle operations are:

- `initialize(config, adapter)`;
- `validate()`;
- `execute(request)`;
- `status()`;
- `shutdown()`.

### 4.3 Allowed transitions

| From | Operation | To |
|---|---|---|
| CREATED | initialize | INITIALIZED |
| INITIALIZED | validate | READY |
| READY | execute | EXECUTING |
| EXECUTING | successful completion | READY |
| EXECUTING | governed failure | READY |
| EXECUTING | runtime integrity failure | DEGRADED |
| CREATED | shutdown | SHUTDOWN |
| INITIALIZED | shutdown | SHUTDOWN |
| READY | shutdown | SHUTDOWN |
| DEGRADED | shutdown | SHUTDOWN |

All other transitions MUST be rejected with `INVALID_LIFECYCLE_TRANSITION`.

`SHUTDOWN` is terminal. A shutdown instance MUST NOT be reinitialized.

Only one request MAY execute per runtime instance at a time unless a future contract version explicitly defines concurrency.

## 5. Initialization contract

`initialize` MUST accept a structured configuration and a host adapter implementing the protocol in section 10.

Initialization MUST:

1. validate the configuration schema;
2. reject unknown security-sensitive fields;
3. verify adapter identity and declared capabilities;
4. calculate the effective authority as the intersection of configuration and adapter capability;
5. persist no secret in status or audit output;
6. move to `INITIALIZED` only after all checks succeed.

Initialization MUST NOT perform governed execution.

## 6. Validation contract

`validate` MUST verify:

- plugin and KYVERNEX version compatibility;
- required governance components are available;
- configured authority does not exceed adapter authority;
- filesystem paths are normalized and inside configured roots;
- network and process permissions are explicit;
- audit sink requirements can be satisfied;
- no unsupported capability is requested.

Successful validation moves the runtime to `READY`. Failure leaves it in `INITIALIZED` unless integrity is uncertain, in which case it moves to `DEGRADED`.

## 7. Host request envelope

Every execution request MUST contain:

```json
{
  "request_id": "opaque-non-empty-string",
  "operation": "governed.execute",
  "input": {},
  "context": {},
  "requested_capabilities": [],
  "authorization": {
    "principal": "opaque-principal-id",
    "grants": []
  },
  "limits": {
    "timeout_seconds": 30,
    "max_output_bytes": 1048576
  }
}
```

Rules:

- `request_id` MUST be unique within an instance audit history;
- `operation` MUST be a supported operation identifier;
- `input` MUST be JSON-serializable;
- `context` MUST NOT silently grant authority;
- `requested_capabilities` MUST be a subset of negotiated capabilities;
- `authorization.grants` MUST be explicit and independently validated;
- limits MUST be positive and MUST NOT exceed configured maximums;
- unknown top-level fields MUST be rejected by default.

The initial contract supports only `governed.execute`. Future operations require a contract-version change.

## 8. Host response envelope

Every completed request MUST return:

```json
{
  "request_id": "same-as-request",
  "status": "SUCCEEDED|BLOCKED|FAILED",
  "result": null,
  "error": null,
  "decision": {
    "authorized": false,
    "reason": "machine-readable-reason",
    "policy_ids": []
  },
  "evidence": {
    "execution_id": "opaque-id-or-null",
    "audit_record_ids": [],
    "started_at": "RFC3339 timestamp",
    "completed_at": "RFC3339 timestamp"
  },
  "plugin": {
    "plugin_id": "kyvernex.plugin.runtime",
    "plugin_api_version": "1.0.0",
    "kyvernex_version": "installed-version"
  }
}
```

Rules:

- `result` MUST be present only for `SUCCEEDED`;
- `error` MUST be present for `FAILED` and MAY be present for `BLOCKED`;
- `BLOCKED` is a governed outcome, not an execution crash;
- evidence MUST distinguish observed facts from claims;
- test, repository, release or publication success MUST NOT be asserted unless supplied by a verified external evidence source.

## 9. Governed error envelope

Errors MUST use:

```json
{
  "code": "MACHINE_READABLE_CODE",
  "message": "human-readable description",
  "category": "VALIDATION|LIFECYCLE|AUTHORIZATION|POLICY|ADAPTER|EXECUTION|INTEGRITY|COMPATIBILITY",
  "retryable": false,
  "details": {},
  "cause_id": null
}
```

Required initial error codes:

- `INVALID_CONFIGURATION`;
- `UNKNOWN_CONFIGURATION_FIELD`;
- `INVALID_LIFECYCLE_TRANSITION`;
- `PLUGIN_NOT_READY`;
- `REQUEST_SCHEMA_INVALID`;
- `DUPLICATE_REQUEST_ID`;
- `CAPABILITY_NOT_NEGOTIATED`;
- `AUTHORIZATION_REQUIRED`;
- `AUTHORITY_EXCEEDED`;
- `POLICY_BLOCKED`;
- `ADAPTER_CONTRACT_VIOLATION`;
- `EXECUTION_FAILED`;
- `EXECUTION_TIMEOUT`;
- `OUTPUT_LIMIT_EXCEEDED`;
- `RUNTIME_DEGRADED`;
- `INCOMPATIBLE_PLUGIN_API`;
- `INCOMPATIBLE_KYVERNEX_VERSION`.

Raw secrets, credentials, unrestricted filesystem paths and unfiltered subprocess output MUST NOT appear in error messages.

## 10. Host adapter protocol

A host adapter MUST expose:

- `adapter_id: str`;
- `adapter_version: str`;
- `capabilities() -> set[str]`;
- `invoke(request, authority) -> adapter_result`;
- `health() -> adapter_health`;
- `shutdown() -> None`.

The adapter MUST NOT decide KYVERNEX governance policy. It MAY report host capabilities and execute only an already authorized bounded action.

The runtime MUST validate adapter results before including them in a response.

An adapter MUST NOT expand authority based on request content, environment variables or implicit host privileges.

## 11. Governance and execution integration

The execution sequence MUST be:

1. request schema validation;
2. lifecycle validation;
3. capability and authorization validation;
4. ARGUS/KYVERNEX governance evaluation;
5. explicit decision recording;
6. KEX-bounded execution when authorized;
7. adapter result validation;
8. audit and evidence recording;
9. structured response construction.

Planning, authorization, execution and evidence are distinct phases and MUST NOT be collapsed into one unsupported claim.

A plan is not authorization. Authorization is not evidence of execution. Execution is not evidence of correctness.

## 12. Configuration contract

Initial configuration fields:

```json
{
  "plugin_api_version": "1.0.0",
  "instance_id": "optional-opaque-id",
  "allowed_capabilities": [],
  "filesystem": {
    "read_roots": [],
    "write_roots": []
  },
  "network": {
    "enabled": false,
    "allowed_hosts": []
  },
  "process": {
    "enabled": false,
    "allowed_commands": []
  },
  "limits": {
    "timeout_seconds": 30,
    "max_output_bytes": 1048576
  },
  "audit": {
    "required": true,
    "include_request_input": false
  }
}
```

Fail-closed defaults:

- no capability is allowed unless listed;
- filesystem read and write roots are empty;
- network is disabled;
- process execution is disabled;
- audit is required;
- request input is excluded from audit unless explicitly enabled;
- unknown fields are rejected;
- configuration changes after initialization are not supported in contract `1.0.0`.

No configuration field may silently increase authority.

## 13. Authority boundaries

### Filesystem

The plugin MUST NOT read or write outside normalized configured roots. Symlink and traversal escapes MUST be rejected. Empty roots mean no filesystem authority.

### Network

Network access is disabled by default. When enabled, only exact configured hosts may be used. Wildcard host authorization is not supported in contract `1.0.0`.

### Processes

Process execution is disabled by default. When enabled, command identity MUST match an explicit allowlist and execution MUST pass through KEX policy.

### Repository and publication

The plugin MUST NOT create or mutate Git refs, branches, pull requests, issues, releases or publication records unless a future separately authorized capability contract defines that authority.

### Secrets

Secrets MUST be supplied through the host adapter or an external secret provider. They MUST NOT be serialized into configuration, status, errors or evidence.

## 14. Status contract

`status()` MUST be non-mutating and return:

- identity metadata;
- lifecycle state;
- negotiated capabilities;
- effective authority summary without secrets;
- current request identifier or null;
- degraded reason or null;
- adapter health summary;
- last completed request status or null.

Status MUST NOT expose request payloads, credentials or unrestricted host internals.

## 15. Shutdown contract

`shutdown()` MUST:

- reject new requests;
- finish or governed-cancel the active request according to configured limits;
- invoke adapter shutdown once;
- flush required audit records;
- clear in-memory secrets;
- enter terminal state `SHUTDOWN`.

Repeated shutdown calls MAY be idempotent but MUST NOT repeat adapter side effects.

## 16. Audit and evidence

Each request MUST produce an audit chain containing, at minimum:

- request identifier;
- instance identifier;
- timestamps;
- validation outcome;
- requested and effective capabilities;
- governance decision;
- execution identifier when execution occurred;
- adapter identifier and version;
- response status;
- governed error code when applicable.

Evidence MUST be deterministic where inputs and external adapter results are deterministic. Evidence records MUST distinguish current-run facts from historical records.

## 17. Compatibility

The host MUST provide a supported `plugin_api_version` during initialization.

Contract `1.0.0` supports only the same major plugin API version. A major-version mismatch MUST fail with `INCOMPATIBLE_PLUGIN_API`.

The runtime MUST declare the minimum and maximum supported KYVERNEX package versions. Unsupported versions MUST fail before `READY`.

New optional response fields MAY be added in a backward-compatible minor contract revision only when unknown response fields are allowed by the host negotiation. New required request fields require a major contract revision.

## 18. Acceptance criteria derivable from this contract

The future runtime test suite MUST demonstrate:

1. every allowed lifecycle transition succeeds;
2. every forbidden transition fails closed;
3. shutdown is terminal;
4. duplicate request identifiers are rejected;
5. unknown request and security-sensitive configuration fields are rejected;
6. no capability can exceed the negotiated intersection;
7. filesystem, network and process defaults grant zero authority;
8. path traversal and symlink escapes are blocked;
9. unauthorized execution returns `BLOCKED`, not `SUCCEEDED`;
10. adapter contract violations cannot produce trusted results;
11. timeout and output limits are enforced;
12. status is non-mutating and secret-free;
13. audit records distinguish planning, authorization, execution and evidence;
14. version incompatibility is detected before readiness;
15. clean shutdown invokes adapter shutdown at most once.

## 19. Frozen decisions

The following decisions are frozen for M6 implementation:

- in-process Python runtime first;
- synchronous single-request execution per instance;
- JSON-serializable public envelopes;
- explicit adapter protocol;
- fail-closed unknown fields;
- zero authority by default;
- no repository or publication mutation authority;
- stable `v1.1.0` remains untouched;
- target line is `1.2.0`.

Any change to these decisions requires a new governed specification revision before implementation.