/**
 * WhatFormat Global Logic
 * Handles Language Switching, Navigation State, API base, and common UI
 */

const i18n = {
    en: {
        nav: {
            home: "Home",
            format: "Format",
            about: "About"
        },
        home: {
            tagline: "Document Intelligence Redefined",
            slogan1: "ORDER",
            slogan2: "FROM",
            slogan3: "CHAOS",
            cta: "Format Now",
            status: "System Status",
            operational: "Operational",
            scroll: "Scroll for more"
        },
        convert: {
            title: "CONVERT",
            subtitle: "Select document type",
            resume: "Resume",
            coverLetter: "Cover Letter",
            dropText: "Drop file or Click",
            convertBtn: "Convert",
            status: "STATUS",
            processing: "PROCESSING",
            uploading: "UPLOADING...",
            completed: "COMPLETED",
            failed: "FAILED",
            download: "Download Result",
            footer: "Template Visualization"
        },
        about: {
            title1: "Our",
            title2: "Mission",
            quote: '"We believe that the <span class="text-white font-medium">form of information</span> is as important as the information itself. We are redefining document intelligence through <span class="text-white font-medium">pure aesthetics</span> and code."',
            stat1: "Accuracy",
            stat2: "Processing",
            stat3: "Uptime",
            footer1: "Est. 2026",
            footer2: "Version 2.0"
        }
    },
    zh: {
        nav: {
            home: "首页",
            format: "格式转换",
            about: "关于"
        },
        home: {
            tagline: "重新定义文档智能",
            slogan1: "秩序",
            slogan2: "源于",
            slogan3: "混沌",
            cta: "立即转换",
            status: "系统状态",
            operational: "运行正常",
            scroll: "向下滚动查看更多"
        },
        convert: {
            title: "格式转换",
            subtitle: "选择文档类型",
            resume: "简历",
            coverLetter: "求职信",
            dropText: "拖放文件或点击上传",
            convertBtn: "开始转换",
            status: "状态",
            processing: "处理中",
            uploading: "上传中...",
            completed: "已完成",
            failed: "失败",
            download: "下载结果",
            footer: "模板可视化"
        },
        about: {
            title1: "我们的",
            title2: "使命",
            quote: '"我们相信<span class="text-white font-medium">信息的形式</span>与信息本身同样重要。我们正在通过<span class="text-white font-medium">纯粹的美学</span>和代码重新定义文档智能。"',
            stat1: "准确率",
            stat2: "处理速度",
            stat3: "在线时间",
            footer1: "创立于 2026",
            footer2: "版本 2.0"
        }
    }
};

function resolveApiBase(rawBase) {
    const fallback = "/api";
    const base = rawBase && String(rawBase).trim() ? String(rawBase).trim() : fallback;
    try {
        const url = new URL(base, window.location.origin);
        return url.toString().replace(/\/$/, "");
    } catch {
        return `${window.location.origin}${fallback}`;
    }
}

window.WF_I18N = i18n;
const API_BASE = resolveApiBase(window.WF_API_BASE);
window.WF_API_BASE_RESOLVED = API_BASE;

async function fetchJson(url) {
    const response = await fetch(url, { headers: { "Accept": "application/json" } });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        const message = data.detail || "Request failed";
        throw new Error(message);
    }
    return data;
}

class AppState {
    constructor() {
        this.lang = localStorage.getItem('wf-lang') || 'en';
        this.init();
    }

    init() {
        this.updateTexts();
        this.bindEvents();
        this.updateActiveNav();
        this.loadApiMeta();
    }

    toggleLang() {
        this.lang = this.lang === 'en' ? 'zh' : 'en';
        localStorage.setItem('wf-lang', this.lang);
        this.updateTexts();
        this.loadApiMeta();
        // Dispatch event for other components (like 3D scene) to react
        window.dispatchEvent(new CustomEvent('langChange', { detail: this.lang }));
    }

    updateTexts() {
        const texts = i18n[this.lang];
        
        // Handle regular text translations
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            const keys = key.split('.');
            let value = texts;
            keys.forEach(k => value = value ? value[k] : '');
            if (value) {
                if(el.tagName === 'INPUT' && el.type === 'submit') el.value = value;
                else if(el.hasAttribute('placeholder')) el.placeholder = value;
                else el.textContent = value;
            }
        });
        
        // Handle HTML translations (for content with markup)
        document.querySelectorAll('[data-i18n-html]').forEach(el => {
            const key = el.dataset.i18nHtml;
            const keys = key.split('.');
            let value = texts;
            keys.forEach(k => value = value ? value[k] : '');
            if (value) {
                el.innerHTML = value;
            }
        });
        
        // Update Lang Button Text - Show the language to switch TO
        const langBtn = document.getElementById('lang-toggle');
        if(langBtn) langBtn.textContent = this.lang === 'en' ? '中文' : 'EN';
    }

    bindEvents() {
        const langBtn = document.getElementById('lang-toggle');
        if(langBtn) {
            langBtn.onclick = () => this.toggleLang();
        }
    }

    updateActiveNav() {
        const path = window.location.pathname;
        const links = document.querySelectorAll('nav a');
        const current = path.endsWith("/") ? `${path}index.html` : path;
        links.forEach(link => {
            const href = link.getAttribute('href');
            const isRootIndex = path === '/' && href === 'index.html';
            const isMatch = current.endsWith(href);
            if (isRootIndex || isMatch) {
                link.classList.add('text-green-400');
            } else {
                link.classList.remove('text-green-400');
            }
        });
    }

    async loadApiMeta() {
        const statusEl = document.getElementById('api-meta-status');
        if (statusEl) statusEl.textContent = i18n[this.lang].convert.metaLoading;

        try {
            const [formats, templates] = await Promise.all([
                fetchJson(`${API_BASE}/supported-formats`),
                fetchJson(`${API_BASE}/templates/info`)
            ]);

            const inputEl = document.getElementById('supported-input');
            const outputEl = document.getElementById('supported-output');
            const resumeTemplateEl = document.getElementById('template-resume-name');
            const coverTemplateEl = document.getElementById('template-cover-name');

            if (inputEl) inputEl.textContent = (formats.input_formats || []).join(', ');
            if (outputEl) outputEl.textContent = (formats.output_formats || []).join(', ');
            if (resumeTemplateEl) resumeTemplateEl.textContent = templates.resume?.name || '-';
            if (coverTemplateEl) coverTemplateEl.textContent = templates.cover_letter?.name || '-';

            if (statusEl) statusEl.textContent = "";
        } catch (err) {
            if (statusEl) statusEl.textContent = i18n[this.lang].convert.metaFailed;
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AppState();
});
