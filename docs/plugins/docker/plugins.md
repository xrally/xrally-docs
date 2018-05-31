# Plugins for Docker

Processed releases: xrally-docker 1.0.0 - 1.0.0

## Environment Component

### Platform

#### existing [Platform]

Default plugin for Docker.

__Platform__: docker

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "object", 
            "properties": {
                "cert_path": {
                    "type": "string", 
                    "description": "A path to a directory containing TLS certificates to use when connecting to the Docker host."
                }, 
                "host": {
                    "type": "string", 
                    "description": "The URL to the Docker host"
                }, 
                "ssl_version": {
                    "type": "integer", 
                    "description": "A valid SSL version (see https://docs.python.org/3.5/library/ssl.html#ssl.PROTOCOL_TLSv1)"
                }, 
                "timeout": {
                    "type": "number", 
                    "description": "Default timeout for API calls, in seconds.", 
                    "minimum": 0
                }, 
                "tls_verify": {
                    "type": "boolean", 
                    "description": "Verify the host against a CA certificate."
                }, 
                "version": {
                    "type": "string", 
                    "description": "The version of the API to use. Defaults to ``auto`` whichmeans automatically detection of the server's version."
                }
            }, 
            "additionalProperties": false
        }

__Module__: [xrally_docker.env.platforms.existing](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/env/platforms/existing.py)

<hr />

## Task Component

### Context

#### images [Context]

Pull new images or load existing ones.

__Platform__: docker

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "object", 
            "properties": {
                "existing": {
                    "type": "boolean", 
                    "description": "Load all existing images"
                }, 
                "names": {
                    "type": "array", 
                    "description": "Pull images from the list.", 
                    "items": {
                        "type": "string", 
                        "description": "The image to pull. (if the tag of image is not specified, 'latest' will be used)."
                    }
                }
            }, 
            "additionalProperties": false
        }

__Module__: [xrally_docker.task.contexts.images](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/contexts/images.py)

<hr />

#### networks [Context]

Create one or several docker networks.

__Platform__: docker

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "oneOf": [
                {
                    "description": "Create a single network", 
                    "$ref": "#/definitions/single-network"
                }, 
                {
                    "type": "array", 
                    "description": "Create several networks.", 
                    "items": {
                        "$ref": "#/definitions/single-network"
                    }, 
                    "minItems": 1
                }
            ], 
            "definitions": {
                "ipam": {
                    "type": "object", 
                    "description": "Custom IP scheme for the network", 
                    "properties": {
                        "Config": {
                            "type": "array", 
                            "description": "A list of IPAM Pool configurations.", 
                            "items": {
                                "type": "object", 
                                "properties": {
                                    "aux_addresses": {
                                        "type": "object", 
                                        "description": "A dictionary of ``key -> ip_address``relationships specifying auxiliary addresses that need to be allocated by the IPAM driver."
                                    }, 
                                    "gateway": {
                                        "type": "string", 
                                        "description": "Custom IP address for the pool's gateway."
                                    }, 
                                    "iprange": {
                                        "type": "string", 
                                        "description": "Custom IP range for endpoints in this IPAM pool using the CIDR notation."
                                    }, 
                                    "subnet": {
                                        "type": "string", 
                                        "description": "Custom subnet for this IPAM pool using the CIDR notation."
                                    }
                                }, 
                                "additionalProperties": false
                            }
                        }, 
                        "Driver": {
                            "type": "string", 
                            "description": "The name of the driver"
                        }, 
                        "Options": {
                            "type": "object", 
                            "description": "Driver options.", 
                            "additionalProperties": true
                        }
                    }, 
                    "additionalProperties": false, 
                    "required": [
                        "Driver"
                    ]
                }, 
                "single-network": {
                    "type": "object", 
                    "properties": {
                        "attachable": {
                            "type": "boolean", 
                            "description": "If enabled, and the network is in the global scope,  non-service containers on worker nodes will be able to connect to the network."
                        }, 
                        "driver": {
                            "type": "string", 
                            "description": "Name of the driver used to create the network"
                        }, 
                        "enable_ipv6": {
                            "type": "boolean", 
                            "description": "Enable IPv6 on the network."
                        }, 
                        "ingress": {
                            "type": "boolean", 
                            "description": "If set, create an ingress network which provides the routing-mesh in swarm mode."
                        }, 
                        "internal": {
                            "type": "boolean", 
                            "description": "Restrict external access to the network."
                        }, 
                        "ipam": {
                            "$ref": "#/definitions/ipam"
                        }, 
                        "labels": {
                            "type": "array", 
                            "description": "A list of labels to apply to the network", 
                            "items": {
                                "type": "string", 
                                "description": "A label to apply."
                            }
                        }, 
                        "options": {
                            "type": "object", 
                            "description": "Driver options."
                        }, 
                        "scope": {
                            "description": "The network's scope", 
                            "enum": [
                                "local", 
                                "global", 
                                "swarm"
                            ]
                        }
                    }, 
                    "additionalProperties": false
                }
            }
        }

