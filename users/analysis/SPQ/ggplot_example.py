from rpy2 import robjects
from rpy2.robjects import Formula
from rpy2.robjects.lib.ggplot2 import *
from rpy2.robjects.vectors import IntVector, FloatVector
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr
from rpy2.robjects.lib import ggbupr

grid.newpage()
# create a rows/columns layout
lt = grid.layout(3, 1)
vp = grid.viewport(layout = lt)
# push it the plotting stack
vp.push()

# create a viewport located at (1,1) in the layout
vp = grid.viewport(**{'layout.pos.col':1, 'layout.pos.row': 1})
# create a (unit) rectangle in that viewport
#grid.rect(vp = vp).draw()
p1.plot(vp=vp)

vp = grid.viewport(**{'layout.pos.col':1, 'layout.pos.row': 2})
# create text in the viewport at (1,2)
p2.plot(vp=vp)

vp = grid.viewport(**{'layout.pos.col':1, 'layout.pos.row': 3})
# create a (unit) circle in the viewport (1,3)
p3.plot(vp=vp)

vp = grid.viewport(**{'layout.pos.col':1, 'layout.pos.row': 4})
# create a (unit) circle in the viewport (1,3)
p4.plot(vp=vp)