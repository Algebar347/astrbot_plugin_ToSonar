from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import random

@register("tosscoin", "Esther", "一个简单的赛博抛硬币插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # 注册指令的装饰器。指令名为抛硬币
    @filter.command("抛硬币")
    async def tosscoin(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        result = random.choice(["正面", "反面"])
        yield event.plain_result(f"{user_name}抛出一枚硬币，结果是：\n{result}\n想必您已经有了自己的答案。")
