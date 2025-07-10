"""
字符串处理工具函数
"""
import re
from typing import List

def to_snake_case(text: str) -> str:
    """
    将文本转换为蛇形命名法
    
    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("helloWorld")
        'hello_world'
        >>> to_snake_case("hello-world")
        'hello_world'
        >>> to_snake_case("hello world")
        'hello_world'
    """
    # 替换非字母数字字符为空格
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    
    # 在大写字母前添加空格
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
    
    # 转换为小写并替换空格为下划线
    return re.sub(r'\s+', '_', text.lower()).strip('_')

def to_pascal_case(text: str) -> str:
    """
    将文本转换为帕斯卡命名法 (PascalCase)
    
    Examples:
        >>> to_pascal_case("hello_world")
        'HelloWorld'
        >>> to_pascal_case("hello-world")
        'HelloWorld'
        >>> to_pascal_case("hello world")
        'HelloWorld'
    """
    # 先转换为蛇形命名法以统一处理
    snake_case = to_snake_case(text)
    
    # 将每个单词首字母大写
    return ''.join(word.capitalize() for word in snake_case.split('_'))

def to_camel_case(text: str) -> str:
    """
    将文本转换为驼峰命名法 (camelCase)
    
    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("HelloWorld")
        'helloWorld'
        >>> to_camel_case("hello-world")
        'helloWorld'
    """
    pascal = to_pascal_case(text)
    return pascal[0].lower() + pascal[1:] if pascal else ''

def to_kebab_case(text: str) -> str:
    """
    将文本转换为短横线命名法 (kebab-case)
    
    Examples:
        >>> to_kebab_case("hello_world")
        'hello-world'
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("helloWorld")
        'hello-world'
    """
    # 先转换为蛇形命名法以统一处理
    snake_case = to_snake_case(text)
    
    # 将下划线替换为短横线
    return snake_case.replace('_', '-')

def pluralize(text: str) -> str:
    """
    将单词转换为复数形式
    这是一个简化版本，只处理常见的英语复数规则
    
    Examples:
        >>> pluralize("user")
        'users'
        >>> pluralize("category")
        'categories'
        >>> pluralize("box")
        'boxes'
    """
    # 特殊情况
    irregular = {
        "child": "children",
        "person": "people",
        "man": "men",
        "woman": "women",
        "tooth": "teeth",
        "foot": "feet",
        "mouse": "mice",
        "goose": "geese",
    }
    
    # 处理特殊情况
    if text.lower() in irregular:
        return irregular[text.lower()]
    
    # 处理已经是复数的单词
    if text.lower().endswith(('s', 'ss', 'sh', 'ch', 'x', 'z')):
        return text + 'es'
    
    # 处理以辅音字母+y结尾的单词
    if text.endswith('y') and len(text) > 1 and text[-2] not in 'aeiou':
        return text[:-1] + 'ies'
    
    # 默认情况：添加s
    return text + 's'

def singularize(text: str) -> str:
    """
    将单词转换为单数形式
    这是一个简化版本，只处理常见的英语单数规则
    
    Examples:
        >>> singularize("users")
        'user'
        >>> singularize("categories")
        'category'
        >>> singularize("boxes")
        'box'
    """
    # 特殊情况
    irregular = {
        "children": "child",
        "people": "person",
        "men": "man",
        "women": "woman",
        "teeth": "tooth",
        "feet": "foot",
        "mice": "mouse",
        "geese": "goose",
    }
    
    # 处理特殊情况
    if text.lower() in irregular:
        return irregular[text.lower()]
    
    # 处理以ies结尾的单词
    if text.endswith('ies') and len(text) > 3:
        return text[:-3] + 'y'
    
    # 处理以es结尾的单词
    if text.endswith('es') and len(text) > 2:
        if text.endswith(('sses', 'shes', 'ches', 'xes', 'zes')):
            return text[:-2]
        return text[:-1]
    
    # 处理以s结尾的单词
    if text.endswith('s') and len(text) > 1:
        return text[:-1]
    
    # 默认情况：保持不变
    return text 