# Plugins for Kubernetes

Processed releases: xrally-kubernetes 1.0.0 - 1.0.0

## Environment Component

### Platform

#### existing [Platform]

Default plugin for Kubernetes.

**Create a spec based on system environment.**

The environment variables could be defined with two mutually exclusive
mandatory ways: check kubeconfig file or kubeconfig envvar, defining
certificates or defining auth token.

To search configuration in kubeconfig file, rally checks standard
`$HOME/.kube/config` file or get `KUBECONFIG` envvar.

To define certificates to connect next variables used:

The URL to the Kubernetes host.
.. envvar:: KUBERNETES_TLS_INSECURE
Not to verify the host against a CA certificate.
.. envvar:: KUBERNETES_CERT_AUTH
A path to a file containing TLS certificate to use when
connecting to the Kubernetes host.
.. envvar:: KUBERNETES_CLIENT_CERT
A path to a file containing client certificate to use when
connecting to the Kubernetes host.
.. envvar:: KUBERNETES_CLIENT_KEY
A path to a file containing client key to use when connecting to
the Kubernetes host.

To define auth token to connect next variables used:

The URL to the Kubernetes host.
.. envvar:: KUBERNETES_CERT_AUTH
A path to a file containing TLS certificate to use when
connecting to the Kubernetes host.
.. envvar:: KUBERNETES_API_KEY
Client API key to use as token when connecting to the Kubernetes
host.
.. envvar:: KUBERNETES_API_KEY_PREFIX
Client API key prefix to use in token when connecting to the
Kubernetes host.

__Platform__: kubernetes

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "object", 
            "oneOf": [
                {
                    "description": "The auth-token authentication", 
                    "properties": {
                        "api_key": {
                            "type": "string", 
                            "description": "API key for API key authorization"
                        }, 
                        "api_key_prefix": {
                            "type": "string", 
                            "description": "API key prefix. Defaults to 'Bearer'."
                        }, 
                        "certificate-authority": {
                            "type": "string", 
                            "description": "Path to certificate authority"
                        }, 
                        "server": {
                            "type": "string", 
                            "description": "An endpoint of Kubernetes API."
                        }
                    }, 
                    "additionalProperties": false, 
                    "required": [
                        "server", 
                        "certificate-authority", 
                        "api_key"
                    ]
                }, 
                {
                    "description": "The authentication via client certificates.", 
                    "properties": {
                        "certificate-authority": {
                            "type": "string", 
                            "description": "Path to certificate authority"
                        }, 
                        "client-certificate": {
                            "type": "string", 
                            "description": "Path to client's certificate."
                        }, 
                        "client-key": {
                            "type": "string", 
                            "description": "Path to client's key."
                        }, 
                        "server": {
                            "type": "string", 
                            "description": "An endpoint of Kubernetes API."
                        }, 
                        "tls_insecure": {
                            "type": "boolean", 
                            "description": "Whether skip or not tls verification. Defaults to False."
                        }
                    }, 
                    "additionalProperties": false, 
                    "required": [
                        "server", 
                        "certificate-authority", 
                        "client-certificate", 
                        "client-key"
                    ]
                }
            ]
        }

__Module__: [xrally_kubernetes.env.platforms.existing](https://github.com/xrally/xrally-kubernetes/blob/master/xrally_kubernetes/env/platforms/existing.py)

<hr />

## Task Component

### Scenario

This is base class for any scenario.

All Scenario Plugins should be subclass of this class.

#### Kubernetes.create_and_delete_namespace [Scenario]

Create namespace, wait until it won't be active and then delete it.

__Platform__: kubernetes

<table>
  <caption>Parameters</caption>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKubernetescreate-and-delete-namespace-name"></a>name<a href="#ScenarioKubernetescreate-and-delete-namespace-name"> [ref]</a>
      </td>
      <td>namespace custom name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKubernetescreate-and-delete-namespace-status-wait"></a>status_wait<a href="#ScenarioKubernetescreate-and-delete-namespace-status-wait"> [ref]</a>
      </td>
      <td>wait namespace status after creation</td>
    </tr>
  </tbody>
</table>


__Module__: [xrally_kubernetes.tasks.scenarios.namespaces](https://github.com/xrally/xrally-kubernetes/blob/master/xrally_kubernetes/tasks/scenarios/namespaces.py)

<hr />

#### Kubernetes.list_namespaces [Scenario]

List cluster namespaces.

__Platform__: kubernetes

__Module__: [xrally_kubernetes.tasks.scenarios.namespaces](https://github.com/xrally/xrally-kubernetes/blob/master/xrally_kubernetes/tasks/scenarios/namespaces.py)

<hr />

### Validator

A base class for all validators.

#### required_kubernetes_platform [Validator]

Check for kubernetes platform in selected environment.

__Platform__: kubernetes

__Module__: [xrally_kubernetes.tasks.validators](https://github.com/xrally/xrally-kubernetes/blob/master/xrally_kubernetes/tasks/validators.py)

<hr />