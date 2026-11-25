import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    abs_index_path = os.path.abspath("index.html").replace("\\", "/")
    url = f"file:///{abs_index_path}"
    print("Testing URL:", url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        await page.goto(url)
        await asyncio.sleep(1)

        # 1. Test Password Gate is visible
        is_gate_visible = await page.locator("#passwordGateModal").is_visible()
        print("1. Password Gate visible initially:", is_gate_visible)
        assert is_gate_visible, "Password Gate should be visible on initial load"

        # 2. Test wrong password
        await page.fill("#passwordInput", "wrongpassword")
        await page.click("#btnUnlock")
        await asyncio.sleep(0.5)
        error_display = await page.evaluate("() => document.getElementById('passwordError').style.display")
        print("2. Error message displayed on wrong password:", error_display == 'block')
        assert error_display == 'block', "Error message should be displayed"

        # 3. Test correct password: nato
        await page.fill("#passwordInput", "nato")
        await page.click("#btnUnlock")
        await asyncio.sleep(0.8)
        is_gate_hidden = await page.evaluate("() => document.getElementById('passwordGateModal').classList.contains('hidden')")
        print("3. Password Gate hidden after entering 'nato':", is_gate_hidden)
        assert is_gate_hidden, "Password gate should be hidden after correct password"

        # Take screenshot of unlocked main page
        await page.screenshot(path="test_unlocked_page.png")
        print("Saved test_unlocked_page.png")

        # 4. Test Font Size Toggle
        await page.click('[data-font-val="xlarge"]')
        font_attr = await page.evaluate("() => document.body.getAttribute('data-font')")
        print("4. Font attribute after clicking '特大':", font_attr)
        assert font_attr == "xlarge", "Font should be xlarge"

        # 5. Test Theme Toggle (Dark, Green, Blue, Light)
        for theme in ["dark", "green", "blue", "light"]:
            await page.click(f'[data-theme-val="{theme}"]')
            theme_attr = await page.evaluate("() => document.body.getAttribute('data-theme')")
            print(f"5. Theme switched to {theme}:", theme_attr == theme)
            assert theme_attr == theme, f"Theme should be {theme}"

        # 6. Test Tabs Switching
        tabs = ["intro", "voice_minutes", "shooting_game", "picture_book", "exam_master", "resources", "prompts", "all"]
        for tab in tabs:
            await page.click(f'[data-tab="{tab}"]')
            await asyncio.sleep(0.2)
            card_count = await page.locator(".slide-card").count()
            print(f"6. Tab '{tab}' clicked. Visible cards:", card_count)

        # 7. Test Lightbox
        await page.click(".slide-thumbnail-wrapper")
        await asyncio.sleep(0.5)
        is_lightbox_active = await page.evaluate("() => document.getElementById('lightboxModal').classList.contains('active')")
        print("7. Lightbox opened on clicking slide thumbnail:", is_lightbox_active)
        assert is_lightbox_active, "Lightbox should be active"

        # Press Next in lightbox
        await page.keyboard.press("ArrowRight")
        indicator_text = await page.locator("#lightboxPageIndicator").inner_text()
        print("Lightbox page indicator after ArrowRight:", indicator_text)

        # Press Escape to close
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.3)
        is_lightbox_closed = await page.evaluate("() => !document.getElementById('lightboxModal').classList.contains('active')")
        print("Lightbox closed after Escape:", is_lightbox_closed)

        print("ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
