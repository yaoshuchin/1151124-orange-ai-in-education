import asyncio
import os
import json
from playwright.async_api import async_playwright

async def main():
    os.makedirs("assets/slides", exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        # 1920x1080
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        url = "https://www.canva.com/design/DAHbCkzhtrM/17Pf5VscLac9I9CxrFw_Og/view?utm_content=DAHbCkzhtrM&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=ha7f38b031f#1"
        print("Navigating to Canva presentation...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(4)
        
        # Determine total slides
        total_slides = 52
        print(f"Total slides to process: {total_slides}")
        
        # Check if we can enter presentation mode or hide toolbar for cleaner screenshots
        # Pressing 'F' or finding presentation button or hiding toolbars via CSS
        await page.add_style_tag(content="""
            /* Hide Canva floating toolbar if desired, or let it stay transparent */
            header, nav { opacity: 0.9 !important; }
        """)
        
        slides = []
        for i in range(1, total_slides + 1):
            slide_path = f"assets/slides/slide_{i:02d}.png"
            
            # Wait for slide transitions to complete
            await asyncio.sleep(1.2)
            
            # Save screenshot
            await page.screenshot(path=slide_path)
            
            # Extract text & links
            slide_data = await page.evaluate('''() => {
                const ignored = [
                    '分享', '在 Canva 中創作', '上一頁', '下一頁', '放大和縮小', 
                    '顯示更多', '進入全螢幕', '工具列', '前往頁面', '淡化', 
                    'Canva', '(在新的索引標籤或視窗中開啟)', '深藍背景', 'A',
                    '複製連結', '嵌入', '簡報', '全螢幕'
                ];
                
                const elements = Array.from(document.querySelectorAll('span, p, h1, h2, h3, h4, div'));
                const texts = [];
                for (let el of elements) {
                    if (el.children.length === 0 && el.innerText && el.innerText.trim()) {
                        const t = el.innerText.trim();
                        if (!ignored.includes(t) && !/^\\d+\\s*\\/\\s*\\d+$/.test(t) && !/^第\\s*\\d+\\s*頁.*共\\s*\\d+\\s*頁/.test(t)) {
                            // avoid duplicate adjacent texts
                            if (texts.length === 0 || texts[texts.length - 1] !== t) {
                                texts.push(t);
                            }
                        }
                    }
                }
                
                const links = Array.from(document.querySelectorAll('a'))
                    .map(a => ({ text: a.innerText.trim(), href: a.href }))
                    .filter(l => l.href && !l.href.includes('canva.com'));
                    
                return {
                    texts: Array.from(new Set(texts)),
                    links: links
                };
            }''')
            
            slide_entry = {
                "page": i,
                "screenshot": slide_path,
                "texts": slide_data["texts"],
                "links": slide_data["links"]
            }
            slides.append(slide_entry)
            print(f"[{i:02d}/{total_slides}] Texts count: {len(slide_entry['texts'])} | sample: {slide_entry['texts'][:2]}")
            
            # Advance slide
            if i < total_slides:
                await page.keyboard.press("ArrowRight")
                
        with open("captured_slides.json", "w", encoding="utf-8") as f:
            json.dump(slides, f, ensure_ascii=False, indent=2)
            
        # Also generate all_slides_summary.txt
        with open("all_slides_summary.txt", "w", encoding="utf-8") as f:
            for s in slides:
                f.write(f"=== Slide {s['page']:02d} ===\n")
                f.write(f"Texts: {' | '.join(s['texts'])}\n")
                if s["links"]:
                    f.write(f"Links: {s['links']}\n")
                f.write("\n")
                
        print("Completed! Saved captured_slides.json and all_slides_summary.txt")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
