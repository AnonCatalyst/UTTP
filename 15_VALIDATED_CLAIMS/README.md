# Validated Claims

**Prepared:** 2026-11-19
**Purpose:** hold claims that survived source review, with confidence labels and
evidence. This is the positive counterpart to
[`16_VALIDATED_FALSE_CLAIMS/`](../16_VALIDATED_FALSE_CLAIMS/).

> A claim here is not necessarily an `E`. Read the confidence column. `C/A` means
> corroborated/assessed, not a court finding.

## Files

| File | Use |
| --- | --- |
| [`VALIDATED_CLAIMS.csv`](VALIDATED_CLAIMS.csv) | Machine-readable claim register. |
| [`SUMMARY.md`](SUMMARY.md) | Short human-readable summary by topic. |
| [`README.md`](README.md) | This rule sheet. |

## Confidence key

- **E** — government instrument, court record, primary document.
- **C** — corroborated by two or more independent sources.
- **A** — WIC assessment from the available record.
- **S** — single-source/unverified.
- **D** — community documentation.
- **X** — disputed/superseded. An `X` here appears only as a negative finding
  (“no evidence located”), not as an approved positive claim.

## Rules

1. Every claim must have a source and a confidence label.
2. A source supports only what it actually says.
3. A designation of 764 or O9A is not a designation of UTTP.
4. A profile path is not an owned account.
5. A community wiki is not a court finding.
6. A negative finding (“no evidence located”) is not proof that no private
   coordination exists; it means the public record does not support the claim.
