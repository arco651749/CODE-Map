"""
🌲 CODE-Map Extension: CSVI Trinity Architecture Invariant Verifier
驗證所有動態載入 CSVI 專案是否符合『大一統三元架構 (Trinity Architecture)』：
1. Dimension 1: C# Backend Logic (IDriver, IModuleHandler, ICallCommand, or ViewModel)
2. Dimension 2: UI FrontPanel (Avalonia UserControl for live monitor / HMI / device view)
3. Dimension 3: Parameter Guidance UI (Wizard tab or IParameterGuidance dialog for interactive configuration)
"""
import sys
import os
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, r"d:\AntiGravity\UIA_Coder")

from code_map.adapters import AdapterRegistry

TARGET_PROJECTS = {
    "MockIO Driver": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\MODULES\IO\DRIVER\MockIO",
        "type": "Driver",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\MODULES\IO\DRIVER\MockIO.csvi"
    },
    "MockMotion Driver": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\MODULES\MOTION\DRIVER\MockMotion",
        "type": "Driver",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\MODULES\MOTION\DRIVER\MockMotion.csvi"
    },
    "MockCamera Driver": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\MODULES\CAPTURE\DRIVER\MockCamera",
        "type": "Driver",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\MODULES\CAPTURE\DRIVER\MockCamera.csvi"
    },
    "MockDAQ Driver": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\MODULES\DAQ\DRIVER\MockDAQ",
        "type": "Driver",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\MODULES\DAQ\DRIVER\MockDAQ.csvi"
    },
    "UserPanel HMI": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\PANELS\UserPanel",
        "type": "UserPanel",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\UserPanel.csvi"
    },
    "MyCsvi Command": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\EXTERNALMODULES\MyCsvi",
        "type": "ExternalCommand",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\ExternalModules\mycsvi.csvi"
    },
    "IO Module Guidance": {
        "dir": r"d:\AntiGravity\ARCOSharp\src\MODULES\IO\USERPARAMETEREDITOR",
        "type": "GuidancePlugin",
        "csvi": r"d:\AntiGravity\ARCOSharp\dist\ARCOS_Runtime\MODULES\IO\SetPort.csvi"
    }
}

