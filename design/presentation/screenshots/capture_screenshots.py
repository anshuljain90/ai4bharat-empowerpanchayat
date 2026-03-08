#!/usr/bin/env python3
"""
Capture screenshots from the live eGramSabha deployment using Playwright.
Target: https://44.194.253.143/
"""
import asyncio
import os
from playwright.async_api import async_playwright

SCREENSHOTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://44.194.253.143"

# Screenshot configurations
SCREENS = [
    {
        "name": "01_citizen_login.png",
        "url": f"{BASE_URL}/citizen-login",
        "wait": 3000,
        "desc": "Citizen Login (Voter ID + Face Scan)",
    },
    {
        "name": "02_citizen_dashboard.png",
        "url": f"{BASE_URL}/citizen/dashboard",
        "wait": 3000,
        "desc": "Citizen Dashboard",
    },
    {
        "name": "03_official_login.png",
        "url": f"{BASE_URL}/login",
        "wait": 3000,
        "desc": "Official/Admin Login",
    },
    {
        "name": "04_landing_page.png",
        "url": f"{BASE_URL}/",
        "wait": 3000,
        "desc": "Landing Page",
    },
]


async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        page = await context.new_page()

        for screen in SCREENS:
            try:
                print(f"  Capturing: {screen['desc']}...")
                await page.goto(screen["url"], wait_until="networkidle", timeout=15000)
                await page.wait_for_timeout(screen["wait"])
                path = os.path.join(SCREENSHOTS_DIR, screen["name"])
                await page.screenshot(path=path, full_page=False)
                print(f"    Saved: {screen['name']}")
            except Exception as e:
                print(f"    Failed: {screen['name']} - {e}")

        await browser.close()


if __name__ == "__main__":
    print("Capturing screenshots from live deployment...")
    asyncio.run(capture_all())
    print("Done.")
