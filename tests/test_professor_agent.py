"""
测试 ProfessorAgent 模块

该模块测试 ProfessorAgent 类的各项功能，包括：
1. Agent 创建
2. 研究框架生成
3. 论文审阅
4. 研究指导
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
from crewai import Agent, Task
from src.coreascher.agents.professor_agent import ProfessorAgent

# 测试数据
TEST_TOPIC = "深度学习在自然语言处理中的应用"
TEST_PAPER = """
Title: 深度学习在自然语言处理中的应用研究
Abstract: 本文研究了深度学习技术在自然语言处理领域的应用...
"""
TEST_QUESTION = "如何改进BERT模型在特定领域的性能？"

@pytest.fixture
def mock_agent_config():
    """模拟 Agent 配置"""
    return {
        'professor_agent': {
            'role': '计算机领域的专家学者',
            'goal': '制定高质量的研究框架并指导研究过程',
            'backstory': '作为一名资深专家学者...'
        }
    }

@pytest.fixture
def mock_task_config():
    """模拟 Task 配置"""
    return {
        'create_research_framework': {
            'description': '生成研究框架',
            'expected_output': '研究框架'
        },
        'review_article': {
            'description': '审阅论文',
            'expected_output': '审阅意见'
        },
        'provide_guidance': {
            'description': '提供指导',
            'expected_output': '指导意见'
        }
    }

@pytest.fixture
def professor_agent(mock_agent_config, mock_task_config):
    """创建 ProfessorAgent 测试实例"""
    return ProfessorAgent(
        agents_config=mock_agent_config,
        tasks_config=mock_task_config
    )

def test_create_agent(professor_agent):
    """测试 Agent 创建"""
    agent = professor_agent.create()
    assert isinstance(agent, Agent)
    assert agent.role == '计算机领域的专家学者'
    assert agent.goal == '制定高质量的研究框架并指导研究过程'
    assert len(agent.tools) > 0

@patch('crewai.agent.Agent.execute_task')
def test_generate_framework(mock_execute, professor_agent):
    """测试研究框架生成"""
    expected_result = {'framework': '研究框架内容'}
    mock_execute.return_value = expected_result
    
    result = professor_agent.generate_framework(TEST_TOPIC)
    assert result == expected_result
    mock_execute.assert_called_once()

@patch('crewai.agent.Agent.execute_task')
def test_review_paper(mock_execute, professor_agent):
    """测试论文审阅"""
    expected_result = {'review': '审阅意见内容'}
    mock_execute.return_value = expected_result
    
    result = professor_agent.review_paper(TEST_PAPER)
    assert result == expected_result
    mock_execute.assert_called_once()

@patch('crewai.agent.Agent.execute_task')
def test_provide_guidance(mock_execute, professor_agent):
    """测试研究指导"""
    expected_result = {'guidance': '指导意见内容'}
    mock_execute.return_value = expected_result
    
    result = professor_agent.provide_guidance(TEST_QUESTION)
    assert result == expected_result
    mock_execute.assert_called_once()

def test_empty_input_validation(professor_agent):
    """测试空输入验证"""
    with pytest.raises(ValueError):
        professor_agent.generate_framework("")
    
    with pytest.raises(ValueError):
        professor_agent.review_paper("")
    
    with pytest.raises(ValueError):
        professor_agent.provide_guidance("")

@patch('crewai.agent.Agent.execute_task')
def test_error_handling(mock_execute, professor_agent):
    """测试错误处理"""
    mock_execute.side_effect = Exception("测试错误")
    
    result = professor_agent.generate_framework(TEST_TOPIC)
    assert result == {}
    
    result = professor_agent.review_paper(TEST_PAPER)
    assert result == {}
    
    result = professor_agent.provide_guidance(TEST_QUESTION)
    assert result == {} 