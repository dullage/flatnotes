# wunschliste

German word for wishlist.

A fork of [flatnotes](https://github.com/dullage/flatnotes) modified to be used as wishlist for our family.

The fork is intended to drift away from the original app over time.

## Deploy

Initial deployment was done according to [this doc](https://fly.io/docs/launch/continuous-deployment-with-github-actions/). The workflow runs against the `prod` env on the `live` branch.

Some special configs for this deployment:
- Before you initially deploy the app add some secrets:
  - `fly secrets set FLATNOTES_PASSWORD=<password> --stage`
  - `fly secrets set FLATNOTES_SECRET_KEY=<secret_key_here> --stage`
- After the initial deployment a custom domain was provisioned according to [this doc](https://fly.io/docs/networking/custom-domain/) 

For Pull Requests a review environment is automatically deployed.

Secrets have been all generated manually and added to this repository.

## Thanks
 
A special thanks to the creator of flatnotes [Adam Dullage](https://github.com/dullage) for making this awesome app! 
