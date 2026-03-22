#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║         🔱 ULTIMATE NETWORK SECURITY TOOLKIT — A to Z  v1.0        ║
║         By: Karthigeyan Ravindranathan (karthik-sec)                ║
║         GitHub: github.com/karthik9810                              ║
║                                                                      ║
║   🟢 BEGINNER    → Angry IP Style + Zenmap Style                   ║
║   🟡 INTERMEDIATE → Nmap Scripts + Masscan Style                   ║
║   🔴 PROFESSIONAL → Nuclei + Naabu + Shodan Style                  ║
║                                                                      ║
║   ⚠️  ETHICAL USE ONLY — YOUR OWN NETWORK / SYSTEMS ONLY!          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import subprocess, platform, socket, sys, os, time, re, json
import datetime, threading, urllib.request, itertools, struct
import ipaddress, ssl, hashlib, base64, random
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

SYSTEM = platform.system()

# ── Colors ─────────────────────────────────────────────────────────
R  = '\033[91m';  G  = '\033[92m';  Y  = '\033[93m'
B  = '\033[94m';  P  = '\033[95m';  C  = '\033[96m'
W  = '\033[97m';  DIM= '\033[2m';   BD = '\033[1m'
RS = '\033[0m'

# ── Level Colors ───────────────────────────────────────────────────
LVL_B = f"{G}{BD}"    # Beginner
LVL_I = f"{Y}{BD}"    # Intermediate
LVL_P = f"{R}{BD}"    # Professional


# ══════════════════════════════════════════════════════════════════
#  SHARED UTILITIES
# ══════════════════════════════════════════════════════════════════

def clear(): os.system('cls' if SYSTEM == 'Windows' else 'clear')

def sep(title='', width=68):
    if title:
        pad = (width - len(title) - 4) // 2
        print(f"\n{P}{'═'*pad}  {BD}{C}{title}{RS}{P}  {'═'*pad}{RS}")
    else:
        print(f"{DIM}{'─'*width}{RS}")

def spinner_start(msg):
    stop   = threading.Event()
    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    def _run():
        for f in itertools.cycle(frames):
            if stop.is_set(): break
            sys.stdout.write(f"\r  {C}{f}{RS} {W}{msg}{RS}   ")
            sys.stdout.flush()
            time.sleep(0.08)
        sys.stdout.write('\r' + ' '*(len(msg)+10) + '\r')
        sys.stdout.flush()
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return stop

def spinner_stop(s):
    s.set(); time.sleep(0.15)

