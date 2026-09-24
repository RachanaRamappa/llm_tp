begin_version
3
end_version
begin_metric
0
end_metric
15
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
2
Atom clear(b1)
NegatedAtom clear(b1)
end_variable
begin_variable
var7
-1
2
Atom clear(b2)
NegatedAtom clear(b2)
end_variable
begin_variable
var8
-1
2
Atom clear(b3)
NegatedAtom clear(b3)
end_variable
begin_variable
var9
-1
2
Atom clear(b4)
NegatedAtom clear(b4)
end_variable
begin_variable
var10
-1
2
Atom arm-empty()
NegatedAtom arm-empty()
end_variable
begin_variable
var11
-1
10
Atom holding(b1)
Atom on(b1, b2)
Atom on(b1, b3)
Atom on(b1, b4)
Atom on-table(b1, t1)
Atom on-table(b1, t2)
Atom on-table(b1, t3)
Atom on-table(b1, t4)
Atom on-table(b1, t5)
Atom on-table(b1, t6)
end_variable
begin_variable
var12
-1
10
Atom holding(b2)
Atom on(b2, b1)
Atom on(b2, b3)
Atom on(b2, b4)
Atom on-table(b2, t1)
Atom on-table(b2, t2)
Atom on-table(b2, t3)
Atom on-table(b2, t4)
Atom on-table(b2, t5)
Atom on-table(b2, t6)
end_variable
begin_variable
var13
-1
10
Atom holding(b3)
Atom on(b3, b1)
Atom on(b3, b2)
Atom on(b3, b4)
Atom on-table(b3, t1)
Atom on-table(b3, t2)
Atom on-table(b3, t3)
Atom on-table(b3, t4)
Atom on-table(b3, t5)
Atom on-table(b3, t6)
end_variable
begin_variable
var14
-1
10
Atom holding(b4)
Atom on(b4, b1)
Atom on(b4, b2)
Atom on(b4, b3)
Atom on-table(b4, t1)
Atom on-table(b4, t2)
Atom on-table(b4, t3)
Atom on-table(b4, t4)
Atom on-table(b4, t5)
Atom on-table(b4, t6)
end_variable
11
begin_mutex_group
5
10 0
11 0
12 0
13 0
14 0
end_mutex_group
begin_mutex_group
5
6 0
11 0
12 1
13 1
14 1
end_mutex_group
begin_mutex_group
5
7 0
11 1
12 0
13 2
14 2
end_mutex_group
begin_mutex_group
5
8 0
11 2
12 2
13 0
14 3
end_mutex_group
begin_mutex_group
5
9 0
11 3
12 3
13 3
14 0
end_mutex_group
begin_mutex_group
5
0 0
11 4
12 4
13 4
14 4
end_mutex_group
begin_mutex_group
5
1 0
11 5
12 5
13 5
14 5
end_mutex_group
begin_mutex_group
5
2 0
11 6
12 6
13 6
14 6
end_mutex_group
begin_mutex_group
5
3 0
11 7
12 7
13 7
14 7
end_mutex_group
begin_mutex_group
5
4 0
11 8
12 8
13 8
14 8
end_mutex_group
begin_mutex_group
5
5 0
11 9
12 9
13 9
14 9
end_mutex_group
begin_state
0
0
1
1
0
0
0
1
0
1
0
1
7
3
6
end_state
begin_goal
4
11 7
12 1
13 6
14 3
end_goal
72
begin_operator
pickup b1 t1
0
4
0 10 0 1
0 6 0 1
0 0 -1 0
0 11 4 0
1
end_operator
begin_operator
pickup b1 t2
0
4
0 10 0 1
0 6 0 1
0 1 -1 0
0 11 5 0
1
end_operator
begin_operator
pickup b1 t3
0
4
0 10 0 1
0 6 0 1
0 2 -1 0
0 11 6 0
1
end_operator
begin_operator
pickup b1 t4
0
4
0 10 0 1
0 6 0 1
0 3 -1 0
0 11 7 0
1
end_operator
begin_operator
pickup b1 t5
0
4
0 10 0 1
0 6 0 1
0 4 -1 0
0 11 8 0
1
end_operator
begin_operator
pickup b1 t6
0
4
0 10 0 1
0 6 0 1
0 5 -1 0
0 11 9 0
1
end_operator
begin_operator
pickup b2 t1
0
4
0 10 0 1
0 7 0 1
0 0 -1 0
0 12 4 0
1
end_operator
begin_operator
pickup b2 t2
0
4
0 10 0 1
0 7 0 1
0 1 -1 0
0 12 5 0
1
end_operator
begin_operator
pickup b2 t3
0
4
0 10 0 1
0 7 0 1
0 2 -1 0
0 12 6 0
1
end_operator
begin_operator
pickup b2 t4
0
4
0 10 0 1
0 7 0 1
0 3 -1 0
0 12 7 0
1
end_operator
begin_operator
pickup b2 t5
0
4
0 10 0 1
0 7 0 1
0 4 -1 0
0 12 8 0
1
end_operator
begin_operator
pickup b2 t6
0
4
0 10 0 1
0 7 0 1
0 5 -1 0
0 12 9 0
1
end_operator
begin_operator
pickup b3 t1
0
4
0 10 0 1
0 8 0 1
0 0 -1 0
0 13 4 0
1
end_operator
begin_operator
pickup b3 t2
0
4
0 10 0 1
0 8 0 1
0 1 -1 0
0 13 5 0
1
end_operator
begin_operator
pickup b3 t3
0
4
0 10 0 1
0 8 0 1
0 2 -1 0
0 13 6 0
1
end_operator
begin_operator
pickup b3 t4
0
4
0 10 0 1
0 8 0 1
0 3 -1 0
0 13 7 0
1
end_operator
begin_operator
pickup b3 t5
0
4
0 10 0 1
0 8 0 1
0 4 -1 0
0 13 8 0
1
end_operator
begin_operator
pickup b3 t6
0
4
0 10 0 1
0 8 0 1
0 5 -1 0
0 13 9 0
1
end_operator
begin_operator
pickup b4 t1
0
4
0 10 0 1
0 9 0 1
0 0 -1 0
0 14 4 0
1
end_operator
begin_operator
pickup b4 t2
0
4
0 10 0 1
0 9 0 1
0 1 -1 0
0 14 5 0
1
end_operator
begin_operator
pickup b4 t3
0
4
0 10 0 1
0 9 0 1
0 2 -1 0
0 14 6 0
1
end_operator
begin_operator
pickup b4 t4
0
4
0 10 0 1
0 9 0 1
0 3 -1 0
0 14 7 0
1
end_operator
begin_operator
pickup b4 t5
0
4
0 10 0 1
0 9 0 1
0 4 -1 0
0 14 8 0
1
end_operator
begin_operator
pickup b4 t6
0
4
0 10 0 1
0 9 0 1
0 5 -1 0
0 14 9 0
1
end_operator
begin_operator
putdown b1 t1
0
4
0 10 -1 0
0 6 -1 0
0 0 0 1
0 11 0 4
1
end_operator
begin_operator
putdown b1 t2
0
4
0 10 -1 0
0 6 -1 0
0 1 0 1
0 11 0 5
1
end_operator
begin_operator
putdown b1 t3
0
4
0 10 -1 0
0 6 -1 0
0 2 0 1
0 11 0 6
1
end_operator
begin_operator
putdown b1 t4
0
4
0 10 -1 0
0 6 -1 0
0 3 0 1
0 11 0 7
1
end_operator
begin_operator
putdown b1 t5
0
4
0 10 -1 0
0 6 -1 0
0 4 0 1
0 11 0 8
1
end_operator
begin_operator
putdown b1 t6
0
4
0 10 -1 0
0 6 -1 0
0 5 0 1
0 11 0 9
1
end_operator
begin_operator
putdown b2 t1
0
4
0 10 -1 0
0 7 -1 0
0 0 0 1
0 12 0 4
1
end_operator
begin_operator
putdown b2 t2
0
4
0 10 -1 0
0 7 -1 0
0 1 0 1
0 12 0 5
1
end_operator
begin_operator
putdown b2 t3
0
4
0 10 -1 0
0 7 -1 0
0 2 0 1
0 12 0 6
1
end_operator
begin_operator
putdown b2 t4
0
4
0 10 -1 0
0 7 -1 0
0 3 0 1
0 12 0 7
1
end_operator
begin_operator
putdown b2 t5
0
4
0 10 -1 0
0 7 -1 0
0 4 0 1
0 12 0 8
1
end_operator
begin_operator
putdown b2 t6
0
4
0 10 -1 0
0 7 -1 0
0 5 0 1
0 12 0 9
1
end_operator
begin_operator
putdown b3 t1
0
4
0 10 -1 0
0 8 -1 0
0 0 0 1
0 13 0 4
1
end_operator
begin_operator
putdown b3 t2
0
4
0 10 -1 0
0 8 -1 0
0 1 0 1
0 13 0 5
1
end_operator
begin_operator
putdown b3 t3
0
4
0 10 -1 0
0 8 -1 0
0 2 0 1
0 13 0 6
1
end_operator
begin_operator
putdown b3 t4
0
4
0 10 -1 0
0 8 -1 0
0 3 0 1
0 13 0 7
1
end_operator
begin_operator
putdown b3 t5
0
4
0 10 -1 0
0 8 -1 0
0 4 0 1
0 13 0 8
1
end_operator
begin_operator
putdown b3 t6
0
4
0 10 -1 0
0 8 -1 0
0 5 0 1
0 13 0 9
1
end_operator
begin_operator
putdown b4 t1
0
4
0 10 -1 0
0 9 -1 0
0 0 0 1
0 14 0 4
1
end_operator
begin_operator
putdown b4 t2
0
4
0 10 -1 0
0 9 -1 0
0 1 0 1
0 14 0 5
1
end_operator
begin_operator
putdown b4 t3
0
4
0 10 -1 0
0 9 -1 0
0 2 0 1
0 14 0 6
1
end_operator
begin_operator
putdown b4 t4
0
4
0 10 -1 0
0 9 -1 0
0 3 0 1
0 14 0 7
1
end_operator
begin_operator
putdown b4 t5
0
4
0 10 -1 0
0 9 -1 0
0 4 0 1
0 14 0 8
1
end_operator
begin_operator
putdown b4 t6
0
4
0 10 -1 0
0 9 -1 0
0 5 0 1
0 14 0 9
1
end_operator
begin_operator
stack b1 b2
0
4
0 10 -1 0
0 6 -1 0
0 7 0 1
0 11 0 1
1
end_operator
begin_operator
stack b1 b3
0
4
0 10 -1 0
0 6 -1 0
0 8 0 1
0 11 0 2
1
end_operator
begin_operator
stack b1 b4
0
4
0 10 -1 0
0 6 -1 0
0 9 0 1
0 11 0 3
1
end_operator
begin_operator
stack b2 b1
0
4
0 10 -1 0
0 6 0 1
0 7 -1 0
0 12 0 1
1
end_operator
begin_operator
stack b2 b3
0
4
0 10 -1 0
0 7 -1 0
0 8 0 1
0 12 0 2
1
end_operator
begin_operator
stack b2 b4
0
4
0 10 -1 0
0 7 -1 0
0 9 0 1
0 12 0 3
1
end_operator
begin_operator
stack b3 b1
0
4
0 10 -1 0
0 6 0 1
0 8 -1 0
0 13 0 1
1
end_operator
begin_operator
stack b3 b2
0
4
0 10 -1 0
0 7 0 1
0 8 -1 0
0 13 0 2
1
end_operator
begin_operator
stack b3 b4
0
4
0 10 -1 0
0 8 -1 0
0 9 0 1
0 13 0 3
1
end_operator
begin_operator
stack b4 b1
0
4
0 10 -1 0
0 6 0 1
0 9 -1 0
0 14 0 1
1
end_operator
begin_operator
stack b4 b2
0
4
0 10 -1 0
0 7 0 1
0 9 -1 0
0 14 0 2
1
end_operator
begin_operator
stack b4 b3
0
4
0 10 -1 0
0 8 0 1
0 9 -1 0
0 14 0 3
1
end_operator
begin_operator
unstack b1 b2
0
4
0 10 0 1
0 6 0 1
0 7 -1 0
0 11 1 0
1
end_operator
begin_operator
unstack b1 b3
0
4
0 10 0 1
0 6 0 1
0 8 -1 0
0 11 2 0
1
end_operator
begin_operator
unstack b1 b4
0
4
0 10 0 1
0 6 0 1
0 9 -1 0
0 11 3 0
1
end_operator
begin_operator
unstack b2 b1
0
4
0 10 0 1
0 6 -1 0
0 7 0 1
0 12 1 0
1
end_operator
begin_operator
unstack b2 b3
0
4
0 10 0 1
0 7 0 1
0 8 -1 0
0 12 2 0
1
end_operator
begin_operator
unstack b2 b4
0
4
0 10 0 1
0 7 0 1
0 9 -1 0
0 12 3 0
1
end_operator
begin_operator
unstack b3 b1
0
4
0 10 0 1
0 6 -1 0
0 8 0 1
0 13 1 0
1
end_operator
begin_operator
unstack b3 b2
0
4
0 10 0 1
0 7 -1 0
0 8 0 1
0 13 2 0
1
end_operator
begin_operator
unstack b3 b4
0
4
0 10 0 1
0 8 0 1
0 9 -1 0
0 13 3 0
1
end_operator
begin_operator
unstack b4 b1
0
4
0 10 0 1
0 6 -1 0
0 9 0 1
0 14 1 0
1
end_operator
begin_operator
unstack b4 b2
0
4
0 10 0 1
0 7 -1 0
0 9 0 1
0 14 2 0
1
end_operator
begin_operator
unstack b4 b3
0
4
0 10 0 1
0 8 -1 0
0 9 0 1
0 14 3 0
1
end_operator
0
