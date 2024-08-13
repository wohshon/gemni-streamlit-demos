
### Demo app to test out gemini model

`streamlit run main.py --server.port 8080`

Assumption, this runs in an env with GCP credentials setup to call vertex ai 

```
pip install --upgrade google-cloud-aiplatform
pip install --upgrade streamlit
```

for the Catalog Management demo, a vector database is required for
recommendation of categories.

//TODO 


References
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/sdk-for-gemini/gemini-sdk-overview-reference
- https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models#gemini-models
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini
