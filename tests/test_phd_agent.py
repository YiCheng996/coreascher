"""
测试博士生代理模块
"""

import unittest
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from pydantic import BaseModel
from src.coreascher.agents.phd_agent import PhDAgent
from dotenv import load_dotenv
from typing import Any, List, Optional

# 加载环境变量
load_dotenv()

class MockToolSchema(BaseModel):
    """模拟工具的参数模式"""
    query: str

class MockTask:
    """模拟 Task 类"""
    def __init__(self, description: str, expected_output: str, agent: Any, 
                 output_file: Optional[str] = None, tools: Optional[List[Any]] = None):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.output_file = output_file
        self.tools = tools
        self._execute_result = "{}"  # 默认返回空的 JSON 字符串

    def execute(self) -> str:
        """执行任务"""
        return self._execute_result

    def set_execute_result(self, result: str):
        """设置执行结果"""
        self._execute_result = result

class TestPhDAgent(unittest.TestCase):
    """PhDAgent测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = Path("test_research_store")
        
        # 创建模拟工具
        self.mock_tool = Mock()
        self.mock_tool.name = "test_tool"
        self.mock_tool.description = "A test tool"
        self.mock_tool.args_schema = MockToolSchema
        
        # 设置测试环境变量
        os.environ["OPENAI_API_KEY"] = "test_key"
        os.environ["OPENAI_API_BASE"] = "test_base"
        
        # 创建 mock Task
        self.mock_task = MockTask(
            description="test",
            expected_output="test",
            agent=None
        )
        
        # 使用 patch 装饰器模拟 Task 类
        patcher = patch('src.coreascher.agents.phd_agent.Task', return_value=self.mock_task)
        patcher.start()
        self.addCleanup(patcher.stop)
        
        self.agent = PhDAgent(
            store_dir=self.test_dir,
            llm_model="zhipu",
            tools=[self.mock_tool],
            verbose=True
        )
        
    def tearDown(self):
        """测试后清理"""
        if self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
            
    def test_initialization(self):
        """测试初始化"""
        # 使用 __dict__ 访问 Agent 的属性
        agent_dict = self.agent.agent.__dict__
        self.assertEqual(agent_dict.get('role'), "计算机科学博士生")
        self.assertTrue(self.test_dir.exists())
        self.assertEqual(self.agent.config.llm_model, "zhipu")
        self.assertEqual(len(self.agent.agent.tools), 1)
        
        # 只比较工具的名称
        tool = self.agent.agent.tools[0]
        self.assertEqual(tool.name, self.mock_tool.name)
        
    def test_prompts_format(self):
        """测试提示词格式"""
        required_prompts = [
            "literature_search",
            "relevance_assessment",
            "section_writing"
        ]
        for prompt_name in required_prompts:
            self.assertIn(prompt_name, self.agent.config.prompts)
            self.assertTrue(isinstance(self.agent.config.prompts[prompt_name], str))
            
    def test_search_literature(self):
        """测试文献搜索"""
        # 设置模拟任务的返回值
        search_json = {
            "search_criteria": {
                "keywords": ["深度学习", "自然语言处理"],
                "filters": ["近五年", "高引用"]
            },
            "expected_results": {
                "min_papers": 10,
                "relevance_threshold": 0.7
            }
        }
        self.mock_task.set_execute_result(json.dumps(search_json))
        
        keywords = ["深度学习", "自然语言处理"]
        result = self.agent.search_literature(keywords)
        
        # 验证搜索结果
        self.assertIsInstance(result, dict)
        self.assertIn("search_criteria", result)
        self.assertIn("expected_results", result)
        self.assertEqual(result["search_criteria"]["keywords"], keywords)
            
    def test_assess_relevance(self):
        """测试相关性评估"""
        # 设置模拟任务的返回值
        assessment_json = {
            "relevance_score": 0.85,
            "relevance_aspects": [
                {
                    "aspect": "主题相关性",
                    "score": 0.9,
                    "explanation": "研究方向高度相关"
                }
            ],
            "recommendation": "保留",
            "reason": "内容与研究主题高度相关"
        }
        self.mock_task.set_execute_result(json.dumps(assessment_json))
        
        content = "这是一篇关于深度学习的论文..."
        task = "研究深度学习在自然语言处理中的应用"
        result = self.agent.assess_relevance(content, task)
        
        # 验证评估结果
        self.assertIsInstance(result, dict)
        self.assertIn("relevance_score", result)
        self.assertIn("relevance_aspects", result)
        self.assertIn("recommendation", result)
        self.assertIn("reason", result)
            
    def test_write_section(self):
        """测试段落撰写"""
        # 设置模拟任务的返回值
        section_json = {
            "section_content": "这是一段关于深度学习的综述...",
            "citations": [
                {
                    "text": "引用的内容",
                    "paper_id": "paper001",
                    "chunk": "chunk1"
                }
            ],
            "key_points": ["深度学习的发展", "主要应用领域"]
        }
        self.mock_task.set_execute_result(json.dumps(section_json))
        
        task = "总结深度学习的发展历程"
        references = [
            {
                "paper_id": "paper001",
                "title": "深度学习综述",
                "content": "这是论文的内容..."
            }
        ]
        result = self.agent.write_section(task, references)
        
        # 验证撰写结果
        self.assertIsInstance(result, dict)
        self.assertIn("section_content", result)
        self.assertIn("citations", result)
        self.assertIn("key_points", result)
        
    def test_knowledge_base_operations(self):
        """测试知识库操作"""
        # 测试添加到知识库
        paper_id = "test_paper_001"
        content = {
            "title": "测试论文",
            "content": "这是论文内容..."
        }
        
        # 添加文献
        success = self.agent.add_to_knowledge_base(paper_id, content)
        self.assertTrue(success)
        
        # 获取文献
        retrieved_content = self.agent.get_from_knowledge_base(paper_id)
        self.assertEqual(retrieved_content, content)
        
        # 获取不存在的文献
        non_existent = self.agent.get_from_knowledge_base("non_existent")
        self.assertIsNone(non_existent)
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试空输入
        with self.assertRaises(ValueError):
            self.agent.search_literature([])
            
        with self.assertRaises(ValueError):
            self.agent.assess_relevance("", "")
            
        with self.assertRaises(ValueError):
            self.agent.write_section("", [])
            
if __name__ == "__main__":
    unittest.main() 