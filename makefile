GCP_PROJECT=thequickbrownfox
FUNCTION=recent_playlist

install:
	pip install -r requirements.txt
dev:
	ENV=dev \
	functions-framework-python --target $(FUNCTION) --debug
deploy:
	gcloud config set project $(GCP_PROJECT)
	gcloud config set run/region us-central1
	gcloud functions deploy recent_playlist \
		--runtime python39 \
		--env-vars-file .env.yaml \
		--trigger-http \
		--allow-unauthenticated 
