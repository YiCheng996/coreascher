"""
测试评审人代理模块
"""

import unittest
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from pydantic import BaseModel
from src.coreascher.agents.reviewer_agent import ReviewerAgent
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

class TestReviewerAgent(unittest.TestCase):
    """ReviewerAgent测试类"""
    
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
        patcher = patch('src.coreascher.agents.reviewer_agent.Task', return_value=self.mock_task)
        patcher.start()
        self.addCleanup(patcher.stop)
        
        self.agent = ReviewerAgent(
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
        self.assertEqual(agent_dict.get('role'), "严苛但公正的评审人")
        self.assertTrue(self.test_dir.exists())
        self.assertEqual(self.agent.config.llm_model, "zhipu")
        self.assertEqual(len(self.agent.agent.tools), 1)
        
        # 只比较工具的名称
        tool = self.agent.agent.tools[0]
        self.assertEqual(tool.name, self.mock_tool.name)
        
    def test_prompts_format(self):
        """测试提示词格式"""
        required_prompts = [
            "paper_review",
            "score_calculation",
            "feedback_generation"
        ]
        for prompt_name in required_prompts:
            self.assertIn(prompt_name, self.agent.config.prompts)
            self.assertTrue(isinstance(self.agent.config.prompts[prompt_name], str))
            
    def test_review_paper(self):
        """测试论文评审"""
        # 设置模拟任务的返回值
        review_json = {
            "summary": "这是一篇关于深度学习的论文",
            "strengths": ["方法创新", "实验充分"],
            "weaknesses": ["相关工作不足", "讨论不够深入"],
            "originality": {
                "score": 3,
                "comments": ["方法有创新", "思路新颖"]
            },
            "quality": {
                "score": 3,
                "comments": ["实验设计合理", "结果可靠"]
            },
            "clarity": {
                "score": 4,
                "comments": ["行文清晰", "结构合理"]
            },
            "significance": {
                "score": 3,
                "comments": ["对领域有贡献", "应用价值高"]
            },
            "questions": ["如何处理异常情况?", "为什么选择这个参数?"],
            "limitations": ["数据集规模小", "计算资源要求高"],
            "ethical_issues": False,
            "technical_soundness": {
                "score": 3,
                "comments": ["技术合理", "推导正确"]
            },
            "presentation": {
                "score": 4,
                "comments": ["图表清晰", "说明详细"]
            },
            "contribution": {
                "score": 3,
                "comments": ["有一定创新", "实用价值高"]
            },
            "overall_score": 8,
            "confidence": 4,
            "decision": "接受"
        }
        self.mock_task.set_execute_result(json.dumps(review_json))
        
        content = "这是一篇关于深度学习的论文..."
        paper_id = "test_paper_001"
        result = self.agent.review_paper(content, paper_id)
        
        # 验证评审结果
        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertIn("strengths", result)
        self.assertIn("weaknesses", result)
        self.assertIn("originality", result)
        self.assertIn("quality", result)
        self.assertIn("clarity", result)
        self.assertIn("significance", result)
        self.assertIn("overall_score", result)
        self.assertIn("decision", result)
            
    def test_calculate_score(self):
        """测试评分计算"""
        # 设置模拟任务的返回值
        calculation_json = {
            "weighted_scores": {
                "originality": 0.75,
                "quality": 0.75,
                "clarity": 1.0,
                "significance": 0.75
            },
            "total_score": 3.25,
            "normalized_score": 8
        }
        self.mock_task.set_execute_result(json.dumps(calculation_json))
        
        scores = {
            "originality": {"score": 3},
            "quality": {"score": 3},
            "clarity": {"score": 4},
            "significance": {"score": 3}
        }
        result = self.agent.calculate_score(scores)
        
        # 验证计算结果
        self.assertIsInstance(result, dict)
        self.assertIn("weighted_scores", result)
        self.assertIn("total_score", result)
        self.assertIn("normalized_score", result)
            
    def test_generate_feedback(self):
        """测试反馈生成"""
        # 设置模拟任务的返回值
        feedback_json = {
            "summary": "论文整体质量良好，有一定创新性",
            "detailed_feedback": [
                {
                    "aspect": "方法创新",
                    "strengths": ["思路新颖", "实现合理"],
                    "suggestions": ["可以考虑更多场景", "补充理论分析"]
                }
            ],
            "improvement_plan": [
                {
                    "priority": "高",
                    "action": "补充相关工作",
                    "expected_outcome": "增强工作的完整性"
                }
            ]
        }
        self.mock_task.set_execute_result(json.dumps(feedback_json))
        
        review = {
            "summary": "这是一篇关于深度学习的论文",
            "strengths": ["方法创新", "实验充分"],
            "weaknesses": ["相关工作不足", "讨论不够深入"]
        }
        result = self.agent.generate_feedback(review)
        
        # 验证反馈结果
        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertIn("detailed_feedback", result)
        self.assertIn("improvement_plan", result)
        
    def test_review_history(self):
        """测试评审历史"""
        # 先进行一次评审
        review_json = {
            "summary": "测试论文",
            "decision": "接受"
        }
        self.mock_task.set_execute_result(json.dumps(review_json))
        
        paper_id = "test_paper_001"
        content = "这是测试论文内容..."
        self.agent.review_paper(content, paper_id)
        
        # 获取评审历史
        history = self.agent.get_review_history(paper_id)
        self.assertIsNotNone(history)
        self.assertEqual(history["summary"], "测试论文")
        self.assertEqual(history["decision"], "接受")
        
        # 获取不存在的评审历史
        non_existent = self.agent.get_review_history("non_existent")
        self.assertIsNone(non_existent)
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试空输入
        with self.assertRaises(ValueError):
            self.agent.review_paper("")
            
        with self.assertRaises(ValueError):
            self.agent.calculate_score({})
            
        with self.assertRaises(ValueError):
            self.agent.generate_feedback({})
            
if __name__ == "__main__":
    unittest.main() 