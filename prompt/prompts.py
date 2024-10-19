# Thinker
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


# Discover_new_conditions = """
# I need you to derive some useful, specific conditions with logical relationships for a target, based on some known conditions
# (at least 3). You will need to clearly indicate to me which known condition or conditions led you to each of these new conditions.

# Example 1:
# Known conditions:
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# Objective:
# 1. find $f^{{-1}}(11)$
# New conditions:
# 1. Based on Known condition 2, we can get: f(9) = f(3) + 2.
# 2. Based on Known condition 2, and Known condition 1, we can get: f(9) = 7.
# 3. Based on Known condition 2, we can get: f(27) = f(9) + 2.

# Example 2:
# Known conditions:
# 1. The difference between the squares of two different prime numbers is 1488.
# 2. Both prime numbers are less than 50.
# Objective:
# 1. Identify the two prime numbers that satisfy these conditions.
# 2. Submit the numbers in either order, separated by a comma.
# New conditions:
# 1. Based on Known condition 1, we can get: Both primes are odd.
# 2. Based on Known condition 1 and Known condition 2, we can get: One prime is significantly larger than the other.
# 3. Based on Known condition 1, we can get: The larger prime number cannot be 3,5, or 7.

# Real question:
# Known conditions:
# {Known_conditions}
# Objective:
# {Objective}
# New conditions:
# """

# Discover_new_conditions = """
# I need you to derive the most direct condition with logical relationships, based on some known conditions.
# You can NOT skip the intermediate steps by using the conditions that are not directly shown in the known conditions.
# You have to use code to perform the math calculation.
# You will need to clearly indicate to me which known condition or conditions led you to each of these new conditions by using the same format as the examples (Based on Known condition..., we can get:...Reason:..)

# Example 1:
# Known conditions:
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# Objective:
# 1. find $f^{{-1}}(11)$
# New condition:
# Based on Known condition 2, we can get: f(9) = f(3) + 2.
# Reason: when x = 3, f(3*3) = f(3) + 2, thus f(9) = f(3) + 2.

# Example 2:
# Known conditions:
# 1. The difference between the squares of two different prime numbers is 1488.
# 2. Both prime numbers are less than 50.
# Objective:
# 1. Identify the two prime numbers that satisfy these conditions.
# 2. Submit the numbers in either order, separated by a comma.
# New condition:
# Based on Known condition 1 and Known condition 2, we can get: One prime is significantly larger than the other.
# Reason: 1488 is a large number compare with 50

# Real question:
# Known conditions:
# {Known_conditions}
# Objective:
# {Objective}
# New condition:
# """

# TODO: do I need to include return type here??
Discover_new_conditions = """
I have some known conditions:
{conditions}
And I want to achieve the following objective(s):
{objectives}.
Please derive more (helpful, in terms of the objective) direct conditions with logical relationships from the known conditions.
NOTE:
1. ONLY use the known conditions to derive new conclusions.
The return type of your answer is a list of the following 'new conclusion' objects:
    based_on_known_conditions: list of the indeces of the known conditions this new condition is based on (list[int])
    new_condition: (str)
    reason: reason behind this new condition (str)
"""


# Discover_new_conditions = """
# I need you to derive the most direct condition with logical relationships, based on some known conditions.
# You can NOT skip the intermediate steps by using the conditions that are not directly shown in the known conditions.
# You have to use code to perform the math calculation.
# You will need to clearly indicate to me which known condition or conditions led you to each of these new conditions by using the same format as the examples (Based on Known condition..., we can get:...Reason:..)

# Example 1:
# Known conditions:
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# New condition:
# Based on Known condition 2, we can get: f(9) = f(3) + 2.
# Reason: when x = 3, f(3*3) = f(3) + 2, thus f(9) = f(3) + 2.

# Example 2:
# Known conditions:
# 1. The difference between the squares of two different prime numbers is 1488.
# 2. Both prime numbers are less than 50.
# New condition:
# Based on Known condition 1 and Known condition 2, we can get: One prime is significantly larger than the other.
# Reason: 1488 is a large number compare with 50

# Real question:
# Known conditions:
# {Known_conditions}
# New condition:
# """


# Determine_Steps = """
# I need you to come up with one solution targeted at our objective, based on all the known conditions.
# Each solution should include specific and clear steps.

# Example 1:
# Known conditions:
# 1. f(3) = 5
# 2. for all x > 0, f(3x) = f(x) + 2
# 3. Because f(3x) = f(x) + 2, so f(9) = f(3) + 2
# 4. Because f(3x) = f(x) + 2, and f(3) = 5, so f(9) = 7
# 5. Because f(3x) = f(x) + 2, so f(27) = f(9) + 2
# Objective:
# find $f^{{-1}}(11)$
# Solutions:
# Step 1:
# Use f(9) to find f(27)
# Step 2:
# Use f(27) to find f(81)
# Step 3:
# Repeat until find x that f(x) = 11

