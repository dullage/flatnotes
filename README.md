# wunschliste

German word for wishlist.

A fork of [flatnotes](https://github.com/dullage/flatnotes) modified to be used as wishlist for our family.

## Deploy

According to [this doc](https://fly.io/docs/launch/continuous-deployment-with-github-actions/):

- Before you deploy the app add some secrets:
  - `fly secrets set FLATNOTES_PASSWORD=<password> --stage`
  - `fly secrets set FLATNOTES_SECRET_KEY=<secret_key_here> --stage`
- A custom domain was provisioned according to [this doc](https://fly.io/docs/networking/custom-domain/) (after first deployment)

## Thanks

A special thanks to the creator of flatnotes [Adam Dullage](https://github.com/dullage) for making this awesome app!