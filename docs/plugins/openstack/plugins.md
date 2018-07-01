# Plugins for OpenStack

Processed releases: rally-openstack 1.0.0 - 1.2.0

## Environment Component

### Platform

#### existing [Platform]

Default plugin for OpenStack platform.

It may be used to test any existing OpenStack API compatible cloud.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "object", 
            "properties": {
                "admin": {
                    "$ref": "#/definitions/user"
                }, 
                "auth_url": {
                    "type": "string"
                }, 
                "endpoint": {
                    "type": [
                        "string", 
                        "null"
                    ]
                }, 
                "endpoint_type": {
                    "enum": [
                        "public", 
                        "internal", 
                        "admin", 
                        null
                    ]
                }, 
                "https_cacert": {
                    "type": "string"
                }, 
                "https_insecure": {
                    "type": "boolean"
                }, 
                "profiler_conn_str": {
                    "type": [
                        "string", 
                        "null"
                    ]
                }, 
                "profiler_hmac_key": {
                    "type": [
                        "string", 
                        "null"
                    ]
                }, 
                "region_name": {
                    "type": "string"
                }, 
                "users": {
                    "type": "array", 
                    "items": {
                        "$ref": "#/definitions/user"
                    }, 
                    "minItems": 1
                }
            }, 
            "additionalProperties": false, 
            "anyOf": [
                {
                    "description": "The case when the admin is specified and the users can be created via 'users@openstack' context or 'existing_users' will be used.", 
                    "required": [
                        "admin", 
                        "auth_url"
                    ]
                }, 
                {
                    "description": "The case when the only existing users are specified.", 
                    "required": [
                        "users", 
                        "auth_url"
                    ]
                }
            ], 
            "definitions": {
                "user": {
                    "type": "object", 
                    "oneOf": [
                        {
                            "description": "Keystone V2.0", 
                            "properties": {
                                "password": {
                                    "type": "string"
                                }, 
                                "tenant_name": {
                                    "type": "string"
                                }, 
                                "username": {
                                    "type": "string"
                                }
                            }, 
                            "additionalProperties": false, 
                            "required": [
                                "username", 
                                "password", 
                                "tenant_name"
                            ]
                        }, 
                        {
                            "description": "Keystone V3.0", 
                            "properties": {
                                "domain_name": {
                                    "type": "string"
                                }, 
                                "password": {
                                    "type": "string"
                                }, 
                                "project_domain_name": {
                                    "type": "string"
                                }, 
                                "project_name": {
                                    "type": "string"
                                }, 
                                "user_domain_name": {
                                    "type": "string"
                                }, 
                                "username": {
                                    "type": "string"
                                }
                            }, 
                            "additionalProperties": false, 
                            "required": [
                                "username", 
                                "password", 
                                "project_name"
                            ]
                        }
                    ]
                }
            }
        }

__Module__: [rally_openstack.platforms.existing](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/platforms/existing.py)

<hr />

## Task Component

### Chart

Base class for charts.

This is a base for all plugins that prepare data for specific charts
in HTML report. Each chart must at least declare chart widget and
prepare data that is suitable for rendering by JavaScript.

#### OSProfiler [Chart]

osprofiler content.

This plugin complete data of osprofiler

__Platform__: default

__Module__: [rally_openstack.embedcharts.osprofilerchart](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/embedcharts/osprofilerchart.py)

<hr />

### Context

#### allow_ssh [Context]

Sets up security groups for all users to access VM via SSH.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "null"
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.network.allow_ssh](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/network/allow_ssh.py)

<hr />

#### api_versions [Context]

Context for specifying OpenStack clients versions and service types.

Some OpenStack services support several API versions. To recognize
the endpoints of each version, separate service types are provided in
Keystone service catalog.

Rally has the map of default service names - service types. But since
service type is an entity, which can be configured manually by admin(
via keystone api) without relation to service name, such map can be
insufficient.

Also, Keystone service catalog does not provide a map types to name
(this statement is true for keystone < 3.3 ).

This context was designed for not-default service types and not-default
API versions usage.

An example of specifying API version:

```json
# In this example we will launch NovaKeypair.create_and_list_keypairs
# scenario on 2.2 api version.
{
    "NovaKeypair.create_and_list_keypairs": [
        {
            "args": {
                "key_type": "x509"
            },
            "runner": {
                "type": "constant",
                "times": 10,
                "concurrency": 2
            },
            "context": {
                "users": {
                    "tenants": 3,
                    "users_per_tenant": 2
                },
                "api_versions": {
                    "nova": {
                        "version": 2.2
                    }
                }
            }
        }
    ]
}
```

An example of specifying API version along with service type:

```json
# In this example we will launch CinderVolumes.create_and_attach_volume
# scenario on Cinder V2
{
    "CinderVolumes.create_and_attach_volume": [
        {
            "args": {
                "size": 10,
                "image": {
                    "name": "^cirros.*-disk$"
                },
                "flavor": {
                    "name": "m1.tiny"
                },
                "create_volume_params": {
                    "availability_zone": "nova"
                }
            },
            "runner": {
                "type": "constant",
                "times": 5,
                "concurrency": 1
            },
            "context": {
                "users": {
                    "tenants": 2,
                    "users_per_tenant": 2
                },
                "api_versions": {
                    "cinder": {
                        "version": 2,
                        "service_type": "volumev2"
                    }
                }
            }
        }
    ]
}
```

Also, it possible to use service name as an identifier of service endpoint,
but an admin user is required (Keystone can return map of service
names - types, but such API is permitted only for admin). An example:

```json
# Similar to the previous example, but `service_name` argument is used
# instead of `service_type`
{
    "CinderVolumes.create_and_attach_volume": [
        {
            "args": {
                "size": 10,
                "image": {
                    "name": "^cirros.*-disk$"
                },
                "flavor": {
                    "name": "m1.tiny"
                },
                "create_volume_params": {
                    "availability_zone": "nova"
                }
            },
            "runner": {
                "type": "constant",
                "times": 5,
                "concurrency": 1
            },
            "context": {
                "users": {
                    "tenants": 2,
                    "users_per_tenant": 2
                },
                "api_versions": {
                    "cinder": {
                        "version": 2,
                        "service_name": "cinderv2"
                    }
                }
            }
        }
    ]
}
```

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "patternProperties": {
                "^[a-z]+$": {
                    "type": "object", 
                    "oneOf": [
                        {
                            "description": "version only", 
                            "properties": {
                                "version": {
                                    "anyOf": [
                                        {
                                            "type": "string", 
                                            "description": "a string-like version."
                                        }, 
                                        {
                                            "type": "number", 
                                            "description": "a number-like version."
                                        }
                                    ]
                                }
                            }, 
                            "additionalProperties": false, 
                            "required": [
                                "version"
                            ]
                        }, 
                        {
                            "description": "version and service_name", 
                            "properties": {
                                "service_name": {
                                    "type": "string"
                                }, 
                                "version": {
                                    "anyOf": [
                                        {
                                            "type": "string", 
                                            "description": "a string-like version."
                                        }, 
                                        {
                                            "type": "number", 
                                            "description": "a number-like version."
                                        }
                                    ]
                                }
                            }, 
                            "additionalProperties": false, 
                            "required": [
                                "service_name"
                            ]
                        }, 
                        {
                            "description": "version and service_type", 
                            "properties": {
                                "service_type": {
                                    "type": "string"
                                }, 
                                "version": {
                                    "anyOf": [
                                        {
                                            "type": "string", 
                                            "description": "a string-like version."
                                        }, 
                                        {
                                            "type": "number", 
                                            "description": "a number-like version."
                                        }
                                    ]
                                }
                            }, 
                            "additionalProperties": false, 
                            "required": [
                                "service_type"
                            ]
                        }
                    ]
                }
            }, 
            "minProperties": 1, 
            "additionalProperties": false
        }

__Module__: [rally_openstack.contexts.api_versions](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/api_versions.py)

<hr />

#### audit_templates [Context]

Creates Watcher audit templates for tenants.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "audit_templates_per_admin": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "fill_strategy": {
                    "enum": [
                        "round_robin", 
                        "random", 
                        null
                    ]
                }, 
                "params": {
                    "type": "array", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "goal": {
                                "type": "object", 
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    }
                                }, 
                                "additionalProperties": false
                            }, 
                            "strategy": {
                                "type": "object", 
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    }
                                }, 
                                "additionalProperties": false
                            }
                        }, 
                        "additionalProperties": false
                    }, 
                    "minItems": 1, 
                    "uniqueItems": true
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "params"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.contexts.watcher.audit_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/watcher/audit_templates.py)

<hr />

#### ca_certs [Context]

Creates ca certs.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "directory": {
                    "type": "string"
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.magnum.ca_certs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/magnum/ca_certs.py)

<hr />

#### ceilometer [Context]

Creates ceilometer samples and resources.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "batch_size": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "batches_allow_lose": {
                    "type": "integer", 
                    "minimum": 0
                }, 
                "counter_name": {
                    "type": "string"
                }, 
                "counter_type": {
                    "type": "string"
                }, 
                "counter_unit": {
                    "type": "string"
                }, 
                "counter_volume": {
                    "type": "number", 
                    "minimum": 0
                }, 
                "metadata_list": {
                    "type": "array", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "created_at": {
                                "type": "string"
                            }, 
                            "deleted": {
                                "type": "string"
                            }, 
                            "name": {
                                "type": "string"
                            }, 
                            "status": {
                                "type": "string"
                            }
                        }, 
                        "additionalProperties": false
                    }
                }, 
                "resources_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "samples_per_resource": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "timestamp_interval": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "counter_name", 
                "counter_type", 
                "counter_unit", 
                "counter_volume"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.ceilometer.samples](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/ceilometer/samples.py)

<hr />

#### cluster_templates [Context]

Creates Magnum cluster template.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "coe": {
                    "type": "string"
                }, 
                "dns_nameserver": {
                    "type": "string"
                }, 
                "docker_storage_driver": {
                    "type": "string"
                }, 
                "docker_volume_size": {
                    "type": "integer"
                }, 
                "external_network_id": {
                    "type": "string"
                }, 
                "fixed_network": {
                    "type": "string"
                }, 
                "fixed_subnet": {
                    "type": "string"
                }, 
                "flavor_id": {
                    "type": "string"
                }, 
                "http_proxy": {
                    "type": "string"
                }, 
                "https_proxy": {
                    "type": "string"
                }, 
                "image_id": {
                    "type": "string"
                }, 
                "labels": {
                    "type": "string"
                }, 
                "master_flavor_id": {
                    "type": "string"
                }, 
                "master_lb_enabled": {
                    "type": "boolean"
                }, 
                "network_driver": {
                    "type": "string"
                }, 
                "no_proxy": {
                    "type": "string"
                }, 
                "public": {
                    "type": "boolean"
                }, 
                "registry_enabled": {
                    "type": "boolean"
                }, 
                "server_type": {
                    "type": "string"
                }, 
                "tls_disabled": {
                    "type": "boolean"
                }, 
                "volume_driver": {
                    "type": "string"
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "image_id", 
                "external_network_id", 
                "coe"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.magnum.cluster_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/magnum/cluster_templates.py)

<hr />

#### clusters [Context]

Creates specified amount of Magnum clusters.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "cluster_template_uuid": {
                    "type": "string"
                }, 
                "node_count": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.magnum.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/magnum/clusters.py)

<hr />

#### ec2_servers [Context]

Creates specified amount of nova servers in each tenant uses ec2 API.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "flavor": {
                    "type": "object", 
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "image": {
                    "type": "object", 
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "servers_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "image", 
                "flavor", 
                "servers_per_tenant"
            ]
        }

__Module__: [rally_openstack.contexts.ec2.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/ec2/servers.py)

<hr />

#### existing_network [Context]

This context supports using existing networks in Rally.

This context should be used on a deployment with existing users.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.network.existing_network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/network/existing_network.py)

<hr />

#### flavors [Context]

Context creates a list of flavors.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "array", 
            "items": {
                "type": "object", 
                "properties": {
                    "disk": {
                        "type": "integer", 
                        "minimum": 0
                    }, 
                    "ephemeral": {
                        "type": "integer", 
                        "minimum": 0
                    }, 
                    "extra_specs": {
                        "type": "object", 
                        "additionalProperties": {
                            "type": "string"
                        }
                    }, 
                    "name": {
                        "type": "string"
                    }, 
                    "ram": {
                        "type": "integer", 
                        "minimum": 1
                    }, 
                    "swap": {
                        "type": "integer", 
                        "minimum": 0
                    }, 
                    "vcpus": {
                        "type": "integer", 
                        "minimum": 1
                    }
                }, 
                "additionalProperties": false, 
                "required": [
                    "name", 
                    "ram"
                ]
            }
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.contexts.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/nova/flavors.py)

<hr />

#### heat_dataplane [Context]

Context class for create stack by given template.

This context will create stacks by given template for each tenant and
add details to context. Following details will be added:

- id of stack;
- template file contents;
- files dictionary;
- stack parameters;

Heat template should define a "gate" node which will interact with Rally
by ssh and workload nodes by any protocol. To make this possible heat
template should accept the following parameters:

- network_id: id of public network
- router_id: id of external router to connect "gate" node
- key_name: name of nova ssh keypair to use for "gate" node

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "context_parameters": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "files": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "parameters": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "stacks_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "template": {
                    "oneOf": [
                        {
                            "type": "string", 
                            "description": ""
                        }, 
                        {
                            "type": "array", 
                            "description": "", 
                            "items": {
                                "type": "string"
                            }, 
                            "minItems": 2, 
                            "maxItems": 2
                        }
                    ]
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.dataplane.heat](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/dataplane/heat.py)

<hr />

#### image_command_customizer [Context]

Context class for generating image customized by a command execution.

Run a command specified by configuration to prepare image.

Use this script e.g. to download and install something.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "command": {
                    "$ref": "#/definitions/commandDict"
                }, 
                "flavor": {
                    "type": "object", 
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "floating_network": {
                    "type": "string"
                }, 
                "image": {
                    "type": "object", 
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "internal_network": {
                    "type": "string"
                }, 
                "password": {
                    "type": "string"
                }, 
                "port": {
                    "type": "integer", 
                    "minimum": 1, 
                    "maximum": 65535
                }, 
                "userdata": {
                    "type": "string"
                }, 
                "username": {
                    "type": "string"
                }, 
                "workers": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "image", 
                "flavor"
            ], 
            "definitions": {
                "commandDict": {
                    "oneOf": [
                        {
                            "$ref": "#/definitions/scriptFile"
                        }, 
                        {
                            "$ref": "#/definitions/scriptInline"
                        }, 
                        {
                            "$ref": "#/definitions/commandPath"
                        }
                    ]
                }, 
                "commandPath": {
                    "type": "object", 
                    "properties": {
                        "command_args": {
                            "$ref": "#/definitions/stringOrStringList"
                        }, 
                        "local_path": {
                            "type": "string"
                        }, 
                        "remote_path": {
                            "$ref": "#/definitions/stringOrStringList"
                        }
                    }, 
                    "additionalProperties": false, 
                    "required": [
                        "remote_path"
                    ]
                }, 
                "scriptFile": {
                    "type": "object", 
                    "properties": {
                        "command_args": {
                            "$ref": "#/definitions/stringOrStringList"
                        }, 
                        "interpreter": {
                            "$ref": "#/definitions/stringOrStringList"
                        }, 
                        "script_file": {
                            "$ref": "#/definitions/stringOrStringList"
                        }
                    }, 
                    "additionalProperties": false, 
                    "required": [
                        "script_file", 
                        "interpreter"
                    ]
                }, 
                "scriptInline": {
                    "type": "object", 
                    "properties": {
                        "command_args": {
                            "$ref": "#/definitions/stringOrStringList"
                        }, 
                        "interpreter": {
                            "$ref": "#/definitions/stringOrStringList"
                        }, 
                        "script_inline": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false, 
                    "required": [
                        "script_inline", 
                        "interpreter"
                    ]
                }, 
                "stringOrStringList": {
                    "anyOf": [
                        {
                            "type": "string", 
                            "description": "just a string"
                        }, 
                        {
                            "type": "array", 
                            "description": "just a list of strings", 
                            "items": {
                                "type": "string"
                            }
                        }
                    ]
                }
            }
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.vm.image_command_customizer](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/vm/image_command_customizer.py)

<hr />

#### images [Context]

Uploads specified Glance images to every tenant.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "container_format": {
                    "description": "Format of the image container.", 
                    "enum": [
                        "aki", 
                        "ami", 
                        "ari", 
                        "bare", 
                        "docker", 
                        "ova", 
                        "ovf"
                    ]
                }, 
                "disk_format": {
                    "description": "The format of the disk.", 
                    "enum": [
                        "qcow2", 
                        "raw", 
                        "vhd", 
                        "vmdk", 
                        "vdi", 
                        "iso", 
                        "aki", 
                        "ari", 
                        "ami"
                    ]
                }, 
                "image_args": {
                    "type": "object", 
                    "description": "This param is deprecated since Rally-0.10.0, specify exact arguments in a root section of context instead.", 
                    "additionalProperties": true
                }, 
                "image_container": {
                    "type": "string", 
                    "description": "This param is deprecated since Rally-0.10.0, use `container_format` instead."
                }, 
                "image_name": {
                    "type": "string", 
                    "description": "The name of image to create. NOTE: it will be ignored in case when `images_per_tenant` is bigger then 1."
                }, 
                "image_type": {
                    "description": "This param is deprecated since Rally-0.10.0, use `disk_format` instead.", 
                    "enum": [
                        "qcow2", 
                        "raw", 
                        "vhd", 
                        "vmdk", 
                        "vdi", 
                        "iso", 
                        "aki", 
                        "ari", 
                        "ami"
                    ]
                }, 
                "image_url": {
                    "type": "string", 
                    "description": "Location of the source to create image from."
                }, 
                "images_per_tenant": {
                    "type": "integer", 
                    "description": "The number of images to create per one single tenant.", 
                    "minimum": 1
                }, 
                "min_disk": {
                    "type": "integer", 
                    "description": "Amount of disk space in GB", 
                    "minimum": 0
                }, 
                "min_ram": {
                    "type": "integer", 
                    "description": "Amount of RAM in MB", 
                    "minimum": 0
                }, 
                "visibility": {
                    "description": "Visibility for this image ('shared' and 'community' are available only in case of Glance V2).", 
                    "enum": [
                        "public", 
                        "private", 
                        "shared", 
                        "community"
                    ]
                }
            }, 
            "additionalProperties": false, 
            "oneOf": [
                {
                    "description": "It is been used since Rally 0.10.0", 
                    "required": [
                        "image_url", 
                        "disk_format", 
                        "container_format"
                    ]
                }, 
                {
                    "description": "One of backward compatible way", 
                    "required": [
                        "image_url", 
                        "image_type", 
                        "container_format"
                    ]
                }, 
                {
                    "description": "One of backward compatible way", 
                    "required": [
                        "image_url", 
                        "disk_format", 
                        "image_container"
                    ]
                }, 
                {
                    "description": "One of backward compatible way", 
                    "required": [
                        "image_url", 
                        "image_type", 
                        "image_container"
                    ]
                }
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/glance/images.py)

<hr />

#### keypair [Context]

Create Nova KeyPair for each user.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "object", 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/nova/keypairs.py)

<hr />

#### lbaas [Context]

Creates a lb-pool for every subnet created in network context.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "lbaas_version": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "pool": {
                    "type": "object", 
                    "additionalProperties": true
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.contexts.neutron.lbaas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/neutron/lbaas.py)

<hr />

#### manila_security_services [Context]

This context creates 'security services' for Manila project.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "security_services": {
                    "type": "array", 
                    "description": "It is expected to be list of dicts with data for creation of security services.", 
                    "items": {
                        "type": "object", 
                        "description": "Data for creation of security services. \n Example:\n\n   .. code-block:: json\n\n     {'type': 'LDAP', 'dns_ip': 'foo_ip', \n      'server': 'bar_ip', 'domain': 'quuz_domain',\n      'user': 'ololo', 'password': 'fake_password'}\n", 
                        "properties": {
                            "type": {
                                "enum": [
                                    "active_directory", 
                                    "kerberos", 
                                    "ldap"
                                ]
                            }
                        }, 
                        "additionalProperties": true, 
                        "required": [
                            "type"
                        ]
                    }
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.manila.manila_security_services](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/manila/manila_security_services.py)

<hr />

#### manila_share_networks [Context]

This context creates share networks for Manila project.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "share_networks": {
                    "type": "object", 
                    "description": "\nThis context arg will be used only when context arg \"use_share_networks\" is\nset to True.\n\nIf context arg 'share_networks' has values then they will be used else share\nnetworks will be autocreated - one for each tenant network. If networks do not\nexist then will be created one share network for each tenant without network\ndata.\n\nExpected value is dict of lists where tenant Name or ID is key and list of\nshare_network Names or IDs is value. Example:\n\n   .. code-block:: json\n\n     \"context\": {\n         \"manila_share_networks\": {\n         \"use_share_networks\": true,\n         \"share_networks\": {\n             \"tenant_1_name_or_id\": [\"share_network_1_name_or_id\",\n                                     \"share_network_2_name_or_id\"],\n             \"tenant_2_name_or_id\": [\"share_network_3_name_or_id\"]}\n         }\n     }\n\nAlso, make sure that all 'existing users' in appropriate registered deployment\nhave share networks if its usage is enabled, else Rally will randomly take\nusers that does not satisfy criteria.\n", 
                    "additionalProperties": true
                }, 
                "use_share_networks": {
                    "type": "boolean", 
                    "description": "Specifies whether manila should use share networks for share creation or not."
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.manila.manila_share_networks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/manila/manila_share_networks.py)

<hr />

#### manila_shares [Context]

This context creates shares for Manila project.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "share_proto": {
                    "type": "string"
                }, 
                "share_type": {
                    "type": "string"
                }, 
                "shares_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "size": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.manila.manila_shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/manila/manila_shares.py)

<hr />

#### monasca_metrics [Context]

Creates Monasca Metrics.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "dimensions": {
                    "type": "object", 
                    "properties": {
                        "hostname": {
                            "type": "string"
                        }, 
                        "region": {
                            "type": "string"
                        }, 
                        "service": {
                            "type": "string"
                        }, 
                        "url": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "metrics_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "name": {
                    "type": "string"
                }, 
                "value_meta": {
                    "type": "array", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "value_meta_key": {
                                "type": "string"
                            }, 
                            "value_meta_value": {
                                "type": "string"
                            }
                        }, 
                        "additionalProperties": false
                    }
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.monasca.metrics](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/monasca/metrics.py)

<hr />

#### murano_environments [Context]

Context class for creating murano environments.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "environments_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "environments_per_tenant"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.murano.murano_environments](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/murano/murano_environments.py)

<hr />

#### murano_packages [Context]

Context class for uploading applications for murano.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "app_package": {
                    "type": "string"
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "app_package"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.murano.murano_packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/murano/murano_packages.py)

<hr />

#### network [Context]

Create networking resources.

This creates networks for all tenants, and optionally creates
another resources like subnets and routers.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "dns_nameservers": {
                    "type": "array", 
                    "items": {
                        "type": "string"
                    }, 
                    "uniqueItems": true
                }, 
                "dualstack": {
                    "type": "boolean"
                }, 
                "network_create_args": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "networks_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "router": {
                    "type": "object", 
                    "properties": {
                        "external": {
                            "type": "boolean"
                        }, 
                        "external_gateway_info": {
                            "type": "object", 
                            "description": "The external gateway information .", 
                            "properties": {
                                "enable_snat": {
                                    "type": "boolean"
                                }, 
                                "network_id": {
                                    "type": "string"
                                }
                            }, 
                            "additionalProperties": false
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "start_cidr": {
                    "type": "string"
                }, 
                "subnets_per_network": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.contexts.network.networks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/network/networks.py)

<hr />

#### profiles [Context]

Context creates a temporary profile for Senlin test.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "properties": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "type": {
                    "type": "string"
                }, 
                "version": {
                    "type": "string"
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "type", 
                "version", 
                "properties"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.senlin.profiles](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/senlin/profiles.py)

<hr />

#### quotas [Context]

Sets OpenStack Tenants quotas.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "cinder": {
                    "type": "object", 
                    "properties": {
                        "backup_gigabytes": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "backups": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "gigabytes": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "snapshots": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "volumes": {
                            "type": "integer", 
                            "minimum": -1
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "designate": {
                    "type": "object", 
                    "properties": {
                        "domain_records": {
                            "type": "integer", 
                            "minimum": 1
                        }, 
                        "domain_recordsets": {
                            "type": "integer", 
                            "minimum": 1
                        }, 
                        "domains": {
                            "type": "integer", 
                            "minimum": 1
                        }, 
                        "recordset_records": {
                            "type": "integer", 
                            "minimum": 1
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "manila": {
                    "type": "object", 
                    "properties": {
                        "gigabytes": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "share_networks": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "shares": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "snapshot_gigabytes": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "snapshots": {
                            "type": "integer", 
                            "minimum": -1
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "neutron": {
                    "type": "object", 
                    "properties": {
                        "floatingip": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "health_monitor": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "network": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "pool": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "port": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "router": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "security_group": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "security_group_rule": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "subnet": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "vip": {
                            "type": "integer", 
                            "minimum": -1
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "nova": {
                    "type": "object", 
                    "properties": {
                        "cores": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "fixed_ips": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "floating_ips": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "injected_file_content_bytes": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "injected_file_path_bytes": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "injected_files": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "instances": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "key_pairs": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "metadata_items": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "ram": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "security_group_rules": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "security_groups": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "server_group_members": {
                            "type": "integer", 
                            "minimum": -1
                        }, 
                        "server_groups": {
                            "type": "integer", 
                            "minimum": -1
                        }
                    }, 
                    "additionalProperties": false
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.contexts.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/quotas/quotas.py)

<hr />

#### roles [Context]

Context class for assigning roles for users.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "array", 
            "items": {
                "type": "string", 
                "description": "The name of role to assign to user"
            }
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.keystone.roles](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/keystone/roles.py)

<hr />

#### router [Context]

Create networking resources.

This creates router for all tenants.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "admin_state_up ": {
                    "type": "boolean", 
                    "description": "A human-readable description for the resource"
                }, 
                "availability_zone_hints": {
                    "type": "boolean", 
                    "description": "Require router_availability_zone extension."
                }, 
                "distributed": {
                    "type": "boolean", 
                    "description": "Distributed router. Require dvr extension."
                }, 
                "external_fixed_ips": {
                    "type": "array", 
                    "description": "Ip(s) of the external gateway interface.", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "ip_address": {
                                "type": "string"
                            }, 
                            "subnet_id": {
                                "type": "string"
                            }
                        }, 
                        "additionalProperties": false
                    }
                }, 
                "external_gateway_info": {
                    "type": "object", 
                    "description": "The external gateway information .", 
                    "properties": {
                        "enable_snat": {
                            "type": "boolean"
                        }, 
                        "network_id": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "ha": {
                    "type": "boolean", 
                    "description": "Highly-available router. Require l3-ha."
                }, 
                "network_id": {
                    "type": "string", 
                    "description": "Network ID"
                }, 
                "routers_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.contexts.network.routers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/network/routers.py)

<hr />

#### sahara_cluster [Context]

Context class for setting up the Cluster an EDP job.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "auto_security_group": {
                    "type": "boolean"
                }, 
                "cluster_configs": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "enable_anti_affinity": {
                    "type": "boolean"
                }, 
                "enable_proxy": {
                    "type": "boolean"
                }, 
                "flavor_id": {
                    "type": "string"
                }, 
                "floating_ip_pool": {
                    "type": "string"
                }, 
                "hadoop_version": {
                    "type": "string"
                }, 
                "master_flavor_id": {
                    "type": "string"
                }, 
                "node_configs": {
                    "type": "object", 
                    "additionalProperties": true
                }, 
                "plugin_name": {
                    "type": "string"
                }, 
                "security_groups": {
                    "type": "array", 
                    "items": {
                        "type": "string"
                    }
                }, 
                "use_autoconfig": {
                    "type": "boolean"
                }, 
                "volumes_per_node": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "volumes_size": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "worker_flavor_id": {
                    "type": "string"
                }, 
                "workers_count": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "plugin_name", 
                "hadoop_version", 
                "workers_count", 
                "master_flavor_id", 
                "worker_flavor_id"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.sahara.sahara_cluster](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/sahara/sahara_cluster.py)

<hr />

#### sahara_image [Context]

Context class for adding and tagging Sahara images.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "hadoop_version": {
                    "type": "string"
                }, 
                "image_url": {
                    "type": "string"
                }, 
                "image_uuid": {
                    "type": "string"
                }, 
                "plugin_name": {
                    "type": "string"
                }, 
                "username": {
                    "type": "string"
                }
            }, 
            "additionalProperties": false, 
            "oneOf": [
                {
                    "description": "Create an image.", 
                    "required": [
                        "image_url", 
                        "username", 
                        "plugin_name", 
                        "hadoop_version"
                    ]
                }, 
                {
                    "description": "Use an existing image.", 
                    "required": [
                        "image_uuid"
                    ]
                }
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.sahara.sahara_image](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/sahara/sahara_image.py)

<hr />

#### sahara_input_data_sources [Context]

Context class for setting up Input Data Sources for an EDP job.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "input_type": {
                    "enum": [
                        "swift", 
                        "hdfs"
                    ]
                }, 
                "input_url": {
                    "type": "string"
                }, 
                "swift_files": {
                    "type": "array", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "download_url": {
                                "type": "string"
                            }, 
                            "name": {
                                "type": "string"
                            }
                        }, 
                        "additionalProperties": false, 
                        "required": [
                            "name", 
                            "download_url"
                        ]
                    }
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "input_type", 
                "input_url"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.sahara.sahara_input_data_sources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/sahara/sahara_input_data_sources.py)

<hr />

#### sahara_job_binaries [Context]

Context class for setting up Job Binaries for an EDP job.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "libs": {
                    "type": "array", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "download_url": {
                                "type": "string"
                            }, 
                            "name": {
                                "type": "string"
                            }
                        }, 
                        "additionalProperties": false, 
                        "required": [
                            "name", 
                            "download_url"
                        ]
                    }
                }, 
                "mains": {
                    "type": "array", 
                    "items": {
                        "type": "object", 
                        "properties": {
                            "download_url": {
                                "type": "string"
                            }, 
                            "name": {
                                "type": "string"
                            }
                        }, 
                        "additionalProperties": false, 
                        "required": [
                            "name", 
                            "download_url"
                        ]
                    }
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.sahara.sahara_job_binaries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/sahara/sahara_job_binaries.py)

<hr />

#### sahara_output_data_sources [Context]

Context class for setting up Output Data Sources for an EDP job.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "output_type": {
                    "enum": [
                        "swift", 
                        "hdfs"
                    ]
                }, 
                "output_url_prefix": {
                    "type": "string"
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "output_type", 
                "output_url_prefix"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.sahara.sahara_output_data_sources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/sahara/sahara_output_data_sources.py)

<hr />

#### servers [Context]

Creates specified amount of Nova Servers per each tenant.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "type": "object", 
            "properties": {
                "auto_assign_nic": {
                    "type": "boolean", 
                    "description": "True if NICs should be assigned."
                }, 
                "flavor": {
                    "type": "object", 
                    "description": "Name of flavor to boot server(s) with.", 
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "image": {
                    "type": "object", 
                    "description": "Name of image to boot server(s) from.", 
                    "properties": {
                        "name": {
                            "type": "string"
                        }
                    }, 
                    "additionalProperties": false
                }, 
                "nics": {
                    "type": "array", 
                    "description": "List of networks to attach to server.", 
                    "items": {
                        "oneOf": [
                            {
                                "type": "object", 
                                "description": "Network ID in a format like OpenStack API expects to see.", 
                                "properties": {
                                    "net-id": {
                                        "type": "string"
                                    }
                                }, 
                                "additionalProperties": false
                            }, 
                            {
                                "type": "string", 
                                "description": "Network ID."
                            }
                        ]
                    }, 
                    "minItems": 1
                }, 
                "servers_per_tenant": {
                    "type": "integer", 
                    "description": "Number of servers to boot in each Tenant.", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "image", 
                "flavor"
            ]
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/nova/servers.py)

<hr />

#### stacks [Context]

Context class for create temporary stacks with resources.

Stack generator allows to generate arbitrary number of stacks for
each tenant before test scenarios. In addition, it allows to define
number of resources (namely OS::Heat::RandomString) that will be created
inside each stack. After test execution the stacks will be
automatically removed from heat.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "resources_per_stack": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "stacks_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/heat/stacks.py)

<hr />

#### swift_objects [Context]

Create containers and objects in each tenant.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "containers_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "object_size": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "objects_per_container": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "resource_management_workers": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/swift/objects.py)

<hr />

#### users [Context]

Creates specified amount of keystone users and tenants.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "anyOf": [
                {
                    "description": "Create new temporary users and tenants.", 
                    "properties": {
                        "project_domain": {
                            "type": "string", 
                            "description": "ID of domain in which projects will be created."
                        }, 
                        "resource_management_workers": {
                            "type": "integer", 
                            "description": "The number of concurrent threads to use for serving users context.", 
                            "minimum": 1
                        }, 
                        "tenants": {
                            "type": "integer", 
                            "description": "The number of tenants to create.", 
                            "minimum": 1
                        }, 
                        "user_choice_method": {
                            "$ref": "#/definitions/user_choice_method"
                        }, 
                        "user_domain": {
                            "type": "string", 
                            "description": "ID of domain in which users will be created."
                        }, 
                        "users_per_tenant": {
                            "type": "integer", 
                            "description": "The number of users to create per one tenant.", 
                            "minimum": 1
                        }
                    }, 
                    "additionalProperties": false
                }, 
                {
                    "description": "Use existing users and tenants.", 
                    "properties": {
                        "user_choice_method": {
                            "$ref": "#/definitions/user_choice_method"
                        }
                    }, 
                    "additionalProperties": false
                }
            ], 
            "definitions": {
                "user_choice_method": {
                    "description": "The mode of balancing usage of users between scenario iterations.", 
                    "enum": [
                        "random", 
                        "round_robin"
                    ]
                }
            }
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.keystone.users](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/keystone/users.py)

<hr />

#### volume_types [Context]

Adds cinder volumes types.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "array", 
            "items": {
                "type": "string"
            }
        }

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.contexts.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/cinder/volume_types.py)

<hr />

#### volumes [Context]

Creates volumes for each tenant.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "size": {
                    "type": "integer", 
                    "minimum": 1
                }, 
                "type": {
                    "oneOf": [
                        {
                            "type": "string", 
                            "description": "a string-like type of volume to create."
                        }, 
                        {
                            "type": "null", 
                            "description": "Use default type for volume to create."
                        }
                    ]
                }, 
                "volumes_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "size"
            ]
        }

__Module__: [rally_openstack.contexts.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/cinder/volumes.py)

<hr />

#### zones [Context]

Context to add `zones_per_tenant` zones for each tenant.

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "zones_per_tenant": {
                    "type": "integer", 
                    "minimum": 1
                }
            }, 
            "additionalProperties": false
        }

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.contexts.designate.zones](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/designate/zones.py)

