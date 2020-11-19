var { AgentAuthorizationClient, BackendITwinClientLoggerCategory } = require("@bentley/backend-itwin-client");
var { AuthStatus, BentleyError, ClientRequestContext, Logger } = require("@bentley/bentleyjs-core");
var { GrantBody, TokenSet } = require("openid-client");
var { credentials } = require("../../config.json");
var { clientId, clientSecret, scope } = credentials['imodel']

var express = require('express');

const loggerCategory = BackendITwinClientLoggerCategory.Authorization;
var app = express();
app.set('port', 3000);
app.listen(app.get('port'));

app.get('/token', (req: any, res: any) => {
    const config = {
        clientId: clientId,
        clientSecret: clientSecret,
        scope: scope,
    }

    try {
        const agent = new AgentAuthorizationClient(config);
        agent.getAccessToken(new ClientRequestContext()).then((accessToken: any) => {
            const token = JSON.stringify(accessToken);
            res.send(token);
        });
    } catch(e) {
        console.log(e);
        res.send('');
    }
})

