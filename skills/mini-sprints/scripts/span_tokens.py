#!/usr/bin/env python3
"""span_tokens.py — 統計一段對話區間的成本（opt-in，給 mini-sprints 量化卡關用）。

它**純本機計算**：讀 Claude Code 的 transcript JSONL，把指定區間內每則 assistant
訊息的 usage 加總、算出花費時間與對話來回次數。不呼叫任何 LLM、不把 transcript
讀進模型 context —— 所以幾乎不耗 token，只回傳幾個總和數字。

框定區間有兩種方式：

  1. 時間錨點（穩，建議）—— 起點訊息的 ISO timestamp：
       python3 span_tokens.py --from-time 2026-06-22T22:14:03.000Z
       python3 span_tokens.py --from-time <起> --to-time <訖>

  2. 文字錨點 —— 出現在某則訊息裡的一段文字：
       python3 span_tokens.py --from "要用 pull 還是 push" --to "決定用 X 方案"

不給終點（--to / --to-time）就統計到 transcript 結尾。不給 --transcript 就自動抓
「當前專案最新的」session 檔。時間與文字錨點可混用（例如 --from-time + --to）。

輸出三類指標：
  - 對話來回   : 區間內真人 user 回合數（排除 tool_result / meta）
  - 花費時間   : 區間首尾 timestamp 差
  - token      : input / cache_creation / cache_read / output 四類（Anthropic 口徑）
                 「新增 token」≈ input + cache_creation + output（cache_read 多為重複
                 讀取，成本低）。
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime


def detect_transcript(cwd: str) -> str | None:
    """從 cwd 推出專案的 transcript 目錄，回傳最新的 .jsonl。"""
    slug = re.sub(r"[^a-zA-Z0-9]", "-", cwd)
    proj_dir = os.path.expanduser(f"~/.claude/projects/{slug}")
    files = glob.glob(os.path.join(proj_dir, "*.jsonl"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def message_text(rec: dict) -> str:
    """把一則訊息的文字內容攤平成字串，供邊界比對。"""
    msg = rec.get("message")
    if not isinstance(msg, dict):
        return ""
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                # text block / tool_result 的文字
                if isinstance(block.get("text"), str):
                    parts.append(block["text"])
                elif isinstance(block.get("content"), str):
                    parts.append(block["content"])
    return "\n".join(parts)


def load_records(path: str) -> list[dict]:
    recs = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return recs


def find_index(recs: list[dict], needle: str, start: int = 0) -> int | None:
    for i in range(start, len(recs)):
        if needle in message_text(recs[i]):
            return i
    return None


def find_index_by_time(recs: list[dict], iso_ts: str, *, is_end: bool, start: int = 0) -> int | None:
    """找第一則 timestamp >= iso_ts 的紀錄（起點）；is_end 時找最後一則 <= iso_ts（終點）。

    ISO-8601 帶 Z 的字串可直接字典序比較，無須解析時區。"""
    if not is_end:
        for i in range(start, len(recs)):
            ts = recs[i].get("timestamp")
            if ts and ts >= iso_ts:
                return i
        return None
    last = None
    for i in range(start, len(recs)):
        ts = recs[i].get("timestamp")
        if ts and ts <= iso_ts:
            last = i
    return last


def is_human_turn(rec: dict) -> bool:
    """真人輸入的回合：type==user、有文字、且不是 tool_result。"""
    if rec.get("type") != "user":
        return False
    msg = rec.get("message")
    if not isinstance(msg, dict):
        return False
    content = msg.get("content")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                return False
    return bool(message_text(rec).strip())


def format_duration(start_ts: str | None, end_ts: str | None) -> str | None:
    if not start_ts or not end_ts:
        return None
    try:
        a = datetime.fromisoformat(start_ts.replace("Z", "+00:00"))
        b = datetime.fromisoformat(end_ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    secs = (b - a).total_seconds()
    if secs < 60:
        return f"{secs:.0f} 秒"
    if secs < 3600:
        return f"{secs / 60:.1f} 分鐘"
    return f"{secs / 3600:.1f} 小時"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--transcript", help="transcript JSONL 路徑；省略則自動抓當前專案最新 session")
    ap.add_argument("--from", dest="frm", help="區間起點（文字錨點）：出現在某則訊息裡的一段文字")
    ap.add_argument("--to", help="區間終點（文字錨點）：出現在某則訊息裡的一段文字")
    ap.add_argument("--from-time", dest="frm_time", help="區間起點（時間錨點）：ISO timestamp，如 2026-06-22T22:14:03.000Z")
    ap.add_argument("--to-time", dest="to_time", help="區間終點（時間錨點）：ISO timestamp")
    ap.add_argument("--cwd", default=os.getcwd(), help="用來推算 transcript 目錄的工作目錄（預設目前目錄）")
    args = ap.parse_args()

    path = args.transcript or detect_transcript(args.cwd)
    if not path or not os.path.exists(path):
        print(f"找不到 transcript（path={path}）。請用 --transcript 指定。", file=sys.stderr)
        return 1

    recs = load_records(path)
    if not recs:
        print("transcript 是空的或無法解析。", file=sys.stderr)
        return 1

    lo = 0
    if args.frm_time:
        idx = find_index_by_time(recs, args.frm_time, is_end=False)
        if idx is None:
            print(f"區間起點找不到（無 timestamp >= {args.frm_time}）", file=sys.stderr)
            return 1
        lo = idx
    elif args.frm:
        idx = find_index(recs, args.frm)
        if idx is None:
            print(f"區間起點找不到：{args.frm!r}", file=sys.stderr)
            return 1
        lo = idx

    hi = len(recs)
    if args.to_time:
        idx = find_index_by_time(recs, args.to_time, is_end=True, start=lo)
        if idx is None:
            print(f"區間終點找不到（無 timestamp <= {args.to_time} 在起點之後）", file=sys.stderr)
            return 1
        hi = idx + 1  # 含終點那則
    elif args.to:
        idx = find_index(recs, args.to, start=lo)
        if idx is None:
            print(f"區間終點找不到（在起點之後）：{args.to!r}", file=sys.stderr)
            return 1
        hi = idx + 1  # 含終點那則

    totals = {"input": 0, "cache_creation": 0, "cache_read": 0, "output": 0}
    assistant_turns = 0
    human_turns = 0
    ts_first = ts_last = None
    for rec in recs[lo:hi]:
        ts = rec.get("timestamp")
        if ts:
            ts_first = ts_first or ts
            ts_last = ts
        if is_human_turn(rec):
            human_turns += 1
            continue
        if rec.get("type") != "assistant":
            continue
        usage = (rec.get("message") or {}).get("usage")
        if not isinstance(usage, dict):
            continue
        assistant_turns += 1
        totals["input"] += usage.get("input_tokens", 0)
        totals["cache_creation"] += usage.get("cache_creation_input_tokens", 0)
        totals["cache_read"] += usage.get("cache_read_input_tokens", 0)
        totals["output"] += usage.get("output_tokens", 0)

    new_tokens = totals["input"] + totals["cache_creation"] + totals["output"]
    duration = format_duration(ts_first, ts_last)

    print(f"transcript : {path}")
    print(f"區間       : 第 {lo} ~ {hi - 1} 則")
    if ts_first:
        print(f"時間       : {ts_first} → {ts_last}")
    print("-" * 48)
    print(f"對話來回   : {human_turns} 個真人回合 / {assistant_turns} 個 AI 回合")
    print(f"花費時間   : {duration or 'n/a'}")
    print("-" * 48)
    print(f"input            : {totals['input']:>10,}")
    print(f"cache_creation   : {totals['cache_creation']:>10,}")
    print(f"cache_read       : {totals['cache_read']:>10,}  (最便宜)")
    print(f"output           : {totals['output']:>10,}")
    print(f"新增 token (約)  : {new_tokens:>10,}  = input + cache_creation + output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
