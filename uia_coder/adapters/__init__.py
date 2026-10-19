import os
from typing import Dict, List, Optional, Type
from uia_coder.core.base_adapter import BaseUIAGraphBuilder
from uia_coder.adapters.javascript_adapter import JavaScriptUIAGraphBuilder
from uia_coder.adapters.python_adapter import PythonUIAGraphBuilder
from uia_coder.adapters.typescript_adapter import TypeScriptUIAGraphBuilder
from uia_coder.adapters.rust_adapter import RustUIAGraphBuilder
from uia_coder.adapters.go_adapter import GoUIAGraphBuilder
from uia_coder.adapters.csharp_adapter import CSharpUIAGraphBuilder


class AdapterRegistry:
    """
    語言適配器註冊中心 (Factory / Registry Pattern)
    依檔案副檔名自動分發對應語言的語意圖譜建構器。
    """

    _registry: Dict[str, Type[BaseUIAGraphBuilder]] = {}
    _instances: Dict[str, BaseUIAGraphBuilder] = {}

    @classmethod
    def register(cls, adapter_cls: Type[BaseUIAGraphBuilder]):
        dummy = adapter_cls()
        for ext in dummy.supported_extensions:
            cls._registry[ext.lower()] = adapter_cls

    @classmethod
    def get_adapter(cls, file_path: str) -> BaseUIAGraphBuilder:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext not in cls._registry:
            supported = ", ".join(sorted(cls._registry.keys()))
            raise ValueError(
                f"尚未支援副檔名 '{ext}' 的程式語言！\n目前已支援副檔名: [{supported}]"
            )

        if ext not in cls._instances:
            cls._instances[ext] = cls._registry[ext]()

        return cls._instances[ext]

    @classmethod
    def list_supported_languages(cls) -> List[Dict[str, str]]:
        languages = []
        seen = set()
        for ext, adapter_cls in cls._registry.items():
            if adapter_cls not in seen:
                seen.add(adapter_cls)
                inst = adapter_cls()
                languages.append({
                    "language": inst.language_name,
                    "extensions": ", ".join(sorted(inst.supported_extensions))
                })
        return languages


# 自動註冊已實作之適配器 (JavaScript, Python, TypeScript, Rust, Go, C#)
AdapterRegistry.register(JavaScriptUIAGraphBuilder)
AdapterRegistry.register(PythonUIAGraphBuilder)
AdapterRegistry.register(TypeScriptUIAGraphBuilder)
AdapterRegistry.register(RustUIAGraphBuilder)
AdapterRegistry.register(GoUIAGraphBuilder)
AdapterRegistry.register(CSharpUIAGraphBuilder)


def get_adapter_for_file(file_path: str) -> BaseUIAGraphBuilder:
    return AdapterRegistry.get_adapter(file_path)


__all__ = [
    "AdapterRegistry",
    "get_adapter_for_file",
    "JavaScriptUIAGraphBuilder",
    "PythonUIAGraphBuilder",
    "TypeScriptUIAGraphBuilder",
    "RustUIAGraphBuilder",
    "GoUIAGraphBuilder",
    "CSharpUIAGraphBuilder",
]
