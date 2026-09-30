"""Export measured facts; preserve the learner's personal analysis sections."""
import contextlib
import io
import json
import re
from pathlib import Path

from evaluate_answers import load_evaluation_inputs, print_exercise_3_2
from template import BenchmarkRunner, FailureAnalyzer, RAGASEvaluator


def main() -> None:
    actual = json.loads(Path('artifacts/actual_answers.json').read_text(encoding='utf-8'))
    pairs, answers = load_evaluation_inputs('golden_dataset.json', 'artifacts/actual_answers.json')
    assert len(pairs) == len(actual['answers']) == 20
    for answer in actual['answers']:
        assert answer['retrieved_contexts']
        for chunk in answer['retrieved_contexts']:
            assert {'source_doc', 'chunk_id', 'text', 'score'} <= chunk.keys()
    runner = BenchmarkRunner()
    results = runner.run(pairs, answers.__getitem__, RAGASEvaluator())
    summary = runner.generate_report(results)
    artifact = json.loads(Path('artifacts/benchmark_results.json').read_text(encoding='utf-8'))
    assert summary == artifact['summary']
    assert [r.qa_pair.metadata['id'] for r in results] == [r['id'] for r in artifact['results']]
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        print_exercise_3_2(results, summary)
    provenance = (f"Actual answers generated_at: `{actual['generated_at']}`; "
                  f"provider: `{actual['agent'].get('provider')}`; model: `{actual['agent']['model']}`. "
                  "Gemini was selected by the learner instead of the starter's gpt-4o-mini.\n\n")
    worksheet = Path('exercises.md')
    text = worksheet.read_text(encoding='utf-8')
    table_marker = '| ID | Question (short) |'
    start = text.index(table_marker)
    end = text.index('**Nhận xét ngắn:**', start)
    text = text[:start] + provenance + output.getvalue() + '\n' + text[end:]
    text = text.replace('CP0–CP3 đã kiểm chứng; dataset CP4 đã PASS. Benchmark chưa chạy\nvì đang chờ cấu hình API key trong `.env`. Không có số liệu benchmark giả định.',
                        'CP0–CP3 đã kiểm chứng; dataset CP4 đã PASS. Benchmark Gemini đã chạy thật đủ 20 QA.\nSố liệu bên dưới được xuất từ artifacts, không phải điểm LLMJudge.')
    text = text.replace('- [ ] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.',
                        '- [x] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.')
    worksheet.write_text(text, encoding='utf-8')

    reflection = Path('reflection.md')
    text = reflection.read_text(encoding='utf-8')
    status_markers = ('**Chưa hoàn thành:**', '**Trạng thái:**')
    start = min(
        (text.index(marker) for marker in status_markers if marker in text),
        default=-1,
    )
    if start < 0:
        raise ValueError('reflection.md is missing a status paragraph')
    end = text.index('Dùng kết quả thật', start)
    text = text[:start] + ('**Cần học viên hoàn thiện:** số liệu và trace đã có; phần phân tích cá nhân,\n'
                          '5 Whys và reflection vẫn cần tự viết theo RULES.md mục 2.\n\n') + provenance + text[end:]
    text = text.replace('**Overall pass rate:** ____%', f"**Overall pass rate:** {summary['pass_rate']:.1%}")
    metrics = [('Context Recall', 'context_recall'), ('Context Precision', 'context_precision'),
               ('Faithfulness', 'faithfulness'), ('Relevance', 'relevance'),
               ('Completeness', 'completeness'), ('Overall Score', 'overall')]
    for label, name in metrics:
        values = [r.overall_score() if name == 'overall' else getattr(r, name) for r in results]
        text = text.replace(f'| {label} | | | | |',
                            f'| {label} | {sum(values)/len(values):.3f} | {min(values):.3f} | {max(values):.3f} | Học viên nhận xét |')
    for kind in ['hallucination', 'irrelevant', 'incomplete', 'off_topic', 'refusal']:
        count = summary['failure_types'].get(kind, 0)
        text = text.replace(f'| {kind} | | |', f'| {kind} | {count} | {count/len(results):.1%} |')
    analyzer = FailureAnalyzer()
    worst = sorted(results, key=lambda r: r.overall_score())[:3]
    for index, result in enumerate(worst, 1):
        start = text.index(f'### Failure {index}')
        end = text.index(f'### Failure {index+1}', start) if index < 3 else text.index('## 3. Failure Clustering', start)
        section = text[start:end]
        for value in [result.qa_pair.metadata['id'] + ': ' + result.qa_pair.question,
                      result.qa_pair.expected_answer, result.actual_answer]:
            section = section.replace('> *Điền:*', '> ' + value.replace('\n', '\n> '), 1)
        scores = ' | '.join(f'{label}: {getattr(result, name):.3f}' for label, name in metrics[:-1])
        section = re.sub(r'\*\*Scores:\*\*.*?Overall: ____',
                         '**Scores:** ' + scores + f' | Overall: {result.overall_score():.3f}\n\n'
                         f'Passed: {result.passed}; Failure type: {result.failure_type}.', section, flags=re.S)
        section += '\nAnalyzer output (gợi ý, chưa xác minh): ' + analyzer.find_root_cause(result) + '\n\n'
        text = text[:start] + section + text[end:]
    failures = [r for r in results if not r.passed]
    mapping = ', '.join(f"F{i:03d} → {r.qa_pair.metadata['id']}" for i, r in enumerate(failures, 1))
    log = artifact['failure_analysis']['improvement_log']
    text = text.replace('```text\n[paste Markdown table here]\n```', log + '\n\nMapping: ' + mapping)
    reflection.write_text(text, encoding='utf-8')

    golden = json.loads(Path('golden_dataset.json').read_text(encoding='utf-8'))
    gold = {r['id']: r for r in golden['qa_pairs']}
    traces = {r['id']: r for r in actual['answers']}
    notes = ['# Evidence for the three lowest scores', provenance]
    for result in worst:
        record_id = result.qa_pair.metadata['id']
        notes += [f'## {record_id}', '### Gold evidence']
        for context in gold[record_id]['contexts']:
            notes += [f"**{context['source_doc']}**", '> ' + context['text'].replace('\n', '\n> ')]
        notes += ['### Retrieved chunks in rank order']
        for rank, chunk in enumerate(traces[record_id]['retrieved_contexts'], 1):
            notes += [f"**Rank {rank}: {chunk['source_doc']} / {chunk['chunk_id']} (BM25 {chunk['score']})**",
                      '> ' + chunk['text'].replace('\n', '\n> ')]
    Path('artifacts/review_evidence.md').write_text('\n\n'.join(notes) + '\n', encoding='utf-8')
    print('Verified 20 answers and benchmark summary; exported worksheet, reflection facts, and review evidence.')


if __name__ == '__main__':
    main()