<hr />

### Hook Action

Factory for hook classes.

#### fault_injection [Hook Action]

Performs fault injection using os-faults library.

Configuration:

- action - string that represents an action (more info in [1])
- verify - whether to verify connection to cloud nodes or not

This plugin discovers extra config of ExistingCloud
and looks for "cloud_config" field. If cloud_config is present then
it will be used to connect to the cloud by os-faults.

Another option is to provide os-faults config file through
OS_FAULTS_CONFIG env variable. Format of the config can
be found in [1].

[1] <http://os-faults.readthedocs.io/en/latest/usage.html>

__Platform__: openstack

??? note "The input of this plugin should be valid to the following JSONSchema"
        :::json
        {
            "$schema": "http://json-schema.org/draft-04/schema", 
            "type": "object", 
            "properties": {
                "action": {
                    "type": "string"
                }, 
                "verify": {
                    "type": "boolean"
                }
            }, 
            "additionalProperties": false, 
            "required": [
                "action"
            ]
        }

__Module__: [rally_openstack.hook.fault_injection](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/hook/fault_injection.py)

<hr />

### Scenario

This is base class for any scenario.

All Scenario Plugins should be subclass of this class.

#### Authenticate.keystone [Scenario]

Check Keystone Client.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_ceilometer [Scenario]

Check Ceilometer Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-ceilometer-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-ceilometer-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_cinder [Scenario]

Check Cinder Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-cinder-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-cinder-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_glance [Scenario]

Check Glance Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.
In following we are checking for non-existent image.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-glance-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-glance-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_heat [Scenario]

Check Heat Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-heat-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-heat-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_monasca [Scenario]

Check Monasca Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-monasca-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-monasca-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_neutron [Scenario]

Check Neutron Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-neutron-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-neutron-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_nova [Scenario]

Check Nova Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

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
        <a name="ScenarioAuthenticatevalidate-nova-repetitions"></a>repetitions<a href="#ScenarioAuthenticatevalidate-nova-repetitions"> [ref]</a>
      </td>
      <td>number of times to validate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### CeilometerAlarms.create_alarm [Scenario]

Create an alarm.

This scenarios test POST /v2/alarms.
meter_name and threshold are required parameters for alarm creation.
kwargs stores other optional parameters like 'ok_actions',
'project_id' etc that may be passed while creating an alarm.

__Platform__: openstack

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
        <a name="ScenarioCeilometerAlarmscreate-alarm-meter-name"></a>meter_name<a href="#ScenarioCeilometerAlarmscreate-alarm-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of the alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-alarm-threshold"></a>threshold<a href="#ScenarioCeilometerAlarmscreate-alarm-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-alarm-kwargs"></a>kwargs<a href="#ScenarioCeilometerAlarmscreate-alarm-kwargs"> [ref]</a>
      </td>
      <td>specifies optional arguments for alarm creation.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.create_alarm_and_get_history [Scenario]

Create an alarm, get and set the state and get the alarm history.

This scenario makes following queries:

> - GET /v2/alarms/{alarm_id}/history
- GET /v2/alarms/{alarm_id}/state
- PUT /v2/alarms/{alarm_id}/state

Initially alarm is created and then get the state of the created alarm
using its alarm_id. Then get the history of the alarm. And finally the
state of the alarm is updated using given state. meter_name and
threshold are required parameters for alarm creation. kwargs stores
other optional parameters like 'ok_actions', 'project_id' etc that may
be passed while alarm creation.

__Platform__: openstack

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
        <a name="ScenarioCeilometerAlarmscreate-alarm-and-get-history-meter-name"></a>meter_name<a href="#ScenarioCeilometerAlarmscreate-alarm-and-get-history-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of the alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-alarm-and-get-history-threshold"></a>threshold<a href="#ScenarioCeilometerAlarmscreate-alarm-and-get-history-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-alarm-and-get-history-state"></a>state<a href="#ScenarioCeilometerAlarmscreate-alarm-and-get-history-state"> [ref]</a>
      </td>
      <td>an alarm state to be set
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-alarm-and-get-history-timeout"></a>timeout<a href="#ScenarioCeilometerAlarmscreate-alarm-and-get-history-timeout"> [ref]</a>
      </td>
      <td>The number of seconds for which to attempt a
successful check of the alarm state
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-alarm-and-get-history-kwargs"></a>kwargs<a href="#ScenarioCeilometerAlarmscreate-alarm-and-get-history-kwargs"> [ref]</a>
      </td>
      <td>specifies optional arguments for alarm creation.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.create_and_delete_alarm [Scenario]

Create and delete the newly created alarm.

This scenarios test DELETE /v2/alarms/(alarm_id)
Initially alarm is created and then the created alarm is deleted using
its alarm_id. meter_name and threshold are required parameters
for alarm creation. kwargs stores other optional parameters like
'ok_actions', 'project_id' etc that may be passed while alarm creation.

__Platform__: openstack

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
        <a name="ScenarioCeilometerAlarmscreate-and-delete-alarm-meter-name"></a>meter_name<a href="#ScenarioCeilometerAlarmscreate-and-delete-alarm-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of the alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-delete-alarm-threshold"></a>threshold<a href="#ScenarioCeilometerAlarmscreate-and-delete-alarm-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-delete-alarm-kwargs"></a>kwargs<a href="#ScenarioCeilometerAlarmscreate-and-delete-alarm-kwargs"> [ref]</a>
      </td>
      <td>specifies optional arguments for alarm creation.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.create_and_get_alarm [Scenario]

Create and get the newly created alarm.

These scenarios test GET /v2/alarms/(alarm_id)
Initially an alarm is created and then its detailed information is
fetched using its alarm_id. meter_name and threshold are required
parameters for alarm creation. kwargs stores other optional parameters
like 'ok_actions', 'project_id' etc. that may be passed while creating
an alarm.

__Platform__: openstack

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
        <a name="ScenarioCeilometerAlarmscreate-and-get-alarm-meter-name"></a>meter_name<a href="#ScenarioCeilometerAlarmscreate-and-get-alarm-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of the alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-get-alarm-threshold"></a>threshold<a href="#ScenarioCeilometerAlarmscreate-and-get-alarm-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-get-alarm-kwargs"></a>kwargs<a href="#ScenarioCeilometerAlarmscreate-and-get-alarm-kwargs"> [ref]</a>
      </td>
      <td>specifies optional arguments for alarm creation.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.create_and_list_alarm [Scenario]

Create and get the newly created alarm.

This scenarios test GET /v2/alarms/(alarm_id)
Initially alarm is created and then the created alarm is fetched using
its alarm_id. meter_name and threshold are required parameters
for alarm creation. kwargs stores other optional parameters like
'ok_actions', 'project_id' etc. that may be passed while creating
an alarm.

__Platform__: openstack

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
        <a name="ScenarioCeilometerAlarmscreate-and-list-alarm-meter-name"></a>meter_name<a href="#ScenarioCeilometerAlarmscreate-and-list-alarm-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of the alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-list-alarm-threshold"></a>threshold<a href="#ScenarioCeilometerAlarmscreate-and-list-alarm-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-list-alarm-kwargs"></a>kwargs<a href="#ScenarioCeilometerAlarmscreate-and-list-alarm-kwargs"> [ref]</a>
      </td>
      <td>specifies optional arguments for alarm creation.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.create_and_update_alarm [Scenario]

Create and update the newly created alarm.

This scenarios test PUT /v2/alarms/(alarm_id)
Initially alarm is created and then the created alarm is updated using
its alarm_id. meter_name and threshold are required parameters
for alarm creation. kwargs stores other optional parameters like
'ok_actions', 'project_id' etc that may be passed while alarm creation.

__Platform__: openstack

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
        <a name="ScenarioCeilometerAlarmscreate-and-update-alarm-meter-name"></a>meter_name<a href="#ScenarioCeilometerAlarmscreate-and-update-alarm-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of the alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-update-alarm-threshold"></a>threshold<a href="#ScenarioCeilometerAlarmscreate-and-update-alarm-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerAlarmscreate-and-update-alarm-kwargs"></a>kwargs<a href="#ScenarioCeilometerAlarmscreate-and-update-alarm-kwargs"> [ref]</a>
      </td>
      <td>specifies optional arguments for alarm creation.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.list_alarms [Scenario]

Fetch all alarms.

This scenario fetches list of all alarms using GET /v2/alarms.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerEvents.create_user_and_get_event [Scenario]

Create user and gets event.

This scenario creates user to store new event and
fetches one event using GET /v2/events/<message_id>.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ceilometer.events](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/events.py)

<hr />

#### CeilometerEvents.create_user_and_list_event_types [Scenario]

Create user and fetch all event types.

This scenario creates user to store new event and
fetches list of all events types using GET /v2/event_types.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ceilometer.events](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/events.py)

<hr />

#### CeilometerEvents.create_user_and_list_events [Scenario]

Create user and fetch all events.

This scenario creates user to store new event and
fetches list of all events using GET /v2/events.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ceilometer.events](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/events.py)

<hr />

#### CeilometerMeters.list_matched_meters [Scenario]

Get meters that matched fields from context and args.

__Platform__: openstack

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
        <a name="ScenarioCeilometerMeterslist-matched-meters-filter-by-user-id"></a>filter_by_user_id<a href="#ScenarioCeilometerMeterslist-matched-meters-filter-by-user-id"> [ref]</a>
      </td>
      <td>flag for query by user_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerMeterslist-matched-meters-filter-by-project-id"></a>filter_by_project_id<a href="#ScenarioCeilometerMeterslist-matched-meters-filter-by-project-id"> [ref]</a>
      </td>
      <td>flag for query by project_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerMeterslist-matched-meters-filter-by-resource-id"></a>filter_by_resource_id<a href="#ScenarioCeilometerMeterslist-matched-meters-filter-by-resource-id"> [ref]</a>
      </td>
      <td>flag for query by resource_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerMeterslist-matched-meters-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerMeterslist-matched-meters-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values for query
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerMeterslist-matched-meters-limit"></a>limit<a href="#ScenarioCeilometerMeterslist-matched-meters-limit"> [ref]</a>
      </td>
      <td>count of resources in response</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.meters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/meters.py)

<hr />

#### CeilometerMeters.list_meters [Scenario]

Check all available queries for list resource request.

__Platform__: openstack

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
        <a name="ScenarioCeilometerMeterslist-meters-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerMeterslist-meters-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerMeterslist-meters-limit"></a>limit<a href="#ScenarioCeilometerMeterslist-meters-limit"> [ref]</a>
      </td>
      <td>limit of meters in response</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.meters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/meters.py)

<hr />

#### CeilometerQueries.create_and_query_alarm_history [Scenario]

Create an alarm and then query for its history.

This scenario tests POST /v2/query/alarms/history
An alarm is first created and then its alarm_id is used to fetch the
history of that specific alarm.

__Platform__: openstack

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
        <a name="ScenarioCeilometerQueriescreate-and-query-alarm-history-meter-name"></a>meter_name<a href="#ScenarioCeilometerQueriescreate-and-query-alarm-history-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarm-history-threshold"></a>threshold<a href="#ScenarioCeilometerQueriescreate-and-query-alarm-history-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarm-history-orderby"></a>orderby<a href="#ScenarioCeilometerQueriescreate-and-query-alarm-history-orderby"> [ref]</a>
      </td>
      <td>optional param for specifying ordering of results
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarm-history-limit"></a>limit<a href="#ScenarioCeilometerQueriescreate-and-query-alarm-history-limit"> [ref]</a>
      </td>
      <td>optional param for maximum number of results returned
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarm-history-kwargs"></a>kwargs<a href="#ScenarioCeilometerQueriescreate-and-query-alarm-history-kwargs"> [ref]</a>
      </td>
      <td>optional parameters for alarm creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.queries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/queries.py)

<hr />

#### CeilometerQueries.create_and_query_alarms [Scenario]

Create an alarm and then query it with specific parameters.

This scenario tests POST /v2/query/alarms
An alarm is first created and then fetched using the input query.

__Platform__: openstack

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
        <a name="ScenarioCeilometerQueriescreate-and-query-alarms-meter-name"></a>meter_name<a href="#ScenarioCeilometerQueriescreate-and-query-alarms-meter-name"> [ref]</a>
      </td>
      <td>specifies meter name of alarm
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarms-threshold"></a>threshold<a href="#ScenarioCeilometerQueriescreate-and-query-alarms-threshold"> [ref]</a>
      </td>
      <td>specifies alarm threshold
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarms-filter"></a>filter<a href="#ScenarioCeilometerQueriescreate-and-query-alarms-filter"> [ref]</a>
      </td>
      <td>optional filter query dictionary
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarms-orderby"></a>orderby<a href="#ScenarioCeilometerQueriescreate-and-query-alarms-orderby"> [ref]</a>
      </td>
      <td>optional param for specifying ordering of results
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarms-limit"></a>limit<a href="#ScenarioCeilometerQueriescreate-and-query-alarms-limit"> [ref]</a>
      </td>
      <td>optional param for maximum number of results returned
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-alarms-kwargs"></a>kwargs<a href="#ScenarioCeilometerQueriescreate-and-query-alarms-kwargs"> [ref]</a>
      </td>
      <td>optional parameters for alarm creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.queries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/queries.py)

<hr />

#### CeilometerQueries.create_and_query_samples [Scenario]

Create a sample and then query it with specific parameters.

This scenario tests POST /v2/query/samples
A sample is first created and then fetched using the input query.

__Platform__: openstack

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
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-counter-name"></a>counter_name<a href="#ScenarioCeilometerQueriescreate-and-query-samples-counter-name"> [ref]</a>
      </td>
      <td>specifies name of the counter
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-counter-type"></a>counter_type<a href="#ScenarioCeilometerQueriescreate-and-query-samples-counter-type"> [ref]</a>
      </td>
      <td>specifies type of the counter
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-counter-unit"></a>counter_unit<a href="#ScenarioCeilometerQueriescreate-and-query-samples-counter-unit"> [ref]</a>
      </td>
      <td>specifies unit of the counter
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-counter-volume"></a>counter_volume<a href="#ScenarioCeilometerQueriescreate-and-query-samples-counter-volume"> [ref]</a>
      </td>
      <td>specifies volume of the counter
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-resource-id"></a>resource_id<a href="#ScenarioCeilometerQueriescreate-and-query-samples-resource-id"> [ref]</a>
      </td>
      <td>specifies resource id for the sample created
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-filter"></a>filter<a href="#ScenarioCeilometerQueriescreate-and-query-samples-filter"> [ref]</a>
      </td>
      <td>optional filter query dictionary
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-orderby"></a>orderby<a href="#ScenarioCeilometerQueriescreate-and-query-samples-orderby"> [ref]</a>
      </td>
      <td>optional param for specifying ordering of results
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-limit"></a>limit<a href="#ScenarioCeilometerQueriescreate-and-query-samples-limit"> [ref]</a>
      </td>
      <td>optional param for maximum number of results returned
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerQueriescreate-and-query-samples-kwargs"></a>kwargs<a href="#ScenarioCeilometerQueriescreate-and-query-samples-kwargs"> [ref]</a>
      </td>
      <td>parameters for sample creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.queries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/queries.py)

<hr />

#### CeilometerResource.get_tenant_resources [Scenario]

Get all tenant resources.

This scenario retrieves information about tenant resources using
GET /v2/resources/(resource_id)

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.resources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/resources.py)

<hr />

#### CeilometerResource.list_matched_resources [Scenario]

Get resources that matched fields from context and args.

__Platform__: openstack

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
        <a name="ScenarioCeilometerResourcelist-matched-resources-filter-by-user-id"></a>filter_by_user_id<a href="#ScenarioCeilometerResourcelist-matched-resources-filter-by-user-id"> [ref]</a>
      </td>
      <td>flag for query by user_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-matched-resources-filter-by-project-id"></a>filter_by_project_id<a href="#ScenarioCeilometerResourcelist-matched-resources-filter-by-project-id"> [ref]</a>
      </td>
      <td>flag for query by project_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-matched-resources-filter-by-resource-id"></a>filter_by_resource_id<a href="#ScenarioCeilometerResourcelist-matched-resources-filter-by-resource-id"> [ref]</a>
      </td>
      <td>flag for query by resource_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-matched-resources-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerResourcelist-matched-resources-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values for query
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-matched-resources-start-time"></a>start_time<a href="#ScenarioCeilometerResourcelist-matched-resources-start-time"> [ref]</a>
      </td>
      <td>lower bound of resource timestamp in isoformat
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-matched-resources-end-time"></a>end_time<a href="#ScenarioCeilometerResourcelist-matched-resources-end-time"> [ref]</a>
      </td>
      <td>upper bound of resource timestamp in isoformat
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-matched-resources-limit"></a>limit<a href="#ScenarioCeilometerResourcelist-matched-resources-limit"> [ref]</a>
      </td>
      <td>count of resources in response</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.resources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/resources.py)

<hr />

#### CeilometerResource.list_resources [Scenario]

Check all available queries for list resource request.

This scenario fetches list of all resources using GET /v2/resources.

__Platform__: openstack

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
        <a name="ScenarioCeilometerResourcelist-resources-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerResourcelist-resources-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values for query
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-resources-start-time"></a>start_time<a href="#ScenarioCeilometerResourcelist-resources-start-time"> [ref]</a>
      </td>
      <td>lower bound of resource timestamp in isoformat
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-resources-end-time"></a>end_time<a href="#ScenarioCeilometerResourcelist-resources-end-time"> [ref]</a>
      </td>
      <td>upper bound of resource timestamp in isoformat
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerResourcelist-resources-limit"></a>limit<a href="#ScenarioCeilometerResourcelist-resources-limit"> [ref]</a>
      </td>
      <td>count of resources in response</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.resources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/resources.py)

<hr />

#### CeilometerSamples.list_matched_samples [Scenario]

Get list of samples that matched fields from context and args.

__Platform__: openstack

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
        <a name="ScenarioCeilometerSampleslist-matched-samples-filter-by-user-id"></a>filter_by_user_id<a href="#ScenarioCeilometerSampleslist-matched-samples-filter-by-user-id"> [ref]</a>
      </td>
      <td>flag for query by user_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerSampleslist-matched-samples-filter-by-project-id"></a>filter_by_project_id<a href="#ScenarioCeilometerSampleslist-matched-samples-filter-by-project-id"> [ref]</a>
      </td>
      <td>flag for query by project_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerSampleslist-matched-samples-filter-by-resource-id"></a>filter_by_resource_id<a href="#ScenarioCeilometerSampleslist-matched-samples-filter-by-resource-id"> [ref]</a>
      </td>
      <td>flag for query by resource_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerSampleslist-matched-samples-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerSampleslist-matched-samples-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values for query
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerSampleslist-matched-samples-limit"></a>limit<a href="#ScenarioCeilometerSampleslist-matched-samples-limit"> [ref]</a>
      </td>
      <td>count of samples in response</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.samples](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/samples.py)

<hr />

#### CeilometerSamples.list_samples [Scenario]

Fetch all available queries for list sample request.

__Platform__: openstack

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
        <a name="ScenarioCeilometerSampleslist-samples-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerSampleslist-samples-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values for query
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerSampleslist-samples-limit"></a>limit<a href="#ScenarioCeilometerSampleslist-samples-limit"> [ref]</a>
      </td>
      <td>count of samples in response</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.samples](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/samples.py)

<hr />

#### CeilometerStats.create_meter_and_get_stats [Scenario]

Create a meter and fetch its statistics.

Meter is first created and then statistics is fetched for the same
using GET /v2/meters/(meter_name)/statistics.

__Platform__: openstack

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
        <a name="ScenarioCeilometerStatscreate-meter-and-get-stats-kwargs"></a>kwargs<a href="#ScenarioCeilometerStatscreate-meter-and-get-stats-kwargs"> [ref]</a>
      </td>
      <td>contains optional arguments to create a meter</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.stats](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/stats.py)

<hr />

#### CeilometerStats.get_stats [Scenario]

Fetch statistics for certain meter.

Statistics is fetched for the using
GET /v2/meters/(meter_name)/statistics.

__Platform__: openstack

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
        <a name="ScenarioCeilometerStatsget-stats-meter-name"></a>meter_name<a href="#ScenarioCeilometerStatsget-stats-meter-name"> [ref]</a>
      </td>
      <td>meter to take statistic for
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-filter-by-user-id"></a>filter_by_user_id<a href="#ScenarioCeilometerStatsget-stats-filter-by-user-id"> [ref]</a>
      </td>
      <td>flag for query by user_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-filter-by-project-id"></a>filter_by_project_id<a href="#ScenarioCeilometerStatsget-stats-filter-by-project-id"> [ref]</a>
      </td>
      <td>flag for query by project_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-filter-by-resource-id"></a>filter_by_resource_id<a href="#ScenarioCeilometerStatsget-stats-filter-by-resource-id"> [ref]</a>
      </td>
      <td>flag for query by resource_id
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-metadata-query"></a>metadata_query<a href="#ScenarioCeilometerStatsget-stats-metadata-query"> [ref]</a>
      </td>
      <td>dict with metadata fields and values for query
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-period"></a>period<a href="#ScenarioCeilometerStatsget-stats-period"> [ref]</a>
      </td>
      <td>the length of the time range covered by these stats
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-groupby"></a>groupby<a href="#ScenarioCeilometerStatsget-stats-groupby"> [ref]</a>
      </td>
      <td>the fields used to group the samples
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCeilometerStatsget-stats-aggregates"></a>aggregates<a href="#ScenarioCeilometerStatsget-stats-aggregates"> [ref]</a>
      </td>
      <td>name of function for samples aggregation
</td>
    </tr>
  </tbody>
</table>


__Returns__:  
list of statistics data

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ceilometer.stats](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/stats.py)

<hr />

#### CeilometerTraits.create_user_and_list_trait_descriptions [Scenario]

Create user and fetch all trait descriptions.

This scenario creates user to store new event and
fetches list of all traits for certain event type using
GET /v2/event_types/<event_type>/traits.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ceilometer.traits](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/traits.py)

<hr />

#### CeilometerTraits.create_user_and_list_traits [Scenario]

Create user and fetch all event traits.

This scenario creates user to store new event and
fetches list of all traits for certain event type and
trait name using GET /v2/event_types/<event_type>/traits/<trait_name>.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ceilometer.traits](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/traits.py)

<hr />

#### CinderQos.create_and_get_qos [Scenario]

Create a qos, then get details of the qos.

__Platform__: openstack

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
        <a name="ScenarioCinderQoscreate-and-get-qos-consumer"></a>consumer<a href="#ScenarioCinderQoscreate-and-get-qos-consumer"> [ref]</a>
      </td>
      <td>Consumer behavior
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-get-qos-write-iops-sec"></a>write_iops_sec<a href="#ScenarioCinderQoscreate-and-get-qos-write-iops-sec"> [ref]</a>
      </td>
      <td>random write limitation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-get-qos-read-iops-sec"></a>read_iops_sec<a href="#ScenarioCinderQoscreate-and-get-qos-read-iops-sec"> [ref]</a>
      </td>
      <td>random read limitation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderQos.create_and_list_qos [Scenario]

Create a qos, then list all qos.

__Platform__: openstack

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
        <a name="ScenarioCinderQoscreate-and-list-qos-consumer"></a>consumer<a href="#ScenarioCinderQoscreate-and-list-qos-consumer"> [ref]</a>
      </td>
      <td>Consumer behavior
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-list-qos-write-iops-sec"></a>write_iops_sec<a href="#ScenarioCinderQoscreate-and-list-qos-write-iops-sec"> [ref]</a>
      </td>
      <td>random write limitation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-list-qos-read-iops-sec"></a>read_iops_sec<a href="#ScenarioCinderQoscreate-and-list-qos-read-iops-sec"> [ref]</a>
      </td>
      <td>random read limitation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderQos.create_and_set_qos [Scenario]

Create a qos, then Add/Update keys in qos specs.

__Platform__: openstack

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
        <a name="ScenarioCinderQoscreate-and-set-qos-consumer"></a>consumer<a href="#ScenarioCinderQoscreate-and-set-qos-consumer"> [ref]</a>
      </td>
      <td>Consumer behavior
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-set-qos-write-iops-sec"></a>write_iops_sec<a href="#ScenarioCinderQoscreate-and-set-qos-write-iops-sec"> [ref]</a>
      </td>
      <td>random write limitation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-set-qos-read-iops-sec"></a>read_iops_sec<a href="#ScenarioCinderQoscreate-and-set-qos-read-iops-sec"> [ref]</a>
      </td>
      <td>random read limitation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-set-qos-set-consumer"></a>set_consumer<a href="#ScenarioCinderQoscreate-and-set-qos-set-consumer"> [ref]</a>
      </td>
      <td>update Consumer behavior
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-set-qos-set-write-iops-sec"></a>set_write_iops_sec<a href="#ScenarioCinderQoscreate-and-set-qos-set-write-iops-sec"> [ref]</a>
      </td>
      <td>update random write limitation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-and-set-qos-set-read-iops-sec"></a>set_read_iops_sec<a href="#ScenarioCinderQoscreate-and-set-qos-set-read-iops-sec"> [ref]</a>
      </td>
      <td>update random read limitation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderQos.create_qos_associate_and_disassociate_type [Scenario]

Create a qos, Associate and Disassociate the qos from volume type.

__Platform__: openstack

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
        <a name="ScenarioCinderQoscreate-qos-associate-and-disassociate-type-consumer"></a>consumer<a href="#ScenarioCinderQoscreate-qos-associate-and-disassociate-type-consumer"> [ref]</a>
      </td>
      <td>Consumer behavior
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-qos-associate-and-disassociate-type-write-iops-sec"></a>write_iops_sec<a href="#ScenarioCinderQoscreate-qos-associate-and-disassociate-type-write-iops-sec"> [ref]</a>
      </td>
      <td>random write limitation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderQoscreate-qos-associate-and-disassociate-type-read-iops-sec"></a>read_iops_sec<a href="#ScenarioCinderQoscreate-qos-associate-and-disassociate-type-read-iops-sec"> [ref]</a>
      </td>
      <td>random read limitation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderVolumeBackups.create_incremental_volume_backup [Scenario]

Create a incremental volume backup.

The scenario first create a volume, the create a backup, the backup
is full backup. Because Incremental backup must be based on the
full backup. finally create a incremental backup.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeBackupscreate-incremental-volume-backup-size"></a>size<a href="#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-size"> [ref]</a>
      </td>
      <td>volume size in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeBackupscreate-incremental-volume-backup-do-delete"></a>do_delete<a href="#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-do-delete"> [ref]</a>
      </td>
      <td>deletes backup and volume after creating if True
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-backup-kwargs"></a>create_backup_kwargs<a href="#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-backup-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume backup</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volume_backups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_backups.py)

<hr />

#### CinderVolumeTypes.create_and_delete_encryption_type [Scenario]

Create and delete encryption type.

This scenario firstly creates an encryption type for a given
volume type, then deletes the created encryption type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-delete-encryption-type-create-specs"></a>create_specs<a href="#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-create-specs"> [ref]</a>
      </td>
      <td>the encryption type specifications to add
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-delete-encryption-type-provider"></a>provider<a href="#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-provider"> [ref]</a>
      </td>
      <td>The class that provides encryption support. For
example, LuksEncryptor.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-delete-encryption-type-cipher"></a>cipher<a href="#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-cipher"> [ref]</a>
      </td>
      <td>The encryption algorithm or mode.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-delete-encryption-type-key-size"></a>key_size<a href="#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-key-size"> [ref]</a>
      </td>
      <td>Size of encryption key, in bits.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-delete-encryption-type-control-location"></a>control_location<a href="#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-control-location"> [ref]</a>
      </td>
      <td>Notional service where encryption is
performed. Valid values are "front-end"
or "back-end."
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_delete_volume_type [Scenario]

Create and delete a volume Type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-delete-volume-type-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-and-delete-volume-type-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-delete-volume-type-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-and-delete-volume-type-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_get_volume_type [Scenario]

Create a volume Type, then get the details of the type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-get-volume-type-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-and-get-volume-type-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-get-volume-type-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-and-get-volume-type-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_list_encryption_type [Scenario]

Create and list encryption type.

This scenario firstly creates a volume type, secondly creates an
encryption type for the volume type, thirdly lists all encryption
types.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-list-encryption-type-create-specs"></a>create_specs<a href="#ScenarioCinderVolumeTypescreate-and-list-encryption-type-create-specs"> [ref]</a>
      </td>
      <td>The encryption type specifications to add.
DEPRECATED, specify arguments explicitly.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-list-encryption-type-provider"></a>provider<a href="#ScenarioCinderVolumeTypescreate-and-list-encryption-type-provider"> [ref]</a>
      </td>
      <td>The class that provides encryption support. For
example, LuksEncryptor.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-list-encryption-type-cipher"></a>cipher<a href="#ScenarioCinderVolumeTypescreate-and-list-encryption-type-cipher"> [ref]</a>
      </td>
      <td>The encryption algorithm or mode.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-list-encryption-type-key-size"></a>key_size<a href="#ScenarioCinderVolumeTypescreate-and-list-encryption-type-key-size"> [ref]</a>
      </td>
      <td>Size of encryption key, in bits.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-list-encryption-type-control-location"></a>control_location<a href="#ScenarioCinderVolumeTypescreate-and-list-encryption-type-control-location"> [ref]</a>
      </td>
      <td>Notional service where encryption is
performed. Valid values are "front-end"
or "back-end."
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-list-encryption-type-search-opts"></a>search_opts<a href="#ScenarioCinderVolumeTypescreate-and-list-encryption-type-search-opts"> [ref]</a>
      </td>
      <td>Options used when search for encryption types</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_list_volume_types [Scenario]

Create a volume Type, then list all types.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-list-volume-types-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-and-list-volume-types-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-list-volume-types-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-and-list-volume-types-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_set_volume_type_keys [Scenario]

Create and set a volume type's extra specs.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-volume-type-key"></a>volume_type_key<a href="#ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-volume-type-key"> [ref]</a>
      </td>
      <td>A dict of key/value pairs to be set
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_update_encryption_type [Scenario]

Create and update encryption type.

This scenario firstly creates a volume type, secondly creates an
encryption type for the volume type, thirdly updates the encryption
type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-provider"></a>create_provider<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-provider"> [ref]</a>
      </td>
      <td>The class that provides encryption support. For
example, LuksEncryptor.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-cipher"></a>create_cipher<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-cipher"> [ref]</a>
      </td>
      <td>The encryption algorithm or mode.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-key-size"></a>create_key_size<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-key-size"> [ref]</a>
      </td>
      <td>Size of encryption key, in bits.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-control-location"></a>create_control_location<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-control-location"> [ref]</a>
      </td>
      <td>Notional service where encryption is
performed. Valid values are "front-end"
or "back-end."
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-provider"></a>update_provider<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-provider"> [ref]</a>
      </td>
      <td>The class that provides encryption support. For
example, LuksEncryptor.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-cipher"></a>update_cipher<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-cipher"> [ref]</a>
      </td>
      <td>The encryption algorithm or mode.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-key-size"></a>update_key_size<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-key-size"> [ref]</a>
      </td>
      <td>Size of encryption key, in bits.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-control-location"></a>update_control_location<a href="#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-control-location"> [ref]</a>
      </td>
      <td>Notional service where encryption is
performed. Valid values are "front-end"
or "back-end."
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_update_volume_type [Scenario]

create a volume type, then update the type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-and-update-volume-type-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-and-update-volume-type-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-volume-type-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-and-update-volume-type-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-volume-type-update-name"></a>update_name<a href="#ScenarioCinderVolumeTypescreate-and-update-volume-type-update-name"> [ref]</a>
      </td>
      <td>if True, can update name by generating random name.
if False, don't update name.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-volume-type-update-description"></a>update_description<a href="#ScenarioCinderVolumeTypescreate-and-update-volume-type-update-description"> [ref]</a>
      </td>
      <td>update Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-and-update-volume-type-update-is-public"></a>update_is_public<a href="#ScenarioCinderVolumeTypescreate-and-update-volume-type-update-is-public"> [ref]</a>
      </td>
      <td>update Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_get_and_delete_encryption_type [Scenario]

Create get and delete an encryption type.

This scenario firstly creates an encryption type for a volume
type created in the context, then gets detailed information of
the created encryption type, finally deletes the created
encryption type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-provider"></a>provider<a href="#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-provider"> [ref]</a>
      </td>
      <td>The class that provides encryption support. For
example, LuksEncryptor.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-cipher"></a>cipher<a href="#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-cipher"> [ref]</a>
      </td>
      <td>The encryption algorithm or mode.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-key-size"></a>key_size<a href="#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-key-size"> [ref]</a>
      </td>
      <td>Size of encryption key, in bits.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-control-location"></a>control_location<a href="#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-control-location"> [ref]</a>
      </td>
      <td>Notional service where encryption is
performed. Valid values are "front-end"
or "back-end."
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_volume_type_add_and_list_type_access [Scenario]

Add and list volume type access for the given project.

This scenario first creates a private volume type, then add project
access and list project access to it.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_volume_type_and_encryption_type [Scenario]

Create encryption type.

This scenario first creates a volume type, then creates an encryption
type for the volume type.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-create-specs"></a>create_specs<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-create-specs"> [ref]</a>
      </td>
      <td>The encryption type specifications to add.
DEPRECATED, specify arguments explicitly.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-provider"></a>provider<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-provider"> [ref]</a>
      </td>
      <td>The class that provides encryption support. For
example, LuksEncryptor.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-cipher"></a>cipher<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-cipher"> [ref]</a>
      </td>
      <td>The encryption algorithm or mode.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-key-size"></a>key_size<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-key-size"> [ref]</a>
      </td>
      <td>Size of encryption key, in bits.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-control-location"></a>control_location<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-control-location"> [ref]</a>
      </td>
      <td>Notional service where encryption is
performed. Valid values are "front-end"
or "back-end."
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-description"></a>description<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-description"> [ref]</a>
      </td>
      <td>Description of the volume type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-is-public"></a>is_public<a href="#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-is-public"> [ref]</a>
      </td>
      <td>Volume type visibility</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumes.create_and_accept_transfer [Scenario]

Create a volume transfer, then accept it.

Measure the "cinder transfer-create" and "cinder transfer-accept"
command performace.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-accept-transfer-size"></a>size<a href="#ScenarioCinderVolumescreate-and-accept-transfer-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-accept-transfer-image"></a>image<a href="#ScenarioCinderVolumescreate-and-accept-transfer-image"> [ref]</a>
      </td>
      <td>image to be used to create initial volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-accept-transfer-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-accept-transfer-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_attach_volume [Scenario]

Create a VM and attach a volume to it.

Simple test to create a VM and attach a volume, then
detach the volume and delete volume/VM.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-attach-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-and-attach-volume-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-attach-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-and-attach-volume-image"> [ref]</a>
      </td>
      <td>Glance image name to use for the VM
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-attach-volume-flavor"></a>flavor<a href="#ScenarioCinderVolumescreate-and-attach-volume-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-attach-volume-create-volume-params"></a>create_volume_params<a href="#ScenarioCinderVolumescreate-and-attach-volume-create-volume-params"> [ref]</a>
      </td>
      <td>optional arguments for volume creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-attach-volume-create-vm-params"></a>create_vm_params<a href="#ScenarioCinderVolumescreate-and-attach-volume-create-vm-params"> [ref]</a>
      </td>
      <td>optional arguments for VM creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-attach-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-attach-volume-kwargs"> [ref]</a>
      </td>
      <td>(deprecated) optional arguments for VM creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_delete_snapshot [Scenario]

Create and then delete a volume-snapshot.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between snapshot creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-delete-snapshot-force"></a>force<a href="#ScenarioCinderVolumescreate-and-delete-snapshot-force"> [ref]</a>
      </td>
      <td>when set to True, allows snapshot of a volume when
the volume is attached to an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-snapshot-min-sleep"></a>min_sleep<a href="#ScenarioCinderVolumescreate-and-delete-snapshot-min-sleep"> [ref]</a>
      </td>
      <td>minimum sleep time between snapshot creation and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-snapshot-max-sleep"></a>max_sleep<a href="#ScenarioCinderVolumescreate-and-delete-snapshot-max-sleep"> [ref]</a>
      </td>
      <td>maximum sleep time between snapshot creation and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-snapshot-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-delete-snapshot-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a snapshot</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_delete_volume [Scenario]

Create and then delete a volume.

Good for testing a maximal bandwidth of cloud. Optional 'min_sleep'
and 'max_sleep' parameters allow the scenario to simulate a pause
between volume creation and deletion (of random duration from
[min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-delete-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-and-delete-volume-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-and-delete-volume-image"> [ref]</a>
      </td>
      <td>image to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-volume-min-sleep"></a>min_sleep<a href="#ScenarioCinderVolumescreate-and-delete-volume-min-sleep"> [ref]</a>
      </td>
      <td>minimum sleep time between volume creation and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-volume-max-sleep"></a>max_sleep<a href="#ScenarioCinderVolumescreate-and-delete-volume-max-sleep"> [ref]</a>
      </td>
      <td>maximum sleep time between volume creation and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-delete-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-delete-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_extend_volume [Scenario]

Create and extend a volume and then delete it.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-extend-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-and-extend-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-extend-volume-new-size"></a>new_size<a href="#ScenarioCinderVolumescreate-and-extend-volume-new-size"> [ref]</a>
      </td>
      <td>volume new size (in GB) or
dictionary, must contain two values:
     min - minimum size volumes will be created as;
     max - maximum size volumes will be created as.
to extend.
Notice: should be bigger volume size
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-extend-volume-min-sleep"></a>min_sleep<a href="#ScenarioCinderVolumescreate-and-extend-volume-min-sleep"> [ref]</a>
      </td>
      <td>minimum sleep time between volume extension and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-extend-volume-max-sleep"></a>max_sleep<a href="#ScenarioCinderVolumescreate-and-extend-volume-max-sleep"> [ref]</a>
      </td>
      <td>maximum sleep time between volume extension and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-extend-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-extend-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to extend the volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_get_volume [Scenario]

Create a volume and get the volume.

Measure the "cinder show" command performance.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-get-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-and-get-volume-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-get-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-and-get-volume-image"> [ref]</a>
      </td>
      <td>image to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-get-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-get-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_list_snapshots [Scenario]

Create and then list a volume-snapshot.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-list-snapshots-force"></a>force<a href="#ScenarioCinderVolumescreate-and-list-snapshots-force"> [ref]</a>
      </td>
      <td>when set to True, allows snapshot of a volume when
the volume is attached to an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-snapshots-detailed"></a>detailed<a href="#ScenarioCinderVolumescreate-and-list-snapshots-detailed"> [ref]</a>
      </td>
      <td>True if detailed information about snapshots
should be listed
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-snapshots-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-list-snapshots-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a snapshot</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_list_volume [Scenario]

Create a volume and list all volumes.

Measure the "cinder volume-list" command performance.

If you have only 1 user in your context, you will
add 1 volume on every iteration. So you will have more
and more volumes and will be able to measure the
performance of the "cinder volume-list" command depending on
the number of images owned by users.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-list-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-and-list-volume-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-detailed"></a>detailed<a href="#ScenarioCinderVolumescreate-and-list-volume-detailed"> [ref]</a>
      </td>
      <td>determines whether the volume listing should contain
detailed information about all of them
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-and-list-volume-image"> [ref]</a>
      </td>
      <td>image to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-list-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_list_volume_backups [Scenario]

Create and then list a volume backup.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-list-volume-backups-size"></a>size<a href="#ScenarioCinderVolumescreate-and-list-volume-backups-size"> [ref]</a>
      </td>
      <td>volume size in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-backups-detailed"></a>detailed<a href="#ScenarioCinderVolumescreate-and-list-volume-backups-detailed"> [ref]</a>
      </td>
      <td>True if detailed information about backup
should be listed
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-backups-do-delete"></a>do_delete<a href="#ScenarioCinderVolumescreate-and-list-volume-backups-do-delete"> [ref]</a>
      </td>
      <td>if True, a volume backup will be deleted
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-backups-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioCinderVolumescreate-and-list-volume-backups-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-list-volume-backups-create-backup-kwargs"></a>create_backup_kwargs<a href="#ScenarioCinderVolumescreate-and-list-volume-backups-create-backup-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume backup</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_restore_volume_backup [Scenario]

Restore volume backup.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-restore-volume-backup-size"></a>size<a href="#ScenarioCinderVolumescreate-and-restore-volume-backup-size"> [ref]</a>
      </td>
      <td>volume size in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-restore-volume-backup-do-delete"></a>do_delete<a href="#ScenarioCinderVolumescreate-and-restore-volume-backup-do-delete"> [ref]</a>
      </td>
      <td>if True, the volume and the volume backup will
be deleted after creation.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-restore-volume-backup-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioCinderVolumescreate-and-restore-volume-backup-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-restore-volume-backup-create-backup-kwargs"></a>create_backup_kwargs<a href="#ScenarioCinderVolumescreate-and-restore-volume-backup-create-backup-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume backup</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_update_volume [Scenario]

Create a volume and update its name and description.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-update-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-and-update-volume-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-update-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-and-update-volume-image"> [ref]</a>
      </td>
      <td>image to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-update-volume-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioCinderVolumescreate-and-update-volume-create-volume-kwargs"> [ref]</a>
      </td>
      <td>dict, to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-update-volume-update-volume-kwargs"></a>update_volume_kwargs<a href="#ScenarioCinderVolumescreate-and-update-volume-update-volume-kwargs"> [ref]</a>
      </td>
      <td>dict, to be used to update volume
update_volume_kwargs["update_name"]=True, if updating the
name of volume.
update_volume_kwargs["description"]="desp", if updating the
description of volume.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_upload_volume_to_image [Scenario]

Create and upload a volume to image.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-size"></a>size<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-size"> [ref]</a>
      </td>
      <td>volume size (integers, in GB), or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-image"></a>image<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-image"> [ref]</a>
      </td>
      <td>image to be used to create volume.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-force"></a>force<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-force"> [ref]</a>
      </td>
      <td>when set to True volume that is attached to an instance
could be uploaded to image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-container-format"></a>container_format<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-container-format"> [ref]</a>
      </td>
      <td>image container format
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-disk-format"></a>disk_format<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-disk-format"> [ref]</a>
      </td>
      <td>disk format for image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-do-delete"></a>do_delete<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-do-delete"> [ref]</a>
      </td>
      <td>deletes image and volume after uploading if True
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-and-upload-volume-to-image-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-and-upload-volume-to-image-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_from_volume_and_delete_volume [Scenario]

Create volume from volume and then delete it.

Scenario for testing volume clone.Optional 'min_sleep' and 'max_sleep'
parameters allow the scenario to simulate a pause between volume
creation and deletion (of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-from-volume-and-delete-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-from-volume-and-delete-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB), or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
Should be equal or bigger source volume size
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-from-volume-and-delete-volume-min-sleep"></a>min_sleep<a href="#ScenarioCinderVolumescreate-from-volume-and-delete-volume-min-sleep"> [ref]</a>
      </td>
      <td>minimum sleep time between volume creation and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-from-volume-and-delete-volume-max-sleep"></a>max_sleep<a href="#ScenarioCinderVolumescreate-from-volume-and-delete-volume-max-sleep"> [ref]</a>
      </td>
      <td>maximum sleep time between volume creation and
deletion (in seconds)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-from-volume-and-delete-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-from-volume-and-delete-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_nested_snapshots_and_attach_volume [Scenario]

Create a volume from snapshot and attach/detach the volume.

This scenario create vm, volume, create it's snapshot, attach volume,
then create new volume from existing snapshot and so on,
with defined nested level, after all detach and delete them.
volume->snapshot->volume->snapshot->volume ...

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-image"> [ref]</a>
      </td>
      <td>Glance image name to use for the VM
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-flavor"></a>flavor<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-size"> [ref]</a>
      </td>
      <td>Volume size - dictionary, contains two values:
   min - minimum size volumes will be created as;
   max - maximum size volumes will be created as.
default values: {"min": 1, "max": 5}
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-nested-level"></a>nested_level<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-nested-level"> [ref]</a>
      </td>
      <td>amount of nested levels
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-snapshot-kwargs"></a>create_snapshot_kwargs<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-snapshot-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a snapshot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-vm-params"></a>create_vm_params<a href="#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-vm-params"> [ref]</a>
      </td>
      <td>optional arguments for VM creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_snapshot_and_attach_volume [Scenario]

Create vm, volume, snapshot and attach/detach volume.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-snapshot-and-attach-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-snapshot-and-attach-volume-image"> [ref]</a>
      </td>
      <td>Glance image name to use for the VM
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-snapshot-and-attach-volume-flavor"></a>flavor<a href="#ScenarioCinderVolumescreate-snapshot-and-attach-volume-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-snapshot-and-attach-volume-volume-type"></a>volume_type<a href="#ScenarioCinderVolumescreate-snapshot-and-attach-volume-volume-type"> [ref]</a>
      </td>
      <td>Name of volume type to use
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-snapshot-and-attach-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-snapshot-and-attach-volume-size"> [ref]</a>
      </td>
      <td>Volume size - dictionary, contains two values:
   min - minimum size volumes will be created as;
   max - maximum size volumes will be created as.
default values: {"min": 1, "max": 5}
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-snapshot-and-attach-volume-create-vm-params"></a>create_vm_params<a href="#ScenarioCinderVolumescreate-snapshot-and-attach-volume-create-vm-params"> [ref]</a>
      </td>
      <td>optional arguments for VM creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-snapshot-and-attach-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-snapshot-and-attach-volume-kwargs"> [ref]</a>
      </td>
      <td>Optional parameters used during volume
snapshot creation.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume [Scenario]

Create a volume.

Good test to check how influence amount of active volumes on
performance of creating new.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-volume-size"></a>size<a href="#ScenarioCinderVolumescreate-volume-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-image"></a>image<a href="#ScenarioCinderVolumescreate-volume-image"> [ref]</a>
      </td>
      <td>image to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_and_clone [Scenario]

Create a volume, then clone it to another volume.

This creates a volume, then clone it to anothor volume,
and then clone the new volume to next volume...

> 0. create source volume (from image)
1. clone source volume to volume1
2. clone volume1 to volume2
3. clone volume2 to volume3
4. ...

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-volume-and-clone-size"></a>size<a href="#ScenarioCinderVolumescreate-volume-and-clone-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB) or
dictionary, must contain two values:
    min - minimum size volumes will be created as;
    max - maximum size volumes will be created as.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-and-clone-image"></a>image<a href="#ScenarioCinderVolumescreate-volume-and-clone-image"> [ref]</a>
      </td>
      <td>image to be used to create initial volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-and-clone-nested-level"></a>nested_level<a href="#ScenarioCinderVolumescreate-volume-and-clone-nested-level"> [ref]</a>
      </td>
      <td>amount of nested levels
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-and-clone-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-volume-and-clone-kwargs"> [ref]</a>
      </td>
      <td>optional args to create volumes</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_and_update_readonly_flag [Scenario]

Create a volume and then update its readonly flag.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-volume-and-update-readonly-flag-size"></a>size<a href="#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-size"> [ref]</a>
      </td>
      <td>volume size (integer, in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-and-update-readonly-flag-image"></a>image<a href="#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-image"> [ref]</a>
      </td>
      <td>image to be used to create volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-and-update-readonly-flag-read-only"></a>read_only<a href="#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-read-only"> [ref]</a>
      </td>
      <td>The value to indicate whether to update volume to
read-only access mode
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-and-update-readonly-flag-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_backup [Scenario]

Create a volume backup.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-volume-backup-size"></a>size<a href="#ScenarioCinderVolumescreate-volume-backup-size"> [ref]</a>
      </td>
      <td>volume size in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-backup-do-delete"></a>do_delete<a href="#ScenarioCinderVolumescreate-volume-backup-do-delete"> [ref]</a>
      </td>
      <td>if True, a volume and a volume backup will
be deleted after creation.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-backup-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioCinderVolumescreate-volume-backup-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-backup-create-backup-kwargs"></a>create_backup_kwargs<a href="#ScenarioCinderVolumescreate-volume-backup-create-backup-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume backup</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_from_snapshot [Scenario]

Create a volume-snapshot, then create a volume from this snapshot.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumescreate-volume-from-snapshot-do-delete"></a>do_delete<a href="#ScenarioCinderVolumescreate-volume-from-snapshot-do-delete"> [ref]</a>
      </td>
      <td>if True, a snapshot and a volume will
be deleted after creation.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-from-snapshot-create-snapshot-kwargs"></a>create_snapshot_kwargs<a href="#ScenarioCinderVolumescreate-volume-from-snapshot-create-snapshot-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a snapshot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumescreate-volume-from-snapshot-kwargs"></a>kwargs<a href="#ScenarioCinderVolumescreate-volume-from-snapshot-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a volume</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.list_transfers [Scenario]

List all transfers.

This simple scenario tests the "cinder transfer-list" command by
listing all the volume transfers.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeslist-transfers-detailed"></a>detailed<a href="#ScenarioCinderVolumeslist-transfers-detailed"> [ref]</a>
      </td>
      <td>If True, detailed information about volume transfer
should be listed
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeslist-transfers-search-opts"></a>search_opts<a href="#ScenarioCinderVolumeslist-transfers-search-opts"> [ref]</a>
      </td>
      <td>Search options to filter out volume transfers.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.list_types [Scenario]

List all volume types.

This simple scenario tests the cinder type-list command by listing
all the volume types.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeslist-types-search-opts"></a>search_opts<a href="#ScenarioCinderVolumeslist-types-search-opts"> [ref]</a>
      </td>
      <td>Options used when search for volume types
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumeslist-types-is-public"></a>is_public<a href="#ScenarioCinderVolumeslist-types-is-public"> [ref]</a>
      </td>
      <td>If query public volume type</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.list_volumes [Scenario]

List all volumes.

This simple scenario tests the cinder list command by listing
all the volumes.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumeslist-volumes-detailed"></a>detailed<a href="#ScenarioCinderVolumeslist-volumes-detailed"> [ref]</a>
      </td>
      <td>True if detailed information about volumes
should be listed
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.modify_volume_metadata [Scenario]

Modify a volume's metadata.

This requires a volume to be created with the volumes
context. Additionally, `sets * set_size` must be greater
than or equal to `deletes * delete_size`.

__Platform__: openstack

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
        <a name="ScenarioCinderVolumesmodify-volume-metadata-sets"></a>sets<a href="#ScenarioCinderVolumesmodify-volume-metadata-sets"> [ref]</a>
      </td>
      <td>how many set_metadata operations to perform
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumesmodify-volume-metadata-set-size"></a>set_size<a href="#ScenarioCinderVolumesmodify-volume-metadata-set-size"> [ref]</a>
      </td>
      <td>number of metadata keys to set in each
set_metadata operation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumesmodify-volume-metadata-deletes"></a>deletes<a href="#ScenarioCinderVolumesmodify-volume-metadata-deletes"> [ref]</a>
      </td>
      <td>how many delete_metadata operations to perform
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioCinderVolumesmodify-volume-metadata-delete-size"></a>delete_size<a href="#ScenarioCinderVolumesmodify-volume-metadata-delete-size"> [ref]</a>
      </td>
      <td>number of metadata keys to delete in each
delete_metadata operation
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### DesignateBasic.create_and_delete_domain [Scenario]

Create and then delete a domain.

Measure the performance of creating and deleting domains
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_records [Scenario]

Create and then delete records.

Measure the performance of creating and deleting records
with different level of load.

__Platform__: openstack

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
        <a name="ScenarioDesignateBasiccreate-and-delete-records-records-per-domain"></a>records_per_domain<a href="#ScenarioDesignateBasiccreate-and-delete-records-records-per-domain"> [ref]</a>
      </td>
      <td>Records to create pr domain.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_recordsets [Scenario]

Create and then delete recordsets.

Measure the performance of creating and deleting recordsets
with different level of load.

__Platform__: openstack

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
        <a name="ScenarioDesignateBasiccreate-and-delete-recordsets-recordsets-per-zone"></a>recordsets_per_zone<a href="#ScenarioDesignateBasiccreate-and-delete-recordsets-recordsets-per-zone"> [ref]</a>
      </td>
      <td>recordsets to create pr zone.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_server [Scenario]

Create and then delete a server.

Measure the performance of creating and deleting servers
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_zone [Scenario]

Create and then delete a zone.

Measure the performance of creating and deleting zones
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_list_domains [Scenario]

Create a domain and list all domains.

Measure the "designate domain-list" command performance.

If you have only 1 user in your context, you will
add 1 domain on every iteration. So you will have more
and more domain and will be able to measure the
performance of the "designate domain-list" command depending on
the number of domains owned by users.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_list_records [Scenario]

Create and then list records.

If you have only 1 user in your context, you will
add 1 record on every iteration. So you will have more
and more records and will be able to measure the
performance of the "designate record-list" command depending on
the number of domains/records owned by users.

__Platform__: openstack

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
        <a name="ScenarioDesignateBasiccreate-and-list-records-records-per-domain"></a>records_per_domain<a href="#ScenarioDesignateBasiccreate-and-list-records-records-per-domain"> [ref]</a>
      </td>
      <td>Records to create pr domain.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_list_recordsets [Scenario]

Create and then list recordsets.

If you have only 1 user in your context, you will
add 1 recordset on every iteration. So you will have more
and more recordsets and will be able to measure the
performance of the "openstack recordset list" command depending on
the number of zones/recordsets owned by users.

__Platform__: openstack

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
        <a name="ScenarioDesignateBasiccreate-and-list-recordsets-recordsets-per-zone"></a>recordsets_per_zone<a href="#ScenarioDesignateBasiccreate-and-list-recordsets-recordsets-per-zone"> [ref]</a>
      </td>
      <td>recordsets to create pr zone.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_list_servers [Scenario]

Create a Designate server and list all servers.

If you have only 1 user in your context, you will
add 1 server on every iteration. So you will have more
and more server and will be able to measure the
performance of the "designate server-list" command depending on
the number of servers owned by users.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_list_zones [Scenario]

Create a zone and list all zones.

Measure the "openstack zone list" command performance.

If you have only 1 user in your context, you will
add 1 zone on every iteration. So you will have more
and more zone and will be able to measure the
performance of the "openstack zone list" command depending on
the number of zones owned by users.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_update_domain [Scenario]

Create and then update a domain.

Measure the performance of creating and updating domains
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_domains [Scenario]

List Designate domains.

This simple scenario tests the designate domain-list command by listing
all the domains.

Suppose if we have 2 users in context and each has 2 domains
uploaded for them we will be able to test the performance of
designate domain-list command in this case.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_records [Scenario]

List Designate records.

This simple scenario tests the designate record-list command by listing
all the records in a domain.

Suppose if we have 2 users in context and each has 2 domains
uploaded for them we will be able to test the performance of
designate record-list command in this case.

__Platform__: openstack

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
        <a name="ScenarioDesignateBasiclist-records-domain-id"></a>domain_id<a href="#ScenarioDesignateBasiclist-records-domain-id"> [ref]</a>
      </td>
      <td>Domain ID</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_recordsets [Scenario]

List Designate recordsets.

This simple scenario tests the openstack recordset list command by
listing all the recordsets in a zone.

__Platform__: openstack

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
        <a name="ScenarioDesignateBasiclist-recordsets-zone-id"></a>zone_id<a href="#ScenarioDesignateBasiclist-recordsets-zone-id"> [ref]</a>
      </td>
      <td>Zone ID</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_servers [Scenario]

List Designate servers.

This simple scenario tests the designate server-list command by listing
all the servers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_zones [Scenario]

List Designate zones.

This simple scenario tests the openstack zone list command by listing
all the zones.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### Dummy.openstack [Scenario]

Do nothing and sleep for the given number of seconds (0 by default).

Dummy.dummy can be used for testing performance of different
ScenarioRunners and of the ability of rally to store a large
amount of results.

__Platform__: openstack

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
        <a name="ScenarioDummyopenstack-sleep"></a>sleep<a href="#ScenarioDummyopenstack-sleep"> [ref]</a>
      </td>
      <td>idle time of method (in seconds).</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.dummy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/dummy.py)

<hr />

#### EC2Servers.boot_server [Scenario]

Boot a server.

Assumes that cleanup is done elsewhere.

__Platform__: openstack

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
        <a name="ScenarioEC2Serversboot-server-image"></a>image<a href="#ScenarioEC2Serversboot-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioEC2Serversboot-server-flavor"></a>flavor<a href="#ScenarioEC2Serversboot-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioEC2Serversboot-server-kwargs"></a>kwargs<a href="#ScenarioEC2Serversboot-server-kwargs"> [ref]</a>
      </td>
      <td>optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ec2.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ec2/servers.py)

<hr />

#### EC2Servers.list_servers [Scenario]

List all servers.

This simple scenario tests the EC2 API list function by listing
all the servers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.ec2.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ec2/servers.py)

<hr />

#### ElasticsearchLogging.log_instance [Scenario]

Create nova instance and check it indexed in elasticsearch.

__Platform__: openstack

__Introduced in__: 1.2.0

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
        <a name="ScenarioElasticsearchLogginglog-instance-image"></a>image<a href="#ScenarioElasticsearchLogginglog-instance-image"> [ref]</a>
      </td>
      <td>image for server
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioElasticsearchLogginglog-instance-flavor"></a>flavor<a href="#ScenarioElasticsearchLogginglog-instance-flavor"> [ref]</a>
      </td>
      <td>flavor for server
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioElasticsearchLogginglog-instance-logging-vip"></a>logging_vip<a href="#ScenarioElasticsearchLogginglog-instance-logging-vip"> [ref]</a>
      </td>
      <td>logging system IP to check server name in
elasticsearch index
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioElasticsearchLogginglog-instance-elasticsearch-port"></a>elasticsearch_port<a href="#ScenarioElasticsearchLogginglog-instance-elasticsearch-port"> [ref]</a>
      </td>
      <td>elasticsearch port to use for check server
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioElasticsearchLogginglog-instance-sleep-time"></a>sleep_time<a href="#ScenarioElasticsearchLogginglog-instance-sleep-time"> [ref]</a>
      </td>
      <td>sleep time in seconds between elasticsearch request
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioElasticsearchLogginglog-instance-retries-total"></a>retries_total<a href="#ScenarioElasticsearchLogginglog-instance-retries-total"> [ref]</a>
      </td>
      <td>total number of retries to check server name in
elasticsearch
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.elasticsearch.logging](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/elasticsearch/logging.py)

<hr />

#### GlanceImages.create_and_deactivate_image [Scenario]

Create an image, then deactivate it.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-and-deactivate-image-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-and-deactivate-image-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-deactivate-image-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-and-deactivate-image-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-deactivate-image-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-and-deactivate-image-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-deactivate-image-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-and-deactivate-image-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-deactivate-image-min-disk"></a>min_disk<a href="#ScenarioGlanceImagescreate-and-deactivate-image-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-deactivate-image-min-ram"></a>min_ram<a href="#ScenarioGlanceImagescreate-and-deactivate-image-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_delete_image [Scenario]

