/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Probot} app
 */
module.exports = (app) => {
  app.log.info("Yay, the app was loaded!");

  app.on("issues.opened", async (context) => {
    const issueComment = context.issue({
      body: "Thanks for opening this issue!",
    });
    return context.octokit.issues.createComment(issueComment);
  });

  app.on('installation.created', async (context) => {
    const owner = context.payload.installation.account.login;

    for (const repository of context.payload.repositories) {
      const repo = repository.name;

      await context.octokit.issues.create({
        repo,
        owner,
        title: 'Thank you for installing!',
        assignee: owner,
        body: 'Greetings from **Mezidia Inspector!**\n' +
          '- My code and instructions you can see [here](https://github.com/mezidia/mezidia-inspector).\n' +
          `- My author is @${process.env.AUTHOR_USERNAME}.\n` +
          '- To close this issue, just type in comments "close".',
        labels: ['thank you'],
      });
    }
  })
};
