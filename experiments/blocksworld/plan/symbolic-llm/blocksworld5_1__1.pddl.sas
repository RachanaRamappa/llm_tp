begin_version
3
end_version
begin_metric
0
end_metric
17
begin_variable
var0
-1
2
Atom clear-table(t1)
NegatedAtom clear-table(t1)
end_variable
begin_variable
var1
-1
2
Atom clear-table(t2)
NegatedAtom clear-table(t2)
end_variable
begin_variable
var2
-1
2
Atom clear-table(t3)
NegatedAtom clear-table(t3)
end_variable
begin_variable
var3
-1
2
Atom clear-table(t4)
NegatedAtom clear-table(t4)
end_variable
begin_variable
var4
-1
2
Atom clear-table(t5)
NegatedAtom clear-table(t5)
end_variable
begin_variable
var5
-1
2
Atom clear-table(t6)
NegatedAtom clear-table(t6)
end_variable
begin_variable
var6
-1
11
Atom holding(b2)
Atom on(b2, b1)
Atom on(b2, b3)
Atom on(b2, b4)
Atom on(b2, b5)
Atom on-table(b2, t1)
Atom on-table(b2, t2)
Atom on-table(b2, t3)
Atom on-table(b2, t4)
Atom on-table(b2, t5)
Atom on-table(b2, t6)
end_variable
begin_variable
var7
-1
11
Atom holding(b3)
Atom on(b3, b1)
Atom on(b3, b2)
Atom on(b3, b4)
Atom on(b3, b5)
Atom on-table(b3, t1)
Atom on-table(b3, t2)
Atom on-table(b3, t3)
Atom on-table(b3, t4)
Atom on-table(b3, t5)
Atom on-table(b3, t6)
end_variable
begin_variable
var8
-1
11
Atom holding(b4)
Atom on(b4, b1)
Atom on(b4, b2)
Atom on(b4, b3)
Atom on(b4, b5)
Atom on-table(b4, t1)
Atom on-table(b4, t2)
Atom on-table(b4, t3)
Atom on-table(b4, t4)
Atom on-table(b4, t5)
Atom on-table(b4, t6)
end_variable
begin_variable
var9
-1
11
Atom holding(b5)
Atom on(b5, b1)
Atom on(b5, b2)
Atom on(b5, b3)
Atom on(b5, b4)
Atom on-table(b5, t1)
Atom on-table(b5, t2)
Atom on-table(b5, t3)
Atom on-table(b5, t4)
Atom on-table(b5, t5)
Atom on-table(b5, t6)
end_variable
begin_variable
var10
-1
2
Atom clear(b2)
NegatedAtom clear(b2)
end_variable
begin_variable
var11
-1
2
Atom clear(b3)
NegatedAtom clear(b3)
end_variable
begin_variable
var12
-1
2
Atom clear(b4)
NegatedAtom clear(b4)
end_variable
begin_variable
var13
-1
2
Atom clear(b5)
NegatedAtom clear(b5)
end_variable
begin_variable
var14
-1
2
Atom arm-empty()
NegatedAtom arm-empty()
end_variable
begin_variable
var15
-1
2
Atom clear(b1)
NegatedAtom clear(b1)
end_variable
begin_variable
var16
-1
11
Atom holding(b1)
Atom on(b1, b2)
Atom on(b1, b3)
Atom on(b1, b4)
Atom on(b1, b5)
Atom on-table(b1, t1)
Atom on-table(b1, t2)
Atom on-table(b1, t3)
Atom on-table(b1, t4)
Atom on-table(b1, t5)
Atom on-table(b1, t6)
end_variable
12
begin_mutex_group
6
14 0
16 0
6 0
7 0
8 0
9 0
end_mutex_group
begin_mutex_group
6
15 0
16 0
6 1
7 1
8 1
9 1
end_mutex_group
begin_mutex_group
6
10 0
16 1
6 0
7 2
8 2
9 2
end_mutex_group
begin_mutex_group
6
11 0
16 2
6 2
7 0
8 3
9 3
end_mutex_group
begin_mutex_group
6
12 0
16 3
6 3
7 3
8 0
9 4
end_mutex_group
begin_mutex_group
6
13 0
16 4
6 4
7 4
8 4
9 0
end_mutex_group
begin_mutex_group
6
0 0
16 5
6 5
7 5
8 5
9 5
end_mutex_group
begin_mutex_group
6
1 0
16 6
6 6
7 6
8 6
9 6
end_mutex_group
begin_mutex_group
6
2 0
16 7
6 7
7 7
8 7
9 7
end_mutex_group
begin_mutex_group
6
3 0
16 8
6 8
7 8
8 8
9 8
end_mutex_group
begin_mutex_group
6
4 0
16 9
6 9
7 9
8 9
9 9
end_mutex_group
begin_mutex_group
6
5 0
16 10
6 10
7 10
8 10
9 10
end_mutex_group
begin_state
1
1
0
0
0
1
6
3
4
10
0
0
1
1
0
0
5
end_state
begin_goal
1
16 9
end_goal
100
begin_operator
pickup b1 t1
0
4
0 14 0 1
0 15 0 1
0 0 -1 0
0 16 5 0
1
end_operator
begin_operator
pickup b1 t2
0
4
0 14 0 1
0 15 0 1
0 1 -1 0
0 16 6 0
1
end_operator
begin_operator
pickup b1 t3
0
4
0 14 0 1
0 15 0 1
0 2 -1 0
0 16 7 0
1
end_operator
begin_operator
pickup b1 t4
0
4
0 14 0 1
0 15 0 1
0 3 -1 0
0 16 8 0
1
end_operator
begin_operator
pickup b1 t5
0
4
0 14 0 1
0 15 0 1
0 4 -1 0
0 16 9 0
1
end_operator
begin_operator
pickup b1 t6
0
4
0 14 0 1
0 15 0 1
0 5 -1 0
0 16 10 0
1
end_operator
begin_operator
pickup b2 t1
0
4
0 14 0 1
0 10 0 1
0 0 -1 0
0 6 5 0
1
end_operator
begin_operator
pickup b2 t2
0
4
0 14 0 1
0 10 0 1
0 1 -1 0
0 6 6 0
1
end_operator
begin_operator
pickup b2 t3
0
4
0 14 0 1
0 10 0 1
0 2 -1 0
0 6 7 0
1
end_operator
begin_operator
pickup b2 t4
0
4
0 14 0 1
0 10 0 1
0 3 -1 0
0 6 8 0
1
end_operator
begin_operator
pickup b2 t5
0
4
0 14 0 1
0 10 0 1
0 4 -1 0
0 6 9 0
1
end_operator
begin_operator
pickup b2 t6
0
4
0 14 0 1
0 10 0 1
0 5 -1 0
0 6 10 0
1
end_operator
begin_operator
pickup b3 t1
0
4
0 14 0 1
0 11 0 1
0 0 -1 0
0 7 5 0
1
end_operator
begin_operator
pickup b3 t2
0
4
0 14 0 1
0 11 0 1
0 1 -1 0
0 7 6 0
1
end_operator
begin_operator
pickup b3 t3
0
4
0 14 0 1
0 11 0 1
0 2 -1 0
0 7 7 0
1
end_operator
begin_operator
pickup b3 t4
0
4
0 14 0 1
0 11 0 1
0 3 -1 0
0 7 8 0
1
end_operator
begin_operator
pickup b3 t5
0
4
0 14 0 1
0 11 0 1
0 4 -1 0
0 7 9 0
1
end_operator
begin_operator
pickup b3 t6
0
4
0 14 0 1
0 11 0 1
0 5 -1 0
0 7 10 0
1
end_operator
begin_operator
pickup b4 t1
0
4
0 14 0 1
0 12 0 1
0 0 -1 0
0 8 5 0
1
end_operator
begin_operator
pickup b4 t2
0
4
0 14 0 1
0 12 0 1
0 1 -1 0
0 8 6 0
1
end_operator
begin_operator
pickup b4 t3
0
4
0 14 0 1
0 12 0 1
0 2 -1 0
0 8 7 0
1
end_operator
begin_operator
pickup b4 t4
0
4
0 14 0 1
0 12 0 1
0 3 -1 0
0 8 8 0
1
end_operator
begin_operator
pickup b4 t5
0
4
0 14 0 1
0 12 0 1
0 4 -1 0
0 8 9 0
1
end_operator
begin_operator
pickup b4 t6
0
4
0 14 0 1
0 12 0 1
0 5 -1 0
0 8 10 0
1
end_operator
begin_operator
pickup b5 t1
0
4
0 14 0 1
0 13 0 1
0 0 -1 0
0 9 5 0
1
end_operator
begin_operator
pickup b5 t2
0
4
0 14 0 1
0 13 0 1
0 1 -1 0
0 9 6 0
1
end_operator
begin_operator
pickup b5 t3
0
4
0 14 0 1
0 13 0 1
0 2 -1 0
0 9 7 0
1
end_operator
begin_operator
pickup b5 t4
0
4
0 14 0 1
0 13 0 1
0 3 -1 0
0 9 8 0
1
end_operator
begin_operator
pickup b5 t5
0
4
0 14 0 1
0 13 0 1
0 4 -1 0
0 9 9 0
1
end_operator
begin_operator
pickup b5 t6
0
4
0 14 0 1
0 13 0 1
0 5 -1 0
0 9 10 0
1
end_operator
begin_operator
putdown b1 t1
0
4
0 14 -1 0
0 15 -1 0
0 0 0 1
0 16 0 5
1
end_operator
begin_operator
putdown b1 t2
0
4
0 14 -1 0
0 15 -1 0
0 1 0 1
0 16 0 6
1
end_operator
begin_operator
putdown b1 t3
0
4
0 14 -1 0
0 15 -1 0
0 2 0 1
0 16 0 7
1
end_operator
begin_operator
putdown b1 t4
0
4
0 14 -1 0
0 15 -1 0
0 3 0 1
0 16 0 8
1
end_operator
begin_operator
putdown b1 t5
0
4
0 14 -1 0
0 15 -1 0
0 4 0 1
0 16 0 9
1
end_operator
begin_operator
putdown b1 t6
0
4
0 14 -1 0
0 15 -1 0
0 5 0 1
0 16 0 10
1
end_operator
begin_operator
putdown b2 t1
0
4
0 14 -1 0
0 10 -1 0
0 0 0 1
0 6 0 5
1
end_operator
begin_operator
putdown b2 t2
0
4
0 14 -1 0
0 10 -1 0
0 1 0 1
0 6 0 6
1
end_operator
begin_operator
putdown b2 t3
0
4
0 14 -1 0
0 10 -1 0
0 2 0 1
0 6 0 7
1
end_operator
begin_operator
putdown b2 t4
0
4
0 14 -1 0
0 10 -1 0
0 3 0 1
0 6 0 8
1
end_operator
begin_operator
putdown b2 t5
0
4
0 14 -1 0
0 10 -1 0
0 4 0 1
0 6 0 9
1
end_operator
begin_operator
putdown b2 t6
0
4
0 14 -1 0
0 10 -1 0
0 5 0 1
0 6 0 10
1
end_operator
begin_operator
putdown b3 t1
0
4
0 14 -1 0
0 11 -1 0
0 0 0 1
0 7 0 5
1
end_operator
begin_operator
putdown b3 t2
0
4
0 14 -1 0
0 11 -1 0
0 1 0 1
0 7 0 6
1
end_operator
begin_operator
putdown b3 t3
0
4
0 14 -1 0
0 11 -1 0
0 2 0 1
0 7 0 7
1
end_operator
begin_operator
putdown b3 t4
0
4
0 14 -1 0
0 11 -1 0
0 3 0 1
0 7 0 8
1
end_operator
begin_operator
putdown b3 t5
0
4
0 14 -1 0
0 11 -1 0
0 4 0 1
0 7 0 9
1
end_operator
begin_operator
putdown b3 t6
0
4
0 14 -1 0
0 11 -1 0
0 5 0 1
0 7 0 10
1
end_operator
begin_operator
putdown b4 t1
0
4
0 14 -1 0
0 12 -1 0
0 0 0 1
0 8 0 5
1
end_operator
begin_operator
putdown b4 t2
0
4
0 14 -1 0
0 12 -1 0
0 1 0 1
0 8 0 6
1
end_operator
begin_operator
putdown b4 t3
0
4
0 14 -1 0
0 12 -1 0
0 2 0 1
0 8 0 7
1
end_operator
begin_operator
putdown b4 t4
0
4
0 14 -1 0
0 12 -1 0
0 3 0 1
0 8 0 8
1
end_operator
begin_operator
putdown b4 t5
0
4
0 14 -1 0
0 12 -1 0
0 4 0 1
0 8 0 9
1
end_operator
begin_operator
putdown b4 t6
0
4
0 14 -1 0
0 12 -1 0
0 5 0 1
0 8 0 10
1
end_operator
begin_operator
putdown b5 t1
0
4
0 14 -1 0
0 13 -1 0
0 0 0 1
0 9 0 5
1
end_operator
begin_operator
putdown b5 t2
0
4
0 14 -1 0
0 13 -1 0
0 1 0 1
0 9 0 6
1
end_operator
begin_operator
putdown b5 t3
0
4
0 14 -1 0
0 13 -1 0
0 2 0 1
0 9 0 7
1
end_operator
begin_operator
putdown b5 t4
0
4
0 14 -1 0
0 13 -1 0
0 3 0 1
0 9 0 8
1
end_operator
begin_operator
putdown b5 t5
0
4
0 14 -1 0
0 13 -1 0
0 4 0 1
0 9 0 9
1
end_operator
begin_operator
putdown b5 t6
0
4
0 14 -1 0
0 13 -1 0
0 5 0 1
0 9 0 10
1
end_operator
begin_operator
stack b1 b2
0
4
0 14 -1 0
0 15 -1 0
0 10 0 1
0 16 0 1
1
end_operator
begin_operator
stack b1 b3
0
4
0 14 -1 0
0 15 -1 0
0 11 0 1
0 16 0 2
1
end_operator
begin_operator
stack b1 b4
0
4
0 14 -1 0
0 15 -1 0
0 12 0 1
0 16 0 3
1
end_operator
begin_operator
stack b1 b5
0
4
0 14 -1 0
0 15 -1 0
0 13 0 1
0 16 0 4
1
end_operator
begin_operator
stack b2 b1
0
4
0 14 -1 0
0 15 0 1
0 10 -1 0
0 6 0 1
1
end_operator
begin_operator
stack b2 b3
0
4
0 14 -1 0
0 10 -1 0
0 11 0 1
0 6 0 2
1
end_operator
begin_operator
stack b2 b4
0
4
0 14 -1 0
0 10 -1 0
0 12 0 1
0 6 0 3
1
end_operator
begin_operator
stack b2 b5
0
4
0 14 -1 0
0 10 -1 0
0 13 0 1
0 6 0 4
1
end_operator
begin_operator
stack b3 b1
0
4
0 14 -1 0
0 15 0 1
0 11 -1 0
0 7 0 1
1
end_operator
begin_operator
stack b3 b2
0
4
0 14 -1 0
0 10 0 1
0 11 -1 0
0 7 0 2
1
end_operator
begin_operator
stack b3 b4
0
4
0 14 -1 0
0 11 -1 0
0 12 0 1
0 7 0 3
1
end_operator
begin_operator
stack b3 b5
0
4
0 14 -1 0
0 11 -1 0
0 13 0 1
0 7 0 4
1
end_operator
begin_operator
stack b4 b1
0
4
0 14 -1 0
0 15 0 1
0 12 -1 0
0 8 0 1
1
end_operator
begin_operator
stack b4 b2
0
4
0 14 -1 0
0 10 0 1
0 12 -1 0
0 8 0 2
1
end_operator
begin_operator
stack b4 b3
0
4
0 14 -1 0
0 11 0 1
0 12 -1 0
0 8 0 3
1
end_operator
begin_operator
stack b4 b5
0
4
0 14 -1 0
0 12 -1 0
0 13 0 1
0 8 0 4
1
end_operator
begin_operator
stack b5 b1
0
4
0 14 -1 0
0 15 0 1
0 13 -1 0
0 9 0 1
1
end_operator
begin_operator
stack b5 b2
0
4
0 14 -1 0
0 10 0 1
0 13 -1 0
0 9 0 2
1
end_operator
begin_operator
stack b5 b3
0
4
0 14 -1 0
0 11 0 1
0 13 -1 0
0 9 0 3
1
end_operator
begin_operator
stack b5 b4
0
4
0 14 -1 0
0 12 0 1
0 13 -1 0
0 9 0 4
1
end_operator
begin_operator
unstack b1 b2
0
4
0 14 0 1
0 15 0 1
0 10 -1 0
0 16 1 0
1
end_operator
begin_operator
unstack b1 b3
0
4
0 14 0 1
0 15 0 1
0 11 -1 0
0 16 2 0
1
end_operator
begin_operator
unstack b1 b4
0
4
0 14 0 1
0 15 0 1
0 12 -1 0
0 16 3 0
1
end_operator
begin_operator
unstack b1 b5
0
4
0 14 0 1
0 15 0 1
0 13 -1 0
0 16 4 0
1
end_operator
begin_operator
unstack b2 b1
0
4
0 14 0 1
0 15 -1 0
0 10 0 1
0 6 1 0
1
end_operator
begin_operator
unstack b2 b3
0
4
0 14 0 1
0 10 0 1
0 11 -1 0
0 6 2 0
1
end_operator
begin_operator
unstack b2 b4
0
4
0 14 0 1
0 10 0 1
0 12 -1 0
0 6 3 0
1
end_operator
begin_operator
unstack b2 b5
0
4
0 14 0 1
0 10 0 1
0 13 -1 0
0 6 4 0
1
end_operator
begin_operator
unstack b3 b1
0
4
0 14 0 1
0 15 -1 0
0 11 0 1
0 7 1 0
1
end_operator
begin_operator
unstack b3 b2
0
4
0 14 0 1
0 10 -1 0
0 11 0 1
0 7 2 0
1
end_operator
begin_operator
unstack b3 b4
0
4
0 14 0 1
0 11 0 1
0 12 -1 0
0 7 3 0
1
end_operator
begin_operator
unstack b3 b5
0
4
0 14 0 1
0 11 0 1
0 13 -1 0
0 7 4 0
1
end_operator
begin_operator
unstack b4 b1
0
4
0 14 0 1
0 15 -1 0
0 12 0 1
0 8 1 0
1
end_operator
begin_operator
unstack b4 b2
0
4
0 14 0 1
0 10 -1 0
0 12 0 1
0 8 2 0
1
end_operator
begin_operator
unstack b4 b3
0
4
0 14 0 1
0 11 -1 0
0 12 0 1
0 8 3 0
1
end_operator
begin_operator
unstack b4 b5
0
4
0 14 0 1
0 12 0 1
0 13 -1 0
0 8 4 0
1
end_operator
begin_operator
unstack b5 b1
0
4
0 14 0 1
0 15 -1 0
0 13 0 1
0 9 1 0
1
end_operator
begin_operator
unstack b5 b2
0
4
0 14 0 1
0 10 -1 0
0 13 0 1
0 9 2 0
1
end_operator
begin_operator
unstack b5 b3
0
4
0 14 0 1
0 11 -1 0
0 13 0 1
0 9 3 0
1
end_operator
begin_operator
unstack b5 b4
0
4
0 14 0 1
0 12 -1 0
0 13 0 1
0 9 4 0
1
end_operator
0