Create and then delete an image.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-and-delete-image-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-and-delete-image-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-delete-image-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-and-delete-image-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-delete-image-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-and-delete-image-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-delete-image-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-and-delete-image-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-delete-image-min-disk"></a>min_disk<a href="#ScenarioGlanceImagescreate-and-delete-image-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-delete-image-min-ram"></a>min_ram<a href="#ScenarioGlanceImagescreate-and-delete-image-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-delete-image-properties"></a>properties<a href="#ScenarioGlanceImagescreate-and-delete-image-properties"> [ref]</a>
      </td>
      <td>A dict of image metadata properties to set
on the image
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_download_image [Scenario]

Create an image, then download data of the image.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-and-download-image-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-and-download-image-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-download-image-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-and-download-image-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-download-image-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-and-download-image-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-download-image-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-and-download-image-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-download-image-min-disk"></a>min_disk<a href="#ScenarioGlanceImagescreate-and-download-image-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-download-image-min-ram"></a>min_ram<a href="#ScenarioGlanceImagescreate-and-download-image-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-download-image-properties"></a>properties<a href="#ScenarioGlanceImagescreate-and-download-image-properties"> [ref]</a>
      </td>
      <td>A dict of image metadata properties to set
on the image
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_get_image [Scenario]

Create and get detailed information of an image.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-and-get-image-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-and-get-image-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-get-image-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-and-get-image-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-get-image-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-and-get-image-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-get-image-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-and-get-image-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-get-image-min-disk"></a>min_disk<a href="#ScenarioGlanceImagescreate-and-get-image-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-get-image-min-ram"></a>min_ram<a href="#ScenarioGlanceImagescreate-and-get-image-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-get-image-properties"></a>properties<a href="#ScenarioGlanceImagescreate-and-get-image-properties"> [ref]</a>
      </td>
      <td>A dict of image metadata properties to set
on the image
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_list_image [Scenario]

Create an image and then list all images.

Measure the "glance image-list" command performance.

If you have only 1 user in your context, you will
add 1 image on every iteration. So you will have more
and more images and will be able to measure the
performance of the "glance image-list" command depending on
the number of images owned by users.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-and-list-image-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-and-list-image-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-list-image-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-and-list-image-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-list-image-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-and-list-image-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-list-image-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-and-list-image-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-list-image-min-disk"></a>min_disk<a href="#ScenarioGlanceImagescreate-and-list-image-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-list-image-min-ram"></a>min_ram<a href="#ScenarioGlanceImagescreate-and-list-image-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-list-image-properties"></a>properties<a href="#ScenarioGlanceImagescreate-and-list-image-properties"> [ref]</a>
      </td>
      <td>A dict of image metadata properties to set
on the image
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_update_image [Scenario]

Create an image then update it.

Measure the "glance image-create" and "glance image-update" commands
performance.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-and-update-image-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-and-update-image-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-and-update-image-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-and-update-image-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-remove-props"></a>remove_props<a href="#ScenarioGlanceImagescreate-and-update-image-remove-props"> [ref]</a>
      </td>
      <td>List of property names to remove.
(It is only supported by Glance v2.)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-and-update-image-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-create-min-disk"></a>create_min_disk<a href="#ScenarioGlanceImagescreate-and-update-image-create-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-create-min-ram"></a>create_min_ram<a href="#ScenarioGlanceImagescreate-and-update-image-create-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-create-properties"></a>create_properties<a href="#ScenarioGlanceImagescreate-and-update-image-create-properties"> [ref]</a>
      </td>
      <td>A dict of image metadata properties to set
on the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-update-min-disk"></a>update_min_disk<a href="#ScenarioGlanceImagescreate-and-update-image-update-min-disk"> [ref]</a>
      </td>
      <td>The min disk of updated images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-and-update-image-update-min-ram"></a>update_min_ram<a href="#ScenarioGlanceImagescreate-and-update-image-update-min-ram"> [ref]</a>
      </td>
      <td>The min ram of updated images</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_image_and_boot_instances [Scenario]

Create an image and boot several instances from it.

__Platform__: openstack

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
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-container-format"></a>container_format<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-container-format"> [ref]</a>
      </td>
      <td>container format of image. Acceptable
formats: ami, ari, aki, bare, and ovf
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-image-location"></a>image_location<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-image-location"> [ref]</a>
      </td>
      <td>image file location
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-disk-format"></a>disk_format<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-disk-format"> [ref]</a>
      </td>
      <td>disk format of image. Acceptable formats:
ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-visibility"></a>visibility<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-visibility"> [ref]</a>
      </td>
      <td>The access permission for the created image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-min-disk"></a>min_disk<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-min-disk"> [ref]</a>
      </td>
      <td>The min disk of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-min-ram"></a>min_ram<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-min-ram"> [ref]</a>
      </td>
      <td>The min ram of created images
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-properties"></a>properties<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-properties"> [ref]</a>
      </td>
      <td>A dict of image metadata properties to set
on the image
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-flavor"></a>flavor<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-flavor"> [ref]</a>
      </td>
      <td>Nova flavor to be used to launch an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-number-instances"></a>number_instances<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-number-instances"> [ref]</a>
      </td>
      <td>number of Nova servers to boot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-boot-server-kwargs"> [ref]</a>
      </td>
      <td>optional parameters to boot server
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGlanceImagescreate-image-and-boot-instances-kwargs"></a>kwargs<a href="#ScenarioGlanceImagescreate-image-and-boot-instances-kwargs"> [ref]</a>
      </td>
      <td>optional parameters to create server (deprecated)</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.list_images [Scenario]

List all images.

This simple scenario tests the glance image-list command by listing
all the images.

Suppose if we have 2 users in context and each has 2 images
uploaded for them we will be able to test the performance of
glance image-list command in this case.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### Gnocchi.get_status [Scenario]

Get the status of measurements processing.

__Platform__: openstack

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
        <a name="ScenarioGnocchiget-status-detailed"></a>detailed<a href="#ScenarioGnocchiget-status-detailed"> [ref]</a>
      </td>
      <td>get detailed output</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.status](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/status.py)

<hr />

#### Gnocchi.list_capabilities [Scenario]

List supported aggregation methods.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.capabilities](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/capabilities.py)

<hr />

#### GnocchiArchivePolicy.create_archive_policy [Scenario]

Create archive policy.

__Platform__: openstack

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
        <a name="ScenarioGnocchiArchivePolicycreate-archive-policy-definition"></a>definition<a href="#ScenarioGnocchiArchivePolicycreate-archive-policy-definition"> [ref]</a>
      </td>
      <td>List of definitions
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiArchivePolicycreate-archive-policy-aggregation-methods"></a>aggregation_methods<a href="#ScenarioGnocchiArchivePolicycreate-archive-policy-aggregation-methods"> [ref]</a>
      </td>
      <td>List of aggregation methods</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy.py)

<hr />

#### GnocchiArchivePolicy.create_delete_archive_policy [Scenario]

Create archive policy and then delete it.

__Platform__: openstack

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
        <a name="ScenarioGnocchiArchivePolicycreate-delete-archive-policy-definition"></a>definition<a href="#ScenarioGnocchiArchivePolicycreate-delete-archive-policy-definition"> [ref]</a>
      </td>
      <td>List of definitions
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiArchivePolicycreate-delete-archive-policy-aggregation-methods"></a>aggregation_methods<a href="#ScenarioGnocchiArchivePolicycreate-delete-archive-policy-aggregation-methods"> [ref]</a>
      </td>
      <td>List of aggregation methods</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy.py)

<hr />

#### GnocchiArchivePolicy.list_archive_policy [Scenario]

List archive policies.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy.py)

<hr />

#### GnocchiArchivePolicyRule.create_archive_policy_rule [Scenario]

Create archive policy rule.

__Platform__: openstack

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
        <a name="ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-metric-pattern"></a>metric_pattern<a href="#ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-metric-pattern"> [ref]</a>
      </td>
      <td>Pattern for matching metrics
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-archive-policy-name"></a>archive_policy_name<a href="#ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-archive-policy-name"> [ref]</a>
      </td>
      <td>Archive policy name</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy_rule](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy_rule.py)

<hr />

#### GnocchiArchivePolicyRule.create_delete_archive_policy_rule [Scenario]

Create archive policy rule and then delete it.

__Platform__: openstack

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
        <a name="ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-metric-pattern"></a>metric_pattern<a href="#ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-metric-pattern"> [ref]</a>
      </td>
      <td>Pattern for matching metrics
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-archive-policy-name"></a>archive_policy_name<a href="#ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-archive-policy-name"> [ref]</a>
      </td>
      <td>Archive policy name</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy_rule](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy_rule.py)

<hr />

#### GnocchiArchivePolicyRule.list_archive_policy_rule [Scenario]

List archive policy rules.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy_rule](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy_rule.py)

<hr />

#### GnocchiMetric.create_delete_metric [Scenario]

Create metric and then delete it.

__Platform__: openstack

__Introduced in__: 1.1.0

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
        <a name="ScenarioGnocchiMetriccreate-delete-metric-archive-policy-name"></a>archive_policy_name<a href="#ScenarioGnocchiMetriccreate-delete-metric-archive-policy-name"> [ref]</a>
      </td>
      <td>Archive policy name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiMetriccreate-delete-metric-resource-id"></a>resource_id<a href="#ScenarioGnocchiMetriccreate-delete-metric-resource-id"> [ref]</a>
      </td>
      <td>The resource ID to attach the metric to
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiMetriccreate-delete-metric-unit"></a>unit<a href="#ScenarioGnocchiMetriccreate-delete-metric-unit"> [ref]</a>
      </td>
      <td>The unit of the metric</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.metric](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/metric.py)

<hr />

#### GnocchiMetric.create_metric [Scenario]

Create metric.

__Platform__: openstack

__Introduced in__: 1.1.0

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
        <a name="ScenarioGnocchiMetriccreate-metric-archive-policy-name"></a>archive_policy_name<a href="#ScenarioGnocchiMetriccreate-metric-archive-policy-name"> [ref]</a>
      </td>
      <td>Archive policy name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiMetriccreate-metric-resource-id"></a>resource_id<a href="#ScenarioGnocchiMetriccreate-metric-resource-id"> [ref]</a>
      </td>
      <td>The resource ID to attach the metric to
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGnocchiMetriccreate-metric-unit"></a>unit<a href="#ScenarioGnocchiMetriccreate-metric-unit"> [ref]</a>
      </td>
      <td>The unit of the metric</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.metric](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/metric.py)

<hr />

#### GnocchiMetric.list_metric [Scenario]

List metrics.

__Platform__: openstack

__Introduced in__: 1.1.0

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
        <a name="ScenarioGnocchiMetriclist-metric-limit"></a>limit<a href="#ScenarioGnocchiMetriclist-metric-limit"> [ref]</a>
      </td>
      <td>Maximum number of metrics to list</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.metric](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/metric.py)

<hr />

#### GnocchiResource.create_delete_resource [Scenario]

Create resource and then delete it.

__Platform__: openstack

__Introduced in__: 1.1.0

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
        <a name="ScenarioGnocchiResourcecreate-delete-resource-resource-type"></a>resource_type<a href="#ScenarioGnocchiResourcecreate-delete-resource-resource-type"> [ref]</a>
      </td>
      <td>Type of the resource</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.resource](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource.py)

<hr />

#### GnocchiResource.create_resource [Scenario]

Create resource.

__Platform__: openstack

__Introduced in__: 1.1.0

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
        <a name="ScenarioGnocchiResourcecreate-resource-resource-type"></a>resource_type<a href="#ScenarioGnocchiResourcecreate-resource-resource-type"> [ref]</a>
      </td>
      <td>Type of the resource</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.resource](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource.py)

<hr />

#### GnocchiResourceType.create_delete_resource_type [Scenario]

Create resource type and then delete it.

__Platform__: openstack

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
        <a name="ScenarioGnocchiResourceTypecreate-delete-resource-type-attributes"></a>attributes<a href="#ScenarioGnocchiResourceTypecreate-delete-resource-type-attributes"> [ref]</a>
      </td>
      <td>List of attributes</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.resource_type](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource_type.py)

<hr />

#### GnocchiResourceType.create_resource_type [Scenario]

Create resource type.

__Platform__: openstack

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
        <a name="ScenarioGnocchiResourceTypecreate-resource-type-attributes"></a>attributes<a href="#ScenarioGnocchiResourceTypecreate-resource-type-attributes"> [ref]</a>
      </td>
      <td>List of attributes</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.gnocchi.resource_type](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource_type.py)

<hr />

#### GnocchiResourceType.list_resource_type [Scenario]

List resource types.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.gnocchi.resource_type](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource_type.py)

<hr />

#### GrafanaMetrics.push_metric_from_instance [Scenario]

Create nova instance with pushing metric script as userdata.

Push metric to metrics storage using Pushgateway and check it in
Grafana.

__Platform__: openstack

__Introduced in__: 1.2.0

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
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-image"></a>image<a href="#ScenarioGrafanaMetricspush-metric-from-instance-image"> [ref]</a>
      </td>
      <td>image for server with userdata script
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-flavor"></a>flavor<a href="#ScenarioGrafanaMetricspush-metric-from-instance-flavor"> [ref]</a>
      </td>
      <td>flavor for server with userdata script
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-monitor-vip"></a>monitor_vip<a href="#ScenarioGrafanaMetricspush-metric-from-instance-monitor-vip"> [ref]</a>
      </td>
      <td>monitoring system IP to push metric
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-pushgateway-port"></a>pushgateway_port<a href="#ScenarioGrafanaMetricspush-metric-from-instance-pushgateway-port"> [ref]</a>
      </td>
      <td>Pushgateway port to use for pushing metric
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-grafana"></a>grafana<a href="#ScenarioGrafanaMetricspush-metric-from-instance-grafana"> [ref]</a>
      </td>
      <td>Grafana dict with creds and port to use for checking
metric. Format: {user: admin, password: pass, port: 9902}
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-datasource-id"></a>datasource_id<a href="#ScenarioGrafanaMetricspush-metric-from-instance-datasource-id"> [ref]</a>
      </td>
      <td>metrics storage datasource ID in Grafana
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-job-name"></a>job_name<a href="#ScenarioGrafanaMetricspush-metric-from-instance-job-name"> [ref]</a>
      </td>
      <td>job name to push metric in it
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-sleep-time"></a>sleep_time<a href="#ScenarioGrafanaMetricspush-metric-from-instance-sleep-time"> [ref]</a>
      </td>
      <td>sleep time between checking metrics in seconds
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-from-instance-retries-total"></a>retries_total<a href="#ScenarioGrafanaMetricspush-metric-from-instance-retries-total"> [ref]</a>
      </td>
      <td>total number of retries to check metric in
Grafana
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.grafana.metrics](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/grafana/metrics.py)

<hr />

#### GrafanaMetrics.push_metric_locally [Scenario]

Push random metric to Pushgateway locally and check it in Grafana.

__Platform__: openstack

__Introduced in__: 1.2.0

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
        <a name="ScenarioGrafanaMetricspush-metric-locally-monitor-vip"></a>monitor_vip<a href="#ScenarioGrafanaMetricspush-metric-locally-monitor-vip"> [ref]</a>
      </td>
      <td>monitoring system IP to push metric
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-locally-pushgateway-port"></a>pushgateway_port<a href="#ScenarioGrafanaMetricspush-metric-locally-pushgateway-port"> [ref]</a>
      </td>
      <td>Pushgateway port to use for pushing metric
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-locally-grafana"></a>grafana<a href="#ScenarioGrafanaMetricspush-metric-locally-grafana"> [ref]</a>
      </td>
      <td>Grafana dict with creds and port to use for checking
metric. Format: {user: admin, password: pass, port: 9902}
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-locally-datasource-id"></a>datasource_id<a href="#ScenarioGrafanaMetricspush-metric-locally-datasource-id"> [ref]</a>
      </td>
      <td>metrics storage datasource ID in Grafana
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-locally-job-name"></a>job_name<a href="#ScenarioGrafanaMetricspush-metric-locally-job-name"> [ref]</a>
      </td>
      <td>job name to push metric in it
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-locally-sleep-time"></a>sleep_time<a href="#ScenarioGrafanaMetricspush-metric-locally-sleep-time"> [ref]</a>
      </td>
      <td>sleep time between checking metrics in seconds
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioGrafanaMetricspush-metric-locally-retries-total"></a>retries_total<a href="#ScenarioGrafanaMetricspush-metric-locally-retries-total"> [ref]</a>
      </td>
      <td>total number of retries to check metric in
Grafana
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.grafana.metrics](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/grafana/metrics.py)

<hr />

#### HeatStacks.create_and_delete_stack [Scenario]

Create and then delete a stack.

Measure the "heat stack-create" and "heat stack-delete" commands
performance.

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-and-delete-stack-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-and-delete-stack-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-and-delete-stack-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-and-delete-stack-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-and-delete-stack-files"></a>files<a href="#ScenarioHeatStackscreate-and-delete-stack-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-and-delete-stack-environment"></a>environment<a href="#ScenarioHeatStackscreate-and-delete-stack-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_and_list_stack [Scenario]

Create a stack and then list all stacks.

Measure the "heat stack-create" and "heat stack-list" commands
performance.

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-and-list-stack-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-and-list-stack-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-and-list-stack-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-and-list-stack-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-and-list-stack-files"></a>files<a href="#ScenarioHeatStackscreate-and-list-stack-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-and-list-stack-environment"></a>environment<a href="#ScenarioHeatStackscreate-and-list-stack-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_check_delete_stack [Scenario]

Create, check and delete a stack.

Measure the performance of the following commands:
- heat stack-create
- heat action-check
- heat stack-delete

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-check-delete-stack-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-check-delete-stack-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-check-delete-stack-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-check-delete-stack-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-check-delete-stack-files"></a>files<a href="#ScenarioHeatStackscreate-check-delete-stack-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-check-delete-stack-environment"></a>environment<a href="#ScenarioHeatStackscreate-check-delete-stack-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_snapshot_restore_delete_stack [Scenario]

Create, snapshot-restore and then delete a stack.

Measure performance of the following commands:
heat stack-create
heat stack-snapshot
heat stack-restore
heat stack-delete

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-snapshot-restore-delete-stack-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-snapshot-restore-delete-stack-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-snapshot-restore-delete-stack-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-snapshot-restore-delete-stack-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-snapshot-restore-delete-stack-files"></a>files<a href="#ScenarioHeatStackscreate-snapshot-restore-delete-stack-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-snapshot-restore-delete-stack-environment"></a>environment<a href="#ScenarioHeatStackscreate-snapshot-restore-delete-stack-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_list_output [Scenario]

Create stack and list outputs by using new algorithm.

Measure performance of the following commands:
heat stack-create
heat output-list

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-stack-and-list-output-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-stack-and-list-output-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-list-output-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-stack-and-list-output-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-list-output-files"></a>files<a href="#ScenarioHeatStackscreate-stack-and-list-output-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-list-output-environment"></a>environment<a href="#ScenarioHeatStackscreate-stack-and-list-output-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_list_output_via_API [Scenario]

Create stack and list outputs by using old algorithm.

Measure performance of the following commands:
heat stack-create
heat output-list

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-stack-and-list-output-via-API-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-stack-and-list-output-via-API-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-list-output-via-API-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-stack-and-list-output-via-API-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-list-output-via-API-files"></a>files<a href="#ScenarioHeatStackscreate-stack-and-list-output-via-API-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-list-output-via-API-environment"></a>environment<a href="#ScenarioHeatStackscreate-stack-and-list-output-via-API-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_scale [Scenario]

Create an autoscaling stack and invoke a scaling policy.

Measure the performance of autoscaling webhooks.

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-stack-and-scale-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-stack-and-scale-template-path"> [ref]</a>
      </td>
      <td>path to template file that includes an
OS::Heat::AutoScalingGroup resource
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-scale-output-key"></a>output_key<a href="#ScenarioHeatStackscreate-stack-and-scale-output-key"> [ref]</a>
      </td>
      <td>the stack output key that corresponds to
the scaling webhook
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-scale-delta"></a>delta<a href="#ScenarioHeatStackscreate-stack-and-scale-delta"> [ref]</a>
      </td>
      <td>the number of instances the stack is expected to
change by.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-scale-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-stack-and-scale-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-scale-files"></a>files<a href="#ScenarioHeatStackscreate-stack-and-scale-files"> [ref]</a>
      </td>
      <td>files used in template (dict of file name to
file path)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-scale-environment"></a>environment<a href="#ScenarioHeatStackscreate-stack-and-scale-environment"> [ref]</a>
      </td>
      <td>stack environment definition (dict)</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_show_output [Scenario]

Create stack and show output by using new algorithm.

Measure performance of the following commands:
heat stack-create
heat output-show

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-stack-and-show-output-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-stack-and-show-output-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-output-key"></a>output_key<a href="#ScenarioHeatStackscreate-stack-and-show-output-output-key"> [ref]</a>
      </td>
      <td>the stack output key that corresponds to
the scaling webhook
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-stack-and-show-output-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-files"></a>files<a href="#ScenarioHeatStackscreate-stack-and-show-output-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-environment"></a>environment<a href="#ScenarioHeatStackscreate-stack-and-show-output-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_show_output_via_API [Scenario]

Create stack and show output by using old algorithm.

Measure performance of the following commands:
heat stack-create
heat output-show

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-stack-and-show-output-via-API-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-stack-and-show-output-via-API-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-via-API-output-key"></a>output_key<a href="#ScenarioHeatStackscreate-stack-and-show-output-via-API-output-key"> [ref]</a>
      </td>
      <td>the stack output key that corresponds to
the scaling webhook
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-via-API-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-stack-and-show-output-via-API-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-via-API-files"></a>files<a href="#ScenarioHeatStackscreate-stack-and-show-output-via-API-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-stack-and-show-output-via-API-environment"></a>environment<a href="#ScenarioHeatStackscreate-stack-and-show-output-via-API-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_suspend_resume_delete_stack [Scenario]

Create, suspend-resume and then delete a stack.

Measure performance of the following commands:
heat stack-create
heat action-suspend
heat action-resume
heat stack-delete

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-suspend-resume-delete-stack-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-suspend-resume-delete-stack-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-suspend-resume-delete-stack-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-suspend-resume-delete-stack-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-suspend-resume-delete-stack-files"></a>files<a href="#ScenarioHeatStackscreate-suspend-resume-delete-stack-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-suspend-resume-delete-stack-environment"></a>environment<a href="#ScenarioHeatStackscreate-suspend-resume-delete-stack-environment"> [ref]</a>
      </td>
      <td>stack environment definition</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_update_delete_stack [Scenario]

Create, update and then delete a stack.

Measure the "heat stack-create", "heat stack-update"
and "heat stack-delete" commands performance.

__Platform__: openstack

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
        <a name="ScenarioHeatStackscreate-update-delete-stack-template-path"></a>template_path<a href="#ScenarioHeatStackscreate-update-delete-stack-template-path"> [ref]</a>
      </td>
      <td>path to stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-updated-template-path"></a>updated_template_path<a href="#ScenarioHeatStackscreate-update-delete-stack-updated-template-path"> [ref]</a>
      </td>
      <td>path to updated stack template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-parameters"></a>parameters<a href="#ScenarioHeatStackscreate-update-delete-stack-parameters"> [ref]</a>
      </td>
      <td>parameters to use in heat template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-updated-parameters"></a>updated_parameters<a href="#ScenarioHeatStackscreate-update-delete-stack-updated-parameters"> [ref]</a>
      </td>
      <td>parameters to use in updated heat template
If not specified then parameters will be
used instead
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-files"></a>files<a href="#ScenarioHeatStackscreate-update-delete-stack-files"> [ref]</a>
      </td>
      <td>files used in template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-updated-files"></a>updated_files<a href="#ScenarioHeatStackscreate-update-delete-stack-updated-files"> [ref]</a>
      </td>
      <td>files used in updated template. If not specified
files value will be used instead
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-environment"></a>environment<a href="#ScenarioHeatStackscreate-update-delete-stack-environment"> [ref]</a>
      </td>
      <td>stack environment definition
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioHeatStackscreate-update-delete-stack-updated-environment"></a>updated_environment<a href="#ScenarioHeatStackscreate-update-delete-stack-updated-environment"> [ref]</a>
      </td>
      <td>environment definition for updated stack</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.list_stacks_and_events [Scenario]

List events from tenant stacks.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.list_stacks_and_resources [Scenario]

List all resources from tenant stacks.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### IronicNodes.create_and_delete_node [Scenario]

Create and delete node.

__Platform__: openstack

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
        <a name="ScenarioIronicNodescreate-and-delete-node-driver"></a>driver<a href="#ScenarioIronicNodescreate-and-delete-node-driver"> [ref]</a>
      </td>
      <td>The name of the driver used to manage this Node.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-delete-node-properties"></a>properties<a href="#ScenarioIronicNodescreate-and-delete-node-properties"> [ref]</a>
      </td>
      <td>Key/value pair describing the physical
characteristics of the node.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-delete-node-kwargs"></a>kwargs<a href="#ScenarioIronicNodescreate-and-delete-node-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for node creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ironic.nodes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ironic/nodes.py)

<hr />

#### IronicNodes.create_and_list_node [Scenario]

Create and list nodes.

__Platform__: openstack

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
        <a name="ScenarioIronicNodescreate-and-list-node-driver"></a>driver<a href="#ScenarioIronicNodescreate-and-list-node-driver"> [ref]</a>
      </td>
      <td>The name of the driver used to manage this Node.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-properties"></a>properties<a href="#ScenarioIronicNodescreate-and-list-node-properties"> [ref]</a>
      </td>
      <td>Key/value pair describing the physical
characteristics of the node.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-associated"></a>associated<a href="#ScenarioIronicNodescreate-and-list-node-associated"> [ref]</a>
      </td>
      <td>Optional argument of list request. Either a Boolean
or a string representation of a Boolean that indicates whether to
return a list of associated (True or "True") or unassociated
(False or "False") nodes.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-maintenance"></a>maintenance<a href="#ScenarioIronicNodescreate-and-list-node-maintenance"> [ref]</a>
      </td>
      <td>Optional argument of list request. Either a Boolean
or a string representation of a Boolean that indicates whether
to return nodes in maintenance mode (True or "True"), or not in
maintenance mode (False or "False").
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-detail"></a>detail<a href="#ScenarioIronicNodescreate-and-list-node-detail"> [ref]</a>
      </td>
      <td>Optional, boolean whether to return detailed
information about nodes.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-sort-dir"></a>sort_dir<a href="#ScenarioIronicNodescreate-and-list-node-sort-dir"> [ref]</a>
      </td>
      <td>Optional, direction of sorting, either 'asc' (the
default) or 'desc'.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-marker"></a>marker<a href="#ScenarioIronicNodescreate-and-list-node-marker"> [ref]</a>
      </td>
      <td>DEPRECATED since Rally 0.10.0
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-limit"></a>limit<a href="#ScenarioIronicNodescreate-and-list-node-limit"> [ref]</a>
      </td>
      <td>DEPRECATED since Rally 0.10.0
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-sort-key"></a>sort_key<a href="#ScenarioIronicNodescreate-and-list-node-sort-key"> [ref]</a>
      </td>
      <td>DEPRECATED since Rally 0.10.0
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioIronicNodescreate-and-list-node-kwargs"></a>kwargs<a href="#ScenarioIronicNodescreate-and-list-node-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for node creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.ironic.nodes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ironic/nodes.py)

<hr />

#### K8sPods.create_pods [Scenario]

create pods and wait for them to be ready.

__Platform__: openstack

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
        <a name="ScenarioK8sPodscreate-pods-manifests"></a>manifests<a href="#ScenarioK8sPodscreate-pods-manifests"> [ref]</a>
      </td>
      <td>manifest files used to create the pods</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.magnum.k8s_pods](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/k8s_pods.py)

<hr />

#### K8sPods.create_rcs [Scenario]

create rcs and wait for them to be ready.

__Platform__: openstack

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
        <a name="ScenarioK8sPodscreate-rcs-manifests"></a>manifests<a href="#ScenarioK8sPodscreate-rcs-manifests"> [ref]</a>
      </td>
      <td>manifest files use to create the rcs</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.magnum.k8s_pods](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/k8s_pods.py)

<hr />

#### K8sPods.list_pods [Scenario]

List all pods.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.magnum.k8s_pods](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/k8s_pods.py)

<hr />

#### KeystoneBasic.add_and_remove_user_role [Scenario]

Create a user role add to a user and disassociate.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.authenticate_user_and_validate_token [Scenario]

Authenticate and validate a keystone token.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_add_and_list_user_roles [Scenario]

Create user role, add it and list user roles for given user.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_delete_ec2credential [Scenario]

Create and delete keystone ec2-credential.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_delete_role [Scenario]

Create a user role and delete it.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_delete_service [Scenario]

Create and delete service.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-delete-service-service-type"></a>service_type<a href="#ScenarioKeystoneBasiccreate-and-delete-service-service-type"> [ref]</a>
      </td>
      <td>type of the service
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKeystoneBasiccreate-and-delete-service-description"></a>description<a href="#ScenarioKeystoneBasiccreate-and-delete-service-description"> [ref]</a>
      </td>
      <td>description of the service</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_get_role [Scenario]

Create a user role and get it detailed information.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-get-role-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-and-get-role-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for roles creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_ec2credentials [Scenario]

Create and List all keystone ec2-credentials.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_roles [Scenario]

Create a role, then list all roles.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-list-roles-create-role-kwargs"></a>create_role_kwargs<a href="#ScenarioKeystoneBasiccreate-and-list-roles-create-role-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for
roles create
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKeystoneBasiccreate-and-list-roles-list-role-kwargs"></a>list_role_kwargs<a href="#ScenarioKeystoneBasiccreate-and-list-roles-list-role-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for roles list</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_services [Scenario]

Create and list services.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-list-services-service-type"></a>service_type<a href="#ScenarioKeystoneBasiccreate-and-list-services-service-type"> [ref]</a>
      </td>
      <td>type of the service
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKeystoneBasiccreate-and-list-services-description"></a>description<a href="#ScenarioKeystoneBasiccreate-and-list-services-description"> [ref]</a>
      </td>
      <td>description of the service</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_tenants [Scenario]

Create a keystone tenant with random name and list all tenants.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-list-tenants-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-and-list-tenants-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_users [Scenario]

Create a keystone user with random name and list all users.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-list-users-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-and-list-users-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters to create users like
"tenant_id", "enabled".
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_update_user [Scenario]

Create user and update the user.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-and-update-user-create-user-kwargs"></a>create_user_kwargs<a href="#ScenarioKeystoneBasiccreate-and-update-user-create-user-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for user
creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKeystoneBasiccreate-and-update-user-update-user-kwargs"></a>update_user_kwargs<a href="#ScenarioKeystoneBasiccreate-and-update-user-update-user-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for user
updation
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_delete_user [Scenario]

Create a keystone user with random name and then delete it.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-delete-user-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-delete-user-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters to create users like
"tenant_id", "enabled".
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_tenant [Scenario]

Create a keystone tenant with random name.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-tenant-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-tenant-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_tenant_with_users [Scenario]

