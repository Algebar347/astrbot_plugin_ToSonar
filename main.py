from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.core.platform.message_type import MessageType
import random,time
from aiocqhttp import CQHttp
from astrbot.api import logger

@register("astrbot_plugin_ToSonar", "Esther", "献给一只猫：赛博抛硬币、摘抄文字图片生成、etc.", "1.0.0","https://github.com/Algebar347/astrbot_plugin_ToSonar")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    #获取群成员信息
    #可用信息包括: group_id, user_id, nickname, card, sex, age, area, level, qq_level, 
    # join_time, last_sent_time, role
    async def get_group_member_info(self, group_id: int, user_id: int):
        self.aiocqhttp_client: CQHttp = self.context.platform_manager.platform_insts[0].bot
        if not isinstance(self.aiocqhttp_client, CQHttp):
            logger.error("不支持此平台") 
            return
        return await self.aiocqhttp_client.api.call_action(
            'get_group_member_info',
            group_id=group_id,
            user_id=user_id
        )
    
    # 赛博抛硬币
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
    
# 摘抄图片生成
    TMPL = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excerpt</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@200..900&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: rgb(255, 255, 255,1);
            min-height: 800px;
            min-width: 2100px;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0; /* 确保没有默认边距 */
            padding: 0;
        }

        .container {
            width: 1800px;  /* 固定容器宽度 */
            min-height: 700px;
            margin: 120px auto;
            padding: 80px;
            background-color:  rgba(255, 252, 240, 1);
            text-align: left;
            border-radius: 40px;
            box-shadow: 0 0 40px rgba(17, 17, 17, 0.5);
            box-sizing: border-box;  /* 确保padding包含在宽度内 */
        }

        .content {
            width: 100%;
            margin: 0 auto
            line-height: 1.5;
            text-align: left;
        }

        .content h1 {
            margin-bottom: 40px;
            word-wrap: break-word;  /* 确保长文本会自动换行 */
            white-space: pre-wrap;  /* 保留空格和换行符 */
            font-family: "Noto Serif SC", serif;
            font-optical-sizing: auto;
            font-weight: 600;
            font-style: normal;
            font-size:100px;
            color: rgba(40, 40, 40, 1);
        }

        .reader {
            margin: 0;
            padding: 20px 0;
            font-family: "Noto Serif SC", serif;
            font-optical-sizing: auto;
            font-weight: 400;
            font-style: normal;
            color: rgba(10, 10, 10, 0.6);
            font-size: 60px;
        }

        .author {
            margin-top: 40px;
            font-size: 80px;
            font-family: "Noto Serif SC", serif;
            font-optical-sizing: auto;
            font-weight: 400;
            font-style: normal;
            color: rgba(10, 10, 10, 0.8);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <p class="reader">{{ reader }} 摘抄于 {{ time }}</p>
            <h1>{{ content }}</h1>

            {% if author and book %}
            <p class="author">——{{ author }}「{{ book }}」</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''
#如果书名和作者未传入参数，则摘抄中的这一行不显示

    @filter.command("摘抄")
    async def quote(self, event: AstrMessageEvent):
        message = event.get_message_str().replace("摘抄", "", 1).strip()
        user_name = event.get_sender_name()
        #摘抄时间戳转换（北京时间）
        quote_timestamp = event.message_obj.timestamp+ 8 * 3600
        quote_timeArray = time.localtime(quote_timestamp)
        quote_time = time.strftime("%Y-%m-%d %H:%M", quote_timeArray)

        if not message:
            yield event.plain_result("格式：摘抄 书名\\作者\\内容，否则默认全部输出内容喵")
            return
        
        if message.count('\\') != 2:
            url = await self.html_render(self.TMPL, {
                "reader":user_name,
                "time":quote_time,
                "content": message.strip(),
            }
            )
        else:    
            book, author, content = message.split('\\')
            url = await self.html_render(self.TMPL, {
                "reader":user_name,
                "time":quote_time,
                "content": content.strip(),
                "book": book.strip(),
                "author": author.strip()
            })
        yield event.image_result(url)

#作息记录
    @filter.command("早安")
    async def SleepDiary(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()