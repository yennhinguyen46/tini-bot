import os
import json
import base64
import logging
import asyncio
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from typing import Optional, Tuple
from dotenv import load_dotenv
from openai import AsyncOpenAI
from duckduckgo_search import DDGS
from telegram import Update, BotCommand, ReactionTypeEmoji
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatAction

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
BOT_NAME = os.getenv("BOT_NAME", "Tí Nị")
BOT_PERSONALITY = os.getenv(
    "BOT_PERSONALITY",
    "Bạn là Tí Nị, một trợ lý AI thân thiện, dễ thương và hay giúp đỡ. "
    "Bạn trả lời bằng tiếng Việt, giọng điệu nhẹ nhàng, vui vẻ và thân thiện như một người bạn tốt.",
)
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Key: (chat_id, user_id) để tách biệt lịch sử theo từng người trong từng chat
conversation_history: dict = defaultdict(list)


def history_key(chat_id: int, user_id: int) -> tuple:
    return (chat_id, user_id)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": (
                "Lấy thông tin thời gian hiện tại chính xác. "
                "Dùng khi người dùng hỏi về giờ, ngày, tháng, năm, thứ hiện tại, "
                "hoặc cần biết thời gian để tính toán, so sánh."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Múi giờ (mặc định: Asia/Ho_Chi_Minh cho Việt Nam)",
                        "enum": ["Asia/Ho_Chi_Minh", "Asia/Bangkok", "Asia/Singapore", "UTC"],
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "CẢNH BÁO: Tool này dễ bị rate limit - CHỈ dùng khi THỰC SỰ cần thiết! "
                "CHỈ search cho: giá cả/tỷ giá HÔM NAY, tin tức TRONG 1-2 NGÀY GẦN ĐÂY, "
                "thời tiết HÔM NAY, sự kiện ĐANG diễn ra. "
                "TUYỆT ĐỐI KHÔNG search cho: kiến thức chung, lịch sử, khoa học, địa lý, "
                "định nghĩa, giải thích, cách làm, hướng dẫn, lập trình. "
                "Với những thứ KHÔNG phải realtime → trả lời từ kiến thức có sẵn, ĐỪNG search!"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Từ khoá tìm kiếm ngắn gọn, rõ ràng",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Tính toán biểu thức toán học phức tạp. "
                "Hỗ trợ: +, -, *, /, **, (), sqrt, sin, cos, tan, log, exp, pi, e. "
                "Dùng khi cần tính toán chính xác thay vì ước lượng."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Biểu thức toán học cần tính (ví dụ: '2**10 + 50', 'sqrt(144)')",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_image",
            "description": (
                "Tạo hình ảnh bằng AI (DALL-E 3) khi người dùng yêu cầu vẽ, tạo ảnh, minh hoạ, "
                "hay bất kỳ yêu cầu tạo hình ảnh nào. "
                "Chuyển mô tả sang tiếng Anh chi tiết trước khi truyền vào prompt."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Mô tả hình ảnh bằng tiếng Anh, chi tiết về chủ thể, phong cách, màu sắc, bố cục",
                    }
                },
                "required": ["prompt"],
            },
        },
    },
]


def load_md_file(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def get_current_datetime_vn() -> dict:
    """Lấy thông tin thời gian hiện tại tại Việt Nam."""
    try:
        tz = ZoneInfo("Asia/Ho_Chi_Minh")
    except:
        # Fallback nếu không có zoneinfo
        from datetime import timezone, timedelta
        tz = timezone(timedelta(hours=7))
    
    now = datetime.now(tz)
    
    weekdays_vn = {
        0: "Thứ Hai",
        1: "Thứ Ba", 
        2: "Thứ Tư",
        3: "Thứ Năm",
        4: "Thứ Sáu",
        5: "Thứ Bảy",
        6: "Chủ Nhật"
    }
    
    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": weekdays_vn[now.weekday()],
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "timezone": "Asia/Ho_Chi_Minh (UTC+7)"
    }


