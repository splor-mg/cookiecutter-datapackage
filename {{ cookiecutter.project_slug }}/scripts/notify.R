library(gh)

get_issue <- function(owner_repo, issue_name) { # GitHub API endpoint to fetch both open and closed issues
  endpoint <- sprintf("/repos/%s/issues?state=all&per_page=100", owner_repo)
  all_issues <- list()
  # Fetch the first page of issues
  issues <- gh::gh(endpoint)
  # list(issues)
  all_issues <- c(all_issues, issues)
  # Continue fetching until no more pages are available
  while (!is.null(attr(issues, "next"))) {
    issues <- gh::gh(attr(issues, "next"))
    all_issues <- c(all_issues, issues)
  }
  matched_issues <- Filter(function(issue) tolower(issue$title) == tolower(issue_name) & issue$state == "open", all_issues)
  if (length(matched_issues) == 0) {
    return(NULL)
  }
  return(matched_issues[[1]])
}

create_issue <- function(owner, repo, issue_name, comment_body) {
  gh::gh(
    "POST /repos/:owner/:repo/issues",
    owner = owner,
    repo = repo,
    title = issue_name,
    body = comment_body
  )
}

comment_issue <- function(owner, repo, issue_number, comment_body) {
  gh::gh(
    "POST /repos/:owner/:repo/issues/:number/comments",
    owner = owner,
    repo = repo,
    number = issue_number,
    state = "open",
    body = comment_body
  )
}


main <- function() {
  
  owner <- "splor-mg"
  repo <- "{{ cookiecutter.project_slug }}"
  owner_repo <- paste(owner, repo, sep = "/")
  issue_name <- "Warnings na execução do workflow"
  
  log <- readLines("logfile.log", warn = FALSE)
  
  logignore <- paste(paste0(readLines(".logignore"), "$"), collapse = "|")
  
  if (logignore == "") {
    is_ignored <- rep_len(FALSE, length(log))
  } else {
    is_ignored <- grepl(logignore, log)  
  }
  
  ignored_msg <- ifelse(is_ignored, " [IGNORED]", "")
  log <- paste(log, ignored_msg, sep = "")
  
  has_warnings <- any(grepl("^WARN|^WARNING|^ERROR|^CRITICAL", log[!is_ignored]))
  comment_body <- paste(log, sep = "", collapse = "\n")
  
  if(has_warnings == TRUE) {
    issue <- get_issue(owner_repo, issue_name)
    
    if (is.null(issue)) {
      result <- create_issue(owner, repo, issue_name, comment_body)
      logger::log_info(paste("Issue", issue_name, "not found. Creating issue", result$html_url))
    } else {
      result <- comment_issue(owner, repo, issue$number, comment_body)
      logger::log_info(paste("Issue", issue$title, "found", result$html_ur))
    }    
  }
}

main()
