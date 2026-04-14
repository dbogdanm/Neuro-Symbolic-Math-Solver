MATH_RULES = \
[   {   'description': 'Infinite tower of powers, repeated exponentiations to infinity, x to the '
                     'power of x to infinity.',
        'hint': 'ATTENTION: An infinite tower of powers only converges for a value <= e^(1/e) ≈ '
                '1.4447. If the value is greater, the equation has no real solution. Answer with '
                '\\boxed{no_solution}.',
        'id': 'teorema_tetratie'},
    {   'description': 'Geometry problem with parallel lines intersected by secants (AB and AC) and '
                     'an isosceles triangle (AB = BC), where the measure of angle x is required.',
        'hint': 'ATTENTION: First determine the angle formed by secant AB using alternate or '
                'supplementary angles. Since the triangle ABC is isosceles (AB = BC), the angles '
                'at the base AC are congruent ($\\angle BAC = \\angle BCA$). Use the sum of the '
                'angles in the triangle ($180^\\circ$) and the properties of parallel lines to '
                'isolate and calculate the value of angle x.',
        'id': 'geometrie_unghiuri_paralele_isoscel'},
    {   'description': 'Combinatorics problem involving seating 7 people at a round table, with the '
                     'restriction that 3 specific people (eg Pierre, Rosa, Thomas) are not allowed '
                     'to sit next to each other (they cannot be adjacent). The number of distinct '
                     'circular arrangements is required.',
        'hint': 'CAUTION: DO NOT use the Principle of Inclusion and Exclusion (PIE), as '
                'calculating the intersection of 3 pairs on a round table frequently leads to '
                "logic errors. Use the 'Gap Method': 1. First seat the other 4 people without "
                'restrictions at the round table using the circular permutations formula: '
                '$(4-1)!$. 2. Notice that these 4 people create exactly 4 empty spaces (gaps) '
                'between them. 3. Place the 3 people with restrictions in these 4 gaps, '
                'calculating arrangements of 4 taken by 3 ($A_4^3$). Multiply the result of the '
                'circular permutations by the result of the arrangements to get the total.',
        'id': 'combinatorica_aranjamente_circulare_restrictii_adiacenta'},
    {   'description': 'Combinatorics problem involving the distribution of 3 types of elements (ice '
                     'cream flavors) to 9 distinct subjects (players), respecting strict '
                     'conditions of order size and minimum presence: $n(C) > n(V) > n(nS) \\ge 1$ '
                     'and their sum being 9. It is required to calculate the total number of '
                     'possible distributions $N$ and the remainder of its division by 1000.',
        'hint': 'To solve the problem, follow these steps: 1. Identify all triplets of positive '
                'integers $(c, v, s)$ that satisfy the conditions: $c + v + s = 9$ and $c > v > s '
                '\\ge 1$. These are the only valid partitions: (6, 2, 1), (5, 3, 1), and (4, 3, '
                '2). 2. For each triplet, calculate the number of ways to assign flavors to the 9 '
                'players using the multinomial coefficient formula: $\\frac{9!}{c! \\cdot v! '
                '\\cdot s!}$. 3. Calculate the values: for (6,2,1) we have $\\frac{9!}{6!2!1!} = '
                '252$, for (5,3,1) we have $\\frac{9!}{5!3!1!} = 504$, and for (4,3,2) we have '
                '$\\frac{9!}{4!3!2!} = 1260$. 4. Sum these results to get $N$ ($252 + 504 + 1260 = '
                '2016$). 5. The final result is the remainder of dividing $N$ by 1000.',
        'id': 'combinatorica_partitii_multimi_coeficienti_multinomiali'},
    {   'description': 'Minimizing a sum of radicals of degree 2 (sqrt) with variables x and y. '
                     'Form: \\sqrt{x^2+a^2} + \\sqrt{y^2+b^2} + \\sqrt{(x-c)^2+(y-d)^2}.',
        'hint': 'CAUTION: DO NOT use partial derivatives! The resulting equations are too complex. '
                "Use Minkowski's Inequality: the sum of the lengths of several vectors is minimal "
                'when the vectors are collinear. 1. Identify the pairwise vectors '
                '(comp_horizontal, comp_vertical) for each radical. For example: \\vec{u}=(x, 20), '
                '\\vec{v}=(30, y), \\vec{w}=(40-x, 50-y). 2. Choose the components so that when '
                'the vectors (\\vec{u}+\\vec{v}+\\vec{w}) are added, the variables x and y cancel. '
                '3. The minimum value is the length of the resulting sum vector: \\sqrt{(\\sum '
                'comp\\_oriz)^2 + (\\sum comp\\_vert)^2}.',
        'id': 'minim_suma_radicali_minkowski'},
    {   'description': 'Converting a point from Cartesian coordinates to polar coordinates.',
        'hint': '1. Use the formulas r = sqrt(x^2 + y^2) and tan(theta) = y/x. 2. For the point '
                '(0,3), x=0 and y=3, so r = sqrt(0^2 + 3^2) = 3. 3. Since the point is on the '
                'positive y-axis, the angle theta is pi/2. 4. The final result in the form (r, '
                'theta) is (3, pi/2).',
        'id': '1_coord_rect_to_polar'},
    {   'description': 'Expressing an infinite double sum in terms of two given infinite sums p and '
                     'q.',
        'hint': '1. Denote the double sum by S. Make a change of variable: let n = j + k. Since j '
                '>= 1 and k >= 1, n varies from 2 to infinity. 2. For a fixed n, the number of '
                'pairs of integers (j, k) satisfying j + k = n is n - 1. 3. Rewrite the double sum '
                'as a simple sum: S = sum_{n=2}^infty (n - 1) / n^3. 4. Separate the fraction: (n '
                '- 1) / n^3 = 1/n^2 - 1/n^3. 5. S = sum_{n=2}^infty (1/n^2) - sum_{n=2}^infty '
                '(1/n^3). 6. Add and subtract the term for n=1: S = (p - 1) - (q - 1) = p - q.',
        'id': '2_series_sum_j_k'},
    {   'description': 'Evaluating a rational function at several points and calculating the sum of '
                     'the values.',
        'hint': '1. Calculate f(-2) replacing x by -2: (3*(-2) - 2) / (-2 - 2) = -8 / -4 = 2. 2. '
                'Calculate f(-1) replacing x by -1: (3*(-1) - 2) / (-1 - 2) = -5 / -3 = 5/3. 3. '
                'Calculate f(0) replacing x with 0: -2 / -2 = 1. 4. Add the three values: 2 + 5/3 '
                '+ 1 = 3 + 5/3 = 14/3. 5. As a neuro-symbolic approach, you can delegate the '
                'computation of the arithmetic expression to a Python interpreter.',
        'id': '3_function_evaluation'},
    {   'description': 'Calculating the number of positive divisors for a given integer (196).',
        'hint': '1. Decompose the number 196 into prime factors. 196 = 14^2 = (2 * 7)^2 = 2^2 * '
                '7^2. 2. Use the formula for the number of divisors: if n = p1^a1 * p2^a2 * ..., '
                'then the number of divisors is (a1 + 1)(a2 + 1)... 3. For 196, the exponents of '
                'both prime factors are 2. 4. Calculate the product (2 + 1)(2 + 1) = 3 * 3 = 9. '
                'The number 196 has 9 positive divisors.',
        'id': '4_number_of_divisors'},
    {   'description': 'Determining the highest average speed based on a distance-time graph.',
        'hint': '1. Average speed is the ratio of distance to time (v = d / t). 2. On a graph with '
                'distance on the y-axis and time on the x-axis, velocity represents the slope of '
                'the line joining the origin to that point. 3. Calculate the y/x ratio for each '
                'plotted point. 4. The point with the highest y/x ratio (steepest slope from the '
                'origin) indicates the student with the highest speed. For example, Evelyn has '
                'approx. 4.5/1.25 = 3.6, way above the rest.',
        'id': '5_greatest_average_speed_graph'},
    {   'description': 'Calculating the perimeter of a regular hexagon knowing the perimeter of one '
                     'of the equilateral triangles into which it was divided.',
        'hint': '1. An equilateral triangle has 3 equal sides. If its perimeter is 21, the side is '
                '21 / 3 = 7 inches. 2. A regular hexagon divided from the center forms 6 '
                'equilateral triangles, where the side of the triangle is equal to the side of the '
                'hexagon. 3. The perimeter of the regular hexagon with 6 sides is 6 * side. 4. '
                'Calculate 6 * 7 = 42 inches.',
        'id': '6_hexagon_perimeter'},
    {   'description': 'Finding the smallest positive perfect cube that can be written as the sum of '
                     'three consecutive integers.',
        'hint': '1. The sum of three consecutive integers (n-1) + n + (n+1) is equal to 3n. 2. So '
                'the perfect cube sought must be a multiple of 3. 3. The smallest positive perfect '
                'cube that is a multiple of 3 must have the factor 3 to the 3rd power (ie '
                'divisible by 27). 4. We check the first such perfect positive cube: 3^3 = 27. 5. '
                'We set 3n = 27, which gives n = 9, so the numbers are 8, 9, 10. The answer is 27.',
        'id': '7_smallest_perfect_cube_sum_consecutive'},
    {   'description': 'Determining the angle between two lines in 3D space given by symmetric '
                     'equations.',
        'hint': '1. Find the direction vector for the first line: 2x = 3y = -z = t implies x=t/2, '
                'y=t/3, z=-t. The vector v1 is proportional to (3, 2, -6). 2. Find the direction '
                'vector for the second line: 6x = -y = -4z = s implies x=s/6, y=-s, z=-s/4. The '
                'vector v2 is proportional to (2, -12, -3). 3. Calculate the dot product v1 dot v2 '
                '= 3*2 + 2*(-12) + (-6)*(-3) = 6 - 24 + 18 = 0. 4. Since the dot product is 0, the '
                'vectors are perpendicular, so the angle is 90 degrees.',
        'id': '8_angle_between_3d_lines'},
    {   'description': 'The intersection of a periodic (or piecewise) function with a non-periodic '
                     'curve (ex: parabola, circle).',
        'hint': "1. It doesn't iterate ad infinitum. Find the bounds where the intersection is "
                'possible. For example, if f(x) is bounded between [a, b], solve the inequality a '
                '<= curve(x) <= b to find the range of x. 2. Use the symmetry of the curve if it '
                'exists (ex: parabolas are symmetric about the vertex). 3. Compute intersections '
                'only in the valid range, then sum the results.',
        'id': 'gen_periodic_func_intersection'},
    {   'description': 'Solving systems of cyclic algebraic inequalities (eg: expressions of the '
                     'form x - yz < y - zx).',
        'hint': '1. Cyclic or symmetric algebraic inequalities usually hide a factorization. 2. '
                'Move all terms to one side of the inequality. 3. Group the terms and force the '
                'common factor (ex: x - y + zx - yz = (x - y)(1 + z)). 4. Analyze the sign of the '
                'obtained factors to deduce the order relationships between the variables (eg: who '
                'is greater, who is positive/negative).',
        'id': 'gen_cyclic_inequalities_factorization'},
    {   'description': 'Calculation of the Expected Value (Expected Value) for geometric '
                     'intersections (eg: chords on a circle).',
        'hint': "1. Don't try to simulate all cases. Use Linearity of Expectation: E[A + B] = E[A] "
                '+ E[B]. 2. To find the expected number of intersections of random chords in a '
                'circle, remember that 4 points on the circle form exactly one pair of chords that '
                'intersect internally (out of the 3 ways to connect them). So the probability is '
                '1/3. 3. Apply combinations: E[intersections] = Combinations(N, 2) * '
                'probability_of_intersection.',
        'id': 'gen_expected_value_geometry'},
    {   'description': 'Minimizing the sum of the distances from a point to the vertices of a '
                     'polygon (ex: AX + BX + CX...).',
        'hint': '1. To minimize distances, do not use complicated derivatives in Cartesian '
                'coordinates. 2. Consider the Triangle Inequality: the minimum distance between '
                'two points is a straight line. 3. Use Unfolding or geometric rotations (such as '
                'the Fermat-Torricelli Point for triangles) to align the points on a single line. '
                '4. If the polygon has special angles (ex: 60, 90 degrees), rotate the sub-figures '
                'to build equilateral triangles or auxiliary rectangles.',
        'id': 'gen_geometric_optimization_distance'},
    {   'description': 'Solving Diophantine equations with sums of large powers and large moduli '
                     '(eg: a^3 + b^3 + c^3 = 0 mod p^k).',
        'hint': '1. AVOID BRUTE FORCE in Python for large modules (eg gives Timeout). 2. Reduce '
                'the problem to a small module first. For example, for cubes, analyze the equation '
                'modulo 9 (perfect cubes modulo 9 are always 0, 1, or -1). 3. After finding the '
                "basic solutions, use Hensel's Lemma (Lifting The Exponent Lemma) to lift the "
                'solution from mode p to mode p^k. 4. Look for symmetries and permutations of '
                'solutions (a, b, c).',
        'id': 'gen_number_theory_modulo_powers'},
    {   'description': 'Extracting the final format required by the problem (eg: answer of the form '
                     'm + n*sqrt(p), requires m+n+p).',
        'hint': '1. When the problem requires computing a final expression from the format '
                'parameters (eg: a + b + c), use SymPy to force pattern matching (eg: expr.match(m '
                '+ n*sqrt(p))). 2. If pattern matching fails, isolate the coefficients by '
                'converting the expression to a dictionary with expr.as_coefficients_dict() or by '
                "substitutions (expr.subs). 3. The 'final_result' variable in the Python code must "
                'ONLY contain the result of the final operation (m+n+p), not the raw math '
                'expression.',
        'id': 'gen_sym_math_format_extraction'},
    {   'description': 'Program-of-Thought (PoT) code optimization to avoid runtime Timeouts.',
        'hint': '1. If the search space is greater than 10^6 iterations, the Python code will '
                'Timeout. 2. Use symbolic math (SymPy) to solve equations analytically instead of '
                "using nested 'for' loops. 3. If you use dynamic programming (DP) or frequency "
                'tables, make sure you apply modular reductions at each step, not just at the end, '
                'to keep the numbers small.',
        'id': 'gen_code_optimization_math'},
    {   'description': 'Counting the number of regions into which a plane or disk is divided by a '
                     'set of lines.',
        'hint': "1. Use Euler's Formula for planar graphs: V - E + F = 1 + C (where F is the "
                'number of regions). 2. A direct theorem for lines in the plane: R = 1 + L + I, '
                'where R is the number of regions, L is the number of lines, and I is the number '
                'of interior intersections. 3. Focus on calculating the number of intersections '
                '(I) using combinatorics or probabilities, then apply the formula.',
        'id': 'gen_graph_theory_regions'},
    {   'description': 'Calculation of the Euclidean distance between two points in the 2D plane.',
        'hint': '1. Use the distance formula: d = sqrt((x2 - x1)^2 + (y2 - y1)^2). 2. Replace the '
                'coordinates: x1=2, y1=-6, x2=-4, y2=3. 3. Calculate the differences: (-4 - 2)^2 = '
                '(-6)^2 = 36 and (3 - (-6))^2 = 9^2 = 81. 4. Add the squares: 36 + 81 = 117. 5. '
                'Simplify the radical: sqrt(117) = sqrt(9 * 13) = 3*sqrt(13).',
        'id': '9_distance_between_points'},
    {   'description': 'Finding the number of distinct values \u200b\u200bthat can be obtained by '
                     'adding parentheses to an arithmetic expression.',
        'hint': '1. The expression is a * b * c * d + e. 2. Any parentheses of the first 4 terms '
                'will not change the result of the product because multiplication is associative, '
                'except when addition (+ 1) is evaluated before some multiplications. 3. Since + '
                'is the last operator, the ways to put parentheses are reduced to when 1 is added. '
                '4. +1 can be added to 5, to (4*5), to (3*4*5), or to the whole product (2*3*4*5). '
                '5. The possible values \u200b\u200bcorrespond to: 2*3*4*(5+1), 2*3*(4*5+1), '
                '2*(3*4*5+1), (2*3*4*5)+1. They all generate distinct results, so there are 4 '
                'values. 6. For a symbolic system, the construction of all parsing trees (Catalan '
                'trees) can be delegated.',
        'id': '10_parentheses_values'},
    {   'description': 'Finding the smallest positive multiple of 30 consisting of only the digits 0 '
                     'and 2.',
        'hint': '1. A number is divisible by 30 if it is divisible by 10 and by 3. 2. Divisibility '
                'by 10 means that the last digit must be 0. 3. Divisibility by 3 means that the '
                'sum of its digits must be divisible by 3. 4. Using only the digits 0 and 2, the '
                "sum of the digits will be 2 * k, where k is the number of digits of '2'. For the "
                'sum to be a multiple of 3, k must be at least 3. 5. The smallest number '
                'consisting of three 2s ending in 0 is 2220.',
        'id': '11_least_multiple_30_digits_0_2'},
    {   'description': 'Determining the value of a polynomial of degree 5 that satisfies a 6-point '
                     'rational relation.',
        'hint': '1. Transform the relation p(n) = n / (n^2 - 1) into the polynomial Q(x) = (x^2 - '
                '1)p(x) - x = 0 for x = 2, 3, 4, 5, 6, 7. 2. Since p(x) has degree 5, Q(x) has '
                'degree 7. The roots of Q(x) are 2, 3, 4, 5, 6, 7. 3. Q(x) is written as A * '
                '(x-2)(x-3)(x-4)(x-5)(x-6)(x-7)(x-r). 4. Notice that Q(1) = -1 and Q(-1) = 1 (from '
                'the definition of Q(x)). Use these two equations to find A and r. 5. After '
                'deducing the final form of Q(x), calculate Q(8) and use it to extract p(8).',
        'id': '12_polynomial_degree_5_interpolation'},
    {   'description': 'Calculation of the sum of the proper divisors for the sum of the proper '
                     'divisors of 284.',
        'hint': '1. Find the sum of the proper divisors of 284. Decomposition: 284 = 2^2 * 71. The '
                'proper divisors are 1, 2, 4, 71, 142. Their sum is 220. 2. Now calculate the sum '
                'of the proper divisors for the new number, 220. Decomposition: 220 = 2^2 * 5 * '
                '11. 3. The proper divisors they are 1, 2, 4, 5, 10, 20, 11, 22, 44, 55, 110. '
                'Adding them, we get 284. 4. Symbolic observation: 220 and 284 form a pair of '
                'friendly numbers.',
        'id': '13_amicable_numbers_284'},
    {   'description': 'Determining the height of a cylinder knowing the volume and radius of the '
                     'base extracted from the diagram.',
        'hint': '1. The formula for the volume of the cylinder is V = pi * r^2 * h. 2. From the '
                'diagram, read the radius r = 3. 3. Substitute the values \u200b\u200bin the '
                'formula: 45 * pi = pi * 3^2 * h. 4. Simplify the equation: 45 = 9 * h. 5. The '
                'result is h = 5 cm.',
        'id': '14_cylinder_height_from_volume'},
    {   'description': 'Using the sine function in a right triangle to find the length of a leg.',
        'hint': '1. Identify the right angle in the diagram (here it is at point F, or E, depends '
                'on asy; according to rightanglemark(D,E,F) the right angle is at E, so the '
                'hypotenuse is DF). 2. The sine function for angle D is the opposite leg above the '
                'hypotenuse: sin(D) = EF / DF. 3. Use the value sin(D) = 0.7 and the lengths given '
                'on the figure to write an equation. 4. Apply the Pythagorean Theorem to find the '
                'required side DE.',
        'id': '15_right_triangle_trig_DE'},
    {   'description': 'Rotating a complex number around another complex number by a certain angle.',
        'hint': '1. The mathematical formula for the rotation of a point z around c by the angle '
                'theta is: w - c = (z - c) * e^(i*theta). 2. Here theta = pi/4, so the multiplier '
                'is cos(pi/4) + i*sin(pi/4) = (sqrt(2)/2) * (1 + i). 3. First calculate the '
                'difference (z - c). 4. Multiply the difference by the complex number of the '
                'rotation. 5. Add c back to the result to get the coordinate of w.',
        'id': '16_complex_rotation'},
    {   'description': 'Calculation of an alternating sum of consecutive numbers from 1 to 100.',
        'hint': '1. Group the terms two by two: (1 - 2) + (3 - 4) + (5 - 6) + ... + (99 - 100). 2. '
                'Calculate the sum of each pair, which is always -1. 3. As there are 100 numbers '
                'in total, exactly 50 pairs are formed. 4. Multiply the number of pairs by the sum '
                'per pair: 50 * (-1) = -50.',
        'id': '17_alternating_sum'},
    {   'description': 'Finding the minimum positive phase shift for a sinusoidal function from its '
                     'graph.',
        'hint': '1. The given equation is of the form y = a * sin(bx + c) + d. The Y-axis '
                'translation is d. 2. Identify the equilibrium axis on the graph, the amplitude a, '
                'and the period (which gives b). 3. The phase shift is -b/b. 4. Find the first '
                'value of x where the function intersects the increasing d equilibrium axis. '
                'There, the phase (bx + c) must be an even multiple of pi (ideally 0). 5. Solve '
                'the inequality to find the smallest positive c.',
        'id': '18_sine_graph_phase_shift'},
    {   'description': 'Determining an angle using the properties of parallel lines and the '
                     'isosceles triangle.',
        'hint': '1. BC is parallel to the line through A. By alternate internal angles, the angle '
                'formed at B (or C) is directly related to the angle at A. 2. We know that AB = '
                'BC, which means that triangle ABC is isosceles, therefore the angles at the base '
                '(BAC and BCA) are equal. 3. Match the adjacent 124-degree angle to the interior '
                'angles using the sum of 180 degrees. 4. Find x from the sum of the interior '
                'angles of the triangle.',
        'id': '19_parallel_lines_isosceles_triangle'},
    {   'description': 'Finding the minimum value for the a parameter such that a reciprocal cubic '
                     'equation has only real roots.',
        'hint': '1. Notice that the equation x^3 + ax^2 + ax + 1 = 0 always has the root x = -1 '
                '(check by substitution). 2. Factor the polynomial by dividing by (x + 1). You get '
                '(x + 1)(x^2 + (a - 1)x + 1) = 0. 3. For all roots to be real, the equation of '
                'degree 2 must have a non-negative discriminant: Delta = (a - 1)^2 - 4 >= 0. 4. '
                'Solve the inequality: (a - 1)^2 >= 4, which for a > 0 implies a - 1 >= 2, i.e. a '
                '>= 3. The minimum value is 3.',
        'id': '20_cubic_roots_real_a'},
    {   'description': 'Evaluating a simple expression with complex numbers.',
        'hint': '1. Respects the order of operations: first perform the multiplication. 2. '
                'Distribute the scalar 6 over the bracket: 6 * 1 + 6 * 2i = 6 + 12i. 3. Subtract '
                'the term 3i from the result: 6 + 12i - 3i. 4. Group the imaginary parts: 12i - 3i '
                '= 9i. The final result is 6 + 9i.',
        'id': '21_complex_arithmetic'},
    {   'description': 'Finding the integer part of a power of the sum of two radicals using the '
                     'conjugate expression.',
        'hint': '1. Write x = (sqrt(7) + sqrt(5))^6 and its conjugate y = (sqrt(7) - sqrt(5))^6. '
                "2. Expanding the sum x + y with Newton's Binomial, all terms with odd powers "
                'reduce, resulting in an even integer N. 3. Since 0 < sqrt(7) - sqrt(5) < 1, it '
                'follows that 0 < y < 1. 4. Since x + y = N and y is fractional, it follows that x '
                '= N - y, so x is N - 1 (an integer) plus a fraction (1 - y). The integer part of '
                'x is therefore N - 1. 5. Calculate N by stepwise exponentiations.',
        'id': '22_greatest_integer_less_than_power'},
    {   'description': 'Solving an algebra problem with proportions and linear equations about pay '
                     'per unit.',
        'hint': '1. Write down the payment factor. The ratio of earnings depends solely on the '
                'number of dogs allocated to each. 2. Case 1: Denali gets 4x dogs (total 16 + 4x), '
                'Nate has 12. Payout ratio is (16 + 4x)/12. 3. Case 2: x dogs are moved from Nate '
                'to Denali. Denali is 16 + x, Nate is 12 - x. The ratio becomes (16 + x)/(12 - x). '
                '4. Since the ratios are equal, construct the equation: (16 + 4x)/12 = (16 + '
                'x)/(12 - x). 5. Multiply by the diagonal, develop and solve the quadratic '
                'equation for x (ignoring the solution x=0).',
        'id': '23_dog_walking_ratio_algebra'},
    {   'description': 'Solving an irrational equation with one variable.',
        'hint': '1. Isolate the radical by moving the constant: x - 4 = sqrt(11 - 2x). 2. Put the '
                'condition of existence of the radical (11 - 2x >= 0) and equality (x - 4 >= 0). '
                '3. Square both sides: (x - 4)^2 = 11 - 2x, which becomes x^2 - 8x + 16 = 11 - 2x. '
                '4. Reduce to standard form: x^2 - 6x + 5 = 0. The roots are 1 and 5. 5. Be sure '
                'to check the roots in the original equation! For x=1 you get 1 = 3 + 4 (false). '
                'For x=5 you get 5 = 1 + 4 (true). The only solution is 5.',
        'id': '24_radical_equation'},
    {   'description': 'Calculation of the minimum compound interest rate for an ordinary annuity '
                     '(annual deposits).',
        'hint': '1. The worker makes 3 deposits at the end of years 1, 2, and 3. 2. Let the '
                'interest rate be r and the multiplier x = 1 + r. The first deposit earns interest '
                'for 2 years, the second for 1 year, the third for 0 years. 3. Add the values: '
                '20000*x^2 + 20000*x + 20000 = 66200. 4. Divide by 20000: x^2 + x + 1 = 3.31, i.e. '
                "x^2 + x - 2.31 = 0. 5. Solve the quadratic equation with Bhaskara's formula "
                '(Delta). The percentage rate is (x - 1) * 100.',
        'id': '25_compound_interest_annuity'},
    {   'description': 'In $\\triangle ABC$, points $D$ and $E$ on side $\\overline{AB}$ and $F$ and '
                     '$G$ on side $\\overline{AC}$ obey certain constant length ratios. Knowing '
                     'the area of \u200b\u200bthe quadrilateral $DEGF$ (288), it is required to '
                     'calculate the area of \u200b\u200ba heptagon obtained by reflecting the '
                     'points $D$ and $G$.',
        'hint': '1. Analyze the given proportions on the sides: note that $AD:DE:EB = 4:16:8 = '
                '1:4:2$ and $AF:FG:GC = 13:52:26 = 1:4:2$. 2. We deduce from these proportions '
                'that the lines are parallel ($DF \\parallel EG \\parallel BC$), which implies the '
                'similarity of three triangles: $\\triangle ADF \\sim \\triangle AEG \\sim '
                '\\triangle ABC$. 3. Use similarity ratios to find areas. The similarity ratio '
                'between $\\triangle ADF$ and $\\triangle AEG$ is $\\frac{1}{5}$, so the ratio of '
                'their areas is $\\frac{1}{25}$. The area of \u200b\u200bthe quadrilateral $DEGF$ '
                'will be $25 - 1 = 24 \\cdot \\text{Area}(\\triangle ADF)$. 4. Calculate the total '
                'area of \u200b\u200b$\\triangle ABC$ knowing that the similarity ratio to '
                '$\\triangle ADF$ is 7, so its area is 49 times larger. 5. By compensating the '
                'areas of the reflections ($M$ and $N$), prove that the required heptagon recovers '
                'the empty spaces and has exactly the same area as the original triangle '
                '$\\triangle ABC$.',
        'id': 'geometrie_asemanare_proportii_arii'},
    {   'description': 'Number theory and algebra problem that requires finding the number of '
                     'ordered pairs of integers $(x,y)$ in the interval $[-100, 100]$ that satisfy '
                     'the homogeneous Diophantine equation of the second degree: $12x^2 - xy - '
                     '6y^2 = 0$.',
        'hint': '1. Factor the quadratic expression as a product of two binomials: $12x^2 - xy - '
                '6y^2 = (4x - 3y)(3x + 2y) = 0$. 2. Separate the problem into two independent '
                'linear equations (cases): $4x = 3y$ and $3x = -2y$. 3. For the first case, write '
                '$y = \\frac{4}{3}x$. The condition that $y$ is an integer requires that $x$ be a '
                'multiple of 3. Calculate how many multiples of 3 exist in the given interval, '
                'subject to the condition that $y \\in [-100, 100]$. 4. Repeat the analysis for '
                'the second case, where $y = -\\frac{3}{2}x$, so $x$ must be even. Find the number '
                'of solutions respecting the limits of the interval. 5. Add the results of the two '
                'cases, but be careful to subtract 1 at the end so as not to count twice the '
                'trivial solution $(0,0)$ that appears in both places.',
        'id': 'algebra_ecuatii_diofantice_omogene'},
    {   'description': 'Counting problem. There are $8!$ distinct 8-digit numbers formed using only '
                     'the digits $1, 2, \\dots, 8$. It is necessary to determine how many of these '
                     'numbers are divisible by $22$.',
        'hint': '1. The criterion of divisibility by 22 simultaneously implies divisibility by 2 '
                '(the last digit is even) and by 11. 2. According to the criterion by 11, the '
                'difference between the sum of the digits in even positions and the sum of those '
                'in odd positions must be a multiple of 11. Since the total sum of the 8 digits is '
                '36, the only valid mathematical option is that both sums be 18. 3. Find the '
                'partitions (the subsets) of exactly 4 distinct digits from the set $\\{1..8\\}$ '
                'that sum to 18. Analysis will show that there are exactly 7 such pairs of '
                'complementary subsets. 4. For each such pair, choose one set for the even '
                'positions and another for the odd positions (and vice versa, multiplying by 2). '
                '5. Apply positional permutations: permute $4!$ ways for odd positions, and note, '
                'for even positions the restriction that the last digit of the general number be '
                'from the set of even digits must be imposed, changing the simple formula of $4!$ '
                'into a probabilistic calculation based on how many even digits the current set '
                'contains.',
        'id': 'combinatorica_permutari_criterii_divizibilitate'},
    {   'description': 'Problem of mathematical analysis and analytic geometry. The intersection of '
                     'a recursively defined sawtooth linear function f(x+4) = f(x) and a parabola '
                     'x = 34y^2. The sum of the ordinates (y) of all intersection points is '
                     'required.',
        'hint': '1. Analyze the periodic function f(x). Its graph is a zigzag between y = -1 and y '
                '= 1. The period is 4. 2. The parabola is horizontal, open to the right, symmetric '
                'about the Ox axis. 3. Since f(x) is bounded between [-1, 1], the intersections '
                'can have the y-coordinate only in the interval [-1, 1]. Therefore, x (which is '
                '34y^2) will take values \u200b\u200bbetween [0, 34]. 4. Calculate how many saw '
                "'teeth' are in the range x of [0, 34]. 5. For each linear segment of the function "
                'f(x) in this interval, write the equation of the segment in the form x = my + c. '
                '6. Substitute in the equation of the parabola: my + c = 34y^2. 7. Use SymPy to '
                'solve the resulting quadratic equations for y, checking that y belongs to the '
                'valid segment. 8. Collect all valid solutions for y. The symmetry of the '
                'functions will cancel out most of the terms, leaving the required expression.',
        'id': '10_functii_liniare_pe_portiuni_parabola_intersectii'},
    {   'description': 'System of nonlinear inequalities in 3D space, restricted to the plane '
                     'x+y+z=75. The defined regions form convex areas. The area of \u200b\u200bthe '
                     'only region with finite area is required.',
        'hint': '1. Simplify the inequalities: x - yz < y - zx becomes (x - y)(1 + z) < 0, and y - '
                'zx < z - xy becomes (y - z)(1 + x) < 0. 2. Combined with the third part, the '
                'inequalities impose sign constraints on the pairs (x-y, 1+z), (y-z, 1+x), and '
                '(z-x, 1+y). 3. Substitute x, y, z using the equation of the plane (eg z = 75 - x '
                '- y) to reduce the problem to a 2D section in an oblique plane. 4. Analyze '
                'regions logically: to obtain a finite region (a triangle in that plane), the '
                'variables must be bounded by the lines x=y, y=z, z=x and x=-1, y=-1, z=-1. 5. '
                'Find the vertices of this triangle in 3D space by solving systems of equations at '
                'the boundaries (intersections of bounding planes/lines). 6. Use the formula for '
                'the area of \u200b\u200ba 3D triangle (half the norm of the vector product of the '
                'sides) via SymPy Vector.',
        'id': '11_inegalitati_algebrice_geometrie_3D_plan_arii'},
    {   'description': 'A disc is divided into 4 quadrants. 25 segments are drawn by connecting '
                     'random edge points in different quadrants. The expected number of regions '
                     'into which the disk is divided is asked.',
        'hint': "1. Use Euler's formula for planar regions: R = 1 + L + I, where R is the number "
                'of regions, L is the number of lines (segments), and I is the number of interior '
                'intersections. 2. Here you have L = 2 + 25 = 27 total lines (2 diameters + 25 '
                'random segments). 3. The task is reduced to computing the expected number of '
                'intersections, E[I]. The linearity of hope allows E[I] = Sum(E[I_jk]) for any '
                'pair of segments j, k. 4. The diameters must intersect in 1 point (the center). '
                '5. Calculate the probability that two random segments (or a segment and a '
                'diameter) intersect, given the restriction that the extremities are in different '
                'quadrants. 6. Program a small Monte Carlo simulator or calculate the exact '
                'combinatorial probabilities, then apply the formula.',
        'id': '12_geometrie_probabilitati_speranta_matematica_linii_disc'},
    {   'description': 'Convex pentagon ABCDE with certain sides and angles (B=E=60 degrees). The '
                     'minimum value of the sum of the distances from some point X to the 5 '
                     'vertices of the pentagon is required (the Fermat-Weber problem for the '
                     'pentagon).',
        'hint': '1. The point that minimizes the sum of the distances to the vertices of a convex '
                'polygon is often related to the intersection of diagonals or Fermat-Torricelli '
                'points. 2. Analyze the 60 degree angles and given lengths. These suggest the '
                "possibility of 'completing' the figure with equilateral triangles or the use of "
                'rotations. 3. Notice the numerical relationships: the sides are 7, 14, 13, 26, '
                '24. These form triangles with remarkable angles (eg the cosine theorem to find '
                'the diagonals). 4. Use the generalized triangle inequality. The minimum sum is '
                'obtained when X collinear with certain minimum distance paths between '
                'non-adjacent vertices. 5. Transform the geometric problem: rotate points B and C '
                'by 60 degrees. The minimum distance often aligns with straight segments resulting '
                "from 'unfolding' by rotating the vertices.",
        'id': '13_geometrie_pentagon_convex_minimizare_distante_fermat_weber'},
    {   'description': 'The number of ordered triplets (a,b,c) with elements up to 3^6, such that '
                     'the sum of the cubes a^3 + b^3 + c^3 is a multiple of 3^7. The remainder of '
                     'dividing this number by 1000 is required.',
        'hint': '1. Analyze cubic residues modulo powers of 3. A number x is congruent to -1, 0, 1 '
                'modulo 3. So x^3 is congruent to -1, 0, 1 modulo 9. 2. For the sum of cubes to be '
                'divisible by 3^7, it must first be divisible by 9. The only way that a^3 + b^3 + '
                'c^3 = 0 (mod 9) is as a, b, c be congruent to (0,0,0) or (1, 1, -2) etc., modulo '
                "3. 3. Use Hensel's Lemma or the 'lifting' property of the exponent (LTE). 4. "
                'Narrow the search space: since a,b,c <= 3^6, you can parametrize the solutions. '
                '5. Delegate a Python script with a smart math approach (not brute force on 3^18): '
                'calculate the frequency of the cubic residuals modulo 3^7 and do the convolution '
                '(or polynomial multiplication/FFT) to find the number of ways to get the desired '
                'sum.',
        'id': '14_teoria_numerelor_congruente_cuburi_modulo'},
    {   'description': 'Six collinear points A-F with specific distances between them. A point G '
                     'outside the line with given distances CG and DG. The area of \u200b\u200bthe '
                     'triangle BGE is required.',
        'hint': '1. Determines the relative positions of points on a line based on given distances '
                '(eg, constructs coordinates on the Ox axis by setting C at the origin). 2. '
                'Calculate the coordinates of points A, B, C, D, E, F along the axis. 3. Use the '
                'coordinates of C, D and the distances CG, DG to find the coordinates of the point '
                "G(x_g, y_g) by solving the circle system (Stewart's or Pythagorean theorem). 4. "
                'After obtaining the coordinates of all points, extract the coordinates of the '
                'vertices of the triangle BGE. 5. Calculate the required area using the '
                'determinant formula (or base BE * height y_g / 2) directly through a SymPy '
                'sequence.',
        'id': '15_geometrie_coliniaritate_teorema_stewart_arii'},
    {   'description': 'The sum of all positive integers n such that n+2 divides the polynomial '
                     'expression 3(n+3)(n^2+9).',
        'hint': '1. Reduce the polynomial expression modulo (n+2). 2. Substitute n = -2 in the '
                'polynomial P(n) = 3(n+3)(n^2+9) (according to the Remainder Theorem). 3. P(-2) = '
                '3 * 1 * 13 = 39. 4. For (n+2) to divide the polynomial, the remainder (39) must '
                'be divisible by (n+2). 5. Find all positive divisors of 39. 6. Match n+2 to each '
                'divisor, solve for n, keep only positive values \u200b\u200b(n > 0). 7. Calculate '
                'the sum of these values.',
        'id': '16_teoria_numerelor_divizibilitate_polinoame'},
    {   'description': 'Coloring 12 segments (red or blue) of a 2x2 grid of unit squares so that '
                     'each of the 4 squares has exactly 2 red and 2 blue sides.',
        'hint': '1. Approach the problem through optimized brute force. There are 12 segments, so '
                '2^12 = 4096 possible colorings in total. This is a very small number for '
                'computers. 2. Identify the 12 segments (eg vertical v1-v6, horizontal h1-h6). 3. '
                'Match each square in the 2x2 grid with the corresponding 4 sides. 4. Write a '
                'Python script that uses `itertools.product` to generate the 4096 combinations. 5. '
                'Checks the condition for each square: the sum of the boolean variables (1 for '
                'red, 0 for blue) of its 4 sides must be exactly 2. 6. Counts the number of valid '
                'configurations.',
        'id': '17_combinatorica_grile_colorare_restrictii'},
    {   'description': 'Evaluating a large product of fractions with logarithms. Logarithm indices '
                     'and arguments follow a quadratic pattern. A fractional form m/n is required.',
        'hint': '1. Use the properties of logarithms: log_A (X^Y) = Y * log_A (X) and change of '
                'base log_a(b) = ln(b)/ln(a). 2. Rewrite the general term of the product. You will '
                'notice that the ln(5) terms cancel (or group). 3. The argument is 5^(k^2 - 1) up '
                'and 5^(k^2 - 4) down. Extract the exponents: k^2 - 1 = (k-1)(k+1) and k^2 - 4 = '
                '(k-2)(k+2). 4. The full expression forms a massive telescoping double product '
                'that will cancel out most of the internal terms, leaving only a few terms at the '
                'limits k=4 and k=63. 5. Write a symbolic SymPy code (using `Product`) or '
                'calculate the remaining terms by hand. 6. Simplify the fraction obtained to '
                'extract m and n.',
        'id': '18_algebra_logaritmi_produse_telescopice'},
    {   'description': 'Triangle ABC with given angles. D,E,F are the means of the sides. The '
                     'circumscribed circle of the triangle DEF (Circle of 9 points) cuts the lines '
                     'BD, AE, AF. A linear combination of the measures of three arcs on this '
                     'circle is required.',
        'hint': '1. Recognize the configuration: the circle circumscribing the median triangle DEF '
                "is the 'Circle of 9 points' of triangle ABC. 2. This circle also contains the "
                'feet of the heights. 3. Use the angular properties of the Circle of 9 points: the '
                'arcs on this circle are twice the corresponding angles in the triangle DEF. 4. '
                'Triangle DEF is similar to triangle ABC (it has the same angles: 84, 60, 36). 5. '
                'Determine the positions of the points G, H, J. G is the intersection of the '
                'circle with BD, i.e. the leg of the altitude in A (since the circle 9 points '
                'passes through the legs of the altitudes). 6. Calculate the angular measures of '
                'the arcs using the inscribed angles. This is a perfect problem to delegate to an '
                'angle geometry solver (or using angle arithmetic in Python with the relationships '
                'demonstrated symbolically).',
        'id': '19_geometrie_cerc_noua_puncte_arce_unghiuri'},
    {   'description': 'Problem of number theory and bases of numeration. Find the sum of all '
                     'integer bases b > 9 for which the number 17_b is a divisor of the number '
                     '97_b.',
        'hint': '1. Convert the numbers to base 10: 17_b = b + 7 and 97_b = 9b + 7. 2. The problem '
                'asks that (b + 7) divide (9b + 7). 3. Delegate the algebraic rewriting to the '
                'symbolic engine: 9b + 7 = 9(b + 7) - 56. For the result to be integer, (b + 7) '
                'must divide by 56. 4. Generate Python code that uses `sympy.divisors(56)` to get '
                'all divisors (positive and negative). 5. For each divisor d, calculate b = d - 7. '
                '6. Filter the results keeping only the values \u200b\u200bwhere b > 9. 7. '
                'Calculate the sum of these valid values.',
        'id': '0_baze_numeratie_divizibilitate_polinoame'},
    {   'description': 'Plane geometry problem with areas, similar triangles and point reflections. '
                     'In the triangle ABC the proportions are given on the sides AB and AC, and '
                     'the area of \u200b\u200ban intermediate quadrilateral DEGF. The area of '
                     '\u200b\u200ba heptagon formed by the reflections of the points is required.',
        'hint': '1. Analyze the proportions of the sides: AD:DE:EB = 4:16:8 = 1:4:2 and AF:FG:GC = '
                '13:52:26 = 1:4:2. Since the ratios are equal, the lines DF, EG, and BC are '
                'parallel. 2. Define in SymPy a symbolic variable S for the area of '
                '\u200b\u200btriangle ADF. 3. Use the similarity theorem: the area of '
                '\u200b\u200btriangle AEG is (1+4)^2 * S = 25S. The area of \u200b\u200bthe '
                'quadrilateral DEGF is the difference of the areas, i.e. 25S - S = 24S. 4. Equate '
                '24S to 288 to find S. 5. Notice that the reflections (M vs. F, N vs. E) create '
                'triangles with areas equivalent to the base due to conservation of distances (eg '
                'area of \u200b\u200bFDM = area of \u200b\u200bADF). 6. Write a Python script that '
                'adds the areas of the geometric components to find the total area of '
                '\u200b\u200bthe heptagon.',
        'id': '1_geometrie_asemanare_triunghiuri_reflexii_arii'},
    {   'description': 'Combinatorics and partitions problem. 9 members choose 3 flavors of ice '
                     'cream, with the restriction of strict inequality between the number of '
                     'choices (chocolate > vanilla > strawberry >= 1). The remainder of dividing '
                     'the total number of associations by 1000 is required.',
        'hint': '1. Model the problem as finding integer partitions (c, v, s) where c + v + s = 9 '
                'and c > v > s >= 1. 2. Ask the Python engine to programmatically find these '
                'triplets (they will be 5+3+1 and 4+3+2). 3. For each valid triplet, the '
                'combinations of players represent permutations with repetition. 4. Use '
                '`math.comb` or multinomial coefficients (9! / (c! * v! * s!)) to calculate '
                'associations for each case. 5. Sum up the results and apply modulo 1000 at the '
                'end.',
        'id': '2_combinatorica_partitii_multinomial_modulo'},
    {   'description': 'Find the number of ordered pairs (x,y) of integers in the interval [-100, '
                     '100] that satisfy the homogeneous Diophantine equation 12x^2 - xy - 6y^2 = '
                     '0.',
        'hint': '1. Treat the expression as a homogeneous polynomial. 2. Delegate the task to the '
                'SymPy engine: `sympy.factor(12*x**2 - x*y - 6*y**2)`. This will result in (4x - '
                '3y)(3x + 2y) = 0. 3. The equation splits into two lines: y = (4/3)x and y = '
                '-(3/2)x. 4. For the first line, x must be a multiple of 3. For the second, x must '
                'be a multiple of 2. 5. Write Python code that iterates x from -100 to 100 and '
                'counts how many pairs (x, y) also have y in the range [-100, 100].',
        'id': '3_ecuatie_diofantica_patratica_factorizare_simbolica'},
    {   'description': 'Digit permutations and divisibility criteria. Out of the 8! numbers made up '
                     'of the digits 1-8 only once, the number of divisible by 22 is required.',
        'hint': '1. A number is divisible by 22 if it is divisible by 2 (the last even digit) and '
                'by 11 (the difference between the sums of the digits on the even and odd '
                'positions is a multiple of 11). 2. The total sum of the digits 1..8 is 36. For '
                'the difference to be 0 or a multiple of 11, the sums of the partitions must be 18 '
                'and 18. 3. Since 8! = 40320 is an extremely small search space for computers, it '
                'delegates direct brute-force solving. 4. Write a Python script using '
                '`itertools.permutations(range(1, 9))` that: forms the number, checks `num % 22 == '
                '0`, counts them (N), and returns the difference required by the problem.',
        'id': '4_teoria_numerelor_divizibilitate_permutari_bruteforce'},
    {   'description': 'Circumscribed isosceles trapezium (inscribed circle) problem. The radius of '
                     'the circle is 3, the area of \u200b\u200bthe trapezoid is 72. The sum of the '
                     'squares of the lengths of the parallel bases r^2 + s^2 is required.',
        'hint': '1. The radius of the inscribed circle is 3, so the height of the trapezoid is h = '
                '6. 2. From the area formula: (r+s)/2 * 6 = 72, the sum of the bases results r+s = '
                "24. 3. Since the quadrilateral has an inscribed circle (Pitot's theorem), the sum "
                'of the bases is equal to the sum of the non-parallel sides: r+s = 2l, from which '
                'the oblique side l = 12. 4. It forms a right triangle lowering the height: the '
                'projection of the oblique side on the large base is (r-s)/2. By the Pythagorean '
                'theorem: ((r-s)/2)^2 + h^2 = l^2. 5. Send the system of equations {r+s=24, '
                '((r-s)/2)^2 + 36 = 144} to SymPy (`sympy.nonlinsolve`) to extract r and s '
                'exactly, then calculate r^2 + s^2.',
        'id': '5_geometrie_trapez_isoscel_circumscris_sisteme'},
    {   'description': 'The letters A-L (12 letters) are randomly grouped into 6 internally '
                     'alphabetically ordered pairs, then the 6 words are alphabetically ordered. '
                     'It asks for the probability that the last word listed contains the letter G.',
        'hint': '1. Approach the problem by counting favorable cases against total cases. The way '
                'to choose the 6 pairs is 11!! = 11*9*7*5*3*1. 2. For the letter G to be in the '
                "last word, the word must be the largest alphabetically. G can only be 'pulled "
                "down' if paired with larger letters (H, I, J, K, L). 3. Write a logical Python "
                'script that recursively generates or combinatorially computes the number of ways '
                'G ends up in the highest-prime pair. 4. Calculate the simplified fraction m/n '
                'with `fractions.Fraction`, then extract the numerator and denominator to '
                'calculate m+n.',
        'id': '6_probabilitati_combinatorica_cuvinte_simulare_exacta'},
    {   'description': 'A system of equations with complex numbers determines exactly one solution. '
                     'The first equation is a circle, the second a median line. The sum of the '
                     'values \u200b\u200bof k is required as a fraction m/n, then m+n.',
        'hint': '1. I translate complex numbers into the Cartesian plane: the first equation is '
                'the circle with center C(25, 20) and radius 5. 2. The second equation is the '
                'geometric place equidistant from the points (k+4, 0) and (k, 3), so the median of '
                'the segment between them. 3. Use `sympy.geometry` or algebraic calculations to '
                'define the k-dependent mediator equation. 4. For the unique solution, the median '
                'must be tangent to the circle, that is, the distance from the center C(25, 20) to '
                'the median must be exactly the radius (5). 5. Solve the resulting modulus '
                'equation for k using SymPy. 6. Add the valid solutions, convert to fraction with '
                '`sympy.Fraction` and return numerator + denominator.',
        'id': '7_numere_complexe_geometrie_analitica_tangenta_fractii'},
    {   'description': 'The parabola y = x^2 - 4 is rotated by 60 degrees trigonometrically. The '
                     'point of intersection in quadrant IV between the original parabola and its '
                     'image is required.',
        'hint': '1. Parameterize the original parabola: P(t) = (t, t^2 - 4). 2. Construct the 2D '
                'rotation matrix for 60 degrees: R = [[cos(60), -sin(60)], [sin(60), cos(60)]]. 3. '
                'Apply the matrix to find the parametric equations of the rotated parabola (X, Y). '
                '4. The intersection condition is that (X, Y) also belongs to the original '
                'parabola, so Y = X^2 - 4. 5. Formulate this complex equation and use '
                '`sympy.solve` to find the root corresponding to quadrant IV (x > 0, y < 0). 6. '
                'Extract the y coordinate in the required form and identify a, b, c by symbolic '
                'pattern matching (`y.match( (a - sqrt(b)) / c )`.',
        'id': '8_geometrie_analitica_parabola_rotatie_intersectie'},
    {   'description': 'Filling in a 3x9 grid with numbers from 1 to 9 so that each row and each of '
                     'the three outlined 3x3 blocks has 9 distinct numbers (as in Sudoku). The '
                     'answer is a product of prime numbers to certain powers.',
        'hint': '1. Break down the problem into completing 3 independent 3x3 blocks (left, center, '
                'right). 2. In the first block, we can place the 9 digits in any way, so 9! '
                'variants. 3. For the second block, the rows must follow the constraints of the '
                'rows in the first block. This is where the concept of permutations without fixed '
                'points (perturbations) on rows or Latin matrices comes into play. 4. Write a '
                'Python script (optimized backtracking or using Latin square formulas) that '
                'calculates exactly the number of variants for blocks 2 and 3 relative to the '
                'first. 5. After getting the total number, use `sympy.factorint(N)` to extract the '
                'prime factors and their powers. 6. Calculate the final formula p*a + '
                '\u200b\u200bq*b + r*c + s*d according to the dictionary returned by the '
                'factorization.',
        'id': '9_combinatorica_grile_sudoku_factorizare_prime'},
    {   'description': 'An isosceles trapezoid has an area of \u200b\u200b$72$ and an inscribed '
                     'circle tangent to all four sides (circumscribing quadrilateral), the radius '
                     'of the circle being $3$. Knowing that the lengths of the parallel bases are '
                     '$r$ and $s$, it is required to determine the value of $r^2 + s^2$.',
        'hint': '1. Rely on the basic property of the circumscribed quadrilateral: the sum of '
                'opposite sides is equal. For the isosceles trapezoid, the sum of the bases '
                '($r+s$) is equal to twice the non-parallel side ($l$). 2. Observe that the height '
                'of the trapezoid ($h$) coincides with the diameter of the inscribed circle: $h = '
                '2 \\cdot 3 = 6$. 3. Substitute in the area formula: $\\frac{(r+s) \\cdot 6}{2} = '
                '72$, from which the sum of the bases $r+s=24$ is obtained, and the non-parallel '
                'side $l=12$. 4. Drop a height from the top of the small base to form a right '
                'triangle. The hypotenuse is $l=12$, a leg is $h=6$, and the projection of the '
                'side on the base is $\\frac{|r-s|}{2}$. 5. Apply the Pythagorean Theorem to find '
                'the value of $(r-s)^2$. 6. With $(r+s)^2$ and $(r-s)^2$ known, apply the '
                'universal algebraic identity $2(r^2+s^2) = (r+s)^2 + (r-s)^2$ to calculate the '
                'final answer.',
        'id': 'geometrie_trapez_circumscriptibil_relatii_metrice'},
    {   'description': 'A system consisting of two equations with complex numbers determines exactly '
                     'one complex solution $z$. The first equation represents a circle given by '
                     '$|25 + 20i - z| = 5$, and the second represents a mediating line dictated by '
                     'the real parameter $k$: $|z - 4 - k| = |z - 3i - k|$. The sum of all '
                     'possible values \u200b\u200bof $k$ is required.',
        'hint': '1. Approach the problem by translating complex numbers into the Cartesian plane. '
                'The first equation translates as the circle with center $C(25, 20)$ and radius '
                '$R=5$. 2. The second equation defines the geometric locus of points in the equal '
                'plane separated by coordinates $(k+4, 0)$ and $(k, 3)$. This geometric place is '
                'the very mediator of the segment formed by the two points. 3. Find the equation '
                'of this median line by calculating the midpoint of the segment and the slope '
                '(which will be the negative inverse of the slope of the segment). The obtained '
                'right will have the equation dependent on the $k$ parameter. 4. For the complex '
                "system to have 'exactly one solution', the mediating line must be fixed tangent "
                'to the circle. 5. Write the formula for the distance from a point (the center of '
                'the circle) to a straight line (the median) and equate it to the radius of the '
                'circle (5). 6. A simple equation of the type $|A - B \\cdot k| will be obtained = '
                'C$. Solve for the two valid values \u200b\u200bof $k$ and perform their sum.',
        'id': 'numere_complexe_geometrie_analitica_tangenta'},
    {   'description': 'Plane geometry problem about side ratios, parallel lines, similar triangles '
                     'and areas of polygons obtained by reflection of points.',
        'hint': 'When several points divide two sides of a triangle in the same ratios, they form '
                'segments parallel to the base. This generates similar triangles. Remember that '
                'the ratio of the areas of two similar triangles is the square of the similarity '
                'ratio. For reflected points, use the principle of conservation of area: the '
                'reflection of a triangle to a point/line has the same area. Calculate the '
                'required area by adding/subtracting triangles from the large figure.',
        'id': '1_geometrie_asemanare_arii_transformari'},
    {   'description': 'Distribution counting problem with strict inequality conditions between '
                     'groups ($a > b > c$).',
        'hint': 'The solution is done in two stages. 1. Find the integer partitions of the total '
                'number that obey the strict inequality (how many elements go into each group). 2. '
                'For each valid partition, since the subjects are distinct, use the multinomial '
                'coefficient formula $\\frac{N!}{a!b!c!}$ to see how many ways they can be '
                'allocated. Finally, add all the results.',
        'id': '2_combinatorica_partitii_multinomial'},
    {   'description': 'Determining the number of integer solutions in a closed interval for a '
                     'Diophantine equation of degree 2, homogeneous.',
        'hint': 'A homogeneous equation of the form $ax^2 + bxy + cy^2 = 0$ can always be factored '
                'into two binomials of degree 1: $(px - qy)(rx - sy) = 0$. Break the equation into '
                'two linear cases (ex: $px = qy$). For the solutions to be integers, $x$ must be a '
                'multiple of the denominator of $y$. Count the multiples in the required range for '
                'each case and be careful not to double count their intersection (usually the '
                'origin $(0,0)$).',
        'id': '3_algebra_ecuatii_diofantice_omogene'},
    {   'description': 'Constructing numbers from distinct digits that meet a compound divisibility '
                     'criterion (eg divisible by 22).',
        'hint': 'Breaks down compound divisibility into prime rules (eg for 22: rules for 2 and '
                '11). The criterion for 11 says that the difference of the sums of the digits '
                '(even vs. odd in position) must be divisible by 11. From the total sum of the '
                'given digits, I deduce exactly what the sum of each subgroup must be. Then, '
                'choose the subsets of digits, permute them on odd positions, and apply the '
                'criterion constraint 2 (last digit be even) to the even positions.',
        'id': '4_combinatorica_permutari_criterii_divizibilitate'},
    {   'description': 'Metric relations in an isosceles trapezoid admitting an inscribed circle '
                     '(circumscribing quadrilateral).',
        'hint': "Use Pitot's Theorem: in a circumscribed quadrilateral, the sum of the opposite "
                'sides is equal. In an isosceles trapezoid, this means that the sum of the bases '
                'is twice the slant. Also, the height of the trapezoid is exactly the diameter of '
                'the inscribed circle. Plot the height to form a right triangle (with leg = '
                'height, hypotenuse = hypotenuse, other leg = semidifference of bases) and apply '
                'Pythagoras to relate the variables.',
        'id': '5_geometrie_trapez_circumscriptibil'},
    {   'description': 'The probability that a given letter appears in the last word formed by '
                     'alphabetically ordered pairs.',
        'hint': 'In a strictly alphabetical sort of pairs, the final position of each pair is '
                'dictated solely by the largest (alphabetical) element in that pair. For a '
                'specific letter (say X) to be in the last pair, it must either be the absolute '
                'maximum element of the entire set, or be "pulled" to the last position if it is '
                'paired with the absolute maximum element. Use combinatorics to count the '
                'favorable pairs over the total number of pairs (which is calculated with double '
                'factorial).',
        'id': '6_probabilitati_imperechere_ordonare'},
    {   'description': 'System of equations in complex numbers with unique solution, involving the '
                     'modulus.',
        'hint': 'Translate complex equations into Cartesian geometry. Equation of type $|z - z_0| '
                '= r$ represents a circle. Equation of type $|z - A| = |z - B|$ represents the '
                'median of the segment $AB$. For the system to have "exactly one solution", the '
                'median must be tangent to the circle. It imposes the condition that the distance '
                'from the center of the circle to the median line is exactly equal to the radius '
                'of the circle and solves the resulting equation.',
        'id': '7_numere_complexe_geometrie_analitica'},
    {   'description': 'Finding the intersection of a parabola and its image rotated about the '
                     'origin.',
        'hint': 'Apply coordinate transformations. Use a rotation matrix or complex numbers to '
                'write a general point on the rotated curve. If $P$ belongs to the first parabola '
                "and $P'$ is its rotated image, the point of intersection must satisfy both "
                'equations. An efficient algebraic approach is to parametrize the parabola (eg '
                '$x=t, y=t^2-C$), rotate it, and force the new coordinates to respect the original '
                'equation of the parabola.',
        'id': '8_geometrie_analitica_rotatie_parabola'},
    {   'description': 'Completing a rectangular grid following strict rules of non-repetition on '
                     'lines and blocks.',
        'hint': 'Approach the problem in sections. The first line/block can always be filled in '
                '$N!$ ways (no restrictions). For adjacent sections, the problem boils down to '
                'counting "arrangements with forbidden positions" (similar to nuisances). For '
                'block intersections, it separates the cases according to which elements are '
                'distributed from the upper blocks, then multiplies the choices using the '
                'fundamental principle of counting.',
        'id': '9_combinatorica_grile_sudoku'},
    {   'description': 'Finding the ordinate sum of the points of intersection between a piecewise '
                     'linear periodic function and a parabola.',
        'hint': 'Draw the graph to see the symmetry of both functions. The periodic function '
                'consists of line segments with simple equations ($y = mx+b$). Due to symmetry '
                'about the coordinate axes, many intersections cancel each other out or occur in '
                'controllable pairs. Identify the individual equations of each line segment, '
                "intersect them with the equation of the second curve, and use Viète's relations "
                'to sum the solutions on each bounded interval.',
        'id': '10_functii_periodice_intersectii'},
    {   'description': 'Calculation of the area of \u200b\u200ba planar region bounded by a set of '
                     'cyclic inequalities in space.',
        'hint': 'Inequalities of the form $A < B < C$ form boundaries when $A=B$, $B=C$, and '
                '$A=C$. The finite region is at the intersection of the principal plane and the '
                'decision planes. Solve the boundary equations to find the coordinates of the '
                'vertices of this 3D triangle (constrained convex polygon of 3 planes). Then apply '
                "a 3D distance formula for the sides and Heron's Formula or vector product formula "
                'to calculate its area.',
        'id': '11_inegalitati_geometrie_3D'},
    {   'description': 'The expected number of regions formed by drawing conditional random strings '
                     'in a circle.',
        'hint': 'The number of regions created by lines in a circle (Euler Characteristic) is $1 + '
                'L + V$ , where $L$ is the number of chords and $V$ the number of interior '
                'intersections. Use Expectation Linearity: $E[Regions] = 1 + L + E[V]$. The '
                'probability that two chords intersect depends on how the ends are chosen (eg if '
                'the ends alternate the order on the circle). Calculates how many pairs of chords '
                'can intersect from the total set.',
        'id': '12_probabilitati_geometrice_regiuni_disc'},
    {   'description': 'Finding the point in the plane that minimizes the sum of the distances to '
                     'the vertices of a convex polygon.',
        'hint': 'When you need to minimize $AX+BX+CX+\\dots$ , the optimal point approaches a '
                'generalized Fermat-Weber point. If the polygon has special angles (eg 60 degrees, '
                '90 degrees), apply the "unfold" method by rotations: rotate the polygon and the '
                'variable point by that special angle. You will transform a broken line (sum of '
                'distances) into a straight line between one fixed end and the rotated image of '
                'another fixed end. The minimum is the length of this line itself.',
        'id': '13_geometrie_punct_Fermat_minimizare'},
    {   'description': 'Counting triplets that obey modulo large divisibility of the sum of three '
                     'perfect cubes.',
        'hint': 'For equations of the type $x^3 + y^3 + z^3 \\equiv 0 \\pmod{p^k}$, first study '
                'the modulo base $p$ or $p^2$ level cases. Cubes have very few possible residues '
                'modulo powers of 3. Analyze the structure of residue classes and use a "lifting" '
                "argument (Lifting The Exponent or Hensel's Lemma): a number of solutions to small "
                'powers of modulo often force clear proportions of valid solutions when extended '
                'to $p^k$.',
        'id': '14_teoria_numerelor_congruente_cuburi'},
    {   'description': 'Finding the area of \u200b\u200ba triangle given the distances from an '
                     'external fixed point to an axis with known collinear points.',
        'hint': "For collinear points on a base connected to an external point, use Stewart's "
                'Theorem or the trigonometric form of the Cosine Theorem in adjacent triangles. '
                'The goal is to determine the height from the outer point to the right (or the '
                'horizontal distance of the projection). Once you know the common height, the area '
                'of \u200b\u200bany triangle formed by a base segment is simply $\\frac{base '
                '\\cdot height}{2}$.',
        'id': '15_geometrie_puncte_coliniare_teorema_Stewart'},
    {   'description': 'Counting the ways to color the edges of a grid so that each cell has a fixed '
                     'parity / number of colors.',
        'hint': 'This problem can be modeled matrixically or by establishing independent variables '
                '(degrees of freedom). If a cell must have 2 red and 2 blue sides, assign +1 and '
                '-1. The sum on each square is 0. Color the top and left edges (which partially '
                'dictate the state). Any shared edge passes the constraint on. It calculates how '
                'many valid configurations you have for the first cell and how they propagate the '
                '"domino effect" on the possibilities of the other cells.',
        'id': '17_combinatorica_grafuri_colorare_restrictii'},
    {   'description': 'Calculating the probability that a given letter appears in the last word '
                     'formed by pairing and alphabetically sorting a given set of letters.',
        'hint': '1. Understand the sorting mechanism: the final word order is dictated solely by '
                "the *first* letter of each pair. 2. For the target letter (eg 'G') to be in the "
                'last word, the first letter of its word must be strictly higher (alphabetically) '
                'than the first letters of all other pairs. 3. If the target were in the second '
                'position in its pair, its word would start with a lower letter than it, so it '
                'would be impossible for it to be last (there being other larger letters in the '
                'set that would "pull" their pairs to the end). So the target *must* occupy the '
                'first position in its pair, i.e. it must be paired with a letter above it '
                'alphabetically. 4. Any other letter higher than the target remaining in play must '
                'be "hidden" in the second position of its pair, otherwise that pair would sort '
                'after the target pair. To be in the second position, absolutely all remaining '
                'upper letters must be paired exclusively with letters lower than the target. 5. '
                'Calculate the probability (Favorable Cases / Total Cases): the total number of '
                'ways to form pairs is calculated by double factorial $(2n-1)!!$. For favorable '
                "cases, combine the number of ways you choose the target's partner with the ways "
                'you choose lower partners for the rest of the upper letters, and finally add the '
                'pairing of the remaining lower letters in between.',
        'id': '30_probabilitati_sortare_alfabetica_perechi'},
    {   'description': 'Simplifying a huge product of fractions with logarithms having progressive '
                     'bases and arguments.',
        'hint': 'It applies the properties of logarithms: $\\log_a(x^p) = p\\log_a(x)$ and uses '
                'the change of base $\\log_a(b) = \\frac{\\ln b}{\\ln a}$. Factors exponents (eg '
                '2nd degree equations). The expression will separate into a product of polynomial '
                'fractions $\\cdot$ product of simple logarithmic fractions. The first will '
                'simplify massively (telescopic fractions, where they cut diagonally), and the '
                'second logarithmic product will reduce completely in the chain.',
        'id': '18_algebra_produse_telescopice_logaritmi'},
    {   'description': 'Calculation of measures of arcs on the circumscribed circle of the median '
                     "triangle (Euler's Circle).",
        'hint': 'The circle that passes through the means of the sides is the Circle of 9 points '
                "(Euler's Circle) and also passes through the feet of the heights. Its "
                'intersections with the lines starting from the vertices create arcs. The measure '
                'of an arc on a circle is twice the angle subtended by the circle. Identify the '
                'right triangles formed and angle-chasing the angles of the original large '
                'triangle to find the required angles.',
        'id': '19_geometrie_cercul_celor_noua_puncte'},
    {   'description': 'The area of \u200b\u200ba rectangle inscribed in a small circle that is '
                     'internally tangent to a large circle, with relations of symmetry and equal '
                     'areas.',
        'hint': 'Approach the problem by Cartesian analytic geometry. Place the origin $(0,0)$ '
                'smartly (at the center of the outer circle or point of tangency). Write the '
                'equations of the two circles. The condition that some lateral areas '
                '(triangles/curvilinear trapezoids) are equal requires that the rectangle has a '
                'strictly symmetrical position. Write the coordinates of the corners of the '
                'rectangle as variables, impose them on the equation of the inner circle, and use '
                'symmetry to deduce the length and width.',
        'id': '20_geometrie_cercuri_tangente_dreptunghi'},
    {   'description': 'The probability that the least common multiple of the elements of a randomly '
                     'chosen subset is a maximum number $N$.',
        'hint': 'Let the target CMMMC = $p^A \\cdot q^B$. For a subset to reach exactly this '
                'CMMMC, it must contain *at least one divisor* that has maximal power $A$ at $p$, '
                'and *at least one* that has $B$ at $q$. It uses the Principle of '
                'Inclusion-Exclusion (PIE) to count the "bad cases": the subsets where the power '
                'of $p$ is strictly less than $A$ , added together with those where the power of '
                '$q$ is strictly less than $B$ , minus their intersection. Subtract the bad cases '
                'from the total of $2^{nr\\_divisors}$.',
        'id': '21_probabilitati_CMMMC_submultimi'},
    {   'description': 'Finding the ranges of values \u200b\u200bfor which a greedy algorithm gives '
                     'a suboptimal coin distribution.',
        'hint': 'The greedy algorithm always works if the denominations are "canonical" (eg powers '
                "of 2). When they aren't, greedy fails when combining a few medium coins exceeds "
                'the value of a large one, but costs fewer pieces (ex: 4 10 coins is worth 40, but '
                'greedy on 40 gives 25+10+1+1+1+1+1). Finds the specific range of numbers for '
                'which the sum of modulo-large-coin residues requires too many small coins, and '
                'deduces the periodic failure rule/pattern.',
        'id': '22_algoritmi_optimizare_greedy_monede'},
    {   'description': 'Counting the solutions of a compound trigonometric function and finding the '
                     'cases where the graph is tangent to the Ox axis.',
        'hint': 'To solve $f(x) = \\sin(g(x)) = 0$, set the inner argument $g(x) = k\\pi$ for an '
                'integer $k$. The points of tangency at the X-axis represent the roots which are '
                "*also* local extreme points, so $f'(x) = 0$. By the Chain Rule, $f'(x) = "
                "g'(x)\\cos(g(x))$. As at those points $\\cos(g(x))$ cannot be 0 (because the sine "
                'is 0), the derivative cancels only if the inner function has a local extremum, '
                "i.e. $g'(x) = 0$. Find the number of solutions for both cases in the required "
                'range.',
        'id': '23_analiza_trigonometrie_intersectii_tangente'},
    {   'description': "Counting selection possibilities with constraints of the type 'X consecutive "
                     "positions cannot be selected' in a row.",
        'hint': 'This is an extended version of the Stars and Bars (Method of Goals) problem. '
                'Transform Condition: If you select chairs, think about the blocks of chairs '
                'selected. The maximum size of a block allowed is 2. Blocks of empty seats between '
                'them must be of size $\\ge 1$. If you denote the number of pairs (blocks of 2) by '
                '$p$ and the number of lone chairs by $s$, you can generate sum equations and '
                'count the valid combinations by iterating over the possible instances of $p$.',
        'id': '24_combinatorica_aranjamente_fara_adiacenta'},
    {   'description': 'Finding the number of ways to perfectly match the vertices of a regular '
                     'polygon using strings of a specific length.',
        'hint': 'Each unique string length corresponds to a "step" or "jump" $k$ around the '
                'regular polygon with $N$ vertices. This decomposes the polygon into independent '
                'cyclic graphs (sub-cycles) according to CMMDC$(N, k)$. If you choose a valid '
                'string, the problem reduces to covering isolated cycles of vertices with '
                '"dominoes" (strings joining adjacent vertices on that cyclic graph). The number '
                'of valid pairs for a linear cycle has recurrent form, but on a full circle only 2 '
                'trivial solutions appear (the two even/odd offsets).',
        'id': '25_combinatorica_grafuri_matchings_poligon'},
    {   'description': 'Relationships in a non-convex polygon constructed from adjacent triangles '
                     'with fixed central angle and constant areas.',
        'hint': 'The area of \u200b\u200bthe triangle formed by consecutive rays from the origin '
                'of the polygon is $\\frac{1}{2} x_n x_{n+1} \\sin(\\theta)$. Since the area and '
                'angle are constant, it follows that the product $x_n x_{n+1}$ is constant, '
                'generating a string of radii whose values \u200b\u200boscillate between 2 states '
                '(if $x_1=a$, then $x_3=a$, etc.). Apply the Cosine Theorem to the outer side and '
                'express the perimeter as a sum dependent on only one variable of radius length, '
                'from which you can calculate any side.',
        'id': '26_geometrie_poligoane_neconvexe_siruri'},
    {   'description': 'Evaluating the value of a string at a large $N$ step, defined by a nonlinear '
                     'fractional recursion.',
        'hint': 'When a string has terms like $x_{k+1} = c(x_k + 1/x_k) + d$, look for a '
                'substitution that linearizes the problem. Most often, the expression form $x_k = '
                '\\frac{a_k + b_k}{a_k - b_k}$ or trigonometric/hyperbolic substitutions is used. '
                'By substituting, you will be able to separate the string into two simple '
                'recursive linear strings for $a_k$ and $b_k$ (exponentials or progressions) and '
                'calculate the term $N$ directly by the obtained general closed term formula.',
        'id': '27_algebra_siruri_recurente_neliniare'},
    {   'description': 'Calculation of the area determined by some interior points whose distances '
                     'to the vertices of the triangle and between them are identical and constant.',
        'hint': 'Equality of distances ($AK=AL=\\dots=KL=d$) means the presence of equilateral '
                'triangles and circles. $A$ and $B$ are on a circle with center $K$. Moreover, the '
                'fixed segment $KL$ forms two equilateral triangles together with other auxiliary '
                'points. Visually translate the problem by "gluing" equilateral triangles to the '
                'edges of the original rectangle. The required quadrilateral becomes a fragment of '
                'a directly calculable area (eg: trapezoid, parallelogram), deduced by '
                'subtractions from the enlarged figure.',
        'id': '28_geometrie_metrica_distantelor_puncte_interioare'},
    {   'description': 'Determining the parameter for which a rational function has an exactly '
                     'specified number of minimum points (local extrema).',
        'hint': "For extreme points, set the first derivative to zero: $f'(x) = 0$. For a rational "
                "function $\\frac{P(x)}{Q(x)}$, the derivative becomes the numerator: $Q(x)P'(x) - "
                'P(x)Q\'(x) = 0$. To have "exactly two real minima", the resulting polynomial '
                'equation of the derivative (usually of high degree) must undergo specific '
                'monotonicity changes, which means the existence of multiple roots (cancelled '
                'delta, second derivative = 0 simultaneously, etc.) at certain asymptotes. Set the '
                'double root condition on the derivative function to find the $k$ parameter.',
        'id': '29_analiza_matematica_extrema_functii_rationale'},
    {   'description': 'The intersection of the trisectors of the angles in a quadrilateral or '
                     'triangle. Angles BAD and CDA trisected, calculation of the angle formed at '
                     'the point of intersection F (AFD).',
        'hint': 'ATTENTION: Do not guess the result! Point F is formed at the intersection of two '
                'rays that trisect the angles at the base. 1. Identify whether F is formed by the '
                'first trisectors (1/3 of the angle) or the second pair (2/3 of the angle). As a '
                "rule, for the 'top' angle (further from the base), 2/3 of the base angles are "
                'used. 2. In the triangle AFD, the measure of the angle AFD is 180 - (measure_FAD '
                '+ measure_FDA). 3. Write Python code that calculates exact fractions (ex: 2/3 * '
                '110) before subtracting from 180. DO NOT hardcode the final result!',
        'id': 'geometrie_trisectoare_intersectie'},
    {   'description': 'Expansion of (sin x)^n or (cos x)^n into multiple angles sin(nx), cos(nx). '
                     'Linearization of powers. Problem asking for constants a, b, c, d in (\\sin '
                     'x)^7 expansion. The coefficient d.',
        'hint': "ATTENTION: To linearize (sin x)^n as sin(kx), use Euler's Formula: sin(x) = "
                '(exp(i*x) - exp(-i*x))/(2*i). Python statement: 1. Define f = (sp.sin(x))**7. 2. '
                'Use sp.expand(f.rewrite(sp.exp)).rewrite(sp.sin) to get the linearized form. 3. '
                'Extract the coefficient of the sin(x) term using f_linearized.coeff(sp.sin(x)).',
        'id': 'trig_linearizare_puteri_n'},
    {   'description': 'Finding the fourth vertex (x, y) of a parallelogram given 3 known points. '
                     'Constraints on coordinates (ex: x > 7 or x < y). Calculation of the sum x + '
                     'y.',
        'hint': 'ATTENTION: Three given points A, B, C can generate three different '
                'parallelograms. If the fourth vertex is D(x, y), it can occupy 3 possible '
                'positions such that the diagonals bisect each other. Use the property: A + D = B '
                '+ C, B + D = A + C, or C + D = A + B. Python code instruction: 1. Compute the 3 '
                'potential points: D1 = B + C - A, D2 = A + C - B, and D3 = A + B - C. 2. '
                'Implement a filter in Python that checks the specified condition (ex: x > 7). 3. '
                'Only after filtering, calculate the x + y sum for the point that meets the '
                'condition.',
        'id': 'paralelogram_coordonate_varf_lipsa'},
    {   'description': 'Rational equations, fractions with x in the denominator, division of an '
                     'expression with x.',
        'hint': "ATTENTION: Don't forget the scope! Checks that the obtained solution does not "
                'cancel the denominator (division by zero). Eliminate false solutions before '
                'writing the result.',
        'id': 'capcana_numitorului'},
    {   'description': 'Euclidean geometry problem with interior tangent circles and an inscribed '
                     'rectangle. Given the circle w1 internal tangent to w2. A rectangle EFGH is '
                     'inscribed in w1. Two resulting triangles have equal areas. The area of '
                     '\u200b\u200bthe rectangle is required as a fraction m/n.',
        'hint': '1. Set up a Cartesian coordinate system. Let the origin be O(0,0) at the center '
                'of w2. Radius w2 = 15. B is the point of tangency at (15, 0). 2. Center A of '
                'circle w1 (radius 6) is on OB at distance 6 from B, so A(9, 0). 3. Diameter BC '
                'implies C(-15, 0). The chord AD perpendicular to BC means x=9 for D. Calculate y '
                'from w2: 9^2 + y^2 = 15^2 -> D(9, 12). 4. The rectangle EFGH is centered on '
                'w1(9,0). Its sides are parallel/perpendicular to BC. Let the coordinates be '
                'F(9+w, h) and G(9-w, h). Being on w1, w^2 + h^2 = 36. 5. Ask the SymPy engine to '
                'exactly express the areas of triangles DGF and CHG as a function of w and h using '
                'the determinant formula (coordinate matrix). 6. Equate the two areas and add the '
                'equation w^2 + h^2 = 36. Solve the nonlinear system using `sympy.nonlinsolve` to '
                'find w and h. 7. The area of \u200b\u200bthe rectangle is 4*w*h.',
        'id': '20_geometrie_euclidiana_cercuri_tangente_arii_coordonate'},
    {   'description': 'Probability and combinatorics on subsets. From a set of divisors of the '
                     'number 2025, a random subset is chosen. It requires the probability that the '
                     'subset is nonempty and the CMMC (Least Common Multiple) of its elements is '
                     'fixed at 2025.',
        'hint': '1. Factor: 2025 = 3^4 * 5^2. 2. Any divisor is of the form 3^i * 5^j, with i '
                'between 0-4 (5 choices) and j between 0-2 (3 choices). There are 15 dividers in '
                'total. 3. The total space of nonempty subsets is 2^15 - 1. 4. For the CMMC of a '
                'subset to be 2025, the subset must contain at least one element where the power '
                'of 3 is 4, and at least one element where the power of 5 is 2. 5. Delegate a '
                'Python script with an Inclusion-Exclusion (PIE) approach. Number of valid subsets '
                '= Total subsets - Subsets (none 3^4) - Subsets (none 5^2) + Subsets (none). 6. '
                'Divide the obtained number by (2^15) and extract the numerator and denominator '
                'for the final result m+n.',
        'id': '21_teoria_numerelor_combinatorica_probabilitati_cmmc_divizori'},
    {   'description': 'Analysis of the Greedy algorithm versus the optimal solution in the Coin '
                     'Change problem. Coins of 1, 10, 25 cents. It asks for the number of values '
                     '\u200b\u200bN in the range [1, 1000] for which the Greedy approach yields '
                     'the same number of coins as Dynamic Programming.',
        'hint': '1. Model the behavior of the Greedy algorithm: N // 25 + (N % 25) // 10 + (N % '
                '25) % 10 coins. 2. Model the optimal behavior (DP) of the Coin Change problem: '
                'dp[i] = 1 + min(dp[i-25], dp[i-10], dp[i-1]). 3. Delegate the solving of a Python '
                'algorithm: initialize array `dp` to 1000 with infinity, `dp[0]=0`. 4. Run a for '
                "loop to complete `dp'. 5. Iterate over i from 1 to 1000 and compare the result of "
                'the greedy formula with `dp[i]`. If they are equal, increment a counter. 6. This '
                'brute force algorithm is executed instantly in Python and guarantees 100% '
                'accuracy.',
        'id': '22_algoritmi_optimizare_greedy_programare_dinamica_rest'},
    {   'description': 'Compound trigonometric equation f(x) = sin(7*pi*sin(5x)) = 0. Count the '
                     'roots in an interval and the points where the graph is tangent to the Ox '
                     'axis.',
        'hint': '1. Analyze the condition f(x) = 0. This means 7*pi*sin(5x) = k*pi, hence sin(5x) '
                '= k/7. Since sine is bounded, k can take integer values \u200b\u200bin the '
                'interval [-7, 7]. 2. For t, the tangency at the Ox axis means that simultaneously '
                "f(x) = 0 and f'(x) = 0. The derivative is f'(x) = cos(7*pi*sin(5x)) * 7*pi * "
                'cos(5x) * 5. For tangency, the only way is for sin(5x) to touch the local '
                'extrema, i.e. cos(5x)=0, which happens when k=7 or k=-7. 3. Formulate the problem '
                "as a Python script using `sympy.solve' or logical counting. 4. The function "
                'sin(5x) makes 5 complete oscillations on [0, 2pi], i.e. it covers the range [-1, '
                '1] 10 times and reaches the maximum 5 times. Use these multipliers on k instances '
                'to find the n+t sum.',
        'id': '23_functii_trigonometrice_ecuatii_derivate_tangente'},
    {   'description': 'Combinatorics and seating problems. Out of 16 seats, 8 occupied seats are '
                     'chosen so that no person has neighbors on both sides (i.e. 3 consecutively '
                     'occupied seats are not accepted).',
        'hint': "1. This is a problem counting binary strings of length 16, with eight 1's and "
                "eight 0's, that do not contain the substring '111'. 2. Since the possible "
                'combinations are only Combinations(16, 8) = 12870, the problem is ideal for '
                'computational simulation instead of complicated recursive formulas. 3. Delegate a '
                'Python script that: imports `itertools.combinations`, generates the 12870 ways to '
                "place 8 '1's in the 16 positions, and checks them iteratively. 4. Check function: "
                'if (current index + 1) and (current index + 2) are in the chosen combination, the '
                'string is invalid. 5. Add the number of valid strings, store in N, and apply N % '
                '1000.',
        'id': '24_combinatorica_siruri_binare_restrictii_adiacente'},
    {   'description': 'In a regular polygon with 24 sides, 12 segments of equal length must be '
                     'drawn that connect each vertex exactly once (equal distance perfect '
                     'coupling).',
        'hint': "1. The distance (or chord type) between two points can be defined by the 'pitch' "
                'k between vertices, where k is from 1 to 12. 2. The polygon breaks into C = '
                'gcd(24, k) disjoint sub-polygons, each having V = 24 / C vertices. 3. For a '
                'sub-polygon to support a perfect coupling of sides (a 1-to-1 matching of '
                'vertices), V must be even. 4. In even V sub-polygons, there are exactly 2 ways to '
                'couple alternating neighbors (for one cycle) - except for k=12, where there is '
                'only one diametrically opposite way. 5. Write Python code that loops k from 1 to '
                '12, calculates C and V, ignores variants where V is odd, and for valid ones adds '
                '2^C (or 1 for k=12) to a total. This logically covers graph couplings.',
        'id': '25_geometrie_combinatoriala_grafuri_cuplaje_poligon'},
    {   'description': 'Polygon with 11 sides. The areas of the triangles formed with the first '
                     'vertex (A1) are 1. The cosines of the angles at A1 are 12/13. The perimeter '
                     'is known. The sum of two specific sides is required.',
        'hint': '1. If the area is 1, 0.5 * A1A_i * A1A_{i+1} * sin(theta) = 1. With '
                'cos(theta)=12/13, sin(theta)=5/13. It follows that the product A1A_i * A1A_{i+1} '
                '= 26/5. This product is constant for all i from 2 to 10. 2. Using the Cosine '
                'Theorem for the perimeter, side A_iA_{i+1}^2 = A1A_i^2 + A1A_{i+1}^2 - '
                '2*(26/5)*(12/13). 3. Define a variable x = A1A_2. The string of distances '
                'alternates: A1A_3 = 5.2/x, A1A_4 = x, etc. By parity, A1A_{11} will end up being '
                'dependent on x in a simple model. 4. The sum A1A_2 + A1A_{11} is fixed the sum of '
                'two elements of this alternation. 5. Write and simplify symbolically in SymPy the '
                'system, applying the perimeter formula as a sum of square roots. The solution '
                'emerges directly from the algebraic evaluation, eliminating manual effort.',
        'id': '26_trigonometrie_geometrie_poligon_concav_arii_laturi'},
    {   'description': 'Recurrent string x_{k+1} = (x_k + 1/x_k - 1)/3 rationally defined. Given x_1 '
                     'and asking for the term x_2025 as an irreducible fraction m/n.',
        'hint': "1. Don't try to find a closed formula by intuition. The string is defined only by "
                'basic algebraic operations. 2. For computers, 2025 iterations represent one '
                'microsecond of computation. 3. Delegate directly to a Python script. 4. Use '
                "Python's `fractions.Fraction` or `sympy.Rational` to ensure that exact precision "
                'is maintained as fractions grow in size (no floating point errors). 5. Write a '
                'for-loop of 2024 steps, apply the operation iteratively. 6. Finally, read the '
                '`.numerator` and `.denominator` attributes of the result, add them and calculate '
                'the remainder modulo 1000.',
        'id': '27_siruri_recurente_functii_rationale_puncte_fixe_iteratii'},
    {   'description': 'Right triangle in A with given hypotenuse. There are two interior points '
                     'with 5 known equal distances from the rest of the points. Area calculation '
                     'for a formed quadrilateral.',
        'hint': '1. Build the system of equations in Python/SymPy. B(b, 0) and C(0, c) with b^2 + '
                'c^2 = 38^2. A(0,0). 2. The conditions AK=AL=14 places K and L on the circle '
                'centered at A of radius 14. 3. The condition KL=14 makes triangle AKL '
                'equilateral. 4. BK=14 means K is on the median of AB, so x_k = b/2. CL=14 means L '
                'is on the median of AC, so y_l = c/2. 5. Combine these constraints: b and c '
                'depend directly on the angle at which the equilateral triangle AKL is rotated. '
                'Send the trigonometric system to `sympy.nonlinsolve`. 6. Once the B, K, L, C '
                'coordinates are symbolically expressed exactly, create `sympy.Polygon(B, K, L, '
                'C)` and ask for the `.area` property to get the format required by the problem.',
        'id': '28_geometrie_triunghi_dreptunghic_sisteme_puncte_interioare_arii'},
    {   'description': 'Rational function f(x) composed of 4 binomials and divided by x, including '
                     'parameter k. We look for the 3 values \u200b\u200bof k for which the '
                     'function has exactly 2 local minimum points.',
        'hint': "1. Analyze the derivative: f(x) = (Polynomial of degree 4) / x. f'(x) brought to "
                'the same denominator will depend on a polynomial of degree 4 in the numerator, '
                'which we call P_4(x). 2. The minimum is obtained from the real roots of P_4(x)=0. '
                'Normally, a function with such behavior can have up to 3 minima and a number of '
                'maxima. To reduce the number of minima to 2, the derivative must lose sign '
                'changes (so P_4 has double roots/tangents on the Ox axis). 3. Double roots of '
                "f'(x) occur when f''(x) = 0 at the same points. 4. Algebraically decompose the "
                'system: P_4(x, k) = 0 and the derivative of P_4(x, k) with respect to x equals 0. '
                "Eliminating x from this system (using resultants or `sympy.solve' simultaneously) "
                'will isolate the polynomial equation in k only. 5. Find the three positive roots '
                'of k from this condition and sum them.',
        'id': '29_calcul_diferential_extreme_locale_polinoame_derivate'},
    {   'description': 'Logarithmic equations, logarithms, log, ln(x), lg(x), sum or difference of '
                     'logarithms.',
        'hint': 'CAUTION: For any logarithmic equation, the logarithm argument must be STRICTLY '
                'POSITIVE (> 0). The base of the logarithm must be > 0 and different from 1. Check '
                'the solutions and eliminate the false ones!',
        'id': 'conditie_logaritmi'},
    {   'description': 'Find the smallest possible value of c in y = a \\sin (bx + c) + d. Graph of '
                     'trigonometric function using [asy] and graph(f). Determining constants a, b, '
                     'c, d.',
        'hint': "ATTENTION: If the problem asks for 'smallest possible value of c' from an [asy] "
                "graph: 1. Search the [asy] code for the line 'return a*sin(b*x + c) + d'. 2. "
                'Identify the value of c directly from that formula. 3. Since sine is periodic, if '
                'c found is positive, check if c - 2*pi is still positive. If c is negative, add '
                '2*pi until you get the smallest positive value. DO NOT invent other conditions '
                '(eg: y(0)=0)!',
        'id': 'trig_graph_params_asy'},
    {   'description': 'Radicals of even order, square root, sqrt(x), irrational equations with '
                     'radical of x.',
        'hint': 'CAUTION: The quantity under an even radical must be >= 0. The result of an even '
                'radical is always >= 0. Squaring may introduce spurious (foreign) solutions. '
                'Check the solutions at the end!',
        'id': 'radicali_ordin_par'},
    {   'description': 'Modulus of x, absolute value, |x|, modulo equations.',
        'hint': 'ATTENTION: The modulus of any real number is always >= 0. An equation of the form '
                '|E(x)| = a, where a < 0, has no real solutions. Treat the cases E(x) >= 0 and '
                'E(x) < 0 separately!',
        'id': 'valoare_absoluta_modul'},
    {   'description': 'Logarithmic or exponential inequalities where the base is a number between 0 '
                     'and 1.',
        'hint': 'ATTENTION: If the base is subunit (0 < b < 1), when dropping the '
                'logarithm/exponential, the MEANING OF THE INEQUALITY CHANGES (< becomes >, etc.).',
        'id': 'inecuatii_logaritmice_baza_subunitara'},
    {   'description': 'Dividing both sides of an equation or inequality by an expression containing '
                     'x.',
        'hint': 'CAUTION: When you divide an inequality in an expression by x, the sign of the '
                'inequality CHANGES if that expression is negative. Analyze the sign of the '
                'expression before dividing, treating the positive and negative cases separately!',
        'id': 'impartire_la_expresie_cu_x'},
    {   'description': 'Equation of degree 2, ax^2 + bx + c = 0, discriminant delta.',
        'hint': 'CAUTION: Real solutions exist ONLY if the discriminant Δ = b² - 4ac >= 0. If Δ < '
                '0, the equation has no real solutions. If Δ = 0, there is only one solution '
                '(double root) x = -b/(2a).',
        'id': 'ecuatia_patratica_discriminant'},
    {   'description': 'Raising to an even power (2, 4, ...) of both members of an inequality.',
        'hint': 'CAUTION: Raising to an even power assumes that BOTH terms are non-negative. If a '
                'member can be negative, you have to treat the cases separately. This step may '
                'introduce false inequalities!',
        'id': 'ridicare_la_putere_para_inecuatie'},
    {   'description': 'Simplifying an expression by division, reducing a common factor.',
        'hint': 'CAUTION: Do not simplify by dividing by an expression that might be zero! If you '
                'simplify x from x·f(x) = x·g(x), you can lose the solution x = 0. Factor and '
                'analyze each case separately.',
        'id': 'impartire_prin_zero'},
    {   'description': 'Equation with modulus of the form |ax^2 + bx + c| = d or |f(x)| = |g(x)|.',
        'hint': 'CAUTION: The equation |f(x)| = |g(x)| is equivalent to f(x) = g(x) OR f(x) = '
                '-g(x). Solve both cases and check the solutions in the original equation.',
        'id': 'ecuatia_modulului_patratic'},
    {   'description': 'System of linear equations, Cramer method, determinant, matrix.',
        'hint': 'ATTENTION: The Cramer method works ONLY if the determinant of the system matrix '
                'is \u200b\u200bzero (det ≠ 0). If det = 0, the system can be incompatible (no '
                'solutions) or indefinitely compatible (infinite solutions). Check the rank!',
        'id': 'sistem_cramer_determinant_zero'},
    {   'description': 'Complex numbers, complex modulus, |z|, argument, trigonometric form.',
        'hint': 'ATTENTION: The modulus of a complex number z = a + bi is |z| = sqrt(a² + b²), '
                'which is always >= 0. The trigonometric form requires the correct calculation of '
                'the argument (angle) taking into account the quadrant z is in.',
        'id': 'numere_complexe_modul'},
    {   'description': "Raising a complex number to a power, De Moivre's formula, z^n.",
        'hint': 'ATTENTION: To calculate z^n, convert to the trigonometric form z = r(cosθ + '
                'i·sinθ), then apply the De Moivre formula: z^n = r^n(cos(nθ) + i·sin(nθ)). Do not '
                'directly raise the real and imaginary part to power!',
        'id': 'putere_numar_complex'},
    {   'description': 'Roots of a complex number, roots of order n of z.',
        'hint': 'CAUTION: The equation z^n = w has EXACTLY n distinct complex solutions. The '
                'solutions are w_k = r^(1/n) · (cos((θ + 2kπ)/n) + i·sin((θ + 2kπ)/n)) for k = 0, '
                "1, ..., n-1. Don't forget any of the n roots!",
        'id': 'radacina_din_numar_complex'},
    {   'description': 'Sum and product of roots of a polynomial, Viète relations, x1+x2, x1·x2.',
        'hint': "CAUTION: Viète's relations apply ONLY if the equation has real solutions (Δ >= "
                "0). The sum of the roots x1+x2 = -b/a and the product x1·x2 = c/a. Don't confuse "
                'them! Always check that the discriminant is non-negative.',
        'id': 'relatiile_lui_vieta'},
    {   'description': 'Biquadratic equation, ax^4 + bx^2 + c = 0, substitution t = x^2.',
        'hint': 'ATTENTION: When substituting t = x^2, the t solutions obtained must be >= 0 to be '
                'able to extract the square root. If t < 0, that solution does not generate real '
                'solutions for x. Each t > 0 generates TWO solutions for x: x = ±√t.',
        'id': 'ecuatie_biquadratica'},
    {   'description': 'Inequality of arithmetic and geometric mean, AM-GM, a+b >= 2sqrt(ab).',
        'hint': 'CAUTION: The AM-GM inequality (arithmetic mean >= geometric mean) applies ONLY to '
                'non-negative numbers (>= 0). Equality occurs ONLY when all numbers are equal to '
                'each other. Do not apply AM-GM to negative numbers!',
        'id': 'inegalitatea_am_gm'},
    {   'description': 'Telescopic sum, telescopic series, sum of consecutive differences f(n+1) - '
                     'f(n).',
        'hint': 'ATTENTION: The telescopic sum of the form Σ[f(k+1) - f(k)] from k=1 to n '
                'simplifies to f(n+1) - f(1). Identify the telescoping structure and write the '
                'first and last terms to see what cancels.',
        'id': 'sir_telescopic'},
    {   'description': 'Prime numbers, prime factorization, CMMDC, CMMMC.',
        'hint': 'ATTENTION: 1 is not a prime number. The number 2 is the only even prime number. '
                'CMMDC(a,b) × CMMMC(a,b) = a × b. If CMMDC(a,b) = 1, the numbers are coprime '
                '(prime to each other).',
        'id': 'numere_prime_si_compuse'},
    {   'description': 'Inverse trigonometric functions, arcsin(x), arccos(x).',
        'hint': 'ATTENTION: The domain of definition for arcsin(x) and arccos(x) is [-1, 1]. If '
                'the argument exceeds these limits, the equation has no real solutions.',
        'id': 'domeniu_arcsin_arccos'},
    {   'description': 'Trigonometric equations with tangent, cotangent, division by sin(x) or '
                     'cos(x).',
        'hint': 'ATTENTION: When dividing an equation by sin(x) or cos(x), check separately also '
                'the cases sin(x) = 0 or cos(x) = 0. You can miss important solutions!',
        'id': 'impartire_trigonometrica_zero'},
    {   'description': 'Trigonometric equations, general solutions, sin(x) = a, cos(x) = a, period.',
        'hint': 'CAUTION: Trigonometric equations generally have infinite solutions due to '
                'periodicity. The general solution for sin(x) = a is x = arcsin(a) + 2kπ OR x = π '
                '- arcsin(a) + 2kπ, k ∈ ℤ. For cos(x) = a: x = ±arccos(a) + 2kπ. Do not forget the '
                'period of the function!',
        'id': 'solutii_periodice_trigonometrie'},
    {   'description': 'Fundamental trigonometric identity, sin^2(x) + cos^2(x) = 1.',
        'hint': 'ATTENTION: The fundamental identity sin²(x) + cos²(x) = 1 is always true. From it '
                'derive: 1 + tan²(x) = 1/cos²(x) and 1 + cot²(x) = 1/sin²(x). Use it to reduce '
                'expressions with sin and cos.',
        'id': 'identitate_pitagoreica'},
    {   'description': 'Addition formulas, sin(a+b), cos(a+b), sin(a-b), cos(a-b), tan(a+b).',
        'hint': 'ATTENTION: sin(a+b) = sin(a)cos(b) + cos(a)sin(b) and cos(a+b) = cos(a)cos(b) - '
                "sin(a)sin(b). Don't confuse the signs! At cos(a+b) the sign is minus, while at "
                'sin(a+b) it is plus.',
        'id': 'formule_adunare_trigonometrie'},
    {   'description': 'Formulas for the double angle, sin(2x), cos(2x), tan(2x).',
        'hint': 'ATTENTION: sin(2x) = 2·sin(x)·cos(x). cos(2x) has THREE equivalent forms: cos²x - '
                'sin²x = 2cos²x - 1 = 1 - 2sin²x. Choose the form that fits the context for easier '
                'simplifications.',
        'id': 'formule_dublului_unghi'},
    {   'description': 'Transformation of sum or difference of sine/cosine into product '
                     '(prosthaphaeresis).',
        'hint': 'ATTENTION: sin(a) + sin(b) = 2·sin((a+b)/2)·cos((a-b)/2). sin(a) - sin(b) = '
                '2·cos((a+b)/2)·sin((a-b)/2). These formulas are useful when you want to factor or '
                'cancel trigonometric expressions.',
        'id': 'transformare_suma_in_produs'},
    {   'description': 'Tangent, cotangent, tg(x), ctg(x), domain of definition.',
        'hint': 'CAUTION: tan(x) is not defined for x = π/2 + kπ (where cos(x) = 0). cot(x) is not '
                'defined for x = kπ (where sin(x) = 0). Exclude these values \u200b\u200bfrom the '
                'field!',
        'id': 'domeniu_tangenta_cotangenta'},
    {   'description': 'Trigonometric inequalities, sin(x) > a, cos(x) < b, solution on '
                     'trigonometric circle.',
        'hint': 'ATTENTION: When solving trigonometric inequalities, represent the solutions on '
                'the trigonometric circle. Pay attention to the direction of travel (trigonometric '
                'sense = counter-clockwise). The solution is an arc of a circle, not a point!',
        'id': 'inegalitati_trigonometrice'},
    {   'description': "Euler's formula, e^(ix) = cos(x) + i·sin(x), the connection with complex "
                     'numbers.',
        'hint': "CAUTION: Euler's formula e^(ix) = cos(x) + i·sin(x) relates trigonometric "
                'functions to complex exponentials. From it: cos(x) = (e^(ix) + e^(-ix))/2 and '
                'sin(x) = (e^(ix) - e^(-ix))/(2i). Famous special case: e^(iπ) + 1 = 0.',
        'id': 'formula_lui_euler'},
    {   'description': 'Limits of functions, indeterminate forms, 0/0, infinity/infinity, '
                     "l'Hopital's rule.",
        'hint': "CAUTION: Apply l'Hôpital's Rule ONLY if the limit is of the form 0/0 or ∞/∞. "
                'Apply it to the numerator and denominator SEPARATELY (not using the quotient '
                'rule!). If after applying an indeterminate form appears again, you can reapply '
                'the rule.',
        'id': 'limite_forme_nedeterminate'},
    {   'description': 'Continuity of a function, continuous function, lateral limit, discontinuity '
                     'jump.',
        'hint': 'CAUTION: A function is continuous in x₀ IF AND ONLY IF: (1) f(x₀) is defined, (2) '
                'the limit exists (side limits are equal), (3) the limit is equal to the value of '
                'the function. Check all three conditions!',
        'id': 'continuitate_functie'},
    {   'description': 'The outstanding limit sin(x)/x, lim sin(x)/x when x->0.',
        'hint': 'CAUTION: The remarkable limit lim(x→0) sin(x)/x = 1 is true ONLY when x is in '
                'radians. If x is in degrees, the formula changes. Also, lim(x→0) (1-cos(x))/x² = '
                '1/2.',
        'id': 'limita_remarcabila_sinx_x'},
    {   'description': "Euler's number is, the limit (1 + 1/n)^n, (1 + x)^(1/x).",
        'hint': 'ATTENTION: lim(n→∞) (1 + 1/n)^n = e ≈ 2.718. More generally: lim(x→0) (1 + '
                'x)^(1/x) = e. The form (1 + α(x))^(1/α(x)) → e if α(x) → 0. Identify the '
                'structure to apply correctly.',
        'id': 'limita_remarcabila_e'},
    {   'description': 'Pliers (sandwich) theorem, inequalities for limits, g(x) <= f(x) <= h(x).',
        'hint': 'CAUTION: If g(x) ≤ f(x) ≤ h(x) around x₀ and lim g(x) = lim h(x) = L, then lim '
                'f(x) = L. Useful for limits of the form sin(x)·bounded_function, since |sin(x)| ≤ '
                '1.',
        'id': 'teorema_sandwich_squeeze'},
    {   'description': 'Asymptote, vertical, horizontal, oblique asymptote, behavior at infinity.',
        'hint': 'ATTENTION: Vertical asymptote: x = a if lim(x→a) f(x) = ±∞. Horizontal asymptote: '
                'y = L if lim(x→±∞) f(x) = L. Oblique asymptote: y = mx + n where m = lim(x→∞) '
                'f(x)/x and n = lim(x→∞) [f(x) - mx].',
        'id': 'asimptote_functie'},
    {   'description': "Darboux's theorem, intermediate values, f(a) and f(b) with opposite sign, "
                     'roots.',
        'hint': 'ATTENTION: If f is continuous on [a,b] and f(a)·f(b) < 0 (opposite signs), then '
                'THERE IS at least one c ∈ (a,b) with f(c) = 0. This theorem guarantees existence '
                'of the root, but not uniqueness!',
        'id': 'teorema_valorilor_intermediare'},
    {   'description': 'Side limits, left limit, right limit, lim x->a-, lim x->a+.',
        'hint': 'ATTENTION: The global limit lim(x→a) f(x) exists ONLY if both side limits exist '
                'and are equal: lim(x→a⁻) f(x) = lim(x→a⁺) f(x). If the side limits are different, '
                'the global limit does NOT exist.',
        'id': 'limite_laterale'},
    {   'description': 'Derivative of the compound function, chain rule, derivative of f(g(x)).',
        'hint': "ATTENTION: The derivative of the composite function f(g(x)) is f'(g(x)) · g'(x). "
                "Don't forget to multiply by the derivative of the inner function! This is a "
                "common mistake with (sin(x²))' = cos(x²) · 2x, not just cos(x²).",
        'id': 'derivata_compusa_chain_rule'},
    {   'description': "The derivative of the inverse function, (f⁻¹)'(x), the derivative of arcsin, "
                     'arccos, arctan.',
        'hint': "ATTENTION: (arcsin(x))' = 1/√(1-x²) defined on (-1,1). (arccos(x))' = -1/√(1-x²). "
                "(arctan(x))' = 1/(1+x²) defined on ℝ. Notice that the derivative of arccos has a "
                'MINUS sign with respect to arcsin!',
        'id': 'derivata_functiei_inverse'},
    {   'description': "The derivative of a product of functions, (f·g)', the Leibniz rule.",
        'hint': "ATTENTION: (f·g)' = f'·g + f·g'. Do not confuse with (f·g)' = f'·g'! This is a "
                'classic mistake. The derivative of the product is NOT the product of derivatives.',
        'id': 'regula_produsului_derivata'},
    {   'description': "The derivative of some functions, (f/g)', the derivative of the fraction.",
        'hint': "ATTENTION: (f/g)' = (f'·g - f·g') / g². The order in the numerator matters: first "
                "f'g, then we subtract fg'. Don't forget to square the denominator! Make sure that "
                'g(x) ≠ 0 on the interval of definition.',
        'id': 'regula_catului_derivata'},
    {   'description': 'Monotonicity of the function, extreme points, local maximum, local minimum, '
                     'first derivative.',
        'hint': "ATTENTION: f'(x) > 0 ⟹ f increasing, f'(x) < 0 ⟹ f decreasing. If f'(x₀) = 0, x₀ "
                "is the extreme CANDIDATE. Check the change of sign of f': if it goes from + to -, "
                'it is a local maximum; from - to +, local minimum. If the sign does not change, '
                'it is NOT extreme!',
        'id': 'monotonie_si_extremele_functiei'},
    {   'description': "Concavity, convexity, inflection point, second derivative, f''(x).",
        'hint': "ATTENTION: f''(x) > 0 ⟹ the function is convex (curved upwards). f''(x) < 0 ⟹ "
                "concave (curved downwards). The inflection point occurs where f''(x) = 0 AND f'' "
                "changes sign. f''(x₀) = 0 alone does not guarantee inflection!",
        'id': 'concavitate_convexitate_derivata_secunda'},
    {   'description': "Mean value theorem, Lagrange's theorem, f'(c) = (f(b)-f(a))/(b-a).",
        'hint': "ATTENTION: Lagrange's theorem guarantees the existence of a c ∈ (a,b) with f'(c) "
                '= (f(b)-f(a))/(b-a), BUT ONLY if f is continuous on [a,b] and differentiable on '
                '(a,b). Check the conditions before applying!',
        'id': 'teorema_lui_lagrange_valoarea_medie'},
    {   'description': "l'Hôpital's rule, indeterminate forms 0·∞, ∞-∞, 0^0, 1^∞, ∞^0.",
        'hint': 'CAUTION: The forms 0·∞, ∞-∞, 0^0, 1^∞, ∞^0 are NOT directly of type 0/0 or ∞/∞. '
                'You have to transform them: 0·∞ → 0/(1/∞) or ∞/(1/0). Forms with powers (0^0, '
                '1^∞) are transformed via logarithm: lim f^g = e^(lim g·ln(f)).',
        'id': 'regula_lhopital_aplicare'},
    {   'description': 'The relationship between derivability and continuity, differentiable '
                     'function vs. continuous function.',
        'hint': 'ATTENTION: If a function is differentiable at x₀, then it is also continuous at '
                'x₀. The converse is NOT true: a function can be continuous but non-differentiable '
                "(eg |x| in 0). In demos, don't confuse the two properties!",
        'id': 'derivabilitate_implica_continuitate'},
    {   'description': 'Optimization problems, maximum and minimum on a closed interval, ends of the '
                     'interval.',
        'hint': 'CAUTION: On a CLOSED interval [a,b], the maximum/minimum value can be reached at '
                "an interior point (where f'=0) OR at the ends of the interval a or b. Compute f "
                'at ALL critical points and ends, then compare!',
        'id': 'optimizare_cu_constrangeri'},
    {   'description': 'Definite integrals, odd functions, symmetric interval, integral from -a to '
                     'a.',
        'hint': 'ATTENTION: The definite integral of an ODD function (f(-x) = -f(x)) on a '
                'symmetric interval [-a, a] is ZERO. The integral of a PARE function (f(-x) = '
                'f(x)) on [-a,a] is twice the integral from 0 to a.',
        'id': 'integrala_impara_simetric'},
    {   'description': 'Indefinite integral, primitive, constant C, antiderivative.',
        'hint': 'ATTENTION: Any undefined (primitive) integral must contain the integration '
                'constant +C at the end. Without +C, the answer is incomplete. The family of '
                'primitives differs by this arbitrary constant.',
        'id': 'constanta_de_integrare'},
    {   'description': 'Integration by parts, ∫u·dv = u·v - ∫v·du, Green-Gauss formula.',
        'hint': 'CAUTION: When integrating by parts ∫u·dv = u·v - ∫v·du, the correct choice of u '
                'and dv is crucial. LIATE Rule: Logarithms, Inverse Trigonometric, Algebraic, '
                'Trigonometric, Exponential – choose u in this order of priority.',
        'id': 'integrare_prin_parti'},
    {   'description': "Change of variable on integration, substitution, ∫f(g(x))·g'(x)dx.",
        'hint': "ATTENTION: When changing the variable t = g(x), don't forget to also change the "
                "differential: dt = g'(x)dx. For DEFINITE integrals, also change the limits of "
                'integration according to the new substitution! Do not revert to the original '
                'variable if you changed the bounds.',
        'id': 'schimbare_variabila_integrare'},
    {   'description': "The fundamental theorem of calculus, the derivative of the integral, F'(x) = "
                     'f(x).',
        'hint': "ATTENTION: If F(x) = ∫[a,x] f(t)dt, then F'(x) = f(x). If the upper bound is a "
                "function g(x), apply the chain rule: d/dx ∫[a,g(x)] f(t)dt = f(g(x)) · g'(x). If "
                'both limits depend on x, break down the integral!',
        'id': 'teorema_fundamentala_calculului'},
    {   'description': 'Improper integral, convergence of the integral, ∫ from a to infinity.',
        'hint': 'ATTENTION: An improper integral ∫[a,∞) f(x)dx converges ONLY if lim(b→∞) ∫[a,b] '
                'f(x)dx exists and is finite. Classic example: ∫[1,∞) 1/x^p dx converges for p > 1 '
                'and diverges for p ≤ 1.',
        'id': 'integrala_improprie_convergenta'},
    {   'description': 'The area of \u200b\u200ba flat surface, the definite integral, the area '
                     'between two curves.',
        'hint': 'ATTENTION: The area between the curves f(x) and g(x) on [a,b] is ∫[a,b] |f(x) - '
                'g(x)|dx. Modulus is ESSENTIAL if the curves intersect on the interval! Find the '
                'intersection points and calculate the integral over each subinterval separately.',
        'id': 'arie_suprafata_integrala'},
    {   'description': 'Integral of powers of trigonometric functions, ∫sin^n(x)dx, ∫cos^n(x)dx.',
        'hint': 'CAUTION: For ∫sin^n(x)dx or ∫cos^n(x)dx: if n is odd, factor out and use '
                'Pythagorean identity. If n is even, use the power-down formulas: sin²x = '
                '(1-cos2x)/2, cos²x = (1+cos2x)/2.',
        'id': 'integrala_functii_trigonometrice_puteri'},
    {   'description': 'Combinatorics, combinations, arrangements, permutations, factorial, C(n,k), '
                     'A(n,k).',
        'hint': 'ATTENTION: For combinations and arrangements, n and k must be natural numbers (≥ '
                '0), and n ≥ k. Any fractional or negative solution is rejected. C(n,0) = C(n,n) = '
                '1. If k > n, C(n,k) = 0.',
        'id': 'conditii_combinari_aranjamente'},
    {   'description': 'The sum of an infinite geometric progression, convergent series, the sum '
                     'from 1 to infinity.',
        'hint': 'ATTENTION: The sum of the infinite geometric progression S = a₁/(1-q) is valid '
                'ONLY if |q| < 1. If |q| ≥ 1, the series diverges and has no finite sum.',
        'id': 'suma_progresie_geometrica_infinita'},
    {   'description': 'Conditional probability, P(A|B), independence of events.',
        'hint': 'CAUTION: P(A|B) = P(A∩B) / P(B), ONLY if P(B) > 0. Two events are independent if '
                "P(A∩B) = P(A)·P(B). Don't confuse independence with incompatibility: incompatible "
                'events (P(A∩B)=0) are usually DEPENDENT!',
        'id': 'probabilitate_conditionata'},
    {   'description': 'Bayes theorem, posterior probability, total probability.',
        'hint': "ATTENTION: Bayes' formula: P(Hₖ|A) = P(Hₖ)·P(A|Hₖ) / Σ P(Hᵢ)·P(A|Hᵢ). Make sure "
                'that the hypotheses Hᵢ form a partition of the space (they are mutually exclusive '
                'and exhaustive). The sum of their probabilities must be 1.',
        'id': 'formula_lui_bayes'},
    {   'description': 'Binomial distribution, probability of k successes out of n trials, B(n,p).',
        'hint': 'ATTENTION: P(X=k) = C(n,k)·p^k·(1-p)^(n-k). Condition: n INDEPENDENT trials with '
                'SAME success probability p. If the probability changes from trial to trial, the '
                'binomial distribution does not apply!',
        'id': 'distributia_binomiala'},
    {   'description': 'Box principle (Pigeonhole), n+1 objects in n boxes, at least one box with 2.',
        'hint': 'ATTENTION: If you distribute n+1 objects into n boxes, at least one box contains '
                'at least 2 objects. Generalization: If you distribute k·n+1 objects into n boxes, '
                "at least one box contains at least k+1 objects. Correctly identify 'objects' and "
                "'boxes'.",
        'id': 'principiul_cutiei_pigeonhole'},
    {   'description': "Newton's binomial, (a+b)^n, binomial coefficients, Pascal's triangle.",
        'hint': 'ATTENTION: (a+b)^n = Σ C(n,k)·a^(n-k)·b^k for k=0,...,n. The general term is '
                'T_{k+1} = C(n,k)·a^(n-k)·b^k. The sum of all coefficients is 2^n. Do not confuse '
                'the term of rank k+1 with the term of rank k!',
        'id': 'binomul_lui_newton'},
    {   'description': 'Mathematical induction, proof by induction, the basic step and the inductive '
                     'step.',
        'hint': 'CAUTION: In proof by induction: (1) check the basis (usually n=1 or n=0), (2) '
                'assume that the statement is true for n=k (induction hypothesis), (3) prove for '
                'n=k+1 USING the hypothesis. Both steps are mandatory!',
        'id': 'inductie_matematica'},
    {   'description': 'Distance from a point to a line, line ax+by+c=0, point (x0,y0).',
        'hint': 'ATTENTION: The distance from the point (x₀,y₀) to the right ax+by+c=0 is d = '
                "|ax₀+by₀+c| / √(a²+b²). Don't forget the modulo in the numerator and the radical "
                'in the denominator! The numerator sign without the mode indicates which side of '
                'the line the point is on.',
        'id': 'distanta_punct_dreapta'},
    {   'description': 'Perpendicularity and parallelism between lines, slopes, director '
                     'coefficients.',
        'hint': 'ATTENTION: Two lines with slopes m₁ and m₂ are parallel if m₁ = m₂ and '
                'perpendicular if m₁·m₂ = -1. If one of the lines is vertical (undefined slope), '
                'treat the case separately! A vertical line is perpendicular to any horizontal '
                'line.',
        'id': 'conditie_perpendicularitate_paralelism'},
    {   'description': 'The scalar product of two vectors, a·b = |a||b|cos(θ), components.',
        'hint': 'ATTENTION: The scalar product a·b = a₁b₁ + a₂b₂ + a₃b₃ = |a|·|b|·cos(θ). Two '
                'vectors are PERPENDICULAR if and only if their scalar product is 0. The scalar '
                'product is COMMUTATIVE: a·b = b·a.',
        'id': 'produsul_scalar_vectori'},
    {   'description': 'The vector product, a×b, the resultant vector perpendicular to both.',
        'hint': 'ATTENTION: The vector product a×b is PERPENDICULAR to both vectors a and b. |a×b| '
                '= |a|·|b|·sin(θ) represents the area of \u200b\u200bthe parallelogram built on a '
                'and b. The vector product is NOT commutative: a×b = -(b×a)!',
        'id': 'produsul_vectorial'},
    {   'description': 'Equation of the circle, center and radius, (x-a)^2 + (y-b)^2 = r^2.',
        'hint': 'CAUTION: The general equation of the circle x²+y²+Dx+Ey+F=0 represents a REAL '
                'circle only if r² = (D/2)²+(E/2)²-F > 0. If r² = 0, it is a point. If r² < 0, the '
                'set is empty. Calculate r² before concluding!',
        'id': 'ecuatia_cercului'},
    {   'description': 'The position of a point relative to a circle, inside, outside, on the '
                     'circle.',
        'hint': 'ATTENTION: Let the circle with center O and radius r be the point P. If |OP| < r, '
                'P is INSIDE the circle. If |OP| = r, P is on the circle. If |OP| > r, P is '
                'OUTSIDE the circle. Calculate the distance and compare with the radius!',
        'id': 'pozitia_punct_fata_de_cerc'},
    {   'description': 'Tangent to a circle from an external point, the number of tangents.',
        'hint': 'ATTENTION: EXACTLY 2 tangents can be drawn from a point outside a circle. From a '
                'point on the circle, exactly 1 tangent. From an inside point, none. The equation '
                'of the tangent at the point (x₀,y₀) to the circle x²+y²=r² is x·x₀ + y·y₀ = r².',
        'id': 'tangenta_la_cerc'},
    {   'description': 'Conic, ellipse, parabola, hyperbola, general equation of degree 2.',
        'hint': 'ATTENTION: The general equation Ax²+Bxy+Cy²+Dx+Ey+F=0 describes: ellipse if '
                'B²-4AC < 0, parabola if B²-4AC = 0, hyperbola if B²-4AC > 0. Calculate the '
                'discriminant to identify the type of conic before other calculations.',
        'id': 'conice_tipuri'},
    {   'description': 'Pythagoras theorem in 3D, diagonal of a parallelepiped, distance in space.',
        'hint': 'ATTENTION: The distance between the points (x₁,y₁,z₁) and (x₂,y₂,z₂) is '
                '√((x₂-x₁)²+(y₂-y₁)²+(z₂-z₁)²). The diagonal of a rectangular parallelepiped with '
                'sides a,b,c is d = √(a²+b²+c²). Do not confuse with face diagonal (2D)!',
        'id': 'teorema_lui_pitagora_spatiu'},
    {   'description': 'Area of \u200b\u200ba triangle with vertices given by coordinates, formula '
                     'with determinant.',
        'hint': 'ATTENTION: The area of \u200b\u200bthe triangle with vertices A(x₁,y₁), B(x₂,y₂), '
                'C(x₃,y₃) is |det([x₂-x₁, y₂-y₁; x₃-x₁, y₃-y₁])| / 2. The module is ESSENTIAL (the '
                'area is positive). If the area = 0, the points are collinear!',
        'id': 'aria_triunghiului_determinant'},
    {   'description': 'Angles in space geometry, dihedral angle, polyhedron angle, projection.',
        'hint': 'ATTENTION: The dihedral angle between two planes is calculated as the angle '
                'between their normals or as the angle between the lines perpendicular to the '
                'common edge, drawn in each plane. Use the dot product of the normals: cos(θ) = '
                '|n₁·n₂| / (|n₁|·|n₂|).',
        'id': 'unghi_poliedru_diedru'},
    {   'description': 'Volumes, polyhedron volume, sphere, cone, pyramid, cylinder.',
        'hint': 'ATTENTION: Volume of sphere = (4/3)πr³. Cone volume = (1/3)πr²h. Pyramid volume = '
                '(1/3)·Base_area·h. Cylinder volume = πr²h. Pay attention to the difference: the '
                'factor 1/3 appears in the cone AND the pyramid, but NOT in the cylinder!',
        'id': 'volume_formule'},
    {   'description': 'Theorem of sines, a/sin(A) = b/sin(B) = c/sin(C) = 2R.',
        'hint': 'ATTENTION: Theorem of sines: a/sin(A) = b/sin(B) = c/sin(C) = 2R, where R is the '
                'radius of the circumscribed circle. Using this theorem, an arcsine angle can be '
                'obtuse or ACUTE – check both possibilities (sin(x) = sin(π-x))!',
        'id': 'teorema_sinusurilor'},
    {   'description': 'Theorem of cosines, c^2 = a^2 + b^2 - 2ab·cos(C), Pythagoras generalization.',
        'hint': 'ATTENTION: The theorem of cosines c² = a²+b²-2ab·cos(C) generalizes Pythagoras. '
                'If cos(C) < 0 (angle C is obtuse), the term -2ab·cos(C) becomes positive, so c² > '
                'a²+b². Checks the type of triangle (acute/obtuse) in the cosine sign.',
        'id': 'teorema_cosinusurilor'},
    {   'description': 'Geometric locus, the set of points satisfying a property, circle, parabola.',
        'hint': 'ATTENTION: A locus is the set of ALL points with a given property, not just a '
                'few. Upon determining it, prove BOTH inclusions: (1) any point in the locus '
                'satisfies the property, (2) any point with the property belongs to the locus.',
        'id': 'locul_geometric'},
    {   'description': 'Modulo congruences, a ≡ b (mod n), modular arithmetic, division remainder.',
        'hint': 'ATTENTION: a ≡ b (mod n) means that n | (a-b). In calculations with congruences '
                'you can add, subtract and multiply, BUT division requires the existence of the '
                'modular inverse. Do not divide directly into congruences – multiply by the '
                'inverse of a (if gcd(a,n)=1).',
        'id': 'congruente_modulo'},
    {   'description': "Fermat's Little Theorem, a^p ≡ a (mod p), p prime number.",
        'hint': "ATTENTION: Fermat's little theorem: if p is prime and gcd(a,p)=1, then a^(p-1) ≡ "
                '1 (mod p). Useful for calculating high powers modulo a prime. Warning: if p is '
                'not prime, the theorem does NOT apply!',
        'id': 'teorema_lui_fermat_mic'},
    {   'description': "Euler's function φ(n), the number of coprime integers with n, Euler's "
                     'theorem.',
        'hint': "ATTENTION: Euler's theorem: a^φ(n) ≡ 1 (mod n), valid when gcd(a,n)=1. φ(p) = p-1 "
                'for p prime. φ(p^k) = p^(k-1)·(p-1). φ is multiplicative: φ(mn) = φ(m)φ(n) if '
                'gcd(m,n)=1.',
        'id': 'functia_lui_euler'},
    {   'description': "Fibonacci sequence, F(n) = F(n-1) + F(n-2), properties, Binet's formula.",
        'hint': "ATTENTION: The general term of the Fibonacci sequence by Binet's formula: F(n) = "
                '(φ^n - ψ^n)/√5, where φ=(1+√5)/2 (the golden section) and ψ=(1-√5)/2. Property: '
                'Any third Fibonacci term is even. gcd(F(m),F(n)) = F(gcd(m,n)).',
        'id': 'sirul_fibonacci_proprietati'},
    {   'description': 'Differential equations, separable variables, dy/dx = f(x)g(y).',
        'hint': 'ATTENTION: When separating the variables, do not forget that if g(y) = 0 there '
                'may be a particular solution y = constant. This singular solution may not be '
                'contained in the general solution. Check separately if g(y) = 0 gives valid '
                'solutions.',
        'id': 'ecuatie_diferentiala_ordinul_1_separabile'},
    {   'description': '2nd order linear differential equation with constant coefficients.',
        'hint': "ATTENTION: The general solution of the equation ay''+by'+cy=0 depends on the "
                'discriminant Δ=b²-4ac: if Δ>0, two distinct real roots; if Δ=0, a double real '
                'root; if Δ<0, conjugate complex roots. Each case gives a different type of '
                'general solution!',
        'id': 'ecuatie_diferentiala_liniara_ordinul_2'},
    {   'description': 'Eigenvalues, eigenvectors, diagonalization of matrices, characteristic '
                     'equation.',
        'hint': 'ATTENTION: The eigenvalues \u200b\u200bare found from the characteristic equation '
                'det(A - λI) = 0. For each eigenvalue λ, the eigenvectors are found by solving '
                '(A-λI)v=0. An eigenvector can NOT be the zero vector! Check that v ≠ 0.',
        'id': 'valori_proprii_vectori_proprii'},
    {   'description': 'Rank of a matrix, Kronecker-Capelli theorem, compatibility of systems.',
        'hint': 'ATTENTION: Kronecker-Capelli theorem: the system Ax=b is compatible IF AND ONLY '
                'IF rank(A) = rank(A|b). If rank(A) = rank(A|b) = n (unknown nos.), the solution '
                'is unique. If rank(A) = rank(A|b) < n, there are infinitely many solutions. If '
                'the ranks differ, the system is incompatible.',
        'id': 'rang_matrice_sistem'},
    {   'description': 'Linear transformations, kernel (ker), image (Im), rank-nullity theorem.',
        'hint': 'ATTENTION: The rank-nullity theorem: dim(ker(T)) + dim(Im(T)) = dim(source '
                'space). dim(ker(T)) is called nullity, dim(Im(T)) is called rank. The '
                'transformation is injective IF AND ONLY IF ker(T) = {0} (nullity = 0).',
        'id': 'transformari_liniare_nucleu_imagine'},
    {   'description': 'Convergence of a series, general term, necessary condition of convergence.',
        'hint': 'CAUTION: NECESSARY (not sufficient) condition of convergence: if the series Σaₙ '
                'converges, then aₙ → 0. The reciprocal is FALSE: the harmonic series Σ(1/n) has '
                "the general term → 0 but DIVERGES. Don't confuse the necessary condition with the "
                'sufficient one!',
        'id': 'convergenta_serie_termenul_general'},
    {   'description': "Ratio criterion (D'Alembert), lim |a_{n+1}/a_n| = L, convergence of the "
                     'series.',
        'hint': "ATTENTION: D'Alembert ratio criterion: let L = lim|a_{n+1}/a_n|. If L < 1, the "
                'series converges absolutely. If L > 1, the series diverges. If L = 1, the '
                'criterion is INCONCLUSION – another criterion must be used (Raabe, Gauss, '
                'comparison, etc.).',
        'id': 'criteriul_raportului_dalembert'},
    {   'description': 'Comparison criterion for series, series less than convergent.',
        'hint': 'ATTENTION: If 0 ≤ aₙ ≤ bₙ for sufficiently large n: if Σbₙ converges, then Σaₙ '
                'converges; if Σaₙ diverges, then Σbₙ diverges. The criterion ONLY works for '
                'series with POSITIVE (or non-negative) terms!',
        'id': 'criteriul_comparatiei_serii'},
    {   'description': 'Taylor series, Maclaurin series, power series development of a function.',
        'hint': 'ATTENTION: The Taylor series of f around a is Σ f^(n)(a)/n! · (x-a)^n. Converges '
                'ONLY within the radius of convergence R. Function = its Taylor series ONLY if '
                'remainder Rₙ(x) → 0. Not every infinitely differentiable function equals its '
                'Taylor series!',
        'id': 'seria_taylor_maclaurin'},
    {   'description': 'Cauchy series, Cauchy criterion of convergence, convergent series implies '
                     'Cauchy series.',
        'hint': 'CAUTION: A convergent series is ALWAYS Cauchy. The converse is true in ℝ (the '
                'completeness of ℝ), but NOT in all metric spaces. A Cauchy string in ℝ ALWAYS '
                'converges.',
        'id': 'sir_cauchy_convergenta'},
    {   'description': 'Arithmetic mean vs. median of a data series, descriptive statistic.',
        'hint': 'ATTENTION: The mean is sensitive to extreme values \u200b\u200b(outliers), while '
                'the median is not. If the distribution is skewed or contains outliers, the median '
                "is a more representative indicator of 'central tendency' than the mean.",
        'id': 'media_versus_mediana'},
    {   'description': 'Variance, dispersion, standard deviation, σ², σ, calculating the spread of '
                     'data.',
        'hint': 'ATTENTION: Population variance σ² = Σ(xᵢ - μ)²/N, and SAMPLE variance s² = Σ(xᵢ - '
                'x̄)²/(n-1) (with n-1, not n!). Dividing by n-1 instead of n is the Bessel '
                "correction to get an unshifted estimator. Don't confuse them!",
        'id': 'varianta_dispersie_deviatia_standard'},
    {   'description': 'Correlation and causation, Pearson coefficient, statistical relationship.',
        'hint': 'CAUTION: STATISTICAL correlation (even strong, with r close to ±1) DOES NOT imply '
                'CAUSATION! Two variables may be correlated because of a common factor '
                '(confounding variable) or by pure coincidence. Do not draw causal conclusions '
                'from observational data without further analysis.',
        'id': 'corelatie_vs_cauzalitate'},
    {   'description': 'Confidence interval, significance level, coverage probability.',
        'hint': 'CAUTION: A 95% confidence interval does NOT mean that the population parameter is '
                'within the interval with 95% probability. It means that the range-building '
                'PROCEDURE produces ranges that contain the parameter 95% of the time. The '
                'parameter either is or is not in the specified range calculated.',
        'id': 'intervalul_de_incredere'},
    {   'description': "Negation of clauses with quantifiers, negation of 'for all' and 'exists'.",
        'hint': "ATTENTION: The negation of '∀x, P(x)' is '∃x, ¬P(x)'. The negation of '∃x, P(x)' "
                "is '∀x, ¬P(x)'. The quantifier changes and the sentence is negated! Common "
                "mistake: writing the negation of '∀x, P(x)' as '∀x, ¬P(x)' – this means something "
                'completely different.',
        'id': 'negarea_cuantificatorilor'},
    {   'description': 'Proof by reduction to the absurd, indirect proof, counter-positive.',
        'hint': 'CAUTION: In the proof by contradiction, you assume that the NEGATION of the '
                'concussion is true and derive a contradiction (a false proposition). The opposite '
                "of 'P ⟹ Q' is '¬Q ⟹ ¬P' and is logically equivalent to the original implication. "
                'Do not confuse with the opposite or conversation!',
        'id': 'demonstratie_prin_contradictie'},
    {   'description': 'Operations with sets, union, intersection, difference, complement, De '
                     "Morgan's laws.",
        'hint': "ATTENTION: De Morgan's laws: complement of union = intersection of complements: "
                '(A∪B)ᶜ = Aᶜ∩Bᶜ, and complement of intersection = union of complements: (A∩B)ᶜ = '
                'Aᶜ∪Bᶜ. They are essential in set theory and logic.',
        'id': 'operatii_cu_multimi'},
    {   'description': 'Cardinal of a set, infinite sets, countability, power set.',
        'hint': 'ATTENTION: |A∪B| = |A| + |B| - |A∩B| (the inclusion-exclusion principle). The '
                "cardinality of the power set P(A) is 2^|A|. There are infinitely many 'types' of "
                "infinity (Cantor): ℕ and ℤ are countable, but ℝ is uncountable (more 'larger').",
        'id': 'cardinalul_multimilor'},
    {   'description': 'Integer part function, floor, ceiling, [x], ⌊x⌋, ⌈x⌉.',
        'hint': 'ATTENTION: ⌊x⌋ (floor) is the largest integer ≤ x. ⌈x⌉ (ceiling) is the smallest '
                'integer ≥ x. Attention: ⌊-2.3⌋ = -3, NOT -2! For negatives, the floor "drops" '
                'more. Also, ⌊x⌋ = x if and only if x ∈ ℤ.',
        'id': 'functia_floor_ceiling'},
    {   'description': 'The sign function (signum), sgn(x), the sign of a real number.',
        'hint': 'ATTENTION: sgn(x) = 1 if x > 0, sgn(x) = 0 if x = 0, sgn(x) = -1 if x < 0. '
                'Property: x = sgn(x)·|x| for any x ∈ ℝ. Do not confuse: sgn(0) = 0, not ±1.',
        'id': 'functia_signum'},
    {   'description': 'The exponential function, e^x, properties, e^x > 0 for any real x.',
        'hint': 'CAUTION: e^x > 0 for ANY x ∈ ℝ – the exponential function is ALWAYS positive, '
                'never zero or negative. e^0 = 1. e^(a+b) = e^a · e^b. (e^a)^b = e^(ab). Do not '
                'confuse e^(a+b) with e^a + e^b!',
        'id': 'functia_exponentiala_proprietati'},
    {   'description': 'Properties of the natural logarithm ln(x), calculation rules.',
        'hint': 'ATTENTION: ln(a·b) = ln(a) + ln(b), ln(a/b) = ln(a) - ln(b), ln(a^r) = r·ln(a). '
                'IMPORTANT ATTENTION: ln(a+b) ≠ ln(a) + ln(b)! There is no simple formula for the '
                'logarithm of a sum. ln(1) = 0, ln(e) = 1.',
        'id': 'proprietati_logaritm_natural'},
    {   'description': 'Changing the base of a logarithm, log_a(b) = ln(b)/ln(a).',
        'hint': 'ATTENTION: log_a(b) = log_c(b) / log_c(a) for any base c > 0, c ≠ 1. Special '
                'case: log_a(b) = 1/log_b(a). Make sure the basis a > 0 and a ≠ 1, and the '
                'argument b > 0 before any calculation.',
        'id': 'schimbare_baza_logaritm'},
    {   'description': 'Notable products, sum and difference of cubes, a^3 ± b^3.',
        'hint': 'ATTENTION: a³+b³ = (a+b)(a²-ab+b²) and a³-b³ = (a-b)(a²+ab+b²). The factor of '
                "degree 2 (a²∓ab+b²) is IRREDUCIBLE in ℝ (the discriminant is negative). Don't "
                'factor it anymore! Common mistake: writing a³+b³ = (a+b)³.',
        'id': 'produsul_notabil_suma_cub'},
    {   'description': "Descartes' rule of signs, the number of positive/negative roots of a "
                     'polynomial.',
        'hint': "CAUTION: Descartes' rule: the number of POSITIVE real roots of the polynomial "
                'P(x) is equal to the number of sign changes of the coefficients OR that number '
                'minus an even number. The negative roots of P(x) correspond to the positive roots '
                'of P(-x).',
        'id': 'regula_semnelor_descartes'},
    {   'description': 'Cauchy-Schwarz inequality, (Σaᵢbᵢ)² ≤ (Σaᵢ²)(Σbᵢ²).',
        'hint': 'ATTENTION: Cauchy-Schwarz inequality: (a₁b₁+a₂b₂+...+aₙbₙ)² ≤ '
                '(a₁²+...+aₙ²)(b₁²+...+bₙ²). Equality occurs IF AND ONLY IF vectors (a₁,...,aₙ) '
                'and (b₁,...,bₙ) are proportional (one is a scalar multiple of the other).',
        'id': 'inegalitatea_cauchy_schwarz'},
    {   'description': 'The triangle inequality, |a+b| ≤ |a|+|b|, the norm of the vectors.',
        'hint': 'ATTENTION: Triangle inequality: |a+b| ≤ |a|+|b|. Equality occurs ONLY when a and '
                'b have the same sign (or one is zero). Reverse version: ||a|-|b|| ≤ |a-b|. Also '
                'valid for vectors and complex numbers!',
        'id': 'inegalitatea_triunghiului'},
    {   'description': 'Periodicity of compound functions, period of function f(ax+b).',
        'hint': 'ATTENTION: If f(x) has period T, then f(ax+b) has period T/|a| (not T!). Example: '
                'sin(2x) has period π = 2π/2, not 2π. For the sum of periodic functions, the '
                'resulting period is the LCM (CMMMC) of the periods, IF it exists.',
        'id': 'functii_periodice_compuse'},
    {   'description': 'Monotonicity of inverse functions, if f is increasing/decreasing, then '
                     'f⁻¹...',
        'hint': 'ATTENTION: If f is STRICTLY MONOTONOUS (increasing or decreasing) and continuous, '
                'then f⁻¹ exists and has the SAME monotonicity as f. An inverse function of an '
                'increasing function is also increasing; of a decreasing, also decreasing.',
        'id': 'monotonie_functii_inverse'},
    {   'description': 'Parity and oddness of functions, f(-x) = f(x) or f(-x) = -f(x).',
        'hint': 'ATTENTION: A function is even if f(-x) = f(x) for any x in the domain, and odd if '
                'f(-x) = -f(x). The domain must be SYMMETRICAL about 0. The sum/difference of two '
                'even functions is even; an odd two is odd; an even with an odd is generally '
                'neither even nor odd.',
        'id': 'paritate_imparitate_functii'},
    {   'description': 'Divisibility between numbers expressed in an arbitrary base b (eg: 17_b '
                     'divide 97_b).',
        'hint': '1. Convert both base 10 numbers as polynomials in b (ex: 17_b = b+7, 97_b = '
                '9b+7). 2. The divisibility condition becomes an algebraic relation in b — '
                'simplify by subtraction or modular reduction: if d | A and d | kA, then d | (B - '
                'kA). 3. You get that (expression in b) divides a constant — so find the divisors '
                'of that constant. 4. Impose the constraints of the problem (ex: b > 9, b integer) '
                'and filter out valid values \u200b\u200bof b.',
        'id': 'gen_base_divisibility'},
    {   'description': 'Calculation of the area of \u200b\u200ba polygon defined by reflections of '
                     'points on the sides of a triangle.',
        'hint': '1. Identify the ratios where the points divide the sides—if the ratios are '
                'proportional on different sides, there is an exploitable symmetry. 2. Express the '
                'coordinates of the reflections directly from the definition (the reflection of P '
                "through Q means Q is the midpoint of the segment P-P'). 3. Decompose the large "
                'polygon into simpler regions (triangles or quadrilaterals) whose area is '
                'expressed as a fraction of the area of \u200b\u200bthe base triangle. 4. Use the '
                'area scaling factor: if a triangle has sides in ratio k to the large triangle, '
                'its area is k² of the large area.',
        'id': 'gen_reflection_area_decomposition'},
    {   'description': 'Counting ordered distributions of an integer n into k categories with strict '
                     'inequality constraints between categories.',
        'hint': '1. Explicitly enumerate valid triplets/k-tuples (there are usually few if the sum '
                'is small). 2. For each valid tuple (c₁ > c₂ > ... > cₖ, sum = n), the number of '
                'assignments of elements to categories is the multinomial C(n, c₁) · C(n-c₁, c₂) · '
                '.... 3. Sum over all valid tuples and apply the required operation (eg: mod '
                '1000). 4. If the sum is large, use function generators or inclusion-exclusion to '
                'count efficiently.',
        'id': 'gen_constrained_composition_counting'},
    {   'description': 'Integer pairs (x,y) satisfying a homogeneous equation of degree 2: '
                     'ax²+bxy+cy²=0.',
        'hint': '1. The homogeneous equation of degree 2 always factorizes as a product of two '
                'linear forms over ℚ: (px+qy)(rx+sy) = 0. 2. Solve the factorization (treat the '
                'discriminant as a perfect square or factor directly). 3. Each factor equal to '
                'zero defines a straight line through the origin with rational slope. 4. On each '
                'line, count the integer pairs (x,y) in the given domain — on the line px+qy=0, '
                'the solutions are (qt, -pt) for integer t. 5. Add and remove the duplicate at the '
                'origin.',
        'id': 'gen_homogeneous_quadratic_diophantine'},
    {   'description': 'Counting the permutations of a set of digits that form numbers divisible by '
                     'a composite number (eg: 22, 33, 36...).',
        'hint': '1. Decompose the divisibility condition into independent conditions for each '
                'prime factor (ex: div/22 = div/2 AND div/11). 2. div/2 condition: last digit must '
                'be even — fix last digit and count remaining permutations. 3. The div/11 '
                'condition: the alternative sum of the digits ≡ 0 (mod 11) — the total sum is '
                'fixed, so the difference between the sum of the digits on odd and even positions '
                'must be a multiple of 11. 4. Combine the two conditions by the principle of '
                'inclusion-exclusion or direct counting by cases. 5. Check that the possible '
                'values \u200b\u200bof the alternating difference are feasible and count the '
                'corresponding permutations.',
        'id': 'gen_permutations_with_divisibility'},
    {   'description': 'Properties of an Inscribed Circle (Isosceles) Trapezoid—Base, Height, and '
                     'Radius Relationships.',
        'hint': '1. A quadrilateral has an inscribed circle ⟺ the sum of the opposite sides are '
                'equal: a+c = b+d. For a trapezoid: sum of bases = sum of oblique sides. 2. Height '
                'of trapezoid with inscribed circle = diameter of the circle = 2r. 3. Area of '
                '\u200b\u200bthe trapezoid = r · semiperim = r · (large_base + small_base + '
                '2·oblique_side)/2. But also Area = (large_base + small_base)/2 · 2r, so Area = '
                'r·(r+s). 4. From Aria and r you get r+s (the sum of the bases). 5. Use Pythagoras '
                'on the isosceles trapezoid to relate the hypotenuse to the difference of the '
                'bases and the height, obtaining a second relationship to determine r·s and hence '
                'r²+s².',
        'id': 'gen_inscribed_circle_trapezoid'},
    {   'description': 'Probability associated with the extreme pair (lexicographic max/min) from a '
                     'random list of pairs.',
        'hint': '1. Identify what determines the maximum/minimum lexicographic element: the first '
                'letter (or number) as large (or small) as possible, equal to the second. 2. The '
                'extreme element depends almost exclusively on how the largest (or smallest) '
                'element of the set is paired. 3. Compute the probability by conditioning on the '
                'extreme element pair: if X is the largest element and is paired with Y, the last '
                "word is 'XY' or 'YX' (reordered alphabetically). 4. Check if another word can "
                "exceed 'YX' lexicographically — generally not, if X is the absolute maximum. 5. "
                'Compute P(item of interest is Y or X) over the uniform space of possible pairs.',
        'id': 'gen_probability_lexicographic_pairing'},
    {   'description': 'Systems in complex plane with circle and another geometric location (median, '
                     'line, circle) — unique solution condition.',
        'hint': '1. Interpret each equation geometrically: |z - z₀| = r is a circle, |z - A| = |z '
                '- B| is the median of segment AB, Re(z) = c or Im(z) = c are straight lines. 2. '
                'Unique solution of the system = geometric tangency between the two places: circle '
                'tangent to the line, or two circles tangent. 3. The tangency condition: the '
                'distance from the center of the circle to the line (or to the other center) = the '
                'radius (or the sum/difference of the radii). 4. Calculate distance as a function '
                'of parameter k and enforce equality with radius — you get equation in k. 5. Solve '
                'the equation (can be quadratic), add the solutions.',
        'id': 'gen_complex_circle_and_locus'},
    {   'description': 'The intersection of an algebraic curve with its image rotated by a given '
                     'angle about the origin.',
        'hint': '1. Rotation by angle θ transforms (x,y) into (x·cosθ - y·sinθ, x·sinθ + y·cosθ). '
                '2. A point P=(x,y) lies on both curves (original and rotated) if: P satisfies the '
                'original equation, and the inverse rotation (with -θ) of P also satisfies the '
                'original equation. 3. Substitute the inverse rotation into the equation of the '
                'original curve, get a system of two equations in x,y. 4. Eliminate one of the '
                'variables and solve the remaining equation—filter the solutions by the required '
                'quadrant. 5. If the angle is special (30°, 45°, 60°), the exact values '
                '\u200b\u200bof sin/cos greatly simplify the calculations.',
        'id': 'gen_curve_rotation_intersection'},
    {   'description': 'Counting completions of a grid with Latin Square or Sudoku type constraints '
                     '(uniqueness on lines/columns/blocks).',
        'hint': '1. Identify the structure: how many blocks there are, how row constraints '
                'interact with block constraints. 2. Complete the blocks sequentially: the first '
                'block has n! free variants, subsequent blocks are constrained by the previous '
                'block by row constraint. 3. The problem reduces to counting compatible '
                'permutations between blocks: if each row in block 1 fixes a partial permutation '
                'of the symbols, how many ways are there to distribute the remaining symbols in '
                'blocks 2 and 3. 4. Express the answer as a product of factors, identify the '
                'factorization as a product of powers of primes, and compute the required linear '
                'combination.',
        'id': 'gen_latin_square_sudoku_counting'},
    {   'description': 'Intersections of a curve (parabola, exponential, etc.) with a piecewise '
                     'linear and periodic function.',
        'hint': '1. Identify the period and the explicit form of the function on each subinterval '
                'of a period. 2. Reverse the problem: instead of y=f(x), find for what values '
                '\u200b\u200bx=g(y) (the inverse of the curve) intersects each line segment of f. '
                '3. On each line segment f(x) = ax+b (or equivalent), the intersection with the '
                'curve becomes a simple algebraic equation (quadratic, etc.). 4. Determine how '
                'many solutions each equation has that fall in the correct segment interval. 5. '
                'Exploit symmetry with respect to Ox to simplify the sum of y coordinates '
                '(symmetric terms cancel).',
        'id': 'gen_piecewise_periodic_curve_intersection'},
    {   'description': 'Regions defined by algebraic inequalities on a plane in ℝ³ — finite region '
                     'identification and area computation.',
        'hint': '1. Substitute the plane constraint (ex: x+y+z=C) to reduce to two free variables. '
                '2. Rewrite each inequality in terms of the two free variables and simplify—often '
                'inequalities factor elegantly (ex: (x-y)(1+z) < 0). 3. Each simplified inequality '
                'defines a half-plane in the 2D plane — their intersection is a polygon (or '
                'unbounded region). 4. Identify which of the 3 (or more) regions is bounded by '
                'solving pairwise systems of equality to find the vertices. 5. Calculate the area '
                'in the 3D plane: if the plane has normal n̂, the 3D area = the projected 2D area '
                '× |n̂| (factor √(a²+b²+c²) if the plane is ax+by+cz=d).',
        'id': 'gen_plane_inequality_regions_3d'},
    {   'description': 'Expected number of regions created by segments (chords) in a disc — '
                     "application of Euler's formula.",
        'hint': "1. Euler's formula for planar subdivisions: R = E - V + 2, where R = regions "
                '(including the outer one), E = edges, V = vertices. Or: interior regions = I + C '
                '- V_interior + 1, where I = interior intersections, C = chords, V_interior = '
                'points on the circle. 2. Compute E[V] = points on circle (deterministic or '
                'expected) + E[interior intersections]. 3. E[interior intersections] = '
                'C(nr_segments, 2) × P(two given segments intersect). 4. The intersection '
                'probability depends on the distribution of endpoints on the circle — two chords '
                'intersect if and only if their ends alternate on the circle. 5. Apply the '
                "linearity of hope to each term in Euler's formula.",
        'id': 'gen_expected_regions_euler_formula'},
    {   'description': 'Counting solutions to congruences of type aⁿ+bⁿ+cⁿ ≡ 0 (mod pᵏ) — '
                     'p-valuation and the Lifting Lemma (LTE).',
        'hint': "1. Write each term as pᵅ·a' with a' not divisible by p. The p-value of the term "
                'is n·α. 2. When two or more terms have the same minimum value, the value of their '
                'sum is not immediately obvious — apply the Lemma of Raising the Exponent (LTE): '
                'vₚ(aⁿ±bⁿ) = vₚ(a±b) + vₚ(n) (under certain conditions). 3. Divide into cases '
                'according to the values \u200b\u200b(α, β, γ) of a, b, c — the all-equal case is '
                'the most delicate. 4. For each case, determine the constraints on the residues '
                'modulo powers of p and count the solutions. 5. Sum the contributions of all '
                'cases, using symmetry when possible.',
        'id': 'gen_padic_valuation_lifting_exponent'},
    {   'description': 'Calculating the area of \u200b\u200ba triangle formed by points on a line '
                     'and an exterior point, using given distances.',
        'hint': '1. Place all collinear points on the Ox axis with a reference point at the '
                'origin. Set the coordinates of the other points as unknown and write the system '
                'of equations from the given distances. 2. Solve the linear system to determine '
                'the absolute positions of all points on the axis. 3. Determine the coordinates of '
                'the outer point using its distances from two known collinear points: '
                '(x-xₐ)²+y²=dₐ² and (x-x_b)²+y²=d_b² — subtracting the equations gives x, then y. '
                '4. Area of \u200b\u200bthe triangle = (1/2) · base (on the collinear axis) · '
                'height (y-coordinate of the outer point).',
        'id': 'gen_collinear_points_exterior_triangle_area'},
    {   'description': 'Finding the integers n for which (n+k) divides a polynomial expression into '
                     'n.',
        'hint': '1. Substitute m = n+k, so n = m-k. Rewrite the expression completely in terms of '
                'm. 2. Reduce each factor modulo m: any multiple of m vanishes, so n ≡ -k (mod m), '
                'n² ≡ k² (mod m), etc. 3. Condition m | expression(m) reduces to m | constant, '
                'where the constant is calculated by substituting n = -k in the original '
                'expression. 4. Find all positive divisors of the constant, filter the values '
                '\u200b\u200bfor which n = m-k satisfies the constraints of the problem (positive, '
                'in the interval, etc.). 5. Sum the valid values.',
        'id': 'gen_divisibility_by_substitution'},
    {   'description': 'Coloring the edges (or cells) of a grid with local per-cell or per-node '
                     'constraints.',
        'hint': '1. Label each edge/cell and identify what constraints connect the local variables '
                '(ex: each square must have exactly k sides of color A). 2. Choose a completion '
                'order (eg row by row, or from the top left corner) and determine what freedoms of '
                'choice remain at each step. 3. Note that interior edges are shared between two '
                'cells — constraining a square propagates information to its neighbor. 4. If the '
                'number of cases is small, list through organized backtracking; if large, builds a '
                "recursion on the 'profile' of a row. 5. Check if the problem requires distinct "
                "colorings modulo symmetries (rotations, reflections) and apply Burnside's lemma "
                'if so.',
        'id': 'gen_grid_coloring_local_constraint'},
    {   'description': 'Telescopic products or sums involving logarithms with variable bases.',
        'hint': '1. Rewrite log_a(b^k) = k · log(b)/log(a) using base change in natural or decimal '
                'logarithm. 2. Each factor of the product becomes a ratio of the form (f(k) · '
                'log(g(k))) / (h(k) · log(j(k))). 3. Factor the numerators and denominators '
                'algebraically (ex: k²-1 = (k-1)(k+1)) to highlight telescoping cancellations. 4. '
                'Write the extended product and identify which terms remain after telescopic '
                'cancellation. 5. Calculate the numerical value of the reduced product and '
                'simplify the fraction m/n.',
        'id': 'gen_telescoping_log_product'},
    {   'description': 'Arcs of the circumcircle of the medial triangle, with additional points '
                     'defined by intersections with medians or sides of the original triangle.',
        'hint': '1. The medial triangle DEF of ABC has the same angles as those of ABC (∠FDE=∠A, '
                '∠DEF=∠B, ∠EFD=∠C) — a consequence of the fact that the sides of the medial '
                'triangle are parallel to the sides of ABC. 2. Arcs of the circumcircle of DEF: '
                'arc DE (subtended by ∠EFD) = 2·∠C, arc EF = 2·∠A, arc FD = 2·∠B. 3. For '
                'additional points G, H, J on the circle, use properties of inscribed angles and '
                'relationships to the original triangle to determine their arcs. 4. The median of '
                'a triangle and the property that the center of gravity, orthocenter, circumcenter '
                "are collinear (Euler's right) can help to locate points accurately. 5. Add the "
                'arcs required according to the formula in the problem.',
        'id': 'gen_circumcircle_medial_triangle_arcs'},
    {   'description': 'Rectangle inscribed in a small circle interior tangent to a large circle — '
                     'additional geometric conditions.',
        'hint': '1. Set the coordinate system with the center of the great circle at the origin '
                'and the relevant diameter on the Ox axis. Determines the positions of all fixed '
                'points in the problem data. 2. Parameterize the rectangle inscribed in the small '
                'circle by the halves of the sides (a, b) with a²+b²=r² (the radius of the small '
                'circle). 3. Write the explicit coordinates of the vertices of the rectangle '
                'according to a, b and the center of the small circle. 4. Express the additional '
                'conditions (ex: equal areas, equal distances) as equations in a and b. 5. Solve '
                'the system {a²+b²=r², additional_condition} to obtain area = 4ab (or required '
                'form).',
        'id': 'gen_two_circles_inscribed_rectangle'},
    {   'description': 'The probability that the lcm of a random subset of the set of divisors of N '
                     'is even N.',
        'hint': '1. Factor N = p₁^a₁ · p₂^a₂ · ... · pₖ^aₖ. The set of divisors A has '
                '(a₁+1)(a₂+1)...(aₖ+1) elements. 2. lcm(B) = N ⟺ for every prime pᵢ, the maximum '
                'exponent of pᵢ in the elements of B is exactly aᵢ. 3. Conditions for different '
                'premiums are independent at the subset level (an element has one component per '
                'premium). 4. P(exp_max for pᵢ = aᵢ in B) = [no. subsets of divisors with exp_max '
                '= aᵢ] / 2^(total_no_divisors). Use inclusion-exclusion: P(max=aᵢ) = P(max≤aᵢ) - '
                'P(max≤aᵢ-1). 5. Multiply the probabilities (prime independence) and adjust for '
                'the empty subset if necessary.',
        'id': 'gen_lcm_subset_divisors'},
    {   'description': 'Optimality Analysis of a Greedy Algorithm for a Coin/Object Remainder '
                     'Problem—Finding Exceptions.',
        'hint': '1. Understand when greedy fails: there is an alternative solution with less '
                'coins/items. Failures occur systematically around certain values. 2. Analyze the '
                'greedy structure: for each value N, simulate the algorithm and obtain the greedy '
                'solution (no. of coins). 3. Compare with the optimal solution — can be calculated '
                'by dynamic programming for all values \u200b\u200bin the range. 4. Identify the '
                'pattern of N values \u200b\u200bwhere greedy fails: it is often determined by N '
                'modulo (the large denominator) and the relationships between the denominators. 5. '
                'Systematically count the N values \u200b\u200bin the interval where greedy is '
                'optimal vs. no, maybe by multiplying the number of exceptions per period.',
        'id': 'gen_greedy_algorithm_optimality'},
    {   'description': 'The zeros and points of tangency of functions of the type sin(a·sin(bx)) or '
                     'cos(f(sin(x))).',
        'hint': '1. f(x) = sin(a·sin(bx)) = 0 ⟺ a·sin(bx) = kπ ⟺ sin(bx) = kπ/a. Valid values '
                '\u200b\u200bof k are those for which |kπ/a| ≤ 1. 2. For each valid k, the '
                'equation sin(bx) = kπ/a has a fixed number of solutions on the given interval — '
                'compute it separately for k=0, k≠0, |k|=a/π (extreme case). 3. Total sum of zeros '
                'n = (solutions for k=0) + 2·(solutions for k>0, |kπ/a|<1) + (solutions for '
                "|kπ/a|=1). 4. Tangency at Ox: f(x)=0 and f'(x)=0 simultaneously. f'(x) = "
                'a·b·cos(a·sin(bx))·cos(bx) = 0, so cos(bx)=0 OR cos(a·sin(bx))=0. Combine with '
                'f(x)=0 to see which cases are compatible. 5. Count the tangency points t and '
                'calculate n+t.',
        'id': 'gen_nested_trigonometric_zeros'},
    {   'description': 'Enumeration of fixed-cardinal subsets of an array of n elements, with no k '
                     'consecutive elements.',
        'hint': '1. Define f(n, r, j) = the number of subsets of r elements in {1,...,n} without '
                'consecutive j. 2. Recursion is based on the decision for element n: if n ∉ S, the '
                'problem reduces to f(n-1, r, j). If n ∈ S, if n-1 ∉ S reduces to f(n-2, r-1, j), '
                'if n-1 ∈ S and n-2 ∉ S reduces to f(n-3, r-2, j), etc. — with j-1 cases for as '
                'many consecutive ones ending in n. 3. Alternatively, use the substitution that '
                "'compresses' the blocks: a non-j consecutive subset of r elements in n "
                'bijectively corresponds to a subset of r elements in n-(r-1)(j-2) without '
                'constraints (classical substitution). 4. Calculate the value for the problem '
                'parameters and apply mode if required.',
        'id': 'gen_no_three_consecutive_subset'},
    {   'description': 'Counting perfect-matchings with fixed-length edges on the vertices of a '
                     'regular polygon.',
        'hint': '1. A regular polygon with 2n vertices — edges of fixed length join vertices at '
                'distance d (steps). All segments have the same length ⟺ the same jump d on the '
                'polygon. 2. Identify the d values \u200b\u200bfor which there is at least one '
                'perfect matching: the graph formed by jump edges d on 2n vertices must be a union '
                'of cycles covering all vertices — it is possible iff 2n/gcd(2n,d) is even (or '
                'equivalently, the graph has matching factors). 3. Once d is fixed, the graph has '
                'cyclic structure — it is a union of gcd(2n,d) cycles of length 2n/gcd(2n,d). The '
                'number of perfect matches per cycle of length 2k is 2 (if k>1) or 1. 4. Multiply '
                "the contributions of each related component and sum over all valid d's.",
        'id': 'gen_perfect_matching_regular_polygon'},
    {   'description': 'Polygons with fixed relationships between consecutive sides at the same '
                     'vertex—hidden geometric recurrences.',
        'hint': '1. If all triangles formed by a fixed vertex A₁ with two consecutive vertices '
                'have equal area and equal angle at A₁, the product of the distances r_i · r_{i+1} '
                '= constant (from the area formula = (1/2)·r_i·r_{i+1}·sin(angle)). 2. The '
                'recurrence r_{i+1} = C/r_i is alternating geometric — the sequence is periodic '
                'with period 2: r₁, r₂, C/r₂, r₂, C/r₂, ... 3. Use the additional constraint '
                '(perimeter, or sum of distances) to form a system in r₂ and C/r₂. 4. The length '
                'of the sides of the polygon is calculated by the law of cosines from r_i, r_{i+1} '
                'and angle. 5. Solve for the required unknowns.',
        'id': 'gen_hidden_geometric_sequence_polygon'},
    {   'description': 'Rational strings defined by a nonlinear recurrence—periodicity detection and '
                     'calculation of a far term.',
        'hint': '1. Calculate the first 5-10 terms numerically to detect a potential period. If x₁ '
                '= x_{k+1} for a small k, the sequence is periodic with period k. 2. Try '
                'substitutions that linearize the recurrence: xₙ = (aₙ/bₙ), or xₙ = cot(θₙ), '
                'tan(θₙ), or a Möbius function xₙ = (αyₙ+β)/(γyₙ+δ). 3. A Möbius recurrence xₙ₊₁ = '
                '(axₙ+b)/(cxₙ+d) corresponds to the repeated multiplication of the matrix '
                '[[a,b],[c,d]] — diagonalizes the matrix or calculates its nth power. 4. If the '
                'matrix has eigenvalues \u200b\u200broots of unity, the recurrence is periodic — '
                'identifies the order. 5. Calculate x₂₀₂₅ = x_{2025 mod T} and determine m+n from '
                'fractional form.',
        'id': 'gen_rational_recurrence_periodicity'},
    {   'description': 'Geometry problems where the condition of equality of several distances '
                     'forces the appearance of hidden equilateral triangles.',
        'hint': '1. If AK=BK=AB (or any three equal distances between three points), the triangle '
                'formed is equilateral — identify all such triples in the problem. 2. The presence '
                'of multiple equilateral triangles suggests that the 60° angles structure the '
                'configuration: place the coordinate system to align these triangles comfortably. '
                '3. Calculate the positions of all points explicitly in coordinates, using that '
                'the third vertex of an equilateral constructed on AB is (midpoint(AB) ± '
                '(√3/2)·perpendicular). 4. Area of \u200b\u200ba compound region = Area(large '
                'triangle) - Area(equilateral sub-triangles) ± adjustments. 5. Use the '
                'relationships between the sides of the base triangle (eg from BC and ∠A=90°, '
                'AB²+AC²=BC²) to determine all dimensions.',
        'id': 'gen_equilateral_triangle_hidden_in_distances'},
    {   'description': 'Rational or polynomial functions that have a minimum at exactly two '
                     'points—determine the corresponding parameters.',
        'hint': '1. A function has a minimum at exactly two points if: (a) it has a flat local '
                "minimum point (triple root in f'), or (b) it has two distinct local minima of the "
                "same value ('W' shape). 2. Rewrite the function in a convenient form: group the "
                'factors, look for symmetric substitutions (eg: t = x + c/x for functions with the '
                "structure f(x)=g(x+k/x)). 3. Calculate f'(x) and determine the conditions for "
                "which f'=0 has the desired structure (multiple roots, or equality of values "
                "\u200b\u200bin two minima). 4. The condition 'two minima of the same value' leads "
                "to a system: f(x₁)=f(x₂), f'(x₁)=0, f'(x₂)=0 — eliminate x₁, x₂ to get equation "
                'in parameter k. 5. The sum of the k values \u200b\u200bresults from the '
                'coefficients of the equation in k (Life).',
        'id': 'gen_rational_function_double_minimum'},
    {   'description': 'Properties of the modulus of complex numbers, |z₁·z₂| = |z₁|·|z₂|.',
        'hint': 'ATTENTION: |z₁·z₂| = |z₁|·|z₂| and |z₁/z₂| = |z₁|/|z₂|. ATTENTION: |z₁+z₂| ≤ '
                '|z₁|+|z₂| (the triangle inequality for complexes). It is NOT true that |z₁+z₂| = '
                '|z₁|+|z₂| in general!',
        'id': 'proprietati_modul_complex'},
    {   'description': 'Calculation of the Euler totient function for products of prime numbers, '
                     'φ(p₁^a₁ · p₂^a₂ ...).',
        'hint': 'ATTENTION: φ(n) = n · ∏(1 - 1/p) for all p primes that divide n. Example: φ(12) = '
                'φ(2²·3) = 12·(1-1/2)·(1-1/3) = 12·1/2·2/3 = 4. If n = p (prime), φ(p) = p-1. φ is '
                'multiplicative only for coprime numbers!',
        'id': 'formula_euler_totient'},
    {   'description': 'Cayley-Hamilton theorem, the characteristic polynomial of a matrix, A '
                     'satisfies its own characteristic equation, p(A) = 0.',
        'hint': 'CAUTION: DO NOT directly substitute the matrix A in the determinant formula '
                'det(λI - A) = 0 instead of λ — this is a fatal error (direct scalar substitution '
                'error). The coefficients of the characteristic polynomial must be calculated '
                'explicitly, and A is substituted into the EXPANDED form of the polynomial, the '
                'free term c₀ becoming c₀·I. Reducing powers of A to linear combinations of lower '
                'powers is done ONLY after this correct substitution.',
        'id': 'teorema_cayley_hamilton'},
    {   'description': 'Locating eigenvalues, Gershgorin circles, spectrum of a matrix, estimation '
                     'of eigenvalues \u200b\u200bwithout direct calculation.',
        'hint': 'CAUTION: The Gershgorin theorem guarantees that ALL eigenvalues \u200b\u200blie '
                'in the UNION of circles, NOT that each circle contains exactly one eigenvalue — a '
                'circle can be completely empty or contain more than one. If the origin (0) is '
                'contained within any circle, the matrix is \u200b\u200bNOT guaranteed to be '
                'invertible by this criterion. The conclusion regarding the number of eigenvalues '
                '\u200b\u200bin an ISOLATED group of circles requires additional topological '
                'analysis (continuous deformation).',
        'id': 'cercurile_gershgorin'},
    {   'description': 'Concurrence of triangles, collinearity of points on the sides of a triangle, '
                     "Ceva's theorem, Menelaus' theorem, ratios of segments.",
        'hint': "CAUTION: Menelaus' Theorem REQUIRES the use of ORIENTED (signed) lengths. If a "
                'point is on the side extension outside the triangle, its ratio is NEGATIVE. '
                "Ignoring the sign leads to false conclusions of collinearity. In Ceva's Theorem, "
                'the product equal to +1 can also indicate PARALLEL lines (infinitely concurrent '
                'in projective geometry), not just affine concurrent — treat the case of parallel '
                'lines separately!',
        'id': 'teorema_ceva_menelaus'},
    {   'description': "Length of a hypotenuse in a triangle, Stewart's Theorem, relationship "
                     'between the hypotenuse and the sides of the triangle, d²a + mna = b²m + c²n.',
        'hint': 'CAUTION: Products associate segments with NON-ADJACENT sides — b²m and c²n, where '
                'm is the segment on side a adjacent to vertex B, and n is the segment adjacent to '
                'C. Reversing the association b↔c produces completely wrong results! If the point '
                'is on the EXTENSION of the side (outside the triangle), one of the segments m or '
                'n becomes negative (oriented length), changing the equation. For bisectors, '
                'combine with the Bisector Theorem (b/c = n/m).',
        'id': 'teorema_stewart'},
    {   'description': "Inscribed quadrilateral, Ptolemy's Theorem, AC·BD = AB·CD + BC·AD, "
                     'relationship between diagonals and sides.',
        'hint': 'ATTENTION: The Ptolemaic equality (AC·BD = AB·CD + BC·AD) is ONLY valid for '
                'INSCRIBIBLE (cyclic) quadrilaterals. For a general quadrilateral, the '
                "relationship becomes INEQUALITY (Ptolemy's Inequality): AC·BD ≤ AB·CD + BC·AD. "
                'ALWAYS check that the 4 points are concyclic before applying equality! General '
                'quadrilateral confusion vs. writable is the main source of errors.',
        'id': 'teorema_ptolemeu'},
    {   'description': "Area of \u200b\u200ban inscribed quadrilateral, Brahmagupta's Formula, K = "
                     'sqrt((s-a)(s-b)(s-c)(s-d)), semiperimeter.',
        'hint': 'ATTENTION: The Brahmagupta formula K = √[(s-a)(s-b)(s-c)(s-d)] is ONLY valid for '
                "INSCRIBABLE (cyclic) quadrilaterals. For a general quadrilateral, Bretschneider's "
                'Formula should be used: K = √[(s-a)(s-b)(s-c)(s-d) - abcd·cos²(θ)], where θ is '
                'half the sum of the opposite angles. Applying Brahmagupta to non-cyclic '
                'quadrilaterals OVERESTIMATES the area (implicitly assumes θ=90°). Note: The '
                'writable configuration maximizes the area for fixed sides.',
        'id': 'formula_brahmagupta'},
    {   'description': "Area of \u200b\u200ba polygon with vertices on full grid nodes, Pick's "
                     'Theorem, A = i + b/2 - 1, interior and boundary points.',
        'hint': 'ATTENTION: Parameter b (boundary points) is NOT calculated by counting vertices '
                'only! On each segment between the vertices (x₁,y₁)-(x₂,y₂) there are GCD(|x₂-x₁|, '
                '|y₂-y₁|) points on the boundary (excluding one end). Omitting the GCD algorithm '
                'massively underestimates b. Also, the formula A = i + b/2 - 1 is INVALID for '
                'polygons with self-intersections or interior HOLES — in those cases, the constant '
                '-1 must be replaced by -χ/2 (the Euler characteristic of the shape).',
        'id': 'teorema_pick'},
    {   'description': "Euler's right, collinearity of orthocenter H, center of gravity G and "
                     'circumcenter O, Circle of 9 points, radius R/2.',
        'hint': "CAUTION: In an EQUILATERAL triangle, the points H, G, and O coincide—Euler's line "
                'becomes undefined (degenerates to a point). The Center of the 9 point Circle does '
                "NOT coincide with the center of gravity G, but is on Euler's Right in the middle "
                'of the HO segment. The radius of the circle of 9 points is EXACTLY R/2 (half of '
                'the circumradius R). Distance relationship: HG = 2·GO (G divides HO in the ratio '
                '2:1).',
        'id': 'dreapta_euler_cercul_9_puncte'},
    {   'description': 'Projective geometry, perspective of two triangles from a point or line, '
                     'Desargues configuration, perspectivist point, perspectrix.',
        'hint': "ATTENTION: Desargues' theorem is NOT valid in any 2D geometry! It fails in "
                'Non-Desarguesian plans (ex: Moulton Plan). The coexistence of standard incidence '
                'axioms does not guarantee Desargues. In the real plane, the coplanar 2D proof '
                "requires additional axioms — the most elegant proof 'escapes' to 3D (raises the "
                'triangles in space, applies the intersection of the planes, then projects back). '
                'The theorem is the necessary condition to be able to construct a coherent '
                'algebraic coordinate system.',
        'id': 'teorema_desargues'},
    {   'description': 'Chinese Remainder Theorem, system of simultaneous congruences, x ≡ aᵢ (mod '
                     'nᵢ), unique solution modulo N.',
        'hint': 'CAUTION: TCR guarantees the existence and uniqueness of the solution ONLY if the '
                'nᵢ modules are PAIRWISE COPRIME (GCD(nᵢ, nⱼ) = 1 for any pair). If GCD > 1, the '
                'system may be incompatible or the solution is no longer unique modulo the product '
                "N, but modulo LCM. The efficient solution is calculated by Extended Euclid's "
                'Algorithm (Bézout coefficients), reducing the complexity from O(N) to O(log N). '
                'Do not iterate raw through all values \u200b\u200bfrom 1 to N!',
        'id': 'teorema_chinezeasca_resturilor'},
    {   'description': 'LTE Lemma (Lifting The Exponent), p-ie evaluation of xⁿ - yⁿ or xⁿ + yⁿ, '
                     'vₚ(xⁿ - yⁿ) = vₚ(x-y) + vₚ(n).',
        'hint': 'ATTENTION: The LTE lemma has DIFFERENT forms for odd p and p=2! For ODD p: if '
                'p∤x, p∤y and p|(x-y), then vₚ(xⁿ-yⁿ) = vₚ(x-y) + vₚ(n). For p=2 with even n: the '
                'formula becomes v₂(xⁿ-yⁿ) = v₂(x-y) + v₂(x+y) + v₂(n) - 1 (add v₂(x+y) and '
                'subtract 1!). The lemma is INVALIDATED if x or y is a multiple of p. Do not apply '
                'the formula for p=2 identical to that for odd p — the difference produces serious '
                'errors in Olympiads.',
        'id': 'lte_lifting_the_exponent'},
    {   'description': 'Irreducibility of a polynomial with integer coefficients over Q, '
                     "Eisenstein's Criterion, existence of a prime number p with conditions on the "
                     'coefficients.',
        'hint': 'ATTENTION: The Eisenstein Criterion is a SUFFICIENT condition, not a necessary '
                'one! If a polynomial fails the criterion, it does NOT mean that it is '
                'reducible—it can be irreducible without any prime satisfying the conditions. '
                "Solution: apply the 'translation trick' — if f(x) fails, test f(x+a) for "
                'a=1,-1,2, etc. Irreducibility is translation invariant, and the new form could '
                'lend itself to Eisenstein. Classic example: the cyclomic polynomial Φₚ(x) '
                "requires the evaluation of Φₚ(x+1) by Newton's binomial.",
        'id': 'criteriul_eisenstein'},
    {   'description': "Newton's Sums (Newton Identities), Sₖ = r₁ᵏ + r₂ᵏ + ... + rₙᵏ, the sum of "
                     'the powers of the roots of a polynomial without calculating the roots.',
        'hint': 'CAUTION: When calculating Sₙ for n greater than the degree of the polynomial, the '
                'recurrence formula requires ARTIFICIAL ZERO EXTENDING of the coefficients '
                '(coefficients of degree higher than the degree of the polynomial are treated as '
                '0). Omitting this extension produces index errors. Also, the method of estimating '
                'the dominant root by the Sₖ/Sₖ₋₁ limit ONLY works if there is only one true '
                'dominant root. Pairs of conjugate complex roots of the same modulus produce '
                'divergent ratio oscillations, invalidating the method.',
        'id': 'sumele_newton_radacini'},
    {   'description': 'Differentiation under the sign of the integral, Leibniz Rule, derivative of '
                     'the parametric integral with variable limits.',
        'hint': "ATTENTION: The full formula is d/dx[∫ₐ₍ₓ₎^b₍ₓ₎ f(x,t)dt] = f(x,b(x))·b'(x) - "
                "f(x,a(x))·a'(x) + ∫ₐ^b ∂f/∂x dt. Don't just throw the derivative under the "
                'integral ignoring the first two boundary terms — this is ONLY valid if the '
                'boundaries a and b are constant with respect to x! At improper integrals '
                '(infinite limits), the derivative-integral order exchange requires the UNIFORM '
                'CONVERGENCE check (the Weierstrass M-test or the Lebesgue Dominated Convergence '
                'Theorem) — without this, the result can be completely wrong.',
        'id': 'regula_leibniz_diferentiere_integrala'},
    {   'description': 'Newton-Raphson method of tangents, finding numerical roots of equations, '
                     "xₙ₊₁ = xₙ - f(xₙ)/f'(xₙ).",
        'hint': 'CAUTION: The Newton-Raphson method has two major pitfalls: (1) DIVISION BY ZERO — '
                "if f'(xₙ) = 0 at any iterative step (extreme point or horizontal tangent "
                'inflection), the formula becomes undefined and the iteration diverges; (2) WRONG '
                "STARTING POINT — if x₀ is chosen outside the 'basin of convergence' of the "
                'desired root, the iteration may oscillate (x₁→x₂→x₁→...) or converge to a root '
                'other than the desired one. Quadratic convergence (doubling exact decimals per '
                'step) is guaranteed ONLY in the neighborhood of the root.',
        'id': 'metoda_newton_raphson'},
    {   'description': "Stirling's approximation for large factorials, n! ≈ √(2πn)·(n/e)ⁿ, O(n log "
                     'n) asymptotic analysis.',
        'hint': 'CAUTION: The Stirling correction series (terms added for extra accuracy) is an '
                'ASYMPTOTIC DIVERGENT series — adding too many correction terms DEGRADES accuracy '
                'instead of improving it! There is an optimal number of terms (at which the error '
                'is minimal), after which the error GROWS exponentially. At small values '
                '\u200b\u200b(n < 10), the basic formula has significant errors. Useful limits: '
                '√(2πn)·(n/e)ⁿ ≤ n! ≤ e·n^(n+1/2)·e^(-n).',
        'id': 'aproximarea_stirling'},
    {   'description': 'Central Limit Theorem (CLT), distribution of the sample mean, convergence to '
                     'normal distribution, i.i.d. variables.',
        'hint': 'CAUTION: The Central Limit Theorem assumes FINITE VARIANCE of the original '
                "population. For 'heavy-tailed' distributions (ex: Cauchy distribution, with "
                'infinite variance and incalculable mean), CLT does NOT apply, no matter how large '
                'the sample is! CLT also requires INDEPENDENT variables—correlated/dependent '
                "samples can produce non-normal distributions. Bernoulli's inequality (1+x)^r ≥ "
                '1+rx applies ONLY for r≥1 and x≥-1; expanding to negative rational r or x<-1 '
                'produces errors.',
        'id': 'teorema_limitei_centrale'},
    {   'description': "Jensen's inequality, φ(E[X]) ≤ E[φ(X)] for convex functions, the expected "
                     'value of a nonlinear transformation.',
        'hint': "CAUTION: Jensen's inequality (φ(E[X]) ≤ E[φ(X)]) holds ONLY if φ is CONVEX (φ'' ≥ "
                "0). For CONCAVE functions (φ'' ≤ 0), the inequality IS INVERTED: φ(E[X]) ≥ "
                'E[φ(X)]. Equality holds ONLY if φ is linear OR if X is constant (zero variance). '
                "Common Modeling Flaw ('Flaw of Averages'): Inserting the average value of the "
                'input into a non-linear function does NOT produce the average value of the output '
                '— Jensen guarantees that it will produce a systematically BIEVATED estimate.',
        'id': 'inegalitatea_jensen'},
    {   'description': 'Roots of unity of order n, zⁿ = 1, complex roots, regular polygons on the '
                     "unit circle, De Moivre's formula.",
        'hint': 'ATTENTION: The equation zⁿ = 1 has EXACTLY n distinct complex solutions: ωₖ = '
                'cos(2kπ/n) + i·sin(2kπ/n) for k=0,1,...,n-1. The SUM of all unit roots of order n '
                'is ZERO (for n≥2). The PRODUCT of all the roots is (-1)^(n+1). On finite fields '
                'of characteristic p, if n is a multiple of p, the formula degenerates — there are '
                'no more n distinct roots! Not to be confused with the roots of zⁿ = a (with a≠1), '
                'which have mode r^(1/n), not 1.',
        'id': 'radacinile_unitatii'},
    {   'description': 'Modulo n congruences, modulo operator, a ≡ b (mod n), equivalence classes, '
                     'modular arithmetic.',
        'hint': 'CAUTION: There is a critical difference between the MATHEMATICAL congruence (a ≡ '
                'b mod n — equivalence class, infinite representatives) and the INFORMATICS '
                'operator (a % b — returns ONE remainder). In some programming languages, a % b '
                'for a NEGATIVE returns a NEGATIVE result (ex: -7 % 3 = -1 in C/C++), violating '
                'the mathematical definition that requires 0 ≤ r < n. The logical reverse is a '
                'trap: a ≡ r (mod n) does NOT guarantee that a%n = r computationally! When '
                "dividing by congruences, don't divide directly — multiply by the MODULAR INVERSE "
                '(which exists ONLY if GCD(a,n)=1).',
        'id': 'aritmetica_modulo_congruente'},
    {   'description': 'Fundamental Theorem of Arithmetic, unique factorization into prime factors, '
                     'decomposition of any integer n>1.',
        'hint': 'CAUTION: The number 1 is NOT prime — including it in the set of primes would '
                'destroy the uniqueness of the factorization (any number would have infinitely '
                'many factorizations: n = 1·n = 1²·n = ...). Factoring is unique ONLY in uniquely '
                'factoring (UFD) rings. In more general rings (ex: Z[√-5]), uniqueness may fail: 6 '
                '= 2·3 = (1+√-5)(1-√-5), both factorizations into irreducible elements. A prime '
                'number p with the property that p|ab implies p|a OR p|b is a PRIME element '
                '(different concept from irreducible in general rings).',
        'id': 'factorizarea_unica_numere_prime'},
    {   'description': "Wilson's primality criterion, (p-1)! ≡ -1 (mod p), necessary and sufficient "
                     'condition for p prime.',
        'hint': "CAUTION: Although Wilson's Theorem provides a NECESSARY AND SUFFICIENT criterion "
                'of primality — p is prime IF AND ONLY IF (p-1)! ≡ -1 (mod p) — it is completely '
                'USELESS in practice for testing the primality of large numbers. The calculation '
                '(p-1)! has O(p·log²p) complexity, exponential to the number of digits, exceeding '
                'any computational resource for cryptographic primes (hundreds of bits). It is '
                'ONLY used in theoretical proofs (Galois fields, multiplicative inverse). Not to '
                "be confused with Fermat's Little Theorem (aᵖ⁻¹ ≡ 1 mod p), which is weaker but "
                'computationally feasible.',
        'id': 'teorema_wilson_primalitate'}]