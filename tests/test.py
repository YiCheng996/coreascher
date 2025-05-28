# 更新为使用 importlib.metadata
import sys
from importlib.metadata import version, PackageNotFoundError

try:
    print(f"crewai-tools 版本: {version('crewai-tools')}")
except PackageNotFoundError:
    print("未找到 crewai-tools 包")