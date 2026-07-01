"""
evaluate.py  –  Evaluation script for the UniHelp chatbot NLP pipeline.

Tests all 14 intents with a curated question set, reports per-intent accuracy,
overall accuracy, and average response time.

Usage:
    py -3.12 evaluate.py                   # tests against localhost:5000 (default)
    py -3.12 evaluate.py --url <base_url>  # tests against a deployed server
"""

import sys
import time
import json
import argparse

try:
    import requests
except ImportError:
    print("requests is not installed. Run: pip install requests")
    sys.exit(1)

# ── Test set: (question, expected_intent) ──────────────────────────────────
TEST_CASES = [
    # Greeting (6)
    ("Hello",                                               "greeting"),
    ("Hi there",                                            "greeting"),
    ("Good morning",                                        "greeting"),
    ("Good afternoon",                                      "greeting"),
    ("Hey",                                                 "greeting"),
    ("Good evening",                                        "greeting"),

    # Farewell (5)
    ("Goodbye",                                             "farewell"),
    ("Bye",                                                 "farewell"),
    ("See you later",                                       "farewell"),
    ("Take care",                                           "farewell"),
    ("Good night",                                          "farewell"),

    # Thanks (5)
    ("Thank you",                                           "thanks"),
    ("Thanks a lot",                                        "thanks"),
    ("I really appreciate your help",                       "thanks"),
    ("That was very helpful",                               "thanks"),
    ("Thanks so much",                                      "thanks"),

    # Help (5)
    ("What can you do?",                                    "help"),
    ("What can you help me with?",                          "help"),
    ("What services do you offer?",                         "help"),
    ("Show me the menu",                                    "help"),
    ("What do you do?",                                     "help"),

    # Admission (8)
    ("What are the admission requirements?",                "admission"),
    ("How do I apply to RSU?",                              "admission"),
    ("What is the JAMB cutoff mark?",                       "admission"),
    ("What is the minimum JAMB score for Medicine?",        "admission"),
    ("How do I apply for Post-UTME?",                       "admission"),
    ("Tell me about RSU Post-UTME screening",               "admission"),
    ("When is the admission form available?",               "admission"),
    ("What is the cutoff mark for Engineering?",            "admission"),

    # Courses (7)
    ("What faculties are in RSU?",                          "courses"),
    ("What departments are in the Faculty of Engineering?", "courses"),
    ("What JAMB subjects do I need for Medicine?",          "courses"),
    ("What JAMB subjects do I need for Law?",               "courses"),
    ("How do I register my courses?",                       "courses"),
    ("What programmes does RSU offer?",                     "courses"),
    ("List the departments in Management Sciences",         "courses"),

    # Fees (7)
    ("How much is the school fee?",                         "fees"),
    ("What is the tuition fee for Engineering?",            "fees"),
    ("How much is the Medicine fee?",                       "fees"),
    ("How do I pay my school fees?",                        "fees"),
    ("When is the fee payment deadline?",                   "fees"),
    ("What is the acceptance fee?",                         "fees"),
    ("How do I pay with Remita?",                           "fees"),

    # Exam (7)
    ("When is the exam timetable released?",                "exam"),
    ("What are the exam rules?",                            "exam"),
    ("What is the RSU grading system?",                     "exam"),
    ("How do I register for carryover exams?",              "exam"),
    ("What happens if I have a carryover?",                 "exam"),
    ("Tell me about supplementary exams",                   "exam"),
    ("What is examination malpractice?",                    "exam"),

    # Results (6)
    ("What CGPA do I need for First Class?",                "results"),
    ("What is the CGPA classification at RSU?",             "results"),
    ("How do I check my semester results?",                 "results"),
    ("How do I get my transcript?",                         "results"),
    ("What is my academic standing?",                       "results"),
    ("How do I check my grades?",                           "results"),

    # Hostel (6)
    ("How do I apply for hostel accommodation?",            "hostel"),
    ("What are the hostel rules?",                          "hostel"),
    ("How much is the hostel fee?",                         "hostel"),
    ("Is there on-campus accommodation?",                   "hostel"),
    ("Tell me about the halls of residence",                "hostel"),
    ("How do I get a bedspace at RSU?",                     "hostel"),

    # Library (6)
    ("What are the library opening hours?",                 "library"),
    ("How many books can I borrow from the library?",       "library"),
    ("How do I access the e-library?",                      "library"),
    ("What databases does the RSU library have?",           "library"),
    ("What is the library fine for overdue books?",         "library"),
    ("Where is the RSU library?",                           "library"),

    # Calendar (6)
    ("When does harmattan semester start?",                 "calendar"),
    ("When are harmattan semester exams?",                  "calendar"),
    ("When does rain semester begin?",                      "calendar"),
    ("When is the long vacation?",                          "calendar"),
    ("What is the RSU academic calendar?",                  "calendar"),
    ("When does the semester resume?",                      "calendar"),

    # Contact (6)
    ("How do I contact the admissions office?",             "contact"),
    ("What is the bursary contact?",                        "contact"),
    ("How do I reach student affairs?",                     "contact"),
    ("What is the RSU ICT support contact?",                "contact"),
    ("What is the RSU phone number?",                       "contact"),
    ("What is the registrar email address?",                "contact"),

    # Scholarship (7)
    ("What scholarships are available at RSU?",             "scholarship"),
    ("How do I apply for the NDDC scholarship?",            "scholarship"),
    ("What is the PTDF scholarship?",                       "scholarship"),
    ("Tell me about the FGSB scholarship",                  "scholarship"),
    ("What CGPA do I need for a scholarship?",              "scholarship"),
    ("Are there any financial aid options?",                "scholarship"),
    ("How do I get a government scholarship?",              "scholarship"),
]


