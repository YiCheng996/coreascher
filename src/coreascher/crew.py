"""
文献综述Crew模块

该模块实现了一个文献综述Crew，协调多个Agent完成文献综述任务。
"""

import logging
import os
from typing import Dict, List, Optional
from crewai import Crew, Task, Agent, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from coreascher.tools.custom_tool import LiteratureSearch

llm = LLM(model="openai/glm-4-plus")

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@CrewBase
class LiteratureReviewCrew:
    """文献综述Crew，协调多个Agent完成综述任务"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    # def __init__(self) -> None:
    #     """初始化文献综述Crew"""
    #     super().__init__()

    #     # 创建日志目录
    #     log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    #     os.makedirs(log_dir, exist_ok=True)
    #     log_file = os.path.join(log_dir, 'crew_execution.log')

    #     # 创建Crew实例
    #     self._crew = Crew(
    #         agents=[
    #             self.professor(),
    #             self.postdoc(),
    #             self.phd(),
    #             self.reviewer()
    #         ],
    #         tasks=[],
    #         verbose=True,
    #         process=Process.sequential,
    #         memory=True,
    #         cache=True,
    #         output_log_file=log_file,
    #         llm=llm
    #     )
    @agent
    def professor(self) -> Agent:
        """创建教授Agent"""
        return Agent(
            config=self.agents_config['professor'],
            verbose=True,
            allow_delegation=False
        )
    @agent   
    def postdoc(self) -> Agent:
        """创建博士后Agent"""
        return Agent(
            config=self.agents_config['postdoc'],
            verbose=True,
            allow_delegation=False
        )
    @agent   
    def phd(self) -> Agent:
        """创建博士生Agent"""
        return Agent(
            config=self.agents_config['phd'],
            verbose=True,
            allow_delegation=True,
            tools=[LiteratureSearch()]           
        )
        
    # @agent 
    # def reviewer(self) -> Agent:
    #     """创建评审人Agent"""
    #     return Agent(
    #         config=self.agents_config['reviewer'],
    #         verbose=True,
    #         allow_delegation=False
    #     )
    
    create_research_framework = Task(
        description = "请为以下研究主题生成一个详细的研究框架: 主题: {topic} 框架应包含： 1. 研究背景 2. 研究目标 3. 研究内容 4. 技术路线 5. 预期成果",
        expected_output = "一个包含完整研究框架的JSON格式结果，包括： - 各章节标题 - 章节内容概述 - 技术路线图",
        agent = professor
    )
    
    analyze_framework = Task(
        description = "分析研究框架并提出完善建议",
        expected_output = "一个包含完整研究框架的JSON格式结果，包括： - 各章节标题 - 章节内容概述 - 技术路线图",
        agent = postdoc,
        context = create_research_framework
    )
    
    keyword_tasks = Task(
        description = "根据研究框架，为研究任务生成具体的搜索关键词和要求",
        expected_output = "keywords: [关键词列表],requirements: [研究任务] ",
        agent = postdoc,
        context = analyze_framework
    )
    
    search_literature = Task(
        description = "根据postdoc_agent给出的关键词调用摘要检索工具搜索相关文献摘要，结合postdoc_agent给出的研究任务，判断文献内容是否与研究任务相关，如果相关则保存至知识库中，不相关则继续搜索下一篇文献。每个研究任务搜索十篇相关文献。",
        expected_output = "文献搜索结果",
        agent = phd,
        tools = [LiteratureSearch()],
        context = keyword_tasks
    )
    
    literature_review = Task(
        description = "根据每个章节的研究任务和知识库中的论文，撰写符合学术用语的高质量论文综述段落。严禁使用知识库外的文献。按照文章内用`<sup>number</sup>`，文章末尾用【标题+所在会议/期刊名称+年份+chunk序号】的规则来进行综述撰写。",
        expected_output = "文献综述",
        agent = phd,
    )
    
    @task
    def create_research_framework(self) -> Task:
        return Task(
            config=self.tasks_config['create_research_framework']
        )
    
    @task
    def analyze_framework(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_framework']
        )
    
    @task # 关键词分配任务
    def keyword_tasks(self) -> Task:
        return Task(
            config=self.tasks_config['keyword_tasks']
        )
    @task
    def search_literature(self) -> Task:
        return Task(
            config=self.tasks_config['search_literature']
        )
    @task
    def literature_review(self) -> Task:
        return Task(
            config=self.tasks_config['literature_review']
        )   
    @task
    def integrate_paper(self) -> Task:
        return Task(
            config=self.tasks_config['integrate_paper']
        )
        
        
    # @task
    # def review_article_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['review_article_task']
    #     )
        
        
    # def search_and_analyze_literature(self, plan: Dict) -> Dict:
    #     """搜索和分析文献
        
    #     Args:
    #         plan: 研究计划
            
    #     Returns:
    #         文献分析结果
    #     """
    #     # 创建任务
    #     search_task = Task(
    #         description=f"根据计划搜索文献：{plan}",
    #         agent=self.phd()
    #     )
        
    #     analyze_task = Task(
    #         description="分析搜索到的文献",
    #         agent=self.phd()
    #     )
        
    #     # 添加任务到Crew
    #     self._crew.tasks = [search_task, analyze_task]
        
    #     # 执行任务
    #     result = self._crew.kickoff(inputs={"plan": plan})
    #     return result
    # @task
    # def write_and_review_paper(self, analysis: Dict, outline: Dict) -> Dict:
    #     """撰写和评审论文
        
    #     Args:
    #         analysis: 文献分析结果
    #         outline: 论文大纲
            
    #     Returns:
    #         评审结果
    #     """
    #     # 创建任务
    #     write_task = Task(
    #         description=f"根据分析结果和大纲撰写论文：\n分析：{analysis}\n大纲：{outline}",
    #         agent=self.phd()
    #     )
        
    #     review_task = Task(
    #         description="评审论文初稿",
    #         agent=self.reviewer()
    #     )
        
    #     revise_task = Task(
    #         description="根据评审意见修改论文",
    #         agent=self.phd()
    #     )
        
    #     final_review_task = Task(
    #         description="进行最终评审",
    #         agent=self.professor()
    #     )
        
        # # 添加任务到Crew
        # self._crew.tasks = [write_task, review_task, revise_task, final_review_task]
        
        # # 执行任务
        # result = self._crew.kickoff()
        # return result
    # @task
    # def generate_final_paper(self, review_result: Dict) -> str:
    #     """生成最终论文
        
    #     Args:
    #         review_result: 评审结果
            
    #     Returns:
    #         最终论文内容
    #     """
    #     # 创建任务
    #     task = Task(
    #         description=f"根据评审结果生成最终论文：{review_result}",
    #         agent=self.phd()
    #     )
        
    #     # 添加任务到Crew
    #     self._crew.tasks = [task]
        
    #     # 执行任务
    #     result = self._crew.kickoff()
    #     return result
    @crew
    def literature_review_crew(self) -> Crew:
        """创建文献综述Crew"""
        return Crew(
            agents=[self.professor(), self.postdoc(), self.phd()],
            tasks=[self.create_research_framework, self.analyze_framework, self.keyword_tasks, self.search_literature, self.literature_review, self.integrate_paper],
            process=Process.sequential,
            verbose=True
        )
