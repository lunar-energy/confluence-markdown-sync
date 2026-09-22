# Confluence Markdown Sync Action

This Github Action serves the purpose of copying the contents of a Markdown `.md` file to a Confluence Cloud Page.

## Getting Started

```yml
# .github/workflows/my-workflow.yml
on: [push]

jobs:
  dev:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - uses: lunar-energy/confluence-markdown-sync@v1
        with:
          from: './README.md'
          to: '123456' # The confluence page id where to write the output
          cloud: <my-confluence-cloud-id>
          user: <my.user@example.org> # omit for a service account token
          token: <my-token>
```

## Authentication

Uses the Confluence REST API **v2** (`/wiki/api/v2/pages`).

Two credential styles are supported:

- **Basic auth** — supply `user` (the email that owns the token) and `token`.
- **Bearer** — omit `user`. The token is sent as `Authorization: Bearer <token>`.
  This is what Atlassian **service account** tokens require, as those accounts
  have no email/password pair.

### Scoped and service account tokens

Scoped tokens (including every service account token) only work against the
platform gateway, never your site URL. Pass the gateway as `cloud`:

```yml
cloud: 'https://api.atlassian.com/ex/confluence/<cloudId>'
```

Your `cloudId` is at `https://<subdomain>.atlassian.net/_edge/tenant_info`.

Because this action calls v2, a scoped token needs the **granular** scopes —
`read:page:confluence` and `write:page:confluence`. The classic scopes
(`read:confluence-content.all`, `write:confluence-content`) are for the v1 API
and will fail with `401 Unauthorized; scope does not match`. Scopes cannot be
edited after a token is created; a different set means a new token.

Scopes are not permissions: the account must also hold Confluence product
access and **Pages: Add** on the target space, or the update returns 403.

- `cloud`: Can be either:
  - A subdomain (`acme` for Atlassian hosted instances (e.g. `https://acme.atlassian.net`))
  - A full URL (e.g., `https://mycompany.com` for self-hosted instances)

- `user`: The user that generated the access token

- `token`: You can generate the token [here](https://id.atlassian.com/manage-profile/security/api-tokens). Link to [Docs](https://confluence.atlassian.com/cloud/api-tokens-938839638.html)

- `to`: The page ID can be found by simply navigating to the page where you want the content to be posted to and look at the url. It will look something like this: 
  - For Atlassian hosted: `https://<subdomain>.atlassian.net/wiki/spaces/<space>/pages/<page-id>/<title>`
  - For self-hosted: `https://<your-url>/wiki/spaces/<space>/pages/<page-id>/<title>`

### Using secrets

It's **higly reccomended** that you use secrets!

To use them you need them to specify them before in your repo. [Docs](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)

Then you can use them in any input field.

```yml
# .github/workflows/my-workflow.yml
# ...
token: ${{ secrets.token }}
```

## Known Limitations

For now images will not be uploaded [see ticket](https://github.com/cupcakearmy/confluence-markdown-sync/issues/5), they would require extra steps. If anyone feedls brave enough, constributions are welcomed :)

## Development

1. Clone the repo
2. Install [act](https://github.com/nektos/act)
3. Create the same config in the repo folder as in the getting started section above.
4. Change `uses: lunar-energy/confluence-markdown-sync` -> `uses: ./`
5. Create an example markdown file `Some.md` and set it in the config `from: './Some.md'`
6. Run locally `act -b`

### With secrets

You can simply create a `.secrets` file and specify it to `act`.

```
TOKEN=abc123
```

```yml
# .github/workflows/dev.yml
# ...
token: ${{ secrets.token }}
```

```bash
act -b --secret-file .secrets
```
