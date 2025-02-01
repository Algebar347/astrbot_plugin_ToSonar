from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.all import *
import random
from aiocqhttp import CQHttp

@register("tosscoin", "Esther", "一个简单的赛博抛硬币插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.aiocqhttp_client: CQHttp = self.context.platform_manager.platform_insts[0].bot
        assert isinstance(self.aiocqhttp_client, CQHttp)

    # 注册指令的装饰器。指令名为抛硬币
    @filter.command("抛硬币")
    async def tosscoin(self, event: AstrMessageEvent):       
        user_name = event.get_sender_name()
        result = random.choice(["正面", "反面"])
        yield event.plain_result(f"{user_name}抛出一枚硬币，结果是：{result}。")
    
    async def get_group_member_info(self, group_id: int, user_id: int):
        return await self.aiocqhttp_client.api.call_action(
            'get_group_member_info',
            group_id=group_id,
            user_id=user_id
        )

    @filter.command('test')
    async def test(self, event: AstrMessageEvent):
        if event.get_message_type() == MessageType.GROUP_MESSAGE:
            group_id = event.message_obj.group_id
            user_id = event.get_sender_id()
            member_info = await self.get_group_member_info(group_id, user_id)
            member_info_text =str(member_info)
            yield event.plain_result(member_info_text)