# Example 2:
# Known conditions:
# 1. a + 1 / b = 22 / 7
# 2. b + 1 / c = 8
# 3. abc = 21
# 4. c = 1 / (8 - b)
# 5. a = (22 / 7) - (1 / b)
# Objective:
# Calaculate c + 1 / a
# Solutions:
# Step 1:
# Substitude a in abc = 21 by (22 / 7) - (1 / b)
# Step 2:
# Substitude c in abc = 21 by 1 / (8 - b)
# Step 3:
# Calculate b
# Step 4:
# Calculate a and c
# Step 5:
# Calculate c + 1 / a

# Real question:
# Known conditions:
# {Known_conditions}
# Objective:
# {Objective}
# Solutions:
# """


Determine_Steps = """
Help me to come up with one solution targeting at our objective. 

Example 1:
Known conditions: 
1. f(3) = 5
2. for all x > 0, f(3x) = f(x) + 2
3. Because f(3x) = f(x) + 2, so f(9) = f(3) + 2
4. Because f(3x) = f(x) + 2, and f(3) = 5, so f(9) = 7
5. Because f(3x) = f(x) + 2, so f(27) = f(9) + 2
Objective:
find $f^{{-1}}(11)$
Solutions:
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
Solutions:
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
Solutions:
"""

# Judge

Judge_condtion = """
I need you to determine if the statement is a condition included inside the problem.
You are only allowed to use the 'True' or 'False' as the final answer.
If it is correct, answer 'True'. 
If it is not correct, answer 'False'. 

Example 1:
problem:
Avery earns 30$ each day, how much will he earn for 30 days?
Statement:
Avery earns 20$ each day
Judgement:
False

Example 2:
problem:
The sum of two numbers is 25 and their difference is 9. What is their product?
Statement:
The sum of two numbers is 25
Judgement:
True

Real question:
problem:
{question}
Statement:
{Initial_conditions}
Judgement:
"""

# Judge_T_F = """
# I need you to determine if the statement is correct or not based on the current conditions?
# You are only allowed to use the 'True' or 'False' as the final answer.
# If it is correct, answer 'True'.
# If it is not correct, answer 'False'.
# You need to use code to determine if you can.

# Example 1:
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# statement:
# Based on Known condition 1 and Known condition 2, we can get: (a / (1 - b)) * (b / (1 - a)) = 1
# Answer:
# True

# Example 2:
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# statement:
# Based on Known condition 1, we can get: a = 22b / (7b - 1)
# Answer:
# False

# Real question:
# Known condtions:
# {Known_condtions}
# statement:
# {condition_from_thinker}
# Answer:
# """

# Judge_T_F = """
# Help me to carefully verify if the statement is correct.
# You have to use code to verify the math calculation.
# Just answer "True" or "False"

# Example 1:
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# statement:
# Based on Known condition 1 and Known condition 2, we can get: (a / (1 - b)) * (b / (1 - a)) = 1
# Answer:
# True

# Example 2:
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# statement:
# Based on Known condition 1, we can get: a = 22b / (7b - 1)
# Answer:
# False

# Real question:
# Known condtions:
# {Known_condtions}
# statement:
# {condition_from_thinker}
# Answer:
# """


Judge_T_F = """
I have some Known condtions:
{known_conditions}
Help me to carefully verify if the following statement is correct: 
{new_condition}

You have to use the code interpreter to verify any math calculations.
"""

T_or_F_prompt = """
Please just tell me if the statement is correct by using 'True' or 'False'.
"""


# Judge_if_got_Answer = """
# I need you to determine if the objective is included inside the current conditions?
# You are only allowed to use the 'True' or 'False' as the final answer.
# If yes, answer 'True'.
# If No, answer 'False'.
# You can use code to determine if necessary.

# Example 1:
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# Objective:
# find the value of a + b
# Answer:
# False

# Example 2:
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# Objective:
# find a + 1 / c
# Answer:
# True

# Real question:
# Known condtions:
# {Known_condtions}
# Objective:
# {Objective}
# Answer:
# """


# Judge_if_got_Answer = """
# Help me to determine if the objective is one of the current conditions.
# You are only allowed to use the 'True' or 'False' as the final answer.

# Example 1:
# Known condtions:
# 1. S = a / (1 - b)
# 2. 1 / S = b / (1 - a)
# Objective:
# find the value of a + b
# Answer:
# False

# Example 2:
# Known condtions:
# 1. a = 22 / 7 - 1 / b
# 2. a + 1 / c = 8
# Objective:
# find a + 1 / c
# Answer:
# True

# Real question:
# Known condtions:
# {Known_condtions}
# Objective:
# {Objective}
# Answer:
# """


Judge_if_got_Answer = """
I have some known conditions:
{conditions}
And I want to achieve the following objective(s):
{objectives}.
Can these objective(s) can be obtained based on the known conditions? or is the objective is already one of the current conditions?.
"""


### Executor

find_target = """
Our objective is:
{Objective}
We have these conditions:
{Conditions}
Follow these steps to find the objective:
{Steps}
Begin:
"""
