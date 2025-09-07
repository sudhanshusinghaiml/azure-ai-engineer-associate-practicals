### Content flag definitions
1. The "adult" classification contains several different categories:
    - Adult images are explicitly sexual in nature and often show nudity and sexual acts.
    - Racy images are sexually suggestive in nature and often contain less sexually explicit content than images tagged as 
    Adult.
    - Gory images show blood/gore.

2. Use the API
    - You can detect adult content with the Analyze Image 3.2 API. 
    - When you add the value of Adult to the visualFeatures query parameter, the API returns three boolean properties — isAdultContent, isRacyContent, and isGoryContent — in its JSON response. 
    - The method also returns corresponding properties — adultScore, racyScore, and goreScore — which represent confidence scores between zero and one for each respective category.