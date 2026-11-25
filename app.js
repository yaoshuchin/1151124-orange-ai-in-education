// Ai在教學上的應用 - 橘子老師實戰講座 數位學習平台前端互動邏輯

document.addEventListener('DOMContentLoaded', () => {
  const data = window.DECK_DATA;
  if (!data) {
    console.error("DECK_DATA not loaded!");
    return;
  }

  // --- 1. 密碼存取保護閘門 (密碼設定: nato) ---
  const passwordGate = document.getElementById('passwordGateModal');
  const passwordInput = document.getElementById('passwordInput');
  const btnUnlock = document.getElementById('btnUnlock');
  const passwordError = document.getElementById('passwordError');
  const passwordCard = document.querySelector('.password-card');
  const btnLockSite = document.getElementById('btnLockSite');

  function checkAuth() {
    const isAuthed = localStorage.getItem('orange_ai_auth') === 'granted';
    if (isAuthed) {
      passwordGate.classList.add('hidden');
    } else {
      passwordGate.classList.remove('hidden');
      setTimeout(() => passwordInput && passwordInput.focus(), 150);
    }
  }

  function handleUnlock() {
    const val = (passwordInput.value || '').trim().toLowerCase();
    if (val === 'nato') {
      localStorage.setItem('orange_ai_auth', 'granted');
      passwordGate.classList.add('hidden');
      passwordError.style.display = 'none';
      showToast('🎉 密碼驗證成功，歡迎進入橘子老師 AI 教學平台！');
    } else {
      passwordError.style.display = 'block';
      passwordCard.classList.remove('shake');
      void passwordCard.offsetWidth; // trigger reflow
      passwordCard.classList.add('shake');
      passwordInput.select();
    }
  }

  if (btnUnlock) btnUnlock.addEventListener('click', handleUnlock);
  if (passwordInput) {
    passwordInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleUnlock();
    });
  }
  if (btnLockSite) {
    btnLockSite.addEventListener('click', () => {
      localStorage.removeItem('orange_ai_auth');
      passwordInput.value = '';
      passwordError.style.display = 'none';
      passwordGate.classList.remove('hidden');
      passwordInput.focus();
      showToast('🔒 系統已安全鎖定');
    });
  }
  checkAuth();

  // --- 2. 字型大小切換 (中 / 大 / 特大) ---
  const fontButtons = document.querySelectorAll('[data-font-val]');
  function setFontSize(fontVal) {
    document.body.setAttribute('data-font', fontVal);
    localStorage.setItem('orange_ai_font', fontVal);
    fontButtons.forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-font-val') === fontVal);
    });
  }
  const savedFont = localStorage.getItem('orange_ai_font') || 'medium';
  setFontSize(savedFont);

  fontButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      setFontSize(btn.getAttribute('data-font-val'));
    });
  });

  // --- 3. 布景主題切換 (淺 / 深 / 綠 / 藍) ---
  const themeButtons = document.querySelectorAll('[data-theme-val]');
  function setTheme(themeVal) {
    document.body.setAttribute('data-theme', themeVal);
    localStorage.setItem('orange_ai_theme', themeVal);
    themeButtons.forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-theme-val') === themeVal);
    });
  }
  const savedTheme = localStorage.getItem('orange_ai_theme') || 'light';
  setTheme(savedTheme);

  themeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      setTheme(btn.getAttribute('data-theme-val'));
    });
  });

  // --- 4. 分頁標籤切換 (Tabs) ---
  let currentTab = 'all';
  const tabButtons = document.querySelectorAll('.tab-btn');
  const slidesGrid = document.getElementById('slidesGrid');
  const resourceCenter = document.getElementById('resourceCenter');
  const promptsCenter = document.getElementById('promptsCenter');
  const searchInput = document.getElementById('searchInput');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTab = btn.getAttribute('data-tab');
      renderView();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      renderView();
    });
  }

  // --- 5. 渲染視圖與篩選 ---
  function renderView() {
    const query = (searchInput.value || '').trim().toLowerCase();

    // 處理特殊獨立分頁：教學資源總庫
    if (currentTab === 'resources') {
      slidesGrid.style.display = 'none';
      if (promptsCenter) promptsCenter.style.display = 'none';
      if (resourceCenter) resourceCenter.style.display = 'block';
      return;
    }

    // 處理特殊獨立分頁：提示詞總庫
    if (currentTab === 'prompts') {
      slidesGrid.style.display = 'none';
      if (resourceCenter) resourceCenter.style.display = 'none';
      if (promptsCenter) promptsCenter.style.display = 'block';
      return;
    }

    // 投影片卡片網格視圖
    if (resourceCenter) resourceCenter.style.display = 'none';
    if (promptsCenter) promptsCenter.style.display = 'none';
    slidesGrid.style.display = 'grid';

    const filtered = data.slides.filter(slide => {
      const matchTab = currentTab === 'all' || slide.category === currentTab;
      if (!matchTab) return false;

      if (!query) return true;
      const titleMatch = slide.title.toLowerCase().includes(query);
      const summaryMatch = slide.summary.toLowerCase().includes(query);
      const tagMatch = slide.tags.some(t => t.toLowerCase().includes(query));
      const pageMatch = String(slide.page) === query || `slide ${slide.page}`.includes(query);
      const rawMatch = slide.raw_texts.some(t => t.toLowerCase().includes(query));
      return titleMatch || summaryMatch || tagMatch || pageMatch || rawMatch;
    });

    if (filtered.length === 0) {
      slidesGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: var(--text-secondary);">
          <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.4;"></i>
          <h3>找不到符合「${query}」的教學內容</h3>
          <p style="margin-top: 0.5rem;">請嘗試不同關鍵字，或切換上方分頁標籤檢視所有資料。</p>
        </div>
      `;
      return;
    }

    slidesGrid.innerHTML = filtered.map(slide => createSlideCardHtml(slide)).join('');
    bindCardEvents();
  }

  function createSlideCardHtml(slide) {
    const categoryNameMap = {
      intro: "課程導言",
      voice_minutes: "語音會議紀錄",
      shooting_game: "複習射擊遊戲",
      picture_book: "雲端繪本生成",
      exam_master: "會考出題大師"
    };

    const promptHtml = slide.prompt ? `
      <div class="prompt-box">
        <div class="prompt-box-header">
          <span class="prompt-box-title"><i class="fas fa-terminal"></i> 實戰指令 Prompt</span>
          <button class="btn-copy-sm" data-copy-text="${encodeURIComponent(slide.prompt)}">
            <i class="far fa-copy"></i> 複製指令
          </button>
        </div>
        <div class="prompt-code">${escapeHtml(slide.prompt)}</div>
      </div>
    ` : '';

    const linksHtml = slide.links && slide.links.length > 0 ? `
      <div class="slide-links">
        ${slide.links.map(l => `
          <a href="${l.href}" target="_blank" rel="noopener noreferrer" class="resource-btn">
            <i class="fas fa-cloud-download-alt"></i> ${escapeHtml(l.text || '下載資源')}
          </a>
        `).join('')}
      </div>
    ` : '';

    return `
      <div class="slide-card" data-page="${slide.page}">
        <div class="slide-thumbnail-wrapper" onclick="openLightbox(${slide.page})">
          <span class="slide-page-badge">第 ${slide.page.toString().padStart(2, '0')} / 52 頁</span>
          <img src="${slide.screenshot}" alt="${escapeHtml(slide.title)}" class="slide-thumbnail" loading="lazy">
          <div class="slide-zoom-hint">
            <i class="fas fa-search-plus"></i>
          </div>
        </div>
        <div class="slide-body">
          <div class="slide-meta-top">
            <span class="category-tag">${categoryNameMap[slide.category] || '教材投影片'}</span>
            <div class="slide-tags">
              ${slide.tags.map(t => `<span class="tag-pill">#${escapeHtml(t)}</span>`).join('')}
            </div>
          </div>
          <h3 class="slide-title">${escapeHtml(slide.title)}</h3>
          <p class="slide-summary">${escapeHtml(slide.summary)}</p>
          ${promptHtml}
          ${linksHtml}
        </div>
      </div>
    `;
  }

  function bindCardEvents() {
    document.querySelectorAll('[data-copy-text]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const text = decodeURIComponent(btn.getAttribute('data-copy-text'));
        copyToClipboard(text);
      });
    });
  }

  // --- 6. 剪貼簿複製與 Toast ---
  function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        showToast('📋 已成功複製提示詞指令到剪貼簿！');
      }).catch(() => fallbackCopy(text));
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      document.execCommand('copy');
      showToast('📋 已成功複製提示詞指令到剪貼簿！');
    } catch (err) {
      showToast('❌ 複製失敗，請手動圈選複製');
    }
    document.body.removeChild(ta);
  }

  const toastNotice = document.getElementById('toastNotice');
  const toastMessage = document.getElementById('toastMessage');
  let toastTimer = null;
  function showToast(msg) {
    if (!toastNotice) return;
    toastMessage.textContent = msg;
    toastNotice.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastNotice.classList.remove('show');
    }, 2500);
  }
  window.showToast = showToast;
  window.copyToClipboard = copyToClipboard;

  // --- 7. 全螢幕投影片燈箱檢視器 (Lightbox / Deck Player) ---
  let currentLightboxPage = 1;
  const lightboxModal = document.getElementById('lightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxPageIndicator = document.getElementById('lightboxPageIndicator');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const btnLightboxPrev = document.getElementById('btnLightboxPrev');
  const btnLightboxNext = document.getElementById('btnLightboxNext');
  const btnLightboxClose = document.getElementById('btnLightboxClose');

  function openLightbox(page) {
    currentLightboxPage = page;
    updateLightbox();
    lightboxModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightboxModal.classList.remove('active');
    document.body.style.overflow = '';
  }

  function updateLightbox() {
    const slide = data.slides.find(s => s.page === currentLightboxPage);
    if (!slide) return;
    lightboxImg.src = slide.screenshot;
    lightboxPageIndicator.textContent = `第 ${slide.page} / 52 頁`;
    lightboxTitle.textContent = slide.title;
  }

  if (btnLightboxClose) btnLightboxClose.addEventListener('click', closeLightbox);
  if (btnLightboxPrev) {
    btnLightboxPrev.addEventListener('click', () => {
      if (currentLightboxPage > 1) {
        currentLightboxPage--;
        updateLightbox();
      }
    });
  }
  if (btnLightboxNext) {
    btnLightboxNext.addEventListener('click', () => {
      if (currentLightboxPage < 52) {
        currentLightboxPage++;
        updateLightbox();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (!lightboxModal.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft' && currentLightboxPage > 1) {
      currentLightboxPage--;
      updateLightbox();
    }
    if (e.key === 'ArrowRight' && currentLightboxPage < 52) {
      currentLightboxPage++;
      updateLightbox();
    }
  });

  window.openLightbox = openLightbox;

  // 快捷進入播放模式按鈕
  const btnStartPresentation = document.getElementById('btnStartPresentation');
  if (btnStartPresentation) {
    btnStartPresentation.addEventListener('click', () => {
      openLightbox(1);
    });
  }

  // --- 8. 工具函數 ---
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // 初始渲染
  renderView();
});
