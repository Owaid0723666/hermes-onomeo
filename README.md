# hermes-onomeo

[onomeo](https://onomeo.com) model-provider plugin for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

Maintained by onomeo. onomeo is an OpenAI-compatible gateway: one key reaches Claude, GPT, Gemini, DeepSeek, Kimi and GLM models, billed per token from a prepaid balance. New accounts can call `deepseek-v4.1-flash` for free within daily limits. onomeo is in public beta: not every feature is guaranteed to work, and feedback is being collected.

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
- **What onomeo keeps:** for each call made with an API key, onomeo keeps an excerpt under your account (the first 1,000 characters of the system prompt, the first 4,000 characters of the last user message and the first 4,000 characters of the reply), with the time, model, calling tool name, result and amount used. At most the latest 100 calls are kept, nothing older than 30 days, and the record is erased when the account is deleted. onomeo does not use them to train models. The last message of each request and each reply are checked against a blocklist for child sexual abuse material. See the [Privacy Policy](https://onomeo.com/privacy) and [Terms](https://onomeo.com/terms).
- **Model listing:** the picker calls `GET /v1/models` with your key.
- **Billing:** paid models are billed per token from your prepaid onomeo balance (top-ups from 5 US dollars by card, WeChat Pay or Alipay). Free models have daily limits. The plugin itself makes no payments.
- **Credentials:** `ONOMEO_API_KEY` only, through Hermes' standard provider auth. The plugin never reads `.env`, `auth.json` or any other credential store.
- **No** background processes, self-updating code, shell commands or telemetry. Requests carry a `User-Agent: HermesAgent-onomeo/<version>` header so onomeo can count usage per calling tool.

## Changes

- **0.1.0:** first release.

## Development

```bash
hermes plugins validate --install-deps .
```

## License

MIT
