* Encoding: ISO-8859-1.
SET DECIMAL=DOT.

DATA LIST FILE= "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SPQ/data_for_spss.csv"  free (",")
ENCODING="Locale"
/ excerpt (F8.0) rmse * systems (F8.0) 
  .

VARIABLE LABELS
excerpt "excerpt" 
 rmse "rmse" 
 systems "systems" 
 .

VALUE LABELS
/
excerpt 
1 "e1" 
 2 "e2" 
 3 "e3" 
/
systems 
1 "Each Beat" 
 2 "Borch" 
 3 "Phase" 
.
VARIABLE LEVEL systems 
 (ordinal).
VARIABLE LEVEL rmse 
 (scale).

EXECUTE.
