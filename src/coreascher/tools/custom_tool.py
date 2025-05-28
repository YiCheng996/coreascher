# """
# 自定义工具模块，实现文献搜索相关功能（基于 @tool 装饰器）
# """

# import json
# import logging
# import requests
# from crewai.tools import tool

# # 设置日志
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # 1️⃣ 文献搜索工具
# @tool("literature_search_tool")
# def literature_search_tool(query: str) -> str:
#     """根据关键词搜索文献"""
#     try:
#         response = requests.get(
#             "http://180.184.65.98:38880/atomgit/search_papers",
#             params={"query": query, "top_k": 30}
#         )
#         response.raise_for_status()
#         return json.dumps(response.json(), ensure_ascii=False)
#     except Exception as e:
#         logger.error(f"文献搜索失败: {str(e)}")
#         return f"搜索失败: {str(e)}"

# # 2️⃣ 论文查询工具
# @tool("paper_query_tool")
# def paper_query_tool(paper_id: str) -> str:
#     """根据论文ID查询论文详细信息"""
#     try:
#         response = requests.get(
#             "http://180.184.65.98:38880/atomgit/query_by_paper_id",
#             params={"paper_id": paper_id, "top_k": 5}
#         )
#         response.raise_for_status()
#         return json.dumps(response.json(), ensure_ascii=False)
#     except Exception as e:
#         logger.error(f"论文查询失败: {str(e)}")
#         return f"查询失败: {str(e)}"
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import arxiv
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestToolInput(BaseModel):
    """Input schema for TestTool."""
    argument: str = Field(..., description="搜索关键词")

class TestTool(BaseTool):
    name: str = "Searchtool"
    description: str = (
        "用于根据文章主题搜索关键词"
    )
    args_schema: Type[BaseModel] = TestToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "在这篇文章中，我们将深入探讨大型语言模型（LLMs）的迷人世界，以及它们理解和生成类似人类语言的不可思议能力。我们将讨论这些模型的历史和演变，涉及到重要的里程碑，如GPT系列及其后继模型。我们还将探索不同类型的LLMs、它们的应用以及支撑许多先进技术的核心概念。"

class LiteratureSearchInput(BaseModel):
    """Input schema for LiteratureSearchTool."""
    query: str = Field(..., description="搜索关键词")

class LiteratureSearch(BaseTool):
    name: str = "LiteratureSearch"
    description: str = "使用arXiv API搜索学术论文"
    args_schema: Type[BaseModel] = LiteratureSearchInput
    
    def _run(self, query: str) -> str:
        """执行arXiv文献搜索"""
        try:
            # 创建搜索客户端
            client = arxiv.Client()
            
            # 构建搜索查询
            search = arxiv.Search(
                query=query,
                max_results=10,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            # 执行搜索
            results = []
            for paper in client.results(search):
                results.append({
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary,
                    "published": paper.published.strftime("%Y-%m-%d"),
                    "pdf_url": paper.pdf_url,
                    "entry_id": paper.entry_id
                })
            
            return json.dumps({"papers": results}, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"arXiv文献搜索失败: {str(e)}")
            return f"搜索失败: {str(e)}"