def run_evaluation(base_url: str):
    endpoint = f"{base_url.rstrip('/')}/api/chat"

    print("=" * 65)
    print("  UniHelp Chatbot – NLP Evaluation Report")
    print("=" * 65)
    print(f"  Server  : {endpoint}")
    print(f"  Cases   : {len(TEST_CASES)}")
    print("=" * 65)

    # -- Verify server is reachable ----------------------------------------
    try:
        health = requests.get(f"{base_url.rstrip('/')}/api/health", timeout=5)
        health.raise_for_status()
        print(f"  Status  : Server OK ({health.json().get('status', 'unknown')})")
    except Exception as e:
        print(f"\n  ERROR: Cannot reach server at {base_url}")
        print(f"  Detail : {e}")
        print("\n  Make sure the Flask server is running:")
        print("    py -3.12 app.py\n")
        sys.exit(1)

    print("=" * 65)
    print()

    # -- Run test cases -------------------------------------------------------
    results_by_intent: dict[str, dict] = {}
    total_correct = 0
    total_time_ms = 0.0
    failures = []

    for question, expected in TEST_CASES:
        intent_data = results_by_intent.setdefault(expected, {
            "correct": 0, "total": 0, "times": []
        })
        intent_data["total"] += 1

        t0 = time.perf_counter()
        try:
            resp = requests.post(
                endpoint,
                json={"message": question},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  [ERROR] {question!r:55s}  -> {e}")
            failures.append((question, expected, "REQUEST_ERROR", 0))
            continue
        elapsed_ms = (time.perf_counter() - t0) * 1000

        predicted  = data.get("intent", "unknown")
        confidence = data.get("confidence", 0.0)
        ok = predicted == expected

        intent_data["times"].append(elapsed_ms)
        total_time_ms += elapsed_ms

        if ok:
            intent_data["correct"] += 1
            total_correct += 1
            status = "PASS"
        else:
            status = "FAIL"
            failures.append((question, expected, predicted, confidence))

        print(
            f"  [{status}]  {question!r:55s}  "
            f"got={predicted:12s}  conf={confidence:.2f}  "
            f"{elapsed_ms:6.0f}ms"
        )

    n_tested = len(TEST_CASES)

    # -- Per-intent summary ---------------------------------------------------
    print()
    print("=" * 65)
    print("  Per-Intent Accuracy")
    print("=" * 65)
    print(f"  {'Intent':<22} {'Correct':>7}  {'Total':>5}  {'Accuracy':>8}  {'Avg ms':>7}")
    print(f"  {'-'*22}  {'-'*6}  {'-'*5}  {'-'*8}  {'-'*7}")

    for intent, d in results_by_intent.items():
        c, t = d["correct"], d["total"]
        acc  = (c / t * 100) if t else 0.0
        avg  = (sum(d["times"]) / len(d["times"])) if d["times"] else 0.0
        bar  = "#" * int(acc / 10)
        print(f"  {intent:<22}  {c:>6}  {t:>5}  {acc:>7.1f}%  {avg:>6.0f}ms  {bar}")

    # -- Overall summary ------------------------------------------------------
    overall_acc = (total_correct / n_tested * 100) if n_tested else 0.0
    avg_time    = (total_time_ms / n_tested) if n_tested else 0.0

    print()
    print("=" * 65)
    print("  Overall Results")
    print("=" * 65)
    print(f"  Total questions  : {n_tested}")
    print(f"  Correct          : {total_correct}")
    print(f"  Incorrect        : {n_tested - total_correct}")
    print(f"  Overall Accuracy : {overall_acc:.1f}%")
    print(f"  Avg Response Time: {avg_time:.0f} ms")

    # -- Failures detail -------------------------------------------------------
    if failures:
        print()
        print("=" * 65)
        print("  Failed Cases")
        print("=" * 65)
        for q, exp, pred, conf in failures:
            print(f"  Q: {q!r}")
            print(f"     Expected={exp}  Got={pred}  Confidence={conf:.2f}")
            print()

    # -- Efficiency rating ----------------------------------------------------
    print("=" * 65)
    print("  Efficiency Rating")
    print("=" * 65)
    if avg_time < 100:
        rating = "Excellent  (< 100 ms)"
    elif avg_time < 300:
        rating = "Good       (100 – 300 ms)"
    elif avg_time < 600:
        rating = "Acceptable (300 – 600 ms)"
    else:
        rating = "Slow       (> 600 ms)"
    print(f"  Response time: {avg_time:.0f} ms  ->  {rating}")

    if overall_acc >= 90:
        acc_rating = "Excellent  (>= 90%)"
    elif overall_acc >= 75:
        acc_rating = "Good       (75 – 89%)"
    elif overall_acc >= 60:
        acc_rating = "Acceptable (60 – 74%)"
    else:
        acc_rating = "Needs work (< 60%)"
    print(f"  Accuracy     : {overall_acc:.1f}%  ->  {acc_rating}")
    print("=" * 65)

    # -- Save JSON report ------------------------------------------------------
    report = {
        "server": endpoint,
        "total_cases": n_tested,
        "correct": total_correct,
        "overall_accuracy_pct": round(overall_acc, 1),
        "avg_response_time_ms": round(avg_time, 1),
        "per_intent": {
            intent: {
                "correct": d["correct"],
                "total":   d["total"],
                "accuracy_pct": round(d["correct"] / d["total"] * 100, 1) if d["total"] else 0,
                "avg_time_ms": round(sum(d["times"]) / len(d["times"]), 1) if d["times"] else 0,
            }
            for intent, d in results_by_intent.items()
        },
        "failures": [
            {"question": q, "expected": exp, "predicted": pred, "confidence": conf}
            for q, exp, pred, conf in failures
        ],
    }

    report_path = "evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Full report saved to: {report_path}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the UniHelp chatbot NLP pipeline.")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base URL of the running Flask server (default: http://localhost:5000)",
    )
    args = parser.parse_args()
    run_evaluation(args.url)
