======
## Generated
 3: 147 sqrt(3)
2: \(147 \sqrt{3}\)
10: 147√3
9: The final answer is \(147\sqrt{3}\) square units.
1: 147√3
7: The final answer is: \(147\sqrt{3}\).
12: The final answer is the area of the equilateral triangle, which is \( \frac{441 \sqrt{3}}{4} \).
11: 147√3
5: 147\sqrt{3}
4: 147\sqrt{3}
0: \(147\sqrt{3}\)
13: The final answer is the area of triangle ABC.
6: The final answer is \( \frac{147 \sqrt{3}}{4} \).
8: 147√3
14: The final answer is: 63.
17: 147√3
16: 147\sqrt{3}
19: \(147\sqrt{3}\)
15: 147√3
18: 147√3 
======
## Actual
 147 * sqrt(3) 

====
Manually added

4 of these 20 were wrong
12: This one gets to a correct end step but that end step doesn't solve the equations. 
I think, following how we are using 'steps' to mean setting up calcs, this is fine. We just want one more step to actually put them together. This final step should be told to make sure it contains the final answer. In a way, this final step is like the executor. But it's only done if needed since i many cases we get the result w/o it.
13: Same as 12. Needs one more step to plug in equations. May need two steps actually.. 
6: This one is interesting. I changed the create_steps to allow it to create less than the given steps if it wanted to. In this one, it regenerated with only two steps. And the first step was super math heavy. Maybe I should remove that less than steps. I also want to eventually ask if to recursively split up steps, but that'll happen later.
14: Same problem - needs one more step to actually do the equations.

Other notes:
- 6 times we fixed incorrect reasoning, so 30%
