"""
智能内容分类模块
使用关键词匹配、正则表达式和同义词库来智能识别简历/求职信的各个部分
"""
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from backend.utils.logger import log_processing


class ResumeSection(Enum):
    """简历章节类型"""
    HEADER = "header"           # 姓名等头部信息
    CONTACT = "contact"         # 联系方式
    EDUCATION = "education"     # 教育背景
    EXPERIENCE = "experience"   # 工作经历
    PROJECTS = "projects"       # 项目经历
    SKILLS = "skills"          # 技能
    SUMMARY = "summary"        # 个人总结/自我评价
    AWARDS = "awards"          # 获奖/荣誉
    PUBLICATIONS = "publications"  # 发表论文
    CERTIFICATIONS = "certifications"  # 证书
    LANGUAGES = "languages"    # 语言能力
    INTERESTS = "interests"    # 兴趣爱好
    UNKNOWN = "unknown"        # 未知


class CoverLetterSection(Enum):
    """求职信章节类型"""
    SENDER_INFO = "sender_info"       # 发件人信息
    RECIPIENT_INFO = "recipient_info"  # 收件人信息
    DATE = "date"                     # 日期
    SALUTATION = "salutation"         # 称呼
    OPENING = "opening"               # 开头段落
    BODY = "body"                     # 正文
    CLOSING = "closing"               # 结尾段落
    SIGNATURE = "signature"           # 签名
    UNKNOWN = "unknown"


@dataclass
class ClassifiedContent:
    """分类后的内容"""
    section: str
    content: str
    confidence: float
    keywords_matched: List[str] = field(default_factory=list)


