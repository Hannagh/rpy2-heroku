install.packages("blockTools")
require(blockTools)

#  Capture important stuff from the API

unit.id <- "[API INPUT]"

exact.var.in <- "[API INPUT]"
exact.var.val.in <- "[API INPUT]"

covar.var.in <- "[API INPUT]"
covar.var.val.in <- "[API INPUT]"


## Assign first unit (assume a 25 year old member of the Republican Party) to a treatment group.
## Save the results in file "sdata.RData":

seqout <- seqblock(query = FALSE, id.vars = "ID", id.vals = unit.id, exact.vars = exact.var.in,
    exact.vals = exact.var.val.in, covar.vars = "age", covar.vals = 25, file.name = "sdata.RData")

final.output <- seqout$x[seqout$x['ID'] == 1 , "Tr"]

## Assign next unit (age 30, Democratic Party):
## seqblock(query = FALSE, object = "sdata.RData", id.vals = 002, exact.vals = "Democrat",
## covar.vars = "age", covar.vals = 30, file.name = "sdata.RData")


# Then finally spit out 'final.output'
