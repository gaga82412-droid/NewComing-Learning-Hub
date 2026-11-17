
import json
import logging

from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """
Bạn là NewComing AI Assistant,
trợ lý học tập của website NewComing Learning Hub.

Hãy trả lời bằng tiếng Việt.
Hỗ trợ người dùng học Python, Django, HTML, CSS,
JavaScript, SQL, cơ sở dữ liệu và mạng máy tính.

Trả lời rõ ràng, dễ hiểu, đúng trọng tâm.
Khi giải thích code, hãy trình bày phù hợp với sinh viên.
"""


def chat_page(request):
    return render(request, "chat/index.html")


@require_POST
def get_response(request):
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Dữ liệu gửi lên không hợp lệ."},
            status=400
        )

    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return JsonResponse(
            {"error": "Bạn chưa nhập câu hỏi."},
            status=400
        )

    api_key = (getattr(settings, "GEMINI_API_KEY", "") or "").strip()
    primary_model = (
        getattr(settings, "GEMINI_MODEL", "") or ""
    ).strip()

    if not api_key:
        return JsonResponse(
            {"error": "Chưa cấu hình GEMINI_API_KEY."},
            status=503
        )

    if not primary_model:
        return JsonResponse(
            {"error": "Chưa cấu hình GEMINI_MODEL."},
            status=503
        )

    # Model dự phòng, ưu tiên tốc độ phản hồi
    fallback_model = "gemini-3.5-flash-lite"

    models_to_try = [primary_model]

    if primary_model != fallback_model:
        models_to_try.append(fallback_model)

    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        logger.exception("Không thể khởi tạo Gemini.")
        return JsonResponse(
            {"error": "Không thể kết nối Gemini. Hãy kiểm tra API Key."},
            status=502
        )

    def generate_stream():
        try:
            for model_name in models_to_try:
                received_text = False

                try:
                    print(f"Đang sử dụng Gemini model: {model_name}")

                    stream = client.models.generate_content_stream(
                        model=model_name,
                        contents=message.strip(),
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            max_output_tokens=768,
                            temperature=0.7
                        )
                    )

                    for chunk in stream:
                        text = getattr(chunk, "text", None)

                        if text:
                            received_text = True

                            yield json.dumps(
                                {"text": text},
                                ensure_ascii=False
                            ) + "\n"

                    yield json.dumps({"done": True}) + "\n"
                    return

                except Exception as e:
                    status_code = getattr(e, "status_code", None)

                    is_overloaded = (
                        status_code == 503
                        or "503" in str(e)
                        or "UNAVAILABLE" in str(e)
                    )

                    # Chỉ chuyển model nếu chưa gửi nội dung nào
                    if (
                        is_overloaded
                        and not received_text
                        and model_name != models_to_try[-1]
                    ):
                        print(
                            f"Model {model_name} đang quá tải. "
                            f"Chuyển sang {fallback_model}..."
                        )
                        continue

                    logger.exception(
                        "Gemini gặp lỗi với model %s",
                        model_name
                    )

                    error_message = (
                        "Gemini đang quá tải hoặc gặp sự cố. "
                        "Vui lòng thử lại sau."
                        if is_overloaded
                        else "Gemini gặp lỗi khi tạo câu trả lời."
                    )

                    yield json.dumps(
                        {"error": error_message},
                        ensure_ascii=False
                    ) + "\n"
                    return

        finally:
            client.close()

    response = StreamingHttpResponse(
        generate_stream(),
        content_type="application/x-ndjson; charset=utf-8"
    )

    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"

    return response
