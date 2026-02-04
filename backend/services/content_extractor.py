"""
内容提取模块
从解析后的文本中提取结构化的简历内容
"""
import re
from pathlib import Path
from typing import List, Optional

from backend.models.schemas import (
    ResumeContent, ContactInfo, EducationItem, 
    ExperienceItem, SkillCategory
)
from backend.services.file_parser import FileParser
from backend.utils.logger import log_processing


class ContentExtractor:
    """内容提取器"""
    
    def __init__(self):
        self.file_parser = FileParser()
        
        # 日期模式
        self.date_patterns = [
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{4}',
            r'\d{1,2}/\d{4}',
            r'\d{4}\s*[-–]\s*(Present|Current|Now|\d{4})',
            r'(Spring|Summer|Fall|Winter)\s*\d{4}',
            r'\d{4}年\d{1,2}月',
        ]
        
        # 联系方式模式
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.phone_pattern = re.compile(r'[\+]?[\d\-\(\)\s]{7,20}')
        self.linkedin_pattern = re.compile(r'linkedin\.com/in/[\w\-]+', re.I)
        self.github_pattern = re.compile(r'github\.com/[\w\-]+', re.I)
    
    def extract(self, file_path: Path) -> ResumeContent:
        """
        从文件提取结构化简历内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            结构化的简历内容
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        log_processing("ContentExtractor", f"提取内容: {file_path.name}")
        
        # 解析文件
        parsed, _ = self.file_parser.parse(file_path)
        
        # 提取各部分内容
        content = ResumeContent()
        content.raw_text = parsed.text
        content.contact = self._extract_contact_info(parsed.paragraphs, parsed.sections)
        content.education = self._extract_education(parsed.sections.get('education', []))
        content.experience = self._extract_experiences(parsed.sections.get('experience', []))
        content.projects = self._extract_experiences(parsed.sections.get('projects', []))
        content.skills = self._extract_skills(parsed.sections.get('skills', []))
        
        return content
    
    def _extract_contact_info(self, paragraphs: List[str], sections: dict) -> ContactInfo:
        """提取联系信息"""
        contact = ContactInfo()
        
        # 从前几行提取姓名和联系方式
        header_lines = paragraphs[:10] if len(paragraphs) > 10 else paragraphs
        
        for i, line in enumerate(header_lines):
            # 检查是否是章节标题
            if any(kw in line.lower() for kw in ['education', 'experience', 'skills', 'project']):
                continue
            
            # 提取邮箱
            email_match = self.email_pattern.search(line)
            if email_match and not contact.email:
                contact.email = email_match.group()
            
            # 提取电话
            phone_match = self.phone_pattern.search(line)
            if phone_match and not contact.phone:
                phone = phone_match.group().strip()
                # 验证是否是有效电话
                digits = re.sub(r'\D', '', phone)
                if len(digits) >= 7:
                    contact.phone = phone
            
            # 提取LinkedIn
            linkedin_match = self.linkedin_pattern.search(line)
            if linkedin_match:
                contact.linkedin = linkedin_match.group()
            
            # 提取GitHub
            github_match = self.github_pattern.search(line)
            if github_match:
                contact.github = github_match.group()
            
            # 第一行通常是姓名
            if i == 0 and not contact.name:
                # 清理姓名
                name = line.strip()
                # 移除 "Resume" 后缀
                name = re.sub(r"'?s?\s*Resume$", "", name, flags=re.I).strip()
                # 检查是否看起来像姓名
                if len(name) < 50 and '@' not in name and not any(c.isdigit() for c in name[:5]):
                    contact.name = name
        
        return contact
    
    def _extract_education(self, section_lines: List[str]) -> List[EducationItem]:
        """提取教育经历"""
        education_items = []
        
        if not section_lines:
            return education_items
        
        current_item = None
        
        for line in section_lines:
            line = line.strip()
            if not line:
                continue
            
            # 跳过章节标题
            if any(kw in line.lower() for kw in ['education', 'educational background']):
                continue
            
            # 检查是否包含日期（通常是新条目的开始）
            has_date = any(re.search(pattern, line, re.I) for pattern in self.date_patterns)
            
            # 检查是否是大学名称
            is_university = any(kw in line.lower() for kw in [
                'university', 'college', 'institute', 'school', 'academy',
                '大学', '学院', '学校'
            ])
            
            if is_university or has_date:
                # 保存之前的条目
                if current_item:
                    education_items.append(current_item)
                
                current_item = EducationItem()
                
                # 解析行内容
                # 尝试提取日期
                for pattern in self.date_patterns:
                    date_match = re.search(pattern, line, re.I)
                    if date_match:
                        current_item.end_date = date_match.group()
                        break
                
                # 提取学校名称
                # 移除日期部分
                name_part = line
                for pattern in self.date_patterns:
                    name_part = re.sub(pattern, '', name_part, flags=re.I)
                
                # 分割学校和位置
                parts = re.split(r'\s*[|,]\s*', name_part.strip())
                if parts:
                    current_item.institution = parts[0].strip()
                    if len(parts) > 1:
                        current_item.location = parts[-1].strip()
            
            elif current_item:
                line_lower = line.lower()
                
                # 检查是否是学位
                if any(kw in line_lower for kw in ['bachelor', 'master', 'phd', 'b.a.', 'b.s.', 'm.s.', '本科', '硕士', '博士']):
                    current_item.degree = line
                
                # 检查是否是GPA
                gpa_match = re.search(r'GPA[:\s]*(\d+\.?\d*)', line, re.I)
                if gpa_match:
                    current_item.gpa = gpa_match.group(1)
                
                # 检查是否是课程
                if 'course' in line_lower or '课程' in line_lower:
                    courses = re.sub(r'(relevant\s+)?courses?[:\s]*', '', line, flags=re.I)
                    current_item.coursework = [c.strip() for c in courses.split(',') if c.strip()]
        
        # 添加最后一个条目
        if current_item:
            education_items.append(current_item)
        
        return education_items
    
    def _extract_experiences(self, section_lines: List[str]) -> List[ExperienceItem]:
        """提取工作/项目经历"""
        experience_items = []
        
        if not section_lines:
            return experience_items
        
        current_item = None
        
        for line in section_lines:
            line = line.strip()
            if not line:
                continue
            
            # 跳过章节标题
            skip_keywords = ['experience', 'professional', 'work', 'projects', 'project experience',
                           '工作经历', '项目经历', '实习经历']
            if any(line.lower().strip() == kw for kw in skip_keywords):
                continue
            
            # 检查是否包含日期
            has_date = any(re.search(pattern, line, re.I) for pattern in self.date_patterns)
            
            # 检查是否是新条目的开始（包含组织名称特征）
            is_org_line = any(kw in line.lower() for kw in [
                'inc', 'corp', 'llc', 'company', 'lab', 'research', 'intern',
                '公司', '集团', '研究', '实验室'
            ]) or '|' in line
            
            if has_date or is_org_line:
                # 保存之前的条目
                if current_item:
                    experience_items.append(current_item)
                
                current_item = ExperienceItem()
                
                # 解析行
                # 提取日期
                for pattern in self.date_patterns:
                    date_match = re.search(pattern, line, re.I)
                    if date_match:
                        current_item.end_date = date_match.group()
                        break
                
                # 移除日期，解析剩余部分
                remaining = line
                for pattern in self.date_patterns:
                    remaining = re.sub(pattern, '', remaining, flags=re.I)
                
                # 按分隔符分割
                parts = re.split(r'\s*[|]\s*', remaining.strip())
                parts = [p.strip() for p in parts if p.strip()]
                
                if len(parts) >= 2:
                    current_item.organization = parts[0]
                    # 检查是否有位置信息
                    for part in parts[1:]:
                        if any(loc in part.lower() for loc in ['ma', 'ny', 'ca', 'tx', 'china', '北京', '上海']):
                            current_item.location = part
                        else:
                            current_item.title = part
                elif len(parts) == 1:
                    current_item.organization = parts[0]
            
            elif current_item:
                # 检查是否是职位行
                if not current_item.title and len(line) < 80:
                    title_keywords = ['intern', 'engineer', 'analyst', 'assistant', 'manager', 'developer',
                                     '实习', '工程师', '分析师', '助理', '经理']
                    if any(kw in line.lower() for kw in title_keywords):
                        current_item.title = line
                        continue
                
                # 作为描述添加
                desc = line.strip()
                # 移除已有的项目符号
                desc = re.sub(r'^[•\-\*]\s*', '', desc)
                if desc and len(desc) > 5:
                    current_item.descriptions.append(desc)
        
        # 添加最后一个条目
        if current_item:
            experience_items.append(current_item)
        
        return experience_items
    
    def _extract_skills(self, section_lines: List[str]) -> List[SkillCategory]:
        """提取技能"""
        skill_categories = []
        
        if not section_lines:
            return skill_categories
        
        for line in section_lines:
            line = line.strip()
            if not line:
                continue
            
            # 跳过章节标题
            if line.lower() in ['skills', 'technical skills', 'abilities', '技能', '专业技能']:
                continue
            
            # 检查是否有分类（包含冒号）
            if ':' in line:
                parts = line.split(':', 1)
                category = parts[0].strip()
                skills_text = parts[1].strip() if len(parts) > 1 else ""
                
                # 如果技能文本很长，可能是描述性文字
                if len(skills_text) > 100:
                    skill_categories.append(SkillCategory(
                        category=category,
                        skills=[skills_text]
                    ))
                else:
                    # 分割技能
                    skills = [s.strip() for s in re.split(r'[,;、]', skills_text) if s.strip()]
                    skill_categories.append(SkillCategory(
                        category=category,
                        skills=skills
                    ))
            else:
                # 没有分类，作为通用技能
                skills = [s.strip() for s in re.split(r'[,;、]', line) if s.strip()]
                if skills:
                    skill_categories.append(SkillCategory(
                        category="General",
                        skills=skills
                    ))
        
        return skill_categories
