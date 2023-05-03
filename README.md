# tap-linkedin-sdk

LinkedIn tap class.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.


## Installation

```bash
pipx install git+https://github.com/MeltanoLabs/tap-linkedin-sdk.git@main
```


## Configuration

### Accepted Config Options

This tap requires the following environmental variables to be set in ```.env```

- [ ] `TAP_LINKEDIN_ACCOUNTS:` linkedin account ID
- [ ] `TAP_LINKEDIN_ACCESS_TOKEN:` linkedin access token
- [ ] `TAP_LINKEDIN_REFRESH_TOKEN:` refresh token
- [ ] `TAP_LINKEDIN_CLIENT_ID:` client ID
- [ ] `TAP_LINKEDIN_OWNER:` owner ID
- [ ] `TAP_LINKEDIN_CAMPAIGN:` campaign ID
- [ ] `TAP_LINKEDIN_CLIENT_SECRET:` client secret

## Meltano Variables

The following config values need to be set in order to use with Meltano. These can be set in `meltano.yml`, via
```meltano config tap-linkedin set --interactive```, or via the env var mappings shown above.

- [ ] `account_id:` linkedin account id
- [ ] `access_token:` linkedin access token
- [ ] `refresh_token:` linkedin api refresh token
- [ ] `client_id:` client id
- [ ] `owner_id:` owner id
- [ ] `campaign_id:` campaign id
- [ ] `client_secret:` client secret
- [ ] `user_agent:` user agent
- [ ] `linkedin_version:` linkedin api version
- [ ] `start_date:` start date
- [ ] `end_date:` end_date

A full list of supported settings and capabilities is available by running:

```bash
tap-linkedin --about
```

### Authentication

The tap requires a LinkedIn OAuth 2.0 access token to make API requests

The access token requires the following permissions:

```r_ads```: read ads  
```rw_ads```: read-write ads  
```r_ads_reporting```: read ads reporting

Access tokens expire after 60 days and require a user to manually authenticate
again. See the [LinkedIn API docs](https://learn.microsoft.com/en-us/linkedin/shared/authentication/postman-getting-started) for more info

## Usage

### AdAnalytics API Column Limitation

The AdAnalytics endpoint in the LinkedIn API can call up to 20 columns at a time, we can create child classes which have 20 columns in them, we can merge their output with get records function.

### SDK X-Restli-Protocol Limitation

The creatives endpoint requires X-Restli-Protocol to be set to 2.0.0. The request URL for tap-linkedin uses ‘()’, which are typically 
encoded in a request URL, but are not when the X-Restli-Protocol is 2.0.0. However, the SDK does not have any handling for reduced encoding yet,
so a request to the creatives endpoint using the tap is currently not possible. When the SDK is updated to handle X-Restli-Protocol is 2.0.0, then
requests to the creatives endpoint using tap-linkedin will be possible.


### Metadata Columns

- [ ] `add_metadata_columns:` Setting this config to 'true' adds the `_SDC_BATCHED_AT`, `_SDC_DELETED_AT` and `_SDC_EXTRACTED_AT` metadata columns to the loaded tables

### Elastic License 2.0

The licensor grants you a non-exclusive, royalty-free, worldwide, non-sublicensable, non-transferable license to use, copy, distribute, make available, and prepare derivative works of the software.

### Executing the Tap Directly

```bash
tap-linkedin-sdk --version
tap-linkedin-sdk --help
tap-linkedin-sdk --config CONFIG --discover > ./catalog.json
```

## Contributing

This project uses parent-child streams. Learn more about them [here](https://gitlab.com/meltano/sdk/-/blob/main/docs/parent_streams.md).

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
``` 

### Create and Run Tests

Create tests within the `lib_tap_linkedin_sdk/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-linkedin-sdk` CLI interface directly using `poetry run`:

```bash
poetry run tap-linkedin --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-linkedin-sdk
meltano install tap-linkedin
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-linkedin --version
# OR run a test `elt` pipeline:
meltano elt tap-linkedin target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
