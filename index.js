/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Probot} app
 */
module.exports = (app) => {
  app.log.info("Yay, the app was loaded!");

  app.on('issues.opened', async (context) => {
    const owner = context.payload.repository.owner.login;
    const issueOwner = context.payload.issue.user.login;
    const newData = context.issue({
      assignee: owner,
      labels: ['work in progress'],
    })
    const comment = context.issue({
      body: 'Hello there, ' + (issueOwner === owner ? 'sensei' : `@${issueOwner}. My owner will answer asap.`) +
        '\nYou can close_ or _reopen_ this issue just typing these words: "close" or "reopen"',
    })
    await context.octokit.issues.update(newData)
    return await context.octokit.issues.createComment(comment);
  });

  app.on('installation.created', async (context) => {
    const owner = context.payload.installation.account.login;

    for (const repository of context.payload.repositories) {
      const repo = repository.name;
      const message = {
        repo,
        owner,
        title: 'Thank you for installing!',
        assignee: owner,
        body: 'Greetings from **Mezidia Inspector!**\n' +
          '- My code and instructions you can see [here](https://github.com/mezidia/mezidia-inspector).\n' +
          `- My author is @${process.env.AUTHOR_USERNAME}.\n` +
          '- To close this issue, just type in comments "close".',
        labels: ['thank you'],
      }
      await context.octokit.issues.create(message);
    }
  })
};
