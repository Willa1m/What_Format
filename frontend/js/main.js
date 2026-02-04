/**
 * WhatFormat Global Logic
 * Handles Language Switching, Navigation State, API base, and common UI
 */

const i18n = {
    en: {
        nav: {
            home: "Home",
            format: "Format",
            about: "About Us"
        },
        home: {
            title: "FORMAT_REDEFINED",
            subtitle: "The ultimate solution for document intelligence.",
            cta: "START CONVERTING",
            features: ["AI Powered", "Secure", "Lightning Fast"]
        },
        convert: {
            title: "INTERACTIVE_CONVERSION",
            select: "Select Document",
            upload: "Upload Document",
            convert: "Convert Now",
            converting: "Processing...",
            download: "Download Result",
            formats: {
                resume: "Resume",
                cover_letter: "Cover Letter"
            },
            inputFormats: "Input formats",
            outputFormats: "Output format",
            metaLoading: "Loading API metadata...",
            metaFailed: "Failed to load API metadata",
            templatesLabel: "Templates",
            recipientName: "Recipient Name",
            recipientTitle: "Recipient Title",
            recipientCompany: "Recipient Company",
            recipientLocation: "Recipient Location",
            errors: {
                noFile: "Please select a file first.",
                failed: "Conversion failed.",
                network: "Network error."
            }
        },
        about: {
            title: "ABOUT_US",
            desc: "We are a team of engineers dedicated to simplifying file complexities through elegant code and immersive design.",
            mission: "Our Mission: To make format conversion an art form."
        }
    },
    zh: {
        nav: {
            home: "首页",
            format: "格式转换",
            about: "关于我们"
        },
        home: {
            title: "格式_重定义",
            subtitle: "智能文档处理的终极方案。",
            cta: "开始转换",
            features: ["AI 驱动", "安全隐私", "极速处理"]
        },
        convert: {
            title: "交互式转换",
            select: "选择文档类型",
            upload: "上传文档",
            convert: "开始转换",
            converting: "处理中...",
            download: "下载结果",
            formats: {
                resume: "简历",
                cover_letter: "求职信"
            },
            inputFormats: "输入格式",
            outputFormats: "输出格式",
            metaLoading: "正在加载接口信息...",
            metaFailed: "接口信息加载失败",
            templatesLabel: "模板",
            recipientName: "收件人姓名",
            recipientTitle: "收件人职位",
            recipientCompany: "收件人公司",
            recipientLocation: "收件人地址",
            errors: {
                noFile: "请先选择文件。",
                failed: "转换失败。",
                network: "网络错误。"
            }
        },
        about: {
            title: "关于我们",
            desc: "我们是一群致力于通过优雅的代码和沉浸式设计简化文件复杂性的工程师团队。",
            mission: "使命：让格式转换成为一门艺术。"
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
        
        // Update Lang Button Text
        const langBtn = document.getElementById('lang-toggle');
        if(langBtn) langBtn.textContent = this.lang === 'en' ? 'CN' : 'EN';
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
