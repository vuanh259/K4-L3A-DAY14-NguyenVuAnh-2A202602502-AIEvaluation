# Trạng thái thực hiện lab

## Đã kiểm chứng

- Repository origin: `https://github.com/vuanh259/K4-L3A-DAY14-NguyenVuAnh-2A202602502-AIEvaluation`.
- Python 3.12, môi trường `.venv`, dependencies từ requirements.txt.
- Import openai, dotenv, pytest: `Environment OK`.
- Baseline starter: 42 failed, không lỗi collection.
- Core Tasks 1–5: **41 passed, 1 skipped**; bonus reranking chưa thực hiện.
- `template.py` và `solution/solution.py` đồng bộ.
- Dataset: **20 QA, 5/7/5/3, 10/10 docs, validator PASS**.
- Corpus và tests gốc không bị sửa. Evidence lấy nguyên văn từ corpus.
- Exercise 3.3 có bốn dimensions, mỗi dimension có rubric 1–5 và bias controls.

## Cần hoàn thành

1. Gemini key đã cấu hình trong `.env`; không gửi key qua chat hoặc commit file này.
2. Generation đã hoàn tất đủ 20 answers thật bằng Gemini `gemini-2.5-flash`;
  artifact ghi provider/model thực tế và có retrieval trace.
3. Evaluation đã ghi `artifacts/benchmark_results.json`; Exercise 3.2 và
  reflection đã được cập nhật với số liệu, top-3 trace, 5 Whys và improvement
  log.
4. Học viên tự viết warm-up, nhận xét dataset, failure analysis, 5 Whys,
   clustering, regression strategy và reflection theo RULES.md mục 2.
5. Review, commit/push và tự nộp link LMS. Chưa xác nhận quyền truy cập GitHub
   hoặc nộp bài. Chưa làm bonus.

## Cấu hình Gemini theo yêu cầu học viên

`domain_assistant.py` tự chọn Gemini khi có `GEMINI_API_KEY`; đọc tên model
nguyên trạng từ `GEMINI_MODEL`. Có thể chọn rõ bằng `AI_PROVIDER=gemini` hoặc
`AI_PROVIDER=openai`. Không cần thêm dependency: dùng Chat Completions tại
endpoint tương thích của Google, không gửi Gemini key đến OpenAI.

Gemini dùng `max_tokens=2048`, temperature mặc định của provider, cùng prompt
và BM25 top_k=5 của starter. OpenAI vẫn giữ cấu hình gốc. Kết quả Gemini không
phải kết quả gpt-4o-mini; artifact lưu đúng provider và model thực dùng.
Tài liệu: https://ai.google.dev/gemini-api/docs/openai

Tests bổ sung trong `tests/test_provider_config.py` kiểm tra routing, endpoint,
và việc từ chối lưu câu trả lời rỗng/bị cắt, retry 429 có giới hạn.
Tổng suite: 46 passed, 1 skipped;
suite gốc: 41 passed, 1 skipped. Không sửa tests gốc.

API thực tế đã trả quota ngày `generate_content_free_tier_requests` với limit 20
cho model `gemini-3.6-flash`; model này không hoàn tất được run. Model
`gemini-2.5-flash` đã chạy đủ 20 câu thật sau retry. Generator giãn cách tối
thiểu 13 giây giữa các lần bắt đầu request; khi 429, chờ 60 giây rồi retry tối
đa ba lần. Không tạo actual answer giả; artifact chỉ lưu khi đủ 20 câu.
Lỗi kết nối cũng được retry có giới hạn, chờ 15 giây giữa các lần thử.

Thư mục hiện tại mang tên repository; yêu cầu lab đặt tên thư mục local là
`K4-DAY14-NguyenVuAnh-2A202602502`. Chưa đổi tên thư mục workspace đang mở.
Hạn nộp trong đề người dùng là 12h hôm sau, còn RULES/SUBMISSION local ghi
23h59 ngày lab; cần theo thông báo mới nhất của coach.

## Lệnh chạy tiếp trong PowerShell tại thư mục gốc

```powershell
.venv\Scripts\Activate.ps1
python --version
python -c "import openai, dotenv, pytest; print('Environment OK')"
python -m pytest tests/ -v -p no:cacheprovider
python validate_golden_dataset.py
python domain_assistant.py
python evaluate_answers.py
python export_benchmark_notes.py
git diff --check
git status --short
```

Nếu PowerShell chặn Activate.ps1, dùng `.venv\Scripts\python.exe` thay `python`.
`-p no:cacheprovider` chỉ tắt cache của pytest vì sandbox từng chặn tạo cache;
nội dung tests và việc thu thập tests không thay đổi.

Sau generation, kiểm tra timestamp mới, đủ 20 IDs, error=null, answer có nội
dung và mỗi retrieved chunk có source_doc/chunk_id/text/score. Chỉ sử dụng
artifact của lần sinh thành công; nếu sửa question phải sinh lại answers.

## Gợi ý học và tự viết phân tích

- Warm-up: nghĩ về paraphrase và refusal đúng chính sách trước khi kết luận
  overlap thấp là lỗi. Chọn quality gate riêng và giải thích, không sửa contract.
- Position bias: dùng cùng cặp câu trả lời, đổi thứ tự, giữ các biến khác cố định.
- Mỗi 5 Whys: ghi claim quan sát, trích gold evidence, đánh dấu chunk có/thiếu
  và phân biệt giả thuyết với kết luận. Không gán nguyên nhân chỉ từ một score.
- Root cause của Analyzer là gợi ý dựa trên metric thấp nhất, không phải kết
  quả điều tra. Khi ties, Analyzer trả “Multiple issues”.
- Improvement log: F001... đánh số failures theo thứ tự dataset, không phải
  thứ hạng Overall. Ghi mapping từ F ID sang QA ID trước khi phân tích.
- Nếu có ít hơn ba failures, giữ đúng passed và hỏi coach cách nghiệm thu;
  không sửa điểm để tạo thêm lỗi.
- Regression: cân nhắc chạy khi đổi prompt/model/retrieval/corpus; cùng bộ QA,
  phiên bản corpus và cấu hình được lưu. Code phát hiện giảm **hơn 0.05** ở
  trung bình ba answer metrics. Giảm đúng 0.05 không bị chặn theo contract.
- Đánh giá lại core dùng answers đã lưu; đánh giá thay đổi hệ thống sinh câu
  trả lời phải sinh actual answers mới. Giữ baseline cũ để so sánh.
- Tự xác định metric chặn/metric cảnh báo và rủi ro riêng tư cần human review.
  Đề xuất cases vòng sau trong reflection, giữ bộ nộp hiện tại đúng 20 slots.

## Giải thích core khi review

Faithfulness chia cho tập từ answer; Relevance chia cho tập từ question;
Completeness và Context Recall chia cho tập từ expected. Recall dùng hợp
chunks, Precision dùng Average Precision tại các hạng liên quan. Overall chỉ
là trung bình ba answer scores. Retrieval None là chưa tính, khác với 0.0.
Empty denominators trả 1.0 theo contract, nên cần đọc answer thực tế khi
diễn giải. Runner giữ QAPair gốc để không mất metadata.id.
