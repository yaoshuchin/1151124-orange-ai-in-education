import json
import os

with open("captured_slides.json", "r", encoding="utf-8") as f:
    slides = json.load(f)

# Define category rules
# 1-4: Intro & Lecturer
# 5-17: Voice-to-Text & Meeting Minutes
# 18-25: Shooting Review Game & Battle Mode
# 26-44: Cloud Picture Book Generator
# 45-52: Comprehensive Exam Question Master

categories = [
    {
        "id": "intro",
        "title": "課程導言與講師介紹",
        "icon": "fas fa-chalkboard-teacher",
        "badge": "講師引言",
        "desc": "橘子老師帶領掌握 AI 時代教學全新可能，整合 Agent 智能代理與教育場景實踐。",
        "slides_range": [1, 4]
    },
    {
        "id": "voice_minutes",
        "title": "語音轉逐字稿與會議記錄",
        "icon": "fas fa-microphone-alt",
        "badge": "行政自動化",
        "desc": "利用 Gemini Notebook 與客製化 SKILL，將會議語音 MP3 自動辨識角色分工並產製標準會議紀錄。",
        "slides_range": [5, 17]
    },
    {
        "id": "shooting_game",
        "title": "課程複習射擊遊戲",
        "icon": "fas fa-gamepad",
        "badge": "遊戲化教學",
        "desc": "整合課本 PDF 與教學進度計畫，自動生成即玩 HTML5 課程射擊複習遊戲與雙人對戰模式。",
        "slides_range": [18, 25]
    },
    {
        "id": "picture_book",
        "title": "雲端上的繪本生成器",
        "icon": "fas fa-book-open",
        "badge": "跨領域創作",
        "desc": "Google 體系 AI 工作流全新視野，從角色一致性設計到 10 頁皮克斯風格繪本全自動排程產出。",
        "slides_range": [26, 44]
    },
    {
        "id": "exam_master",
        "title": "會考出題大師與素養評量",
        "icon": "fas fa-file-signature",
        "badge": "智慧命題",
        "desc": "直接將 SKILL 壓縮包安裝，上傳題目截圖即可一鍵召喚 AI 進行素養導向命題、概念解析與測驗卷生成。",
        "slides_range": [45, 52]
    }
]

