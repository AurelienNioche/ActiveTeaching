import copy

from teacher.tracking_teacher import TrackingTeacher

from solver import solver


class NirajTeacher(TrackingTeacher):

    def __init__(self, n_items=20, t_max=100, grade=1, handle_similarities=True, verbose=False):

        super().__init__(n_items=n_items, t_max=t_max, grade=grade, handle_similarities=handle_similarities,
                         verbose=verbose)

    def ask(self):

        question = solver.get_next_node(
            questions=self.questions,
            successes=self.successes,
            agent=copy.deepcopy(self.agent),
            n_items=self.n_items
        )

        possible_replies = self.get_possible_replies(question)

        if self.verbose:
            print(f"Question chosen: {self.kanjis[question]}; "
                  f"correct answer: {self.meanings[question]}; "
                  f"possible replies: {self.meanings[possible_replies]};")

        return question, possible_replies
