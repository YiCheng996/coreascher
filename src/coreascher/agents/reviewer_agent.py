"""
评审人代理模块

该模块实现了一个严谨的评审人代理，负责：
1. 评估论文质量
2. 提供修改建议
3. 确保论文符合学术规范
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from crewai import Agent
from crewai.project import CrewBase, agent

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@CrewBase
class ReviewerAgent:
    """评审人代理，负责论文评审和质量把控"""
    
    def __init__(self) -> None:
        """初始化评审人代理"""
        super().__init__()
        
        # 确保存储目录存在
        self.store_dir = Path("data/reviewer")
        self.store_dir.mkdir(parents=True, exist_ok=True)
    
    @agent
    def reviewer_agent(self) -> Agent:
        """获取Agent实例"""
        return Agent(
            role="严谨的评审人",
            goal="评估综述质量并提供改进建议",
            backstory="""您是一位严谨的评审人，
                希望您的评审能给研究课题带来启发。
                您注重论文的学术价值、创新性和规范性，
                能够提供专业、建设性的修改意见。""",
            verbose=True,
            allow_delegation=False,
            memory=True,
            max_iterations=3,
            tools=[]
        )
    
    def evaluate_paper(self, paper: str) -> Dict:
        """评估论文质量
        
        Args:
            paper: 论文内容
            
        Returns:
            评估结果字典
        """
        if not paper:
            raise ValueError("论文内容不能为空")
            
        try:
            prompt = f"""
            请评估以下论文的质量：
            
            论文内容：{paper}
            
            请从以下方面进行评估：
            1. 研究方法的合理性
            2. 论述的逻辑性
            3. 创新点分析
            4. 实验设计和结果分析
            5. 写作规范性
            
            请提供以下格式的评估结果：
            {{
                "scores": {{
                    "methodology": 分数,  # 1-10分
                    "logic": 分数,
                    "innovation": 分数,
                    "experiment": 分数,
                    "writing": 分数
                }},
                "comments": {{
                    "strengths": ["优点1", "优点2"],
                    "weaknesses": ["不足1", "不足2"]
                }},
                "overall_score": 总分,  # 1-10分
                "recommendation": "接受/修改后接受/拒绝"
            }}
            """
            return self.reviewer_agent().execute(prompt)
        except Exception as e:
            logger.error(f"评估论文时出错: {str(e)}")
            return {}
    
    def provide_suggestions(self, evaluation: Dict) -> Dict:
        """提供修改建议
        
        Args:
            evaluation: 评估结果
            
        Returns:
            修改建议字典
        """
        if not evaluation:
            raise ValueError("评估结果不能为空")
            
        try:
            prompt = f"""
            请根据以下评估结果提供具体的修改建议：
            
            评估结果：{json.dumps(evaluation, ensure_ascii=False)}
            
            请提供以下格式的修改建议：
            {{
                "major_revisions": [  # 主要修改建议
                    {{
                        "aspect": "修改方面",
                        "current_issue": "当前问题",
                        "suggestion": "具体建议",
                        "expected_outcome": "预期效果"
                    }}
                ],
                "minor_revisions": [  # 次要修改建议
                    {{
                        "aspect": "修改方面",
                        "suggestion": "具体建议"
                    }}
                ],
                "priority_order": ["建议1", "建议2"]  # 建议的优先顺序
            }}
            """
            return self.reviewer_agent().execute(prompt)
        except Exception as e:
            logger.error(f"提供修改建议时出错: {str(e)}")
            return {}
    
    def check_revision(self, original: str, revised: str, suggestions: Dict) -> Dict:
        """检查修改情况
        
        Args:
            original: 原始论文
            revised: 修改后的论文
            suggestions: 修改建议
            
        Returns:
            检查结果字典
        """
        if not all([original, revised, suggestions]):
            raise ValueError("参数不能为空")
            
        try:
            prompt = f"""
            请检查论文的修改情况：
            
            原始论文：{original}
            修改后的论文：{revised}
            修改建议：{json.dumps(suggestions, ensure_ascii=False)}
            
            请提供以下格式的检查结果：
            {{
                "addressed_suggestions": [  # 已采纳的建议
                    {{
                        "suggestion": "建议内容",
                        "implementation": "实施情况",
                        "effectiveness": "效果评价"
                    }}
                ],
                "pending_suggestions": [  # 未完全采纳的建议
                    {{
                        "suggestion": "建议内容",
                        "current_status": "当前状态",
                        "further_advice": "进一步建议"
                    }}
                ],
                "new_issues": ["新问题1", "新问题2"],  # 修改后出现的新问题
                "overall_assessment": "总体评价",
                "next_steps": ["后续步骤1", "后续步骤2"]
            }}
            """
            return self.reviewer_agent().execute(prompt)
        except Exception as e:
            logger.error(f"检查修改情况时出错: {str(e)}")
            return {}
    
    def final_review(self, paper: str) -> Dict:
        """进行最终评审
        
        Args:
            paper: 最终论文内容
            
        Returns:
            最终评审结果
        """
        if not paper:
            raise ValueError("论文内容不能为空")
            
        try:
            prompt = f"""
            请对以下论文进行最终评审：
            
            论文内容：{paper}
            
            请提供以下格式的评审结果：
            {{
                "final_scores": {{
                    "methodology": 分数,  # 1-10分
                    "logic": 分数,
                    "innovation": 分数,
                    "experiment": 分数,
                    "writing": 分数,
                    "overall": 分数
                }},
                "final_assessment": {{
                    "major_contributions": ["贡献1", "贡献2"],
                    "limitations": ["局限1", "局限2"],
                    "future_work": ["建议1", "建议2"]
                }},
                "publication_readiness": {{
                    "status": "可以发表/需要修改/不建议发表",
                    "confidence": 置信度,  # 1-5
                    "additional_comments": "补充说明"
                }}
            }}
            """
            return self.reviewer_agent().execute(prompt)
        except Exception as e:
            logger.error(f"进行最终评审时出错: {str(e)}")
            return {}
