#!/usr/bin/env python3
"""
API 文档构建器 - 构建 OpenAPI 规范
"""

import re
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


def build_api_doc(routes_path: str, title: str = "API Documentation", 
                  version: str = "1.0.0") -> Dict[str, Any]:
    """构建 API 文档 (OpenAPI 3.0 格式)"""
    p = Path(routes_path).resolve()
    
    if not p.exists():
        return {"error": f"路径不存在: {routes_path}"}
    
    if p.is_file():
        files = [p]
    else:
        files = list(p.rglob('*.py'))
        files.extend(p.rglob('*.js'))
        files.extend(p.rglob('*.ts'))
        files = [f for f in files if not any(part.startswith('.') for part in f.parts)][:50]
    
    if not files:
        return {"error": "未找到路由文件", "path": routes_path}
    
    # 提取路由
    endpoints = []
    for f in files:
        ext = f.suffix
        if ext == '.py':
            endpoints.extend(_extract_python_routes(f))
        elif ext in ('.js', '.ts'):
            endpoints.extend(_extract_js_routes(f))
    
    # 构建 OpenAPI spec
    spec = _build_openapi_spec(endpoints, title, version)
    
    return {
        "title": title,
        "version": version,
        "source_path": str(p),
        "files_scanned": len(files),
        "endpoints_found": len(endpoints),
        "openapi_spec": spec,
        "endpoints_summary": [
            {
                "method": ep["method"].upper(),
                "path": ep["path"],
                "summary": ep.get("summary", ""),
                "source_file": ep.get("source_file", "")
            }
            for ep in endpoints
        ]
    }


def _extract_python_routes(file_path: Path) -> List[Dict[str, Any]]:
    """从 Python 文件提取路由（Flask/FastAPI/Django 风格）"""
    try:
        source = file_path.read_text(encoding='utf-8')
    except Exception:
        return []
    
    endpoints = []
    
    # Flask 风格: @app.route('/path', methods=['GET'])
    flask_pattern = r'@\w+\.route\s*\(\s*[\'"]([^\'"]+)[\'"]\s*(?:,\s*methods\s*=\s*\[([^\]]+)\])?\s*\)'
    for match in re.finditer(flask_pattern, source):
        path = match.group(1)
        methods_str = match.group(2)
        if methods_str:
            methods = re.findall(r'[\'"](\w+)[\'"]', methods_str)
        else:
            methods = ['GET']
        
        # 尝试获取函数名
        func_match = re.search(
            rf'{re.escape(match.group(0))}\s*def\s+(\w+)',
            source[match.start():match.start()+500]
        )
        func_name = func_match.group(1) if func_match else "unknown"
        
        for method in methods:
            endpoints.append({
                "method": method.lower(),
                "path": path,
                "function": func_name,
                "summary": f"{func_name} 处理函数",
                "framework": "flask",
                "source_file": str(file_path)
            })
    
    # FastAPI 风格: @app.get('/path'), @router.post('/path')
    fastapi_pattern = r'@(?:app|router)\.(get|post|put|delete|patch|options|head)\s*\(\s*[\'"]([^\'"]+)[\'"]'
    for match in re.finditer(fastapi_pattern, source):
        method = match.group(1)
        path = match.group(2)
        
        func_match = re.search(
            rf'{re.escape(match.group(0))}[\s\S]*?def\s+(\w+)',
            source[match.start():match.start()+500]
        )
        func_name = func_match.group(1) if func_match else "unknown"
        
        endpoints.append({
            "method": method,
            "path": path,
            "function": func_name,
            "summary": f"{func_name} 处理函数",
            "framework": "fastapi",
            "source_file": str(file_path)
        })
    
    # Django 风格: path('url/', views.view_func)
    django_pattern = r'(?:path|re_path)\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*(\w+)'
    for match in re.finditer(django_pattern, source):
        url_pattern = match.group(1)
        view_func = match.group(2)
        
        # 转换 Django URL 到 OpenAPI 路径
        path = '/' + url_pattern.replace('<str:', '{').replace('<int:', '{').replace('>', '}')
        if not path.startswith('/'):
            path = '/' + path
        
        endpoints.append({
            "method": "get",  # Django 不在此指定方法
            "path": path.rstrip('/'),
            "function": view_func,
            "summary": f"{view_func} 视图",
            "framework": "django",
            "source_file": str(file_path)
        })
    
    return endpoints


def _extract_js_routes(file_path: Path) -> List[Dict[str, Any]]:
    """从 JS/TS 文件提取路由 (Express/Koa 风格)"""
    try:
        source = file_path.read_text(encoding='utf-8')
    except Exception:
        return []
    
    endpoints = []
    
    # Express: app.get('/path', handler) / router.post('/path', ...)
    express_pattern = r'(?:app|router)\.(get|post|put|delete|patch|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
    for match in re.finditer(express_pattern, source):
        method = match.group(1)
        path = match.group(2)
        
        endpoints.append({
            "method": method if method != "all" else "get",
            "path": path,
            "function": "handler",
            "summary": f"{method.upper()} {path}",
            "framework": "express",
            "source_file": str(file_path)
        })
    
    # Koa: router.get('/path', ...)
    koa_pattern = r'router\.(get|post|put|delete|patch)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
    for match in re.finditer(koa_pattern, source):
        method = match.group(1)
        path = match.group(2)
        
        endpoints.append({
            "method": method,
            "path": path,
            "function": "handler",
            "summary": f"{method.upper()} {path}",
            "framework": "koa",
            "source_file": str(file_path)
        })
    
    return endpoints


def _build_openapi_spec(endpoints: List[Dict], title: str, version: str) -> Dict[str, Any]:
    """构建 OpenAPI 3.0 规范"""
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": title,
            "version": version,
            "description": f"自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "contact": {}
        },
        "paths": {},
        "components": {
            "schemas": {}
        }
    }
    
    for ep in endpoints:
        path = ep["path"]
        method = ep["method"].lower()
        
        # 确保路径以 / 开头
        if not path.startswith('/'):
            path = '/' + path
        
        if path not in spec["paths"]:
            spec["paths"][path] = {}
        
        operation = {
            "summary": ep.get("summary", ""),
            "operationId": f"{ep.get('function', 'unknown')}_{method}",
            "tags": [ep.get("framework", "api")],
            "responses": {
                "200": {
                    "description": "成功响应",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object"
                            }
                        }
                    }
                },
                "400": {"description": "请求参数错误"},
                "401": {"description": "未授权"},
                "404": {"description": "资源不存在"},
                "500": {"description": "服务器内部错误"}
            }
        }
        
        # 提取路径参数
        path_params = re.findall(r'\{(\w+)\}', path)
        if path_params:
            operation["parameters"] = [
                {
                    "name": param,
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"}
                }
                for param in path_params
            ]
        
        # POST/PUT/PATCH 方法添加请求体
        if method in ("post", "put", "patch"):
            operation["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "description": "请求体 (请根据实际接口补充)"
                        }
                    }
                }
            }
        
        spec["paths"][path][method] = operation
    
    return spec
