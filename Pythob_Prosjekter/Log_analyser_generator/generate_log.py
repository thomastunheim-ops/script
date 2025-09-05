import random
from datetime import datetime, timedelta

# ----- Config -----
TOTAL_LINES = 400
DOS_BURSTS = [
    # (start_offset_sec, duration_sec, rps, ip)
    (120, 30, 50, "185.199.110.153"),   # 50 req/s for 30s
    (300, 15, 100, "104.21.77.12"),     # 100 req/s for 15s (short, intense)
]
# You can add more bursts above

ips_normal = ["192.168.1.10", "192.168.1.11", "203.0.113.5", "198.51.100.42", "10.0.0.25"]
ips_attackers = ["45.33.32.156", "5.188.10.20", "103.21.244.0", "66.249.66.1"]

user_agents_normal = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
]
user_agents_susp = [
    "curl/7.68.0",
    "sqlmap/1.4",
    "python-requests/2.28.1",
    "nikto/2.1.6"
]

normal_paths = [
    "/", "/index.html", "/about", "/contact", "/products",
    "/images/logo.png", "/scripts/app.js", "/styles/main.css"
]

attack_paths = [
    "/wp-admin", "/wp-login.php", "/phpmyadmin", "/.git/config",
    "/etc/passwd", "/login.php?id=1'--", "/search.php?q=union+select+1,2,3",
    "/index.php?page=../../../../etc/passwd", "/cmd?exec=ls", "/?id=%24%7B7*7%7D"
]

statuses_normal = [200, 200, 200, 404, 403, 500]
statuses_attack = [200, 403, 404, 500]

# Base time for first line
start_time = datetime(2024, 10, 10, 13, 55, 36)

def fmt_line(ip, ts, path, status, size, ua):
    ts_str = ts.strftime("%d/%b/%Y:%H:%M:%S +0000")
    return f'{ip} - - [{ts_str}] "GET {path} HTTP/1.1" {status} {size} "-" "{ua}"\n'

def gen_background_traffic():
    """Generate background (normal + malicious) traffic ~TOTAL_LINES lines with ~1 req/sec cadence."""
    lines = []
    t = start_time
    for i in range(TOTAL_LINES):
        # 15% malicious
        if random.random() < 0.15:
            ip = random.choice(ips_attackers)
            path = random.choice(attack_paths)
            ua = random.choice(user_agents_susp + user_agents_normal)  # mix
            status = random.choice(statuses_attack)
        else:
            ip = random.choice(ips_normal)
            path = random.choice(normal_paths)
            ua = random.choice(user_agents_normal)
            status = random.choice(statuses_normal)

        size = random.randint(200, 5000)
        lines.append(fmt_line(ip, t, path, status, size, ua))

        # next second (base cadence)
        t += timedelta(seconds=1)
    return lines

def gen_burst_traffic():
    """Generate high-rate bursts (DoS-like)."""
    burst_lines = []
    for start_offset, duration, rps, ip in DOS_BURSTS:
        burst_start = start_time + timedelta(seconds=start_offset)
        # For each second in duration, create rps lines at that same second timestamp
        for sec in range(duration):
            ts = burst_start + timedelta(seconds=sec)
            for _ in range(rps):
                # simple mix of paths/status for bursts (often 200/404 spam)
                if random.random() < 0.2:
                    path = random.choice(attack_paths)
                    ua = random.choice(user_agents_susp)
                    status = random.choice([200, 404, 403])
                else:
                    path = random.choice(normal_paths)
                    ua = random.choice(user_agents_normal + user_agents_susp)
                    status = random.choice([200, 200, 404])
                size = random.randint(200, 4000)
                burst_lines.append(fmt_line(ip, ts, path, status, size, ua))
    return burst_lines

def main():
    bg = gen_background_traffic()
    bursts = gen_burst_traffic()

    # Combine and sort by timestamp (to look realistic)
    all_lines = bg + bursts

    # Parse timestamp out of each line for sort (quick-and-dirty)
    def parse_ts(line):
        # find between '[' and ']'
        i = line.find('[')
        j = line.find(']')
        ts = line[i+1:j]  # e.g., 10/Oct/2024:13:55:36 +0000
        # ignore timezone for sorting
        ts_core = ts.split(" ")[0]
        return datetime.strptime(ts_core, "%d/%b/%Y:%H:%M:%S")

    all_lines.sort(key=parse_ts)

    with open("sample.log", "w", encoding="utf-8") as f:
        f.writelines(all_lines)

    approx_total = len(all_lines)
    print(f"✅ Generated sample.log with ~{approx_total} lines (background + DoS bursts)")
    print("   Bursts included (start_offset sec, duration sec, rps, ip):")
    for b in DOS_BURSTS:
        print(f"   - {b}")

if __name__ == "__main__":
    main()
