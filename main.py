from mindmap import MindMapGenerator
from apis import WENXIN4
from instruction import MODIFIED_PROMPT, EXPLAND_PROMPT

# 示例文本
text = """
* 民航飞机的发展史
    * 早期民航飞机
        * 莱特兄弟的飞行器
            * 飞行器的构造
            * 飞行器的特点
        * 其他早期飞行器
            * 其他飞行器的构造
            * 其他飞行器的特点
    * 二战时期的民航飞机
        * 军用运输机
            * C-100“大力神”运输机
            * 其他军用运输机
        * 民航客机的兴起
            * 波音247
            * 道格拉斯DC-3
    * 喷气式客机的兴起
        * 英国的喷气式客机
            * “彗星”客机
            * 其他英国喷气式客机
        * 美国的喷气式客机
            * “星座”客机
            * 其他美国喷气式客机
    * 现代民航飞机的发展
        * 高效能窄体客机
            * 波音737
            * 空中客车A320
        * 长途宽体客机
            * 波音747
            * 空中客车A380
    * 绿色民航飞机的发展
        * 生物燃料的使用
            * 生物燃料的应用
            * 生物燃料的优势与挑战
        * 节能减排技术
            * 节能减排技术的应用
            * 节能减排技术的挑战与前景
"""
generator = MindMapGenerator(WENXIN4, 'init_prompt', MODIFIED_PROMPT, EXPLAND_PROMPT)
root = generator.init_mindmap(text)
# print(root.str)
# new_root = generator.regenerate(root, '空中客车A380')
# print(new_root.str)
# print('\n')
# root = generator.expland(root, '绿色民航飞机的发展', True)
# print(root.str)
root = generator.expland(root, '波音747', False)
print(root.str)