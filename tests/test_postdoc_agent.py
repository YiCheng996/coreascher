"""
测试博士后代理模块
"""

import unittest
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from pydantic import BaseModel
from src.coreascher.agents.postdoc_agent import PostDocAgent
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

class TestPostDocAgent(unittest.TestCase):
    """PostDocAgent测试类"""
    
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
        patcher = patch('src.coreascher.agents.postdoc_agent.Task', return_value=self.mock_task)
        patcher.start()
        self.addCleanup(patcher.stop)
        
        self.agent = PostDocAgent(
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
        self.assertEqual(agent_dict.get('role'), "计算机科学博士后研究员")
        self.assertTrue(self.test_dir.exists())
        self.assertEqual(self.agent.config.llm_model, "zhipu")
        self.assertEqual(len(self.agent.agent.tools), 1)
        
        # 只比较工具的名称
        tool = self.agent.agent.tools[0]
        self.assertEqual(tool.name, self.mock_tool.name)
        
    def test_prompts_format(self):
        """测试提示词格式"""
        required_prompts = [
            "framework_analysis",
            "task_assignment",
            "paper_integration"
        ]
        for prompt_name in required_prompts:
            self.assertIn(prompt_name, self.agent.config.prompts)
            self.assertTrue(isinstance(self.agent.config.prompts[prompt_name], str))
            
    def test_analyze_framework(self):
        """测试框架分析"""
        # 设置模拟任务的返回值
        analysis_json = {
            "analysis": {
                "strengths": ["结构清晰", "主题明确"],
                "weaknesses": ["缺少实验设计", "讨论不够深入"],
                "suggestions": ["添加实验章节", "加强讨论部分"]
            }
        }
        self.mock_task.set_execute_result(json.dumps(analysis_json))
        
        framework = {
            "sections": [
                {
                    "title": "引言",
                    "content": "研究背景和目标"
                }
            ]
        }
        result = self.agent.analyze_framework(framework)
        
        # 验证分析结果
        self.assertIsInstance(result, dict)
        self.assertIn("analysis", result)
        self.assertIn("strengths", result["analysis"])
        self.assertIn("weaknesses", result["analysis"])
        self.assertIn("suggestions", result["analysis"])
            
    def test_assign_tasks(self):
        """测试任务分配"""
        # 设置模拟任务的返回值
        assignment_json = {
            "keywords": ["深度学习", "自然语言处理"],
            "requirements": ["近五年文献", "高引用论文"],
            "expected_outcomes": ["文献综述", "技术对比"]
        }
        self.mock_task.set_execute_result(json.dumps(assignment_json))
        
        task = "研究深度学习在自然语言处理中的应用"
        result = self.agent.assign_tasks(task)
        
        # 验证分配结果
        self.assertIsInstance(result, dict)
        self.assertIn("keywords", result)
        self.assertIn("requirements", result)
        self.assertIn("expected_outcomes", result)
            
    def test_integrate_paper(self):
        """测试论文整合"""
        # 设置模拟任务的返回值
        integration_json = {
            "integrated_content": "整合后的论文内容...",
            "modifications": [
                {
                    "type": "结构调整",
                    "description": "重新组织章节顺序"
                }
            ]
        }
        self.mock_task.set_execute_result(json.dumps(integration_json))
        
        content = "这是一段论文内容..."
        result = self.agent.integrate_paper(content)
        
        # 验证整合结果
        self.assertIsInstance(result, dict)
        self.assertIn("integrated_content", result)
        self.assertIn("modifications", result)
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试空输入
        with self.assertRaises(ValueError):
            self.agent.analyze_framework({})
            
        with self.assertRaises(ValueError):
            self.agent.assign_tasks("")
            
        with self.assertRaises(ValueError):
            self.agent.integrate_paper("")
            
if __name__ == "__main__":
    unittest.main() 