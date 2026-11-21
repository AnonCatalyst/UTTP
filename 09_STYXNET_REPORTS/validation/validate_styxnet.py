#!/usr/bin/env python3
"""Validate the StyxNet UTTP export without modifying the raw files.

Outputs are group-level review artifacts. They do not establish ownership,
membership, or intent. Raw exports remain unchanged.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "09_STYXNET_REPORTS" / "styxnet_UTTP_csv_1789803261.csv"
OUT = Path(__file__).resolve().parent

PLATFORM_VARIANTS = [
    ("Codecademy", "Codecademy", "brand"),
    ("codersrank-org", "CodersRank", "variant"),
    ("codersrank", "CodersRank", "brand"),
    ("thesimsresourcedotcom", "The Sims Resource", "variant"),
    ("TheSimsResource", "The Sims Resource", "brand"),
    ("livetrack24", "LiveTrack24", "variant"),
    ("LiveTrack24", "LiveTrack24", "brand"),
    ("HackThisSite.org", "HackThisSite", "variant"),
    ("hackthissite", "HackThisSite", "variant"),
    ("HackThisSite", "HackThisSite", "brand"),
    ("MAGIX_INT", "MAGIX", "variant"),
    ("MAGIX", "MAGIX", "brand"),
    ("magix", "MAGIX", "variant"),
    ("WynkMusic", "Wynk Music", "brand"),
    ("wynkmusic", "Wynk Music", "variant"),
    ("Salon24pl", "Salon24", "variant"),
    ("salon24.pl", "Salon24", "brand"),
    ("FlashFlashRevolution", "FlashFlashRevolution", "brand"),
    ("TheOfficial_FFR", "FlashFlashRevolution", "variant"),
    ("ffr", "FlashFlashRevolution", "variant"),
    ("Podcastindex-org", "Podcast Index", "variant"),
    ("PodcastindexOrg", "Podcast Index", "variant"),
    ("pennyarcadetv", "Penny Arcade TV", "brand"),
    ("subscan_io", "Subscan", "variant"),
    ("stackernews", "Stacker News", "brand"),
    ("cssbattle.dev", "CSSBattle", "brand"),
    ("css_battle", "CSSBattle", "variant"),
    ("dicedotcom", "Dice", "variant"),
    ("coddytech", "Coddy", "variant"),
    ("coddy.tech", "Coddy", "brand"),
    ("coddylearn", "Coddy", "variant"),
    ("coddy_tech", "Coddy", "variant"),
    ("flyertalkforums", "FlyerTalk", "variant"),
    ("FlyerTalk", "FlyerTalk", "brand"),
    ("prokoni.ru", "Prokoni", "brand"),
    ("prokoni_ru", "Prokoni", "variant"),
    ("car72ru", "Car72", "variant"),
    ("wwwcar72ru", "Car72", "variant"),
    ("LancerX.ru", "LancerX", "brand"),
    ("LancerX_ru", "LancerX", "variant"),
    ("TTSPORT.ru", "TTSPORT", "brand"),
    ("poembook_ru", "Poembook", "variant"),
    ("maccentre_ru", "MacCentre", "variant"),
    ("yamaya_ru", "Yamaya", "variant"),
    ("radiomedru", "Radiomed", "variant"),
    ("romanticcollectionru", "RomanticCollection", "variant"),
    ("bysoloby", "BySoloby", "brand"),
]

GENERIC = {
    "platform", "share", "member", "user", "channel", "dialog", "intent",
    "playlist", "pages", "images", "uploads", "en-us", "pastebin", "sharer.php",
}

TIER1 = {"frickfunnymikeuttpthtdc", "uttp_offical", "uttpmastdept"}
TIER2 = {
    "uttparkrosie.bsky.social", "michaelsuttptv.bsky.social",
    "uttpalette.bsky.social", "kiloratstrzntputtp.bsky.social",
    "uttpofficercoplord.bsky.social", "uttp-lieutenant2.bsky.social",
    "uttpus.bsky.social",
}
TIER3 = {"uttpower", "kecuttpikding1970", "vecuttpadi1981", "uttpthdtc"}
TARGET = {"uttp"}
UTTAPAL = {
    "uttpal", "uttpalsingh", "uttpalmishra", "uttpal47", "uttpalkachhawa",
    "uttpatisahu", "uttpol11", "uttpalkant", "uttpal-tripathy", "uttpal1",
    "uttpaul", "uttpal95", "uttpal-076", "uttprerak", "uttpal-kumar",
    "uttpesh-vyas",
}
NUMERIC_LOW_SIGNAL = {"uttp3", "uttp333"}
FUZZY = {"utp", "utti", "utop"}


def nkey(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def nurl(value: str) -> str:
    value = (value or "").strip().lower().rstrip("/")
    value = re.sub(r"^https?://", "", value)
    value = re.sub(r"^www\.", "", value)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify_handle(handle: str) -> tuple[str, str, str, str]:
    key = nkey(handle)
    low = (handle or "").lower()
    if key in {nkey(v) for v, _, _ in PLATFORM_VARIANTS}:
        return "rejected", "platform_identity_string", "X", "Platform brand/site identity, not a user handle"
    if key in {nkey(v) for v in GENERIC}:
        return "rejected", "generic_field_label", "X", "UI/state label, not a user handle"
    if key in {nkey(v) for v in TIER1}:
        return "candidate", "brand_token_tier1", "A", "Brand/faction token; structural only"
    if key in {nkey(v) for v in TIER2}:
        return "candidate", "brand_token_cluster_tier2", "A", "Structured Bluesky cluster; structural only"
    if key in {nkey(v) for v in TIER3}:
        return "candidate", "brand_token_tier3", "S", "Single-source brand token; unverified"
    if key in {nkey(v) for v in TARGET}:
        return "candidate", "target_handle_only", "S", "Exact target string; no ownership evidence"
    if key in {nkey(v) for v in UTTAPAL}:
        return "rejected", "collision_uttapal_name", "X", "Unrelated personal name containing 'uttp'"
    if key in {nkey(v) for v in NUMERIC_LOW_SIGNAL}:
        return "rejected", "low_signal_numeric", "X", "Low-signal numeric string; no brand evidence"
    if key in {nkey(v) for v in FUZZY}:
        return "rejected", "fuzzy_match_false_positive", "X", "Fuzzy match, not exact token"
    if key in {"puttputt", "smuttprogramming", "pnuttpad"} or "butt" in low:
        return "rejected", "substring_collision_butt", "X", "'uttp' spans an unrelated word"
    return "review", "unclassified", "D", "Needs manual review"


def classify_row(row: dict[str, str], seen_urls: set[str]) -> str:
    url = nurl(row["url"])
    title = (row["title"] or "").lower()
    status = row["status"]
    if status not in {"200", "206", "204"}:
        return "error_or_non_200"
    if row["platform"].lower() == "npm" and "github.com" in url:
        return "non_profile_artifact"
    if any(
        marker in url
        for marker in (
            "/search", "search?", "keywords=", "author=", "?q=", "&q=",
            "query=", "filter?search", "/find?", "search-index",
        )
    ):
        return "search_or_query_page"
    if any(
        marker in title
        for marker in (
            "login", "log in", "sign in", "signin", "register", "вход",
            "регистрация", "error", "ошибка", "404", "not found",
            "access denied", "one moment", "making sure", "just a moment",
            "validating",
        )
    ):
        return "error_or_gated_page"
    if any(
        marker in title
        for marker in (
            "информация", "information", "результаты поиска", "search results",
            "dice account", "already a member", "auth-controller",
        )
    ):
        return "gated_or_generic_page"
    if url in seen_urls:
        return "duplicate_url"
    seen_urls.add(url)
    parts = re.split(r"[/?=&@]+", url)
    if any(part == "uttp" or part.startswith("uttp.") for part in parts):
        return "profile_path_unverified"
    return "unclear"


def main() -> None:
    rows = list(csv.DictReader(RAW.open(newline="")))
    OUT.mkdir(parents=True, exist_ok=True)

    with (OUT / "styxnet_platform_name_blocklist.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["variant", "canonical_platform", "normalized_key", "category", "reason"])
        for variant, canonical, category in PLATFORM_VARIANTS:
            writer.writerow([
                variant,
                canonical,
                nkey(variant),
                category,
                "Platform/site identity string, not a user handle",
            ])

    handles: dict[str, dict[str, object]] = defaultdict(
        lambda: {"count": 0, "platforms": set(), "source_types": set()}
    )
    for row in rows:
        handle = row["aliases"] or row["similar_username"]
        if not handle:
            continue
        if row["platform"].lower() == "npm" and "github.com" in (row["url"] or "").lower():
            continue
        item = handles[handle]
        item["count"] = int(item["count"]) + 1
        item["platforms"].add(row["platform"])
        item["source_types"].add(row["search_type"])

    handle_counts: Counter[tuple[str, str]] = Counter()
    candidates: list[dict[str, object]] = []
    for handle, item in handles.items():
        status, reason, confidence, note = classify_handle(handle)
        handle_counts[(status, reason)] += 1
        if status == "candidate":
            candidates.append({
                "handle": handle,
                "platforms": ";".join(sorted(item["platforms"])),
                "occurrences": item["count"],
                "classification": reason,
                "confidence": confidence,
                "reason": note,
            })
    candidates.sort(key=lambda row: (row["classification"], row["handle"].lower()))

    with (OUT / "styxnet_handle_candidates.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["handle", "platforms", "occurrences", "classification", "confidence", "reason"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(candidates)

    with (OUT / "styxnet_handle_class_counts.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["status", "reason", "count"])
        for (status, reason), count in sorted(handle_counts.items()):
            writer.writerow([status, reason, count])

    seen_urls: set[str] = set()
    row_counts: Counter[str] = Counter()
    for row in rows:
        row_counts[classify_row(row, seen_urls)] += 1

    with (OUT / "styxnet_row_class_counts.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["row_class", "count"])
        for row_class, count in sorted(row_counts.items()):
            writer.writerow([row_class, count])

    summary = {
        "raw_file": str(RAW.relative_to(ROOT)),
        "raw_sha256": sha256(RAW),
        "raw_rows": len(rows),
        "search_types": dict(Counter(row["search_type"] for row in rows)),
        "platform_variants": len(PLATFORM_VARIANTS),
        "platform_normalized_keys": len({nkey(v) for v, _, _ in PLATFORM_VARIANTS}),
        "unique_handles": len(handles),
        "handle_classes": {
            f"{status}:{reason}": count for (status, reason), count in sorted(handle_counts.items())
        },
        "row_classes": dict(sorted(row_counts.items())),
        "candidate_handles": len(candidates),
        "ownership_verified": 0,
    }
    (OUT / "styxnet_validation_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    for candidate in candidates:
        key = nkey(str(candidate["handle"]))
        if key in {nkey(v) for v, _, _ in PLATFORM_VARIANTS}:
            raise SystemExit(f"platform name leaked into candidates: {candidate['handle']}")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
