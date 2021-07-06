const texts = {
  'created': {
    'title': 'Thank you for installing!',
    'body': 'Greetings from **Mezidia Inspector!**\n' +
      '- My code and instructions you can see [here](https://github.com/mezidia/mezidia-inspector).\n' +
      `- My author is @${process.env.AUTHOR_USERNAME}.\n` +
      '- This issue was closed immediately.',
    'labels': ['thank you'],
  },
  'deleted': {
    'title': 'Thank you for using!',
    'body': 'If you have some reports about using this app, write this [email](mezidiaofficial@gmail.com)',
    'labels': ['good bye'],
  },
}

const handleInstallation = async (context) => {
  const owner = context.payload.installation.account.login;

  for (const repository of context.payload.repositories) {
    const repo = repository.name;

    let response = await context.octokit.issues.create({
        repo,
        owner,
        title: texts[context.payload.action].title,
        assignee: owner,
        body: texts[context.payload.action].body,
        labels: texts[context.payload.action].labels,
      }
    );
    await context.octokit.rest.issues.update({
      repo,
      owner,
      issue_number: response.data.number,
      state: 'closed'
    })
  }
}

const handleDeletion = async (context) => {
  // const owner = context.payload.installation.account.login;
  //
  // for (const repository of context.payload.repositories) {
  //   const repo = repository.name;
  //
  //   await context.octokit.issues.create({
  //       repo,
  //       owner,
  //       title: texts[context.payload.action].title,
  //       assignee: owner,
  //       body: texts[context.payload.action].body,
  //       labels: texts[context.payload.action].labels,
  //     }
  //   );
  // }
  console.log('Deleted')
}

module.exports = {handleInstallation, handleDeletion};
