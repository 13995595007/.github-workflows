#!/usr/bin/env python3
"""Smoke tests for kid-reward-game.html.

Run: python3 scripts/test_kid_reward_game.py
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "kid-reward-game.html"


def assert_contains(text: str, pattern: str, description: str) -> None:
    if re.search(pattern, text, flags=re.MULTILINE) is None:
        raise AssertionError(f"Missing {description}: /{pattern}/")


def main() -> int:
    if not HTML_FILE.exists():
        print(f"FAIL: file not found: {HTML_FILE}")
        return 1

    html = HTML_FILE.read_text(encoding="utf-8")

    # Core UI elements
    assert_contains(html, r'id="score"', "score panel")
    assert_contains(html, r'id="stars"', "stars panel")
    assert_contains(html, r'id="streak"', "streak panel")
    assert_contains(html, r'id="goodBtn"', "good action button")
    assert_contains(html, r'id="badBtn"', "bad action button")
    assert_contains(html, r'id="difficultySel"', "difficulty selector")

    # Core gameplay rules
    assert_contains(html, r'score\s*=\s*Math\.max\(0,\s*state\.score\s*-\s*scoreRule\.bad\)', "score floor rule")
    assert_contains(html, r'state\.stars\s*=\s*Math\.floor\(state\.score\s*/\s*5\)', "star calculation rule")

    # Persistence
    assert_contains(html, r'localStorage\.setItem\(["\']kidRewardGameState["\']', "state persistence")
    assert_contains(html, r'localStorage\.getItem\(["\']kidRewardGameState["\']', "state restore")

    # Difficulty rules
    assert_contains(html, r'easy\s*:\s*\{\s*good:\s*2,\s*bad:\s*2', "easy scoring")
    assert_contains(html, r'normal\s*:\s*\{\s*good:\s*3,\s*bad:\s*2', "normal scoring")
    assert_contains(html, r'hard\s*:\s*\{\s*good:\s*4,\s*bad:\s*3', "hard scoring")

    print("PASS: kid-reward-game smoke checks passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
