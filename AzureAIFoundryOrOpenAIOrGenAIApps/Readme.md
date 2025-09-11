### [Role-based access control for Azure OpenAI in Azure AI Foundry Models](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-openai-user)

- Subscription level Owner and Contributor roles are inherited and take priority over the custom Azure OpenAI roles applied at the Resource Group level.

- Azure OpenAI roles
    - Cognitive Services OpenAI User
    - Cognitive Services OpenAI Contributor
    - Cognitive Services Contributor
    - Cognitive Services Usages Reader

#### Cognitive Services OpenAI User
- If a user were granted role-based access to only this role for an Azure OpenAI resource, they would be able to perform the following common tasks:
✅ View the resource in Azure portal
✅ View the resource endpoint under Keys and Endpoint
✅ Ability to view the resource and associated model deployments in Azure AI Foundry portal.
✅ Ability to view what models are available for deployment in Azure AI Foundry portal.
✅ Use the Chat, Completions, and DALL-E (preview) playground experiences to generate text and images with any models that have already been deployed to this Azure OpenAI resource.
✅ Make inference API calls with Microsoft Entra ID.

- A user with only this role assigned would be unable to:
❌ Create new Azure OpenAI resources
❌ View/Copy/Regenerate keys under Keys and Endpoint
❌ Create new model deployments or edit existing model deployments
❌ Create/deploy custom fine-tuned models
❌ Upload datasets for fine-tuning
❌ View, query, filter Stored completions data
❌ Access quota
❌ Create customized content filters


#### Cognitive Services OpenAI Contributor
- This role has all the permissions of Cognitive Services OpenAI User and is also able to perform additional tasks like:
✅ Create custom fine-tuned models
✅ Upload datasets for fine-tuning
✅ View, query, filter Stored completions data
✅ Create new model deployments or edit existing model deployments [Added Fall 2023]
✅ Grant access to the Assistants API
✅ Add data sources to Azure OpenAI On Your Data.
- A user with only this role assigned would be unable to:
❌ Create new Azure OpenAI resources
❌ View/Copy/Regenerate keys under Keys and Endpoint
❌ Access quota
❌ Create customized content filters.

#### Cognitive Services Contributor
- This role is typically granted access at the resource group level for a user in conjunction with additional roles. By itself this role would allow a user to perform the following tasks.
✅ Create new Azure OpenAI resources within the assigned resource group.
✅ View resources in the assigned resource group in the Azure portal.
✅ View the resource endpoint under Keys and Endpoint
✅ View/Copy/Regenerate keys under Keys and Endpoint
✅ Ability to view what models are available for deployment in Azure AI Foundry portal
✅ Use the Chat, Completions, and DALL-E (preview) playground experiences to generate text and images with any models that have already been deployed to this Azure OpenAI resource
✅ Create customized content filters
✅ Add data sources to Azure OpenAI On Your Data.
✅ Create new model deployments or edit existing model deployments (via API)
✅ Create custom fine-tuned models [Added Fall 2023]
✅ Upload datasets for fine-tuning [Added Fall 2023]
✅ Create new model deployments or edit existing model deployments (via Azure AI Foundry) [Added Fall 2023]
✅ View, query, filter Stored completions data
- A user with only this role assigned would be unable to:
❌ Access quota
❌ Make inference API calls with Microsoft Entra ID.

#### Cognitive Services Usages Reader
- Viewing quota requires


### [Agent Service - Quickstart: Create a new agent](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart?pivots=rest-api)
- Azure AI Foundry Agent Service allows you to create AI agents tailored to your needs through custom instructions and augmented by advanced tools like code interpreter, and custom functions.
- **Create an agent**:
    - With Azure AI Agents Service the model parameter requires model deployment name. If your model deployment name is different than the underlying model name then you would adjust your code to "model": "{your-custom-model-deployment-name}".
    ```JSON
    curl --request POST \
        --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=2025-05-01 \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "instructions": "You are a helpful agent.",
            "name": "my-agent",
            "tools": [{"type": "code_interpreter"}],
            "model": "gpt-4o-mini"
        }'
    ```

- **Create a thread**:
    ```JSON
    curl --request POST \
        --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=2025-05-01 \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        -d ''
    ```

- **Add a user question to the thread**:
    ```JSON
    curl --request POST \
        --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=2025-05-01 \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        -d ''
    ```

- **Run the thread**:
    ```JSON
    curl --request POST \
        --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=2025-05-01 \
        -H "Authorization: Bearer $AGENT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "assistant_id": "asst_abc123",
        }'
    ```