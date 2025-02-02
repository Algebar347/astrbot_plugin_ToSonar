from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.core.platform.message_type import MessageType
import random
from aiocqhttp import CQHttp

@register("astrbot_plugin_", "Esther", "一个简单的赛博抛硬币插件", "1.0.0","https://github.com/Algebar347/astrbot_plugin_ToSonar")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.aiocqhttp_client: CQHttp = self.context.platform_manager.platform_insts[0].bot
        assert isinstance(self.aiocqhttp_client, CQHttp)

    #获取群成员信息
    #可用信息包括: group_id, user_id, nickname, card, sex, age, area, level, qq_level, 
    # join_time, last_sent_time, role
    async def get_group_member_info(self, group_id: int, user_id: int):
        return await self.aiocqhttp_client.api.call_action(
            'get_group_member_info',
            group_id=group_id,
            user_id=user_id
        )
    
    # 注册指令的装饰器。指令名为抛硬币
    @filter.command("抛硬币")
    async def tosscoin(self, event: AstrMessageEvent):       
        if event.get_message_type() == MessageType.GROUP_MESSAGE:
            group_id = event.message_obj.group_id
            user_id = event.get_sender_id()
            member_info = await self.get_group_member_info(group_id, user_id)
            member_card = member_info.get('card')
            user_name = member_card if member_card else event.get_sender_name()
        else:
            user_name = event.get_sender_name()
        outcomes = ["正面", "反面", "立起来了！"]
        weights = [0.497, 0.497, 0.006]  # 49.7% + 49.7% + 0.6% = 100%
        result = random.choices(outcomes, weights=weights)[0]
        if result == "立起来了！":
            await event.plain_result(f"{user_name}抛出一枚硬币，震惊地看着它稳稳地立在了桌子上！Sonar欢呼着给日历上的今天盖上了幸运戳ᕕ(ᐛ)ᕗ")
        yield event.plain_result(f"刹那间，{user_name}的硬币在希尔伯特空间表现出——\n{result}的绝对真实！")
    
    # 自定义的 Jinja2 模板，支持 CSS
TMPL = '''
    <div style="font-size: 64px;"> 
    <h1 style="color: black">Test</h1>

    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </div>
    '''

@filter.command("test")
async def quote(self, event: AstrMessageEvent):
    url = await self.html_render(TMPL, {"items": ["男的滚", "祥黑滚", "玩原神的滚"]}) # 第二个参数是 Jinja2 的渲染数据
    yield event.image_result(url)