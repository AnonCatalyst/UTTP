# Entity Map — group level only

This map intentionally contains **no private individuals, addresses, employers,
or family details**. It maps groups, factions, and ecosystems so a reader can
follow the archive without treating it as a target list.

```mermaid
graph TD
  UTTP[UTTP / UTube Troll Police]
  OLD[Old-sector / legacy UTTP]
  NU[Nu-UTTP / UTTP Empire]
  RUTTP[RUTTP / TYRANNY]
  AFR[Anti-Fandom Resistance]
  DPOS[DPOS]
  FPE[FPE ecosystem]
  FPEB[FPE-Police branding]
  AUTTP[AUTTP / Anti-UTTP coalition]
  N764[764 network]
  O9A[O9A]
  NLM[NLM / other NVE networks]
  WIC[WIC — documenter, not a member]
  SRA[SRA]
  TM[TM-TNM]
  UU[Universal Union]
  G148[148-1488]
  ENCL[UETR-GSR]
  SPWN[SPWN]
  E11[11th Street]
  C09A[09A Cult]

  UTTP --> OLD
  UTTP --> NU
  UTTP --> RUTTP
  UTTP --> AFR
  UTTP --> DPOS
  NU -. assessed edge fusion, not merger .-> N764
  N764 -. listed as O9A nexion .-> O9A
  N764 --- NLM
  UTTP -. targeted / infiltrated .-> FPE
  FPE --> FPEB
  FPE -. defense/archive context .-> WIC
  AUTTP -. opposes .-> UTTP
  UTTP -. documented affiliation/lead .-> SRA
  UTTP -. documented affiliation/lead .-> TM
  UTTP -. documented affiliation/lead .-> UU
  UTTP -. documented affiliation/lead .-> G148
  UTTP -. documented affiliation/lead .-> ENCL
  UTTP -. documented affiliation/lead .-> SPWN
  DPOS --> E11
  DPOS -. assessed tactical overlap, no command .-> N764
  DPOS -. target/incursion .-> FPE
  DPOS -. individual crossover .-> TM
  C09A -. parent/predecessor context .-> O9A
```

## Relationship table

| From | To | Relationship | Confidence | Note |
| --- | --- | --- | --- | --- |
| UTTP | Old-sector / Nu-UTTP | Internal factions | A/D | Faction labels come from community/WIC records; boundaries are disputed. |
| UTTP | RUTTP/TYRANNY, AFR | Splinters | D | Community-reported; not formally confirmed. |
| UTTP | DPOS | Hardcore offshoot/splinter | C/D | DPOS inherits UTTP raid culture and targets; see `04_OFFSHOOTS/DPOS.../ANALYSIS/`. |
| DPOS | 764 | Tactical/ideological overlap; no command/merger | C/A | Grooming/blackmail/self-harm/shock overlap; not a 764 unit. |
| DPOS | FPE | Target/incursion ecosystem | A/S | FPE harassment/doxxing allegations; FPE is a target, not an ally. |
| DPOS | TNM/148/GRS/Enclave | Individual crossover | A/D | Personnel rotate between adjacent raid/extremist spaces. |
| UTTP | 764 | Edge fusion/membership overlap (assessed); no merger or operational-arm evidence | A/C | 764 is independently designated; UTTP-specific command/merger claims are not supported. |
| 764 | O9A | Listed as an O9A nexion in the NZ statement of case; decentralised ecosystem | E/C | Nexions are operationally independent; this is not a command relationship. |
| UTTP | FPE | Target/incursion ecosystem | A | WIC's FPE record; not an alliance. |
| WIC | FPE | Documenter / temporary defense role | A | WIC states it is not an FPE partner and did not accept a governing role. |
| AUTTP | UTTP | Opposition/coalition | D | Community documentation. |
| UTTP | SRA, TM-TNM, UU, 148-1488, UETR-GSR, SPWN | Affiliation/lead folders | A/D | Presence in `03_AFFILIATIONS/` means documented/lead material, not proof of command. |
| 09A Cult | O9A | Legacy archive label for O9A-adjacent material | D | Not a headquarters or proven parent; "09A" is an alternate spelling. |

## Reading rule

A line in this map is a **research relationship**, not a criminal charge. For a
specific allegation, use `CLAIM_LEDGER.md` and the underlying source.