class SmartClassifier:
    """智能内容分类器"""
    
    def __init__(self):
        # 简历章节关键词及其同义词（中英文）
        self.resume_section_keywords = {
            ResumeSection.EDUCATION: {
                "primary": ["education", "educational background", "academic background", 
                           "学历", "教育背景", "教育经历", "学习经历"],
                "synonyms": ["university", "college", "school", "degree", "bachelor", "master", 
                            "phd", "diploma", "gpa", "major", "minor", "coursework",
                            "大学", "学院", "学位", "本科", "硕士", "博士", "专业", "课程"]
            },
            ResumeSection.EXPERIENCE: {
                "primary": ["experience", "work experience", "professional experience", 
                           "employment", "work history", "career history",
                           "工作经历", "工作经验", "实习经历", "职业经历"],
                "synonyms": ["intern", "internship", "job", "position", "role", "company", 
                            "employer", "responsibilities", "duties", "achieved",
                            "实习", "职位", "公司", "工作", "负责", "业绩"]
            },
            ResumeSection.PROJECTS: {
                "primary": ["projects", "project experience", "academic projects", 
                           "personal projects", "项目经历", "项目经验", "项目"],
                "synonyms": ["developed", "built", "created", "implemented", "designed",
                            "开发", "构建", "实现", "设计", "技术栈"]
            },
            ResumeSection.SKILLS: {
                "primary": ["skills", "technical skills", "professional skills", "abilities",
                           "competencies", "expertise", "技能", "专业技能", "技术能力"],
                "synonyms": ["proficient", "experienced", "familiar", "knowledge", "tools",
                            "programming", "software", "languages", "frameworks",
                            "熟练", "精通", "了解", "掌握", "工具", "语言"]
            },
            ResumeSection.SUMMARY: {
                "primary": ["summary", "profile", "objective", "about me", "self-appraisal",
                           "professional summary", "career objective",
                           "个人简介", "自我评价", "个人总结", "职业目标", "求职意向"],
                "synonyms": ["passionate", "motivated", "seeking", "goal", "aspiration",
                            "热情", "积极", "寻求", "目标", "志向"]
            },
            ResumeSection.AWARDS: {
                "primary": ["awards", "honors", "achievements", "recognition",
                           "荣誉", "获奖", "奖励", "成就"],
                "synonyms": ["scholarship", "dean's list", "prize", "winner", "certificate",
                            "奖学金", "优秀", "第一", "冠军"]
            },
            ResumeSection.CERTIFICATIONS: {
                "primary": ["certifications", "certificates", "licenses", "credentials",
                           "证书", "认证", "资格"],
                "synonyms": ["certified", "licensed", "accredited", "qualification",
                            "获得", "通过", "考取"]
            },
            ResumeSection.LANGUAGES: {
                "primary": ["languages", "language skills", "语言能力", "语言"],
                "synonyms": ["fluent", "native", "proficient", "intermediate", "beginner",
                            "english", "chinese", "spanish", "french", "german",
                            "流利", "母语", "精通", "中级", "初级"]
            },
            ResumeSection.INTERESTS: {
                "primary": ["interests", "hobbies", "activities", "extracurricular",
                           "兴趣爱好", "爱好", "课外活动"],
                "synonyms": ["volunteer", "club", "sports", "music", "travel",
                            "志愿者", "社团", "运动", "音乐", "旅行"]
            },
            ResumeSection.CONTACT: {
                "primary": ["contact", "contact information", "personal information",
                           "联系方式", "个人信息"],
                "synonyms": ["email", "phone", "address", "linkedin", "github", "website",
                            "邮箱", "电话", "地址", "手机"]
            }
        }
        
        # 求职信章节识别模式
        self.cover_letter_patterns = {
            CoverLetterSection.SENDER_INFO: [
                r'^[A-Z][a-z]+\s+[A-Z][a-z]+$',  # 姓名
                r'^[\w\.-]+@[\w\.-]+\.\w+$',     # 邮箱
                r'^\+?\d[\d\s\-\(\)]{6,}$',      # 电话
            ],
            CoverLetterSection.DATE: [
                r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s*\d{4}',
                r'\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}',
                r'\d{4}年\d{1,2}月\d{1,2}日',
            ],
            CoverLetterSection.SALUTATION: [
                r'^Dear\s+',
                r'^To\s+whom',
                r'^尊敬的',
                r'^亲爱的',
            ],
            CoverLetterSection.CLOSING: [
                r'^Sincerely,?$',
                r'^Best\s+regards,?$',
                r'^Thank\s+you',
                r'^此致敬礼',
                r'^祝好',
            ],
            CoverLetterSection.SIGNATURE: [
                r'^[A-Z][a-z]+\s+[A-Z][a-z]+$',  # 末尾的姓名
            ]
        }
        
        # 联系方式正则
        self.contact_patterns = {
            "email": re.compile(r'[\w\.-]+@[\w\.-]+\.\w+'),
            "phone": re.compile(r'[\+]?[\d\-\(\)\s]{7,20}'),
            "linkedin": re.compile(r'linkedin\.com/in/[\w\-]+', re.I),
            "github": re.compile(r'github\.com/[\w\-]+', re.I),
            "address": re.compile(r'[A-Z][a-z]+,?\s*[A-Z]{2}\s*\d{0,5}'),
        }
    
    def classify_resume_section(self, text: str) -> Tuple[ResumeSection, float, List[str]]:
        """
        对文本进行简历章节分类
        
        Returns:
            (章节类型, 置信度, 匹配的关键词列表)
        """
        text_lower = text.lower()
        best_match = ResumeSection.UNKNOWN
        best_score = 0.0
        matched_keywords = []
        
        for section, keywords in self.resume_section_keywords.items():
            score = 0.0
            current_matches = []
            
            # 检查主要关键词（权重高）
            for kw in keywords["primary"]:
                if kw in text_lower:
                    score += 3.0
                    current_matches.append(kw)
            
            # 检查同义词（权重较低）
            for kw in keywords["synonyms"]:
                if kw in text_lower:
                    score += 1.0
                    current_matches.append(kw)
            
            # 计算置信度
            total_keywords = len(keywords["primary"]) * 3 + len(keywords["synonyms"])
            confidence = min(score / max(total_keywords * 0.3, 1), 1.0)
            
            if score > best_score:
                best_score = score
                best_match = section
                matched_keywords = current_matches
        
        final_confidence = min(best_score / 5.0, 1.0) if best_score > 0 else 0.0
        return best_match, final_confidence, matched_keywords
    
    def classify_resume_content(self, paragraphs: List[str]) -> List[ClassifiedContent]:
        """
        对简历内容进行智能分类
        """
        log_processing("SmartClassifier", "开始智能分类简历内容")
        
        classified = []
        current_section = ResumeSection.HEADER
        
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            
            # 检测是否是章节标题
            section, confidence, keywords = self.classify_resume_section(para)
            
            # 如果是明确的章节标题（短文本+高置信度）
            if len(para) < 50 and confidence > 0.5:
                current_section = section
                classified.append(ClassifiedContent(
                    section=current_section.value,
                    content=para,
                    confidence=confidence,
                    keywords_matched=keywords
                ))
            else:
                # 使用当前章节或尝试根据内容判断
                content_section, content_conf, content_kw = self.classify_resume_section(para)
                
                # 如果内容本身有明确的特征
                if content_conf > 0.3:
                    classified.append(ClassifiedContent(
                        section=content_section.value,
                        content=para,
                        confidence=content_conf,
                        keywords_matched=content_kw
                    ))
                else:
                    # 继承当前章节
                    classified.append(ClassifiedContent(
                        section=current_section.value,
                        content=para,
                        confidence=0.5,
                        keywords_matched=[]
                    ))
        
        log_processing("SmartClassifier", f"分类完成: {len(classified)} 个内容块")
        return classified
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """提取联系信息"""
        contact = {}
        
        for field, pattern in self.contact_patterns.items():
            match = pattern.search(text)
            if match:
                contact[field] = match.group()
        
        return contact
    
    def classify_cover_letter_section(self, text: str, position: int, total: int) -> CoverLetterSection:
        """
        对求职信段落进行分类
        
        Args:
            text: 段落文本
            position: 段落位置（从0开始）
            total: 总段落数
        """
        # 检查特定模式
        for section, patterns in self.cover_letter_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.I):
                    return section
        
        # 根据位置判断
        if position < 3:
            # 前几行可能是发件人信息
            if self.contact_patterns["email"].search(text):
                return CoverLetterSection.SENDER_INFO
            if self.contact_patterns["phone"].search(text):
                return CoverLetterSection.SENDER_INFO
        
        if position == total - 1 or position == total - 2:
            # 最后几行可能是签名
            if len(text) < 50 and not any(c in text for c in '.!?。！？'):
                return CoverLetterSection.SIGNATURE
        
        # 检查是否是收件人信息
        recipient_keywords = ['manager', 'director', 'coordinator', 'hr', 'hiring', 
                             'recruiter', 'inc', 'ltd', 'company', 'corporation']
        if any(kw in text.lower() for kw in recipient_keywords):
            if position < 6:
                return CoverLetterSection.RECIPIENT_INFO
        
        # 默认为正文
        return CoverLetterSection.BODY
    
    def classify_cover_letter_content(self, paragraphs: List[str]) -> List[ClassifiedContent]:
        """对求职信内容进行智能分类"""
        log_processing("SmartClassifier", "开始智能分类求职信内容")
        
        classified = []
        total = len(paragraphs)
        
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            
            section = self.classify_cover_letter_section(para, i, total)
            
            classified.append(ClassifiedContent(
                section=section.value,
                content=para,
                confidence=0.8,
                keywords_matched=[]
            ))
        
        log_processing("SmartClassifier", f"分类完成: {len(classified)} 个内容块")
        return classified
    
    def merge_similar_sections(self, classified: List[ClassifiedContent]) -> Dict[str, List[str]]:
        """将相同章节的内容合并"""
        merged = {}
        
        for item in classified:
            if item.section not in merged:
                merged[item.section] = []
            merged[item.section].append(item.content)
        
        return merged


# 全局实例
smart_classifier = SmartClassifier()
