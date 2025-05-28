"""
博士生代理模块

该模块实现了一个计算机科学博士生代理，负责：
1. 文献检索和分析
2. 撰写论文初稿
3. 根据反馈修改论文
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from crewai import Agent
from crewai.project import CrewBase
from coreascher.tools.custom_tool import TestTool


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@CrewBase
class PhDAgent:
    """博士生代理，负责文献检索和论文写作"""
    
    def __init__(self) -> None:
        """初始化博士生代理"""
        super().__init__()
        
        # 确保存储目录存在
        self.store_dir = Path("data/phd")
        self.store_dir.mkdir(parents=True, exist_ok=True)
        
        
        # 初始化知识库
        self.knowledge_base = {}
    
    def phd_agent(self) -> Agent:
        """获取Agent实例"""
        return Agent(
            role="计算机科学博士生",
            goal="执行文献检索和综述撰写任务",
            backstory="""您是一位计算机科学专业的博士生，
                擅长阅读和理解计算机领域的文献，
                能够提炼出与研究主题高度相关的内容。
                您负责文献检索、分析和论文写作工作。""",
            verbose=True,
            allow_delegation=True,
            memory=True,
            max_iterations=3,
            tools=[TestTool()] 
        )
    
    def search_literature(self, keywords: List[str], top_k: int = 30) -> List[Dict]:
        """根据关键词搜索相关文献
        
        Args:
            keywords: 关键词列表
            top_k: 每个关键词返回的结果数量
            
        Returns:
            文献检索结果列表
        """
        if not keywords:
            logger.error("关键词列表不能为空")
            return []
            
        results = []
        
        try:
            for keyword in keywords:
                # 使用搜索工具
                semantic_results = TestTool._run({"query": keyword})
                
                # 解析结果
                try:
                    result_list = json.loads(semantic_results)
                    results.extend(result_list[:top_k])
                except json.JSONDecodeError as e:
                    logger.error(f"解析搜索结果失败: {str(e)}")
                    continue
                
                # 获取详细信息
                for result in results:
                    if paper_id := result.get("paper_id"):
                        try:
                            paper_details = self.paper_query_tool._run({"paper_id": paper_id})
                            details = json.loads(paper_details)
                            result.update(details)
                        except Exception as e:
                            logger.error(f"获取论文详情失败: {str(e)}")
                            continue
        except Exception as e:
            logger.error(f"文献搜索过程出错: {str(e)}")
            
        return results
    
    def analyze_literature(self, papers: List[Dict]) -> Dict:
        """分析文献内容，提取关键信息
        
        Args:
            papers: 文献列表
            
        Returns:
            分析结果字典
        """
        try:
            prompt = f"""
            请分析以下文献内容，提取关键信息：
            文献内容：{json.dumps(papers, ensure_ascii=False)}
            
            请提供以下分析：
            {{
                "key_findings": ["发现1", "发现2"],
                "methodologies": ["方法1", "方法2"],
                "future_directions": ["方向1", "方向2"]
            }}
            """
            return self.phd_agent().execute(prompt)
        except Exception as e:
            logger.error(f"分析文献时出错: {str(e)}")
            return {}
    
    def write_draft(self, analysis: Dict, outline: Dict) -> str:
        """根据文献分析和大纲撰写论文初稿
        
        Args:
            analysis: 文献分析结果
            outline: 论文大纲
            
        Returns:
            论文初稿内容
        """
        try:
            prompt = f"""
            请根据以下文献分析和大纲撰写论文初稿：
            
            文献分析：{json.dumps(analysis, ensure_ascii=False)}
            论文大纲：{json.dumps(outline, ensure_ascii=False)}
            
            要求：
            1. 按照大纲结构组织内容
            2. 引用相关文献支持论述
            3. 使用学术写作风格
            4. 确保内容的连贯性和逻辑性
            """
            return self.phd_agent().execute(prompt)
        except Exception as e:
            logger.error(f"撰写论文时出错: {str(e)}")
            return ""
    
    def revise_draft(self, draft: str, feedback: Dict) -> str:
        """根据反馈修改论文
        
        Args:
            draft: 论文初稿
            feedback: 反馈意见
            
        Returns:
            修改后的论文内容
        """
        try:
            prompt = f"""
            请根据以下反馈修改论文：
            
            论文初稿：{draft}
            反馈意见：{json.dumps(feedback, ensure_ascii=False)}
            
            要求：
            1. 针对每条反馈进行修改
            2. 保持文章结构的完整性
            3. 确保修改后内容的连贯性
            4. 标注修改的部分
            """
            return self.phd_agent().execute(prompt)
        except Exception as e:
            logger.error(f"修改论文时出错: {str(e)}")
            return ""
    
    def add_to_knowledge_base(self, paper_id: str, content: Dict) -> bool:
        """将文献添加到知识库
        
        Args:
            paper_id: 论文ID
            content: 论文内容
            
        Returns:
            是否添加成功
        """
        try:
            self.knowledge_base[paper_id] = content
            return True
        except Exception as e:
            logger.error(f"添加到知识库时出错: {str(e)}")
            return False
    
    def get_from_knowledge_base(self, paper_id: str) -> Optional[Dict]:
        """从知识库获取文献
        
        Args:
            paper_id: 论文ID
            
        Returns:
            文献内容，如果不存在则返回None
        """
        return self.knowledge_base.get(paper_id) 