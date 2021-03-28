from environment import *
from cheater_detection import cheater_detector

numTests = 100

testPassed=0

for test in range(numTests):
    testcase,cheater_id = generate_testcase()
    pred_cheater_id = cheater_detector(testcase)
    if(cheater_id==pred_cheater_id):
        testPassed += 1
        print("Testcase {} passed!!!".format(test+1))
    else:
        print("Testcase {} failed :(".format(test+1))

accuracy = 100*testPassed/numTests

print("Your cheater detection is {}% accurate".format(accuracy))
