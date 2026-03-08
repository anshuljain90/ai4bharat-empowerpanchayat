#!/usr/bin/env python3
"""
Render a clean system architecture diagram using matplotlib.
Gives precise control over box placement and arrow routing.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "architecture.png")

# Color palette
C_BLUE      = '#1565C0'
C_BLUE_LT   = '#1976D2'
C_ORANGE    = '#FF6F00'
C_ORANGE_LT = '#FB8C00'
C_GREEN     = '#2E7D32'
C_GREEN_DK  = '#1B5E20'
C_TEAL      = '#00838F'
C_GRAY      = '#37474F'
C_GRAY_LT   = '#546E7A'
C_PURPLE    = '#7B1FA2'
C_RED       = '#D32F2F'
C_YELLOW    = '#FFA000'
C_WHITE     = '#FFFFFF'
C_BG        = '#FAFAFA'


def rounded_box(ax, x, y, w, h, text, color, fontsize=9, text_color='white',
                subtext=None, subtextsize=7, bold=True):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                         facecolor=color, edgecolor='none', linewidth=0, zorder=3)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ty = y + h * 0.6 if subtext else y + h / 2
    ax.text(x + w/2, ty, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, fontweight=weight, zorder=4)
    if subtext:
        ax.text(x + w/2, y + h * 0.28, subtext, ha='center', va='center',
                fontsize=subtextsize, color=text_color, fontweight='normal', zorder=4)


def section_box(ax, x, y, w, h, label, color, alpha=0.12):
    """Draw a section background with a label."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                         facecolor=color, edgecolor=color, linewidth=1.5,
                         alpha=alpha, zorder=1)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 0.18, label, ha='center', va='top',
            fontsize=9, color=color, fontweight='bold', zorder=2)


def arrow(ax, x1, y1, x2, y2, label=None, color='#78909C'):
    """Draw a curved arrow between two points."""
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle='->', mutation_scale=12,
                          connectionstyle='arc3,rad=0.05',
                          color=color, linewidth=1.3, zorder=2)
    ax.add_patch(arr)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 0.12
        ax.text(mx, my, label, ha='center', va='center',
                fontsize=6, color='#455A64', fontstyle='italic', zorder=5)


