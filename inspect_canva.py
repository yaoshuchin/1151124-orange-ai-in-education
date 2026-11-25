import asyncio
import os
import json
from playwright.async_api import async_playwright

async def main():
    os.makedirs("assets/slides", exist_ok=True)
    url = "https://www.canva.com/design/DAHbCkzhtrM/17Pf5VscLac9I9CxrFw_Og/view?utm_content=DAHbCkzhtrM&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=ha7f38b031f#1"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        print("Loading Canva URL...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        title = await page.title()
        print("Page Title:", title)
        
        # Check total slides count from DOM or footer
        total_pages = await page.evaluate('''() => {
            const bodyText = document.body.innerText;
            const match = bodyText.match(/\\b(\\d+)\\s*\\/\\s*(\\d+)\\b/) || bodyText.match(/共\\s*(\\d+)\\s*頁/);
            if (match) {
                return match[2] || match[1];
            }
            return null;
        }''')
        print("Detected total pages:", total_pages)
        
        # Try extracting window['bootstrap'] if present
        bootstrap_data = await page.evaluate('''() => {
            const scripts = Array.from(document.querySelectorAll('script'));
            for (let s of scripts) {
                if (s.textContent && s.textContent.includes("window['bootstrap']")) {
                    const idx1 = s.textContent.indexOf("JSON.parse('");
                    if (idx1 !== -1) {
                        const start = idx1 + 12;
                        const end = s.textContent.lastIndexOf("');");
                        const raw = s.textContent.substring(start, end);
                        try {
                            const unescaped = raw.replace(/\\\\'/g, "'").replace(/\\\\\\\\/g, "\\\\");
                            return JSON.parse(unescaped);
                        } catch(e) {
                            return { error: e.toString() };
                        }
                    }
                }
            }
            return null;
        }''')
        
        if bootstrap_data and "error" not in bootstrap_data:
            with open("canva_bootstrap.json", "w", encoding="utf-8") as f:
                json.dump(bootstrap_data, f, ensure_ascii=False, indent=2)
            print("Extracted bootstrap JSON successfully!")
        
        await page.screenshot(path="canva_page_1.png")
        print("Saved canva_page_1.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
