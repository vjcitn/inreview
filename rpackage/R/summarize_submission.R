#' summarize the repo underlying a submission issue
#' @param url character(1) with correct https URL for contribution repo
#' @note At present we have hardcoded the LLM to use as gpt-4. At most 2000 words from DESCRIPTION
#' and at most 4000 words from README are provided for a brief prompt asking for technical summary.
#' @note The python code was written by instructing perplexity.ai on Nov 18 2025.
#' @return A list with components `summary` (text string with summary, and `url`
#' (the repo URL string.  See inst/python/summ1.py for hardcoded openai parameters
#' @examples
#' t1 = summarize_submission("https://github.com/bioconductor/AnVILVRS")
#' cat(strwrap(t1, 75), sep="\n")
#' @export
summarize_submission = function(url) {
 spl = strsplit(url, "\\/")
 owner = spl[[1]][4]
 repo = spl[[1]][5]
 pysoft = pymods4issues()
 meta = try( pysoft$get_repo_metadata(owner, repo) )
 if (inherits(meta, "try-error")) stop("problem with get_repo_metadata")
 names(meta) = c("repo_meta", "README", "DESCRIPTION")
 summ = pysoft$summarize_purpose_with_openai( meta[["repo_meta"]], meta[["README"]], meta[["DESCRIPTION"]] )
 summ = iconv(summ, to="ASCII")
 list(summary=summ, url=url)
}
