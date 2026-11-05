class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices  # 리스트 형태 (4개)
        self.answer = answer    # 정답 번호 (1~4)
        self.hint = hint        # 보너스 과제: 힌트 속성 추가

    def display(self, index):
        print(f"\n[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }