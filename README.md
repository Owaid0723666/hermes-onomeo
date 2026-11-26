# hermes-onomeo

[onomeo](https://onomeo.com) model-provider plugin for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

Maintained by onomeo. onomeo is an OpenAI-compatible gateway: one key reaches Claude, GPT, Gemini, DeepSeek, Kimi and GLM models, billed per token from a prepaid balance. New accounts can call `deepseek-v4.1-flash` for free within usage limits (30 free-model calls per account every 5 hours). onomeo is in public beta: not every feature is guaranteed to work, and feedback is being collected.

This plugin registers an `onomeo` provider profile (alias `onomeo-ai`) so the setup wizard, key storage, `/model` picker, `hermes doctor` and `--provider onomeo` work without editing YAML. It is two files: `plugin.yaml` and `__init__.py`. It uses only `providers.register_provider(ProviderProfile)`: no tools, hooks, middleware or core patching.

## Install

```bash
hermes plugins install onomeo                          # from the Hermes plugin catalog, once listed
# or straight from this repo:
hermes plugins install Owaid0723666/hermes-onomeo --enable
```

Then add your key (create one at https://onomeo.com/dashboard):

```bash
hermes auth add onomeo                                 # or: export ONOMEO_API_KEY=...
hermes -z "hello" --provider onomeo -m deepseek-v4.1-flash
```

| Setting | Value |
| --- | --- |
| Provider id | `onomeo` (alias `onomeo-ai`) |
| API key env var | `ONOMEO_API_KEY` |
| Base URL override | `ONOMEO_BASE_URL` (default `https://onomeo.com/v1`) |
| API mode | `chat_completions` |
| Model list | live `GET https://onomeo.com/v1/models` with your key; a short fallback list is shown only when that is unreachable |
| Aux model (compression, titles) | `deepseek-v4.1-flash` |

Model ids are bare, for example `deepseek-v4.1-flash`, `claude-sonnet-5.5`, `claude-opus-5.5`, `claude-haiku-5.5`, `gpt-6.2-sol`, `gemini-4-argon`, `kimi-k3` and `glm-5.3`. The live catalog is the source of truth for what is available. Pick a model with native tool calling for agent work.

Vision is left off (`supports_vision` default `False`) because input modalities differ per model.

## What this plugin does and sends (disclosure)

- **Network calls:** Hermes' normal provider traffic to `https://onomeo.com/v1`: your prompts, conversation history, tool definitions and tool results. onomeo forwards each request to a third-party provider that serves the chosen model; that provider's processing location and retention can differ per model.
- **What onomeo keeps:** for each call made with an API key, onomeo keeps an excerpt under your account (the first 1,000 characters of the system prompt, the first 4,000 characters of the last user message and the first 4,000 characters of the reply), with the time, model, calling tool name, result and amount used. At most the latest 100 calls are kept, nothing older than 30 days, and the record is erased when the account is deleted. onomeo does not use them to train models. See the [Privacy Policy](https://onomeo.com/privacy) and [Terms](https://onomeo.com/terms).
- **Content moderation record (kept separately):** the last message of each request and each reply are compared with a list of terms for child sexual abuse material on onomeo's own server; nothing is sent elsewhere for this check. Each check creates a separate moderation record that is not covered by the 100-call / 30-day limit above: the time, your account and its email address, where on the site it happened, the first 200 characters of the checked message or reply, the decision, the category and the operator's review, if any. Only the operator can see these records. The most recent 5,000 records across the whole site are kept, and older ones are deleted as new ones arrive. When the account is deleted, the account, email address and excerpt are removed from its records; the time, place, category, decision and review are kept as the record of how the policy was enforced. This is described in the [Privacy Policy](https://onomeo.com/privacy) under "Content moderation".
- **Model listing:** the picker calls `GET /v1/models` with your key.
- **Billing:** paid models are billed per token from your prepaid onomeo balance (top-ups from 5 US dollars by card, WeChat Pay or Alipay). Free models have usage limits (30 calls per account every 5 hours). The plugin itself makes no payments.
- **Credentials:** `ONOMEO_API_KEY` only, through Hermes' standard provider auth. The plugin never reads `.env`, `auth.json` or any other credential store.
- **No** background processes, self-updating code, shell commands or telemetry. Requests carry a `User-Agent: HermesAgent-onomeo/<version>` header so onomeo can count usage per calling tool.

## Changes

- **0.1.0:** first release. README: disclose the separate content-moderation record and its retention.

## Development

```bash
hermes plugins validate --install-deps .
```

## License

MIT
