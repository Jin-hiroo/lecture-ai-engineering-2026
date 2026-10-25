"""第1回: 素のLLMと会話履歴を保って質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 講座に固有の質問から会話を始める

初回の質問のあと、同じチャットセッションで続けて質問できます。
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat, question: str) -> str:
    response = chat.send_message(question)
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMと会話する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")

    first_question = args.question
    while True:
        print(f"[質問] {first_question}\n")
        try:
            print(ask(chat, first_question))
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            return

        print()
        try:
            first_question = input("次の質問 (終了: exit または Ctrl+D)> ").strip()
        except EOFError:
            print()
            break

        if not first_question:
            continue
        if first_question.lower() in {"exit", "quit"}:
            break


if __name__ == "__main__":
    main()