Create a keystone tenant and several users belonging to it.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-tenant-with-users-users-per-tenant"></a>users_per_tenant<a href="#ScenarioKeystoneBasiccreate-tenant-with-users-users-per-tenant"> [ref]</a>
      </td>
      <td>number of users to create for the tenant
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKeystoneBasiccreate-tenant-with-users-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-tenant-with-users-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters for tenant creation
</td>
    </tr>
  </tbody>
</table>


__Returns__:  
keystone tenant instance

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_update_and_delete_tenant [Scenario]

Create, update and delete tenant.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-update-and-delete-tenant-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-update-and-delete-tenant-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters for tenant creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_user [Scenario]

Create a keystone user with random name.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-user-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-user-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters to create users like
"tenant_id", "enabled".
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_user_set_enabled_and_delete [Scenario]

Create a keystone user, enable or disable it, and delete it.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-enabled"></a>enabled<a href="#ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-enabled"> [ref]</a>
      </td>
      <td>Initial state of user 'enabled' flag. The user
will be created with 'enabled' set to this
value, and then it will be toggled.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-kwargs"></a>kwargs<a href="#ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-kwargs"> [ref]</a>
      </td>
      <td>Other optional parameters to create user.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_user_update_password [Scenario]

Create user and update password for that user.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.get_entities [Scenario]

Get instance of a tenant, user, role and service by id's.

An ephemeral tenant, user, and role are each created. By
default, fetches the 'keystone' service. This can be
overridden (for instance, to get the 'Identity Service'
service on older OpenStack), or None can be passed explicitly
to service_name to create a new service and then query it by
ID.

__Platform__: openstack

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
        <a name="ScenarioKeystoneBasicget-entities-service-name"></a>service_name<a href="#ScenarioKeystoneBasicget-entities-service-name"> [ref]</a>
      </td>
      <td>The name of the service to get by ID; or
None, to create an ephemeral service and
get it by ID.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### MagnumClusterTemplates.list_cluster_templates [Scenario]

List all cluster_templates.

Measure the "magnum cluster_template-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioMagnumClusterTemplateslist-cluster-templates-limit"></a>limit<a href="#ScenarioMagnumClusterTemplateslist-cluster-templates-limit"> [ref]</a>
      </td>
      <td>(Optional) The maximum number of results to return
          per request, if:

1) limit > 0, the maximum number of cluster_templates to return.
2) limit param is NOT specified (None), the number of items
   returned respect the maximum imposed by the Magnum API
   (see Magnum's api.max_limit option).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMagnumClusterTemplateslist-cluster-templates-kwargs"></a>kwargs<a href="#ScenarioMagnumClusterTemplateslist-cluster-templates-kwargs"> [ref]</a>
      </td>
      <td>optional additional arguments for cluster_templates
listing
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.magnum.cluster_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/cluster_templates.py)

<hr />

#### MagnumClusters.create_and_list_clusters [Scenario]

create cluster and then list all clusters.

__Platform__: openstack

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
        <a name="ScenarioMagnumClusterscreate-and-list-clusters-node-count"></a>node_count<a href="#ScenarioMagnumClusterscreate-and-list-clusters-node-count"> [ref]</a>
      </td>
      <td>the cluster node count.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMagnumClusterscreate-and-list-clusters-cluster-template-uuid"></a>cluster_template_uuid<a href="#ScenarioMagnumClusterscreate-and-list-clusters-cluster-template-uuid"> [ref]</a>
      </td>
      <td>optional, if user want to use an existing
cluster_template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMagnumClusterscreate-and-list-clusters-kwargs"></a>kwargs<a href="#ScenarioMagnumClusterscreate-and-list-clusters-kwargs"> [ref]</a>
      </td>
      <td>optional additional arguments for cluster creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.magnum.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/clusters.py)

<hr />

#### MagnumClusters.list_clusters [Scenario]

List all clusters.

Measure the "magnum clusters-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioMagnumClusterslist-clusters-limit"></a>limit<a href="#ScenarioMagnumClusterslist-clusters-limit"> [ref]</a>
      </td>
      <td>(Optional) The maximum number of results to return
          per request, if:

1) limit > 0, the maximum number of clusters to return.
2) limit param is NOT specified (None), the number of items
   returned respect the maximum imposed by the Magnum API
   (see Magnum's api.max_limit option).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMagnumClusterslist-clusters-kwargs"></a>kwargs<a href="#ScenarioMagnumClusterslist-clusters-kwargs"> [ref]</a>
      </td>
      <td>optional additional arguments for clusters listing</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.magnum.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/clusters.py)

<hr />

#### ManilaShares.attach_security_service_to_share_network [Scenario]

Attaches security service to share network.

__Platform__: openstack

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
        <a name="ScenarioManilaSharesattach-security-service-to-share-network-security-service-type"></a>security_service_type<a href="#ScenarioManilaSharesattach-security-service-to-share-network-security-service-type"> [ref]</a>
      </td>
      <td>type of security service to use.
Should be one of following: 'ldap', 'kerberos' or
'active_directory'.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_delete_share [Scenario]

Create and delete a share.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between share creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-and-delete-share-share-proto"></a>share_proto<a href="#ScenarioManilaSharescreate-and-delete-share-share-proto"> [ref]</a>
      </td>
      <td>share protocol, valid values are NFS, CIFS,
GlusterFS and HDFS
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-delete-share-size"></a>size<a href="#ScenarioManilaSharescreate-and-delete-share-size"> [ref]</a>
      </td>
      <td>share size in GB, should be greater than 0
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-delete-share-min-sleep"></a>min_sleep<a href="#ScenarioManilaSharescreate-and-delete-share-min-sleep"> [ref]</a>
      </td>
      <td>minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-delete-share-max-sleep"></a>max_sleep<a href="#ScenarioManilaSharescreate-and-delete-share-max-sleep"> [ref]</a>
      </td>
      <td>maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-delete-share-kwargs"></a>kwargs<a href="#ScenarioManilaSharescreate-and-delete-share-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a share</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_extend_share [Scenario]

Create and extend a share.

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-and-extend-share-share-proto"></a>share_proto<a href="#ScenarioManilaSharescreate-and-extend-share-share-proto"> [ref]</a>
      </td>
      <td>share protocol for new share
available values are NFS, CIFS, CephFS, GlusterFS and HDFS.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-size"></a>size<a href="#ScenarioManilaSharescreate-and-extend-share-size"> [ref]</a>
      </td>
      <td>size in GiB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-new-size"></a>new_size<a href="#ScenarioManilaSharescreate-and-extend-share-new-size"> [ref]</a>
      </td>
      <td>new size of the share in GiB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-snapshot-id"></a>snapshot_id<a href="#ScenarioManilaSharescreate-and-extend-share-snapshot-id"> [ref]</a>
      </td>
      <td>ID of the snapshot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-description"></a>description<a href="#ScenarioManilaSharescreate-and-extend-share-description"> [ref]</a>
      </td>
      <td>description of a share
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-metadata"></a>metadata<a href="#ScenarioManilaSharescreate-and-extend-share-metadata"> [ref]</a>
      </td>
      <td>optional metadata to set on share creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-share-network"></a>share_network<a href="#ScenarioManilaSharescreate-and-extend-share-share-network"> [ref]</a>
      </td>
      <td>either instance of ShareNetwork or text with ID
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-share-type"></a>share_type<a href="#ScenarioManilaSharescreate-and-extend-share-share-type"> [ref]</a>
      </td>
      <td>either instance of ShareType or text with ID
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-is-public"></a>is_public<a href="#ScenarioManilaSharescreate-and-extend-share-is-public"> [ref]</a>
      </td>
      <td>whether to set share as public or not.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-availability-zone"></a>availability_zone<a href="#ScenarioManilaSharescreate-and-extend-share-availability-zone"> [ref]</a>
      </td>
      <td>availability zone of the share
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-extend-share-share-group-id"></a>share_group_id<a href="#ScenarioManilaSharescreate-and-extend-share-share-group-id"> [ref]</a>
      </td>
      <td>ID of the share group to which the share
should belong
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_list_share [Scenario]

Create a share and list all shares.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between share creation and list
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-and-list-share-share-proto"></a>share_proto<a href="#ScenarioManilaSharescreate-and-list-share-share-proto"> [ref]</a>
      </td>
      <td>share protocol, valid values are NFS, CIFS,
GlusterFS and HDFS
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-list-share-size"></a>size<a href="#ScenarioManilaSharescreate-and-list-share-size"> [ref]</a>
      </td>
      <td>share size in GB, should be greater than 0
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-list-share-min-sleep"></a>min_sleep<a href="#ScenarioManilaSharescreate-and-list-share-min-sleep"> [ref]</a>
      </td>
      <td>minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-list-share-max-sleep"></a>max_sleep<a href="#ScenarioManilaSharescreate-and-list-share-max-sleep"> [ref]</a>
      </td>
      <td>maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-list-share-detailed"></a>detailed<a href="#ScenarioManilaSharescreate-and-list-share-detailed"> [ref]</a>
      </td>
      <td>defines whether to get detailed list of shares or not
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-list-share-kwargs"></a>kwargs<a href="#ScenarioManilaSharescreate-and-list-share-kwargs"> [ref]</a>
      </td>
      <td>optional args to create a share</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_shrink_share [Scenario]

Create and shrink a share.

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-and-shrink-share-share-proto"></a>share_proto<a href="#ScenarioManilaSharescreate-and-shrink-share-share-proto"> [ref]</a>
      </td>
      <td>share protocol for new share
available values are NFS, CIFS, CephFS, GlusterFS and HDFS.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-size"></a>size<a href="#ScenarioManilaSharescreate-and-shrink-share-size"> [ref]</a>
      </td>
      <td>size in GiB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-new-size"></a>new_size<a href="#ScenarioManilaSharescreate-and-shrink-share-new-size"> [ref]</a>
      </td>
      <td>new size of the share in GiB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-snapshot-id"></a>snapshot_id<a href="#ScenarioManilaSharescreate-and-shrink-share-snapshot-id"> [ref]</a>
      </td>
      <td>ID of the snapshot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-description"></a>description<a href="#ScenarioManilaSharescreate-and-shrink-share-description"> [ref]</a>
      </td>
      <td>description of a share
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-metadata"></a>metadata<a href="#ScenarioManilaSharescreate-and-shrink-share-metadata"> [ref]</a>
      </td>
      <td>optional metadata to set on share creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-share-network"></a>share_network<a href="#ScenarioManilaSharescreate-and-shrink-share-share-network"> [ref]</a>
      </td>
      <td>either instance of ShareNetwork or text with ID
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-share-type"></a>share_type<a href="#ScenarioManilaSharescreate-and-shrink-share-share-type"> [ref]</a>
      </td>
      <td>either instance of ShareType or text with ID
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-is-public"></a>is_public<a href="#ScenarioManilaSharescreate-and-shrink-share-is-public"> [ref]</a>
      </td>
      <td>whether to set share as public or not.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-availability-zone"></a>availability_zone<a href="#ScenarioManilaSharescreate-and-shrink-share-availability-zone"> [ref]</a>
      </td>
      <td>availability zone of the share
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-and-shrink-share-share-group-id"></a>share_group_id<a href="#ScenarioManilaSharescreate-and-shrink-share-share-group-id"> [ref]</a>
      </td>
      <td>ID of the share group to which the share
should belong
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_security_service_and_delete [Scenario]

Creates security service and then deletes.

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-security-service-and-delete-security-service-type"></a>security_service_type<a href="#ScenarioManilaSharescreate-security-service-and-delete-security-service-type"> [ref]</a>
      </td>
      <td>security service type, permitted values
are 'ldap', 'kerberos' or 'active_directory'.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-security-service-and-delete-dns-ip"></a>dns_ip<a href="#ScenarioManilaSharescreate-security-service-and-delete-dns-ip"> [ref]</a>
      </td>
      <td>dns ip address used inside tenant's network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-security-service-and-delete-server"></a>server<a href="#ScenarioManilaSharescreate-security-service-and-delete-server"> [ref]</a>
      </td>
      <td>security service server ip address or hostname
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-security-service-and-delete-domain"></a>domain<a href="#ScenarioManilaSharescreate-security-service-and-delete-domain"> [ref]</a>
      </td>
      <td>security service domain
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-security-service-and-delete-user"></a>user<a href="#ScenarioManilaSharescreate-security-service-and-delete-user"> [ref]</a>
      </td>
      <td>security identifier used by tenant
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-security-service-and-delete-password"></a>password<a href="#ScenarioManilaSharescreate-security-service-and-delete-password"> [ref]</a>
      </td>
      <td>password used by user
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-security-service-and-delete-description"></a>description<a href="#ScenarioManilaSharescreate-security-service-and-delete-description"> [ref]</a>
      </td>
      <td>security service description</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_share_network_and_delete [Scenario]

Creates share network and then deletes.

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-share-network-and-delete-neutron-net-id"></a>neutron_net_id<a href="#ScenarioManilaSharescreate-share-network-and-delete-neutron-net-id"> [ref]</a>
      </td>
      <td>ID of Neutron network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-delete-neutron-subnet-id"></a>neutron_subnet_id<a href="#ScenarioManilaSharescreate-share-network-and-delete-neutron-subnet-id"> [ref]</a>
      </td>
      <td>ID of Neutron subnet
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-delete-nova-net-id"></a>nova_net_id<a href="#ScenarioManilaSharescreate-share-network-and-delete-nova-net-id"> [ref]</a>
      </td>
      <td>ID of Nova network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-delete-description"></a>description<a href="#ScenarioManilaSharescreate-share-network-and-delete-description"> [ref]</a>
      </td>
      <td>share network description</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_share_network_and_list [Scenario]

Creates share network and then lists it.

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-share-network-and-list-neutron-net-id"></a>neutron_net_id<a href="#ScenarioManilaSharescreate-share-network-and-list-neutron-net-id"> [ref]</a>
      </td>
      <td>ID of Neutron network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-list-neutron-subnet-id"></a>neutron_subnet_id<a href="#ScenarioManilaSharescreate-share-network-and-list-neutron-subnet-id"> [ref]</a>
      </td>
      <td>ID of Neutron subnet
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-list-nova-net-id"></a>nova_net_id<a href="#ScenarioManilaSharescreate-share-network-and-list-nova-net-id"> [ref]</a>
      </td>
      <td>ID of Nova network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-list-description"></a>description<a href="#ScenarioManilaSharescreate-share-network-and-list-description"> [ref]</a>
      </td>
      <td>share network description
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-list-detailed"></a>detailed<a href="#ScenarioManilaSharescreate-share-network-and-list-detailed"> [ref]</a>
      </td>
      <td>defines either to return detailed list of
objects or not.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-network-and-list-search-opts"></a>search_opts<a href="#ScenarioManilaSharescreate-share-network-and-list-search-opts"> [ref]</a>
      </td>
      <td>container of search opts such as
"name", "nova_net_id", "neutron_net_id", etc.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_share_then_allow_and_deny_access [Scenario]

Create a share and allow and deny access to it.

__Platform__: openstack

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
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-proto"></a>share_proto<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-proto"> [ref]</a>
      </td>
      <td>share protocol for new share
available values are NFS, CIFS, CephFS, GlusterFS and HDFS.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-type"></a>access_type<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-type"> [ref]</a>
      </td>
      <td>represents the access type (e.g: 'ip', 'domain'...)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-access"></a>access<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-access"> [ref]</a>
      </td>
      <td>represents the object (e.g: '127.0.0.1'...)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-level"></a>access_level<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-level"> [ref]</a>
      </td>
      <td>access level to the share (e.g: 'rw', 'ro')
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-size"></a>size<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-size"> [ref]</a>
      </td>
      <td>size in GiB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-new-size"></a>new_size<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-new-size"> [ref]</a>
      </td>
      <td>new size of the share in GiB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-snapshot-id"></a>snapshot_id<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-snapshot-id"> [ref]</a>
      </td>
      <td>ID of the snapshot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-description"></a>description<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-description"> [ref]</a>
      </td>
      <td>description of a share
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-metadata"></a>metadata<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-metadata"> [ref]</a>
      </td>
      <td>optional metadata to set on share creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-network"></a>share_network<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-network"> [ref]</a>
      </td>
      <td>either instance of ShareNetwork or text with ID
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-type"></a>share_type<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-type"> [ref]</a>
      </td>
      <td>either instance of ShareType or text with ID
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-is-public"></a>is_public<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-is-public"> [ref]</a>
      </td>
      <td>whether to set share as public or not.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-availability-zone"></a>availability_zone<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-availability-zone"> [ref]</a>
      </td>
      <td>availability zone of the share
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-group-id"></a>share_group_id<a href="#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-group-id"> [ref]</a>
      </td>
      <td>ID of the share group to which the share
should belong
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.list_share_servers [Scenario]

Lists share servers.

Requires admin creds.

__Platform__: openstack

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
        <a name="ScenarioManilaShareslist-share-servers-search-opts"></a>search_opts<a href="#ScenarioManilaShareslist-share-servers-search-opts"> [ref]</a>
      </td>
      <td>container of following search opts:
"host", "status", "share_network" and "project_id".
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.list_shares [Scenario]

Basic scenario for 'share list' operation.

__Platform__: openstack

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
        <a name="ScenarioManilaShareslist-shares-detailed"></a>detailed<a href="#ScenarioManilaShareslist-shares-detailed"> [ref]</a>
      </td>
      <td>defines either to return detailed list of
objects or not.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaShareslist-shares-search-opts"></a>search_opts<a href="#ScenarioManilaShareslist-shares-search-opts"> [ref]</a>
      </td>
      <td>container of search opts such as
"name", "host", "share_type", etc.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.set_and_delete_metadata [Scenario]

Sets and deletes share metadata.

This requires a share to be created with the shares
context. Additionally, `sets * set_size` must be greater
than or equal to `deletes * delete_size`.

__Platform__: openstack

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
        <a name="ScenarioManilaSharesset-and-delete-metadata-sets"></a>sets<a href="#ScenarioManilaSharesset-and-delete-metadata-sets"> [ref]</a>
      </td>
      <td>how many set_metadata operations to perform
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharesset-and-delete-metadata-set-size"></a>set_size<a href="#ScenarioManilaSharesset-and-delete-metadata-set-size"> [ref]</a>
      </td>
      <td>number of metadata keys to set in each
set_metadata operation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharesset-and-delete-metadata-delete-size"></a>delete_size<a href="#ScenarioManilaSharesset-and-delete-metadata-delete-size"> [ref]</a>
      </td>
      <td>number of metadata keys to delete in each
delete_metadata operation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharesset-and-delete-metadata-key-min-length"></a>key_min_length<a href="#ScenarioManilaSharesset-and-delete-metadata-key-min-length"> [ref]</a>
      </td>
      <td>minimal size of metadata key to set
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharesset-and-delete-metadata-key-max-length"></a>key_max_length<a href="#ScenarioManilaSharesset-and-delete-metadata-key-max-length"> [ref]</a>
      </td>
      <td>maximum size of metadata key to set
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharesset-and-delete-metadata-value-min-length"></a>value_min_length<a href="#ScenarioManilaSharesset-and-delete-metadata-value-min-length"> [ref]</a>
      </td>
      <td>minimal size of metadata value to set
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioManilaSharesset-and-delete-metadata-value-max-length"></a>value_max_length<a href="#ScenarioManilaSharesset-and-delete-metadata-value-max-length"> [ref]</a>
      </td>
      <td>maximum size of metadata value to set</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### MistralExecutions.create_execution_from_workbook [Scenario]

Scenario tests execution creation and deletion.

This scenario is a very useful tool to measure the
"mistral execution-create" and "mistral execution-delete"
commands performance.

__Platform__: openstack

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
        <a name="ScenarioMistralExecutionscreate-execution-from-workbook-definition"></a>definition<a href="#ScenarioMistralExecutionscreate-execution-from-workbook-definition"> [ref]</a>
      </td>
      <td>string (yaml string) representation of given file
content (Mistral workbook definition)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionscreate-execution-from-workbook-workflow-name"></a>workflow_name<a href="#ScenarioMistralExecutionscreate-execution-from-workbook-workflow-name"> [ref]</a>
      </td>
      <td>string the workflow name to execute. Should be
one of the to workflows in the definition. If no
 workflow_name is passed, one of the workflows in
 the definition will be taken.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionscreate-execution-from-workbook-wf-input"></a>wf_input<a href="#ScenarioMistralExecutionscreate-execution-from-workbook-wf-input"> [ref]</a>
      </td>
      <td>file containing a json string of mistral workflow
input
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionscreate-execution-from-workbook-params"></a>params<a href="#ScenarioMistralExecutionscreate-execution-from-workbook-params"> [ref]</a>
      </td>
      <td>file containing a json string of mistral params
(the string is the place to pass the environment)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionscreate-execution-from-workbook-do-delete"></a>do_delete<a href="#ScenarioMistralExecutionscreate-execution-from-workbook-do-delete"> [ref]</a>
      </td>
      <td>if False than it allows to check performance
in "create only" mode.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.mistral.executions](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/executions.py)

<hr />

#### MistralExecutions.list_executions [Scenario]

Scenario test mistral execution-list command.

This simple scenario tests the Mistral execution-list
command by listing all the executions.

__Platform__: openstack

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
        <a name="ScenarioMistralExecutionslist-executions-marker"></a>marker<a href="#ScenarioMistralExecutionslist-executions-marker"> [ref]</a>
      </td>
      <td>The last execution uuid of the previous page, displays
list of executions after "marker".
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionslist-executions-limit"></a>limit<a href="#ScenarioMistralExecutionslist-executions-limit"> [ref]</a>
      </td>
      <td>number Maximum number of executions to return in a single
result.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionslist-executions-sort-keys"></a>sort_keys<a href="#ScenarioMistralExecutionslist-executions-sort-keys"> [ref]</a>
      </td>
      <td>id,description
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralExecutionslist-executions-sort-dirs"></a>sort_dirs<a href="#ScenarioMistralExecutionslist-executions-sort-dirs"> [ref]</a>
      </td>
      <td>[SORT_DIRS] Comma-separated list of sort directions.
Default: asc.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.mistral.executions](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/executions.py)

<hr />

#### MistralWorkbooks.create_workbook [Scenario]

Scenario tests workbook creation and deletion.

This scenario is a very useful tool to measure the
"mistral workbook-create" and "mistral workbook-delete"
commands performance.

__Platform__: openstack

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
        <a name="ScenarioMistralWorkbookscreate-workbook-definition"></a>definition<a href="#ScenarioMistralWorkbookscreate-workbook-definition"> [ref]</a>
      </td>
      <td>string (yaml string) representation of given
file content (Mistral workbook definition)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMistralWorkbookscreate-workbook-do-delete"></a>do_delete<a href="#ScenarioMistralWorkbookscreate-workbook-do-delete"> [ref]</a>
      </td>
      <td>if False than it allows to check performance
in "create only" mode.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.mistral.workbooks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/workbooks.py)

<hr />

#### MistralWorkbooks.list_workbooks [Scenario]

Scenario test mistral workbook-list command.

This simple scenario tests the Mistral workbook-list
command by listing all the workbooks.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.mistral.workbooks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/workbooks.py)

<hr />

#### MonascaMetrics.list_metrics [Scenario]

Fetch user's metrics.

__Platform__: openstack

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
        <a name="ScenarioMonascaMetricslist-metrics-kwargs"></a>kwargs<a href="#ScenarioMonascaMetricslist-metrics-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for list query:
name, dimensions, start_time, etc
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.monasca.metrics](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/monasca/metrics.py)

<hr />

#### MuranoEnvironments.create_and_delete_environment [Scenario]

Create environment, session and delete environment.

__Platform__: openstack

__Module__: [rally_openstack.scenarios.murano.environments](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/environments.py)

<hr />

#### MuranoEnvironments.create_and_deploy_environment [Scenario]

Create environment, session and deploy environment.

Create environment, create session, add app to environment
packages_per_env times, send environment to deploy.

__Platform__: openstack

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
        <a name="ScenarioMuranoEnvironmentscreate-and-deploy-environment-packages-per-env"></a>packages_per_env<a href="#ScenarioMuranoEnvironmentscreate-and-deploy-environment-packages-per-env"> [ref]</a>
      </td>
      <td>number of packages per environment</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.murano.environments](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/environments.py)

<hr />

#### MuranoEnvironments.list_environments [Scenario]

List the murano environments.

Run murano environment-list for listing all environments.

__Platform__: openstack

__Module__: [rally_openstack.scenarios.murano.environments](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/environments.py)

<hr />

#### MuranoPackages.import_and_delete_package [Scenario]

Import Murano package and then delete it.

Measure the "murano import-package" and "murano package-delete"
commands performance.
It imports Murano package from "package" (if it is not a zip archive
then zip archive will be prepared) and deletes it.

__Platform__: openstack

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
        <a name="ScenarioMuranoPackagesimport-and-delete-package-package"></a>package<a href="#ScenarioMuranoPackagesimport-and-delete-package-package"> [ref]</a>
      </td>
      <td>path to zip archive that represents Murano
application package or absolute path to folder with
package components
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.murano.packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/packages.py)

<hr />

#### MuranoPackages.import_and_filter_applications [Scenario]

Import Murano package and then filter packages by some criteria.

Measure the performance of package import and package
filtering commands.
It imports Murano package from "package" (if it is not a zip archive
then zip archive will be prepared) and filters packages by some
criteria.

__Platform__: openstack

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
        <a name="ScenarioMuranoPackagesimport-and-filter-applications-package"></a>package<a href="#ScenarioMuranoPackagesimport-and-filter-applications-package"> [ref]</a>
      </td>
      <td>path to zip archive that represents Murano
application package or absolute path to folder with
package components
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMuranoPackagesimport-and-filter-applications-filter-query"></a>filter_query<a href="#ScenarioMuranoPackagesimport-and-filter-applications-filter-query"> [ref]</a>
      </td>
      <td>dict that contains filter criteria, lately it
will be passed as **kwargs to filter method
e.g. {"category": "Web"}
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.murano.packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/packages.py)

<hr />

#### MuranoPackages.import_and_list_packages [Scenario]

Import Murano package and get list of packages.

Measure the "murano import-package" and "murano package-list" commands
performance.
It imports Murano package from "package" (if it is not a zip archive
then zip archive will be prepared) and gets list of imported packages.

__Platform__: openstack

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
        <a name="ScenarioMuranoPackagesimport-and-list-packages-package"></a>package<a href="#ScenarioMuranoPackagesimport-and-list-packages-package"> [ref]</a>
      </td>
      <td>path to zip archive that represents Murano
application package or absolute path to folder with
package components
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMuranoPackagesimport-and-list-packages-include-disabled"></a>include_disabled<a href="#ScenarioMuranoPackagesimport-and-list-packages-include-disabled"> [ref]</a>
      </td>
      <td>specifies whether the disabled packages will
be included in a the result or not.
Default value is False.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.murano.packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/packages.py)

<hr />

#### MuranoPackages.package_lifecycle [Scenario]

Import Murano package, modify it and then delete it.

Measure the Murano import, update and delete package
commands performance.
It imports Murano package from "package" (if it is not a zip archive
then zip archive will be prepared), modifies it (using data from
"body") and deletes.

__Platform__: openstack

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
        <a name="ScenarioMuranoPackagespackage-lifecycle-package"></a>package<a href="#ScenarioMuranoPackagespackage-lifecycle-package"> [ref]</a>
      </td>
      <td>path to zip archive that represents Murano
application package or absolute path to folder with
package components
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMuranoPackagespackage-lifecycle-body"></a>body<a href="#ScenarioMuranoPackagespackage-lifecycle-body"> [ref]</a>
      </td>
      <td>dict object that defines what package property will be
updated, e.g {"tags": ["tag"]} or {"enabled": "true"}
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioMuranoPackagespackage-lifecycle-operation"></a>operation<a href="#ScenarioMuranoPackagespackage-lifecycle-operation"> [ref]</a>
      </td>
      <td>string object that defines the way of how package
property will be updated, allowed operations are
"add", "replace" or "delete".
Default value is "replace".
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.murano.packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/packages.py)

<hr />

#### NeutronBGPVPN.create_and_delete_bgpvpns [Scenario]

Create bgpvpn and delete the bgpvpn.

Measure the "neutron bgpvpn-create" and neutron bgpvpn-delete
command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported and
used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-export-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-distinguishers"> [ref]</a>
      </td>
      <td>List of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_list_bgpvpns [Scenario]

Create a bgpvpn and then list all bgpvpns.

Measure the "neutron bgpvpn-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported and
used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-export-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-distinguishers"> [ref]</a>
      </td>
      <td>List of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_list_networks_associations [Scenario]

Associate a network and list networks associations.

Measure the "neutron bgpvpn-create",
"neutron bgpvpn-net-assoc-create" and
"neutron bgpvpn-net-assoc-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported and
used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-networks-associations-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-networks-associations-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-export-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-distinguishers"> [ref]</a>
      </td>
      <td>List of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-networks-associations-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_list_routers_associations [Scenario]

Associate a router and list routers associations.

Measure the "neutron bgpvpn-create",
"neutron bgpvpn-router-assoc-create" and
"neutron bgpvpn-router-assoc-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported and
used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-routers-associations-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-routers-associations-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-export-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-distinguishers"> [ref]</a>
      </td>
      <td>List of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-list-routers-associations-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_update_bgpvpns [Scenario]

Create and Update bgpvpns.

Measure the "neutron bgpvpn-update" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-update-name"></a>update_name<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-update-name"> [ref]</a>
      </td>
      <td>bool, whether or not to modify BGP VPN name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported
and used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-targets"></a>updated_route_targets<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-targets"> [ref]</a>
      </td>
      <td>Updated Route Targets that will be both
imported and used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-import-targets"></a>updated_import_targets<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-import-targets"> [ref]</a>
      </td>
      <td>Updated additional Route Targets that
will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-export-targets"> [ref]</a>
      </td>
      <td>additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-export-targets"></a>updated_export_targets<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-export-targets"> [ref]</a>
      </td>
      <td>Updated additional Route Targets that
will be used for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-distinguishers"> [ref]</a>
      </td>
      <td>list of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-distinguishers"></a>updated_route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-distinguishers"> [ref]</a>
      </td>
      <td>Updated list of route
distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_bgpvpn_assoc_disassoc_networks [Scenario]

Associate a network and disassociate it from a BGP VPN.

Measure the "neutron bgpvpn-create", "neutron bgpvpn-net-assoc-create"
and "neutron bgpvpn-net-assoc-delete" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported and
used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-export-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-distinguishers"> [ref]</a>
      </td>
      <td>List of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_bgpvpn_assoc_disassoc_routers [Scenario]

Associate a router and disassociate it from a BGP VPN.

Measure the "neutron bgpvpn-create",
"neutron bgpvpn-router-assoc-create" and
"neutron bgpvpn-router-assoc-delete" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-targets"></a>route_targets<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-targets"> [ref]</a>
      </td>
      <td>Route Targets that will be both imported and
used for export
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-import-targets"></a>import_targets<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-import-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be imported
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-export-targets"></a>export_targets<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-export-targets"> [ref]</a>
      </td>
      <td>Additional Route Targets that will be used
for export.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-distinguishers"></a>route_distinguishers<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-distinguishers"> [ref]</a>
      </td>
      <td>List of route distinguisher strings
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-bgpvpn-type"></a>bgpvpn_type<a href="#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-bgpvpn-type"> [ref]</a>
      </td>
      <td>type of VPN and the technology behind it.
