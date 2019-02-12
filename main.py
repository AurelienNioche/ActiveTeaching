from graph import plot

from model.learner import QLearner, ActRLearner
from model.teacher import Teacher

from task import exercise


def run_rl():

    t_max = exercise.t_max

    learner = QLearner()
    teacher = Teacher()

    for t in range(t_max):

        question = teacher.choose_question(t=t)
        reply = learner.decide(question=question)
        correct_answer, success = teacher.evaluate(t=t, reply=reply)
        learner.learn(question=question, reply=reply, correct_answer=correct_answer)

    return teacher.summarize()


def run_act_r():

    t_max = exercise.t_max

    learner = ActRLearner()
    teacher = Teacher()

    for t in range(t_max):

        question = teacher.choose_question(t=t)
        reply = learner.decide(question=question)
        correct_answer, success = teacher.evaluate(t=t, reply=reply)
        learner.learn(question=question, reply=reply, correct_answer=correct_answer)

    return teacher.summarize()


def main():

    success = run_act_r()
    plot.success(success)


if __name__ == "__main__":

    main()
