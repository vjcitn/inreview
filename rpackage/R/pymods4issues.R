#' obtain modules for interrogating and summarizing a github issues stream
#' @examples
#' pp = pymods4issues()  # wants GITHUB_TOKEN and OPENAI_API_KEY
#' names(pp)
#' @export
pymods4issues = function() {
 reticulate::py_require("openai")  # maybe pin versions?
 reticulate::py_require("requests")
 reticulate::py_run_file(system.file("python", "summ1.py", package="BiocRevSumm"))
}
