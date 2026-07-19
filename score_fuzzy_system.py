import numpy as np
import matplotlib.pyplot as plot
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# the range 0 to 100
presence=ctrl.Antecedent(np.arange(0, 101, 1), 'presence')

# the range 0 to 20
exam=ctrl.Antecedent(np.arange(0, 21, 1), 'exam')

# the range 0 to 100
homework=ctrl.Antecedent(np.arange(0, 101, 1), 'homework')

# the range 0 to 20
final_score=ctrl.Consequent(np.arange(0, 21, 1), 'final_score')

presence['full absent']=fuzz.trimf(presence.universe, [0, 0, 30])
presence['half absent']=fuzz.trimf(presence.universe, [20, 40, 60])
presence['few absent']=fuzz.trimf(presence.universe, [50, 70, 90])
presence['present']=fuzz.trimf(presence.universe, [80, 100, 100])

exam['very weak']=fuzz.trimf(exam.universe, (0, 0, 4))
exam['weak']=fuzz.trimf(exam.universe, (2, 5, 8))
exam['average']=fuzz.trimf(exam.universe, (6, 10, 14))
exam['good']=fuzz.trimf(exam.universe, (12, 15, 18))
exam['excellent']=fuzz.trimf(exam.universe, (17, 20, 20))

homework['none']=fuzz.trimf(homework.universe, (0, 0, 30))
homework['partial']=fuzz.trimf(homework.universe, (20, 50, 80))
homework['complete']=fuzz.trimf(homework.universe, (70, 100, 100))

final_score['fail']=fuzz.trimf(final_score.universe, (0, 0, 5))
final_score['weak']=fuzz.trimf(final_score.universe, (3, 6, 9))
final_score['average']=fuzz.trimf(final_score.universe, (8, 11, 14))
final_score['good']=fuzz.trimf(final_score.universe, (13, 16, 18))
final_score['excellent']=fuzz.trimf(final_score.universe, (17, 20, 20))

presence.view()
plot.show()

exam.view()
plot.show()

homework.view()
plot.show()

final_score.view()
plot.show()

rule1 = ctrl.Rule(
    presence['present'] &
    exam['excellent'] &
    homework['complete'],
    final_score['excellent']
)

rule2 = ctrl.Rule(
    presence['present'] &
    exam['excellent'] &
    homework['partial'],
    final_score['good']
)

rule3 = ctrl.Rule(
    presence['few absent'] &
    exam['excellent'] &
    homework['complete'],
    final_score['good']
)

rule4 = ctrl.Rule(
    presence['half absent'] &
    exam['excellent'] &
    homework['complete'],
    final_score['good']
)

rule5 = ctrl.Rule(
    presence['full absent'] &
    exam['excellent'],
    final_score['average']
)

rule6 = ctrl.Rule(
    presence['present'] &
    exam['good'] &
    homework['complete'],
    final_score['good']
)

rule7 = ctrl.Rule(
    presence['present']&
    exam['good']&
    homework['partial'],
    final_score['average']
)

rule8 = ctrl.Rule(
    presence['few absent'] &
    exam['good'] &
    homework['complete'],
    final_score['average']
)

rule9 = ctrl.Rule(
    presence['half absent'] &
    exam['good'] ,
    final_score['weak']
)

rule10 = ctrl.Rule(
    presence['full absent'] &
    exam['good'],
    final_score['fail']
)

rule11 = ctrl.Rule(
    presence['present'] &
    exam['average'] &
    homework['complete'],
    final_score['good']
)

rule12 = ctrl.Rule(
    exam['average'] &
    presence['present'] &
    homework['partial'],
    final_score['average']
)

rule13 = ctrl.Rule(
    exam['average'] &
    presence['few absent'] &
    homework['partial'],
    final_score['average']
)

rule14 = ctrl.Rule(
    exam['average'] &
    presence['half absent'],
    final_score['weak']
)

rule15 = ctrl.Rule(
    exam['weak'] &
    presence['present'] &
    homework['complete'],
    final_score['average']
)

rule16 = ctrl.Rule(
    exam['weak'] &
    presence['present'] &
    homework['partial'],
    final_score['weak']
)

rule17 = ctrl.Rule(
    exam['weak'] &
    presence['few absent'],
    final_score['weak']
)

rule18 = ctrl.Rule(
    presence['half absent'] &
    exam['weak'] ,
    final_score['fail']
)

rule19 = ctrl.Rule(
    exam['weak'] &
    homework['none'],
    final_score['fail']
)

rule20= ctrl.Rule(
    exam['very weak'],
    final_score['fail']
)

rule21 = ctrl.Rule(
    exam['average'] &
    homework['complete'] &
    presence['few absent'],
    final_score['good']
)

rule22 = ctrl.Rule(
    exam['good'] &
    homework['complete'] &
    presence['half absent'],
    final_score['average']
)

rule23 = ctrl.Rule(
    exam['excellent'] &
    homework['none'] &
    presence['present'],
    final_score['average']
)

rule24 = ctrl.Rule(
    exam['average'] &
    homework['none'],
    final_score['weak']
)

rule25 = ctrl.Rule(
    exam['good'] &
    homework['complete'] &
    presence['few absent'],
    final_score['good']
)

grading_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5,
    rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15,
    rule16, rule17, rule18, rule19, rule20,
    rule21, rule22, rule23, rule24, rule25
])

grading = ctrl.ControlSystemSimulation(grading_ctrl)

# sample students

students = [
    (85, 17, 90),
    (70, 11, 60),
    (0, 0, 0),
    (100, 20, 100)
]

for i,p in enumerate(students):

    grading.input['presence']=p[0]
    grading.input['exam']=p[1]
    grading.input['homework']=p[2]

    grading.compute()

    print(f"Student {i+1}")

    print(grading.output['final_score'])

    final_score.view(sim=grading)
    plot.show()
