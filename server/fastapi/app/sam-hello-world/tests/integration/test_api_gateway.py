import os

import boto3
import pytest
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test.
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')
        # クライアント取得時には明示的にリージョンを指定する(ここでは簡易的にベタ書きだが本来は環境変数にしておく)
        client = boto3.client("cloudformation", region_name="ap-northeast-1")
        print(f"Region: {os.environ.get('AWS_DEFAULT_REGION')}")
        print(f"Stack name: {stack_name}")


        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "HelloWorldApi"]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack output

    def test_root(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.get(api_gateway_url + "/hello")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello SAM World"}


    def test_get_item(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.get(api_gateway_url + "/item?id=ABC")

        assert response.status_code == 200
        assert response.json() == {"id":"ABC","name":"get_item+ABC","description":"get_item+ABC","price":100.0}


    def test_post_item(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        request_url = api_gateway_url + "/item"
        headers = {"Content-Type" : "application/json"}
        json_data = {"name": "post_item","description":"post_item","price":200.0}
        response = requests.post(request_url, headers=headers, json=json_data)
        del_id_res = response.json()
        print(del_id_res)
        del del_id_res["id"]
        assert response.status_code == 201
        assert del_id_res == {"name": "post_item","description":"post_item","price":200.0}


    def test_put_item(self, api_gateway_url):
      """ Call the API Gateway endpoint and check the response """
      response = requests.put(api_gateway_url + "/item/9")

      assert response.status_code == 201
      assert response.json == {"id": "9", "name": "put_item+9","description":"put_item+9","price":300.0}