Acceptable formats: l2 and l3
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronLoadbalancerV1.create_and_delete_healthmonitors [Scenario]

Create a healthmonitor(v1) and delete healthmonitors(v1).

Measure the "neutron lb-healthmonitor-create" and "neutron
lb-healthmonitor-delete" command performance. The scenario creates
healthmonitors and deletes those healthmonitors.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-delete-healthmonitors-healthmonitor-create-args"></a>healthmonitor_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-delete-healthmonitors-healthmonitor-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/healthmonitors request
options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_delete_pools [Scenario]

Create pools(v1) and delete pools(v1).

Measure the "neutron lb-pool-create" and "neutron lb-pool-delete"
command performance. The scenario creates a pool for every subnet
and then deletes those pools.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-delete-pools-pool-create-args"></a>pool_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-delete-pools-pool-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_delete_vips [Scenario]

Create a vip(v1) and then delete vips(v1).

Measure the "neutron lb-vip-create" and "neutron lb-vip-delete"
command performance. The scenario creates a vip for pool and
then deletes those vips.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-delete-vips-pool-create-args"></a>pool_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-delete-vips-pool-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronLoadbalancerV1create-and-delete-vips-vip-create-args"></a>vip_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-delete-vips-vip-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/vips request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_list_healthmonitors [Scenario]

Create healthmonitors(v1) and list healthmonitors(v1).

Measure the "neutron lb-healthmonitor-list" command performance. This
scenario creates healthmonitors and lists them.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-list-healthmonitors-healthmonitor-create-args"></a>healthmonitor_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-list-healthmonitors-healthmonitor-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/healthmonitors request
options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_list_pools [Scenario]

Create a pool(v1) and then list pools(v1).

Measure the "neutron lb-pool-list" command performance.
The scenario creates a pool for every subnet and then lists pools.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-list-pools-pool-create-args"></a>pool_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-list-pools-pool-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_list_vips [Scenario]

Create a vip(v1) and then list vips(v1).

Measure the "neutron lb-vip-create" and "neutron lb-vip-list" command
performance. The scenario creates a vip for every pool created and
then lists vips.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-list-vips-vip-create-args"></a>vip_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-list-vips-vip-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/vips request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronLoadbalancerV1create-and-list-vips-pool-create-args"></a>pool_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-list-vips-pool-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_update_healthmonitors [Scenario]

Create a healthmonitor(v1) and update healthmonitors(v1).

Measure the "neutron lb-healthmonitor-create" and "neutron
lb-healthmonitor-update" command performance. The scenario creates
healthmonitors and then updates them.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-create-args"></a>healthmonitor_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/healthmonitors request
options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-update-args"></a>healthmonitor_update_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-update-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/healthmonitors update
options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_update_pools [Scenario]

Create pools(v1) and update pools(v1).

Measure the "neutron lb-pool-create" and "neutron lb-pool-update"
command performance. The scenario creates a pool for every subnet
and then update those pools.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-create-args"></a>pool_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-update-args"></a>pool_update_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-update-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools update options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_update_vips [Scenario]

Create vips(v1) and update vips(v1).

Measure the "neutron lb-vip-create" and "neutron lb-vip-update"
command performance. The scenario creates a pool for every subnet
and then update those pools.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-vips-pool-create-args"></a>pool_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-vips-pool-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/pools request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-create-args"></a>vip_create_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/vips request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-update-args"></a>vip_update_args<a href="#ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-update-args"> [ref]</a>
      </td>
      <td>dict, POST /lb/vips update options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV2.create_and_list_loadbalancers [Scenario]

Create a loadbalancer(v2) and then list loadbalancers(v2).

Measure the "neutron lbaas-loadbalancer-list" command performance.
The scenario creates a loadbalancer for every subnet and then lists
loadbalancers.

__Platform__: openstack

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
        <a name="ScenarioNeutronLoadbalancerV2create-and-list-loadbalancers-lb-create-args"></a>lb_create_args<a href="#ScenarioNeutronLoadbalancerV2create-and-list-loadbalancers-lb-create-args"> [ref]</a>
      </td>
      <td>dict, POST /lbaas/loadbalancers
request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v2](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v2.py)

<hr />

#### NeutronNetworks.create_and_delete_floating_ips [Scenario]

Create and delete floating IPs.

Measure the "neutron floating-ip-create" and "neutron
floating-ip-delete" commands performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-network"></a>floating_network<a href="#ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-network"> [ref]</a>
      </td>
      <td>str, external network for floating IP creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-ip-args"></a>floating_ip_args<a href="#ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-ip-args"> [ref]</a>
      </td>
      <td>dict, POST /floatingips request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_networks [Scenario]

Create and delete a network.

Measure the "neutron net-create" and "net-delete" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-delete-networks-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-networks-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request options</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_ports [Scenario]

Create and delete a port.

Measure the "neutron port-create" and "neutron port-delete"
commands performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-delete-ports-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-ports-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-ports-port-create-args"></a>port_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-ports-port-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/ports request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-ports-ports-per-network"></a>ports_per_network<a href="#ScenarioNeutronNetworkscreate-and-delete-ports-ports-per-network"> [ref]</a>
      </td>
      <td>int, number of ports for one network</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_routers [Scenario]

Create and delete a given number of routers.

Create a network, a given number of subnets and routers
and then delete all routers.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-delete-routers-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-routers-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-routers-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-routers-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-routers-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-delete-routers-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-routers-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-delete-routers-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-routers-router-create-args"></a>router_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-routers-router-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/routers request options</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_subnets [Scenario]

Create and delete a given number of subnets.

The scenario creates a network, a given number of subnets and then
deletes subnets.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-delete-subnets-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-subnets-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-delete-subnets-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-delete-subnets-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_floating_ips [Scenario]

Create and list floating IPs.

Measure the "neutron floating-ip-create" and "neutron floating-ip-list"
commands performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-network"></a>floating_network<a href="#ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-network"> [ref]</a>
      </td>
      <td>str, external network for floating IP creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-ip-args"></a>floating_ip_args<a href="#ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-ip-args"> [ref]</a>
      </td>
      <td>dict, POST /floatingips request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_networks [Scenario]

Create a network and then list all networks.

Measure the "neutron net-list" command performance.

If you have only 1 user in your context, you will
add 1 network on every iteration. So you will have more
and more networks and will be able to measure the
performance of the "neutron net-list" command depending on
the number of networks owned by users.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-list-networks-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-networks-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_ports [Scenario]

Create and a given number of ports and list all ports.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-list-ports-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-ports-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-ports-port-create-args"></a>port_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-ports-port-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/ports request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-ports-ports-per-network"></a>ports_per_network<a href="#ScenarioNeutronNetworkscreate-and-list-ports-ports-per-network"> [ref]</a>
      </td>
      <td>int, number of ports for one network</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_routers [Scenario]

Create and a given number of routers and list all routers.

Create a network, a given number of subnets and routers
and then list all routers.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-list-routers-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-routers-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-routers-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-routers-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-routers-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-list-routers-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-routers-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-list-routers-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-routers-router-create-args"></a>router_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-routers-router-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/routers request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_subnets [Scenario]

Create and a given number of subnets and list all subnets.

The scenario creates a network, a given number of subnets and then
lists subnets.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-list-subnets-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-subnets-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-subnets-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-list-subnets-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-subnets-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-list-subnets-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-list-subnets-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-list-subnets-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_network [Scenario]

Create a network and show network details.

Measure the "neutron net-show" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-show-network-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-network-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_ports [Scenario]

Create a given number of ports and show created ports in trun.

Measure the "neutron port-create" and "neutron port-show" commands
performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-show-ports-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-ports-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-ports-port-create-args"></a>port_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-ports-port-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/ports request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-ports-ports-per-network"></a>ports_per_network<a href="#ScenarioNeutronNetworkscreate-and-show-ports-ports-per-network"> [ref]</a>
      </td>
      <td>int, number of ports for one network</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_routers [Scenario]

Create and show a given number of routers.

Create a network, a given number of subnets and routers
and then show all routers.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-show-routers-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-routers-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-routers-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-routers-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-routers-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-show-routers-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-routers-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-show-routers-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for each network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-routers-router-create-args"></a>router_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-routers-router-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/routers request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_subnets [Scenario]

Create and show a subnet details.

The scenario creates a network, a given number of subnets
and show the subnet details. This scenario measures the
"neutron subnet-show" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-show-subnets-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-subnets-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-subnets-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-show-subnets-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-subnets-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-show-subnets-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-show-subnets-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-show-subnets-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_networks [Scenario]

Create and update a network.

Measure the "neutron net-create and net-update" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-update-networks-network-update-args"></a>network_update_args<a href="#ScenarioNeutronNetworkscreate-and-update-networks-network-update-args"> [ref]</a>
      </td>
      <td>dict, PUT /v2.0/networks update request
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-networks-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-networks-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_ports [Scenario]

Create and update a given number of ports.

Measure the "neutron port-create" and "neutron port-update" commands
performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-update-ports-port-update-args"></a>port_update_args<a href="#ScenarioNeutronNetworkscreate-and-update-ports-port-update-args"> [ref]</a>
      </td>
      <td>dict, PUT /v2.0/ports update request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-ports-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-ports-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-ports-port-create-args"></a>port_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-ports-port-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/ports request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-ports-ports-per-network"></a>ports_per_network<a href="#ScenarioNeutronNetworkscreate-and-update-ports-ports-per-network"> [ref]</a>
      </td>
      <td>int, number of ports for one network</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_routers [Scenario]

Create and update a given number of routers.

Create a network, a given number of subnets and routers
and then updating all routers.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-update-routers-router-update-args"></a>router_update_args<a href="#ScenarioNeutronNetworkscreate-and-update-routers-router-update-args"> [ref]</a>
      </td>
      <td>dict, PUT /v2.0/routers update options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-routers-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-routers-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-routers-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-routers-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-routers-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-update-routers-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-routers-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-update-routers-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-routers-router-create-args"></a>router_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-routers-router-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/routers request options</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_subnets [Scenario]

Create and update a subnet.

The scenario creates a network, a given number of subnets
and then updates the subnet. This scenario measures the
"neutron subnet-update" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkscreate-and-update-subnets-subnet-update-args"></a>subnet_update_args<a href="#ScenarioNeutronNetworkscreate-and-update-subnets-subnet-update-args"> [ref]</a>
      </td>
      <td>dict, PUT /v2.0/subnets update options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-subnets-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-subnets-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-subnets-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNeutronNetworkscreate-and-update-subnets-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-subnets-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNeutronNetworkscreate-and-update-subnets-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworkscreate-and-update-subnets-subnets-per-network"></a>subnets_per_network<a href="#ScenarioNeutronNetworkscreate-and-update-subnets-subnets-per-network"> [ref]</a>
      </td>
      <td>int, number of subnets for one network</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.list_agents [Scenario]

List all neutron agents.

This simple scenario tests the "neutron agent-list" command by
listing all the neutron agents.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworkslist-agents-agent-args"></a>agent_args<a href="#ScenarioNeutronNetworkslist-agents-agent-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/agents request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.set_and_clear_router_gateway [Scenario]

Set and Remove the external network gateway from a router.

create an external network and a router, set external network
gateway for the router, remove the external network gateway from
the router.

__Platform__: openstack

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
        <a name="ScenarioNeutronNetworksset-and-clear-router-gateway-enable-snat"></a>enable_snat<a href="#ScenarioNeutronNetworksset-and-clear-router-gateway-enable-snat"> [ref]</a>
      </td>
      <td>True if enable snat
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworksset-and-clear-router-gateway-network-create-args"></a>network_create_args<a href="#ScenarioNeutronNetworksset-and-clear-router-gateway-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronNetworksset-and-clear-router-gateway-router-create-args"></a>router_create_args<a href="#ScenarioNeutronNetworksset-and-clear-router-gateway-router-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/routers request options</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronSecurityGroup.create_and_delete_security_group_rule [Scenario]

Create and delete Neutron security-group-rule.

Measure the "neutron security-group-rule-create" and "neutron
security-group-rule-delete" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-args"></a>security_group_args<a href="#ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-rule-args"></a>security_group_rule_args<a href="#ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-rule-args"> [ref]</a>
      </td>
      <td>dict,
POST /v2.0/security-group-rules request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_delete_security_groups [Scenario]

Create and delete Neutron security-groups.

Measure the "neutron security-group-create" and "neutron
security-group-delete" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-delete-security-groups-security-group-create-args"></a>security_group_create_args<a href="#ScenarioNeutronSecurityGroupcreate-and-delete-security-groups-security-group-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_list_security_group_rules [Scenario]

Create and list Neutron security-group-rules.

Measure the "neutron security-group-rule-create" and "neutron
security-group-rule-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-args"></a>security_group_args<a href="#ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-rule-args"></a>security_group_rule_args<a href="#ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-rule-args"> [ref]</a>
      </td>
      <td>dict,
POST /v2.0/security-group-rules request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_list_security_groups [Scenario]

Create and list Neutron security-groups.

Measure the "neutron security-group-create" and "neutron
security-group-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-list-security-groups-security-group-create-args"></a>security_group_create_args<a href="#ScenarioNeutronSecurityGroupcreate-and-list-security-groups-security-group-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_show_security_group [Scenario]

Create and show Neutron security-group.

Measure the "neutron security-group-create" and "neutron
security-group-show" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-show-security-group-security-group-create-args"></a>security_group_create_args<a href="#ScenarioNeutronSecurityGroupcreate-and-show-security-group-security-group-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_show_security_group_rule [Scenario]

Create and show Neutron security-group-rule.

Measure the "neutron security-group-rule-create" and "neutron
security-group-rule-show" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-args"></a>security_group_args<a href="#ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-rule-args"></a>security_group_rule_args<a href="#ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-rule-args"> [ref]</a>
      </td>
      <td>dict,
POST /v2.0/security-group-rules request options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_update_security_groups [Scenario]

Create and update Neutron security-groups.

Measure the "neutron security-group-create" and "neutron
security-group-update" command performance.

__Platform__: openstack

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
        <a name="ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-create-args"></a>security_group_create_args<a href="#ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/security-groups
request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-update-args"></a>security_group_update_args<a href="#ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-update-args"> [ref]</a>
      </td>
      <td>dict, PUT /v2.0/security-groups
update options
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSubnets.delete_subnets [Scenario]

Delete a subnet that belongs to each precreated network.

Each runner instance picks a specific subnet from the list based on its
positional location in the list of users. By doing so, we can start
multiple threads with sufficient number of users created and spread
delete requests across all of them, so that they hit different subnets
concurrently.

Concurrent execution of this scenario should help reveal any race
conditions and other concurrency issues in Neutron IP allocation layer,
among other things.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NovaAgents.list_agents [Scenario]

List all builds.

Measure the "nova agent-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaAgentslist-agents-hypervisor"></a>hypervisor<a href="#ScenarioNovaAgentslist-agents-hypervisor"> [ref]</a>
      </td>
      <td>List agent builds on a specific hypervisor.
None (default value) means list for all
hypervisors
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.agents](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/agents.py)

<hr />

#### NovaAggregates.create_aggregate_add_and_remove_host [Scenario]

Create an aggregate, add a host to and remove the host from it.

Measure "nova aggregate-add-host" and "nova aggregate-remove-host"
command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaAggregatescreate-aggregate-add-and-remove-host-availability-zone"></a>availability_zone<a href="#ScenarioNovaAggregatescreate-aggregate-add-and-remove-host-availability-zone"> [ref]</a>
      </td>
      <td>The availability zone of the aggregate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_aggregate_add_host_and_boot_server [Scenario]

Scenario to create and verify an aggregate.

This scenario creates an aggregate, adds a compute host and metadata
to the aggregate, adds the same metadata to the flavor and creates an
instance. Verifies that instance host is one of the hosts in the
aggregate.

__Platform__: openstack

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
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-image"></a>image<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-image"> [ref]</a>
      </td>
      <td>The image ID to boot from
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-metadata"></a>metadata<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-metadata"> [ref]</a>
      </td>
      <td>The metadata to be set as flavor extra specs
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-availability-zone"></a>availability_zone<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-availability-zone"> [ref]</a>
      </td>
      <td>The availability zone of the aggregate
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-ram"></a>ram<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-vcpus"></a>vcpus<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-disk"></a>disk<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-boot-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments to verify host
aggregates
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_delete_aggregate [Scenario]

Create an aggregate and then delete it.

This scenario first creates an aggregate and then delete it.

__Platform__: openstack

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
        <a name="ScenarioNovaAggregatescreate-and-delete-aggregate-availability-zone"></a>availability_zone<a href="#ScenarioNovaAggregatescreate-and-delete-aggregate-availability-zone"> [ref]</a>
      </td>
      <td>The availability zone of the aggregate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_get_aggregate_details [Scenario]

Create an aggregate and then get its details.

This scenario first creates an aggregate and then get details of it.

__Platform__: openstack

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
        <a name="ScenarioNovaAggregatescreate-and-get-aggregate-details-availability-zone"></a>availability_zone<a href="#ScenarioNovaAggregatescreate-and-get-aggregate-details-availability-zone"> [ref]</a>
      </td>
      <td>The availability zone of the aggregate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_list_aggregates [Scenario]

Create a aggregate and then list all aggregates.

This scenario creates a aggregate and then lists all aggregates.

__Platform__: openstack

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
        <a name="ScenarioNovaAggregatescreate-and-list-aggregates-availability-zone"></a>availability_zone<a href="#ScenarioNovaAggregatescreate-and-list-aggregates-availability-zone"> [ref]</a>
      </td>
      <td>The availability zone of the aggregate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_update_aggregate [Scenario]

Create an aggregate and then update its name and availability_zone.

This scenario first creates an aggregate and then update its name and
availability_zone

__Platform__: openstack

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
        <a name="ScenarioNovaAggregatescreate-and-update-aggregate-availability-zone"></a>availability_zone<a href="#ScenarioNovaAggregatescreate-and-update-aggregate-availability-zone"> [ref]</a>
      </td>
      <td>The availability zone of the aggregate</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.list_aggregates [Scenario]

List all nova aggregates.

Measure the "nova aggregate-list" command performance.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAvailabilityZones.list_availability_zones [Scenario]

List all availability zones.

Measure the "nova availability-zone-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaAvailabilityZoneslist-availability-zones-detailed"></a>detailed<a href="#ScenarioNovaAvailabilityZoneslist-availability-zones-detailed"> [ref]</a>
      </td>
      <td>True if the availability-zone listing should contain
detailed information about all of them
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.availability_zones](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/availability_zones.py)

<hr />

#### NovaFlavors.create_and_delete_flavor [Scenario]

Create flavor and delete the flavor.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-ram"></a>ram<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-vcpus"></a>vcpus<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-disk"></a>disk<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-flavorid"></a>flavorid<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-flavorid"> [ref]</a>
      </td>
      <td>ID for the flavor (optional). You can use the reserved
value ``"auto"`` to have Nova generate a UUID for the
flavor in cases where you cannot simply pass ``None``.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-ephemeral"></a>ephemeral<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-ephemeral"> [ref]</a>
      </td>
      <td>Ephemeral space size in GB (default 0).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-swap"></a>swap<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-swap"> [ref]</a>
      </td>
      <td>Swap space in MB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-rxtx-factor"></a>rxtx_factor<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-rxtx-factor"> [ref]</a>
      </td>
      <td>RX/TX factor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-delete-flavor-is-public"></a>is_public<a href="#ScenarioNovaFlavorscreate-and-delete-flavor-is-public"> [ref]</a>
      </td>
      <td>Make flavor accessible to the public (default true).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_and_get_flavor [Scenario]

Create flavor and get detailed information of the flavor.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-ram"></a>ram<a href="#ScenarioNovaFlavorscreate-and-get-flavor-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-vcpus"></a>vcpus<a href="#ScenarioNovaFlavorscreate-and-get-flavor-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-disk"></a>disk<a href="#ScenarioNovaFlavorscreate-and-get-flavor-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-flavorid"></a>flavorid<a href="#ScenarioNovaFlavorscreate-and-get-flavor-flavorid"> [ref]</a>
      </td>
      <td>ID for the flavor (optional). You can use the reserved
value ``"auto"`` to have Nova generate a UUID for the
flavor in cases where you cannot simply pass ``None``.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-ephemeral"></a>ephemeral<a href="#ScenarioNovaFlavorscreate-and-get-flavor-ephemeral"> [ref]</a>
      </td>
      <td>Ephemeral space size in GB (default 0).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-swap"></a>swap<a href="#ScenarioNovaFlavorscreate-and-get-flavor-swap"> [ref]</a>
      </td>
      <td>Swap space in MB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-rxtx-factor"></a>rxtx_factor<a href="#ScenarioNovaFlavorscreate-and-get-flavor-rxtx-factor"> [ref]</a>
      </td>
      <td>RX/TX factor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-get-flavor-is-public"></a>is_public<a href="#ScenarioNovaFlavorscreate-and-get-flavor-is-public"> [ref]</a>
      </td>
      <td>Make flavor accessible to the public (default true).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_and_list_flavor_access [Scenario]

Create a non-public flavor and list its access rules.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-ram"></a>ram<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-vcpus"></a>vcpus<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-disk"></a>disk<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-flavorid"></a>flavorid<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-flavorid"> [ref]</a>
      </td>
      <td>ID for the flavor (optional). You can use the reserved
value ``"auto"`` to have Nova generate a UUID for the
flavor in cases where you cannot simply pass ``None``.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-ephemeral"></a>ephemeral<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-ephemeral"> [ref]</a>
      </td>
      <td>Ephemeral space size in GB (default 0).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-swap"></a>swap<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-swap"> [ref]</a>
      </td>
      <td>Swap space in MB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-rxtx-factor"></a>rxtx_factor<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-rxtx-factor"> [ref]</a>
      </td>
      <td>RX/TX factor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-and-list-flavor-access-is-public"></a>is_public<a href="#ScenarioNovaFlavorscreate-and-list-flavor-access-is-public"> [ref]</a>
      </td>
      <td>Make flavor accessible to the public (default true).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_flavor [Scenario]

Create a flavor.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorscreate-flavor-ram"></a>ram<a href="#ScenarioNovaFlavorscreate-flavor-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-vcpus"></a>vcpus<a href="#ScenarioNovaFlavorscreate-flavor-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-disk"></a>disk<a href="#ScenarioNovaFlavorscreate-flavor-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-flavorid"></a>flavorid<a href="#ScenarioNovaFlavorscreate-flavor-flavorid"> [ref]</a>
      </td>
      <td>ID for the flavor (optional). You can use the reserved
value ``"auto"`` to have Nova generate a UUID for the
flavor in cases where you cannot simply pass ``None``.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-ephemeral"></a>ephemeral<a href="#ScenarioNovaFlavorscreate-flavor-ephemeral"> [ref]</a>
      </td>
      <td>Ephemeral space size in GB (default 0).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-swap"></a>swap<a href="#ScenarioNovaFlavorscreate-flavor-swap"> [ref]</a>
      </td>
      <td>Swap space in MB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-rxtx-factor"></a>rxtx_factor<a href="#ScenarioNovaFlavorscreate-flavor-rxtx-factor"> [ref]</a>
      </td>
      <td>RX/TX factor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-is-public"></a>is_public<a href="#ScenarioNovaFlavorscreate-flavor-is-public"> [ref]</a>
      </td>
      <td>Make flavor accessible to the public (default true).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_flavor_and_add_tenant_access [Scenario]

Create a flavor and Add flavor access for the given tenant.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ram"></a>ram<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-vcpus"></a>vcpus<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-disk"></a>disk<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-flavorid"></a>flavorid<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-flavorid"> [ref]</a>
      </td>
      <td>ID for the flavor (optional). You can use the reserved
value ``"auto"`` to have Nova generate a UUID for the
flavor in cases where you cannot simply pass ``None``.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ephemeral"></a>ephemeral<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ephemeral"> [ref]</a>
      </td>
      <td>Ephemeral space size in GB (default 0).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-swap"></a>swap<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-swap"> [ref]</a>
      </td>
      <td>Swap space in MB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-rxtx-factor"></a>rxtx_factor<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-rxtx-factor"> [ref]</a>
      </td>
      <td>RX/TX factor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-is-public"></a>is_public<a href="#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-is-public"> [ref]</a>
      </td>
      <td>Make flavor accessible to the public (default true).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_flavor_and_set_keys [Scenario]

Create flavor and set keys to the flavor.

Measure the "nova flavor-key" command performance.
the scenario first create a flavor,then add the extra specs to it.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-ram"></a>ram<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-ram"> [ref]</a>
      </td>
      <td>Memory in MB for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-vcpus"></a>vcpus<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-vcpus"> [ref]</a>
      </td>
      <td>Number of VCPUs for the flavor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-disk"></a>disk<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-disk"> [ref]</a>
      </td>
      <td>Size of local disk in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-extra-specs"></a>extra_specs<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-extra-specs"> [ref]</a>
      </td>
      <td>additional arguments for flavor set keys
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-flavorid"></a>flavorid<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-flavorid"> [ref]</a>
      </td>
      <td>ID for the flavor (optional). You can use the reserved
value ``"auto"`` to have Nova generate a UUID for the
flavor in cases where you cannot simply pass ``None``.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-ephemeral"></a>ephemeral<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-ephemeral"> [ref]</a>
      </td>
      <td>Ephemeral space size in GB (default 0).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-swap"></a>swap<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-swap"> [ref]</a>
      </td>
      <td>Swap space in MB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-rxtx-factor"></a>rxtx_factor<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-rxtx-factor"> [ref]</a>
      </td>
      <td>RX/TX factor
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorscreate-flavor-and-set-keys-is-public"></a>is_public<a href="#ScenarioNovaFlavorscreate-flavor-and-set-keys-is-public"> [ref]</a>
      </td>
      <td>Make flavor accessible to the public (default true).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.list_flavors [Scenario]

List all flavors.

Measure the "nova flavor-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaFlavorslist-flavors-detailed"></a>detailed<a href="#ScenarioNovaFlavorslist-flavors-detailed"> [ref]</a>
      </td>
      <td>Whether flavor needs to be return with details
(optional).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-is-public"></a>is_public<a href="#ScenarioNovaFlavorslist-flavors-is-public"> [ref]</a>
      </td>
      <td>Filter flavors with provided access type (optional).
None means give all flavors and only admin has query
access to all flavor types.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-marker"></a>marker<a href="#ScenarioNovaFlavorslist-flavors-marker"> [ref]</a>
      </td>
      <td>Begin returning flavors that appear later in the flavor
list than that represented by this flavor id (optional).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-min-disk"></a>min_disk<a href="#ScenarioNovaFlavorslist-flavors-min-disk"> [ref]</a>
      </td>
      <td>Filters the flavors by a minimum disk space, in GiB.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-min-ram"></a>min_ram<a href="#ScenarioNovaFlavorslist-flavors-min-ram"> [ref]</a>
      </td>
      <td>Filters the flavors by a minimum RAM, in MB.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-limit"></a>limit<a href="#ScenarioNovaFlavorslist-flavors-limit"> [ref]</a>
      </td>
      <td>maximum number of flavors to return (optional).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-sort-key"></a>sort_key<a href="#ScenarioNovaFlavorslist-flavors-sort-key"> [ref]</a>
      </td>
      <td>Flavors list sort key (optional).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaFlavorslist-flavors-sort-dir"></a>sort_dir<a href="#ScenarioNovaFlavorslist-flavors-sort-dir"> [ref]</a>
      </td>
      <td>Flavors list sort direction (optional).</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaHypervisors.list_and_get_hypervisors [Scenario]

List and Get hypervisors.

The scenario first lists all hypervisors, then get detailed information
of the listed hypervisors in turn.

Measure the "nova hypervisor-show" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaHypervisorslist-and-get-hypervisors-detailed"></a>detailed<a href="#ScenarioNovaHypervisorslist-and-get-hypervisors-detailed"> [ref]</a>
      </td>
      <td>True if the hypervisor listing should contain
detailed information about all of them
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.list_and_get_uptime_hypervisors [Scenario]

List hypervisors,then display the uptime of it.

The scenario first list all hypervisors,then display
the uptime of the listed hypervisors in turn.

Measure the "nova hypervisor-uptime" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaHypervisorslist-and-get-uptime-hypervisors-detailed"></a>detailed<a href="#ScenarioNovaHypervisorslist-and-get-uptime-hypervisors-detailed"> [ref]</a>
      </td>
      <td>True if the hypervisor listing should contain
detailed information about all of them
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.list_and_search_hypervisors [Scenario]

List all servers belonging to specific hypervisor.

The scenario first list all hypervisors,then find its hostname,
then list all servers belonging to the hypervisor

Measure the "nova hypervisor-servers <hostname>" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaHypervisorslist-and-search-hypervisors-detailed"></a>detailed<a href="#ScenarioNovaHypervisorslist-and-search-hypervisors-detailed"> [ref]</a>
      </td>
      <td>True if the hypervisor listing should contain
detailed information about all of them
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.list_hypervisors [Scenario]

List hypervisors.

Measure the "nova hypervisor-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaHypervisorslist-hypervisors-detailed"></a>detailed<a href="#ScenarioNovaHypervisorslist-hypervisors-detailed"> [ref]</a>
      </td>
      <td>True if the hypervisor listing should contain
detailed information about all of them
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.statistics_hypervisors [Scenario]

Get hypervisor statistics over all compute nodes.

Measure the "nova hypervisor-stats" command performance.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaImages.list_images [Scenario]

[DEPRECATED] List all images.

Measure the "nova image-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaImageslist-images-detailed"></a>detailed<a href="#ScenarioNovaImageslist-images-detailed"> [ref]</a>
      </td>
      <td>True if the image listing
should contain detailed information
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaImageslist-images-kwargs"></a>kwargs<a href="#ScenarioNovaImageslist-images-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for image listing</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/images.py)

<hr />

#### NovaKeypair.boot_and_delete_server_with_keypair [Scenario]

Boot and delete server with keypair.

Plan of this scenario:

- create a keypair
- boot a VM with created keypair
- delete server
- delete keypair

__Platform__: openstack

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
        <a name="ScenarioNovaKeypairboot-and-delete-server-with-keypair-image"></a>image<a href="#ScenarioNovaKeypairboot-and-delete-server-with-keypair-image"> [ref]</a>
      </td>
      <td>ID of the image to be used for server creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaKeypairboot-and-delete-server-with-keypair-flavor"></a>flavor<a href="#ScenarioNovaKeypairboot-and-delete-server-with-keypair-flavor"> [ref]</a>
      </td>
      <td>ID of the flavor to be used for server creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaKeypairboot-and-delete-server-with-keypair-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioNovaKeypairboot-and-delete-server-with-keypair-boot-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for VM
creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaKeypairboot-and-delete-server-with-keypair-server-kwargs"></a>server_kwargs<a href="#ScenarioNovaKeypairboot-and-delete-server-with-keypair-server-kwargs"> [ref]</a>
      </td>
      <td>Deprecated alias for boot_server_kwargs
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaKeypairboot-and-delete-server-with-keypair-kwargs"></a>kwargs<a href="#ScenarioNovaKeypairboot-and-delete-server-with-keypair-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for keypair creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaKeypair.create_and_delete_keypair [Scenario]

Create a keypair with random name and delete keypair.

This scenario creates a keypair and then delete that keypair.

