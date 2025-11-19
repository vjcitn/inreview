#' derive target repos from all open issues for a contributions-like repository
#' @param owner character(1) github.com repo owner
#' @param repo character(1) repo name
#' @note The python code was written by instructing perplexity.ai on Nov 18 2025.
#' @return A vector of URLs supplied by contributors, identifying the URL of their contribution's repo.
#' @examples
#' rs = get_repos_from_open_issues("bioconductor", "contributions")
#' head(rs)
#' @export
get_repos_from_open_issues = function(owner, repo) {
 pysoft = pymods4issues()
 zz = pysoft$get_issues(owner, repo) # get all issues
 ans = lapply(zz, pysoft$get_first_url_issue_and_comments)  # complex extraction of "Repository" from issues
 gsub("Repository: ", "", sapply(ans, "[", 1)) # extract the actual URL
}
