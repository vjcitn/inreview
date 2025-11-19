
prompt = "Here is a list of github repository URLs for R packages and associated textual descriptions of package capabilities. Please group the packages into 10-12 conceptual topics focusing on the molecular biology methods addressed by the package.  Produce a markdown document with the grouping.  For each package in the grouping provide the URL as given."

library(ellmer)
library(btw)
ch = chat_openai(model="gpt-4o")
#load("desc.rda")
#dr = which(sapply(desc, function(x) is.na(x$summary)))
#if (length(dr)>0) desc = desc[-dr]
ch$chat(btw(desc), prompt)
