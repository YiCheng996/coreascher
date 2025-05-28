"""
教授代理模块

该模块实现了一个计算机科学教授代理，负责：
1. 制定研究框架
2. 指导研究方向
3. 评审研究成果
"""

import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
from loguru import logger
from crewai import Agent
from crewai.project import CrewBase

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@CrewBase
class ProfessorAgent:
    """教授代理，负责研究指导和评审"""
    
    def __init__(self) -> None:
        """初始化教授代理"""
        super().__init__()
        
        # 确保存储目录存在
        self.store_dir = Path("data/professor")
        self.store_dir.mkdir(parents=True, exist_ok=True)
    
    def professor_agent(self) -> Agent:
        """获取Agent实例"""
        return Agent(
            role="研究教授",
            goal="指导和评审研究工作",
            backstory="""作为一位经验丰富的研究教授，您专注于帮助研究生完成高质量的研究工作。
                您擅长制定研究框架、评审论文并提供建设性的反馈。""",
            verbose=True,
            allow_delegation=False,
            memory=True,
            max_iterations=5,
            tools=[]
        )
    
    def create_framework(self, topic: str) -> Dict:
        """创建研究框架
        
        Args:
            topic: 研究主题
            
        Returns:
            研究框架字典
            
        Raises:
            ValueError: 当主题为空时
        """
        if not topic:
            logger.error("研究主题不能为空")
            raise ValueError("研究主题不能为空")
            
        try:
            prompt = f"""
            请为以下研究主题创建详细的研究框架：
            主题：{topic}
            
            请提供以下内容：
            {{
                "background": "研究背景",
                "objectives": ["研究目标1", "研究目标2"],
                "methodology": {{
                    "approach": "研究方法",
                    "steps": ["步骤1", "步骤2"]
                }},
                "expected_outcomes": ["预期成果1", "预期成果2"]
            }}
            """
            result = self.professor_agent().execute(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError as e:
                logger.error(f"解析框架结果失败: {str(e)}")
                return {}
        except Exception as e:
            logger.error(f"创建研究框架时出错: {str(e)}")
            return {}
    
    def review_paper(self, paper: str) -> Dict:
        """评审论文
        
        Args:
            paper: 论文内容
            
        Returns:
            评审结果字典
            
        Raises:
            ValueError: 当论文内容为空时
        """
        if not paper:
            raise ValueError("论文内容不能为空")
            
        try:
            prompt = f"""
            请评审以下论文：
            论文内容：{paper}
            
            请提供以下评审结果：
            {{
                "overall_assessment": {{
                    "strengths": ["优点1", "优点2"],
                    "weaknesses": ["不足1", "不足2"]
                }},
                "detailed_review": {{
                    "methodology": {{
                        "score": 0,  # 1-10分
                        "comments": "评价意见"
                    }},
                    "results": {{
                        "score": 0,
                        "comments": "评价意见"
                    }},
                    "discussion": {{
                        "score": 0,
                        "comments": "评价意见"
                    }}
                }},
                "recommendations": ["建议1", "建议2"]
            }}
            """
            return self.professor_agent().execute(prompt)
        except Exception as e:
            logger.error(f"评审论文时出错: {str(e)}")
            return {}
    
    def provide_guidance(self, question: str) -> Dict:
        """提供研究指导
        
        Args:
            question: 研究问题
            
        Returns:
            指导意见字典
            
        Raises:
            ValueError: 当问题为空时
        """
        if not question:
            raise ValueError("研究问题不能为空")
            
        try:
            prompt = f"""
            请为以下研究问题提供指导意见：
            问题：{question}
            
            请提供以下内容：
            {{
                "analysis": {{
                    "key_points": ["要点1", "要点2"],
                    "challenges": ["挑战1", "挑战2"]
                }},
                "suggestions": {{
                    "immediate_actions": ["行动1", "行动2"],
                    "long_term_plan": ["计划1", "计划2"]
                }},
                "references": ["参考资料1", "参考资料2"]
            }}
            """
            return self.professor_agent().execute(prompt)
        except Exception as e:
            logger.error(f"提供指导意见时出错: {str(e)}")
            return {} 