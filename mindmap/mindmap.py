"""
欢迎使用我的代码库：
    pip install GauDLutils
    
@author: Gauthierli
@email: lwklxh@163.com
@date: 2023-11-24

Gusse what's this? 
[25105, 26412, 23558, 24515, 21521, 26126, 26376, 65292, 22856, 20309, 26126, 26376, 29031, 27807, 28192, 12290]
"""
from .element import Node
from typing import Literal
try:
    from gutils import print_run_time
except Exception as e:
    print(e)
    raise ImportError('Please install gutils by following commands: pip install GauDLutils')

class MindMapGenerator(object):
    def __init__(self, 
                 llm_api,
                 init_prompt: str,
                 modified_prompt: str,
                 expland_prompt: str):
        """
            分为三个prompt，第一个是一次性生成一个脑图；
            第二个是基于现有的脑图，然后修改内容的prompt；
        """
        self.llm_api = llm_api
        self.init_prompt = init_prompt
        self.modified_prompt = modified_prompt
        self.expland_prompt = expland_prompt
    
    @print_run_time
    def init_mindmap(self, query: str) -> Node:
        text = self.llm_api(self.init_prompt.format(query))
        if '* ' in text:
            text = self.markdown_style_transfer(text)
        if '-' in text:
            text = self.convert_dash_to_headline(text)
        root = None
        current_node = None
        print(text)
        for line in text.split('\n'):
            if not line.startswith('#'):
                continue
            try:
                if line.strip():
                    level = line.count('#')
                    title = line.strip('# ').strip()
                    if title.endswith('<EOS>'):
                        new_node = Node(title.strip('<EOS>'), level)
                        # 是否需要设置叶子结点不可展开？？2PPT时候如果深度不够叶子结点也需要展开
                        # new_node.explandable = False
                    else:
                        new_node = Node(title, level)
                    
                    if level == 1:
                        root = new_node
                    else:
                        while current_node and current_node.level >= level:
                            current_node = current_node.pre
                        current_node.add_child(new_node)
                    current_node = new_node
            except Exception as e:
                print(e)
                print('line {} 解析失败'.format(line))
        return root
    
    def markdown_style_transfer(self, text: str) -> str:
        lines = text.split('\n')
        converted_lines = []

        for line in lines:
            if line.strip().startswith('*'):
                # 计算缩进层级（每个缩进通常为4个空格）
                indent_level = line.count('    ')  
                hash_prefix = '#' * (indent_level + 1)
                converted_line = hash_prefix + ' ' + line.lstrip().lstrip('*').strip()
                converted_lines.append(converted_line)
            else:
                converted_lines.append(line)

        return '\n'.join(converted_lines)
    
    @print_run_time
    def convert_dash_to_headline(self, text: str) -> str:
        lines = text.split('\n')
        current_level = 0  # 当前标题的级别
        converted_lines = []

        for line in lines:
            if line.startswith('#'):
                current_level = line.count('#')
                converted_lines.append(line)
            elif line.strip().startswith('-'):
                # 为 '-' 替换为比当前标题更高一级的 '#'
                new_line = '#' * (current_level + 1) + line.strip().strip('-') + '<EOS>'
                converted_lines.append(new_line)
            else:
                converted_lines.append(line)
        return '\n'.join(converted_lines)
    
    @print_run_time
    def find_node(self, root: Node, title: str) -> Node:
        if root.title == title:
            return root
        
        if root.children == []:
            return None
        else:
            for nd in root.children:
                result = self.find_node(nd, title)
                if result is not None:
                    return result                    
        return None
    
    def regenerate(self, 
                   root: Node, 
                   text: str) -> Node:        
        target_node = self.find_node(root, text)
        if target_node is None:
            print('Not found target node')
            return root

        all_heads = []
        find_node = target_node.pre
        for subnode in find_node.children:
            if subnode.title != text:
                all_heads.append(subnode.level * '#' \
                    + ' ' + subnode.pre.title)
        while find_node.pre is not None:
            all_heads.append(find_node.pre.level * '#' \
                + ' ' + find_node.pre.title)
            find_node = find_node.pre
        all_heads.reverse()
        subheadline = '\n'.join(all_heads)
        new_content = self.llm_api(
            self.modified_prompt.format(subheadline)
            )
        # 如果需要后处理，在这里写
        # xxxx
        target_node.title = new_content
        return root
        
    def expland(self, 
                root: Node, 
                text: str,
                keep_level: bool = True) -> Node:
        target_node = self.find_node(root, text)
        if target_node is None:
            print('Not found target node')
            return root
        if not target_node.explandable:
            print('This node is not explandable')
            return root
        all_heads = []
        if keep_level:
            find_node = target_node
            for subnode in find_node.children:
                all_heads.append(subnode.level * '#' \
                    + ' ' + subnode.title)
            # import pdb; pdb.set_trace()
            while find_node is not None:
                all_heads.append(find_node.level * '#' \
                    + ' ' + find_node.title)
                find_node = find_node.pre
            all_heads.reverse()
            subheadline = '\n'.join(all_heads)
            # 和改写逻辑一样，只不过改写需要替换原来的，扩写则是增加一个
            new_content = self.llm_api(
                self.modified_prompt.format(subheadline)
                )
            # 如果需要后处理，在这里写
            # xxxx
            new_node_level = target_node.level 
            new_node = Node(new_content.strip('#'*new_node_level).strip(), new_node_level)
            target_node.pre.add_child(new_node)
            return root
        else:
            # 深度增加的扩写逻辑
            find_node = target_node
            while find_node is not None:
                all_heads.append(find_node.level * '#' \
                    + ' ' + find_node.title)
                find_node = find_node.pre
            all_heads.reverse()
            subheadline = '\n'.join(all_heads)
            expland_content = self.llm_api(
                self.expland_prompt.format(subheadline)
            )
            # 后处理
            expland_content = expland_content.replace('*', '-')
            expland_level = target_node.level + 1
            expland_results = [title.strip().strip('- ') for title in expland_content.split('\n') 
                              if title.strip().startswith('- ')]
            for er in expland_results:
                target_node.add_child(Node(er, expland_level))
            return root
        
    
