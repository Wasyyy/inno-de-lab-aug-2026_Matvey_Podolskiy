from task1_hw9 import Trainee


class HardworkingTrainee(Trainee):
    """
    Стажер-трудоголик - за домашку получает больше баллов.
    """

    def do_homework(self) -> None:
        """
        Increases score by 2
        """
        self.score = self.score + 2


class AuditTrainee(Trainee):
    """
    Вольнослушатель - формально всегда проходит курс.
    """

    def is_passing(self) -> bool:
        return True


class Cohort:
    """
    Учебная группа - хранит список стажеров и умеет проводить лекции.
    """

    def __init__(self, title: str, trainees: list[Trainee] = None) -> None:
        self.title: str = title
        self.trainees: list[Trainee] = trainees if trainees is not None else []

    def add_trainee(self, trainee: Trainee) -> None:
        self.trainees.append(trainee)

    def conduct_lecture(self) -> None:
        for trainee in self.trainees:
            trainee.visit_lecture()

    def get_passing_students(self) -> list[Trainee]:
        return [trainee for trainee in self.trainees if trainee.is_passing()]


if __name__ == "__main__":
    std_trainee = Trainee("Алексей", "Смирнов", score=8, passing_grade=10)
    hard_trainee = HardworkingTrainee("Елена", "Петрова", score=8, passing_grade=10)
    audit_trainee = AuditTrainee("Дмитрий", "Сидоров", score=0, passing_grade=10)

    cohort = Cohort("Python Advanced")
    cohort.add_trainee(std_trainee)
    cohort.add_trainee(hard_trainee)
    cohort.add_trainee(audit_trainee)

    cohort.conduct_lecture()
    hard_trainee.do_homework()

    passing_students = cohort.get_passing_students()

    print(f"=== УСПЕВАЕМОСТЬ ГРУППЫ '{cohort.title}' ===")
    for student in cohort.trainees:
        print(f"{student.name} {student.surname} | Баллы: {student.score} | Проходит: {student.is_passing()}")

    print("\nУспешно зачислены на следующий модуль:")
    for student in passing_students:
        print(f"- {student.name} {student.surname}")