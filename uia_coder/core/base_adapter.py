from abc import ABC, abstractmethod
from typing import Set
from uia_coder.core.graph import UIACodeGraph


class BaseUIAGraphBuilder(ABC):
    """
    所有語言語意圖譜建構器的抽象基礎介面 (Strategy Pattern)
    """

    @property
    @abstractmethod
    def supported_extensions(self) -> Set[str]:
        """支援的副檔名集合，例如 {'.js', '.mjs'} 或 {'.py'}"""
        pass

    @property
    @abstractmethod
    def language_name(self) -> str:
        """語言名稱，例如 'JavaScript', 'Python'"""
        pass

    @abstractmethod
    def parse_and_build(self, source_code: str, file_path: str = "main") -> UIACodeGraph:
        """
        將原始碼字串解析為標準 UIACodeGraph
        """
        pass