__Platform__: openstack

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
        <a name="ScenarioNovaKeypaircreate-and-delete-keypair-kwargs"></a>kwargs<a href="#ScenarioNovaKeypaircreate-and-delete-keypair-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for keypair creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaKeypair.create_and_get_keypair [Scenario]

Create a keypair and get the keypair details.

__Platform__: openstack

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
        <a name="ScenarioNovaKeypaircreate-and-get-keypair-kwargs"></a>kwargs<a href="#ScenarioNovaKeypaircreate-and-get-keypair-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for keypair creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaKeypair.create_and_list_keypairs [Scenario]

Create a keypair with random name and list keypairs.

This scenario creates a keypair and then lists all keypairs.

__Platform__: openstack

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
        <a name="ScenarioNovaKeypaircreate-and-list-keypairs-kwargs"></a>kwargs<a href="#ScenarioNovaKeypaircreate-and-list-keypairs-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for keypair creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaServerGroups.create_and_delete_server_group [Scenario]

Create a server group, then delete it.

Measure the "nova server-group-create" and "nova server-group-delete"
command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServerGroupscreate-and-delete-server-group-policies"></a>policies<a href="#ScenarioNovaServerGroupscreate-and-delete-server-group-policies"> [ref]</a>
      </td>
      <td>Server group policy
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerGroupscreate-and-delete-server-group-kwargs"></a>kwargs<a href="#ScenarioNovaServerGroupscreate-and-delete-server-group-kwargs"> [ref]</a>
      </td>
      <td>The server group specifications to add.
DEPRECATED, specify arguments explicitly.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.server_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/server_groups.py)

<hr />

#### NovaServerGroups.create_and_get_server_group [Scenario]

Create a server group, then get its detailed information.

Measure the "nova server-group-create" and "nova server-group-get"
command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServerGroupscreate-and-get-server-group-policies"></a>policies<a href="#ScenarioNovaServerGroupscreate-and-get-server-group-policies"> [ref]</a>
      </td>
      <td>Server group policy
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerGroupscreate-and-get-server-group-kwargs"></a>kwargs<a href="#ScenarioNovaServerGroupscreate-and-get-server-group-kwargs"> [ref]</a>
      </td>
      <td>The server group specifications to add.
DEPRECATED, specify arguments explicitly.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.server_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/server_groups.py)

<hr />

#### NovaServerGroups.create_and_list_server_groups [Scenario]

Create a server group, then list all server groups.

Measure the "nova server-group-create" and "nova server-group-list"
command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServerGroupscreate-and-list-server-groups-policies"></a>policies<a href="#ScenarioNovaServerGroupscreate-and-list-server-groups-policies"> [ref]</a>
      </td>
      <td>Server group policy
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerGroupscreate-and-list-server-groups-all-projects"></a>all_projects<a href="#ScenarioNovaServerGroupscreate-and-list-server-groups-all-projects"> [ref]</a>
      </td>
      <td>If True, display server groups from all
projects(Admin only)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerGroupscreate-and-list-server-groups-kwargs"></a>kwargs<a href="#ScenarioNovaServerGroupscreate-and-list-server-groups-kwargs"> [ref]</a>
      </td>
      <td>The server group specifications to add.
DEPRECATED, specify arguments explicitly.
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.server_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/server_groups.py)

<hr />

#### NovaServers.boot_and_associate_floating_ip [Scenario]

Boot a server and associate a floating IP to it.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-associate-floating-ip-image"></a>image<a href="#ScenarioNovaServersboot-and-associate-floating-ip-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-associate-floating-ip-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-associate-floating-ip-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-associate-floating-ip-create-floating-ip-args"></a>create_floating_ip_args<a href="#ScenarioNovaServersboot-and-associate-floating-ip-create-floating-ip-args"> [ref]</a>
      </td>
      <td>Optional additional arguments for
floating ip creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-associate-floating-ip-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-associate-floating-ip-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_bounce_server [Scenario]

Boot a server and run specified actions against it.

Actions should be passed into the actions parameter. Available actions
are 'hard_reboot', 'soft_reboot', 'stop_start', 'rescue_unrescue',
'pause_unpause', 'suspend_resume', 'lock_unlock' and 'shelve_unshelve'.
Delete server after all actions were completed.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-bounce-server-image"></a>image<a href="#ScenarioNovaServersboot-and-bounce-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-bounce-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-bounce-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-bounce-server-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-and-bounce-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-bounce-server-actions"></a>actions<a href="#ScenarioNovaServersboot-and-bounce-server-actions"> [ref]</a>
      </td>
      <td>list of action dictionaries, where each action
dictionary speicifes an action to be performed
in the following format:
{"action_name": <no_of_iterations>}
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-bounce-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-bounce-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_delete_multiple_servers [Scenario]

Boot multiple servers in a single request and delete them.

Deletion is done in parallel with one request per server, not
with a single request for all servers.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-image"></a>image<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-image"> [ref]</a>
      </td>
      <td>The image to boot from
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-flavor"> [ref]</a>
      </td>
      <td>Flavor used to boot instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-count"></a>count<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-count"> [ref]</a>
      </td>
      <td>Number of instances to boot
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-multiple-servers-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-delete-multiple-servers-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for instance creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_delete_server [Scenario]

Boot and delete a server.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between volume creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-delete-server-image"></a>image<a href="#ScenarioNovaServersboot-and-delete-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-delete-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-server-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-and-delete-server-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-server-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-and-delete-server-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-server-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-and-delete-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-delete-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-delete-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_get_console_output [Scenario]

Get text console output from server.

This simple scenario tests the nova console-log command by retrieving
the text console log output.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-get-console-output-image"></a>image<a href="#ScenarioNovaServersboot-and-get-console-output-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-get-console-output-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-get-console-output-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-get-console-output-length"></a>length<a href="#ScenarioNovaServersboot-and-get-console-output-length"> [ref]</a>
      </td>
      <td>The number of tail log lines you would like to retrieve.
None (default value) or -1 means unlimited length.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-get-console-output-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-get-console-output-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation
</td>
    </tr>
  </tbody>
</table>


__Returns__:  
Text console log output for server

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_get_console_url [Scenario]

Retrieve a console url of a server.

This simple scenario tests retrieving the console url of a server.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-get-console-url-image"></a>image<a href="#ScenarioNovaServersboot-and-get-console-url-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-get-console-url-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-get-console-url-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-get-console-url-console-type"></a>console_type<a href="#ScenarioNovaServersboot-and-get-console-url-console-type"> [ref]</a>
      </td>
      <td>type can be novnc/xvpvnc for protocol vnc;
spice-html5 for protocol spice; rdp-html5 for
protocol rdp; serial for protocol serial.
webmks for protocol mks (since version 2.8).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-get-console-url-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-get-console-url-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_list_server [Scenario]

Boot a server from an image and then list all servers.

Measure the "nova list" command performance.

If you have only 1 user in your context, you will
add 1 server on every iteration. So you will have more
and more servers and will be able to measure the
performance of the "nova list" command depending on
the number of servers owned by users.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-list-server-image"></a>image<a href="#ScenarioNovaServersboot-and-list-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-list-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-list-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-list-server-detailed"></a>detailed<a href="#ScenarioNovaServersboot-and-list-server-detailed"> [ref]</a>
      </td>
      <td>True if the server listing should contain
detailed information about all of them
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-list-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-list-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_live_migrate_server [Scenario]

Live Migrate a server.

This scenario launches a VM on a compute node available in
the availability zone and then migrates the VM to another
compute node on the same availability zone.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between VM booting and running live migration
(of random duration from range [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-live-migrate-server-image"></a>image<a href="#ScenarioNovaServersboot-and-live-migrate-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-live-migrate-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-live-migrate-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-live-migrate-server-block-migration"></a>block_migration<a href="#ScenarioNovaServersboot-and-live-migrate-server-block-migration"> [ref]</a>
      </td>
      <td>Specifies the migration type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-live-migrate-server-disk-over-commit"></a>disk_over_commit<a href="#ScenarioNovaServersboot-and-live-migrate-server-disk-over-commit"> [ref]</a>
      </td>
      <td>Specifies whether to allow overcommit
on migrated instance or not
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-live-migrate-server-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-and-live-migrate-server-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-live-migrate-server-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-and-live-migrate-server-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-live-migrate-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-live-migrate-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_migrate_server [Scenario]

Migrate a server.

This scenario launches a VM on a compute node available in
the availability zone, and then migrates the VM
to another compute node on the same availability zone.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-migrate-server-image"></a>image<a href="#ScenarioNovaServersboot-and-migrate-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-migrate-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-migrate-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-migrate-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-migrate-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_rebuild_server [Scenario]

Rebuild a server.

This scenario launches a VM, then rebuilds that VM with a
different image.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-rebuild-server-from-image"></a>from_image<a href="#ScenarioNovaServersboot-and-rebuild-server-from-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-rebuild-server-to-image"></a>to_image<a href="#ScenarioNovaServersboot-and-rebuild-server-to-image"> [ref]</a>
      </td>
      <td>image to be used to rebuild the instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-rebuild-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-rebuild-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-rebuild-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-rebuild-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_show_server [Scenario]

Show server details.

This simple scenario tests the nova show command by retrieving
the server details.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-show-server-image"></a>image<a href="#ScenarioNovaServersboot-and-show-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-show-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-show-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-show-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-show-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation
</td>
    </tr>
  </tbody>
</table>


__Returns__:  
Server details

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_update_server [Scenario]

Boot a server, then update its name and description.

The scenario first creates a server, then update it.
Assumes that cleanup is done elsewhere.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-and-update-server-image"></a>image<a href="#ScenarioNovaServersboot-and-update-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-update-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-and-update-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-update-server-description"></a>description<a href="#ScenarioNovaServersboot-and-update-server-description"> [ref]</a>
      </td>
      <td>update the server description
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-and-update-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-and-update-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_lock_unlock_and_delete [Scenario]

Boot a server, lock it, then unlock and delete it.

Optional 'min_sleep' and 'max_sleep' parameters allow the
scenario to simulate a pause between locking and unlocking the
server (of random duration from min_sleep to max_sleep).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-lock-unlock-and-delete-image"></a>image<a href="#ScenarioNovaServersboot-lock-unlock-and-delete-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-lock-unlock-and-delete-flavor"></a>flavor<a href="#ScenarioNovaServersboot-lock-unlock-and-delete-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-lock-unlock-and-delete-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-lock-unlock-and-delete-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time between locking and unlocking
in seconds
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-lock-unlock-and-delete-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-lock-unlock-and-delete-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time between locking and unlocking
in seconds
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-lock-unlock-and-delete-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-lock-unlock-and-delete-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-lock-unlock-and-delete-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-lock-unlock-and-delete-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server [Scenario]

Boot a server.

Assumes that cleanup is done elsewhere.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-image"></a>image<a href="#ScenarioNovaServersboot-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-auto-assign-nic"></a>auto_assign_nic<a href="#ScenarioNovaServersboot-server-auto-assign-nic"> [ref]</a>
      </td>
      <td>True if NICs should be assigned
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_and_attach_interface [Scenario]

Create server and subnet, then attach the interface to it.

This scenario measures the "nova interface-attach" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-and-attach-interface-image"></a>image<a href="#ScenarioNovaServersboot-server-and-attach-interface-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-attach-interface-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-and-attach-interface-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-attach-interface-network-create-args"></a>network_create_args<a href="#ScenarioNovaServersboot-server-and-attach-interface-network-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/networks request
options.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-attach-interface-subnet-create-args"></a>subnet_create_args<a href="#ScenarioNovaServersboot-server-and-attach-interface-subnet-create-args"> [ref]</a>
      </td>
      <td>dict, POST /v2.0/subnets request options
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-attach-interface-subnet-cidr-start"></a>subnet_cidr_start<a href="#ScenarioNovaServersboot-server-and-attach-interface-subnet-cidr-start"> [ref]</a>
      </td>
      <td>str, start value for subnets CIDR
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-attach-interface-boot-server-args"></a>boot_server_args<a href="#ScenarioNovaServersboot-server-and-attach-interface-boot-server-args"> [ref]</a>
      </td>
      <td>Optional additional arguments for
server creation
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_and_list_interfaces [Scenario]

Boot a server and list interfaces attached to it.

Measure the "nova boot" and "nova interface-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-and-list-interfaces-image"></a>image<a href="#ScenarioNovaServersboot-server-and-list-interfaces-image"> [ref]</a>
      </td>
      <td>ID of the image to be used for server creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-list-interfaces-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-and-list-interfaces-flavor"> [ref]</a>
      </td>
      <td>ID of the flavor to be used for server creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-and-list-interfaces-kwargs"></a>**kwargs<a href="#ScenarioNovaServersboot-server-and-list-interfaces-kwargs"> [ref]</a>
      </td>
      <td>Optional arguments for booting the instance</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_associate_and_dissociate_floating_ip [Scenario]

Boot a server associate and dissociate a floating IP from it.

The scenario first boot a server and create a floating IP. then
associate the floating IP to the server.Finally dissociate the floating
IP.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-image"></a>image<a href="#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-create-floating-ip-args"></a>create_floating_ip_args<a href="#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-create-floating-ip-args"> [ref]</a>
      </td>
      <td>Optional additional arguments for
floating ip creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_attach_created_volume_and_live_migrate [Scenario]

Create a VM, attach a volume to it and live migrate.

Simple test to create a VM and attach a volume, then migrate the VM,
detach the volume and delete volume/VM.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between attaching a volume and running live
migration (of random duration from range [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-image"></a>image<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-image"> [ref]</a>
      </td>
      <td>Glance image name to use for the VM
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-size"></a>size<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-block-migration"></a>block_migration<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-block-migration"> [ref]</a>
      </td>
      <td>Specifies the migration type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-disk-over-commit"></a>disk_over_commit<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-disk-over-commit"> [ref]</a>
      </td>
      <td>Specifies whether to allow overcommit
on migrated instance or not
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-boot-server-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for VM creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for volume creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_attach_created_volume_and_resize [Scenario]

Create a VM from image, attach a volume to it and resize.

Simple test to create a VM and attach a volume, then resize the VM,
detach the volume then delete volume and VM.
Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between attaching a volume and running resize
(of random duration from range [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-image"></a>image<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-image"> [ref]</a>
      </td>
      <td>Glance image name to use for the VM
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-to-flavor"></a>to_flavor<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-to-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to resize the booted instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-confirm"></a>confirm<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-confirm"> [ref]</a>
      </td>
      <td>True if need to confirm resize else revert resize
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-do-delete"></a>do_delete<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-do-delete"> [ref]</a>
      </td>
      <td>True if resources needs to be deleted explicitly
else use rally cleanup to remove resources
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-boot-server-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for VM creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-created-volume-and-resize-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioNovaServersboot-server-attach-created-volume-and-resize-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for volume creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_attach_volume_and_list_attachments [Scenario]

Create a VM, attach N volume to it and list server's attachemnt.

Measure the "nova volume-attachments" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-attach-volume-and-list-attachments-image"></a>image<a href="#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-image"> [ref]</a>
      </td>
      <td>Glance image name to use for the VM
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-volume-and-list-attachments-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB), default 1G
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-num"></a>volume_num<a href="#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-num"> [ref]</a>
      </td>
      <td>the num of attached volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-volume-and-list-attachments-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-boot-server-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for VM creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-attach-volume-and-list-attachments-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for volume creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume [Scenario]

Boot a server from volume.

The scenario first creates a volume and then a server.
Assumes that cleanup is done elsewhere.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-from-volume-image"></a>image<a href="#ScenarioNovaServersboot-server-from-volume-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-from-volume-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-from-volume-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-volume-type"></a>volume_type<a href="#ScenarioNovaServersboot-server-from-volume-volume-type"> [ref]</a>
      </td>
      <td>specifies volume type when there are
multiple backends
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-auto-assign-nic"></a>auto_assign_nic<a href="#ScenarioNovaServersboot-server-from-volume-auto-assign-nic"> [ref]</a>
      </td>
      <td>True if NICs should be assigned
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-server-from-volume-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume_and_delete [Scenario]

Boot a server from volume and then delete it.

The scenario first creates a volume and then a server.
Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between volume creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-image"></a>image<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-volume-type"></a>volume_type<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-volume-type"> [ref]</a>
      </td>
      <td>specifies volume type when there are
multiple backends
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-delete-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-server-from-volume-and-delete-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume_and_live_migrate [Scenario]

Boot a server from volume and then migrate it.

The scenario first creates a volume and a server booted from
the volume on a compute node available in the availability zone and
then migrates the VM to another compute node on the same availability
zone.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between VM booting and running live migration
(of random duration from range [min_sleep, max_sleep]).

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-image"></a>image<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-type"></a>volume_type<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-type"> [ref]</a>
      </td>
      <td>specifies volume type when there are
multiple backends
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-block-migration"></a>block_migration<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-block-migration"> [ref]</a>
      </td>
      <td>Specifies the migration type
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-disk-over-commit"></a>disk_over_commit<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-disk-over-commit"> [ref]</a>
      </td>
      <td>Specifies whether to allow overcommit
on migrated instance or not
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-live-migrate-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-server-from-volume-and-live-migrate-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume_and_resize [Scenario]

Boot a server from volume, then resize and delete it.

The scenario first creates a volume and then a server.
Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between volume creation and deletion
(of random duration from [min_sleep, max_sleep]).

This test will confirm the resize by default,
or revert the resize if confirm is set to false.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-image"></a>image<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-to-flavor"></a>to_flavor<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-to-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to resize the booted instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-min-sleep"></a>min_sleep<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-min-sleep"> [ref]</a>
      </td>
      <td>Minimum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-max-sleep"></a>max_sleep<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-max-sleep"> [ref]</a>
      </td>
      <td>Maximum sleep time in seconds (non-negative)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-force-delete"></a>force_delete<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-confirm"></a>confirm<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-confirm"> [ref]</a>
      </td>
      <td>True if need to confirm resize else revert resize
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-do-delete"></a>do_delete<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-do-delete"> [ref]</a>
      </td>
      <td>True if resources needs to be deleted explicitly
else use rally cleanup to remove resources
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-boot-server-kwargs"></a>boot_server_kwargs<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-boot-server-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for VM creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-and-resize-create-volume-kwargs"></a>create_volume_kwargs<a href="#ScenarioNovaServersboot-server-from-volume-and-resize-create-volume-kwargs"> [ref]</a>
      </td>
      <td>optional arguments for volume creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume_snapshot [Scenario]

Boot a server from a snapshot.

The scenario first creates a volume and creates a
snapshot from this volume, then boots a server from
the created snapshot.
Assumes that cleanup is done elsewhere.

__Platform__: openstack

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
        <a name="ScenarioNovaServersboot-server-from-volume-snapshot-image"></a>image<a href="#ScenarioNovaServersboot-server-from-volume-snapshot-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-snapshot-flavor"></a>flavor<a href="#ScenarioNovaServersboot-server-from-volume-snapshot-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-snapshot-volume-size"></a>volume_size<a href="#ScenarioNovaServersboot-server-from-volume-snapshot-volume-size"> [ref]</a>
      </td>
      <td>volume size (in GB)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-snapshot-volume-type"></a>volume_type<a href="#ScenarioNovaServersboot-server-from-volume-snapshot-volume-type"> [ref]</a>
      </td>
      <td>specifies volume type when there are
multiple backends
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-snapshot-auto-assign-nic"></a>auto_assign_nic<a href="#ScenarioNovaServersboot-server-from-volume-snapshot-auto-assign-nic"> [ref]</a>
      </td>
      <td>True if NICs should be assigned
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersboot-server-from-volume-snapshot-kwargs"></a>kwargs<a href="#ScenarioNovaServersboot-server-from-volume-snapshot-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.list_servers [Scenario]

List all servers.

This simple scenario test the nova list command by listing
all the servers.

__Platform__: openstack

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
        <a name="ScenarioNovaServerslist-servers-detailed"></a>detailed<a href="#ScenarioNovaServerslist-servers-detailed"> [ref]</a>
      </td>
      <td>True if detailed information about servers
should be listed
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.pause_and_unpause_server [Scenario]

Create a server, pause, unpause and then delete it.

__Platform__: openstack

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
        <a name="ScenarioNovaServerspause-and-unpause-server-image"></a>image<a href="#ScenarioNovaServerspause-and-unpause-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerspause-and-unpause-server-flavor"></a>flavor<a href="#ScenarioNovaServerspause-and-unpause-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerspause-and-unpause-server-force-delete"></a>force_delete<a href="#ScenarioNovaServerspause-and-unpause-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerspause-and-unpause-server-kwargs"></a>kwargs<a href="#ScenarioNovaServerspause-and-unpause-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.resize_server [Scenario]

Boot a server, then resize and delete it.

This test will confirm the resize by default,
or revert the resize if confirm is set to false.

__Platform__: openstack

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
        <a name="ScenarioNovaServersresize-server-image"></a>image<a href="#ScenarioNovaServersresize-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-server-flavor"></a>flavor<a href="#ScenarioNovaServersresize-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-server-to-flavor"></a>to_flavor<a href="#ScenarioNovaServersresize-server-to-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to resize the booted instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-server-force-delete"></a>force_delete<a href="#ScenarioNovaServersresize-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersresize-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.resize_shutoff_server [Scenario]

Boot a server and stop it, then resize and delete it.

This test will confirm the resize by default,
or revert the resize if confirm is set to false.

__Platform__: openstack

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
        <a name="ScenarioNovaServersresize-shutoff-server-image"></a>image<a href="#ScenarioNovaServersresize-shutoff-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-shutoff-server-flavor"></a>flavor<a href="#ScenarioNovaServersresize-shutoff-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-shutoff-server-to-flavor"></a>to_flavor<a href="#ScenarioNovaServersresize-shutoff-server-to-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to resize the booted instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-shutoff-server-confirm"></a>confirm<a href="#ScenarioNovaServersresize-shutoff-server-confirm"> [ref]</a>
      </td>
      <td>True if need to confirm resize else revert resize
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-shutoff-server-force-delete"></a>force_delete<a href="#ScenarioNovaServersresize-shutoff-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersresize-shutoff-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersresize-shutoff-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.shelve_and_unshelve_server [Scenario]

Create a server, shelve, unshelve and then delete it.

__Platform__: openstack

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
        <a name="ScenarioNovaServersshelve-and-unshelve-server-image"></a>image<a href="#ScenarioNovaServersshelve-and-unshelve-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersshelve-and-unshelve-server-flavor"></a>flavor<a href="#ScenarioNovaServersshelve-and-unshelve-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersshelve-and-unshelve-server-force-delete"></a>force_delete<a href="#ScenarioNovaServersshelve-and-unshelve-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServersshelve-and-unshelve-server-kwargs"></a>kwargs<a href="#ScenarioNovaServersshelve-and-unshelve-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.snapshot_server [Scenario]

Boot a server, make its snapshot and delete both.

__Platform__: openstack

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
        <a name="ScenarioNovaServerssnapshot-server-image"></a>image<a href="#ScenarioNovaServerssnapshot-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerssnapshot-server-flavor"></a>flavor<a href="#ScenarioNovaServerssnapshot-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerssnapshot-server-force-delete"></a>force_delete<a href="#ScenarioNovaServerssnapshot-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerssnapshot-server-kwargs"></a>kwargs<a href="#ScenarioNovaServerssnapshot-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.suspend_and_resume_server [Scenario]

Create a server, suspend, resume and then delete it.

__Platform__: openstack

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
        <a name="ScenarioNovaServerssuspend-and-resume-server-image"></a>image<a href="#ScenarioNovaServerssuspend-and-resume-server-image"> [ref]</a>
      </td>
      <td>image to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerssuspend-and-resume-server-flavor"></a>flavor<a href="#ScenarioNovaServerssuspend-and-resume-server-flavor"> [ref]</a>
      </td>
      <td>flavor to be used to boot an instance
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerssuspend-and-resume-server-force-delete"></a>force_delete<a href="#ScenarioNovaServerssuspend-and-resume-server-force-delete"> [ref]</a>
      </td>
      <td>True if force_delete should be used
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServerssuspend-and-resume-server-kwargs"></a>kwargs<a href="#ScenarioNovaServerssuspend-and-resume-server-kwargs"> [ref]</a>
      </td>
      <td>Optional additional arguments for server creation</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServices.list_services [Scenario]

List all nova services.

Measure the "nova service-list" command performance.

__Platform__: openstack

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
        <a name="ScenarioNovaServiceslist-services-host"></a>host<a href="#ScenarioNovaServiceslist-services-host"> [ref]</a>
      </td>
      <td>List nova services on host
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioNovaServiceslist-services-binary"></a>binary<a href="#ScenarioNovaServiceslist-services-binary"> [ref]</a>
      </td>
      <td>List nova services matching given binary</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.nova.services](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/services.py)

<hr />

#### Quotas.cinder_get [Scenario]

Get quotas for Cinder.

Measure the "cinder quota-show" command performance

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.cinder_update [Scenario]

Update quotas for Cinder.

__Platform__: openstack

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
        <a name="ScenarioQuotascinder-update-max-quota"></a>max_quota<a href="#ScenarioQuotascinder-update-max-quota"> [ref]</a>
      </td>
      <td>Max value to be updated for quota.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.cinder_update_and_delete [Scenario]

Update and Delete quotas for Cinder.

__Platform__: openstack

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
        <a name="ScenarioQuotascinder-update-and-delete-max-quota"></a>max_quota<a href="#ScenarioQuotascinder-update-and-delete-max-quota"> [ref]</a>
      </td>
      <td>Max value to be updated for quota.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.neutron_update [Scenario]

Update quotas for neutron.

__Platform__: openstack

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
        <a name="ScenarioQuotasneutron-update-max-quota"></a>max_quota<a href="#ScenarioQuotasneutron-update-max-quota"> [ref]</a>
      </td>
      <td>Max value to be updated for quota.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.nova_get [Scenario]

Get quotas for nova.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.nova_update [Scenario]

Update quotas for Nova.

__Platform__: openstack

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
        <a name="ScenarioQuotasnova-update-max-quota"></a>max_quota<a href="#ScenarioQuotasnova-update-max-quota"> [ref]</a>
      </td>
      <td>Max value to be updated for quota.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.nova_update_and_delete [Scenario]

Update and delete quotas for Nova.

__Platform__: openstack

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
        <a name="ScenarioQuotasnova-update-and-delete-max-quota"></a>max_quota<a href="#ScenarioQuotasnova-update-and-delete-max-quota"> [ref]</a>
      </td>
      <td>Max value to be updated for quota.</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true, "users": true}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### SaharaClusters.create_and_delete_cluster [Scenario]

Launch and delete a Sahara Cluster.

This scenario launches a Hadoop cluster, waits until it becomes
'Active' and deletes it.

__Platform__: openstack

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
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-flavor"></a>flavor<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be for nodes in the
created node groups. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-master-flavor"></a>master_flavor<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-master-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be used for the master
instance of the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-worker-flavor"></a>worker_flavor<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-worker-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be used for the workers of
the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-workers-count"></a>workers_count<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-workers-count"> [ref]</a>
      </td>
      <td>number of worker instances in a cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-plugin-name"></a>plugin_name<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-plugin-name"> [ref]</a>
      </td>
      <td>name of a provisioning plugin
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-hadoop-version"></a>hadoop_version<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-hadoop-version"> [ref]</a>
      </td>
      <td>version of Hadoop distribution supported by
the specified plugin.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-floating-ip-pool"></a>floating_ip_pool<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-floating-ip-pool"> [ref]</a>
      </td>
      <td>floating ip pool name from which Floating
IPs will be allocated. Sahara will determine
automatically how to treat this depending on
its own configurations. Defaults to None
because in some cases Sahara may work w/o
Floating IPs.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-volumes-per-node"></a>volumes_per_node<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-volumes-per-node"> [ref]</a>
      </td>
      <td>number of Cinder volumes that will be
attached to every cluster node
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-volumes-size"></a>volumes_size<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-volumes-size"> [ref]</a>
      </td>
      <td>size of each Cinder volume in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-auto-security-group"></a>auto_security_group<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-auto-security-group"> [ref]</a>
      </td>
      <td>boolean value. If set to True Sahara will
create a Security Group for each Node Group
in the Cluster automatically.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-security-groups"></a>security_groups<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-security-groups"> [ref]</a>
      </td>
      <td>list of security groups that will be used
while creating VMs. If auto_security_group
is set to True, this list can be left empty.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-node-configs"></a>node_configs<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-node-configs"> [ref]</a>
      </td>
      <td>config dict that will be passed to each Node
Group
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-cluster-configs"></a>cluster_configs<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-cluster-configs"> [ref]</a>
      </td>
      <td>config dict that will be passed to the
Cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-enable-anti-affinity"></a>enable_anti_affinity<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-enable-anti-affinity"> [ref]</a>
      </td>
      <td>If set to true the vms will be scheduled
one per compute node.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-enable-proxy"></a>enable_proxy<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-enable-proxy"> [ref]</a>
      </td>
      <td>Use Master Node of a Cluster as a Proxy node and
do not assign floating ips to workers.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-and-delete-cluster-use-autoconfig"></a>use_autoconfig<a href="#ScenarioSaharaClusterscreate-and-delete-cluster-use-autoconfig"> [ref]</a>
      </td>
      <td>If True, instances of the node group will be
automatically configured during cluster
creation. If False, the configuration values
should be specify manually
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.sahara.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/clusters.py)

<hr />

#### SaharaClusters.create_scale_delete_cluster [Scenario]

Launch, scale and delete a Sahara Cluster.

This scenario launches a Hadoop cluster, waits until it becomes
'Active'. Then a series of scale operations is applied. The scaling
happens according to numbers listed in

__Platform__: openstack

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
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-flavor"></a>flavor<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be for nodes in the
created node groups. Deprecated.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-master-flavor"></a>master_flavor<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-master-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be used for the master
instance of the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-worker-flavor"></a>worker_flavor<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-worker-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be used for the workers of
the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-workers-count"></a>workers_count<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-workers-count"> [ref]</a>
      </td>
      <td>number of worker instances in a cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-plugin-name"></a>plugin_name<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-plugin-name"> [ref]</a>
      </td>
      <td>name of a provisioning plugin
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-hadoop-version"></a>hadoop_version<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-hadoop-version"> [ref]</a>
      </td>
      <td>version of Hadoop distribution supported by
the specified plugin.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-deltas"></a>deltas<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-deltas"> [ref]</a>
      </td>
      <td>list of integers which will be used to add or
remove worker nodes from the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-floating-ip-pool"></a>floating_ip_pool<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-floating-ip-pool"> [ref]</a>
      </td>
      <td>floating ip pool name from which Floating
IPs will be allocated. Sahara will determine
automatically how to treat this depending on
its own configurations. Defaults to None
because in some cases Sahara may work w/o
Floating IPs.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-neutron-net-id"></a>neutron_net_id<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-neutron-net-id"> [ref]</a>
      </td>
      <td>id of a Neutron network that will be used
for fixed IPs. This parameter is ignored when
Nova Network is set up.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-per-node"></a>volumes_per_node<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-per-node"> [ref]</a>
      </td>
      <td>number of Cinder volumes that will be
attached to every cluster node
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-size"></a>volumes_size<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-size"> [ref]</a>
      </td>
      <td>size of each Cinder volume in GB
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-auto-security-group"></a>auto_security_group<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-auto-security-group"> [ref]</a>
      </td>
      <td>boolean value. If set to True Sahara will
create a Security Group for each Node Group
in the Cluster automatically.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-security-groups"></a>security_groups<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-security-groups"> [ref]</a>
      </td>
      <td>list of security groups that will be used
while creating VMs. If auto_security_group
is set to True this list can be left empty.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-node-configs"></a>node_configs<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-node-configs"> [ref]</a>
      </td>
      <td>configs dict that will be passed to each Node
Group
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-cluster-configs"></a>cluster_configs<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-cluster-configs"> [ref]</a>
      </td>
      <td>configs dict that will be passed to the
Cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-enable-anti-affinity"></a>enable_anti_affinity<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-enable-anti-affinity"> [ref]</a>
      </td>
      <td>If set to true the vms will be scheduled
one per compute node.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-enable-proxy"></a>enable_proxy<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-enable-proxy"> [ref]</a>
      </td>
      <td>Use Master Node of a Cluster as a Proxy node and
do not assign floating ips to workers.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaClusterscreate-scale-delete-cluster-use-autoconfig"></a>use_autoconfig<a href="#ScenarioSaharaClusterscreate-scale-delete-cluster-use-autoconfig"> [ref]</a>
      </td>
      <td>If True, instances of the node group will be
automatically configured during cluster
creation. If False, the configuration values
should be specify manually
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.sahara.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/clusters.py)

<hr />

#### SaharaJob.create_launch_job [Scenario]

Create and execute a Sahara EDP Job.

This scenario Creates a Job entity and launches an execution on a
Cluster.

__Platform__: openstack

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
        <a name="ScenarioSaharaJobcreate-launch-job-job-type"></a>job_type<a href="#ScenarioSaharaJobcreate-launch-job-job-type"> [ref]</a>
      </td>
      <td>type of the Data Processing Job
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaJobcreate-launch-job-configs"></a>configs<a href="#ScenarioSaharaJobcreate-launch-job-configs"> [ref]</a>
      </td>
      <td>config dict that will be passed to a Job Execution
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaJobcreate-launch-job-job-idx"></a>job_idx<a href="#ScenarioSaharaJobcreate-launch-job-job-idx"> [ref]</a>
      </td>
      <td>index of a job in a sequence. This index will be
used to create different atomic actions for each job
in a sequence
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.sahara.jobs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/jobs.py)

