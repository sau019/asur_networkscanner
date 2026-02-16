# Port Scanner - Features Implemented ✅

## Core Features

### ✅ argparse CLI
- Full command-line interface with argument parsing
- Positional argument for target (IP/domain)
- Optional arguments with sensible defaults
- Auto-generated help with `-h` flag

### ✅ Threading (Fast)
- Daemon threads for efficient scanning
- Enter key listener thread (press Enter during scan to see current port)
- Non-blocking, responsive UI during scanning

### ✅ Timeout Control
- Configurable socket timeout with `-t` or `--timeout`
- Default: 1.0 second
- Prevents hanging on unreachable hosts
- Example: `python basicportscanner.py target.com -t 2.5`

### ✅ Banner
````markdown
# Port Scanner - Features Implemented ✅

## Core Features (Updated)

### ✅ Command-line interface (`argparse`)
- Positional `target` argument (IP or domain)
- Flags: `-p/--port`, `-t/--timeout`, `-o/--output`, `-v/--verbose`, `--version`

### ✅ Interactive Console (`asur>`)
- Run `python basicportscanner.py` or `python basicportscanner.py --console` to launch the interactive Asur Console
- Use `set`, `show`, `run`, `history`, `clear`, `help`, `exit` inside console
- Quick workflow: `set target 1.2.3.4` → `set ports 80,443` → `run`

### ✅ Scan Modes
- `-a/--aggressive`: Faster scanning with reduced timeout
- `-s/--stealth`: Slower, randomized delays to reduce detectability
- `--anonymity`: Informational anonymity mode (simulated)

### ✅ Environment / Identity Options (Informational placeholders)
- `--vpn <iface>`: Indicate routing via a VPN interface (requires external VPN setup)
- `--mac-spoof <MAC>`: Informational MAC spoof option (requires privileged platform-specific commands)

### ✅ NSE-like Scripts (Simulated)
- `--nse-script <default|version|vuln|all|script1,script2>`
- Simulates common NSE actions (HTTP title, SSL cert, SSH hostkey, etc.)
- Can be integrated with `nmap --script` (optional enhancement)

### ✅ Saving & Output
- `-o/--output` saves formatted scan results including modes and NSE output

### ✅ UX & Telemetry
- Randomized epic banners (one shown per run)
- Enter-key listener shows live scanning progress
- Human-friendly summary table at end of scan

## Usage Examples

```bash
# Launch interactive console (recommended for discovery)
python basicportscanner.py

# Direct CLI scan (ports, timeout, NSE simulation)
python basicportscanner.py 192.168.1.1 -p 22,80,443 -t 1 --nse-script default

# Aggressive scan
python basicportscanner.py 10.0.0.1 -p 1-1024 -a

# Stealth scan with NSE scripts
python basicportscanner.py example.com -p 80,443 -s --nse-script vuln

# Save results
python basicportscanner.py localhost -p 80 -o results.txt
```

## CLI Options (summary)

```
-p, --port PORT            Port(s) to scan (single, comma list, range, or mixed)
-t, --timeout TIMEOUT      Socket timeout in seconds (default: 1.0)
-o, --output OUTPUT        Save results to output file
-v, --verbose              Show all scanned ports (including closed)
-a, --aggressive           Aggressive mode (faster, reduced timeout)
-s, --stealth              Stealth mode (random delays, evasive)
--anonymity                Anonymity mode (simulated spoofing)
--vpn VPN                  VPN interface name (informational)
--mac-spoof MAC_SPOOF      MAC address to spoof (informational)
--nse-script SCRIPT        NSE-like script(s) to run on open ports (simulated)
--console                  Launch interactive Asur Console
--version                  Show program version
```

## Additional Features

- **Port Service Mapping**: 500+ common ports mapped to services
- **Simulated NSE**: Quick plugin-like checks on open services (HTTP title, SSL cert, SSH key)
- **Interactive Console**: Metasploit-like `asur>` prompt for iterative workflows
- **Error Handling & Interrupts**: Graceful Ctrl+C handling and informative errors

## Limitations & Notes

- `--nse-script` is simulated by default. I can integrate with `nmap --script` to run real NSE scripts if you have `nmap` installed.
- `--mac-spoof` and `--vpn` are currently informational placeholders — actual MAC changes or routing require platform-specific privileged commands or external tools.
- This tool is educational; do not scan targets without permission.

## ⚠️ Important

This tool is for **educational purposes only**. Only scan systems you own or have explicit permission to test. Unauthorized port scanning is illegal.

````
