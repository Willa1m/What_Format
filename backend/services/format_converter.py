"""
格式转换模块
将提取的内容映射到模板样式
"""
from typing import Dict, List, Any

from backend.models.schemas import ResumeContent, TemplateStyle
from backend.utils.logger import log_processing


class FormatConverter:
    """格式转换器"""
    
    def __init__(self):
        # 章节标题映射
        self.section_titles = {
            "education": "EDUCATION",
            "experience": "PROFESSIONAL EXPERIENCE",
            "projects": "ACADEMIC PROJECTS",
            "skills": "OTHER SKILLS",
            "summary": "PROFILE",
            "awards": "HONORS & AWARDS",
            "certifications": "CERTIFICATIONS",
            "activities": "ACTIVITIES",
        }
    
    def convert(self, content: ResumeContent, style: TemplateStyle = None) -> Dict[str, Any]:
        """
        将内容转换为格式化的输出结构
        
        Args:
            content: 简历内容
            style: 模板样式（可选）
            
        Returns:
            格式化的数据结构
        """
        log_processing("FormatConverter", "开始格式转换")
        
        result = {
            "header": {
                "name": content.contact.name,
            },
            "contact": {
                "email": content.contact.email,
                "phone": content.contact.phone,
                "address": content.contact.address,
                "linkedin": content.contact.linkedin,
                "github": content.contact.github,
            },
            "sections": []
        }
        
        # 添加教育
        if content.education:
            result["sections"].append({
                "type": "education",
                "title": self.section_titles.get("education", "EDUCATION"),
                "items": self._format_education(content.education)
            })
        
        # 添加经历
        if content.experience:
            result["sections"].append({
                "type": "experience",
                "title": self.section_titles.get("experience", "EXPERIENCE"),
                "items": self._format_experience(content.experience)
            })
        
        # 添加项目
        if content.projects:
            result["sections"].append({
                "type": "projects",
                "title": self.section_titles.get("projects", "PROJECTS"),
                "items": self._format_projects(content.projects)
            })
        
        # 添加技能
        if content.skills:
            result["sections"].append({
                "type": "skills",
                "title": self.section_titles.get("skills", "SKILLS"),
                "items": self._format_skills(content.skills)
            })
        
        log_processing("FormatConverter", f"转换完成: {len(result['sections'])} 个章节")
        return result
    
    def _format_education(self, education_items: List) -> List[Dict]:
        """格式化教育条目"""
        formatted = []
        for edu in education_items:
            formatted.append({
                "institution": edu.institution,
                "location": edu.location,
                "degree": edu.degree,
                "dates": edu.end_date,
                "gpa": edu.gpa,
                "coursework": edu.coursework,
                "honors": edu.honors,
            })
        return formatted
    
    def _format_experience(self, experience_items: List) -> List[Dict]:
        """格式化经历条目"""
        formatted = []
        for exp in experience_items:
            formatted.append({
                "organization": exp.organization,
                "location": exp.location,
                "title": exp.title,
                "dates": exp.end_date,
                "descriptions": exp.descriptions,
            })
        return formatted
    
    def _format_projects(self, project_items: List) -> List[Dict]:
        """格式化项目条目"""
        formatted = []
        for proj in project_items:
            formatted.append({
                "name": proj.organization,  # 项目名称
                "technology": proj.location,  # 技术栈
                "descriptions": proj.descriptions,
            })
        return formatted
    
    def _format_skills(self, skill_items: List) -> List[Dict]:
        """格式化技能条目"""
        formatted = []
        for skill in skill_items:
            formatted.append({
                "category": skill.category,
                "skills": skill.skills,
            })
        return formatted