def get_system_prompt() -> str:
    soul = load_md_file("soul.md")
    knowledge = load_md_file("knowledge.md")
    
    # Thêm thông tin thời gian hiện tại vào system prompt
    current_time = get_current_datetime_vn()
    time_context = f"""
---
THÔNG TIN THỜI GIAN HIỆN TẠI:
- Ngày giờ: {current_time['datetime']}
- Ngày: {current_time['date']} ({current_time['weekday']})
- Giờ: {current_time['time']}
- Múi giờ: {current_time['timezone']}

Sử dụng thông tin này khi người dùng hỏi về thời gian, ngày tháng, hoặc cần tính toán dựa trên thời gian.
---

HƯỚNG DẪN KHI TÌM KIẾM WEB:
Tính năng search_web có thể bị rate limit nếu dùng quá nhiều.

NGUYÊN TẮC QUAN TRỌNG - HẠN CHẾ SEARCH TỐI ĐA:
1. CHỈ search khi THỰC SỰ CẦN thông tin realtime trong vài ngày gần đây
2. Ưu tiên trả lời từ kiến thức có sẵn trước
3. Với câu hỏi kiến thức CHUNG (lịch sử, khoa học, địa lý, định nghĩa) → KHÔNG search
4. Chỉ search cho: giá cả HÔM NAY, tin tức TRONG 1-2 NGÀY, thời tiết HÔM NAY

Khi nhận được kết quả "SEARCH_FAILED" hoặc "SEARCH_EMPTY":
1. KHÔNG nói "tìm kiếm thất bại" khô khan
2. Thành thật thông báo: "Em không tra được mạng lúc này"
3. Hướng dẫn cách tra cứu thủ công cụ thể:
   - Giá vàng: "Chị Google 'giá vàng SJC hôm nay' hoặc vào sjc.com.vn / pnj.com.vn nha"
   - Tỷ giá: "Chị tra trên vietcombank.com.vn hoặc Google 'tỷ giá USD VND' nha"
   - Tin tức: "Chị vào vnexpress.net hoặc Google keyword tin tức đó nha"
   - Thời tiết: "Chị Google 'thời tiết [tên thành phố]' để xem dự báo nha"
4. Có thể chia sẻ kiến thức CHUNG (không số liệu cụ thể) từ knowledge.md nếu có

VÍ DỤ TRẢ LỜI TỐT:
"Ủa em không tra được giá vàng lúc này do hệ thống đang giới hạn em rồi 😅 Chị Google 'giá vàng SJC hôm nay' hoặc vào sjc.com.vn để xem giá mới nhất nha. Thường giá vàng thay đổi nhiều lần trong ngày nên cần tra trực tiếp mới chính xác đó!"
---
"""
    
    parts = [time_context]
    if soul:
        parts.append(soul)
    if knowledge:
        parts.append(f"\n\n---\n\n{knowledge}")
    
    return "\n".join(parts) if parts else BOT_PERSONALITY


_last_search_time: float = 0.0
_MIN_SEARCH_INTERVAL = 10.0  # Tăng từ 3s lên 10s để tránh rate limit
_search_executor = ThreadPoolExecutor(max_workers=1)  # Giảm từ 3 xuống 1 để search tuần tự


def _do_search(query: str, max_results: int = 5) -> str:
    """Chạy DuckDuckGo search trong thread riêng, không block event loop."""
    global _last_search_time

    # Đợi ít nhất 10 giây giữa các lần search
    elapsed = time.time() - _last_search_time
    if elapsed < _MIN_SEARCH_INTERVAL:
        time.sleep(_MIN_SEARCH_INTERVAL - elapsed)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Tăng timeout và thử với cấu hình khác nhau
            if attempt == 0:
                timeout = 25
                wait_before = 0
            elif attempt == 1:
                timeout = 30
                wait_before = 5  # Đợi 5s trước lần thử 2
            else:
                timeout = 40
                wait_before = 10  # Đợi 10s trước lần thử 3
            
            if wait_before > 0:
                logger.info(f"Đợi {wait_before}s trước khi thử lại...")
                time.sleep(wait_before)
            
            # Thử search với timeout cao
            with DDGS(timeout=timeout) as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            
            _last_search_time = time.time()

            if not results:
                return "SEARCH_EMPTY"

            lines = []
            for r in results:
                title = r.get('title', '')
                body = r.get('body', '')
                href = r.get('href', '')
                if title or body:  # Chỉ thêm nếu có nội dung
                    lines.append(f"- **{title}**: {body} ({href})")
            
            if not lines:
                return "SEARCH_EMPTY"
            
            return "\n".join(lines)

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Search error (attempt {attempt + 1}/{max_retries}): {error_msg}")
            
            # Nếu chưa phải lần cuối, tiếp tục thử
            if attempt < max_retries - 1:
                continue
            
            # Lần cuối cũng thất bại
            return "SEARCH_FAILED"
    
    return "SEARCH_FAILED"


