all: build
push: push
.PHONY: push build

# To bump the Zeppelin version, bump the version in
# zeppelin/Dockerfile and bump this tag and reset to v1.
TAG = 1.1.13
PROJECT_NAME = k8s-controller

build:
	docker build -t projectepic/$(PROJECT_NAME) .
	docker tag projectepic/$(PROJECT_NAME) projectepic/$(PROJECT_NAME):$(TAG)

push: build
	docker push projectepic/$(PROJECT_NAME)
	docker push projectepic/$(PROJECT_NAME):$(TAG)

clean:
	docker rmi projectepic/$(PROJECT_NAME):$(TAG) || :
	docker rmi projectepic/$(PROJECT_NAME) || :
