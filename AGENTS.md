# PolicyEngine US Agent Instructions

Follow the repository guidance in `CLAUDE.md` for commands, style, changelog entries, and PolicyEngine modeling conventions.

## Partner API Contract Tests

Files under `policyengine_us/tests/policy/baseline/partners/**` are API partner contract tests.

Do not rewrite these expected outputs merely to match changed model behavior or make CI pass. If a model change causes one of these tests to fail, treat that as a possible partner-facing API change.

Subagents must not edit partner test files. If a subagent finds that an edit is needed, it must stop and report back; the top-level agent runs the three-question gate with the user before any edit is made.

Before changing expected outputs in this folder:

- Flag the partner-facing risk to the user.
- Use the `AskUserQuestion` tool to ask these three questions in a single call (per CLAUDE.md):
  1. Are you sure you want to edit this test file?
  2. Have you notified a team member about this change?
  3. Have you notified the API partner about this change?
- Identify the model change that caused the partner output change.
- Preserve the failing behavior as evidence unless the change is intentional.
- Explain the partner-facing impact to the user.

Changing these tests without explicit user confirmation is unsafe, even if CI passes afterward.

## Parameter Data Is Production Logic

Most of the business logic in this repository lives in data, not in code. Files
under `policyengine_us/parameters/**` are the policy database: YAML keyed by a
breakdown entity (declared in `metadata.breakdown`, most often `state_code`) and
by effective date.

```yaml
metadata:
  breakdown:
  - state_code
MO:
  2018-01-01: 1.55
```

The variables under `policyengine_us/variables/**` read those values at runtime:

```python
ma = parameters(period).gov.hhs.medicaid.eligibility.categories.older_child
income_limit = ma.income_limit[state]
return is_older_child & (income < income_limit)
```

So a two-character edit to a state key is a behavior change for every household
in that state, with no code in the diff to review.

### Invariants for reviewing a parameter change

1. **Scope.** A state-keyed file lists all fifty states next to each other. The
   dominant failure mode is editing a state the requirement never mentioned, or
   editing the state that was intended and leaving a neighbour edited too.
   Every key touched must be named in the ticket.
2. **Effective date.** The date under a key is when the value starts applying.
   A correction filed under the wrong date rewrites prior years.
3. **Downstream flow.** Follow the parameter's dotted path into
   `policyengine_us/variables/**` and name what moves. Some thresholds also
   re-route households between programs; work out from the code which programs
   are involved rather than assuming, and say so explicitly when it happens.
4. **Boundary coverage.** A moved threshold needs a baseline test on each side
   of the new value under `policyengine_us/tests/policy/baseline/**`.