def analyze_project(name, info):
    pdir = Path(info["dir"])
    ptype = info["type"]
    
    cs_adapter = AdapterRegistry.get_adapter("test.cs")
    xaml_adapter = AdapterRegistry.get_adapter("test.axaml")
    
    cs_files = list(pdir.glob("*.cs"))
    xaml_files = list(pdir.glob("*.axaml"))
    
    cs_classes = []
    cs_interfaces = set()
    cs_methods = set()
    
    # 1. Parse C# files with Tree-sitter AST
    for cs_path in cs_files:
        try:
            content = cs_path.read_text(encoding="utf-8")
        except Exception:
            content = cs_path.read_text(encoding="cp950", errors="replace")
        
        graph = cs_adapter.parse_and_build(content, file_path=str(cs_path))
        for nid, data in graph.g.nodes(data=True):
            category = data.get("category", "")
            label = data.get("label", "")
            cls_name = data.get("props", {}).get("class_name", "")
            if cls_name and cls_name not in cs_classes:
                cs_classes.append(cls_name)
            if category == "FUNCTION_DEF":
                cs_methods.add(label)
        
        # Check interfaces in text / AST
        if "IDriver" in content:
            cs_interfaces.add("IDriver")
        if "IModuleHandler" in content:
            cs_interfaces.add("IModuleHandler")
        if "ICallCommand" in content:
            cs_interfaces.add("ICallCommand")
        if "IParameterGuidance" in content:
            cs_interfaces.add("IParameterGuidance")
        if "CreateDriverView" in content:
            cs_methods.add("CreateDriverView")
        if "GetFrontPanelControl" in content:
            cs_methods.add("GetFrontPanelControl")
        if "ShowGuidanceDialogAsync" in content:
            cs_methods.add("ShowGuidanceDialogAsync")
    
    # 2. Parse Avalonia XAML files
    xaml_controls = []
    has_tab_control = False
    has_wizard_tab = False
    has_front_panel = len(xaml_files) > 0
    
    for x_path in xaml_files:
        try:
            content = x_path.read_text(encoding="utf-8")
        except Exception:
            content = x_path.read_text(encoding="cp950", errors="replace")
            
        x_graph = xaml_adapter.parse_and_build(content, file_path=str(x_path))
        for nid, data in x_graph.g.nodes(data=True):
            ctrl_type = data.get("control_type", "")
            label = data.get("label", "")
            xaml_controls.append(f"{ctrl_type}:{label}")
            if "TabControl" in ctrl_type or "TabControl" in label:
                has_tab_control = True
        
        # Check wizard tab keywords
        lower_content = content.lower()
        if "wizard" in lower_content or "導引" in content or "引導" in content or "wiz" in lower_content:
            has_wizard_tab = True

    # 3. Dimension 1: C# Code Check
    dim1_ok = False
    dim1_desc = []
    if ptype == "Driver":
        if "IDriver" in cs_interfaces:
            dim1_ok = True
            dim1_desc.append("implements IDriver")
        else:
            dim1_desc.append("MISSING IDriver")
    elif ptype == "ExternalCommand":
        if "ICallCommand" in cs_interfaces or "IModuleHandler" in cs_interfaces:
            dim1_ok = True
            dim1_desc.append("implements ICallCommand/IModuleHandler")
        else:
            dim1_desc.append("MISSING ICallCommand")
    elif ptype == "GuidancePlugin":
        if "IParameterGuidance" in cs_interfaces:
            dim1_ok = True
            dim1_desc.append("implements IParameterGuidance")
    elif ptype == "UserPanel":
        dim1_ok = len(cs_classes) > 0
        dim1_desc.append(f"Controller/ViewModel classes ({len(cs_classes)})")

    # 4. Dimension 2: UI FrontPanel Check
    dim2_ok = False
    dim2_desc = []
    if len(xaml_files) > 0:
        if ptype == "Driver":
            if "CreateDriverView" in cs_methods:
                dim2_ok = True
                dim2_desc.append(f"Avalonia XAML View + CreateDriverView() present ({[x.name for x in xaml_files]})")
            else:
                dim2_desc.append("Has XAML but missing CreateDriverView()")
        elif ptype == "UserPanel":
            dim2_ok = True
            dim2_desc.append(f"UserPanelView UserControl ({[x.name for x in xaml_files]})")
        elif ptype == "ExternalCommand" or ptype == "GuidancePlugin":
            # Check if has View or GetFrontPanelControl
            if "GetFrontPanelControl" in cs_methods or any("View" in x.name for x in xaml_files):
                dim2_ok = True
                dim2_desc.append("Has FrontPanel View / GetFrontPanelControl()")
            else:
                dim2_desc.append("No FrontPanel View (Optional or Missing)")
    else:
        dim2_desc.append("NO XAML files found")

    # 5. Dimension 3: Parameter Guidance UI Check
    dim3_ok = False
    dim3_desc = []
    if "IParameterGuidance" in cs_interfaces or "ShowGuidanceDialogAsync" in cs_methods:
        dim3_ok = True
        dim3_desc.append("implements IParameterGuidance / ShowGuidanceDialogAsync")
    elif has_wizard_tab:
        dim3_ok = True
        dim3_desc.append("TabControl embedded Driver Wizard / Parameter Builder")
    else:
        dim3_desc.append("MISSING Wizard tab & IParameterGuidance")

    # Overall Verdict
    is_fully_compliant = dim1_ok and dim2_ok and dim3_ok
    
    return {
        "name": name,
        "type": ptype,
        "dir": str(pdir),
        "dim1_cs": {"ok": dim1_ok, "detail": ", ".join(dim1_desc)},
        "dim2_ui": {"ok": dim2_ok, "detail": ", ".join(dim2_desc)},
        "dim3_guidance": {"ok": dim3_ok, "detail": ", ".join(dim3_desc)},
        "compliant": is_fully_compliant
    }

def main():
    print("=" * 80)
    print("🌲 CODE-Map: CSVI Grand Unified Trinity Architecture Compliance Verification")
    print("=" * 80)
    
    results = []
    for name, info in TARGET_PROJECTS.items():
        res = analyze_project(name, info)
        results.append(res)
        
        verdict_str = "🟢 PASS (Trinity Compliant)" if res["compliant"] else "🔴 INCOMPLETE (Missing Dimensions)"
        print(f"\n📦 [{name}] ({res['type']}) -> {verdict_str}")
        
        d1_icon = "✅" if res["dim1_cs"]["ok"] else "❌"
        d2_icon = "✅" if res["dim2_ui"]["ok"] else "❌"
        d3_icon = "✅" if res["dim3_guidance"]["ok"] else "❌"
        
        print(f"  {d1_icon} Dimension 1 [C# Backend Logic]   : {res['dim1_cs']['detail']}")
        print(f"  {d2_icon} Dimension 2 [UI FrontPanel]        : {res['dim2_ui']['detail']}")
        print(f"  {d3_icon} Dimension 3 [Parameter Guidance UI]: {res['dim3_guidance']['detail']}")

    print("\n" + "=" * 80)
    summary_compliant = sum(1 for r in results if r["compliant"])
    print(f"📊 SUMMARY: {summary_compliant}/{len(results)} CSVI Projects Fully Conform to Trinity Architecture.")
    print("=" * 80)

if __name__ == "__main__":
    main()
