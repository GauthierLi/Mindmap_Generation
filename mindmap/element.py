from typing import Any 

class Node(object):
    def __init__(self, title: str, level: int = 1) -> None:
        self.title = title
        self.children = []
        self.pre = None
        self.level = level
        self.explandable = True

    def add_child(self, child):
        self.children.append(child)
        child.pre = self
    
    @property
    def str(self):
        if self.children == []:
            return self.level * '#' + ' ' + self.title
        else:
            base_strings = self.level * '#' + ' ' + self.title + '\n'
            for child in self.children:
                base_strings += child.str + '\n'
            return base_strings.strip()
            
    def __str__(self):
        return self.str
        
        