async def web_search(query: str, max_results: int = 6) -> str:
    """Async wrapper – chạy search trên thread riêng."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_search_executor, _do_search, query, max_results)


async def generate_image_dalle(prompt: str) -> Optional[str]:
    """Tạo ảnh với DALL-E 3. Trả về URL hoặc None nếu lỗi."""
    try:
        logger.info(f"🎨 Tạo ảnh: {prompt[:80]}...")
        response = await openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        url = response.data[0].url
        logger.info(f"✅ Tạo ảnh thành công")
        return url
    except Exception as e:
        logger.error(f"DALL-E error: {e}")
        return None


def get_current_time_info(timezone: str = "Asia/Ho_Chi_Minh") -> str:
    """Tool function: Lấy thông tin thời gian hiện tại."""
    try:
        tz = ZoneInfo(timezone)
    except:
        from datetime import timezone as tz_mod, timedelta
        tz = tz_mod(timedelta(hours=7))
    
    now = datetime.now(tz)
    
    weekdays_vn = {
        0: "Thứ Hai", 1: "Thứ Ba", 2: "Thứ Tư",
        3: "Thứ Năm", 4: "Thứ Sáu", 5: "Thứ Bảy", 6: "Chủ Nhật"
    }
    
    months_vn = {
        1: "Giêng", 2: "Hai", 3: "Ba", 4: "Tư", 5: "Năm", 6: "Sáu",
        7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười", 11: "Mười một", 12: "Mười hai"
    }
    
    result = f"""Thời gian hiện tại:
