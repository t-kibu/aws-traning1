# ちと古いのを承知で指定通り
FROM public.ecr.aws/lambda/python:3.9

# lessを入れる
RUN apt-get update
RUN apt-get install -y less

# イメージの設定、Macなのでarm64としておく
FROM --platform=linux/arm64 base as stage-arm64

# CLIとSessionManagerとSAM CLIのインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update && \
    rm -rf awscliv2.zip
RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_arm64/session-manager-plugin.deb" -o "session-manager-plugin.deb" && \
  apt-get install -y ./session-manager-plugin.deb && \
    rm -f session-manager-plugin.deb
RUN curl -LO "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-arm64.zip" && \
    unzip aws-sam-cli-linux-arm64.zip -d sam-installation && \
    ./sam-installation/install && \
    rm -rf aws-sam-cli-linux-arm64.zip sam-installation

# amd64系の処理。Mac以外ならこっち
# FROM --platform=linux/amd64 base as stage-amd64

# RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# RUN curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb

COPY app.py requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt -t .


# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
