"""
Capture comprehensive multi-device visual evidence for V3 CRO Prototype.
Covers Desktop (1440x900), Laptop (1280x800), Tablet (768x1024), and Mobile (390x844).
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PROTOTYPE_PATH = (Path(__file__).parent / "prototype" / "index.html").resolve()
OUTPUT_DIR = (Path(__file__).parent / "screenshots").resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROTOTYPE_URL = f"file:///{str(PROTOTYPE_PATH).replace(chr(92), '/')}"

def run_capture():
    print(f"Target prototype: {PROTOTYPE_URL}")
    print(f"Saving screenshots to: {OUTPUT_DIR}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ── 1. DESKTOP VIEWPORT (1440 x 900) ───────────────────────────
        print("\n[1/4] Capturing Desktop viewports (1440x900)...")
        ctx_desktop = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx_desktop.new_page()
        page.goto(PROTOTYPE_URL)
        page.wait_for_timeout(1500)

        # Desktop Above-the-fold Hero
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_hero.png"))
        print("  ✓ Saved v3_desktop_hero.png")

        # Desktop Tabs / Science Section
        page.evaluate("document.getElementById('productDetailsSection').scrollIntoView({behavior: 'instant'});")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_tabs_science.png"))
        print("  ✓ Saved v3_desktop_tabs_science.png")

        # Desktop Reviews Section
        page.evaluate("document.getElementById('customerReviewsSection').scrollIntoView({behavior: 'instant'});")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_reviews.png"))
        print("  ✓ Saved v3_desktop_reviews.png")

        # Desktop Cross-Sell / Similar Products
        page.evaluate("document.getElementById('similarProductsSection').scrollIntoView({behavior: 'instant'});")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_similar_products.png"))
        print("  ✓ Saved v3_desktop_similar_products.png")

        # Desktop Cart Drawer Open with Coupon Applied
        page.evaluate("window.scrollTo(0, 0);")
        page.wait_for_timeout(400)
        page.click("#atcBtn")
        page.wait_for_timeout(600)
        page.fill("#cartCouponInput", "WELLBEING10")
        page.click(".apply-coupon-btn")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_cart_drawer.png"))
        print("  ✓ Saved v3_desktop_cart_drawer.png")

        # Desktop AI Chatbot Interaction
        page.evaluate("closeCart();")
        page.wait_for_timeout(400)
        page.click("#chatbotTriggerBtn")
        page.wait_for_timeout(500)
        # Click suggested prompt
        prompt_btn = page.locator(".chat-prompt-pill").first
        if prompt_btn.count() > 0:
            prompt_btn.click()
            page.wait_for_timeout(600)
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_chatbot.png"))
        print("  ✓ Saved v3_desktop_chatbot.png")

        # Desktop Full Page
        page.evaluate("toggleChatbotModal(false);")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUTPUT_DIR / "v3_desktop_full.png"), full_page=True)
        print("  ✓ Saved v3_desktop_full.png")

        ctx_desktop.close()

        # ── 2. LAPTOP VIEWPORT (1280 x 800) ────────────────────────────
        print("\n[2/4] Capturing Laptop viewports (1280x800)...")
        ctx_laptop = browser.new_context(viewport={"width": 1280, "height": 800})
        p_lap = ctx_laptop.new_page()
        p_lap.goto(PROTOTYPE_URL)
        p_lap.wait_for_timeout(1000)
        p_lap.screenshot(path=str(OUTPUT_DIR / "v3_laptop_hero.png"))
        print("  ✓ Saved v3_laptop_hero.png")
        ctx_laptop.close()

        # ── 3. TABLET VIEWPORT (768 x 1024) ────────────────────────────
        print("\n[3/4] Capturing Tablet viewports (768x1024)...")
        ctx_tab = browser.new_context(viewport={"width": 768, "height": 1024})
        p_tab = ctx_tab.new_page()
        p_tab.goto(PROTOTYPE_URL)
        p_tab.wait_for_timeout(1000)
        p_tab.screenshot(path=str(OUTPUT_DIR / "v3_tablet_hero.png"))
        print("  ✓ Saved v3_tablet_hero.png")
        ctx_tab.close()

        # ── 4. MOBILE VIEWPORT (390 x 844 - iPhone 12/13/14) ───────────
        print("\n[4/4] Capturing Mobile viewports (390x844)...")
        ctx_mob = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        p_mob = ctx_mob.new_page()
        p_mob.goto(PROTOTYPE_URL)
        p_mob.wait_for_timeout(1000)

        # Mobile Above-the-fold
        p_mob.screenshot(path=str(OUTPUT_DIR / "v3_mobile_atf.png"))
        print("  ✓ Saved v3_mobile_atf.png")

        # Mobile Scrolled with Sticky ATC Bar & Chatbot
        p_mob.evaluate("window.scrollTo(0, 750);")
        p_mob.wait_for_timeout(600)
        p_mob.screenshot(path=str(OUTPUT_DIR / "v3_mobile_sticky_bar.png"))
        print("  ✓ Saved v3_mobile_sticky_bar.png")

        # Mobile Cart Drawer
        p_mob.evaluate("window.scrollTo(0, 0);")
        p_mob.wait_for_timeout(300)
        p_mob.click("#atcBtn")
        p_mob.wait_for_timeout(600)
        p_mob.screenshot(path=str(OUTPUT_DIR / "v3_mobile_cart_drawer.png"))
        print("  ✓ Saved v3_mobile_cart_drawer.png")

        # Mobile Full Page
        p_mob.evaluate("closeCart();")
        p_mob.wait_for_timeout(300)
        p_mob.screenshot(path=str(OUTPUT_DIR / "v3_mobile_full.png"), full_page=True)
        print("  ✓ Saved v3_mobile_full.png")

        ctx_mob.close()

        browser.close()
    print("\n✓ All V3 screenshots successfully captured and saved to screenshots/ directory!")

if __name__ == "__main__":
    run_capture()