def main():
    fig, ax = plt.subplots(1, 1, figsize=(20, 11), dpi=150)
    ax.set_xlim(-0.5, 19.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # ===== ROW 1: Frontend =====
    section_box(ax, 0, 8.2, 4.5, 2.0, 'BROWSER / MOBILE', C_BLUE)
    rounded_box(ax, 0.3, 8.4, 3.9, 1.3, 'React 19 + MUI 7',  C_BLUE_LT,
                fontsize=11, subtext='face-api.js · MediaPipe · JioMeet · jsPDF')

    # ===== ROW 1: API Gateway =====
    section_box(ax, 5.5, 8.2, 3.5, 2.0, 'AWS EDGE', C_ORANGE)
    rounded_box(ax, 5.8, 8.4, 2.9, 1.3, 'API Gateway', C_ORANGE_LT,
                fontsize=11, subtext='100 req/s · API Key · Rate Limit')

    # Arrow: Frontend -> API GW
    arrow(ax, 4.5, 9.1, 5.8, 9.1, 'HTTPS')

    # ===== ROW 2: Docker Compose (EC2) =====
    section_box(ax, 0, 4.0, 14.0, 3.8, 'EC2 t3.medium — Docker Compose (4 containers)', C_GRAY)

    # Nginx
    rounded_box(ax, 0.5, 6.2, 3.0, 1.0, 'Nginx', C_GRAY_LT,
                fontsize=10, subtext='TLS · Rate Limiting · Reverse Proxy')

    # Node.js
    rounded_box(ax, 4.0, 6.2, 4.2, 1.0, 'Node.js / Express :5000', C_GREEN,
                fontsize=10, subtext='Auth · CRUD · S3 · SNS · Cron Jobs')

    # Python/FastAPI
    rounded_box(ax, 4.0, 4.6, 4.2, 1.0, 'Python / FastAPI :8000', C_ORANGE_LT,
                fontsize=10, subtext='STT · LLM · TTS · Translate · Sentiment')

    # MongoDB
    rounded_box(ax, 9.0, 5.2, 3.5, 1.4, 'MongoDB :27017', C_PURPLE,
                fontsize=10, subtext='14 Collections · GridFS')

    # Arrow: APIGW -> Nginx
    arrow(ax, 7.8, 8.4, 2.0, 7.2, '')

    # Arrows inside Docker
    arrow(ax, 3.5, 6.7, 4.0, 6.7, '/api/*')     # Nginx -> Node
    arrow(ax, 3.5, 6.3, 4.0, 5.1, '/ai/*')       # Nginx -> Python
    arrow(ax, 8.2, 6.5, 9.0, 6.2, '')             # Node -> Mongo
    arrow(ax, 8.2, 5.0, 9.0, 5.6, '')             # Python -> Mongo

    # ===== ROW 3: AWS AI Services (Active) =====
    section_box(ax, 0, 0.2, 9.5, 3.4, 'AWS AI & STORAGE SERVICES — Active (11)', C_GREEN_DK)

    # AI Services
    rounded_box(ax, 0.3, 2.2, 2.6, 0.9, 'Bedrock', C_GREEN,
                fontsize=10, subtext='Nova Lite / Claude Sonnet')
    rounded_box(ax, 3.2, 2.2, 2.6, 0.9, 'AWS Translate', C_GREEN,
                fontsize=10, subtext='10+ Indian Languages')
    rounded_box(ax, 6.1, 2.2, 3.1, 0.9, 'Amazon Polly', C_GREEN,
                fontsize=10, subtext='Aditi · Raveena · S3 Cache')

    # Storage & Ops
    rounded_box(ax, 0.3, 0.6, 2.1, 0.9, 'S3 (×2)', C_TEAL,
                fontsize=9, subtext='Intelligent-Tiering')
    rounded_box(ax, 2.7, 0.6, 2.1, 0.9, 'CloudWatch', C_TEAL,
                fontsize=9, subtext='Structured Logs')
    rounded_box(ax, 5.1, 0.6, 2.1, 0.9, 'Secrets Mgr', C_TEAL,
                fontsize=9, subtext='JWT Secrets')
    rounded_box(ax, 7.5, 0.6, 1.7, 0.9, 'IAM', C_TEAL,
                fontsize=9, subtext='Least Privilege')

    # Arrows: Containers -> AWS Services
    arrow(ax, 5.5, 4.6, 1.6, 3.1, '')   # Python -> Bedrock
    arrow(ax, 6.0, 4.6, 4.5, 3.1, '')   # Python -> Translate
    arrow(ax, 6.5, 4.6, 7.6, 3.1, '')   # Python -> Polly
    arrow(ax, 6.0, 6.2, 1.3, 1.5, '')   # Node -> S3
    arrow(ax, 7.0, 6.2, 3.7, 1.5, '')   # Node -> CloudWatch
    arrow(ax, 7.5, 6.2, 6.1, 1.5, '')   # Node -> Secrets

    # ===== Code-Ready Services =====
    section_box(ax, 10.5, 0.2, 8.5, 3.4, 'CODE-READY — Activate via ENV (4)', C_YELLOW)

    rounded_box(ax, 10.8, 1.8, 3.5, 1.1, 'Rekognition', C_YELLOW,
                fontsize=10, subtext='Face Verification · 90% threshold')
    rounded_box(ax, 14.8, 1.8, 3.8, 1.1, 'DocumentDB', C_YELLOW,
                fontsize=10, subtext='Managed MongoDB Migration')
    rounded_box(ax, 10.8, 0.5, 3.5, 1.0, 'AWS Transcribe', C_YELLOW,
                fontsize=10, subtext='STT · 28 Languages')
    rounded_box(ax, 14.8, 0.5, 3.8, 1.0, 'Amazon SNS', C_YELLOW,
                fontsize=10, subtext='SMS Notifications · Transactional')

    # ===== Provider Abstraction note =====
    rounded_box(ax, 14.5, 4.5, 5.0, 1.2, 'Provider Abstraction', C_GRAY,
                fontsize=11, subtext='8 ENV switches · Swap any service\nJio↔Whisper↔Transcribe · Polly↔gTTS · etc.')

    # Legend
    legend_y = 8.5
    legend_x = 10.0
    ax.text(legend_x, legend_y + 1.2, 'LEGEND', fontsize=9, fontweight='bold', color='#37474F')
    for i, (label, color) in enumerate([
        ('Frontend', C_BLUE_LT), ('API Gateway', C_ORANGE_LT),
        ('Node.js Backend', C_GREEN), ('AI Backend (Python)', C_ORANGE_LT),
        ('Database', C_PURPLE), ('AWS AI Services', C_GREEN),
        ('AWS Storage/Ops', C_TEAL), ('Code-Ready', C_YELLOW),
    ]):
        row = i // 2
        col = i % 2
        bx = legend_x + col * 4.5
        by = legend_y + 0.7 - row * 0.42
        box = FancyBboxPatch((bx, by), 0.3, 0.25, boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='none', zorder=3)
        ax.add_patch(box)
        ax.text(bx + 0.45, by + 0.12, label, fontsize=7.5, va='center', color='#37474F')

    plt.tight_layout(pad=0.5)
    plt.savefig(OUTPUT, dpi=150, bbox_inches='tight', facecolor=C_BG, pad_inches=0.3)
    plt.close()
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Architecture diagram saved: {OUTPUT} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
