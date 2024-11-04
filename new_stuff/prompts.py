# Note - changing the wording from conditions to assumptions returns worse and less precise conditions.
# Wonder if there is a better word than either conditions or assumptions though..
givens_from_problem = """
Given the following question, return a list of implicit conditions and the objective of the problem
1. Be specific about conditions. 
2. Conditions should be empirical.
3. Each condition should stand alone, and should not reference other conditions. Conditions can overlap.
4. The conditions must be derived directly from the problem; deductions or calculations to establish conditions are not allowed.

Question:
{question}"""


direct_mathematical_relationship = """
Given the following true conditions:
{conditions}

And the stated objective(s):
{objectives}

Please come up with a maximum of two proven mathematical relationships that can be applied given these conditions,
AND may be helpful as intermediate steps towards reaching the objective 

1. ONLY return existing mathematical relationships
2. ONLY use the known conditions as existing knowledge.
3. ONLY return 0, 1, or 2 relationships. No more.
4. Refer to ONLY the NECESSARY conditions by returning their index (starting at 1, given above)
The return type of your answer is a list of the following '' objects:
    conditions: list of the indeces of the known conditions this new relationship uses (list[int]) 
    relationship: (str)
    reason: reason this relationship is helpful towards achieving the objective.
"""

verify_relationship_prompt = """
Evaluate the following

Is this mathematical relationship:
{relationship}

Both 
1. mathematically proven to be true, given these conditions: 
{conditions}
And
2. relevant to the objective(s) {objectives}, by way of reasoning: {reason} ?

Return relevant as true or false based on the relationships relevancy
Return proven as true or flase based on whether or not the relationship is mathematically proven
Finally return accept as true if both are true. If both aren't true, return accept: false to reject this relationship
"""

find_method_prompt = """
We've been given the following question:
{question}

We have the following derived knowledge:
Implicit conditions:
{conditions}
Objective(s):
{objectives}
Applicable mathematical relationships:
{relationships}

Knowing this, come up with a method we can use to learn more about the problem and get closer to the objectives.
1. The method should result in more known CORRECT knowledge about the problem
2. The method should use logical inference about the problem.
3. The method does not need to answer the objective - just get CLOSER to the objective by learning MORE

Return a logically inferred method we can attempt using, explaining the logical inferences in it, and the reason behind why we should use it.
"""

verify_method_prompt = """
Given the question:
{question}

and the derived knowledge:
Implicit conditions:
{conditions}
Objective(s):
{objectives}
Applicable mathematical relationships:
{relationships}

Is this method:
{method}

A good choice to learn more about the problem for the reason:
{reason}
"""


# TODO: moving this to the end
sub_objective_prompt = """
Given the objective(s):
{objectives}
"""