<hr />

#### SaharaJob.create_launch_job_sequence [Scenario]

Create and execute a sequence of the Sahara EDP Jobs.

This scenario Creates a Job entity and launches an execution on a
Cluster for every job object provided.

__Platform__: openstack

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
        <a name="ScenarioSaharaJobcreate-launch-job-sequence-jobs"></a>jobs<a href="#ScenarioSaharaJobcreate-launch-job-sequence-jobs"> [ref]</a>
      </td>
      <td>list of jobs that should be executed in one context</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.sahara.jobs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/jobs.py)

<hr />

#### SaharaJob.create_launch_job_sequence_with_scaling [Scenario]

Create and execute Sahara EDP Jobs on a scaling Cluster.

This scenario Creates a Job entity and launches an execution on a
Cluster for every job object provided. The Cluster is scaled according
to the deltas values and the sequence is launched again.

__Platform__: openstack

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
        <a name="ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-jobs"></a>jobs<a href="#ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-jobs"> [ref]</a>
      </td>
      <td>list of jobs that should be executed in one context
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-deltas"></a>deltas<a href="#ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-deltas"> [ref]</a>
      </td>
      <td>list of integers which will be used to add or
remove worker nodes from the cluster
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.sahara.jobs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/jobs.py)

<hr />

#### SaharaNodeGroupTemplates.create_and_list_node_group_templates [Scenario]

Create and list Sahara Node Group Templates.

This scenario creates two Node Group Templates with different set of
node processes. The master Node Group Template contains Hadoop's
management processes. The worker Node Group Template contains
Hadoop's worker processes.

By default the templates are created for the vanilla Hadoop
provisioning plugin using the version 1.2.1

After the templates are created the list operation is called.

__Platform__: openstack

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
        <a name="ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-flavor"></a>flavor<a href="#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be for nodes in the
created node groups
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-plugin-name"></a>plugin_name<a href="#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-plugin-name"> [ref]</a>
      </td>
      <td>name of a provisioning plugin
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-hadoop-version"></a>hadoop_version<a href="#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-hadoop-version"> [ref]</a>
      </td>
      <td>version of Hadoop distribution supported by
the specified plugin.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-use-autoconfig"></a>use_autoconfig<a href="#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-use-autoconfig"> [ref]</a>
      </td>
      <td>If True, instances of the node group will be
automatically configured during cluster
creation. If False, the configuration values
should be specify manually
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.sahara.node_group_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/node_group_templates.py)

<hr />

#### SaharaNodeGroupTemplates.create_delete_node_group_templates [Scenario]

Create and delete Sahara Node Group Templates.

This scenario creates and deletes two most common types of
Node Group Templates.

By default the templates are created for the vanilla Hadoop
provisioning plugin using the version 1.2.1

__Platform__: openstack

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
        <a name="ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-flavor"></a>flavor<a href="#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-flavor"> [ref]</a>
      </td>
      <td>Nova flavor that will be for nodes in the
created node groups
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-plugin-name"></a>plugin_name<a href="#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-plugin-name"> [ref]</a>
      </td>
      <td>name of a provisioning plugin
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-hadoop-version"></a>hadoop_version<a href="#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-hadoop-version"> [ref]</a>
      </td>
      <td>version of Hadoop distribution supported by
the specified plugin.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-use-autoconfig"></a>use_autoconfig<a href="#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-use-autoconfig"> [ref]</a>
      </td>
      <td>If True, instances of the node group will be
automatically configured during cluster
creation. If False, the configuration values
should be specify manually
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.sahara.node_group_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/node_group_templates.py)

<hr />

#### SenlinClusters.create_and_delete_cluster [Scenario]

Create a cluster and then delete it.

Measure the "senlin cluster-create" and "senlin cluster-delete"
commands performance.

__Platform__: openstack

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
        <a name="ScenarioSenlinClusterscreate-and-delete-cluster-desired-capacity"></a>desired_capacity<a href="#ScenarioSenlinClusterscreate-and-delete-cluster-desired-capacity"> [ref]</a>
      </td>
      <td>The capacity or initial number of nodes
owned by the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSenlinClusterscreate-and-delete-cluster-min-size"></a>min_size<a href="#ScenarioSenlinClusterscreate-and-delete-cluster-min-size"> [ref]</a>
      </td>
      <td>The minimum number of nodes owned by the cluster
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSenlinClusterscreate-and-delete-cluster-max-size"></a>max_size<a href="#ScenarioSenlinClusterscreate-and-delete-cluster-max-size"> [ref]</a>
      </td>
      <td>The maximum number of nodes owned by the cluster.
-1 means no limit
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSenlinClusterscreate-and-delete-cluster-timeout"></a>timeout<a href="#ScenarioSenlinClusterscreate-and-delete-cluster-timeout"> [ref]</a>
      </td>
      <td>The timeout value in seconds for cluster creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSenlinClusterscreate-and-delete-cluster-metadata"></a>metadata<a href="#ScenarioSenlinClusterscreate-and-delete-cluster-metadata"> [ref]</a>
      </td>
      <td>A set of key value pairs to associate with the cluster</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.senlin.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/senlin/clusters.py)

<hr />

#### SwiftObjects.create_container_and_object_then_delete_all [Scenario]

Create container and objects then delete everything created.

__Platform__: openstack

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
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-delete-all-objects-per-container"></a>objects_per_container<a href="#ScenarioSwiftObjectscreate-container-and-object-then-delete-all-objects-per-container"> [ref]</a>
      </td>
      <td>int, number of objects to upload
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-delete-all-object-size"></a>object_size<a href="#ScenarioSwiftObjectscreate-container-and-object-then-delete-all-object-size"> [ref]</a>
      </td>
      <td>int, temporary local object size
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-delete-all-kwargs"></a>kwargs<a href="#ScenarioSwiftObjectscreate-container-and-object-then-delete-all-kwargs"> [ref]</a>
      </td>
      <td>dict, optional parameters to create container</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.create_container_and_object_then_download_object [Scenario]

Create container and objects then download all objects.

__Platform__: openstack

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
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-download-object-objects-per-container"></a>objects_per_container<a href="#ScenarioSwiftObjectscreate-container-and-object-then-download-object-objects-per-container"> [ref]</a>
      </td>
      <td>int, number of objects to upload
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-download-object-object-size"></a>object_size<a href="#ScenarioSwiftObjectscreate-container-and-object-then-download-object-object-size"> [ref]</a>
      </td>
      <td>int, temporary local object size
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-download-object-kwargs"></a>kwargs<a href="#ScenarioSwiftObjectscreate-container-and-object-then-download-object-kwargs"> [ref]</a>
      </td>
      <td>dict, optional parameters to create container</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.create_container_and_object_then_list_objects [Scenario]

Create container and objects then list all objects.

__Platform__: openstack

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
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-list-objects-objects-per-container"></a>objects_per_container<a href="#ScenarioSwiftObjectscreate-container-and-object-then-list-objects-objects-per-container"> [ref]</a>
      </td>
      <td>int, number of objects to upload
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-list-objects-object-size"></a>object_size<a href="#ScenarioSwiftObjectscreate-container-and-object-then-list-objects-object-size"> [ref]</a>
      </td>
      <td>int, temporary local object size
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioSwiftObjectscreate-container-and-object-then-list-objects-kwargs"></a>kwargs<a href="#ScenarioSwiftObjectscreate-container-and-object-then-list-objects-kwargs"> [ref]</a>
      </td>
      <td>dict, optional parameters to create container</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.list_and_download_objects_in_containers [Scenario]

List and download objects in all containers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.list_objects_in_containers [Scenario]

List objects in all containers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### VMTasks.boot_runcommand_delete [Scenario]

Boot a server, run script specified in command and delete server.

__Platform__: openstack

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
        <a name="ScenarioVMTasksboot-runcommand-delete-image"></a>image<a href="#ScenarioVMTasksboot-runcommand-delete-image"> [ref]</a>
      </td>
      <td>glance image name to use for the vm. Optional
in case of specified "image_command_customizer" context
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-flavor"></a>flavor<a href="#ScenarioVMTasksboot-runcommand-delete-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-username"></a>username<a href="#ScenarioVMTasksboot-runcommand-delete-username"> [ref]</a>
      </td>
      <td>ssh username on server, str
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-password"></a>password<a href="#ScenarioVMTasksboot-runcommand-delete-password"> [ref]</a>
      </td>
      <td>Password on SSH authentication
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-command"></a>command<a href="#ScenarioVMTasksboot-runcommand-delete-command"> [ref]</a>
      </td>
      <td>Command-specifying dictionary that either specifies
remote command path via `remote_path' (can be uploaded from a
local file specified by `local_path`), an inline script via
`script_inline' or a local script file path using `script_file'.
Both `script_file' and `local_path' are checked to be accessible
by the `file_exists' validator code.

The `script_inline' and `script_file' both require an `interpreter'
value to specify the interpreter script should be run with.

Note that any of `interpreter' and `remote_path' can be an array
prefixed with environment variables and suffixed with args for
the `interpreter' command. `remote_path's last component must be
a path to a command to execute (also upload destination if a
`local_path' is given). Uploading an interpreter is possible
but requires that `remote_path' and `interpreter' path do match.

Examples:

  .. code-block:: python

    # Run a `local_script.pl' file sending it to a remote
    # Perl interpreter
    command = {
        "script_file": "local_script.pl",
        "interpreter": "/usr/bin/perl"
    }

    # Run an inline script sending it to a remote interpreter
    command = {
        "script_inline": "echo 'Hello, World!'",
        "interpreter": "/bin/sh"
    }

    # Run a remote command
    command = {
        "remote_path": "/bin/false"
    }

    # Copy a local command and run it
    command = {
        "remote_path": "/usr/local/bin/fio",
        "local_path": "/home/foobar/myfiodir/bin/fio"
    }

    # Copy a local command and run it with environment variable
    command = {
        "remote_path": ["HOME=/root", "/usr/local/bin/fio"],
        "local_path": "/home/foobar/myfiodir/bin/fio"
    }

    # Run an inline script sending it to a remote interpreter
    command = {
        "script_inline": "echo "Hello, ${NAME:-World}"",
        "interpreter": ["NAME=Earth", "/bin/sh"]
    }

    # Run an inline script sending it to an uploaded remote
    # interpreter
    command = {
        "script_inline": "echo "Hello, ${NAME:-World}"",
        "interpreter": ["NAME=Earth", "/tmp/sh"],
        "remote_path": "/tmp/sh",
        "local_path": "/home/user/work/cve/sh-1.0/bin/sh"
    }
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-volume-args"></a>volume_args<a href="#ScenarioVMTasksboot-runcommand-delete-volume-args"> [ref]</a>
      </td>
      <td>volume args for booting server from volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-floating-network"></a>floating_network<a href="#ScenarioVMTasksboot-runcommand-delete-floating-network"> [ref]</a>
      </td>
      <td>external network name, for floating ip
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-port"></a>port<a href="#ScenarioVMTasksboot-runcommand-delete-port"> [ref]</a>
      </td>
      <td>ssh port for SSH connection
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-use-floating-ip"></a>use_floating_ip<a href="#ScenarioVMTasksboot-runcommand-delete-use-floating-ip"> [ref]</a>
      </td>
      <td>bool, floating or fixed IP for SSH connection
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-force-delete"></a>force_delete<a href="#ScenarioVMTasksboot-runcommand-delete-force-delete"> [ref]</a>
      </td>
      <td>whether to use force_delete for servers
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-wait-for-ping"></a>wait_for_ping<a href="#ScenarioVMTasksboot-runcommand-delete-wait-for-ping"> [ref]</a>
      </td>
      <td>whether to check connectivity on server creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-max-log-length"></a>max_log_length<a href="#ScenarioVMTasksboot-runcommand-delete-max-log-length"> [ref]</a>
      </td>
      <td>The number of tail nova console-log lines user
would like to retrieve
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksboot-runcommand-delete-kwargs"></a>kwargs<a href="#ScenarioVMTasksboot-runcommand-delete-kwargs"> [ref]</a>
      </td>
      <td>extra arguments for booting the server</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.vm.vmtasks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/vm/vmtasks.py)

<hr />

#### VMTasks.dd_load_test [Scenario]

Boot a server from a custom image and performs dd load test.

!!! note
    dd load test is prepared script by Rally team. It checks
    writing and reading metrics from the VM.

__Platform__: openstack

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
        <a name="ScenarioVMTasksdd-load-test-image"></a>image<a href="#ScenarioVMTasksdd-load-test-image"> [ref]</a>
      </td>
      <td>glance image name to use for the vm. Optional
in case of specified "image_command_customizer" context
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-flavor"></a>flavor<a href="#ScenarioVMTasksdd-load-test-flavor"> [ref]</a>
      </td>
      <td>VM flavor name
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-username"></a>username<a href="#ScenarioVMTasksdd-load-test-username"> [ref]</a>
      </td>
      <td>ssh username on server, str
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-password"></a>password<a href="#ScenarioVMTasksdd-load-test-password"> [ref]</a>
      </td>
      <td>Password on SSH authentication
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-interpreter"></a>interpreter<a href="#ScenarioVMTasksdd-load-test-interpreter"> [ref]</a>
      </td>
      <td>the interpreter to execute script with dd load test
(defaults to /bin/sh)
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-command"></a>command<a href="#ScenarioVMTasksdd-load-test-command"> [ref]</a>
      </td>
      <td>DEPRECATED. use interpreter instead.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-volume-args"></a>volume_args<a href="#ScenarioVMTasksdd-load-test-volume-args"> [ref]</a>
      </td>
      <td>volume args for booting server from volume
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-floating-network"></a>floating_network<a href="#ScenarioVMTasksdd-load-test-floating-network"> [ref]</a>
      </td>
      <td>external network name, for floating ip
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-port"></a>port<a href="#ScenarioVMTasksdd-load-test-port"> [ref]</a>
      </td>
      <td>ssh port for SSH connection
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-use-floating-ip"></a>use_floating_ip<a href="#ScenarioVMTasksdd-load-test-use-floating-ip"> [ref]</a>
      </td>
      <td>bool, floating or fixed IP for SSH connection
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-force-delete"></a>force_delete<a href="#ScenarioVMTasksdd-load-test-force-delete"> [ref]</a>
      </td>
      <td>whether to use force_delete for servers
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-wait-for-ping"></a>wait_for_ping<a href="#ScenarioVMTasksdd-load-test-wait-for-ping"> [ref]</a>
      </td>
      <td>whether to check connectivity on server creation
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-max-log-length"></a>max_log_length<a href="#ScenarioVMTasksdd-load-test-max-log-length"> [ref]</a>
      </td>
      <td>The number of tail nova console-log lines user
would like to retrieve
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksdd-load-test-kwargs"></a>kwargs<a href="#ScenarioVMTasksdd-load-test-kwargs"> [ref]</a>
      </td>
      <td>extra arguments for booting the server</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"users": true}

__Module__: [rally_openstack.scenarios.vm.vmtasks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/vm/vmtasks.py)

<hr />

#### VMTasks.runcommand_heat [Scenario]

Run workload on stack deployed by heat.

Workload can be either file or resource:

```json
{"file": "/path/to/file.sh"}
{"resource": ["package.module", "workload.py"]}
```

> Also it should contain "username" key.

> Given file will be uploaded to `gate_node` and started. This script
should print `key` `value` pairs separated by colon. These pairs will
be presented in results.

> Gate node should be accessible via ssh with keypair `key_name`, so
heat template should accept parameter `key_name`.

__Platform__: openstack

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
        <a name="ScenarioVMTasksruncommand-heat-workload"></a>workload<a href="#ScenarioVMTasksruncommand-heat-workload"> [ref]</a>
      </td>
      <td>workload to run
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksruncommand-heat-template"></a>template<a href="#ScenarioVMTasksruncommand-heat-template"> [ref]</a>
      </td>
      <td>path to heat template file
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksruncommand-heat-files"></a>files<a href="#ScenarioVMTasksruncommand-heat-files"> [ref]</a>
      </td>
      <td>additional template files
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioVMTasksruncommand-heat-parameters"></a>parameters<a href="#ScenarioVMTasksruncommand-heat-parameters"> [ref]</a>
      </td>
      <td>parameters for heat template</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.vm.vmtasks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/vm/vmtasks.py)

<hr />

#### Watcher.create_audit_and_delete [Scenario]

Create and delete audit.

Create Audit, wait until whether Audit is in SUCCEEDED state or in
FAILED and delete audit.

__Platform__: openstack

__Module__: [rally_openstack.scenarios.watcher.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/watcher/basic.py)

<hr />

#### Watcher.create_audit_template_and_delete [Scenario]

Create audit template and delete it.

__Platform__: openstack

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
        <a name="ScenarioWatchercreate-audit-template-and-delete-goal"></a>goal<a href="#ScenarioWatchercreate-audit-template-and-delete-goal"> [ref]</a>
      </td>
      <td>The goal audit template is based on
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatchercreate-audit-template-and-delete-strategy"></a>strategy<a href="#ScenarioWatchercreate-audit-template-and-delete-strategy"> [ref]</a>
      </td>
      <td>The strategy used to provide resource optimization
algorithm
</td>
    </tr>
  </tbody>
</table>


__Requires platform(s)__:

* openstack with the next options: {"admin": true}

__Module__: [rally_openstack.scenarios.watcher.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/watcher/basic.py)

<hr />

#### Watcher.list_audit_templates [Scenario]

List existing audit templates.

Audit templates are being created by Audit Template Context.

__Platform__: openstack

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
        <a name="ScenarioWatcherlist-audit-templates-name"></a>name<a href="#ScenarioWatcherlist-audit-templates-name"> [ref]</a>
      </td>
      <td>Name of the audit template
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatcherlist-audit-templates-goal"></a>goal<a href="#ScenarioWatcherlist-audit-templates-goal"> [ref]</a>
      </td>
      <td>Name of the goal
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatcherlist-audit-templates-strategy"></a>strategy<a href="#ScenarioWatcherlist-audit-templates-strategy"> [ref]</a>
      </td>
      <td>Name of the strategy
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatcherlist-audit-templates-limit"></a>limit<a href="#ScenarioWatcherlist-audit-templates-limit"> [ref]</a>
      </td>
      <td>The maximum number of results to return per
request, if:

  1) limit > 0, the maximum number of audit templates to return.
  2) limit == 0, return the entire list of audit_templates.
  3) limit param is NOT specified (None), the number of items
     returned respect the maximum imposed by the Watcher API
    (see Watcher's api.max_limit option).
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatcherlist-audit-templates-sort-key"></a>sort_key<a href="#ScenarioWatcherlist-audit-templates-sort-key"> [ref]</a>
      </td>
      <td>Optional, field used for sorting.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatcherlist-audit-templates-sort-dir"></a>sort_dir<a href="#ScenarioWatcherlist-audit-templates-sort-dir"> [ref]</a>
      </td>
      <td>Optional, direction of sorting, either 'asc' (the
default) or 'desc'.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioWatcherlist-audit-templates-detail"></a>detail<a href="#ScenarioWatcherlist-audit-templates-detail"> [ref]</a>
      </td>
      <td>Optional, boolean whether to return detailed information
about audit_templates.
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.watcher.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/watcher/basic.py)

<hr />

#### ZaqarBasic.create_queue [Scenario]

Create a Zaqar queue with a random name.

__Platform__: openstack

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
        <a name="ScenarioZaqarBasiccreate-queue-kwargs"></a>kwargs<a href="#ScenarioZaqarBasiccreate-queue-kwargs"> [ref]</a>
      </td>
      <td>other optional parameters to create queues like
"metadata"
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.zaqar.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/zaqar/basic.py)

<hr />

#### ZaqarBasic.producer_consumer [Scenario]

Serial message producer/consumer.

Creates a Zaqar queue with random name, sends a set of messages
and then retrieves an iterator containing those.

__Platform__: openstack

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
        <a name="ScenarioZaqarBasicproducer-consumer-min-msg-count"></a>min_msg_count<a href="#ScenarioZaqarBasicproducer-consumer-min-msg-count"> [ref]</a>
      </td>
      <td>min number of messages to be posted
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioZaqarBasicproducer-consumer-max-msg-count"></a>max_msg_count<a href="#ScenarioZaqarBasicproducer-consumer-max-msg-count"> [ref]</a>
      </td>
      <td>max number of messages to be posted
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="ScenarioZaqarBasicproducer-consumer-kwargs"></a>kwargs<a href="#ScenarioZaqarBasicproducer-consumer-kwargs"> [ref]</a>
      </td>
      <td>other optional parameters to create queues like
"metadata"
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.zaqar.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/zaqar/basic.py)

<hr />

### Validator

A base class for all validators.

#### check_api_versions [Validator]

Additional validation for api_versions context.

__Platform__: default

__Module__: [rally_openstack.contexts.api_versions](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/api_versions.py)

<hr />

#### check_cleanup_resources [Validator]

Validates that openstack resource managers exist.

__Platform__: default

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
        <a name="Validatorcheck-cleanup-resources-admin-required"></a>admin_required<a href="#Validatorcheck-cleanup-resources-admin-required"> [ref]</a>
      </td>
      <td>describes access level to resource</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.contexts.cleanup.base](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/cleanup/base.py)

<hr />

#### external_network_exists [Validator]

Validator checks that external network with given name exists.

__Platform__: openstack

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
        <a name="Validatorexternal-network-exists-param-name"></a>param_name<a href="#Validatorexternal-network-exists-param-name"> [ref]</a>
      </td>
      <td>name of validated network</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### flavor_exists [Validator]

Returns validator for flavor.

__Platform__: openstack

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
        <a name="Validatorflavor-exists-param-name"></a>param_name<a href="#Validatorflavor-exists-param-name"> [ref]</a>
      </td>
      <td>defines which variable should be used
to get flavor id value.
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### image_exists [Validator]

Validator checks existed image or not.

__Platform__: openstack

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
        <a name="Validatorimage-exists-param-name"></a>param_name<a href="#Validatorimage-exists-param-name"> [ref]</a>
      </td>
      <td>defines which variable should be used
to get image id value.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorimage-exists-nullable"></a>nullable<a href="#Validatorimage-exists-nullable"> [ref]</a>
      </td>
      <td>defines image id param is required</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### image_valid_on_flavor [Validator]

Returns validator for image could be used for current flavor.

__Platform__: openstack

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
        <a name="Validatorimage-valid-on-flavor-flavor-param"></a>flavor_param<a href="#Validatorimage-valid-on-flavor-flavor-param"> [ref]</a>
      </td>
      <td>defines which variable should be used
to get flavor id value.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorimage-valid-on-flavor-image-param"></a>image_param<a href="#Validatorimage-valid-on-flavor-image-param"> [ref]</a>
      </td>
      <td>defines which variable should be used
to get image id value.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorimage-valid-on-flavor-validate-disk"></a>validate_disk<a href="#Validatorimage-valid-on-flavor-validate-disk"> [ref]</a>
      </td>
      <td>flag to indicate whether to validate flavor's
disk. Should be True if instance is booted from
image. Should be False if instance is booted
from volume. Default value is True.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorimage-valid-on-flavor-fail-on-404-image"></a>fail_on_404_image<a href="#Validatorimage-valid-on-flavor-fail-on-404-image"> [ref]</a>
      </td>
      <td>flag what indicate whether to validate image
or not.
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_api_versions [Validator]

Validator checks component API versions.

__Platform__: openstack

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
        <a name="Validatorrequired-api-versions-component"></a>component<a href="#Validatorrequired-api-versions-component"> [ref]</a>
      </td>
      <td>name of required component
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorrequired-api-versions-versions"></a>versions<a href="#Validatorrequired-api-versions-versions"> [ref]</a>
      </td>
      <td>version of required component</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_cinder_services [Validator]

Validator checks that specified Cinder service is available.

It uses Cinder client with admin permissions to call
'cinder service-list' call

__Platform__: openstack

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
        <a name="Validatorrequired-cinder-services-services"></a>services<a href="#Validatorrequired-cinder-services-services"> [ref]</a>
      </td>
      <td>Cinder service name</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_clients [Validator]

Validator checks if specified OpenStack clients are available.

__Platform__: openstack

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
        <a name="Validatorrequired-clients-components"></a>components<a href="#Validatorrequired-clients-components"> [ref]</a>
      </td>
      <td>list of client components names
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorrequired-clients-kwargs"></a>**kwargs<a href="#Validatorrequired-clients-kwargs"> [ref]</a>
      </td>
      <td>optional parameters:
admin - bool, whether to use admin clients
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_neutron_extensions [Validator]

Validator checks if the specified Neutron extension is available.

__Platform__: openstack

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
        <a name="Validatorrequired-neutron-extensions-extensions"></a>extensions<a href="#Validatorrequired-neutron-extensions-extensions"> [ref]</a>
      </td>
      <td>list of Neutron extensions</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_services [Validator]

Validator checks if specified OpenStack services are available.

__Platform__: openstack

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
        <a name="Validatorrequired-services-services"></a>services<a href="#Validatorrequired-services-services"> [ref]</a>
      </td>
      <td>list with names of required services</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### valid_command [Validator]

Checks that parameter is a proper command-specifying dictionary.

Ensure that the command dictionary is a proper command-specifying
dictionary described in 'vmtasks.VMTasks.boot_runcommand_delete'
docstring.

__Platform__: openstack

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
        <a name="Validatorvalid-command-param-name"></a>param_name<a href="#Validatorvalid-command-param-name"> [ref]</a>
      </td>
      <td>Name of parameter to validate
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorvalid-command-required"></a>required<a href="#Validatorvalid-command-required"> [ref]</a>
      </td>
      <td>Boolean indicating that the command dictionary is
required
</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.scenarios.vm.vmtasks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/vm/vmtasks.py)

<hr />

#### validate_heat_template [Validator]

Validates heat template.

__Platform__: openstack

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
        <a name="Validatorvalidate-heat-template-params"></a>params<a href="#Validatorvalidate-heat-template-params"> [ref]</a>
      </td>
      <td>list of parameters to be validated.</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### volume_type_exists [Validator]

Returns validator for volume types.

__Platform__: openstack

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
        <a name="Validatorvolume-type-exists-param-name"></a>param_name<a href="#Validatorvolume-type-exists-param-name"> [ref]</a>
      </td>
      <td>defines variable to be used as the flag to
determine if volume types should be checked for
existence.
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorvolume-type-exists-nullable"></a>nullable<a href="#Validatorvolume-type-exists-nullable"> [ref]</a>
      </td>
      <td>defines volume_type param is required</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### workbook_contains_workflow [Validator]

Validate that workflow exist in workbook when workflow is passed.

__Platform__: openstack

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
        <a name="Validatorworkbook-contains-workflow-workbook-param"></a>workbook_param<a href="#Validatorworkbook-contains-workflow-workbook-param"> [ref]</a>
      </td>
      <td>parameter containing the workbook definition
</td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="Validatorworkbook-contains-workflow-workflow-param"></a>workflow_param<a href="#Validatorworkbook-contains-workflow-workflow-param"> [ref]</a>
      </td>
      <td>parameter containing the workflow name</td>
    </tr>
  </tbody>
</table>


__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

## Verification Component

### Verifier Manager

Verifier base class.

This class provides an interface for operating specific tool.

#### tempest [Verifier Manager]

Tempest verifier.

**Description**:

> Quote from official documentation:

> > This is a set of integration tests to be run against a live OpenStack
cluster. Tempest has batteries of tests for OpenStack API validation,
Scenarios, and other specific tests useful in validating an OpenStack
deployment.

> Rally supports features listed below:

> - *cloning Tempest*: repository and version can be specified
- *installation*: system-wide with checking existence of required
  packages or in virtual environment
- *configuration*: options are discovered via OpenStack API, but you can
  override them if you need
- *running*: pre-creating all required resources(i.e images, tenants,
  etc), prepare arguments, launching Tempest, live-progress output
- *results*: all verifications are stored in db, you can built reports,
  compare verification at whatever you want time.

> Appeared in Rally 0.8.0 *(actually, it appeared long time ago with first
revision of Verification Component, but 0.8.0 is mentioned since it is
first release after Verification Component redesign)*

**Running arguments**:

- *concurrency*: Number of processes to be used for launching tests. In case of 0 value, number of processes will be equal to number of CPU cores.
- *load_list*: a list of tests to launch.
- *pattern*: a regular expression of tests to launch.
- *set*: Name of predefined set of tests. Known names: full, smoke, baremetal, clustering, compute, database, data_processing, identity, image, messaging, network, object_storage, orchestration, telemetry, volume, scenario
- *skip_list*: a list of tests to skip (actually, it is a dict where keys are names of tests, values are reasons).
- *xfail_list*: a list of tests that are expected to fail (actually, it is a dict where keys are names of tests, values are reasons).

**Installation arguments**:

- *system_wide*: Whether or not to use the system-wide environment for verifier instead of a virtual environment. Defaults to False.
- *source*: Path or URL to the repo to clone verifier from. Defaults to <https://git.openstack.org/openstack/tempest>
- *version*: Branch, tag or commit ID to checkout before verifier installation. Defaults to 'master'.

__Platform__: openstack

__Module__: [rally_openstack.verification.tempest.manager](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/verification/tempest/manager.py)

<hr />