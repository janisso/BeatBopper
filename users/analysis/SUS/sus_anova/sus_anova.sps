SET DECIMAL=DOT.

DATA LIST FILE= "/Users/mb/Desktop/Janis.so/06_qmul/BeatBopper/users/analysis/SUS/sus_anova/sus_anova.csv"  free (",")
ENCODING="Locale"
/ rater * system (F8.0) score 
  .

VARIABLE LABELS
rater "rater" 
 system "system" 
 score "score" 
 .

VALUE LABELS
/
system 
1 "Each Beat" 
 2 "Borch" 
 3 "Phase" 
.
VARIABLE LEVEL system 
 (ordinal).
VARIABLE LEVEL rater, score 
 (scale).

EXECUTE.
