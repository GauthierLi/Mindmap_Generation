from .element import Node
from .mindmap import MindMapGenerator

class MindMap2PPT(MindMapGenerator):
    def __init__(self, 
                 llm_api,
                 init_prompt: str,
                 modified_prompt: str,
                 expland_prompt: str,
                 ppt_expland_prompt: str, 
                 **kwargs) -> None:
        super(MindMap2PPT, self).__init__(
            llm_api,
            init_prompt,
            modified_prompt,
            expland_prompt,
            **kwargs
        )
        self.ppt_expland_prompt = ppt_expland_prompt
        
    def mmp2ppt_node(self, node: Node) -> Node:
        """将脑图转为固定四层的一个脑图"""
        if node.level < 4 and node.children == []:
            node = self.expland(node, node.title, keep_level=False)
            for child in node.children:
                self.mmp2ppt_node(child)
        if node.level > 4:
            pre_node = node.pre 
            pre_node.remove(node)
        return node 
    
    def expland_content_from_pptnode(self, node: Node) -> Node:
        """根据四级标题扩写内容"""
        if node.level == 4:
            preview_info = []
            find_node = node 
            while find_node.pre is not None:
                preview_info.append(find_node.format_title)
                find_node = find_node.pre
            preview_info.append(find_node.format_title)
            preview_info.reverse()
            assert len(preview_info) == 4
            result = \
            self.llm_api(
                self.ppt_expland_prompt.format(
                    '\n'.join(preview_info[:-1]), 
                    preview_info[-1].replace('#### ', ' ')
                )
            )
            node.title = node.title + '：' + result
            
        for child in node.children:
            self.expland_content_from_pptnode(child)
        return node
    
    def mmp2ppt(self, root_node: Node) -> str:
        ppt_node = self.mmp2ppt_node(root_node)
        expland_ppt_content_node = \
            self.expland_content_from_pptnode(ppt_node)
        return expland_ppt_content_node.str.replace('#### ', '- ')
            
    
    
    
    
    
                        
        