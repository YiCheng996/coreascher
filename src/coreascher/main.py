# """
# 文献综述系统主程序
# """

# import os
# import sys
# import logging
# from pathlib import Path
# from typing import Dict, Optional
# from loguru import logger
# from dotenv import load_dotenv

# # 添加项目根目录到 Python 路径
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.insert(0, project_root)

# from coreascher.crew import LiteratureReviewCrew

# # 加载环境变量
# load_dotenv()

# # 设置日志
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class LiteratureReviewSystem:
#     """文献综述系统"""
    
#     def __init__(self) -> None:
#         """初始化文献综述系统"""
#         # 确保日志目录存在
#         self.log_dir = Path("logs")
#         self.log_dir.mkdir(parents=True, exist_ok=True)
        
#         # 初始化Crew
#         self.crew = LiteratureReviewCrew()
        
#     def generate_review(self, topic: str) -> Dict:
#         """生成文献综述
        
#         Args:
#             topic: 研究主题
            
#         Returns:
#             综述结果字典
#         """
#         try:
#             # 1. 创建研究框架
#             framework = self.crew.create_research_framework(topic)
#             logger.info(f"研究框架已创建: {framework}")
            
#             # 2. 完善研究计划
#             plan = self.crew.refine_research_plan(framework)
#             logger.info(f"研究计划已完善: {plan}")
            
#             # 3. 搜索和分析文献
#             analysis = self.crew.search_and_analyze_literature(plan)
#             logger.info(f"文献分析完成: {analysis}")
            
#             # 4. 撰写和评审论文
#             outline = {"sections": ["引言", "研究方法", "结果分析", "结论"]}
#             review_result = self.crew.write_and_review_paper(analysis, outline)
#             logger.info(f"论文评审完成: {review_result}")
            
#             # 5. 生成最终论文
#             final_paper = self.crew.generate_final_paper(review_result)
#             logger.info(f"最终论文已生成: {final_paper}")
            
#             # 获取使用指标
#             metrics = self.crew.get_usage_metrics()
#             logger.info(f"任务执行指标: {metrics}")
            
#             return {
#                 "framework": framework,
#                 "plan": plan,
#                 "analysis": analysis,
#                 "review_result": review_result,
#                 "final_paper": final_paper,
#                 "metrics": metrics
#             }
            
#         except Exception as e:
#             logger.error(f"生成综述时出错: {str(e)}")
#             raise

# def main() -> None:
#     """主程序入口"""
#     try:
#         # 检查环境变量
#         if not os.getenv("OPENAI_API_KEY"):
#             raise ValueError("请设置 OPENAI_API_KEY 环境变量")
            
#         # 创建系统实例
#         system = LiteratureReviewSystem()
        
#         # 设置研究主题
#         topic = "人工智能在教育领域的应用"
        
#         # 生成综述
#         result = system.generate_review(topic)
        
#         # 输出结果
#         print("\n综述生成完成！")
#         print(f"研究主题: {topic}")
#         print(f"综述结果: {result}")
        
#     except KeyboardInterrupt:
#         print("\n程序已终止")
#     except Exception as e:
#         print(f"\n程序出错: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()

import sys
import warnings

from coreascher.crew import literature_review_crew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    literature_review_crew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        literature_review_crew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        literature_review_crew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        literature_review_crew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")