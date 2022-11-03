#!/usr/bin/env python3
import argparse
import json
import urllib.parse
from collections import defaultdict
from oic.oic import Client, RegistrationResponse
from oic.oic.message import AuthorizationResponse, AuthorizationErrorResponse
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic import rndstr
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/":
            self._handle_initial()
        elif url.path.startswith("/callback/"):
            self._handle_callback()
        else:
            self.return_redirect("/")

    def _handle_initial(self):
        global session

        # setup oic code flow
        session["state"] = rndstr()
        session["nonce"] = rndstr()
        auth_req = client.construct_AuthorizationRequest(
            request_args={
                "response_type": "code",
                "scope": " ".join(cmd_args.scope),
                "state": session["state"],
                "nonce": session["nonce"],
                "redirect_uri": f"http://{self.server.server_address[0]}:{self.server.server_address[1]}/callback/",
            }
        )
        login_url = auth_req.request(client.authorization_endpoint)

        # send response
        self.return_redirect(login_url)

    def _handle_callback(self):
        global session

        # parse callback
        auth_response = client.parse_response(
            AuthorizationResponse, info=self.path, sformat="urlencoded"
        )
        if auth_response["state"] != session["state"]:
            self.send_error(
                HTTPStatus.BAD_REQUEST,
                "invalid state",
                explain="The state of the callback does not match in-memory state",
            )
            return
        if isinstance(auth_response, AuthorizationErrorResponse):
            self.send_error(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                auth_response["error"],
                explain=auth_response["error_description"],
            )
            return

        # exchange received code for proper access and refresh tokens
        token_response = client.do_access_token_request(
            scope=cmd_args.scope,
            state=session["state"],
            request_args={"code": auth_response["code"]},
        )
        # retrieve user information with newly received access token
        userinfo = client.do_user_info_request(
            state=session["state"], scope=cmd_args.scope
        )

        # output data
        self.return_json_response(
            {
                "token_response": token_response.to_dict(),
                "userinfo": userinfo.to_dict(),
            }
        )
        print("===============================================================")
        print(f"token_type: {token_response.get('token_type')}")
        print("access_token:")
        print(token_response.get("access_token"))
        print("===============================================================")

    def return_redirect(self, to: str, code: int = HTTPStatus.FOUND):
        self.send_response(code)
        self.send_header("location", to)
        self.end_headers()

    def return_json_response(self, content: dict):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(content).encode("UTF-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "get_tokens", description="Retrieves access and id tokens from Mafiasi Identity"
    )
    parser.add_argument(
        "--issuer",
        help="OpenId Connect issuer. Defaults to Mafiasi",
        default="https://identity.mafiasi.de/auth/realms/mafiasi",
    )
    parser.add_argument(
        "--client-id",
        help="OpenId Connect client id. Defaults to dev-client",
        default="dev-client",
    )
    parser.add_argument(
        "--client-secret",
        help="OpenId Connect client secret. Defaults to dev-client's secret",
        default="bb0c83bc-1dd9-4946-a074-d452bc1fb830",
    )
    parser.add_argument(
        "--scope",
        help="OpenID scopes to request",
        action="append",
        default=["openid", "dev-scope", "profile", "email"],
    )
    cmd_args = parser.parse_args()

    # initialize openid client
    client = Client(
        client_id=cmd_args.client_id, client_authn_method=CLIENT_AUTHN_METHOD
    )
    client.provider_config(cmd_args.issuer)
    client.store_registration_info(
        RegistrationResponse(
            client_id=cmd_args.client_id, client_secret=cmd_args.client_secret
        )
    )

    # initialize a session object (which is very primitive but works)
    session = defaultdict(lambda: "")

    # serve a basic http server so that authorization code flow can be used
    with HTTPServer(("127.0.0.1", 8080), RequestHandler) as server:
        print(f"Open http://{server.server_name}:{server.server_port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
