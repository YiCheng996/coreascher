import unittest
import shutil
from pathlib import Path
from src.coreascher.tools.arxiv_tool import ArxivSearchTool

class TestArxivSearchTool(unittest.TestCase):
    """ArxivSearchTool测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_topic = "test_topic"
        self.tool = ArxivSearchTool(topic=self.test_topic)
        
    def tearDown(self):
        """测试后清理"""
        # 删除测试生成的文件
        if Path("literature_store").exists():
            shutil.rmtree("literature_store")
    
    def test_initialization(self):
        """测试工具初始化"""
        self.assertEqual(self.tool.topic, self.test_topic)
        self.assertTrue(self.tool.store_dir.exists())
        self.assertTrue(self.tool.index_file.exists())
        
    def test_search_and_store(self):
        """测试搜索和存储功能"""
        # 执行搜索
        result = self.tool._run(
            query="GPT",
            max_results=2,
            conferences=['ICML']
        )
        
        # 验证返回结果
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "未找到相关论文")
        
        # 验证文件存储
        index = self.tool._load_index()
        self.assertGreater(len(index["papers"]), 0)
        
        # 验证论文文件
        paper_files = list(self.tool.store_dir.glob("*.json"))
        self.assertGreater(len(paper_files), 0)
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效查询
        result = self.tool._run(
            query="",
            max_results=1
        )
        self.assertIn("搜索失败", result)
        
    def test_duplicate_storage(self):
        """测试重复存储处理"""
        # 执行两次相同的搜索
        self.tool._run(
            query="GPT",
            max_results=1,
            conferences=['ICML']
        )
        
        # 记录第一次搜索后的文件数
        first_count = len(list(self.tool.store_dir.glob("*.json")))
        
        # 再次执行相同搜索
        self.tool._run(
            query="GPT",
            max_results=1,
            conferences=['ICML']
        )
        
        # 验证文件数没有变化
        second_count = len(list(self.tool.store_dir.glob("*.json")))
        self.assertEqual(first_count, second_count)
        
    def test_sort_by_date(self):
        """测试按发布时间排序"""
        result = self.tool._run(
            query="GPT",
            max_results=3,
            sort_by="date",
            sort_order="descending"
        )
        
        # 验证结果包含日期信息
        self.assertIn("发布日期", result)
        
        # 验证排序顺序
        dates = []
        for line in result.split('\n'):
            if line.startswith("发布日期:"):
                dates.append(line.split(": ")[1])
        
        # 验证日期是降序排列的
        self.assertEqual(dates, sorted(dates, reverse=True))
        
    def test_sort_by_citations(self):
        """测试按引用数排序"""
        result = self.tool._run(
            query="GPT",
            max_results=3,
            sort_by="citations",
            sort_order="descending",
            min_citations=1
        )
        
        # 验证结果包含引用数信息
        self.assertIn("引用数", result)
        
        # 验证排序顺序
        citations = []
        for line in result.split('\n'):
            if line.startswith("引用数:"):
                try:
                    citations.append(int(line.split(": ")[1]))
                except ValueError:
                    continue
        
        # 验证引用数是降序排列的
        self.assertEqual(citations, sorted(citations, reverse=True))
        
    def test_min_citations_filter(self):
        """测试最小引用数过滤"""
        min_citations = 100
        result = self.tool._run(
            query="GPT",
            max_results=3,
            min_citations=min_citations
        )
        
        # 如果有结果，验证所有论文的引用数都大于等于最小值
        if result != "未找到相关论文":
            citations = []
            for line in result.split('\n'):
                if line.startswith("引用数:"):
                    try:
                        citation = int(line.split(": ")[1])
                        citations.append(citation)
                        self.assertGreaterEqual(citation, min_citations)
                    except ValueError:
                        continue

if __name__ == '__main__':
    unittest.main() 