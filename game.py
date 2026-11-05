import json
import os
import random
from datetime import datetime
from quiz import Quiz

class QuizGame:
    def __init__(self, filename="state.json"):
        self.filename = filename
        self.quizzes = []
        self.best_score = 0
        self.history = []  # 보너스 과제: 점수 기록 히스토리
        self.load_data()
        
        # 데이터가 없을 경우 기본 퀴즈 세팅 (영화/상식 주제 예시)
        if not self.quizzes:
            self.load_default_quizzes()

    def load_default_quizzes(self):
        default_data = [
            Quiz("Python의 창시자는 누구인가?", ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1, "파이썬의 이름은 그가 좋아하는 코미디 쇼에서 유래했습니다."),
            Quiz("영화 '인터스텔라'에서 주인공이 탑승한 우주선의 이름은?", ["엔듀런스호", "디스커버리호", "아폴로 11호", "비글 2호"], 1, "지구의 인류를 구하기 위해 탐사대가 탄 우주선입니다."),
            Quiz("대한민국의 수도는 어디인가?", ["부산", "인천", "서울", "대구"], 3, "한강이 흐르는 대한민국 중심 도시입니다."),
            Quiz("AI 에이전트 개발에 주로 사용되며, 빠르고 비동기를 지원하는 파이썬 웹 프레임워크는?", ["Django", "FastAPI", "Flask", "Spring"], 2, "자동 문서화(Swagger) 기능이 뛰어납니다."),
            Quiz("지구에서 가장 큰 대양은?", ["대서양", "인도양", "태평양", "북극해"], 3, "아시아와 아메리카 대륙 사이에 있습니다.")
        ]
        self.quizzes = default_data
        self.save_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
                    self.history = data.get("history", [])
                    
                    raw_quizzes = data.get("quizzes", [])
                    self.quizzes = [
                        Quiz(q["question"], q["choices"], q["answer"], q.get("hint", "힌트가 없습니다."))
                        for q in raw_quizzes
                    ]
                print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
            except (json.JSONDecodeError, IOError):
                print("⚠️ 데이터 파일이 손상되었거나 읽을 수 없습니다. 기본 데이터로 복구합니다.")
                self.load_default_quizzes()
        else:
            print("📂 기존 데이터 파일이 없어 새로 생성합니다.")
            self.load_default_quizzes()

    def save_data(self):
        try:
            data = {
                "best_score": self.best_score,
                "history": self.history,
                "quizzes": [q.to_dict() for q in self.quizzes]
            }
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            print("⚠️ 데이터를 파일에 저장하는 중 오류가 발생했습니다.")

    def run(self):
        while True:
            print("\n" + "=" * 40)
            print("        🎯 나만의 퀴즈 게임 🎯        ")
            print("=" * 40)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록 보기")
            print("4. 퀴즈 삭제")
            print("5. 점수 및 히스토리 확인")
            print("6. 종료")
            print("=" * 40)

            try:
                choice = input("선택: ").strip()
                if not choice:
                    print("⚠️ 빈 입력입니다. 1-6 사이의 숫자를 입력하세요.")
                    continue
                
                if choice == "1":
                    self.play_quiz()
                elif choice == "2":
                    self.add_quiz()
                elif choice == "3":
                    self.show_quizzes()
                elif choice == "4":
                    self.delete_quiz()
                elif choice == "5":
                    self.show_score_history()
                elif choice == "6":
                    print("\n👋 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
                    self.save_data()
                    break
                else:
                    print("⚠️ 잘못된 입력입니다. 1-6 사이의 숫자를 입력하세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 강제 종료 신호가 감지되었습니다. 안전하게 데이터를 저장하고 종료합니다.")
                self.save_data()
                break

    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해 주세요.")
            return

        # 보너스 과제: 문제 수 선택
        print(f"\n📌 총 등록된 퀴즈 수: {len(self.quizzes)}개")
        count_input = input(f"풀고 싶은 문제 수를 입력하세요 (1~{len(self.quizzes)}, 전체는 엔터): ").strip()
        
        if count_input == "":
            num_to_solve = len(self.quizzes)
        else:
            try:
                num_to_solve = int(count_input)
                if not (1 <= num_to_solve <= len(self.quizzes)):
                    print(f"⚠️ 1에서 {len(self.quizzes)} 사이의 숫자를 입력해야 합니다. 전체 문제로 진행합니다.")
                    num_to_solve = len(self.quizzes)
            except ValueError:
                print("⚠️ 올바른 숫자가 아닙니다. 전체 문제로 진행합니다.")
                num_to_solve = len(self.quizzes)

        # 보너스 과제: 문제 순서 랜덤 섞기
        shuffled_quizzes = self.quizzes.copy()
        random.shuffle(shuffled_quizzes)
        selected_quizzes = shuffled_quizzes[:num_to_solve]

        score = 0
        correct_count = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {num_to_solve}문제)")

        for idx, quiz in enumerate(selected_quizzes, 1):
            print("-" * 40)
            quiz.display(idx)
            
            # 보너스 과제: 힌트 기능 제공
            while True:
                user_input = input("정답 입력 (1~4) 또는 힌트 보기('h'): ").strip().lower()
                
                if user_input == 'h':
                    print(모든 힌트 내용: f"💡 [HINT] {quiz.hint}")
                    continue
                
                try:
                    ans_num = int(user_input)
                    if 1 <= ans_num <= 4:
                        break
                    else:
                        print("⚠️ 1부터 4 사이의 숫자를 입력해주세요.")
                except ValueError:
                    print("⚠️ 숫자 또는 'h'만 입력 가능합니다.")

            if quiz.check_answer(ans_num):
                print("✅ 정답입니다!")
                correct_count += 1
                score += 20  조정 가능 점수
            else:
                print(f"❌ 틀렸습니다! 정답은 {quiz.answer}번입니다.")

        total_score = int((correct_count / num_to_solve) * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {num_to_solve}문제 중 {correct_count}문제 정답! ({total_score}점)")
        
        if total_score > self.best_score:
            self.best_score = total_score
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

        # 히스토리 기록 추가 (보너스 5번)
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": num_to_solve,
            "correct_count": correct_count,
            "score": total_score
        }
        self.history.append(record)
        self.save_data()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        try:
            question = input("문제를 입력하세요: ").strip()
            if not question:
                print("⚠️ 빈 문제는 추가할 수 없습니다.")
                return

            choices = []
            for i in range(1, 5):
                choice = input(f"선택지 {i}: ").strip()
                if not choice:
                    print("⚠️ 선택지는 비워둘 수 없습니다. 처음부터 다시 시도해주세요.")
                    return
                choices.append(choice)

            answer_str = input("정답 번호 (1-4): ").strip()
            answer = int(answer_str)
            if not (1 <= answer <= 4):
                print("⚠️ 정답은 1~4 사이여야 합니다.")
                return

            hint = input("이 문제의 힌트를 입력하세요 (선택사항): ").strip()
            if not hint:
                hint = "제공된 힌트가 없습니다."

            new_quiz = Quiz(question, choices, answer, hint)
            self.quizzes.append(new_quiz)
            self.save_data()
            print("✅ 퀴즈가 성공적으로 추가되어 파일에 저장되었습니다!")
        except ValueError:
            print("⚠️ 잘못된 입력 형식입니다. (정답 번호는 숫자여야 합니다)")

    def show_quizzes(self):
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for idx, q in enumerate(self.quizzes, 1):
            print(f"[{idx}] {q.question}")
            print(f"    - 정답: {q.answer}번 / 힌트: {q.hint}")
        print("-" * 40)

    def delete_quiz(self):
        # 보너스 과제: 퀴즈 삭제 기능
        if not self.quizzes:
            print("\n📋 삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()
        try:
            del_input = input("삭제할 퀴즈 번호를 입력하세요 (취소는 엔터): ").strip()
            if not del_input:
                return
            
            idx = int(del_input)
            if 1 <= idx <= len(self.quizzes):
                removed = self.quizzes.pop(idx - 1)
                self.save_data()
                print(f"🗑️ 삭제 완료: \"{removed.question}\"")
            else:
                print("⚠️ 존재하지 않는 번호입니다.")
        except ValueError:
            print("⚠️ 올바른 숫자를 입력해주세요.")

    def show_score_history(self):
        print("\n" + "=" * 40)
        print(f"🏆 최고 점수: {self.best_score}점")
        print("=" * 40)
        
        # 보너스 과제: 점수 기록 히스토리 출력
        if not self.history:
            print("📜 아직 게임 플레이 기록이 없습니다.")
        else:
            print("📜 최근 게임 기록 히스토리:")
            for i, h in enumerate(self.history[-5:], 1):  # 최근 5개만 출력
                print(f" {i}. [{h['date']}] {h['total_questions']}문제 중 {h['correct_count']}문제 정답 ({h['score']}점)")
        print("=" * 40)