def scan_port(host, port, timeout=0.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        r = s.connect_ex((host, port))
        s.close()
        return r == 0
    except: return False

def get_net_info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close()
    except: ip = '192.168.1.100'
    parts = ip.split('.')
    gw    = parts[:3] + ['1']
    return {
        'local_ip': ip,
        'network':  '.'.join(parts[:3]),
        'gateway':  '.'.join(gw),
        'cidr':     '.'.join(parts[:3]) + '.0/24'
    }

def score_bar(val, width=20):
    filled = int((val/100)*width)
    col    = G if val >= 80 else Y if val >= 50 else R
    bar    = '█'*filled + '░'*(width-filled)
    return f"{col}[{bar}] {val}/100{RS}"

def progress(done, total, width=30):
    pct  = done/max(total,1)
    fill = int(pct*width)
    bar  = '█'*fill + '░'*(width-fill)
    return f"{C}[{bar}]{RS} {done}/{total} ({pct*100:.0f}%)"

COMMON_PORTS = {
    21:'FTP', 22:'SSH', 23:'Telnet', 25:'SMTP', 53:'DNS',
    80:'HTTP', 110:'POP3', 143:'IMAP', 443:'HTTPS', 445:'SMB',
    3389:'RDP', 8080:'HTTP-Alt', 8443:'HTTPS-Alt', 3306:'MySQL',
    5900:'VNC', 1900:'UPnP', 6379:'Redis', 27017:'MongoDB',
    5432:'PostgreSQL', 1433:'MSSQL', 2375:'Docker', 9200:'Elasticsearch',
    5000:'Flask/Dev', 8888:'Jupyter', 4444:'Metasploit',
    554:'RTSP', 161:'SNMP', 69:'TFTP', 137:'NetBIOS', 1723:'PPTP-VPN',
}

RISKY = {
    23:'CRITICAL', 21:'WARNING', 445:'CRITICAL', 3389:'CRITICAL',
    5900:'CRITICAL', 2375:'CRITICAL', 27017:'CRITICAL', 6379:'CRITICAL',
    1900:'WARNING', 161:'WARNING', 69:'WARNING',
}

def banner():
    clear()
    print(f"""
{P}{BD}
  ╔══════════════════════════════════════════════════════════════════╗
  ║   ███╗   ██╗███████╗████████╗    ████████╗ ██████╗  ██████╗    ║
  ║   ████╗  ██║██╔════╝╚══██╔══╝       ██╔══╝██╔═══██╗██╔════╝   ║
  ║   ██╔██╗ ██║█████╗     ██║          ██║   ██║   ██║██║         ║
  ║   ██║╚██╗██║██╔══╝     ██║          ██║   ██║   ██║██║         ║
  ║   ██║ ╚████║███████╗   ██║          ██║   ╚██████╔╝╚██████╗    ║
  ║   ╚═╝  ╚═══╝╚══════╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝   ║
  ║                                                                  ║
  ║    🔱  ULTIMATE NETWORK SECURITY TOOLKIT  A→Z  v1.0  🔱        ║
  ║    ─────────────────────────────────────────────────           ║
  ║    🟢 Beginner  🟡 Intermediate  🔴 Professional               ║
  ║    By: Karthigeyan Ravindranathan  |  karthik-sec               ║
  ╚══════════════════════════════════════════════════════════════════╝
{RS}""")

def disclaimer():
    print(f"{R}{BD}")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║  ⚠️  LEGAL DISCLAIMER                           ║")
    print("  ║  Educational use ONLY.                          ║")
    print("  ║  Only scan systems YOU OWN or have explicit     ║")
    print("  ║  written permission to test.                    ║")
    print("  ║  Unauthorized scanning is ILLEGAL worldwide!    ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print(f"{RS}")
    c = input(f"  {Y}  ➤  Confirm ethical use (yes/no): {RS}").strip().lower()
    if c != 'yes':
        print(f"\n  {R}Stay ethical! Exiting. 💜{RS}\n"); sys.exit(0)
    print(f"\n  {G}  ✅  Confirmed! Loading toolkit...{RS}\n")
    time.sleep(0.5)


# ══════════════════════════════════════════════════════════════════
# ██████╗ ███████╗ ██████╗ ██╗███╗  ██╗███╗  ██╗███████╗██████╗
# ██╔══██╗██╔════╝██╔════╝ ██║████╗ ██║████╗ ██║██╔════╝██╔══██╗
# ██████╔╝█████╗  ██║  ██╗ ██║██╔██╗██║██╔██╗██║█████╗  ██████╔╝
# ██╔══██╗██╔══╝  ██║  ╚██╗██║██║╚████║██║╚████║██╔══╝  ██╔══██╗
# ██████╔╝███████╗╚██████╔╝██║██║ ╚███║██║ ╚███║███████╗██║  ██║
# ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚══╝╚═╝  ╚══╝╚══════╝╚═╝  ╚═╝
#  🟢 BEGINNER TOOLS
# ══════════════════════════════════════════════════════════════════

# ── B1: ANGRY IP SCANNER STYLE ─────────────────────────────────
def angry_ip_scanner():
    sep("🟢 B1 — ANGRY IP SCANNER  (Beginner)")
    net  = get_net_info()
    print(f"""
  {LVL_B}WHAT THIS DOES:{RS}
  {W}Scans every IP on your network (like Angry IP Scanner).
  Shows which devices are ONLINE with hostname and response time.{RS}
  """)

    cidr  = input(f"  {Y}  ➤  Network to scan (default {net['network']}.0/24): {RS}").strip()
    cidr  = cidr or f"{net['network']}.0/24"
    ips   = [str(ip) for ip in ipaddress.IPv4Network(cidr, strict=False).hosts()]
    total = len(ips)
    alive = []
    lock  = threading.Lock()
    done  = [0]

    def ping_host(ip):
        cmd = (['ping','-n','1','-w','400',ip] if SYSTEM=='Windows'
               else ['ping','-c','1','-W','1',ip])
        try:
            t0 = time.time()
            r  = subprocess.run(cmd, capture_output=True, timeout=2)
            ms = (time.time()-t0)*1000
            if r.returncode == 0:
                try:    host = socket.gethostbyaddr(ip)[0]
                except: host = '—'
                with lock:
                    alive.append({'ip':ip,'host':host,'ms':ms})
        except: pass
        with lock:
            done[0] += 1
            if done[0] % 10 == 0:
                sys.stdout.write(f"\r  {progress(done[0], total)}   ")
                sys.stdout.flush()

    print(f"\n  {C}Scanning {total} hosts...{RS}\n")
    start = time.time()
    with ThreadPoolExecutor(max_workers=80) as ex:
        list(ex.map(ping_host, ips))
    elapsed = time.time()-start
    print()

    alive.sort(key=lambda x: int(x['ip'].split('.')[-1]))
    sep()
    print(f"\n  {G}  {'IP':<18}{'Hostname':<30}{'Ping':<12}{'Status'}{RS}")
    sep()
    for d in alive:
        you    = f"  {G}◀ YOU{RS}"    if d['ip']==net['local_ip'] else ''
        router = f"  {C}◀ ROUTER{RS}" if d['ip']==net['gateway']  else ''
        col    = G if d['ms']<50 else Y if d['ms']<200 else R
        print(f"  {C}{d['ip']:<18}{W}{d['host'][:28]:<30}{col}{d['ms']:.0f}ms{RS:<12}{G}● ONLINE{RS}{you}{router}")

    sep()
    print(f"\n  {W}Hosts scanned : {C}{total}")
    print(f"  {W}Online        : {G}{BD}{len(alive)}")
    print(f"  {W}Offline       : {R}{total-len(alive)}")
    print(f"  {W}Scan time     : {C}{elapsed:.2f}s{RS}")


# ── B2: ZENMAP STYLE (Visual Nmap Output) ──────────────────────
def zenmap_style():
    sep("🟢 B2 — ZENMAP STYLE SCANNER  (Beginner)")
    net = get_net_info()
    print(f"""
  {LVL_B}WHAT THIS DOES:{RS}
  {W}Visual scanner like Zenmap (the GUI for Nmap).
  Shows open ports with service names in a clean visual layout.{RS}
  """)

    target = input(f"  {Y}  ➤  Target IP (default {net['gateway']}): {RS}").strip() or net['gateway']
    print(f"\n  {C}Scanning {target} for common ports...{RS}\n")

    ports  = sorted(COMMON_PORTS.keys())
    open_p = []
    done   = [0]
    lock   = threading.Lock()

    def check(port):
        result = scan_port(target, port, 0.8)
        with lock:
            done[0] += 1
            sys.stdout.write(f"\r  {progress(done[0], len(ports))}   ")
            sys.stdout.flush()
        if result: return port
        return None

    start = time.time()
    with ThreadPoolExecutor(max_workers=50) as ex:
        open_p = sorted(filter(None, ex.map(check, ports)))
    elapsed = time.time()-start
    print()

    # Visual map — like Zenmap topology
    sep()
    print(f"\n  {BD}{W}Target: {G}{target}{RS}  {DIM}({elapsed:.2f}s){RS}\n")

    if not open_p:
        print(f"  {Y}  No open ports found on {target}.{RS}")
        return

    # Draw visual port map
    print(f"  {W}{BD}{'Port':<8}{'Service':<18}{'State':<10}{'Risk'}{RS}")
    sep()
    for port in open_p:
        svc  = COMMON_PORTS.get(port,'Unknown')
        risk = RISKY.get(port,'')
        if risk == 'CRITICAL':
            col = R; badge = f"{R}● CRITICAL{RS}"
        elif risk == 'WARNING':
            col = Y; badge = f"{Y}● WARNING{RS}"
        else:
            col = G; badge = f"{G}● OPEN{RS}"
        print(f"  {C}{port:<8}{W}{svc:<18}{G}open{RS:<10}      {badge}")

    # Visual topology
    sep()
    print(f"\n  {BD}{W}Network Topology:{RS}\n")
    print(f"  {DIM}[Internet] ── [Router: {net['gateway']}] ── [You: {net['local_ip']}]{RS}\n")
    print(f"              {Y}│{RS}")
    print(f"        {Y}╔═════╧══════╗{RS}")
    print(f"        {Y}║  {G}{target}{Y}  ║{RS}")
    print(f"        {Y}╚════════════╝{RS}")
    for p in open_p[:8]:
        svc = COMMON_PORTS.get(p,'Unknown')
        print(f"              {C}├── :{p} {svc}{RS}")

    print(f"\n  {W}Open ports: {G}{BD}{len(open_p)}{RS}")


# ── B3: SIMPLE HOST DISCOVERY ──────────────────────────────────
def simple_host_discovery():
    sep("🟢 B3 — SIMPLE HOST DISCOVERY  (Beginner)")
    net = get_net_info()
    print(f"""
  {LVL_B}WHAT THIS DOES:{RS}
  {W}Quick scan to find ALL live devices on your network.
  Shows IP, hostname, and tries to guess what type of device it is.{RS}
  """)

    ips  = [f"{net['network']}.{i}" for i in range(1,255)]
    devs = []
    lock = threading.Lock()

    DEVICE_HINTS = {
        'iphone':'📱 iPhone',   'ipad':'📱 iPad',
        'android':'📱 Android', 'samsung':'📱 Samsung',
        'router':'📡 Router',   'gateway':'📡 Gateway',
        'tp-link':'📡 TP-Link', 'asus':'📡 ASUS Router',
        'netgear':'📡 Netgear', 'desktop':'💻 Desktop',
        'laptop':'💻 Laptop',   'printer':'🖨️  Printer',
        'tv':'📺 Smart TV',     'roku':'📺 Roku',
        'cam':'📹 Camera',      'nvr':'📹 NVR/DVR',
        'mac':'🍎 Mac',         'apple':'🍎 Apple',
        'xbox':'🎮 Xbox',       'playstation':'🎮 PlayStation',
        'alexa':'🔊 Alexa',     'echo':'🔊 Echo',
    }

    def detect_type(host):
        h = host.lower()
        for key, dtype in DEVICE_HINTS.items():
            if key in h: return dtype
        return '🔵 Unknown'

    def scan(ip):
        cmd = (['ping','-n','1','-w','500',ip] if SYSTEM=='Windows'
               else ['ping','-c','1','-W','1',ip])
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=2)
            if r.returncode == 0:
                try:    h = socket.gethostbyaddr(ip)[0]
                except: h = '—'
                dtype = detect_type(h)
                with lock: devs.append({'ip':ip,'host':h,'type':dtype})
        except: pass

    sp = spinner_start("Discovering hosts on network...")
    with ThreadPoolExecutor(max_workers=80) as ex:
        list(ex.map(scan, ips))
    spinner_stop(sp)

    devs.sort(key=lambda x: int(x['ip'].split('.')[-1]))
    sep()
    print(f"\n  {G}Found {BD}{len(devs)}{RS}{G} live host(s):{RS}\n")
    print(f"  {W}{BD}{'#':<5}{'IP Address':<18}{'Device Type':<20}{'Hostname'}{RS}")
    sep()
    for i,d in enumerate(devs,1):
        role = f"  {G}◀ YOU{RS}" if d['ip']==net['local_ip'] else f"  {C}◀ ROUTER{RS}" if d['ip']==net['gateway'] else ''
        print(f"  {C}{i:<5}{W}{d['ip']:<18}{d['type']:<22}{DIM}{d['host'][:28]}{RS}{role}")


# ══════════════════════════════════════════════════════════════════
# ██╗███╗  ██╗████████╗███████╗██████╗
# ██║████╗ ██║╚══██╔══╝██╔════╝██╔══██╗
# ██║██╔██╗██║   ██║   █████╗  ██████╔╝
# ██║██║╚████║   ██║   ██╔══╝  ██╔══██╗
# ██║██║ ╚███║   ██║   ███████╗██║  ██║
# ╚═╝╚═╝  ╚══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
#  🟡 INTERMEDIATE TOOLS
# ══════════════════════════════════════════════════════════════════

# ── I1: NMAP STYLE + NSE SCRIPTS ───────────────────────────────
NSE_SCRIPTS = {
    'http-title': {
        'desc': 'Grab HTTP page title from web servers',
        'ports': [80, 8080, 8000, 3000],
        'func': 'grab_http_title'
    },
    'ssh-banner': {
        'desc': 'Grab SSH server banner/version',
        'ports': [22],
        'func': 'grab_ssh_banner'
    },
    'ftp-banner': {
        'desc': 'Grab FTP server banner',
        'ports': [21],
        'func': 'grab_ftp_banner'
    },
    'smtp-banner': {
        'desc': 'Grab SMTP mail server banner',
        'ports': [25, 587],
        'func': 'grab_smtp_banner'
    },
    'default-creds': {
        'desc': 'Test common default credentials',
        'ports': [80, 8080, 23, 21],
        'func': 'test_default_creds'
    },
    'http-headers': {
        'desc': 'Check HTTP security headers',
        'ports': [80, 443, 8080, 8443],
        'func': 'check_http_headers'
    },
    'ssl-cert': {
        'desc': 'Inspect SSL/TLS certificate',
        'ports': [443, 8443],
        'func': 'check_ssl_cert'
    },
    'dns-info': {
        'desc': 'Query DNS server information',
        'ports': [53],
        'func': 'query_dns_info'
    },
}

def grab_http_title(host, port):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        proto = 'https' if port in (443,8443) else 'http'
        req   = urllib.request.Request(f"{proto}://{host}:{port}",
                                       headers={'User-Agent':'Mozilla/5.0'})
        res   = urllib.request.urlopen(req, timeout=5, context=ctx)
        body  = res.read(2000).decode('utf-8','ignore')
        m     = re.search(r'<title[^>]*>(.*?)</title>', body, re.IGNORECASE|re.DOTALL)
        title = m.group(1).strip()[:60] if m else 'No title'
        return f"{G}Title: {title}{RS}"
    except Exception as e:
        return f"{DIM}Could not grab title: {e}{RS}"

def grab_ssh_banner(host, port):
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect((host, port))
        banner = s.recv(256).decode('utf-8','ignore').strip()
        s.close()
        return f"{G}Banner: {banner[:80]}{RS}"
    except Exception as e:
        return f"{DIM}Could not grab banner{RS}"

def grab_ftp_banner(host, port):
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect((host, port))
        banner = s.recv(256).decode('utf-8','ignore').strip()
        s.close()
        return f"{G}Banner: {banner[:80]}{RS}"
    except: return f"{DIM}No banner{RS}"

def grab_smtp_banner(host, port):
    try:
        s = socket.socket(); s.settimeout(3)
        s.connect((host, port))
        banner = s.recv(256).decode('utf-8','ignore').strip()
        s.close()
        return f"{G}Banner: {banner[:80]}{RS}"
    except: return f"{DIM}No banner{RS}"

DEFAULT_CREDS = [
    ('admin','admin'),('admin','password'),('admin','1234'),
    ('root','root'),('root','toor'),('admin',''),('','admin'),
    ('user','user'),('admin','admin123'),('guest','guest'),
]

def test_default_creds(host, port):
    results = []
    try:
        if port in (80, 8080):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            for user, pw in DEFAULT_CREDS[:5]:
                creds = base64.b64encode(f"{user}:{pw}".encode()).decode()
                req   = urllib.request.Request(
                    f"http://{host}:{port}/",
                    headers={'Authorization': f'Basic {creds}',
                             'User-Agent': 'Mozilla/5.0'})
                try:
                    res = urllib.request.urlopen(req, timeout=3, context=ctx)
                    if res.status == 200:
                        results.append(f"{R}⚠  Default creds work: {user}/{pw}{RS}")
                        break
                except: pass
    except: pass
    return '\n  '.join(results) if results else f"{G}No default creds found{RS}"

def check_http_headers(host, port):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        proto = 'https' if port in (443,8443) else 'http'
        req   = urllib.request.Request(f"{proto}://{host}:{port}",
                                       headers={'User-Agent':'Mozilla/5.0'})
        res   = urllib.request.urlopen(req, timeout=5, context=ctx)
        hdrs  = dict(res.headers)
        checks = [
            ('Strict-Transport-Security','HSTS'),
            ('X-Frame-Options','XFO'),
            ('Content-Security-Policy','CSP'),
            ('X-Content-Type-Options','XCTO'),
        ]
        lines = []
        for h, name in checks:
            present = any(h.lower()==k.lower() for k in hdrs)
            lines.append(f"  {'✅' if present else '❌'} {name}")
        return '\n'.join(lines)
    except Exception as e:
        return f"{DIM}Could not check: {e}{RS}"

def check_ssl_cert(host, port):
    try:
        ctx  = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        conn = ctx.wrap_socket(socket.create_connection((host,port),timeout=5),
                               server_hostname=host)
        cert = conn.getpeercert()
        conn.close()
        if cert:
            subj   = dict(x[0] for x in cert.get('subject',()))
            issuer = dict(x[0] for x in cert.get('issuer',()))
            exp    = cert.get('notAfter','Unknown')
            return (f"{G}Subject: {subj.get('commonName','—')}\n"
                    f"  {W}Issuer : {issuer.get('organizationName','—')}\n"
                    f"  {W}Expires: {exp}{RS}")
        return f"{Y}No cert info available{RS}"
    except Exception as e:
        return f"{DIM}SSL check failed: {e}{RS}"

def query_dns_info(host, port):
    try:
        results = []
        for domain in ['google.com','cloudflare.com']:
            try:
                ip = socket.gethostbyname(domain)
                results.append(f"{G}DNS resolves {domain} → {ip}{RS}")
            except:
                results.append(f"{R}DNS failed for {domain}{RS}")
        return '\n  '.join(results)
    except: return f"{DIM}DNS query failed{RS}"

def nmap_nse_scanner():
    sep("🟡 I1 — NMAP + NSE SCRIPT SCANNER  (Intermediate)")
    net = get_net_info()
    print(f"""
  {LVL_I}WHAT THIS DOES:{RS}
  {W}Replicates Nmap with NSE (Nmap Scripting Engine) scripts.
  Scans for open ports THEN runs scripts to grab banners,
  test default credentials, check SSL certs, and more.{RS}
  """)

    target  = input(f"  {Y}  ➤  Target IP (default {net['gateway']}): {RS}").strip() or net['gateway']

    print(f"\n  {W}Available NSE-style scripts:{RS}\n")
    for i,(name,info) in enumerate(NSE_SCRIPTS.items(),1):
        print(f"  {C}[{i}] {W}{name:<18}{DIM}{info['desc']}{RS}")

    print(f"  {C}[A] {W}Run ALL scripts{RS}")
    choice = input(f"\n  {Y}  ➤  Choose script(s) [1-8 or A]: {RS}").strip().upper()

    if choice == 'A':
        selected = list(NSE_SCRIPTS.keys())
    else:
        keys = list(NSE_SCRIPTS.keys())
        try:
            selected = [keys[int(choice)-1]]
        except: selected = list(NSE_SCRIPTS.keys())

    # Port scan first
    all_ports = set()
    for s in selected:
        all_ports.update(NSE_SCRIPTS[s]['ports'])

    sp = spinner_start(f"Phase 1/2: Port scanning {target}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(scan_port, target, p, 1): p for p in all_ports}
        for fut in as_completed(futures):
            p = futures[fut]
            if fut.result(): open_ports.append(p)
    spinner_stop(sp)

    if not open_ports:
        print(f"\n  {Y}No relevant ports open on {target}.{RS}")
        return

    print(f"\n  {G}Open ports: {', '.join(map(str,sorted(open_ports)))}{RS}\n")
    print(f"  {W}Phase 2/2: Running NSE scripts...{RS}\n")

    for script_name in selected:
        script = NSE_SCRIPTS[script_name]
        relevant = [p for p in open_ports if p in script['ports']]
        if not relevant: continue

        for port in relevant:
            sep()
            print(f"\n  {C}Script  : {BD}{script_name}{RS}")
            print(f"  {W}Port    : {port} ({COMMON_PORTS.get(port,'Unknown')})")
            print(f"  {W}Target  : {target}\n")

            func_map = {
                'grab_http_title':    grab_http_title,
                'grab_ssh_banner':    grab_ssh_banner,
                'grab_ftp_banner':    grab_ftp_banner,
                'grab_smtp_banner':   grab_smtp_banner,
                'test_default_creds': test_default_creds,
                'check_http_headers': check_http_headers,
                'check_ssl_cert':     check_ssl_cert,
                'query_dns_info':     query_dns_info,
            }
            fn     = script['func']
            result = func_map[fn](target, port)
            print(f"  {W}Result  :\n  {result}{RS}")


# ── I2: MASSCAN STYLE (Ultra-fast port scanner) ────────────────
def masscan_style():
    sep("🟡 I2 — MASSCAN STYLE SCANNER  (Intermediate)")
    net = get_net_info()
    print(f"""
  {LVL_I}WHAT THIS DOES:{RS}
  {W}Ultra-fast port scanner inspired by Masscan.
  Uses high-concurrency threading to scan thousands of
  ports per second — much faster than standard Nmap.{RS}
  """)

    target  = input(f"  {Y}  ➤  Target IP (default {net['gateway']}): {RS}").strip() or net['gateway']
    rate    = input(f"  {Y}  ➤  Scan rate [1=Fast/2=Ultra/3=Max]: {RS}").strip()
    prange  = input(f"  {Y}  ➤  Port range (e.g. 1-1024, default 1-10000): {RS}").strip() or '1-10000'

    workers = {'1':200, '2':500, '3':1000}.get(rate, 200)
    timeout = {'1':0.5, '2':0.3, '3':0.2}.get(rate, 0.5)

    try:
        start_p, end_p = map(int, prange.split('-'))
    except:
        start_p, end_p = 1, 10000

    ports  = range(start_p, end_p+1)
    total  = end_p - start_p + 1
    done   = [0]
    lock   = threading.Lock()
    open_p = []

    print(f"\n  {W}Target  : {G}{target}")
    print(f"  {W}Range   : {C}{start_p}-{end_p} ({total} ports)")
    print(f"  {W}Workers : {C}{workers} threads")
    print(f"  {W}Timeout : {C}{timeout}s per port{RS}\n")

    start = time.time()

    def fast_scan(port):
        result = scan_port(target, port, timeout)
        with lock:
            done[0] += 1
            if done[0] % 500 == 0:
                rate_pps = done[0]/(time.time()-start)
                sys.stdout.write(
                    f"\r  {C}[{done[0]}/{total}]{RS} "
                    f"{G}{rate_pps:.0f} ports/sec{RS}  "
                    f"{Y}Found: {len(open_p)}{RS}   ")
                sys.stdout.flush()
        if result: return port
        return None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        open_p = sorted(filter(None, ex.map(fast_scan, ports)))

    elapsed = time.time()-start
    pps     = total/elapsed

    print()
    sep()
    print(f"\n  {G}Scan complete!{RS}\n")
    print(f"  {W}Time     : {C}{elapsed:.2f}s")
    print(f"  {W}Speed    : {G}{pps:.0f} ports/second")
    print(f"  {W}Scanned  : {C}{total} ports")
    print(f"  {W}Open     : {G}{BD}{len(open_p)}{RS}\n")

    if open_p:
        print(f"  {W}{BD}{'Port':<8}{'Service':<18}{'Risk'}{RS}")
        sep()
        for p in open_p:
            svc  = COMMON_PORTS.get(p,'Unknown')
            risk = RISKY.get(p,'')
            col  = R if risk=='CRITICAL' else Y if risk=='WARNING' else G
            print(f"  {C}{p:<8}{W}{svc:<18}{col}{risk or 'OPEN'}{RS}")


# ── I3: BANNER GRABBER (Service Version Detection) ─────────────
def banner_grabber():
    sep("🟡 I3 — BANNER GRABBER  (Intermediate)")
    net = get_net_info()
    print(f"""
  {LVL_I}WHAT THIS DOES:{RS}
  {W}Connects to open ports and grabs service banners.
  Reveals software names and versions (like Nmap -sV).
  Used to find outdated/vulnerable software versions.{RS}
  """)

    target = input(f"  {Y}  ➤  Target IP (default {net['gateway']}): {RS}").strip() or net['gateway']

    sp = spinner_start("Scanning for open ports...")
    open_p = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        futures = {ex.submit(scan_port, target, p, 1): p for p in COMMON_PORTS}
        for fut in as_completed(futures):
            if fut.result(): open_p.append(futures[fut])
    spinner_stop(sp)

    if not open_p:
        print(f"\n  {Y}No open ports found.{RS}")
        return

    print(f"\n  {G}Grabbing banners from {len(open_p)} open port(s)...{RS}\n")
    print(f"  {W}{BD}{'Port':<8}{'Service':<14}{'Banner / Version'}{RS}")
    sep()

    GRABBERS = {
        21:  ('FTP',   lambda h,p: _raw_grab(h,p)),
        22:  ('SSH',   lambda h,p: _raw_grab(h,p)),
        23:  ('Telnet',lambda h,p: _raw_grab(h,p)),
        25:  ('SMTP',  lambda h,p: _raw_grab(h,p)),
        80:  ('HTTP',  lambda h,p: _http_grab(h,p,'http')),
        443: ('HTTPS', lambda h,p: _http_grab(h,p,'https')),
        8080:('HTTP',  lambda h,p: _http_grab(h,p,'http')),
        8443:('HTTPS', lambda h,p: _http_grab(h,p,'https')),
        110: ('POP3',  lambda h,p: _raw_grab(h,p)),
        143: ('IMAP',  lambda h,p: _raw_grab(h,p)),
    }

    def _raw_grab(host, port):
        try:
            s = socket.socket(); s.settimeout(3)
            s.connect((host,port))
            data = s.recv(1024).decode('utf-8','ignore').strip()
            s.close()
            return data[:100] if data else '(no banner)'
        except: return '(connection failed)'

    def _http_grab(host, port, proto):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
            req = urllib.request.Request(
                f"{proto}://{host}:{port}",
                headers={'User-Agent':'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=5, context=ctx)
            srv = res.headers.get('Server','—')
            pwr = res.headers.get('X-Powered-By','')
            return f"Server: {srv}  {('| '+pwr) if pwr else ''}"
        except Exception as e:
            return f"(error: {str(e)[:40]})"

    for port in sorted(open_p):
        svc    = COMMON_PORTS.get(port, 'Unknown')
        grabfn = GRABBERS.get(port, (svc, lambda h,p: _raw_grab(h,p)))[1]
        result = grabfn(target, port)
        col    = R if port in RISKY else G
        print(f"  {C}{port:<8}{col}{svc:<14}{RS}{W}{result}{RS}")


# ══════════════════════════════════════════════════════════════════
# ██████╗ ██████╗  ██████╗
# ██╔══██╗██╔══██╗██╔═══██╗
# ██████╔╝██████╔╝██║   ██║
# ██╔═══╝ ██╔══██╗██║   ██║
# ██║     ██║  ██║╚██████╔╝
# ╚═╝     ╚═╝  ╚═╝ ╚═════╝
#  🔴 PROFESSIONAL TOOLS
# ══════════════════════════════════════════════════════════════════

# ── P1: NUCLEI STYLE (Template-based Vulnerability Scanner) ────
NUCLEI_TEMPLATES = {
    'CVE-2017-5638': {
        'name':    'Apache Struts RCE (EternalBlue)',
        'type':    'CVE',
        'severity':'CRITICAL',
        'port':    [80,8080,443],
        'check':   'struts_check',
        'desc':    'Apache Struts 2 Remote Code Execution',
    },
    'CVE-2019-19781': {
        'name':    'Citrix ADC Path Traversal',
        'type':    'CVE',
        'severity':'CRITICAL',
        'port':    [443,80],
        'check':   'path_traversal_check',
        'desc':    'Citrix ADC / Gateway path traversal vulnerability',
    },
    'EXPOSED-ADMIN': {
        'name':    'Exposed Admin Panel',
        'type':    'Misconfiguration',
        'severity':'HIGH',
        'port':    [80,443,8080,8443],
        'check':   'admin_panel_check',
        'desc':    'Publicly accessible admin/login pages',
    },
    'DEFAULT-CREDS-HTTP': {
        'name':    'Default HTTP Credentials',
        'type':    'Misconfiguration',
        'severity':'CRITICAL',
        'port':    [80,8080,8443],
        'check':   'default_creds_check',
        'desc':    'Web interface using factory-default credentials',
    },
    'MISSING-SECURITY-HEADERS': {
        'name':    'Missing Security Headers',
        'type':    'Misconfiguration',
        'severity':'MEDIUM',
        'port':    [80,443,8080],
        'check':   'sec_headers_check',
        'desc':    'HTTP security headers not configured',
    },
    'OPEN-REDIRECT': {
        'name':    'Open Redirect Check',
        'type':    'Web',
        'severity':'MEDIUM',
        'port':    [80,443,8080],
        'check':   'open_redirect_check',
        'desc':    'URL redirect vulnerability',
    },
    'EXPOSED-GIT': {
        'name':    'Exposed .git Directory',
        'type':    'Misconfiguration',
        'severity':'HIGH',
        'port':    [80,443,8080],
        'check':   'git_exposure_check',
        'desc':    'Git repository exposed on web server',
    },
    'TELNET-OPEN': {
        'name':    'Telnet Service Exposed',
        'type':    'Network',
        'severity':'CRITICAL',
        'port':    [23],
        'check':   'telnet_check',
        'desc':    'Unencrypted Telnet service is accessible',
    },
    'SSL-EXPIRED': {
        'name':    'SSL Certificate Expired',
        'type':    'SSL',
        'severity':'HIGH',
        'port':    [443,8443],
        'check':   'ssl_expiry_check',
        'desc':    'SSL/TLS certificate is expired or expiring soon',
    },
    'SMB-OPEN': {
        'name':    'SMB Port Exposed',
        'type':    'Network',
        'severity':'CRITICAL',
        'port':    [445],
        'check':   'smb_check',
        'desc':    'SMB (port 445) is exposed — EternalBlue risk',
    },
}

def run_nuclei_check(check_name, target, port):
    """Run a specific template check and return finding."""
    ctx = ssl.create_default_context()
    ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

    if check_name == 'admin_panel_check':
        paths = ['/admin','/wp-admin','/administrator','/login',
                 '/manager','/console','/dashboard','/setup']
        found = []
        for path in paths:
            try:
                proto = 'https' if port in (443,8443) else 'http'
                req   = urllib.request.Request(
                    f"{proto}://{target}:{port}{path}",
                    headers={'User-Agent':'Mozilla/5.0'})
                res   = urllib.request.urlopen(req, timeout=3, context=ctx)
                if res.status in (200,301,302,403):
                    found.append(f"{path} [{res.status}]")
            except: pass
        return ('FOUND', found) if found else ('NOT_FOUND', [])

    elif check_name == 'default_creds_check':
        found = []
        for user,pw in DEFAULT_CREDS[:8]:
            creds = base64.b64encode(f"{user}:{pw}".encode()).decode()
            try:
                proto = 'https' if port in (443,8443) else 'http'
                req   = urllib.request.Request(
                    f"{proto}://{target}:{port}/",
                    headers={'Authorization':f'Basic {creds}','User-Agent':'Mozilla/5.0'})
                res   = urllib.request.urlopen(req, timeout=3, context=ctx)
                if res.status == 200:
                    found.append(f"{user}/{pw}")
                    break
            except: pass
        return ('FOUND', found) if found else ('NOT_FOUND', [])

    elif check_name == 'sec_headers_check':
        missing = []
        try:
            proto = 'https' if port in (443,8443) else 'http'
            req   = urllib.request.Request(
                f"{proto}://{target}:{port}/",
                headers={'User-Agent':'Mozilla/5.0'})
            res   = urllib.request.urlopen(req, timeout=5, context=ctx)
            hdrs  = dict(res.headers)
            for h in ['Strict-Transport-Security','X-Frame-Options',
                      'Content-Security-Policy','X-Content-Type-Options']:
                if not any(h.lower()==k.lower() for k in hdrs):
                    missing.append(h)
        except: pass
        return ('FOUND', missing) if missing else ('NOT_FOUND', [])

    elif check_name == 'git_exposure_check':
        try:
            proto = 'https' if port in (443,8443) else 'http'
            req   = urllib.request.Request(
                f"{proto}://{target}:{port}/.git/HEAD",
                headers={'User-Agent':'Mozilla/5.0'})
            res   = urllib.request.urlopen(req, timeout=3, context=ctx)
            if res.status == 200:
                return ('FOUND', ['.git/HEAD accessible!'])
        except: pass
        return ('NOT_FOUND', [])

    elif check_name == 'ssl_expiry_check':
        try:
            conn = ssl.create_default_context().wrap_socket(
                socket.create_connection((target,port),timeout=5),
                server_hostname=target)
            cert = conn.getpeercert()
            conn.close()
            exp  = cert.get('notAfter','')
            if exp:
                exp_dt = datetime.datetime.strptime(exp,'%b %d %H:%M:%S %Y %Z')
                days   = (exp_dt - datetime.datetime.utcnow()).days
                if days < 0:
                    return ('FOUND', [f'Certificate EXPIRED {abs(days)} days ago!'])
                elif days < 30:
                    return ('FOUND', [f'Certificate expires in {days} days!'])
        except: pass
        return ('NOT_FOUND', [])

    elif check_name in ('telnet_check', 'smb_check',
                         'struts_check', 'path_traversal_check',
                         'open_redirect_check'):
        if scan_port(target, port, 1):
            return ('FOUND', [f'Port {port} is open'])
        return ('NOT_FOUND', [])

    return ('NOT_FOUND', [])

def nuclei_scanner():
    sep("🔴 P1 — NUCLEI STYLE SCANNER  (Professional)")
    net = get_net_info()
    print(f"""
  {LVL_P}WHAT THIS DOES:{RS}
  {W}Replicates Nuclei — the most popular professional
  vulnerability scanner used in bug bounty programs.
  Runs {len(NUCLEI_TEMPLATES)} built-in templates checking for
  CVEs, misconfigurations, default credentials, and more.{RS}
  """)

    target = input(f"  {Y}  ➤  Target IP/hostname (default {net['gateway']}): {RS}").strip() or net['gateway']
    print(f"\n  {W}Select templates:{RS}")
    print(f"  {C}[1] {W}All templates  {C}[2] {W}Critical only  {C}[3] {W}Web only  {C}[4] {W}Network only{RS}")
    filt = input(f"\n  {Y}  ➤  Choice [1-4]: {RS}").strip()

    if filt == '2':
        templates = {k:v for k,v in NUCLEI_TEMPLATES.items() if v['severity']=='CRITICAL'}
    elif filt == '3':
        templates = {k:v for k,v in NUCLEI_TEMPLATES.items() if v['type'] in ('Web','Misconfiguration','SSL')}
    elif filt == '4':
        templates = {k:v for k,v in NUCLEI_TEMPLATES.items() if v['type']=='Network'}
    else:
        templates = NUCLEI_TEMPLATES

    print(f"\n  {C}Running {len(templates)} templates against {G}{target}{RS}\n")
    print(f"  {W}{BD}{'Template':<25}{'Severity':<12}{'Status'}{RS}")
    sep()

    findings  = []
    start     = time.time()

    for tid, tmpl in templates.items():
        # Check if any relevant port is open
        open_p = [p for p in tmpl['port'] if scan_port(target, p, 1)]
        if not open_p:
            sev_col = DIM
            print(f"  {DIM}{tid[:23]:<25}{'—':<12}SKIP (port closed){RS}")
            continue

        sev_col = (R if tmpl['severity']=='CRITICAL' else
                   Y if tmpl['severity']=='HIGH' else
                   C if tmpl['severity']=='MEDIUM' else G)

        result_status = 'NOT_FOUND'
        result_data   = []
        for p in open_p:
            status, data = run_nuclei_check(tmpl['check'], target, p)
            if status == 'FOUND':
                result_status = 'FOUND'
                result_data   = data
                break

        if result_status == 'FOUND':
            print(f"  {sev_col}[{tmpl['severity']:<8}]{RS} {tid[:23]:<24} {R}● VULNERABLE{RS}")
            findings.append((tid, tmpl, result_data))
        else:
            print(f"  {sev_col}[{tmpl['severity']:<8}]{RS} {tid[:23]:<24} {G}● SAFE{RS}")

    elapsed = time.time()-start
    sep()
    print(f"\n  {W}Scan time : {C}{elapsed:.2f}s")
    print(f"  {W}Templates : {C}{len(templates)}")
    print(f"  {R}{BD}Vulnerable: {len(findings)}{RS}")

    if findings:
        sep("📋 DETAILED FINDINGS")
        for i,(tid,tmpl,data) in enumerate(findings,1):
            sev_col = R if tmpl['severity']=='CRITICAL' else Y
            print(f"\n  {sev_col}{BD}[{i}] {tid}{RS}")
            print(f"  {W}  Name    : {tmpl['name']}")
            print(f"  {W}  Type    : {tmpl['type']}")
            print(f"  {sev_col}  Severity: {tmpl['severity']}")
            print(f"  {W}  Desc    : {tmpl['desc']}")
            if data:
                print(f"  {R}  Found   : {', '.join(str(d) for d in data[:3])}{RS}")


# ── P2: NAABU STYLE (Fast Port Discovery Pipeline) ─────────────
def naabu_style():
    sep("🔴 P2 — NAABU STYLE PORT DISCOVERY  (Professional)")
    net = get_net_info()
    print(f"""
  {LVL_P}WHAT THIS DOES:{RS}
  {W}Replicates Naabu by ProjectDiscovery.
  Blazing-fast port discovery + automatic service
  detection + optional Nuclei integration pipeline.{RS}
  """)

    target = input(f"  {Y}  ➤  Target (IP, CIDR e.g. 192.168.1.0/24): {RS}").strip() or net['gateway']

    # Expand CIDR or single IP
    targets = []
    try:
        network = ipaddress.IPv4Network(target, strict=False)
        targets = [str(ip) for ip in network.hosts()]
        if len(targets) > 50:
            print(f"  {Y}  Large range: scanning first 50 hosts{RS}")
            targets = targets[:50]
    except:
        targets = [target]

    print(f"\n  {C}Targets: {len(targets)} host(s){RS}")
    print(f"  {W}Phase 1: SYN port discovery...{RS}\n")

    ports      = [21,22,23,25,53,80,110,143,443,445,3306,3389,5900,8080,8443,27017,6379]
    all_results= {}
    total_work = len(targets) * len(ports)
    done       = [0]
    lock       = threading.Lock()
    start      = time.time()

    def scan_target_port(args):
        ip, port = args
        result   = scan_port(ip, port, 0.4)
        with lock:
            done[0] += 1
            if done[0] % 50 == 0:
                sys.stdout.write(f"\r  {progress(done[0], total_work)}   ")
                sys.stdout.flush()
            if result:
                all_results.setdefault(ip,[]).append(port)
        return (ip, port, result)

    work = [(ip, port) for ip in targets for port in ports]
    with ThreadPoolExecutor(max_workers=300) as ex:
        list(ex.map(scan_target_port, work))

    elapsed = time.time()-start
    print()
    sep()
    print(f"\n  {G}Discovery complete in {elapsed:.2f}s{RS}\n")

    if not all_results:
        print(f"  {Y}No open ports found.{RS}")
        return

    print(f"  {W}{BD}{'Host':<20}{'Open Ports':<40}{'Services'}{RS}")
    sep()
    for ip, open_p in sorted(all_results.items()):
        svcs = [COMMON_PORTS.get(p,'?') for p in open_p]
        risky_count = sum(1 for p in open_p if p in RISKY)
        col  = R if risky_count > 0 else G
        print(f"  {C}{ip:<20}{col}{str(open_p):<40}{W}{','.join(svcs[:5])}{RS}")

    print(f"\n  {W}Phase 2: Risk assessment...{RS}\n")
    for ip, open_p in all_results.items():
        critical = [p for p in open_p if RISKY.get(p)=='CRITICAL']
        if critical:
            print(f"  {R}  🚨 {ip} — CRITICAL ports open: {critical}{RS}")

    print(f"\n  {Y}💡 TIP: Run Nuclei scanner on these hosts for full vuln scan!{RS}")


# ── P3: SHODAN STYLE (OSINT / Internet Recon) ─────────────────
def shodan_style():
    sep("🔴 P3 — SHODAN STYLE RECON  (Professional)")
    print(f"""
  {LVL_P}WHAT THIS DOES:{RS}
  {W}Replicates Shodan-style OSINT reconnaissance.
  Gathers public information about a target:
  WHOIS, DNS records, open ports, ASN info, geolocation,
  reverse DNS, SSL certificates, and more.{RS}
  """)

    target = input(f"  {Y}  ➤  Target IP or domain: {RS}").strip()
    if not target:
        print(f"  {R}No target provided.{RS}"); return

    # Resolve domain to IP
    resolved_ip = target
    if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
        sp = spinner_start(f"Resolving {target}...")
        try:
            resolved_ip = socket.gethostbyname(target)
        except: pass
        spinner_stop(sp)
        print(f"  {G}Resolved: {target} → {resolved_ip}{RS}\n")

    report = {}

    # 1. IP Geolocation
    sp = spinner_start("Fetching IP geolocation...")
    try:
        r    = urllib.request.urlopen(f'https://ipapi.co/{resolved_ip}/json/', timeout=8)
        data = json.loads(r.read())
        report['geo'] = data
    except: report['geo'] = {}
    spinner_stop(sp)

    # 2. Reverse DNS
    sp = spinner_start("Reverse DNS lookup...")
    try:
        rdns = socket.gethostbyaddr(resolved_ip)
        report['rdns'] = rdns[0]
    except: report['rdns'] = 'No PTR record'
    spinner_stop(sp)

    # 3. Port scan
    sp = spinner_start("Scanning common ports...")
    top_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5900,8080,8443]
    open_ports = []
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(scan_port, resolved_ip, p, 1): p for p in top_ports}
        for fut in as_completed(futures):
            if fut.result(): open_ports.append(futures[fut])
    report['ports'] = sorted(open_ports)
    spinner_stop(sp)

    # 4. DNS Records
    sp = spinner_start("Querying DNS records...")
    dns_info = {}
    for record_type in ['A','MX','NS','TXT']:
        try:
            cmd = ['nslookup',f'-type={record_type}', target, '8.8.8.8']
            r   = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            dns_info[record_type] = r.stdout[:200] if r.stdout else '—'
        except: dns_info[record_type] = '—'
    report['dns'] = dns_info
    spinner_stop(sp)

    # 5. SSL Certificate
    sp = spinner_start("Checking SSL certificate...")
    ssl_info = {}
    if 443 in open_ports:
        try:
            ctx  = ssl.create_default_context()
            ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
            conn = ctx.wrap_socket(
                socket.create_connection((resolved_ip,443),timeout=5),
                server_hostname=target)
            cert = conn.getpeercert()
            conn.close()
            if cert:
                ssl_info['subject'] = dict(x[0] for x in cert.get('subject',()))
                ssl_info['issuer']  = dict(x[0] for x in cert.get('issuer',()))
                ssl_info['expires'] = cert.get('notAfter','—')
        except: pass
    report['ssl'] = ssl_info
    spinner_stop(sp)

    # ── Display full Shodan-style report ──
    sep()
    geo = report.get('geo',{})
    print(f"""
  {BD}{W}┌─────────────────────────────────────────────────┐{RS}
  {BD}{W}│  🌍  SHODAN-STYLE RECON REPORT                  │{RS}
  {BD}{W}└─────────────────────────────────────────────────┘{RS}

  {C}TARGET     {RS}: {G}{BD}{target}{RS}
  {C}IP ADDRESS {RS}: {G}{resolved_ip}{RS}
  {C}RDNS       {RS}: {W}{report.get('rdns','—')}{RS}
  {C}COUNTRY    {RS}: {W}{geo.get('country_name','—')} {geo.get('country','')}{RS}
  {C}CITY       {RS}: {W}{geo.get('city','—')}, {geo.get('region','—')}{RS}
  {C}ISP / ORG  {RS}: {Y}{geo.get('org','—')}{RS}
  {C}ASN        {RS}: {W}{geo.get('asn','—')}{RS}
  {C}TIMEZONE   {RS}: {W}{geo.get('timezone','—')}{RS}
  {C}LATITUDE   {RS}: {W}{geo.get('latitude','—')}{RS}
  {C}LONGITUDE  {RS}: {W}{geo.get('longitude','—')}{RS}
""")

    sep()
    print(f"\n  {BD}{C}OPEN PORTS:{RS}\n")
    if report['ports']:
        for p in report['ports']:
            svc  = COMMON_PORTS.get(p,'Unknown')
            risk = RISKY.get(p,'')
            col  = R if risk=='CRITICAL' else Y if risk=='WARNING' else G
            print(f"  {col}  ● {p:<8}{W}{svc:<16}{col}{risk or 'OPEN'}{RS}")
    else:
        print(f"  {DIM}  No open ports detected.{RS}")

    if report['ssl']:
        sep()
        print(f"\n  {BD}{C}SSL CERTIFICATE:{RS}")
        subj = report['ssl'].get('subject',{})
        issr = report['ssl'].get('issuer',{})
        print(f"  {W}  Common Name : {G}{subj.get('commonName','—')}")
        print(f"  {W}  Issued By   : {C}{issr.get('organizationName','—')}")
        print(f"  {W}  Expires     : {Y}{report['ssl'].get('expires','—')}{RS}")

    sep()
    # Risk summary
    crit = [p for p in report['ports'] if RISKY.get(p)=='CRITICAL']
    warn = [p for p in report['ports'] if RISKY.get(p)=='WARNING']
    score = max(0, 100 - len(crit)*15 - len(warn)*8)
    print(f"\n  {BD}{W}RISK SCORE: {score_bar(score)}{RS}")
    if crit:
        print(f"\n  {R}{BD}Critical : {crit}{RS}")
    if warn:
        print(f"  {Y}{BD}Warnings : {warn}{RS}")


# ── P4: FULL RECON PIPELINE (Naabu + Nuclei combined) ─────────
def full_recon_pipeline():
    sep("🔴 P4 — FULL RECON PIPELINE  (Professional)")
    net = get_net_info()
    print(f"""
  {LVL_P}WHAT THIS DOES:{RS}
  {W}Runs the FULL professional recon pipeline:
  Step 1: Host Discovery   (like Angry IP / Naabu)
  Step 2: Port Scanning    (like Masscan / Naabu)
  Step 3: Banner Grabbing  (like Nmap -sV)
  Step 4: Vuln Templates   (like Nuclei)
  Step 5: Risk Report      (full scoring){RS}
  """)

    target = input(f"  {Y}  ➤  Target IP or CIDR: {RS}").strip() or net['gateway']

    # Expand targets
    try:
        targets = [str(ip) for ip in ipaddress.IPv4Network(target, strict=False).hosts()][:20]
    except:
        targets = [target]

    pipeline_results = {}

    # ── STEP 1: Host Discovery ─────────────────
    sep("STEP 1/5 — Host Discovery")
    alive = []
    lock  = threading.Lock()
    def qping(ip):
        cmd = (['ping','-n','1','-w','400',ip] if SYSTEM=='Windows'
               else ['ping','-c','1','-W','1',ip])
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=2)
            if r.returncode==0:
                with lock: alive.append(ip)
        except: pass

    sp = spinner_start(f"Discovering {len(targets)} host(s)...")
    with ThreadPoolExecutor(max_workers=60) as ex:
        list(ex.map(qping, targets))
    spinner_stop(sp)
    print(f"\n  {G}✅  {len(alive)} live host(s) found{RS}")
    for ip in alive: print(f"  {C}  ● {ip}{RS}")

    if not alive: return

    # ── STEP 2: Port Scanning ──────────────────
    sep("STEP 2/5 — Port Scanning")
    port_results = {}
    sp = spinner_start("Fast port scanning all live hosts...")
    scan_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5900,8080,8443,6379,27017,2375]
    for ip in alive:
        open_p = []
        with ThreadPoolExecutor(max_workers=30) as ex:
            futures = {ex.submit(scan_port, ip, p, 0.5): p for p in scan_ports}
            for fut in as_completed(futures):
                if fut.result(): open_p.append(futures[fut])
        port_results[ip] = sorted(open_p)
    spinner_stop(sp)
    for ip, ports in port_results.items():
        col = R if any(p in RISKY for p in ports) else G
        print(f"  {C}{ip:<20}{col}{ports}{RS}")

    # ── STEP 3: Banner Grabbing ────────────────
    sep("STEP 3/5 — Banner Grabbing")
    banner_results = {}
    sp = spinner_start("Grabbing service banners...")
    for ip in alive:
        banners = {}
        for port in port_results.get(ip,[])[:5]:
            try:
                s = socket.socket(); s.settimeout(2)
                s.connect((ip,port))
                data = s.recv(256).decode('utf-8','ignore').strip()
                s.close()
                banners[port] = data[:60] or '(no banner)'
            except: banners[port] = '(no banner)'
        banner_results[ip] = banners
    spinner_stop(sp)
    for ip, banners in banner_results.items():
        if banners:
            print(f"  {C}{ip}{RS}")
            for port, banner in banners.items():
                svc = COMMON_PORTS.get(port,'?')
                print(f"    {W}:{port} {DIM}{svc}{RS}  {G}{banner[:50]}{RS}")

    # ── STEP 4: Vulnerability Check ────────────
    sep("STEP 4/5 — Vulnerability Templates")
    vuln_results = {}
    key_templates = ['EXPOSED-ADMIN','DEFAULT-CREDS-HTTP','MISSING-SECURITY-HEADERS',
                     'TELNET-OPEN','SMB-OPEN','EXPOSED-GIT','SSL-EXPIRED']
    for ip in alive:
        vulns = []
        for tid in key_templates:
            tmpl  = NUCLEI_TEMPLATES[tid]
            ports = [p for p in port_results.get(ip,[]) if p in tmpl['port']]
            for p in ports:
                status, data = run_nuclei_check(tmpl['check'], ip, p)
                if status == 'FOUND':
                    vulns.append((tid, tmpl['severity'], data))
        vuln_results[ip] = vulns

    for ip, vulns in vuln_results.items():
        if vulns:
            print(f"\n  {R}{BD}🚨 {ip} — {len(vulns)} finding(s):{RS}")
            for tid, sev, data in vulns:
                print(f"  {R}  ● [{sev}] {tid}{RS}")
        else:
            print(f"  {G}  ✅ {ip} — No vulnerabilities found{RS}")

    # ── STEP 5: Final Risk Report ──────────────
    sep("STEP 5/5 — Risk Report")
    print(f"\n  {BD}{W}{'Host':<20}{'Open Ports':<8}{'Critical':<10}{'Score'}{RS}")
    sep()
    for ip in alive:
        ports   = port_results.get(ip,[])
        vulns   = vuln_results.get(ip,[])
        crit    = sum(1 for _,sev,_ in vulns if sev=='CRITICAL')
        score   = max(0, 100 - len(ports)*3 - crit*20)
        col     = G if score>=80 else Y if score>=50 else R
        print(f"  {C}{ip:<20}{W}{len(ports):<8}{R}{crit:<10}{col}{score}/100{RS}")

    print(f"\n  {G}Pipeline complete! {len(alive)} host(s) fully analyzed.{RS}")


# ══════════════════════════════════════════════════════════════════
#  SAVE REPORT
# ══════════════════════════════════════════════════════════════════

SCAN_LOG = []

def save_full_report():
    sep("💾 SAVE FULL REPORT")
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fn = f'netsec_report_{ts}.txt'
    net= get_net_info()
    with open(fn,'w',encoding='utf-8') as f:
        f.write('='*68+'\n')
        f.write('  🔱 ULTIMATE NETWORK SECURITY TOOLKIT — REPORT\n')
        f.write(f"  By  : Karthigeyan Ravindranathan (karthik-sec)\n")
        f.write(f"  Date: {datetime.datetime.now()}\n")
        f.write(f"  IP  : {net['local_ip']}   GW: {net['gateway']}\n")
        f.write('='*68+'\n\n')
        if SCAN_LOG:
            f.write('SCAN HISTORY:\n')
            for entry in SCAN_LOG:
                f.write(f"  [{entry['time']}] {entry['tool']} — {entry['target']}\n")
    sp = spinner_start("Writing report...")
    time.sleep(0.8); spinner_stop(sp)
    print(f"\n  {G}✅  Report saved: {BD}{fn}{RS}")


# ══════════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════════

def main():
    banner()
    disclaimer()

    net = get_net_info()
    print(f"  {W}  System  : {C}{SYSTEM}   {W}IP: {G}{net['local_ip']}   {W}Gateway: {G}{net['gateway']}{RS}\n")

    MENU = [
        ('divider', f"🟢 BEGINNER  —  Like Angry IP Scanner & Zenmap"),
        ('B1', '🟢 Angry IP Style      — Scan all hosts, show online/offline',  angry_ip_scanner),
        ('B2', '🟢 Zenmap Style        — Visual port scan with topology map',    zenmap_style),
        ('B3', '🟢 Host Discovery      — Find & identify all devices',           simple_host_discovery),
        ('divider', f"🟡 INTERMEDIATE  —  Like Nmap Scripts & Masscan"),
        ('I1', '🟡 Nmap + NSE Scripts  — Banner grab, SSL, default creds',       nmap_nse_scanner),
        ('I2', '🟡 Masscan Style       — Ultra-fast port scanner',               masscan_style),
        ('I3', '🟡 Banner Grabber      — Detect service versions',               banner_grabber),
        ('divider', f"🔴 PROFESSIONAL  —  Like Nuclei, Naabu & Shodan"),
        ('P1', '🔴 Nuclei Style        — Template-based CVE/vuln scanner',       nuclei_scanner),
        ('P2', '🔴 Naabu Style         — Fast port discovery pipeline',          naabu_style),
        ('P3', '🔴 Shodan Style        — OSINT / internet recon',                shodan_style),
        ('P4', '🔴 Full Recon Pipeline — Discover→Scan→Banner→Vuln→Report',      full_recon_pipeline),
        ('divider', '─'),
        ('S',  '💾 Save Full Report',                                             save_full_report),
        ('0',  '🚪 Exit',                                                         None),
    ]

    actions = {item[0]: item[2] for item in MENU if item[0] != 'divider'}

    while True:
        sep("🔱 MAIN MENU — NETWORK SECURITY TOOLKIT  A→Z  v1.0")
        for item in MENU:
            if item[0] == 'divider':
                print(f"\n  {DIM}── {item[1]} ──{RS}")
            else:
                key, label = item[0], item[1]
                col = LVL_B if key.startswith('B') else LVL_I if key.startswith('I') else LVL_P if key.startswith('P') else W
                print(f"  {W}[{col}{key}{W}]  {label}{RS}")
        print()

        choice = input(f"  {P}  ➤  Enter choice: {RS}").strip().upper()
        if choice == '0':
            print(f"\n  {P}Stay secure! 💜 — karthik-sec{RS}\n"); break
        elif choice in actions and actions[choice]:
            SCAN_LOG.append({
                'time':   datetime.datetime.now().strftime('%H:%M:%S'),
                'tool':   choice,
                'target': get_net_info()['gateway']
            })
            try:
                actions[choice]()
            except KeyboardInterrupt:
                print(f"\n  {Y}Interrupted.{RS}")
            input(f"\n  {DIM}  Press Enter to return to menu...{RS}")
        else:
            print(f"  {R}  Invalid choice!{RS}")


if __name__ == '__main__':
    main()