# Curated detailed cards for each slide
slide_meta = {
    1: {
        "title": "Ai在教學上的應用 - 封面首頁",
        "cat": "intro",
        "summary": "橘子老師主講：AI 在教學上的全方位創新應用與教育落地實戰。",
        "tags": ["首頁", "橘子老師", "AI教學"]
    },
    2: {
        "title": "講師介紹與粉專資源",
        "cat": "intro",
        "summary": "追蹤「橘子老師」個人專頁與「橘子老師教室」，掌握第一手 AI 教育教學資訊與資源包。",
        "tags": ["粉絲專頁", "教學社群"]
    },
    3: {
        "title": "加入學習社群與教學交流",
        "cat": "intro",
        "summary": "與全台熱心教育工作者一同探索 Gemini、NotebookLM 與 Agent 教學實踐技巧。",
        "tags": ["教育社群", "交流成長"]
    },
    4: {
        "title": "開啟 Gemini 教學應用新紀元",
        "cat": "intro",
        "summary": "以 Google 體系強大生態鏈為核心，解鎖從行政、教學到評量的多重 AI 工具鏈。",
        "tags": ["Google生態", "Gemini"]
    },
    5: {
        "title": "Gemini 介面與功能準備",
        "cat": "voice_minutes",
        "summary": "登入 Gemini 工作環境，準備語音多模態分析與長文件處理流程。",
        "tags": ["Gemini", "長文本"]
    },
    6: {
        "title": "多模態資訊處理基礎",
        "cat": "voice_minutes",
        "summary": "理解 Gemini 如何處理音訊、圖像、文件等多模態輸入並建立上下文對齊。",
        "tags": ["多模態", "音訊處理"]
    },
    7: {
        "title": "Gemini Notebook 筆記本概念",
        "cat": "voice_minutes",
        "summary": "將不同教學專案與行政資料分類管理，建立獨立知識脈絡的專屬筆記本。",
        "tags": ["Notebook", "知識管理"]
    },
    8: {
        "title": "語音轉逐字稿與會議記錄架構",
        "cat": "voice_minutes",
        "summary": "學校行政會報、教學研討會音訊檔案直接轉化為標準公文紀錄之核心工作流。",
        "tags": ["語音轉逐字稿", "會議記錄", "行政減負"]
    },
    9: {
        "title": "建立語音辨識筆記本與上傳素材",
        "cat": "voice_minutes",
        "summary": "步驟 1：建立【語音辨識】筆記本，上傳行政會報音訊檔與會議記錄格式範本 PDF。",
        "tags": ["素材準備", "格式對齊"]
    },
    10: {
        "title": "提示詞實戰：雲端硬碟自動儲存版",
        "cat": "voice_minutes",
        "summary": "提示詞自動辨識講者角色 (講者1、講者2)，於雲端硬碟自動以時間命名建立資料夾並儲存逐字稿與會議摘要文件。",
        "tags": ["提示詞實戰", "雲端硬碟自動化", "講者辨識"],
        "prompt": """1.開啟Gemini Notebook 中[語音辨識]筆記本，將筆記本中語音檔12月30日 上午行政會報.mp3進行語音辨識，如果語音中有不同人物的語音，請以講者1、講者2來標示，將辨識後的逐字稿儲存在雲端硬碟中會議工具資料夾，並且以當時日期時間為名稱建立資料夾，將辨識後的逐字稿以文字檔儲存在雲端硬碟該資料夾中(檔案命名: 資料夾名稱-辨識逐字稿)
2.依照Gemini Notebook 中語音辨識筆記本中行政會報會議記錄範本.pdf格式，將逐字稿內容整理成範本格式，並儲存檔案在該資料夾中(檔案命名:資料夾名稱-會議紀錄彙整)"""
    },
    11: {
        "title": "提示詞實戰：直接下載版 (免串雲端)",
        "cat": "voice_minutes",
        "summary": "適合個別操作的輕量版提示詞，辨識不同講者身分後，直接產製 txt 逐字稿與 Google Docs 格式會議紀錄供一鍵下載。",
        "tags": ["一鍵下載", "免設定雲端"],
        "prompt": """開啟Gemini Notebook 中[語音辨識]筆記本，將筆記本中mp3語音檔進行語音辨識，如果語音中有不同人物的語音，請以講者1(身分)、講者2(身分)來標示(如果知道講者身分則標註身分)，將辨識後的逐字稿提供txt檔案下載，檔案命名: 當天日期時間-辨識逐字稿
2.依照Gemini Notebook 中語音辨識筆記本中行政會報會議記錄範本.pdf格式，將逐字稿內容整理成範本格式，提供彙整後會議紀錄google文件檔案下載，檔案命名: 當天日期時間-會議紀錄彙整"""
    },
    12: {
        "title": "雙版本提示詞比對與教學建議",
        "cat": "voice_minutes",
        "summary": "比對「雲端硬碟歸檔版」與「直接下載版」之適用情境，助行政同仁與教師靈活選擇。",
        "tags": ["版本比對", "教學指引"]
    },
    13: {
        "title": "進階自動化：封裝為專屬 SKILL",
        "cat": "voice_minutes",
        "summary": "將繁複的逐字稿與會議記錄提示詞封裝成可重複調用的 SKILL.md 技能檔，實現一秒召喚。",
        "tags": ["SKILL封裝", "可重用技能"]
    },
    14: {
        "title": "下載 SKILL.md 與結構說明",
        "cat": "voice_minutes",
        "summary": "下載官方提供的 SKILL.md 範本檔，修改技能名稱與對應自訂需求。",
        "tags": ["SKILL下載", "自訂技能"]
    },
    15: {
        "title": "修改技能名稱與參數調校",
        "cat": "voice_minutes",
        "summary": "根據學校各處室特性（教務、學務、總務）自訂欄位，設定專屬會議紀錄範式。",
        "tags": ["參數配置", "處室客製化"]
    },
    16: {
        "title": "上傳 SKILL.md 至 AI 平台啟用",
        "cat": "voice_minutes",
        "summary": "將設定完成的 SKILL 檔案上傳至系統中，往後只需一句話即可全自動執行會議記錄。",
        "tags": ["上傳啟用", "自動化工作流"]
    },
    17: {
        "title": "語音自動化成果總結與課堂銜接",
        "cat": "voice_minutes",
        "summary": "完成行政事務自動化，接著邁向課堂教學互動化——進入「課程複習射擊遊戲」篇章。",
        "tags": ["行政轉教學", "承先啟後"]
    },
    18: {
        "title": "課程複習射擊遊戲 - 概念介紹",
        "cat": "shooting_game",
        "summary": "告別枯燥考卷！利用 AI 自動將課本單元內容編排為學生最愛的打字射擊與問答闖關遊戲。",
        "tags": ["遊戲化學習", "射擊遊戲", "課堂互動"]
    },
    19: {
        "title": "下載射擊遊戲 SKILL 與環境設定",
        "cat": "shooting_game",
        "summary": "取得「課程複習射擊遊戲」專屬技能檔，支援輸入 @ 直接喚醒遊戲生成引擎。",
        "tags": ["SKILL下載", "喚醒指令"]
    },
    20: {
        "title": "上傳教學教材與 @ 呼叫技能",
        "cat": "shooting_game",
        "summary": "上傳課程單元資料，輸入 @射擊遊戲 即可依據教學重點自動產生單人闖關網頁遊戲。",
        "tags": ["單人模式", "HTML5遊戲"]
    },
    21: {
        "title": "升級：課程複習射擊遊戲 - 對戰版",
        "cat": "shooting_game",
        "summary": "支援雙人連線或同屏對戰！讓學生以即時競速搶答形式擊落知識隕石與敵機，激發高度學習動機。",
        "tags": ["對戰版", "雙人競賽", "刺激複習"]
    },
    22: {
        "title": "對戰版整合 Google 雲端硬碟教材",
        "cat": "shooting_game",
        "summary": "輸入提示詞讓 AI 自動讀取雲端教材（如七年級資訊科技課本 PDF）與當週教學進度，自動精準命中命題範圍。",
        "tags": ["雲端整合", "課本PDF", "進度對齊"],
        "prompt": """@Google 雲端硬碟 讀取射擊遊戲/南一版_七年級科技(資訊科技).pdf，依照執行當天日期讀取當週單元/主題名稱與活動內容，並對照射擊遊戲資料夾中課本內容檔案，使用 @射擊遊戲對戰版 輸入對應課本內容生成對戰遊戲html檔案"""
    },
    23: {
        "title": "對戰版排程執行提示詞",
        "cat": "shooting_game",
        "summary": "設定自動排程！每週固定時間自動對照教學行事曆，將產出的對戰 html 儲存至輸出資料夾。",
        "tags": ["排程執行", "無人值守", "自動更新"],
        "prompt": """@Google 雲端硬碟 讀取射擊遊戲/南一版_七年級科技(資訊科技).pdf，依照執行當天日期讀取當週單元/主題名稱與活動內容，並對照射擊遊戲資料夾中課本內容檔案，使用 @射擊遊戲對戰版 輸入對應課本內容生成對戰遊戲html檔案，並且將生成的html檔案儲存在射擊遊戲/output資料夾中，檔案名稱為當日日期.html"""
    },
    24: {
        "title": "排程成果驗收與網頁即玩體驗",
        "cat": "shooting_game",
        "summary": "產出之 html 檔案為標準獨立純前端網頁，支援手機、平板、電子白板，免裝軟體隨開即玩。",
        "tags": ["零伺服器", "跨載具", "隨開即玩"]
    },
    25: {
        "title": "射擊遊戲小結與下一步：繪本生成器",
        "cat": "shooting_game",
        "summary": "從動態互動遊戲拓展至圖文並茂的跨領域創作，開啟「雲端上的繪本生成器」實作。",
        "tags": ["單元小結", "跨域整合"]
    },
    26: {
        "title": "雲端上的繪本生成器 - 總覽",
        "cat": "picture_book",
        "summary": "Google 體系 AI 工作流全新視野：只要一份大綱，自動產生風格一致、人物不走樣的精美繪本！",
        "tags": ["AI繪本", "皮克斯風格", "工作流"]
    },
    27: {
        "title": "繪本生成器兩大核心步驟",
        "cat": "picture_book",
        "summary": "步驟 1：建立專屬繪本 SKILL；步驟 2：排程自動執行生成與組裝。",
        "tags": ["兩大步驟", "標準SOP"]
    },
    28: {
        "title": "下載繪本製作 SKILL 與提示詞",
        "cat": "picture_book",
        "summary": "取得橘子老師獨家調校的「Notebook 繪本製作 SKILL」與提示詞模板。",
        "tags": ["提示詞模板", "SKILL下載"]
    },
    29: {
        "title": "設定角色故事與視覺錨定",
        "cat": "picture_book",
        "summary": "在提示詞中定義角色設定（外觀、服裝、五官特徵），確保後續 10 頁插圖角色始終一致。",
        "tags": ["角色設定", "一致性維持"]
    },
    30: {
        "title": "編排分頁分鏡腳本架構",
        "cat": "picture_book",
        "summary": "規劃繪本起承轉合，精確描述每一頁的故事情節、環境背景與構圖運鏡。",
        "tags": ["分鏡腳本", "視覺描述"]
    },
    31: {
        "title": "風格參數定義：皮克斯 3D 渲染",
        "cat": "picture_book",
        "summary": "指定繪本為 3D Pixar Animation 溫暖光影風格，兼具童趣與專業出版質感。",
        "tags": ["Pixar風", "3D渲染", "光影細節"]
    },
    32: {
        "title": "生成角色基準圖像 (Reference Anchor)",
        "cat": "picture_book",
        "summary": "先產出基準角色立繪（角色1、角色2），確認五官與辨識度特徵完美定案。",
        "tags": ["角色定稿", "錨定圖"]
    },
    33: {
        "title": "將腳本與角色設定存為 PDF",
        "cat": "picture_book",
        "summary": "將腳本文字與定稿角色圖像組合成一份 PDF 參考設定集，作為後續知識脈絡基礎。",
        "tags": ["設定文件", "PDF彙整"]
    },
    34: {
        "title": "滿版無字圖像生成策略",
        "cat": "picture_book",
        "summary": "提示詞重點：滿版構圖且畫面絕不出現文字，以便後續進行無損文字排版與雙語印製。",
        "tags": ["滿版無字", "純淨畫面"]
    },
    35: {
        "title": "依照設定文件逐頁生成繪本",
        "cat": "picture_book",
        "summary": "對照 PDF 設定文件，依照每頁腳本內容穩定輸出連續性場景與角色互動畫面。",
        "tags": ["連續鏡頭", "逐頁生成"]
    },
    36: {
        "title": "進階實作：將 SKILL 排程自動執行",
        "cat": "picture_book",
        "summary": "結合自動化排程引擎，讓繪本創作在背景定時產出，無需人工盯著畫面守候。",
        "tags": ["排程自動化", "後台生成"]
    },
    37: {
        "title": "下載繪本排程專屬提示詞",
        "cat": "picture_book",
        "summary": "下載「Notebook 繪本製作 排程」指令範本，建立一鍵排程腳本。",
        "tags": ["排程提示詞", "定時任務"]
    },
    38: {
        "title": "排程提示詞參數與環境配置",
        "cat": "picture_book",
        "summary": "設定目標輸出資料夾、命名規則與生成輪數，確保任務有條不紊完成。",
        "tags": ["任務設定", "路徑配置"]
    },
    39: {
        "title": "取得官方範例檔案進行驗證",
        "cat": "picture_book",
        "summary": "下載橘子老師提供的實測範例檔案，比對生成效果與標準成品的差異。",
        "tags": ["範例比對", "驗證確認"]
    },
    40: {
        "title": "上傳 PDF 至 Notebook 建立知識庫",
        "cat": "picture_book",
        "summary": "將完整的繪本設定與參考材料上傳至 Notebook，鎖定 AI 創作的上下文記憶。",
        "tags": ["知識上傳", "記憶鎖定"]
    },
    41: {
        "title": "全套繪本生成終極提示詞指令",
        "cat": "picture_book",
        "summary": "核心指令：依照資料來源生成 10 頁皮克斯風格圖像繪本故事，角色造型五官嚴格維持一致。",
        "tags": ["終極提示詞", "角色一致性", "10頁繪本"],
        "prompt": """依照資料來源生成10頁皮克斯風格圖像繪本故事，每頁故事內容依照腳本內容描述，畫面依照每頁描述畫面呈現，依照角色設定故事角色1，角色2，每一頁中角色造型五官須維持與設定一致"""
    },
    42: {
        "title": "生成畫面驗證與品質檢查",
        "cat": "picture_book",
        "summary": "檢查 10 頁插圖的色彩協調度、角色動態與敘事節奏，確保故事引人入勝。",
        "tags": ["品質檢驗", "色彩連貫"]
    },
    43: {
        "title": "繪本生成成果影片與電子書輸出",
        "cat": "picture_book",
        "summary": "整合翻頁電子書與 1.7 秒短影音摘要，快速將繪本成果分享給學生與家長觀看。",
        "tags": ["成果展示", "影音摘要", "數位出版"]
    },
    44: {
        "title": "繪本篇總結與銜接「會考出題大師」",
        "cat": "picture_book",
        "summary": "完成創意圖文創作後，進入教學最核心的評量環節——「會考出題大師」素養命題技能！",
        "tags": ["評量轉向", "出題大師"]
    },
    45: {
        "title": "會考出題大師 - 技能下載與安裝",
        "cat": "exam_master",
        "summary": "直接將 SKILL 壓縮檔安裝至 AI 助手，立即獲取頂級素養出題專家的所有思考鏈能力。",
        "tags": ["會考出題", "SKILL安裝", "免手動調教"]
    },
    46: {
        "title": "上傳題目截圖 → @呼叫SKILL",
        "cat": "exam_master",
        "summary": "只需將歷屆試題或模擬題截圖上傳，並輸入 @會考出題大師，AI 即刻解析題目背後的素養指標與解題陷阱。",
        "tags": ["圖片辨識", "截圖出題", "呼叫指令"]
    },
    47: {
        "title": "取得出題大師範例題庫與素材",
        "cat": "exam_master",
        "summary": "開啟官方提供的出題範例資料夾，練習各種題型（圖表題、實驗題、跨領域情境題）的改寫與變形。",
        "tags": ["範例題庫", "圖表分析"]
    },
    48: {
        "title": "類題變形與多元選項生成",
        "cat": "exam_master",
        "summary": "保留相同觀念但替換生活情境，自動生成 4 個具備合理誘答力（Distractor）的高品質選項。",
        "tags": ["類題變形", "誘答設計"]
    },
    49: {
        "title": "完整詳解與迷思概念剖析",
        "cat": "exam_master",
        "summary": "為每道題目產製「正解解析」與「常見學生迷思盲點提示」，方便教師課堂檢討與印發補充講義。",
        "tags": ["迷思概念", "詳解產製"]
    },
    50: {
        "title": "難易度梯度與素養指標對齊",
        "cat": "exam_master",
        "summary": "依據布魯姆認知歷程維度（記憶、理解、應用、分析、評鑑、創造）精確分級，確保試卷效度。",
        "tags": ["認知維度", "難易度梯度"]
    },
    51: {
        "title": "一鍵匯出 Word/PDF 考卷排版",
        "cat": "exam_master",
        "summary": "自動產生符合標準段考卷面配置的雙欄排版或 Google 表單線上測驗題目代碼。",
        "tags": ["考卷排版", "雙欄列印", "Google表單"]
    },
    52: {
        "title": "課程總結與未來 AI 教學願景",
        "cat": "exam_master",
        "summary": "橘子老師 AI 教學應用全流程總結：結合 Agent 代理人思維，讓科技真正成為教師的超強教學外腦！",
        "tags": ["課程總結", "AI教育願景", "致謝"]
    }
}

# Compile complete metadata
complete_data = {
    "title": "Ai在教學上的應用 - 橘子老師實戰講座",
    "author": "橘子老師",
    "updated": "2026年11月",
    "categories": categories,
    "slides": []
}

for s in slides:
    p = s["page"]
    meta = slide_meta.get(p, {
        "title": f"投影片第 {p} 頁",
        "cat": "intro",
        "summary": " | ".join(s["texts"][:3]),
        "tags": ["投影片"]
    })
    
    slide_obj = {
        "page": p,
        "title": meta["title"],
        "category": meta["cat"],
        "summary": meta["summary"],
        "tags": meta["tags"],
        "screenshot": f"assets/slides/slide_{p:02d}.png",
        "raw_texts": s["texts"],
        "links": s["links"],
        "prompt": meta.get("prompt", None)
    }
    complete_data["slides"].append(slide_obj)

with open("slides_categorized.json", "w", encoding="utf-8") as f:
    json.dump(complete_data, f, ensure_ascii=False, indent=2)

print("Saved slides_categorized.json successfully!")
