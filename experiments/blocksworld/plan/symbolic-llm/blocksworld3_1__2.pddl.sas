begin_version
3
end_version
begin_metric
0
end_metric
13
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
9
Atom holding(b1)
Atom on(b1, b2)
Atom on(b1, b3)
Atom on-table(b1, t1)
Atom on-table(b1, t2)
Atom on-table(b1, t3)
Atom on-table(b1, t4)
Atom on-table(b1, t5)
Atom on-table(b1, t6)
end_variable
begin_variable
var7
-1
9
Atom holding(b2)
Atom on(b2, b1)
Atom on(b2, b3)
Atom on-table(b2, t1)
Atom on-table(b2, t2)
Atom on-table(b2, t3)
Atom on-table(b2, t4)
Atom on-table(b2, t5)
Atom on-table(b2, t6)
end_variable
begin_variable
var8
-1
2
Atom clear(b1)
NegatedAtom clear(b1)
end_variable
begin_variable
var9
-1
2
Atom clear(b2)
NegatedAtom clear(b2)
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
2
Atom clear(b3)
NegatedAtom clear(b3)
end_variable
begin_variable
var12
-1
9
Atom holding(b3)
Atom on(b3, b1)
Atom on(b3, b2)
Atom on-table(b3, t1)
Atom on-table(b3, t2)
Atom on-table(b3, t3)
Atom on-table(b3, t4)
Atom on-table(b3, t5)
Atom on-table(b3, t6)
end_variable
10
begin_mutex_group
4
10 0
6 0
7 0
12 0
end_mutex_group
begin_mutex_group
4
8 0
6 0
7 1
12 1
end_mutex_group
begin_mutex_group
4
9 0
6 1
7 0
12 2
end_mutex_group
begin_mutex_group
4
11 0
6 2
7 2
12 0
end_mutex_group
begin_mutex_group
4
0 0
6 3
7 3
12 3
end_mutex_group
begin_mutex_group
4
1 0
6 4
7 4
12 4
end_mutex_group
begin_mutex_group
4
2 0
6 5
7 5
12 5
end_mutex_group
begin_mutex_group
4
3 0
6 6
7 6
12 6
end_mutex_group
begin_mutex_group
4
4 0
6 7
7 7
12 7
end_mutex_group
begin_mutex_group
4
5 0
6 8
7 8
12 8
end_mutex_group
begin_state
0
1
1
1
0
0
5
4
0
0
0
0
6
end_state
begin_goal
1
12 1
end_goal
48
begin_operator
pickup b1 t1
0
4
0 10 0 1
0 8 0 1
0 0 -1 0
0 6 3 0
1
end_operator
begin_operator
pickup b1 t2
0
4
0 10 0 1
0 8 0 1
0 1 -1 0
0 6 4 0
1
end_operator
begin_operator
pickup b1 t3
0
4
0 10 0 1
0 8 0 1
0 2 -1 0
0 6 5 0
1
end_operator
begin_operator
pickup b1 t4
0
4
0 10 0 1
0 8 0 1
0 3 -1 0
0 6 6 0
1
end_operator
begin_operator
pickup b1 t5
0
4
0 10 0 1
0 8 0 1
0 4 -1 0
0 6 7 0
1
end_operator
begin_operator
pickup b1 t6
0
4
0 10 0 1
0 8 0 1
0 5 -1 0
0 6 8 0
1
end_operator
begin_operator
pickup b2 t1
0
4
0 10 0 1
0 9 0 1
0 0 -1 0
0 7 3 0
1
end_operator
begin_operator
pickup b2 t2
0
4
0 10 0 1
0 9 0 1
0 1 -1 0
0 7 4 0
1
end_operator
begin_operator
pickup b2 t3
0
4
0 10 0 1
0 9 0 1
0 2 -1 0
0 7 5 0
1
end_operator
begin_operator
pickup b2 t4
0
4
0 10 0 1
0 9 0 1
0 3 -1 0
0 7 6 0
1
end_operator
begin_operator
pickup b2 t5
0
4
0 10 0 1
0 9 0 1
0 4 -1 0
0 7 7 0
1
end_operator
begin_operator
pickup b2 t6
0
4
0 10 0 1
0 9 0 1
0 5 -1 0
0 7 8 0
1
end_operator
begin_operator
pickup b3 t1
0
4
0 10 0 1
0 11 0 1
0 0 -1 0
0 12 3 0
1
end_operator
begin_operator
pickup b3 t2
0
4
0 10 0 1
0 11 0 1
0 1 -1 0
0 12 4 0
1
end_operator
begin_operator
pickup b3 t3
0
4
0 10 0 1
0 11 0 1
0 2 -1 0
0 12 5 0
1
end_operator
begin_operator
pickup b3 t4
0
4
0 10 0 1
0 11 0 1
0 3 -1 0
0 12 6 0
1
end_operator
begin_operator
pickup b3 t5
0
4
0 10 0 1
0 11 0 1
0 4 -1 0
0 12 7 0
1
end_operator
begin_operator
pickup b3 t6
0
4
0 10 0 1
0 11 0 1
0 5 -1 0
0 12 8 0
1
end_operator
begin_operator
putdown b1 t1
0
4
0 10 -1 0
0 8 -1 0
0 0 0 1
0 6 0 3
1
end_operator
begin_operator
putdown b1 t2
0
4
0 10 -1 0
0 8 -1 0
0 1 0 1
0 6 0 4
1
end_operator
begin_operator
putdown b1 t3
0
4
0 10 -1 0
0 8 -1 0
0 2 0 1
0 6 0 5
1
end_operator
begin_operator
putdown b1 t4
0
4
0 10 -1 0
0 8 -1 0
0 3 0 1
0 6 0 6
1
end_operator
begin_operator
putdown b1 t5
0
4
0 10 -1 0
0 8 -1 0
0 4 0 1
0 6 0 7
1
end_operator
begin_operator
putdown b1 t6
0
4
0 10 -1 0
0 8 -1 0
0 5 0 1
0 6 0 8
1
end_operator
begin_operator
putdown b2 t1
0
4
0 10 -1 0
0 9 -1 0
0 0 0 1
0 7 0 3
1
end_operator
begin_operator
putdown b2 t2
0
4
0 10 -1 0
0 9 -1 0
0 1 0 1
0 7 0 4
1
end_operator
begin_operator
putdown b2 t3
0
4
0 10 -1 0
0 9 -1 0
0 2 0 1
0 7 0 5
1
end_operator
begin_operator
putdown b2 t4
0
4
0 10 -1 0
0 9 -1 0
0 3 0 1
0 7 0 6
1
end_operator
begin_operator
putdown b2 t5
0
4
0 10 -1 0
0 9 -1 0
0 4 0 1
0 7 0 7
1
end_operator
begin_operator
putdown b2 t6
0
4
0 10 -1 0
0 9 -1 0
0 5 0 1
0 7 0 8
1
end_operator
begin_operator
putdown b3 t1
0
4
0 10 -1 0
0 11 -1 0
0 0 0 1
0 12 0 3
1
end_operator
begin_operator
putdown b3 t2
0
4
0 10 -1 0
0 11 -1 0
0 1 0 1
0 12 0 4
1
end_operator
begin_operator
putdown b3 t3
0
4
0 10 -1 0
0 11 -1 0
0 2 0 1
0 12 0 5
1
end_operator
begin_operator
putdown b3 t4
0
4
0 10 -1 0
0 11 -1 0
0 3 0 1
0 12 0 6
1
end_operator
begin_operator
putdown b3 t5
0
4
0 10 -1 0
0 11 -1 0
0 4 0 1
0 12 0 7
1
end_operator
begin_operator
putdown b3 t6
0
4
0 10 -1 0
0 11 -1 0
0 5 0 1
0 12 0 8
1
end_operator
begin_operator
stack b1 b2
0
4
0 10 -1 0
0 8 -1 0
0 9 0 1
0 6 0 1
1
end_operator
begin_operator
stack b1 b3
0
4
0 10 -1 0
0 8 -1 0
0 11 0 1
0 6 0 2
1
end_operator
begin_operator
stack b2 b1
0
4
0 10 -1 0
0 8 0 1
0 9 -1 0
0 7 0 1
1
end_operator
begin_operator
stack b2 b3
0
4
0 10 -1 0
0 9 -1 0
0 11 0 1
0 7 0 2
1
end_operator
begin_operator
stack b3 b1
0
4
0 10 -1 0
0 8 0 1
0 11 -1 0
0 12 0 1
1
end_operator
begin_operator
stack b3 b2
0
4
0 10 -1 0
0 9 0 1
0 11 -1 0
0 12 0 2
1
end_operator
begin_operator
unstack b1 b2
0
4
0 10 0 1
0 8 0 1
0 9 -1 0
0 6 1 0
1
end_operator
begin_operator
unstack b1 b3
0
4
0 10 0 1
0 8 0 1
0 11 -1 0
0 6 2 0
1
end_operator
begin_operator
unstack b2 b1
0
4
0 10 0 1
0 8 -1 0
0 9 0 1
0 7 1 0
1
end_operator
begin_operator
unstack b2 b3
0
4
0 10 0 1
0 9 0 1
0 11 -1 0
0 7 2 0
1
end_operator
begin_operator
unstack b3 b1
0
4
0 10 0 1
0 8 -1 0
0 11 0 1
0 12 1 0
1
end_operator
begin_operator
unstack b3 b2
0
4
0 10 0 1
0 9 -1 0
0 11 0 1
0 12 2 0
1
end_operator
0
