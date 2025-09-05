# Copilot Instructions for azure-ai-engineer-associate-practicals

## Project Overview
This repository contains practicals, templates, and sample code for Azure AI-102 certification preparation. It covers GenAI app development, RAG (Retrieval-Augmented Generation), document intelligence, and multimodal AI scenarios using Azure services.

## Major Components & Structure
- **ContentUnderstanding/**: Demos for document, video, and multimodal content analysis. Key scripts in `src/` and clients in `python/`.
- **DevelopGenAIApps/**: Stepwise GenAI app development, including:
  - Model deployment (`02-Choose-Deploy-models-from-model-catalog/`)
  - GenAI chat apps (`03-AIApp-with-AzureAIFoundrySDK/`)
  - Prompt flow management (`04-Using-promptflow-to-manage-conversation-in-chatapp/`)
  - RAG implementations (`05-Develop-GenAI-app-using-RAG/`)
  - LLM fine-tuning (`06-FineTuning-LLM-on-Serverless/`)
- **SampleCodes/**: Standalone samples for document intelligence, entity linking, language, vision, and more.

## Key Workflows
- **Authentication**: Use `az login` (or `az login --use-device-code` in Codespaces) before running scripts that interact with Azure.
- **Environment Setup**: Many scripts require Azure resource details in YAML or environment variables. See `DevelopGenAIApps/04-Using-promptflow-to-manage-conversation-in-chatapp/README.md` for provisioning steps.
- **Running Demos**: Most scripts are run directly with Python. Example:
  ```sh
  cd ContentUnderstanding/src
  python document_main.py
  ```
- **Provisioning Resources**: Some flows require running provisioning scripts (e.g., `python provisioning/provision.py --export-env .env` from the correct directory).

## Project Conventions
- **Directory Structure**: Each major scenario is isolated in its own folder with a `Readme.md` and supporting scripts/data.
- **Naming**: Scripts are named for their scenario (e.g., `search_with_video.py`, `fine_tune.ipynb`).
- **Data**: Sample data is in `data/` subfolders within each scenario.
- **No Monolithic Entrypoint**: Each scenario is self-contained; there is no single build or run command for the whole repo.

## Integration & Dependencies
- **Azure SDKs**: Most scripts use Azure Python SDKs (e.g., `azure-ai`, `azure-search-documents`).
- **Prompt Flow**: Some GenAI apps use Azure Prompt Flow for managing chat and RAG workflows.
- **External Resources**: Resource names, keys, and endpoints are often required as environment variables or YAML config.

## Examples
- To run a RAG app:
  ```sh
  cd DevelopGenAIApps/05-Develop-GenAI-app-using-RAG
  python rag_app.py
  ```
- To fine-tune an LLM:
  ```sh
  cd DevelopGenAIApps/06-FineTuning-LLM-on-Serverless
  python finetune_and_invoke_llm.py
  ```

## Tips for AI Agents
- Always check the scenario's `Readme.md` for setup and run instructions.
- Scripts are not guaranteed to be production-ready; validate outputs for your use case.
- When adding new samples, follow the existing folder and naming conventions.

---
For more details, see the main `README.md` and scenario-specific `Readme.md` files.
