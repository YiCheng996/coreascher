import arxiv
import datetime
import logging
import time

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定义四大顶会关键词
TOP_CONF = {
    'ICML': 'International Conference on Machine Learning',
    'NeurIPS': ['Neural Information Processing Systems', 'NeurIPS'],
    'ICLR': 'International Conference on Learning Representations',
    'AAAI': 'Association for the Advancement of Artificial Intelligence'
}

def search_top_conf_papers(query: str, max_results: int = 10, sort_by: str = "submittedDate", 
                          sort_order: str = "descending", conferences: list = None) -> list:
    """
    搜索四大计算机顶会的论文
    
    参数:
        query: 搜索关键词
        max_results: 返回结果数量 (最大 2000)
        sort_by: 排序字段 ("relevance", "lastUpdatedDate", "submittedDate")
        sort_order: 排序顺序 ("ascending", "descending")
        conferences: 指定会议列表，默认全部 ['ICML', 'NeurIPS', 'ICLR', 'AAAI']
        
    返回:
        包含论文信息的列表
    """
    try:
        # 创建客户端
        client = arxiv.Client(
            page_size=100,
            delay_seconds=3,
            num_retries=3
        )
        
        # 如果未指定会议，则搜索所有顶会
        if conferences is None:
            conferences = list(TOP_CONF.keys())
            
        # 构建会议查询字符串
        conf_queries = []
        for conf in conferences:
            if conf in TOP_CONF:
                if isinstance(TOP_CONF[conf], list):
                    # 如果会议有多个名称变体
                    conf_parts = [f'"{name}"' for name in TOP_CONF[conf]]
                    conf_queries.extend(conf_parts)
                else:
                    conf_queries.append(f'"{TOP_CONF[conf]}"')
        
        # 构建完整的查询字符串
        # 限制在 cs.AI, cs.LG, cs.CL, cs.CV 等相关类别中搜索
        query_str = (
            f'abs:"{query}" AND ('
            + ' OR '.join(conf_queries)
            + ') AND ('
            + ' OR '.join(['cat:cs.AI', 'cat:cs.LG', 'cat:cs.CL', 'cat:cs.CV', 'cat:cs.NE'])
            + ')'
        )
        
        logger.info(f"搜索查询: {query_str}")
        
        # 构建搜索查询
        search = arxiv.Search(
            query=query_str,
            max_results=min(max_results, 2000),
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending if sort_order == "descending" else arxiv.SortOrder.Ascending
        )
        
        papers = []
        try:
            # 获取结果
            results = list(client.results(search))
            logger.info(f"找到 {len(results)} 篇论文")
            
            for result in results:
                try:
                    # 提取会议信息（通常在comment或journal_ref中）
                    conference_info = None
                    if hasattr(result, 'comment') and result.comment:
                        conference_info = result.comment
                    if hasattr(result, 'journal_ref') and result.journal_ref:
                        conference_info = result.journal_ref
                    
                    paper = {
                        "title": result.title,
                        "authors": [author.name for author in result.authors],
                        "abstract": result.summary,
                        "published_date": result.published.strftime("%Y-%m-%d"),
                        "updated_date": result.updated.strftime("%Y-%m-%d"),
                        "url": result.entry_id,
                        "pdf_url": result.pdf_url,
                        "categories": result.categories,
                        "primary_category": result.primary_category,
                        "conference_info": conference_info,
                        "comment": result.comment if hasattr(result, 'comment') else None,
                        "journal_ref": result.journal_ref if hasattr(result, 'journal_ref') else None,
                        "doi": result.doi if hasattr(result, 'doi') else None
                    }
                    papers.append(paper)
                    logger.debug(f"成功处理论文: {paper['title'][:50]}...")
                    
                except Exception as e:
                    logger.error(f"处理单篇论文时发生错误: {str(e)}")
                    continue
                    
            return papers
            
        except Exception as e:
            logger.error(f"获取搜索结果时发生错误: {str(e)}")
            raise
            
    except Exception as e:
        logger.error(f"搜索过程中发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # 测试搜索
        results = search_top_conf_papers(
            query="GPT",
            max_results=5,
            conferences=['ICML', 'NeurIPS']  # 可以指定特定会议
        )
        
        if not results:
            print("未找到任何结果")
            exit()
            
        # 打印结果
        for i, paper in enumerate(results, 1):
            print(f"\n论文 {i}:")
            print(f"标题: {paper['title']}")
            print(f"作者: {', '.join(paper['authors'])}")
            print(f"发布日期: {paper['published_date']}")
            print(f"更新日期: {paper['updated_date']}")
            print(f"主分类: {paper['primary_category']}")
            print(f"所有分类: {', '.join(paper['categories'])}")
            if paper['conference_info']:
                print(f"会议信息: {paper['conference_info']}")
            print(f"URL: {paper['url']}")
            print(f"PDF: {paper['pdf_url']}")
            if paper['doi']:
                print(f"DOI: {paper['doi']}")
            if paper['journal_ref']:
                print(f"期刊引用: {paper['journal_ref']}")
            if paper['comment']:
                print(f"评论: {paper['comment']}")
            print("\n摘要:")
            print(paper['abstract'][:300] + "...")
            print("-" * 80)

    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise