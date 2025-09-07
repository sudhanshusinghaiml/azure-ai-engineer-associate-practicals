# Fine-tune models using serverless API deployments in Azure AI Foundry
# Source: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/fine-tune-serverless?tabs=chat-completion&pivots=programming-language-python

import os
import time
import uuid
import requests
from azure.ai.ml import MLClient
from azure.identity import (
    DefaultAzureCredential,
    InteractiveBrowserCredential,
)
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Data
from azure.ai.ml.entities import MarketplaceSubscription
from azure.ai.ml.finetuning import FineTuningTaskType, create_finetuning_job
from azure.ai.ml.entities import ServerlessEndpoint
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment


class FineTuneLLM():
    def __init__(self):
        self.subscription_id = os.getenv("SUBSCRIPTION_ID")
        self.resource_group = os.getenv("RESOURCE_GROUP")
        self.workspace_name = os.getenv("WORKSPACE_NAME")
        
        self.dataset_version = os.getenv('DATASET_VERSION')
        self.training_data_path = os.getenv('TRAINING_DATA_PATH')
        self.train_dataset_name = os.getenv('TRAIN_DATASET_NAME')
        self.validation_data_path = os.getenv('VALIDATION_DATA_PATH')
        self.validation_dataset_name = os.getenv('VALIDATION_DATASET_NAME')

        self.ml_client: MLClient = None
        self.registry: MLClient = None
        
        self.short_guid = str(uuid.uuid4())[:8]        
        self.deployed_endpoint = os.getenv("DEPLOYED_ENDPOINT", "")
        # self.deployed_model_id = os.getenv("DEPLOYED_MODEL_ID", "")
        
        self.workspace = None
        self.finetuned_model_name = None
        self.finetuned_model_version = None
        
        self.created_endpoint = None


    def get_client(self):
        """ 
            Create the client to consume the model. The following code uses an endpoint URL and key that are 
            stored in environment variables. and is passed when object is initialized
        """
        try:
            credential = DefaultAzureCredential()
            credential.get_token("https://management.azure.com/.default")
        except Exception as ex:
            credential = InteractiveBrowserCredential()

        try:
            self.ml_client = MLClient.from_config(credential=credential)
        except:
            self.ml_client = MLClient(
                credential,
                subscription_id = self.subscription_id,
                resource_group_name = self.resource_group,
                workspace_name = self.workspace_name,
            )

        # the models, fine tuning pipelines and environments are available in various AzureML system registries,
        # Example: Phi family of models are in "azureml", Llama family of models are in "azureml-meta" registry.
        self.registry = MLClient(credential, registry_name="azureml")

        # Get AzureML workspace object.
        self.workspace = self.ml_client._workspaces.get(self.ml_client.workspace_name)

        return self.workspace.id, self.registry
    
    def data_preparation(self):
        """
            Prepare your training and validation data to fine-tune your model. 
            Your training and validation data consist of input and output examples for how you would like the model to perform.
        """

        """ 
            Make sure all your training examples follow the expected format for inference. 
            To fine-tune models effectively, ensure a diverse dataset by maintaining data balance, 
            including various scenarios, and periodically refining training data to align with real-world expectations. 
            These actions ultimately lead to more accurate and balanced model responses.
        """
        pass


    def ensure_datasets(self):
        """
            This code snippet shows you how to define a training dataset.
            The next step provides options to configure the model to use validation data in the training process.
        """
        # Training Data
        try:
            self.ml_client.data.get(self.train_dataset_name, version = self.dataset_version)
            print(f"Dataset {self.train_dataset_name}:{self.dataset_version} already exists")
        except:
            print("creating dataset")
            train_data = Data(
                path= self.training_data_path,
                type=AssetTypes.URI_FILE,
                description="Training dataset",
                name= self.train_dataset_name,
                version= self.dataset_version,
            )
            self.ml_client.data.create_or_update(train_data)

        # Validation Data
        try:
            self.ml_client.data.get(self.validation_dataset_name, version= self.dataset_version)
            print(f"Dataset {self.validation_dataset_name} already exists")
        except:
            print("creating dataset")
            validation_data = Data(
                path= self.validation_data_path,
                type=AssetTypes.URI_FILE,
                description="Validation dataset",
                name= self.validation_dataset_name,
                version="1",
            )
            self.ml_client.data.create_or_update(validation_data)

        return


    def subscribe_to_marketplace(self, base_model_asset, normalized_model_name):
        """
            This step is required for all non-Microsoft models.
            Example of a Microsoft model is the Phi family of models.
        """
        model_id_to_subscribe = "/".join(base_model_asset.id.split("/")[:-2])
        normalized_model_name = model_id_to_subscribe.replace(".", "-")

        marketplace_subscription = MarketplaceSubscription(
            model_id = model_id_to_subscribe,
            name = f"{normalized_model_name}-sub",
        )

        # note: this will throw exception if the subscription already exists or subscription is not required (for example, if the model is not in the marketplace like Phi family)
        try:
            marketplace_subscription = (
                self.ml_client.marketplace_subscriptions.begin_create_or_update(
                    marketplace_subscription
                ).result()
            )
        except Exception as ex:
            print(ex)


    def submit_finetune_job(self, base_model_asset, task=FineTuningTaskType.CHAT_COMPLETION):
        """
            There are following set of parameters that are required to fine-tune your model. 
            Each parameter is defined in the following:
                model: Base model to fine-tune.
                training_data: Training data for fine-tuning the base model.
                validation_data: Validation data for fine-tuning the base model.
                task: Fine-tuning task to perform. eg. CHAT_COMPLETION for chat-completion fine-tuning jobs.
                outputs: Output registered model name.

            The following parameters are optional:
                hyperparameters: Parameters that control the fine-tuning behavior at run-time.
                name: Fine-tuning job name
                experiment_name: Experiment name for fin-tuning job.
                display_name: Fine-tuning job display name.
        """        
        pass
        normalized = base_model_asset.name.replace(".", "-")
        job_display = f"{normalized}-display-{self.short_guid}"
        job_name = f"{normalized}-job-{self.short_guid}"
        output_prefix = f"{normalized}-{self.short_guid}-ft"
        experiment_name = f"{normalized}-exp"
        
        train_id = self.ml_client.data.get(self.train_dataset_name, self.dataset_version).id
        val_id   = self.ml_client.data.get(self.validation_dataset_name, self.dataset_version).id

        finetuning_job = create_finetuning_job(
            task = task,
            model = base_model_asset.id,
            training_data = train_id,
            validation_data = val_id,
            hyperparameters = {
                "per_device_train_batch_size": "1",
                "learning_rate": "0.00002",
                "num_train_epochs": "1",
            },
            display_name = job_display,
            name = job_name,
            experiment_name = experiment_name,
            tags={"name": "mslearn-finetuning"},
            properties={"owner": "finetuning-sdk"},
            output_model_name_prefix = output_prefix            
        )

        created_job = self.ml_client.jobs.create_or_update(finetuning_job)
        self.ml_client.jobs.get(created_job.name)

        status = self.ml_client.jobs.get(created_job.name).status

        while True:
            status = self.ml_client.jobs.get(created_job.name).status
            print(f"Current job status: {status}")
            if status in ["Failed", "Completed", "Canceled"]:
                print("Job has finished with status: {0}".format(status))
                break
            else:
                print("Job is still running. Checking again in 30 seconds.")
                time.sleep(30)

        registered_model = created_job.outputs["registered_model"]["name"]
        model = self.ml_client.models.get(registered_model, version="1")
        self.finetuned_model_name = model.name
        self.finetuned_model_version = model.version
        return model
    

    def deploy_serverless(self, custom_model):
        """
            Deploy the model as a serverless endpoint
        """
        try:
            if not custom_model:
                raise Exception(f"Custom/FineTuned Model was not shared")

            if not self.deployed_endpoint:
                self.deployed_endpoint = f"{custom_model.name}-ft-{self.short_guid}"

            ep = ServerlessEndpoint(name = self.deployed_endpoint, model_id = custom_model.id)
            self.created_endpoint = self.ml_client.serverless_endpoints.begin_create_or_update(ep).result()
        except:
            raise ValueError(f"For the model : {self.created_endpoint}")
        

    def deploy_realtime_endpoints(self, custom_model):
        try:
            if not custom_model:
                raise Exception(f"Custom/FineTuned Model was not shared")

            if not self.deployed_endpoint:
                self.deployed_endpoint = f"{custom_model.name}-ft-{self.short_guid}"
                
            # create endpoint object
            endpoint = ManagedOnlineEndpoint(
                name= self.deployed_endpoint,
                auth_mode="key",    # could also be 'aad_token'
                description="Realtime endpoint for fine-tuned model"
            )

            # register endpoint
            self.ml_client.online_endpoints.begin_create_or_update(endpoint).result()

            # point deployment at your fine-tuned model
            deployment = ManagedOnlineDeployment(
                name="blue",                       # deployment name
                endpoint_name= self.deployed_endpoint,
                model=custom_model.id,             # your fine-tuned model's ID
                instance_type="Standard_F8s_v2",   # choose SKU; adjust for GPU if needed
                instance_count=1
            )

            self.ml_client.online_deployments.begin_create_or_update(deployment).result()

            # set this deployment as the default
            self.ml_client.online_endpoints.begin_update(self.deployed_endpoint, traffic={"blue": 100}).result()

            return endpoint, deployment
        except:
            raise ValueError(f"Endpoint Deployment failed")
    


    def invoke(self, message: str, serverless: bool):
        """
            After our custom model deploys, we can use it like any other deployed model. 
            We can continue to use the same parameters with custom model, such as temperature and max_tokens, 
            as we can with other deployed models.
        """
        if serverless:
            endpoint = self.ml_client.serverless_endpoints.get(self.deployed_endpoint)
            endpoint_keys = self.ml_client.serverless_endpoints.get_keys(self.deployed_endpoint)
            auth_key = endpoint_keys.primary_key
        else:
            endpoint = self.ml_client.online_endpoints.get(self.deployed_endpoint)
            endpoint_keys = self.ml_client.online_endpoints.get_keys(self.deployed_endpoint)
            auth_key = endpoint_keys.primary_key

        url = f"{endpoint.scoring_uri}/v1/chat/completions"

        payload = {
            "max_tokens": 1024,
            "messages": [
                {   "role": "user",
                    "content": message,
                }
            ],
        }
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {auth_key}",
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        response.raise_for_status()
        return response.json()
    

if __name__ == "__main__":
    llm_service = FineTuneLLM()

    llm_service.get_client()

    model_name = os.getenv('MODEL_NAME_FOR_FINETUNING')

    model_to_finetune = llm_service.registry.models.get(model_name, label="latest")
    
    llm_service.ensure_datasets()

    finetuned_model = llm_service.submit_finetune_job(base_model_asset= model_to_finetune)

    if os.getenv("SERVERLESS"):
        llm_service.deploy_serverless(custom_model= finetuned_model)
        message="This script is great so far. Can you add more dialogue between Amanda and Thierry to build up their chemistry and connection?"
        print(llm_service.invoke(message= message), serverless = True)
    else:
        llm_service.deployed_endpoint = "fine-tune-llm-inference-fthjk"
        endpoint, deployment = llm_service.deploy_realtime_endpoints(custom_model= finetuned_model)
        message="This script is great so far. Can you add more dialogue between Amanda and Thierry to build up their chemistry and connection?"
        print(llm_service.invoke(message= message, serverless= False))