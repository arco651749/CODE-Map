import os
from typing import Dict, List, Optional, Type
from code_map.core.base_adapter import BaseCodeMapBuilder
from code_map.adapters.javascript_adapter import JavaScriptCodeMapBuilder
from code_map.adapters.python_adapter import PythonCodeMapBuilder
from code_map.adapters.typescript_adapter import TypeScriptCodeMapBuilder
from code_map.adapters.rust_adapter import RustCodeMapBuilder
from code_map.adapters.go_adapter import GoCodeMapBuilder
from code_map.adapters.csharp_adapter import CSharpCodeMapBuilder
from code_map.adapters.html_adapter import HTMLCodeMapBuilder
from code_map.adapters.xaml_adapter import XAMLCodeMapBuilder


class AdapterRegistry:
    """
    語言適配器註冊中心 (Factory / Registry Pattern)
    依檔案副檔名自動分發對應語言的語意圖譜建構器。
    """

    _registry: Dict[str, Type[BaseCodeMapBuilder]] = {}
    _instances: Dict[str, BaseCodeMapBuilder] = {}

    @classmethod
    def register(cls, adapter_cls: Type[BaseCodeMapBuilder]):
        dummy = adapter_cls()
        for ext in dummy.supported_extensions:
            cls._registry[ext.lower()] = adapter_cls

    @classmethod
    def get_adapter(cls, file_path: str) -> BaseCodeMapBuilder:
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


# 自動註冊已實作之適配器 (JavaScript, Python, TypeScript, Rust, Go, C#, HTML)
AdapterRegistry.register(JavaScriptCodeMapBuilder)
AdapterRegistry.register(PythonCodeMapBuilder)
AdapterRegistry.register(TypeScriptCodeMapBuilder)
AdapterRegistry.register(RustCodeMapBuilder)
AdapterRegistry.register(GoCodeMapBuilder)
AdapterRegistry.register(CSharpCodeMapBuilder)
AdapterRegistry.register(HTMLCodeMapBuilder)
AdapterRegistry.register(XAMLCodeMapBuilder)


def get_adapter_for_file(file_path: str) -> BaseCodeMapBuilder:
    return AdapterRegistry.get_adapter(file_path)


__all__ = [
    "AdapterRegistry",
    "get_adapter_for_file",
    "JavaScriptCodeMapBuilder",
    "PythonCodeMapBuilder",
    "TypeScriptCodeMapBuilder",
    "RustCodeMapBuilder",
    "GoCodeMapBuilder",
    "CSharpCodeMapBuilder",
    "HTMLCodeMapBuilder",
    "XAMLCodeMapBuilder",
]
