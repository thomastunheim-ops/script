#!/usr/bin/env python3
"""
Log Analyzer with Threat Detection + HTML report (Jinja2 + Chart.js)
- Parses Apache/Nginx access logs (common/combined)
- Flags brute-force, scanning, SQLi/LFI/RCE patterns, high-rate IPs, suspicious UAs
- Outputs console summary, optional JSON, and HTML
"""

import re
import sys
import json
import argparse
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from urllib.parse import unquote
from pathlib import Path

# Try import Jinja2; we only need it if --html is used
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    JINJA2_AVAILABLE = True
except Exception:
    JINJA2_AVAILABLE = False

# ===== Apache/Nginx Combined Log Regex =====
LOG_RE = re.compile(
    r'(?P<ip>\S+) '
    r'\S+ \S+ '
    r'\[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+)(?: HTTP/\d\.\d)?" '
    r'(?P<status>\d{3}) (?P<size>\S+) '
    r'"(?P<ref>[^"]*)" "(?P<ua>[^"]*)"'
)

# ===== Threat Patterns =====
SENSITIVE_PATHS = [
    "/wp-login.php", "/wp-admin", "/xmlrpc.php", "/phpmyadmin", "/admin",
    "/.git", "/.env", "/server-status", "/actuator/health", "/login", "/etc/passwd"
]

SQLI_PATTERNS = [
    r"(?i)(\bor\b|\band\b)\s+1=1",
    r"(?i)union\s+select",
    r"(?i)information_schema",
    r"(?i)load_file\s*\(",
    r"(?i)sleep\s*\(",
    r"(?i)benchmark\s*\(",
    r"(?i)'--", r"(?i)\"--", r"(?i)';--", r"(?i)\";--"
]

LFI_RFI_PATTERNS = [
    r"(?i)\.\./\.\./", r"(?i)/etc/passwd", r"(?i)file:\/\/", r"(?i)php:\/\/",
    r"(?i)http(s)?:\/\/[^\s]+"
]

RCE_PATTERNS = [
    r"(?i)\b(?:cmd|exec|system|passthru|popen|proc_open)\b",
    r"(?i)\b(?:\$\{.*\})\b",
    r"(?i)wget\s+http", r"(?i)curl\s+http"
]

SUSPICIOUS_UA = [
    "sqlmap", "nikto", "nmap", "curl", "wget", "python-requests", "masscan", "dirbuster", "gobuster"
]

# ===== Defaults / Heuristics =====
DEFAULT_RATE_WINDOW_MIN = 1
DEFAULT_RATE_THRESHOLD = 100
DEFAULT_401_403_THRESHOLD = 10
DEFAULT_404_THRESHOLD = 30
DEFAULT_TOP = 10

# ===== Helpers =====
def parse_ts(ts_str: str) -> datetime:
    # Example: 10/Oct/2024:13:55:36 +0000
    return datetime.strptime(ts_str.split()[0], "%d/%b/%Y:%H:%M:%S")

def is_suspicious_ua(ua: str) -> bool:
    if not ua or ua == "-":
        return True
    ua_lower = ua.lower()
    return any(token in ua_lower for token in SUSPICIOUS_UA)

def path_contains_any(path: str, needles) -> bool:
    p = path.lower()
    return any(n.lower() in p for n in needles)

def matches_any(patterns, text: str) -> bool:
    for pat in patterns:
        if re.search(pat, text):
            return True
    return False

