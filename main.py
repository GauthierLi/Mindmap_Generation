from mindmap import MindMapGenerator, MindMap2PPT
from apis import WENXIN4
from instruction import MODIFIED_PROMPT, EXPLAND_PROMPT, \
INIT_PROMPT, MMP2PPT_EXPLAND_PROMPT

text = "绿色飞机天上飞"
generator = MindMap2PPT(WENXIN4, INIT_PROMPT, MODIFIED_PROMPT, EXPLAND_PROMPT, MMP2PPT_EXPLAND_PROMPT)
root = generator.init_mindmap(text)
# generator.expland(root, '绿色飞机', True)
# generator.expland(root, '绿色飞机', False)
ppt = generator.mmp2ppt(root)
print(ppt)
