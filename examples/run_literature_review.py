"""
文献综述示例脚本

该脚本展示了如何使用 coreascher 进行文献综述任务。
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

from coreascher.agents.professor_agent import ProfessorAgent
from coreascher.agents.phd_agent import PhDAgent
from coreascher.agents.reviewer_agent import ReviewerAgent

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """运行文献综述示例"""
    try:
        # 初始化代理
        professor = ProfessorAgent()
        phd = PhDAgent()
        reviewer = ReviewerAgent()
        
        # 设置研究主题
        research_topic = "深度学习在自然语言处理中的最新进展"
        
        # 1. 创建研究框架
        logger.info("创建研究框架...")
        framework = professor.create_framework(research_topic)
        logger.info(f"研究框架: {json.dumps(framework, ensure_ascii=False, indent=2)}")
        
        # 2. 文献检索
        logger.info("开始文献检索...")
        keywords = ["deep learning", "natural language processing", "transformer", "large language model"]
        papers = phd.search_literature(keywords)
        logger.info(f"找到 {len(papers)} 篇相关文献")
        
        # 3. 文献分析
        logger.info("分析文献...")
        analysis = phd.analyze_literature(papers)
        logger.info(f"文献分析结果: {json.dumps(analysis, ensure_ascii=False, indent=2)}")
        
        # 4. 撰写初稿
        logger.info("撰写论文初稿...")
        draft = phd.write_draft(analysis, framework)
        logger.info("初稿完成")
        
        # 5. 评审初稿
        logger.info("评审初稿...")
        evaluation = reviewer.evaluate_paper(draft)
        logger.info(f"评审结果: {json.dumps(evaluation, ensure_ascii=False, indent=2)}")
        
        # 6. 提供修改建议
        logger.info("提供修改建议...")
        suggestions = reviewer.provide_suggestions(evaluation)
        logger.info(f"修改建议: {json.dumps(suggestions, ensure_ascii=False, indent=2)}")
        
        # 7. 修改论文
        logger.info("修改论文...")
        revised = phd.revise_draft(draft, suggestions)
        logger.info("修改完成")
        
        # 8. 检查修改
        logger.info("检查修改情况...")
        revision_check = reviewer.check_revision(draft, revised, suggestions)
        logger.info(f"修改检查结果: {json.dumps(revision_check, ensure_ascii=False, indent=2)}")
        
        # 9. 最终评审
        logger.info("进行最终评审...")
        final_review = reviewer.final_review(revised)
        logger.info(f"最终评审结果: {json.dumps(final_review, ensure_ascii=False, indent=2)}")
        
        # 保存结果
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "framework.json", "w", encoding="utf-8") as f:
            json.dump(framework, f, ensure_ascii=False, indent=2)
            
        with open(output_dir / "analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
            
        with open(output_dir / "draft.txt", "w", encoding="utf-8") as f:
            f.write(draft)
            
        with open(output_dir / "evaluation.json", "w", encoding="utf-8") as f:
            json.dump(evaluation, f, ensure_ascii=False, indent=2)
            
        with open(output_dir / "suggestions.json", "w", encoding="utf-8") as f:
            json.dump(suggestions, f, ensure_ascii=False, indent=2)
            
        with open(output_dir / "revised.txt", "w", encoding="utf-8") as f:
            f.write(revised)
            
        with open(output_dir / "revision_check.json", "w", encoding="utf-8") as f:
            json.dump(revision_check, f, ensure_ascii=False, indent=2)
            
        with open(output_dir / "final_review.json", "w", encoding="utf-8") as f:
            json.dump(final_review, f, ensure_ascii=False, indent=2)
            
        logger.info("文献综述任务完成！所有结果已保存到 output 目录")
        
    except Exception as e:
        logger.error(f"运行过程中出错: {str(e)}")
        raise

if __name__ == "__main__":
    main() 