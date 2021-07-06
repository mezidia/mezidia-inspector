const handleIssueOpen = async (context) => {
  const owner = context.payload.repository.owner.login;
  const issueOwner = context.payload.issue.user.login;
  if (!context.payload.issue.body.startsWith('Greetings from')) {
    const newData = context.issue({
      assignee: owner,
      labels: ['work in progress'],
    })
    const comment = context.issue({
      body: 'Hello there, ' + (issueOwner === owner ? 'sensei' : `@${issueOwner}. My owner will answer asap.`) +
        '\nYou can _close_ or _reopen_ this issue just typing these words: "close" or "reopen"',
    })
    await context.octokit.issues.update(newData)
    return await context.octokit.issues.createComment(comment);
  }
}

module.exports = {handleIssueOpen};
