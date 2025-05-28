#!/usr/bin/env python
"""
文献综述系统启动脚本
"""

import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.coreascher.main import main

if __name__ == "__main__":
    main() 