- Ngày giờ đầy đủ: {now.strftime('%d/%m/%Y %H:%M:%S')}
- Thứ: {weekdays_vn[now.weekday()]}
- Ngày: {now.day} tháng {months_vn[now.month]} năm {now.year}
- Giờ: {now.hour} giờ {now.minute} phút {now.second} giây
- Múi giờ: {timezone}
- Timestamp: {int(now.timestamp())}"""
    
    return result


def calculate_expression(expression: str) -> str:
    """Tool function: Tính toán biểu thức toán học."""
    try:
        import math
        # Whitelist các hàm an toàn
        safe_dict = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round,
            "pow": pow,
        }
        
        # Tính toán trong môi trường an toàn
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"Kết quả: {result}"
    except Exception as e:
        return f"Lỗi tính toán: {str(e)}"


async def chat_with_ai(
    chat_id: int,
    user_id: int,
    user_message: str,
    reply_context: Optional[str] = None,
    user_name: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """Trả về (text_reply, generated_image_url_or_None)."""
    key = history_key(chat_id, user_id)
    history = conversation_history[key]

    if reply_context and not history:
        history.append({"role": "assistant", "content": reply_context})

    history.append({"role": "user", "content": user_message})

    if len(history) > MAX_HISTORY:
        conversation_history[key] = history[-MAX_HISTORY:]

    system = get_system_prompt()
    if user_name:
        system += f"\n\n---\nNgười đang nhắn tin tên là: {user_name}. Hãy xưng hô phù hợp."

    messages = [{"role": "system", "content": system}] + conversation_history[key]
    generated_image_url: Optional[str] = None

    try:
        response = await openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=1024,
            temperature=0.8,
        )

        message = response.choices[0].message
        max_tool_rounds = 3
        current_round = 0

        while message.tool_calls and current_round < max_tool_rounds:
            current_round += 1
            messages.append(message)

            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if fn_name == "get_current_time":
                    timezone = args.get("timezone", "Asia/Ho_Chi_Minh")
                    logger.info(f"🕐 Lấy thời gian: {timezone}")
                    result = get_current_time_info(timezone)

                elif fn_name == "search_web":
                    query = args.get("query", user_message)
                    logger.info(f"🔍 Tìm kiếm lần {current_round}: {query}")
                    search_result = await web_search(query, max_results=6)
                    
                    # Xử lý khi search thất bại
                    if search_result == "SEARCH_FAILED":
                        result = (
                            "Tìm kiếm thất bại do vấn đề kết nối hoặc timeout. "
                            "Vui lòng trả lời dựa trên kiến thức có sẵn của bạn, "
                            "hoặc thông báo cho người dùng rằng không thể tìm kiếm được lúc này "
                            "và khuyên họ thử lại sau."
                        )
                    elif search_result == "SEARCH_EMPTY":
                        result = "Không tìm thấy kết quả nào cho truy vấn này."
                    else:
                        result = search_result

                elif fn_name == "calculate":
                    expression = args.get("expression", "")
                    logger.info(f"🧮 Tính toán: {expression}")
                    result = calculate_expression(expression)

                elif fn_name == "generate_image":
                    prompt = args.get("prompt", "")
                    image_url = await generate_image_dalle(prompt)
                    if image_url:
                        generated_image_url = image_url
                        result = "Đã tạo ảnh thành công. Hãy thông báo cho người dùng biết ảnh đã được tạo."
                    else:
                        result = "Tạo ảnh thất bại."

                else:
                    result = "Tool không xác định."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

            next_response = await openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                max_tokens=1024,
                temperature=0.8,
            )
            message = next_response.choices[0].message

        reply = message.content or ""
        conversation_history[key].append({"role": "assistant", "content": reply})
        return reply, generated_image_url

    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return "Ồ, mình gặp chút vấn đề rồi. Bạn thử lại sau nhé! 🙏", None


async def chat_with_ai_vision(
    chat_id: int,
    user_id: int,
    image_b64: str,
    caption: str = "",
    user_name: Optional[str] = None,
) -> str:
    """Phân tích ảnh/video thumbnail bằng GPT-4o-mini vision."""
    key = history_key(chat_id, user_id)

    question = caption.strip() if caption.strip() else "Bạn thấy gì trong hình này? Mô tả và nhận xét nhé."

    content = [
        {"type": "text", "text": question},
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_b64}",
                "detail": "auto",
            },
        },
    ]

    system = get_system_prompt()
    if user_name:
        system += f"\n\nNgười đang nhắn tin tên là: {user_name}."

    history = conversation_history[key]
    history.append({"role": "user", "content": content})
    if len(history) > MAX_HISTORY:
        conversation_history[key] = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": system}] + conversation_history[key]

    try:
        response = await openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.8,
        )
        reply = response.choices[0].message.content or ""

        # Lưu text-only vào history để tránh base64 nặng trong bộ nhớ
        conversation_history[key][-1] = {
            "role": "user",
            "content": f"[Gửi ảnh] {caption}".strip(),
        }
        conversation_history[key].append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        logger.error(f"Vision error: {e}")
        return "Ủa Tí Nị không xem được hình này rồi 😅 Thử lại sau nha!"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    first_name = user.first_name if user.first_name else "bạn"
    key = history_key(update.effective_chat.id, user.id)
    conversation_history[key].clear()

    welcome = (
        f"Xin chào {first_name}! 👋\n\n"
        f"Mình là *{BOT_NAME}* – trợ lý AI của bạn! 🌸\n\n"
        "Bạn có thể:\n"
        "• Nhắn tin để trò chuyện bất cứ lúc nào\n"
        "• Hỏi tin tức, thời sự – mình tự tìm Google 🔍\n"
        "• Gửi ảnh để mình xem và nhận xét 👁\n"
        "• Gửi video – mình xem thumbnail và mô tả 🎬\n"
        "• Nhờ mình vẽ/tạo ảnh bằng AI 🎨\n"
        "• /new – Bắt đầu cuộc hội thoại mới\n"
        "• /help – Xem hướng dẫn\n\n"
        "Hôm nay mình có thể giúp gì cho bạn nào? 😊"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        f"📖 *Hướng dẫn sử dụng {BOT_NAME}*\n\n"
        "*Các lệnh:*\n"
        "• /start – Chào mừng & reset hội thoại\n"
        "• /new – Bắt đầu cuộc trò chuyện mới\n"
        "• /help – Xem hướng dẫn này\n"
        "• /about – Thông tin về bot\n\n"
        "*Khả năng đặc biệt:*\n"
        "• 🕐 Biết thời gian thực (giờ, ngày, tháng, năm hiện tại)\n"
        "• 🔍 Tự tìm Google khi cần thông tin mới nhất\n"
        "• 🧮 Tính toán toán học chính xác\n"
        "• 👁 Xem và phân tích ảnh bạn gửi\n"
        "• 🎬 Xem thumbnail video và mô tả\n"
        "• 🎨 Tạo ảnh AI theo yêu cầu (nhờ mình vẽ/tạo ảnh là được)\n"
        "• 🧠 Nhớ lịch sử hội thoại\n\n"
        "Dùng /new để bắt đầu chủ đề mới."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        f"🌸 *Về {BOT_NAME}*\n\n"
        f"Mình là {BOT_NAME} – trợ lý AI được tạo ra bởi chị Nhi!\n\n"
        "💡 Mình có thể:\n"
        "• Trả lời câu hỏi, giải thích khái niệm\n"
        "• 🕐 Biết thời gian thực (ngày giờ hiện tại)\n"
        "• 🔍 Tìm kiếm thông tin, tin tức mới nhất\n"
        "• 🧮 Tính toán toán học chính xác\n"
        "• 👁 Xem và phân tích ảnh\n"
        "• 🎬 Xem và mô tả video (qua thumbnail)\n"
        "• 🎨 Tạo ảnh AI bằng DALL-E 3\n"
        "• Giúp viết lách, sáng tác\n"
        "• Lên kế hoạch, đưa ra lời khuyên\n"
        "• Dịch thuật, học ngoại ngữ\n"
        "• Trò chuyện và giải trí 😄\n\n"
        f"🤖 Model: {OPENAI_MODEL}\n\n"
        "Cứ hỏi mình bất cứ điều gì bạn nhé!"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")


async def new_conversation_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key = history_key(update.effective_chat.id, update.effective_user.id)
    conversation_history[key].clear()
    await update.message.reply_text(
        "🆕 Đã bắt đầu cuộc hội thoại mới!\nBạn muốn nói về chủ đề gì nào? 😊"
    )


def is_mentioned(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Kiểm tra bot có được tag hoặc được reply không (cả text lẫn caption)."""
    message = update.message
    if not message:
        return False

    chat_type = update.effective_chat.type

    # Chat riêng → luôn trả lời
    if chat_type == "private":
        return True

    bot_username = context.bot.username
    if not bot_username:
        return False

    # Được reply tin nhắn của bot
    if message.reply_to_message and message.reply_to_message.from_user:
        reply_username = message.reply_to_message.from_user.username or ""
        if reply_username.lower() == bot_username.lower():
            return True

    # Được @tag trong text
    text = message.text or ""
    for entity in (message.entities or []):
        if entity.type == "mention":
            mention = text[entity.offset: entity.offset + entity.length]
            if mention.lower() == f"@{bot_username}".lower():
                return True

    # Được @tag trong caption (ảnh/video)
    caption = message.caption or ""
    for entity in (message.caption_entities or []):
        if entity.type == "mention":
            mention = caption[entity.offset: entity.offset + entity.length]
            if mention.lower() == f"@{bot_username}".lower():
                return True

    return False


