"""
工具函数测试
"""
import pytest
from fastapi_generator.utils.string_utils import (
    to_snake_case,
    to_pascal_case,
    to_camel_case,
    to_kebab_case,
    pluralize,
    singularize,
)

class TestStringUtils:
    """字符串工具函数测试"""
    
    def test_to_snake_case(self):
        """测试蛇形命名法转换"""
        assert to_snake_case("HelloWorld") == "hello_world"
        assert to_snake_case("helloWorld") == "hello_world"
        assert to_snake_case("hello-world") == "hello_world"
        assert to_snake_case("hello world") == "hello_world"
        assert to_snake_case("HELLO_WORLD") == "hello_world"
    
    def test_to_pascal_case(self):
        """测试帕斯卡命名法转换"""
        assert to_pascal_case("hello_world") == "HelloWorld"
        assert to_pascal_case("hello-world") == "HelloWorld"
        assert to_pascal_case("hello world") == "HelloWorld"
        assert to_pascal_case("HelloWorld") == "HelloWorld"
    
    def test_to_camel_case(self):
        """测试驼峰命名法转换"""
        assert to_camel_case("hello_world") == "helloWorld"
        assert to_camel_case("HelloWorld") == "helloWorld"
        assert to_camel_case("hello-world") == "helloWorld"
        assert to_camel_case("Hello World") == "helloWorld"
    
    def test_to_kebab_case(self):
        """测试短横线命名法转换"""
        assert to_kebab_case("hello_world") == "hello-world"
        assert to_kebab_case("HelloWorld") == "hello-world"
        assert to_kebab_case("helloWorld") == "hello-world"
        assert to_kebab_case("Hello World") == "hello-world"
    
    def test_pluralize(self):
        """测试单词复数形式转换"""
        assert pluralize("user") == "users"
        assert pluralize("category") == "categories"
        assert pluralize("box") == "boxes"
        assert pluralize("child") == "children"
        assert pluralize("person") == "people"
    
    def test_singularize(self):
        """测试单词单数形式转换"""
        assert singularize("users") == "user"
        assert singularize("categories") == "category"
        assert singularize("boxes") == "box"
        assert singularize("children") == "child"
        assert singularize("people") == "person" 