__Module__: [xrally_docker.task.contexts.networks](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/contexts/networks.py)

<hr />

### Scenario

This is base class for any scenario.

All Scenario Plugins should be subclass of this class.

#### Docker.create_and_delete_network [Scenario]

Create and delete docker network.

__Platform__: docker

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
        <a name="ScenarioDockercreate-and-delete-network-driver"></a>driver<a href="#ScenarioDockercreate-and-delete-network-driver"> [ref]</a>
      </td>
      <td>Name of the driver used to create the network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-options"></a>options<a href="#ScenarioDockercreate-and-delete-network-options"> [ref]</a>
      </td>
      <td>Driver options as a key-value dictionary
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-ipam"></a>ipam<a href="#ScenarioDockercreate-and-delete-network-ipam"> [ref]</a>
      </td>
      <td>Optional custom IP scheme for the network.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-check-duplicate"></a>check_duplicate<a href="#ScenarioDockercreate-and-delete-network-check-duplicate"> [ref]</a>
      </td>
      <td>Request daemon to check for networks with
same name.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-internal"></a>internal<a href="#ScenarioDockercreate-and-delete-network-internal"> [ref]</a>
      </td>
      <td>Restrict external access to the network.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-labels"></a>labels<a href="#ScenarioDockercreate-and-delete-network-labels"> [ref]</a>
      </td>
      <td>Map of labels to set on the network.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-enable-ipv6"></a>enable_ipv6<a href="#ScenarioDockercreate-and-delete-network-enable-ipv6"> [ref]</a>
      </td>
      <td>Enable IPv6 on the network.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-attachable"></a>attachable<a href="#ScenarioDockercreate-and-delete-network-attachable"> [ref]</a>
      </td>
      <td>If enabled, and the network is in the global
scope,  non-service containers on worker nodes will be able to
connect to the network.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-scope"></a>scope<a href="#ScenarioDockercreate-and-delete-network-scope"> [ref]</a>
      </td>
      <td>Specify the network's scope (``local``, ``global`` or
``swarm``)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockercreate-and-delete-network-ingress"></a>ingress<a href="#ScenarioDockercreate-and-delete-network-ingress"> [ref]</a>
      </td>
      <td>If set, create an ingress network which provides
the routing-mesh in swarm mode.
</td>
    </tr>
  </tbody>
</table>


__Module__: [xrally_docker.task.scenarios.networks](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/scenarios/networks.py)

<hr />

#### Docker.list_networks [Scenario]

List docker networks.

__Platform__: docker

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
        <a name="ScenarioDockerlist-networks-driver"></a>driver<a href="#ScenarioDockerlist-networks-driver"> [ref]</a>
      </td>
      <td>a network driver to match
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockerlist-networks-label"></a>label<a href="#ScenarioDockerlist-networks-label"> [ref]</a>
      </td>
      <td>label to match
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockerlist-networks-ntype"></a>ntype<a href="#ScenarioDockerlist-networks-ntype"> [ref]</a>
      </td>
      <td>Filters networks by type.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockerlist-networks-detailed"></a>detailed<a href="#ScenarioDockerlist-networks-detailed"> [ref]</a>
      </td>
      <td>Grep detailed information about networks (aka greedy)</td>
    </tr>
  </tbody>
</table>


__Module__: [xrally_docker.task.scenarios.networks](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/scenarios/networks.py)

<hr />

#### Docker.run_container [Scenario]

Run a docker container from image and execute a command in it.

__Platform__: docker

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
        <a name="ScenarioDockerrun-container-image-name"></a>image_name<a href="#ScenarioDockerrun-container-image-name"> [ref]</a>
      </td>
      <td>The name of image to start
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioDockerrun-container-command"></a>command<a href="#ScenarioDockerrun-container-command"> [ref]</a>
      </td>
      <td>The command to launch in container</td>
    </tr>
  </tbody>
</table>


__Module__: [xrally_docker.task.scenarios.container](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/scenarios/container.py)

<hr />

### Validator

A base class for all validators.

#### check_cleanup_resources [Validator]

Validates that docker resource managers exist.

__Platform__: docker

__Module__: [xrally_docker.task.contexts.cleanup](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/contexts/cleanup.py)

<hr />

#### required_docker_platform [Validator]

Check for docker platform in selected environment.

__Platform__: docker

__Module__: [xrally_docker.task.validators](https://github.com/xrally/xrally-docker/blob/master/xrally_docker/task/validators.py)

<hr />