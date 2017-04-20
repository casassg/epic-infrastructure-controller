FROM python:3.6-alpine

ADD requirements.txt /
RUN pip install -r requirements.txt
ADD play.py /
ADD k8scontroller.py /
RUN mkdir /k8sdeployments
ADD k8sdeployments /k8sdeployments


ENTRYPOINT ["python", "./play.py"]