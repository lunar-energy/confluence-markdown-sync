FROM python:3.14-alpine

WORKDIR /action

# Inside a single-purpose container there is no user to drop to and no venv to
# use, so pip's root warning and version notice are just noise in the build log.
ENV PIP_ROOT_USER_ACTION=ignore \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1

COPY ./Pipfile* ./
RUN pip install pipenv && \
  pipenv install --system --deploy && \
  pipenv --clear

COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
