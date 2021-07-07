const {leaveComment} = require('./utils')

const comments = {
  'opened': 'Hello there, ' + (issueOwner === owner ? 'sensei' : `@${issueOwner}. My owner will answer asap.`) +
    '\nYou can _close_ or _reopen_ this issue just typing these words: "close" or "reopen"',
  'closed': '',
  'labeled': '',
}

const handleIssue = async (context) => {
  const owner = context.payload.repository.owner.login;
  const issueOwner = context.payload.issue.user.login;
  let comment;
  if (context.payload.action === 'opened') {
    if (!context.payload.issue.body.startsWith('Greetings from')) {
      const newData = context.issue({
        assignee: owner,
        labels: ['work in progress'],
      })
      await context.octokit.issues.update(newData)
      comment = context.issue({
        body: comments[context.payload.action],
      })
    }
  }
  else {
    comment = context.issue({
      body: 'Wow! New label! @{sender}, thank you!',
    })
  }
  return await leaveComment(context.octokit.issues, comment);
}

module.exports = {handleIssue};
