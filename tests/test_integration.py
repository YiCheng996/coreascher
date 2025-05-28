def test_full_workflow():
    # 测试端到端流程
    result = run_research(topic="AI教育系统")
    assert 'research_framework' in result
    assert 'paper_review' in result
    assert len(result['research_framework']) >= 2000 