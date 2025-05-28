"""
博士后研究员代理模块

该模块实现了一个计算机科学博士后研究员代理，负责：
1. 理解和完善研究框架
2. 分配研究任务
3. 整合论文内容
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from loguru import logger
from crewai import Agent
from crewai.project import CrewBase
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@CrewBase
class PostDocAgent:
    """博士后代理，负责研究框架完善和论文整合"""
    
    def __init__(self) -> None:
        """初始化博士后代理"""
        super().__init__()
        
        # 确保存储目录存在
        self.store_dir = Path("data/postdoc")
        self.store_dir.mkdir(parents=True, exist_ok=True)
    
    def postdoc_agent(self) -> Agent:
        """获取Agent实例"""
        return Agent(
            role="计算机科学博士后研究员",
            goal="将研究计划转化为具体任务并整合研究成果",
            backstory="""您是一位计算机科学领域的博士后研究员，
                擅长将高水平的研究计划转化为具体的实验设计。
                您负责理解和完善研究框架，分配研究任务，
                并确保最终的论文符合学术规范。""",
            verbose=True,
            allow_delegation=False,
            memory=True,
            max_iterations=3,
            tools=[]
        )
    
    def analyze_framework(self, framework: Dict) -> Dict:
        """分析研究框架并提出完善建议
        
        Args:
            framework: 研究框架字典
            
        Returns:
            分析结果字典
            
        Raises:
            ValueError: 当框架为空时
        """
        if not framework:
            logger.error("研究框架不能为空")
            raise ValueError("研究框架不能为空")
            
        try:
            prompt = f"""
            请分析以下研究框架，并提出完善建议：
            框架内容：{json.dumps(framework, ensure_ascii=False)}
            
            请提供以下分析：
            {{
                "analysis": {{
                    "strengths": ["优点1", "优点2"],
                    "weaknesses": ["不足1", "不足2"],
                    "suggestions": ["建议1", "建议2"]
                }}
            }}
            """
            result = self.postdoc_agent().execute(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError as e:
                logger.error(f"解析分析结果失败: {str(e)}")
                return {}
        except Exception as e:
            logger.error(f"分析框架时出错: {str(e)}")
            return {}
            
    def assign_tasks(self, task: str) -> Dict:
        """为研究任务生成具体的搜索关键词和要求
        
        Args:
            task: 研究任务描述
            
        Returns:
            任务分配结果字典
            
        Raises:
            ValueError: 当任务描述为空时
        """
        if not task:
            raise ValueError("研究任务不能为空")
            
        try:
            prompt = f"""
            请根据以下研究任务，生成具体的搜索关键词和要求：
            任务内容：{task}
            
            请提供以下内容：
            {{
                "keywords": ["关键词1", "关键词2"],
                "requirements": ["要求1", "要求2"],
                "expected_outcomes": ["预期结果1", "预期结果2"]
            }}
            """
            return self.postdoc_agent().execute(prompt)
        except Exception as e:
            logger.error(f"分配任务时出错: {str(e)}")
            return {}
            
    def integrate_paper(self, content: str) -> Dict:
        """整合论文段落，确保内容连贯
        
        Args:
            content: 论文段落内容
            
        Returns:
            整合结果字典
            
        Raises:
            ValueError: 当内容为空时
        """
        if not content:
            raise ValueError("论文内容不能为空")
            
        try:
            prompt = f"""
            请整合以下论文段落，确保内容连贯且符合学术规范：
            段落内容：{content}
            
            请提供以下内容：
            {{
                "integrated_content": "整合后的内容",
                "modifications": [
                    {{
                        "type": "修改类型",
                        "description": "修改说明"
                    }}
                ]
            }}
            """
            return self.postdoc_agent().execute(prompt)
        except Exception as e:
            logger.error(f"整合论文时出错: {str(e)}")
            return {} 