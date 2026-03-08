#!/usr/bin/env python3
"""
Render all .mmd Mermaid diagrams to high-resolution PNG using mmdc (Mermaid CLI).
Requires: npm install -g @mermaid-js/mermaid-cli
"""
import os
import subprocess
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Puppeteer config to allow running on this system
PUPPETEER_CFG = os.path.join(SCRIPT_DIR, "puppeteer-config.json")


def write_puppeteer_config():
    config = {
        "headless": "new",
        "args": ["--no-sandbox", "--disable-setuid-sandbox"]
    }
    with open(PUPPETEER_CFG, "w") as f:
        json.dump(config, f)


def render_all():
    write_puppeteer_config()

    mmd_files = sorted(f for f in os.listdir(SCRIPT_DIR) if f.endswith('.mmd'))
    print(f"Found {len(mmd_files)} Mermaid diagrams to render.\n")

    for mmd_file in mmd_files:
        mmd_path = os.path.join(SCRIPT_DIR, mmd_file)
        png_path = os.path.join(SCRIPT_DIR, mmd_file.replace('.mmd', '.png'))
        name = mmd_file.replace('.mmd', '')

        print(f"  Rendering {name}...")

        mmdc_path = os.path.join(os.environ.get("APPDATA", ""), "npm", "mmdc.cmd")
        if not os.path.exists(mmdc_path):
            mmdc_path = "mmdc"

        cmd = [
            mmdc_path,
            "-i", mmd_path,
            "-o", png_path,
            "-b", "white",
            "-w", "2400",
            "-H", "1200",
            "-s", "2",
            "-p", PUPPETEER_CFG,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=True)
            if result.returncode == 0 and os.path.exists(png_path):
                size_kb = os.path.getsize(png_path) / 1024
                print(f"    OK: {png_path} ({size_kb:.0f} KB)")
            else:
                print(f"    FAIL: {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"    ERROR: mmdc not found. Install with: npm install -g @mermaid-js/mermaid-cli")
            return
        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT: {name}")

    # Cleanup
    if os.path.exists(PUPPETEER_CFG):
        os.remove(PUPPETEER_CFG)

    print("\nDone.")


if __name__ == "__main__":
    render_all()
