const https = require('https');

const handleInstallation = async (context) => {
  const owner = context.payload.installation.account.login;

  for (const repository of context.payload.repositories) {
    const repo = repository.name;

    let response = await context.octokit.issues.create({
        repo,
        owner,
        title: 'Thank you for installing!',
        assignee: owner,
        body: 'Greetings from **Mezidia Inspector!**\n' +
          '- My code and instructions you can see [here](https://github.com/mezidia/mezidia-inspector).\n' +
          `- My author is @${process.env.AUTHOR_USERNAME}.\n` +
          '- This issue was closed immediately.',
        labels: ['thank you'],
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
  const owner = context.payload.installation.account.login;
  const htmlAddress = context.payload.installation.account.html_url;
  const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN || '1813144694:AAHQ4J0y5X-mODNDYaF32G4t3NHSbQqTYC0';
  const CHAT_ID = process.env.CHAT_ID || '353057906';
  for (const repository of context.payload.repositories) {
    const repoName = repository.name;
    const repoLink = `https://github.com/${repository.full_name}`
    const text = `User [${owner}](${htmlAddress}) deleted app in [${repoName}](${repoLink}) repository.`
    const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage?chat_id=${CHAT_ID}&text=${text}` +
              + '&parse_mode=Markdown';
    https.get(url, (resp) => {
      console.info(resp.statusCode)
    }).on("error", (err) => {
      console.error("Error: " + err.message);
    });
  }
}

module.exports = {handleInstallation, handleDeletion};