def read_lines_any_encoding(path):
    """Be forgiving with encoding (PowerShell may write UTF-16)."""
    for enc in ("utf-8", "utf-16", "utf-16le", "utf-16be", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
    with open(path, "rb") as f:
        return f.read().decode("latin-1", errors="ignore").splitlines()

# ===== Core Analyzer =====
class LogAnalyzer:
    def __init__(self, rate_window_min=DEFAULT_RATE_WINDOW_MIN, rate_threshold=DEFAULT_RATE_THRESHOLD,
                 fail_threshold=DEFAULT_401_403_THRESHOLD, notfound_threshold=DEFAULT_404_THRESHOLD):
        self.rate_window = timedelta(minutes=rate_window_min)
        self.rate_threshold = rate_threshold
        self.fail_threshold = fail_threshold
        self.notfound_threshold = notfound_threshold

        # Aggregates
        self.by_ip = defaultdict(list)
        self.count_status = Counter()
        self.count_by_ip = Counter()
        self.fail_by_ip = Counter()
        self.notfound_by_ip = Counter()
        self.suspicious_hits = []

        # Timeline per minute
        self.status_by_minute = defaultdict(Counter)

    def ingest_line(self, line: str, line_no: int):
        m = LOG_RE.search(line)
        if not m:
            return
        ip = m.group("ip")
        ts = parse_ts(m.group("ts"))
        method = m.group("method")
        raw_path = m.group("path")
        path = unquote(raw_path)
        status = int(m.group("status"))
        ua = m.group("ua") or "-"

        event = {"ip": ip, "ts": ts, "method": method, "path": path, "status": status, "ua": ua, "line": line_no}

        # Store
        self.by_ip[ip].append(event)
        self.count_status[status] += 1
        self.count_by_ip[ip] += 1
        if status in (401, 403):
            self.fail_by_ip[ip] += 1
        if status == 404:
            self.notfound_by_ip[ip] += 1

        # Rules
        reasons = []
        if path_contains_any(path, SENSITIVE_PATHS):
            reasons.append("Sensitive path probing")
        if matches_any(SQLI_PATTERNS, path):
            reasons.append("SQLi pattern")
        if matches_any(LFI_RFI_PATTERNS, path):
            reasons.append("LFI/RFI pattern")
        if matches_any(RCE_PATTERNS, path):
            reasons.append("RCE pattern")
        if is_suspicious_ua(ua):
            reasons.append("Suspicious/empty User-Agent")

        for r in reasons:
            self.suspicious_hits.append((ip, r, line_no, path))

        # Timeline aggregation (minute buckets)
        minute = ts.replace(second=0, microsecond=0)
        self.status_by_minute[minute][status] += 1

    def analyze_rates(self):
        bursting_ips = []
        for ip, events in self.by_ip.items():
            events_sorted = sorted(events, key=lambda e: e["ts"])
            start = 0
            for i, ev in enumerate(events_sorted):
                while events_sorted[start]["ts"] < ev["ts"] - self.rate_window:
                    start += 1
                window_count = i - start + 1
                if window_count >= self.rate_threshold:
                    bursting_ips.append(ip)
                    break
        return list(sorted(set(bursting_ips)))

    def summarize(self):
        # Major suspects
        brute_force_ips = [ip for ip, c in self.fail_by_ip.items() if c >= self.fail_threshold]
        scanner_ips = [ip for ip, c in self.notfound_by_ip.items() if c >= self.notfound_threshold]
        burst_ips = self.analyze_rates()

        # Rank by total hits
        top_talkers = self.count_by_ip.most_common()

        # Group suspicious hits by IP
        susp_by_ip = defaultdict(list)
        for ip, reason, line_no, path in self.suspicious_hits:
            susp_by_ip[ip].append({"reason": reason, "line": line_no, "path": path})

        # Timeline prep
        all_minutes = sorted(self.status_by_minute.keys())
        status_codes = sorted({s for cnt in self.status_by_minute.values() for s in cnt.keys()})
        labels = [m.strftime("%Y-%m-%d %H:%M") for m in all_minutes]
        series = {str(s): [self.status_by_minute[m].get(s, 0) for m in all_minutes] for s in status_codes}

        return {
            "status_counts": dict(self.count_status),
            "top_talkers": top_talkers,
            "brute_force_ips": brute_force_ips,
            "scanner_ips": scanner_ips,
            "burst_ips": burst_ips,
            "suspicious_hits": {ip: rows for ip, rows in susp_by_ip.items()},
            "timeline": {"labels": labels, "series": series}
        }

def print_console(report, top=DEFAULT_TOP):
    print("\n=== LOG ANALYZER SUMMARY ===")
    print("HTTP Status Counts:")
    for code, cnt in sorted(report["status_counts"].items()):
        print(f"  {code}: {cnt}")

    print("\nTop Talkers:")
    for ip, cnt in report["top_talkers"][:top]:
        print(f"  {ip:<16} {cnt}")

    def print_group(name, ips):
        print(f"\n{name}:")
        if not ips:
            print("  (none)")
        else:
            for ip in ips:
                print(f"  {ip}")

    print_group("Brute-force suspects (many 401/403)", report["brute_force_ips"])
    print_group("Scanner suspects (many 404)", report["scanner_ips"])
    print_group("High-rate suspects (bursting window)", report["burst_ips"])

    print("\nSuspicious Hits (grouped):")
    if not report["suspicious_hits"]:
        print("  (none)")
    else:
        for ip, rows in report["suspicious_hits"].items():
            print(f"  {ip}:")
            for r in rows[:DEFAULT_TOP]:
                print(f"    - {r['reason']} | line {r['line']} | {r['path']}")
            if len(rows) > DEFAULT_TOP:
                print(f"    ... and {len(rows)-DEFAULT_TOP} more")

def save_json(report, path="report.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nJSON report saved to: {path}")

def render_html(report, html_out: str, template_path: str):
    if not JINJA2_AVAILABLE:
        print("Error: Jinja2 is not installed. Install with: pip install jinja2 markupsafe")
        sys.exit(2)
    template_file = Path(template_path)
    if not template_file.exists():
        print(f"Error: Template not found: {template_file}")
        sys.exit(2)

    env = Environment(
        loader=FileSystemLoader(str(template_file.parent)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template_file.name)

    # Build chart-ready data and pre-serialize to JSON
    top_ips = report["top_talkers"][:10]
    top_ips_labels = [ip for ip, _ in top_ips]
    top_ips_values = [cnt for _, cnt in top_ips]

    status_labels = [str(k) for k in sorted(report["status_counts"].keys())]
    status_values = [report["status_counts"][int(k)] if isinstance(k, str) else report["status_counts"][k] for k in sorted(report["status_counts"].keys())]

    context = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_ips_labels_json": json.dumps(top_ips_labels),
        "top_ips_values_json": json.dumps(top_ips_values),
        "status_labels_json": json.dumps(status_labels),
        "status_values_json": json.dumps(status_values),
        "timeline_labels_json": json.dumps(report["timeline"]["labels"]),
        "timeline_series_json": json.dumps(report["timeline"]["series"]),
        "brute_force_ips": report["brute_force_ips"],
        "scanner_ips": report["scanner_ips"],
        "burst_ips": report["burst_ips"],
        "suspicious_hits": report["suspicious_hits"],
    }

    html = template.render(**context)
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML report saved to: {html_out}")

def main():
    ap = argparse.ArgumentParser(description="Analyze web server logs, flag threats, and optionally render HTML report.")
    ap.add_argument("-i", "--input", required=True, help="Path to access log file")
    ap.add_argument("--top", type=int, default=DEFAULT_TOP, help="How many items to show in top lists (console) (default 10)")
    ap.add_argument("--window", type=int, default=DEFAULT_RATE_WINDOW_MIN, help="Rate window minutes (default 1)")
    ap.add_argument("--rate-threshold", type=int, default=DEFAULT_RATE_THRESHOLD, help="Requests per window threshold (default 100)")
    ap.add_argument("--fail-threshold", type=int, default=DEFAULT_401_403_THRESHOLD, help="401/403 threshold per IP (default 10)")
    ap.add_argument("--nf-threshold", type=int, default=DEFAULT_404_THRESHOLD, help="404 threshold per IP (default 30)")
    ap.add_argument("--json", dest="json_out", help="Write JSON report to given filepath (e.g., report.json)")
    ap.add_argument("--html", dest="html_out", help="Write HTML report to given filepath (e.g., report.html)")
    ap.add_argument("--template", default="report_template.html", help="Jinja2 HTML template path (default: report_template.html)")
    args = ap.parse_args()

    analyzer = LogAnalyzer(
        rate_window_min=args.window,
        rate_threshold=args.rate_threshold,
        fail_threshold=args.fail_threshold,
        notfound_threshold=args.nf_threshold
    )

    lines = read_lines_any_encoding(args.input)
    for idx, line in enumerate(lines, start=1):
        analyzer.ingest_line(line, idx)

    report = analyzer.summarize()
    print_console(report, top=args.top)

    if args.json_out:
        save_json(report, path=args.json_out)

    if args.html_out:
        render_html(report, html_out=args.html_out, template_path=args.template)

if __name__ == "__main__":
    main()
