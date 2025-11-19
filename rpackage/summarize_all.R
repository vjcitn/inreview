

prompt = "Here is a list of github repository URLs for R packages and associated textual descriptions of package capabilities. Please group the packages into 2-4 conceptual topics focusing on the molecular biology methods addressed by the package.  Produce a markdown document with the grouping.  For each package in the grouping provide the URL as given."

library(ellmer)
library(btw)

#ch = chat_openai(model="gpt-4")

library(BiocRevSumm)

urls = get_repos_from_open_issues("bioconductor", "contributions")


desc = lapply(seq_len(length(urls)), function(i) {Sys.sleep(15); cat(urls[i], "\n"); try(summarize_submission(urls[i]))}) # costs
save(desc, file="desc.rda")

library(ellmer)
library(btw)
ch = chat_openai(model="gpt-4")
#load("desc.rda")
dr = which(sapply(desc, function(x) is.na(x$summary)))
if (length(dr)>0) desc = desc[-dr]
ch$chat(btw(desc), prompt)
