"""
模板分析模块
分析模板文件的视觉结构和样式信息
"""
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from backend.utils.logger import logger, log_processing
from backend.models.schemas import (
    TemplateStyle, SectionStyle, FontStyle, ParagraphStyle
)
from backend.services.file_parser import FileParser, ParsedContent, ParsedStyle
from backend.config import TEMPLATE_STYLE_MAP


@dataclass
class AnalyzedTemplate:
    """分析后的模板"""
    style: TemplateStyle
    section_order: List[str]
    raw_structure: Dict[str, Any]


class TemplateAnalyzer:
    """模板分析器"""
    
    def __init__(self):
        self.file_parser = FileParser()
    
    def analyze(self, template_path: Path) -> AnalyzedTemplate:
        """
        分析模板文件
        
        Args:
            template_path: 模板文件路径
            
        Returns:
            AnalyzedTemplate 对象
        """
        log_processing("TemplateAnalyzer", f"开始分析模板: {template_path.name}")
        
        # 解析文件
        content, style_info = self.file_parser.parse(template_path)
        
        # 分析样式
        template_style = self._analyze_style(style_info, content)
        
        # 分析章节顺序
        section_order = self._analyze_section_order(content.structure.get("sections", []))
        
        # 构建原始结构
        raw_structure = {
            "sections": content.structure.get("sections", []),
            "fonts": style_info.fonts,
            "layout": style_info.layout
        }
        
        result = AnalyzedTemplate(
            style=template_style,
            section_order=section_order,
            raw_structure=raw_structure
        )
        
        log_processing("TemplateAnalyzer", "模板分析完成", {
            "sections": len(section_order),
            "fonts": len(style_info.fonts)
        })
        
        return result
    
    def _analyze_style(self, style_info: ParsedStyle, content: ParsedContent) -> TemplateStyle:
        """分析样式信息"""
        
        # 确定主要字体
        main_font = self._determine_main_font(style_info.fonts)
        
        # 创建默认字体样式
        default_font = FontStyle(
            name=main_font.get("name", "Times New Roman"),
            size=main_font.get("size", 11),
            bold=main_font.get("bold", False),
            italic=main_font.get("italic", False)
        )
        
        # 分析各章节样式
        section_styles = {}
        for section in content.structure.get("sections", []):
            section_name = section.get("name", "")
            if section_name:
                section_styles[section_name] = self._create_section_style(
                    section, style_info, default_font
                )
        
        # 创建header样式（通常是最大字体）
        header_font = self._find_largest_font(style_info.fonts)
        header_style = SectionStyle(
            title_font=FontStyle(
                name=header_font.get("name", default_font.name),
                size=header_font.get("size", 18),
                bold=True
            ),
            title_paragraph=ParagraphStyle(alignment="center"),
            has_separator=False
        )
        
        # 创建contact样式
        contact_style = SectionStyle(
            content_font=FontStyle(
                name=default_font.name,
                size=10
            ),
            content_paragraph=ParagraphStyle(alignment="center"),
            has_separator=False
        )
        
        return TemplateStyle(
            page_margins={"top": 0.5, "bottom": 0.5, "left": 0.5, "right": 0.5},
            header_style=header_style,
            contact_style=contact_style,
            section_styles=section_styles,
            default_font=default_font,
            column_layout=1
        )
    
    def _determine_main_font(self, fonts: List[Dict]) -> Dict:
        """确定主要字体（出现最多的字体）"""
        if not fonts:
            return {"name": "Times New Roman", "size": 11}
        
        # 简单统计，返回第一个有效字体
        for font in fonts:
            if font.get("name") and font.get("size"):
                return font
        
        return fonts[0] if fonts else {"name": "Times New Roman", "size": 11}
    
    def _find_largest_font(self, fonts: List[Dict]) -> Dict:
        """找到最大的字体（用于标题）"""
        if not fonts:
            return {"name": "Times New Roman", "size": 18}
        
        largest = max(fonts, key=lambda f: f.get("size", 0), default=fonts[0])
        return largest
    
    def _create_section_style(
        self, 
        section: Dict, 
        style_info: ParsedStyle,
        default_font: FontStyle
    ) -> SectionStyle:
        """为章节创建样式"""
        
        # 基于预定义模板样式
        preset = TEMPLATE_STYLE_MAP.get("section_title", {})
        
        title_font = FontStyle(
            name=preset.get("font_name", default_font.name),
            size=preset.get("font_size", 12),
            bold=preset.get("bold", True),
            underline=preset.get("underline", False)
        )
        
        content_font = FontStyle(
            name=TEMPLATE_STYLE_MAP.get("body", {}).get("font_name", default_font.name),
            size=TEMPLATE_STYLE_MAP.get("body", {}).get("font_size", 10)
        )
        
        return SectionStyle(
            title_font=title_font,
            title_paragraph=ParagraphStyle(
                alignment="left",
                space_before=6,
                space_after=3
            ),
            content_font=content_font,
            content_paragraph=ParagraphStyle(
                alignment="left",
                line_spacing=1.0
            ),
            bullet_style="•",
            has_separator=True,
            separator_style="line"
        )
    
    def _analyze_section_order(self, sections: List[Dict]) -> List[str]:
        """分析章节顺序"""
        order = []
        for section in sections:
            name = section.get("name", "")
            if name and name not in order:
                order.append(name)
        
        # 如果没有检测到章节，使用默认顺序
        if not order:
            order = [
                "header",
                "contact", 
                "education",
                "skills",
                "experience",
                "projects",
                "leadership"
            ]
        
        return order
    
    def get_style_for_section(
        self, 
        template: AnalyzedTemplate, 
        section_name: str
    ) -> SectionStyle:
        """获取指定章节的样式"""
        return template.style.section_styles.get(
            section_name,
            SectionStyle()  # 默认样式
        )
