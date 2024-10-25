## Thinker
extract_conditions_objectives_from_problem = """
Given the following question, return a list of implicit conditions and objective(s) in the problem

Most problems will only have one objective, but more complex problems may have multiple.
Conditions will be used later, so be clear about the subject of each condition - if there are multiple of an item, give them consistent names, such as a,b,c or 1,2,3, and refer to them by name in the condition
The conditions must be derived directly from the problem; deductions or calculations to establish these conditions are not allowed.
Do not come up with a solution.

Example 1:
Question:
Louis earns a base monthly salary of $\\$$1,200 with 5$\\%$ commission on sales. For a month with $\\$$25,000 in sales, what are Louis's total earnings?
Conditions:
    ["Louis earns a base monthly salary of $1,200", "Louis earns a commission of 5$\\%$ on sales", "In the specificied month, Louis makes $25,000 in sales"]
Objectives:
    ["Calculate Louis's total earnings for the month"]

Example 2:
Question:
A line segment has one endpoint at $(6,8)$ and midpoint at $(1,1)$. What is the sum of the coordinates of the other endpoint?
Conditions:
    ["Line segment 'A' has one endpoint at (6,8)", "Line segment 'A' has a midpoint at (1,1)"]
Objectives:
    ["Find the coordinates of Line 'A's other endpoint", "Find the sum of these both endpoint coordinates"]

Note: return the following object format
    conditions: list[str]
    objectives: list[str]

Question:
{question}
"""

Discover_new_conditions = """
I have some known conditions:
{conditions}
And I want to achieve the following objective(s):
{objectives}.
Please derive (maximum of 3) NEW conditions with direct, logical relationships from the known conditions.
Only derive conditions that may be helpful as steps towards reaching the objective.

NOTE:
1. ONLY use the known conditions to derive new conclusions.
2. ONLY derive a maximum of 3 conditions
The return type of your answer is a list of the following 'new conclusion' objects:
    based_on_known_conditions: list of the indeces of the known conditions this new condition is based on (list[int])
    new_condition: (str)
    reason: reason behind this new condition (str)
"""

Determine_Steps = """
Create a list of steps to solve the objective, incorporating the known conditions.
Do not actually solve for anything along the way.
Use the known conditions as a source of truth.

Example 1:
Known conditions: 
1. f(3) = 5
2. for all x > 0, f(3x) = f(x) + 2
3. Because f(3x) = f(x) + 2, so f(9) = f(3) + 2
4. Because f(3x) = f(x) + 2, and f(3) = 5, so f(9) = 7
5. Because f(3x) = f(x) + 2, so f(27) = f(9) + 2
Objective:
find $f^{{-1}}(11)$
Optional comments:

Steps:
Step 1:
Use f(9) to find f(27)
Step 2:
Use f(27) to find f(81)
Step 3:
Repeat until find x that f(x) = 11

Example 2:
Known conditions: 
1. a + 1 / b = 22 / 7
2. b + 1 / c = 8
3. abc = 21
4. c = 1 / (8 - b)
5. a = (22 / 7) - (1 / b) 
Objective:
Calaculate c + 1 / a
Optional comments:

Steps:
Step 1:
Substitude a in abc = 21 by (22 / 7) - (1 / b) 
Step 2:
Substitude c in abc = 21 by 1 / (8 - b) 
Step 3:
Calculate b 
Step 4:
Calculate a and c
Step 5:
Calculate c + 1 / a

Real question:
Known conditions:
{Known_conditions}
Objective:
{Objective}
Optional Comments:
{optional_comments}
Steps:
"""

## Judge
Judge_T_F = """
I have some known conditions:
{known_conditions}

and known objective:
{objectives}

Help me to carefully verify if the following statement is correct AND may be helpful in reaching the objective:
{new_condition}

You have to use the code interpreter to verify any math calculations.
"""

Judge_if_got_Answer = """
I have some known conditions:
{conditions}
And I want to achieve the following objective(s):
{objectives}.
Can these objective(s) can be obtained based on the known conditions? or is the objective is already one of the current conditions?.
"""

judge_if_steps_correct = """
Given a generated list of steps and an objective, verify them to see if they are both achieve the objective, and are logically correct

Objective:
{objectives}

Steps:
{steps}
"""

are_conditions_contradictory = """
We have some known conditions regarding a problem:
{conditions}

Do any of these conditions contradict others or themselves?
If so, which conditions are wrong and should be removed?
Refer to them by their index (starting at 1, as seen above)

Analyze in detail
"""

### Executor
find_target = """
Our objective is:
{Objective}
We know these conditions:
{Conditions}
We've been given these steps to arrive at the conclusion. Follow them as much as possible:
{Steps}
Begin:
"""