def is_tagged(message, bot_username: str) -> bool:
    """Kiểm tra tin nhắn có @tag bot trong text không (dùng để thả react)."""
    if not message or not bot_username or not message.entities or not message.text:
        return False
    for entity in message.entities:
        if entity.type == "mention":
            mention = message.text[entity.offset: entity.offset + entity.length]
            if mention.lower() == f"@{bot_username}".lower():
                return True
    return False


def is_tagged_in_caption(message, bot_username: str) -> bool:
    """Kiểm tra caption ảnh/video có @tag bot không (dùng để thả react)."""
    if not message or not bot_username:
        return False
    caption = message.caption or ""
    for entity in (message.caption_entities or []):
        if entity.type == "mention":
            mention = caption[entity.offset: entity.offset + entity.length]
            if mention.lower() == f"@{bot_username}".lower():
                return True
    return False


def remove_mention(text: str, bot_username: str) -> str:
    """Xoá @mention ra khỏi tin nhắn trước khi gửi cho AI."""
    if not bot_username:
        return text.strip()
    return text.replace(f"@{bot_username}", "").replace(f"@{bot_username.lower()}", "").strip()


async def _try_react(message, chat_type: str, bot_username: str) -> None:
    """Thả react 😏 nếu private chat hoặc được @tag."""
    should_react = (
        chat_type == "private"
        or is_tagged(message, bot_username)
        or is_tagged_in_caption(message, bot_username)
    )
    if should_react:
        try:
            await message.set_reaction([ReactionTypeEmoji(emoji="😡")])
            logger.info(f"✅ React 😡 cho message {message.message_id}")
        except Exception as e:
            logger.warning(f"⚠️ Không thả được react: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return

    if not is_mentioned(update, context):
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    user_name = update.effective_user.first_name or ""
    user_text = remove_mention(update.message.text or "", context.bot.username)

    if not user_text:
        return

    await _try_react(update.message, chat_type, context.bot.username or "")

    # Lấy nội dung tin nhắn được reply (nếu có) làm ngữ cảnh
    reply_context = None
    if update.message.reply_to_message and update.message.reply_to_message.text:
        replied_msg = update.message.reply_to_message
        key = history_key(chat_id, user_id)
        if not conversation_history[key]:
            sender = replied_msg.from_user.first_name if replied_msg.from_user else "ai đó"
            reply_username = (replied_msg.from_user.username or "") if replied_msg.from_user else ""
            is_bot_reply = reply_username.lower() == (context.bot.username or "").lower()
            if is_bot_reply:
                reply_context = replied_msg.text
            else:
                reply_context = f"[{sender} nói: {replied_msg.text}]"

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    reply, image_url = await chat_with_ai(chat_id, user_id, user_text, reply_context, user_name)

    if image_url:
        await update.message.reply_photo(photo=image_url, caption=reply)
    else:
        await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xem và phân tích ảnh bằng GPT-4o-mini vision."""
    if not update.message or not update.effective_user:
        return
    if not is_mentioned(update, context):
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    user_name = update.effective_user.first_name or ""
    caption = remove_mention(update.message.caption or "", context.bot.username or "")

    await _try_react(update.message, chat_type, context.bot.username or "")
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_bytes = await file.download_as_bytearray()
        image_b64 = base64.b64encode(bytes(file_bytes)).decode("utf-8")

        reply = await chat_with_ai_vision(chat_id, user_id, image_b64, caption, user_name)
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Photo handler error: {e}")
        await update.message.reply_text("Tí Nị không đọc được hình này rồi, bạn thử gửi lại nha 😅")


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xem video qua thumbnail bằng GPT-4o-mini vision."""
    if not update.message or not update.effective_user:
        return
    if not is_mentioned(update, context):
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or ""
    caption = remove_mention(update.message.caption or "", context.bot.username or "")

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    video = update.message.video
    thumbnail = getattr(video, "thumbnail", None) if video else None

    if thumbnail:
        try:
            file = await context.bot.get_file(thumbnail.file_id)
            file_bytes = await file.download_as_bytearray()
            image_b64 = base64.b64encode(bytes(file_bytes)).decode("utf-8")

            prefix = f"[Thumbnail của video] {caption}" if caption else "[Thumbnail của video] Mô tả nội dung video này nhé."
            reply = await chat_with_ai_vision(chat_id, user_id, image_b64, prefix, user_name)
            await update.message.reply_text(reply)
            return

        except Exception as e:
            logger.error(f"Video thumbnail error: {e}")

    await update.message.reply_text(
        "Tí Nị thấy video rồi nhưng chưa đọc được nội dung bên trong 😅 "
        "Bạn mô tả hoặc chụp màn hình gửi lại nha!"
    )


async def handle_unsupported(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_mentioned(update, context):
        return
    await update.message.reply_text(
        "Loại file này Tí Nị chưa đọc được nha 😅 "
        "Bạn thử gửi ảnh, video, hoặc nhắn chữ để mình hỗ trợ nhé!"
    )


async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "Bắt đầu & chào mừng"),
        BotCommand("new", "Bắt đầu hội thoại mới"),
        BotCommand("help", "Xem hướng dẫn"),
        BotCommand("about", "Thông tin về bot"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info(f"Bot {BOT_NAME} đã khởi động thành công!")


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("Thiếu TELEGRAM_BOT_TOKEN trong file .env!")
    if not OPENAI_API_KEY:
        raise ValueError("Thiếu OPENAI_API_KEY trong file .env!")

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("new", new_conversation_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(
        MessageHandler(filters.VOICE | filters.Document.ALL | filters.Sticker.ALL, handle_unsupported)
    )

    logger.info(f"Đang chạy bot {BOT_NAME}...")
    app.run_polling(
        allowed_updates=["message", "edited_message", "callback_query"]
    )


if __name__ == "__main__":
    main()
