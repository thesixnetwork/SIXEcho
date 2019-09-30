const { Api, JsonRpc, RpcError } = require('eosjs');
const { JsSignatureProvider } = require('eosjs/dist/eosjs-jssig'); // development only
const fetch = require('node-fetch');
const { TextEncoder, TextDecoder } = require('util'); // node only; native TextEncoder/Decoder

const defaultPrivateKey = '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3'; // bob
const signatureProvider = new JsSignatureProvider([defaultPrivateKey]);
const rpc = new JsonRpc('http://127.0.0.1:8888', { fetch });
const api = new Api({
  rpc,
  signatureProvider,
  chainId: 'cf057bbfb72640471fd910bcb67639c22df9f92470936cddc1ade0e2f2e7dc4f',
  textDecoder: new TextDecoder(),
  textEncoder: new TextEncoder()
});
const EOS = require('eosjs');

(async () => {
  api
    .transact(
      {
        actions: [
          {
            account: 'hello',
            name: 'hi',
            authorization: [
              {
                actor: 'bob',
                permission: 'active'
              }
            ],
            data: {
              user: 'bob'
            }
          }
        ]
      },
      {
        blocksBehind: 3,
        expireSeconds: 30
      }
    )
    .then(r => {
      console.log(JSON.stringify(r, null, 2));
    })
    .catch(console.log);
})();
