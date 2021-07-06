/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Probot} app
 */

const {handleInstallation, handleDeletion} = require('./lib/installation');
const {handleIssueOpen} = require('./lib/issues');

module.exports = (app) => {
  app.log.info("Yay, the app was loaded!");

  app.on('issues.opened', async (context) => await handleIssueOpen(context));

  app.on('installation.created', async (context) => await handleInstallation(context))
  app.on('installation.deleted', async (context) => await handleDeletion(context))
}
