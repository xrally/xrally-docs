# Plugins for OpenStack

Processed releases: rally-openstack 1.0.0 - 1.1.0

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True}

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

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.contexts.magnum.ca_certs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/magnum/ca_certs.py)

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True, u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True, u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True, u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True}

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

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_ceilometer [Scenario]

Check Ceilometer Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-ceilometer-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-ceilometer-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_cinder [Scenario]

Check Cinder Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-cinder-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-cinder-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_glance [Scenario]

Check Glance Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.
In following we are checking for non-existent image.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-glance-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-glance-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_heat [Scenario]

Check Heat Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-heat-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-heat-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_monasca [Scenario]

Check Monasca Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-monasca-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-monasca-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_neutron [Scenario]

Check Neutron Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-neutron-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-neutron-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### Authenticate.validate_nova [Scenario]

Check Nova Client to ensure validation of token.

Creation of the client does not ensure validation of the token.
We have to do some minimal operation to make sure token gets validated.

__Platform__: openstack

**Parameters**:

<a name=ScenarioAuthenticatevalidate-nova-repetitions></a>

* *repetitions* [[ref]](#ScenarioAuthenticatevalidate-nova-repetitions)  
  number of times to validate

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.authenticate.authenticate](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/authenticate/authenticate.py)

<hr />

#### CeilometerAlarms.create_alarm [Scenario]

Create an alarm.

This scenarios test POST /v2/alarms.
meter_name and threshold are required parameters for alarm creation.
kwargs stores other optional parameters like 'ok_actions',
'project_id' etc that may be passed while creating an alarm.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerAlarmscreate-alarm-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-meter-name)  
  specifies meter name of the alarm
  

<a name=ScenarioCeilometerAlarmscreate-alarm-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerAlarmscreate-alarm-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-kwargs)  
  specifies optional arguments for alarm creation.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCeilometerAlarmscreate-alarm-and-get-history-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-and-get-history-meter-name)  
  specifies meter name of the alarm
  

<a name=ScenarioCeilometerAlarmscreate-alarm-and-get-history-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-and-get-history-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerAlarmscreate-alarm-and-get-history-state></a>

* *state* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-and-get-history-state)  
  an alarm state to be set
  

<a name=ScenarioCeilometerAlarmscreate-alarm-and-get-history-timeout></a>

* *timeout* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-and-get-history-timeout)  
  The number of seconds for which to attempt a
  successful check of the alarm state
  

<a name=ScenarioCeilometerAlarmscreate-alarm-and-get-history-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerAlarmscreate-alarm-and-get-history-kwargs)  
  specifies optional arguments for alarm creation.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCeilometerAlarmscreate-and-delete-alarm-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerAlarmscreate-and-delete-alarm-meter-name)  
  specifies meter name of the alarm
  

<a name=ScenarioCeilometerAlarmscreate-and-delete-alarm-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerAlarmscreate-and-delete-alarm-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerAlarmscreate-and-delete-alarm-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerAlarmscreate-and-delete-alarm-kwargs)  
  specifies optional arguments for alarm creation.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCeilometerAlarmscreate-and-get-alarm-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerAlarmscreate-and-get-alarm-meter-name)  
  specifies meter name of the alarm
  

<a name=ScenarioCeilometerAlarmscreate-and-get-alarm-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerAlarmscreate-and-get-alarm-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerAlarmscreate-and-get-alarm-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerAlarmscreate-and-get-alarm-kwargs)  
  specifies optional arguments for alarm creation.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCeilometerAlarmscreate-and-list-alarm-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerAlarmscreate-and-list-alarm-meter-name)  
  specifies meter name of the alarm
  

<a name=ScenarioCeilometerAlarmscreate-and-list-alarm-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerAlarmscreate-and-list-alarm-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerAlarmscreate-and-list-alarm-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerAlarmscreate-and-list-alarm-kwargs)  
  specifies optional arguments for alarm creation.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCeilometerAlarmscreate-and-update-alarm-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerAlarmscreate-and-update-alarm-meter-name)  
  specifies meter name of the alarm
  

<a name=ScenarioCeilometerAlarmscreate-and-update-alarm-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerAlarmscreate-and-update-alarm-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerAlarmscreate-and-update-alarm-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerAlarmscreate-and-update-alarm-kwargs)  
  specifies optional arguments for alarm creation.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerAlarms.list_alarms [Scenario]

Fetch all alarms.

This scenario fetches list of all alarms using GET /v2/alarms.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.alarms](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/alarms.py)

<hr />

#### CeilometerEvents.create_user_and_get_event [Scenario]

Create user and gets event.

This scenario creates user to store new event and
fetches one event using GET /v2/events/<message_id>.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ceilometer.events](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/events.py)

<hr />

#### CeilometerEvents.create_user_and_list_event_types [Scenario]

Create user and fetch all event types.

This scenario creates user to store new event and
fetches list of all events types using GET /v2/event_types.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ceilometer.events](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/events.py)

<hr />

#### CeilometerEvents.create_user_and_list_events [Scenario]

Create user and fetch all events.

This scenario creates user to store new event and
fetches list of all events using GET /v2/events.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ceilometer.events](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/events.py)

<hr />

#### CeilometerMeters.list_matched_meters [Scenario]

Get meters that matched fields from context and args.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerMeterslist-matched-meters-filter-by-user-id></a>

* *filter_by_user_id* [[ref]](#ScenarioCeilometerMeterslist-matched-meters-filter-by-user-id)  
  flag for query by user_id
  

<a name=ScenarioCeilometerMeterslist-matched-meters-filter-by-project-id></a>

* *filter_by_project_id* [[ref]](#ScenarioCeilometerMeterslist-matched-meters-filter-by-project-id)  
  flag for query by project_id
  

<a name=ScenarioCeilometerMeterslist-matched-meters-filter-by-resource-id></a>

* *filter_by_resource_id* [[ref]](#ScenarioCeilometerMeterslist-matched-meters-filter-by-resource-id)  
  flag for query by resource_id
  

<a name=ScenarioCeilometerMeterslist-matched-meters-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerMeterslist-matched-meters-metadata-query)  
  dict with metadata fields and values for query
  

<a name=ScenarioCeilometerMeterslist-matched-meters-limit></a>

* *limit* [[ref]](#ScenarioCeilometerMeterslist-matched-meters-limit)  
  count of resources in response

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.meters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/meters.py)

<hr />

#### CeilometerMeters.list_meters [Scenario]

Check all available queries for list resource request.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerMeterslist-meters-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerMeterslist-meters-metadata-query)  
  dict with metadata fields and values
  

<a name=ScenarioCeilometerMeterslist-meters-limit></a>

* *limit* [[ref]](#ScenarioCeilometerMeterslist-meters-limit)  
  limit of meters in response

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.meters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/meters.py)

<hr />

#### CeilometerQueries.create_and_query_alarm_history [Scenario]

Create an alarm and then query for its history.

This scenario tests POST /v2/query/alarms/history
An alarm is first created and then its alarm_id is used to fetch the
history of that specific alarm.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerQueriescreate-and-query-alarm-history-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarm-history-meter-name)  
  specifies meter name of alarm
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarm-history-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarm-history-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarm-history-orderby></a>

* *orderby* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarm-history-orderby)  
  optional param for specifying ordering of results
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarm-history-limit></a>

* *limit* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarm-history-limit)  
  optional param for maximum number of results returned
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarm-history-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarm-history-kwargs)  
  optional parameters for alarm creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.queries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/queries.py)

<hr />

#### CeilometerQueries.create_and_query_alarms [Scenario]

Create an alarm and then query it with specific parameters.

This scenario tests POST /v2/query/alarms
An alarm is first created and then fetched using the input query.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerQueriescreate-and-query-alarms-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarms-meter-name)  
  specifies meter name of alarm
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarms-threshold></a>

* *threshold* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarms-threshold)  
  specifies alarm threshold
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarms-filter></a>

* *filter* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarms-filter)  
  optional filter query dictionary
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarms-orderby></a>

* *orderby* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarms-orderby)  
  optional param for specifying ordering of results
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarms-limit></a>

* *limit* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarms-limit)  
  optional param for maximum number of results returned
  

<a name=ScenarioCeilometerQueriescreate-and-query-alarms-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerQueriescreate-and-query-alarms-kwargs)  
  optional parameters for alarm creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.queries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/queries.py)

<hr />

#### CeilometerQueries.create_and_query_samples [Scenario]

Create a sample and then query it with specific parameters.

This scenario tests POST /v2/query/samples
A sample is first created and then fetched using the input query.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerQueriescreate-and-query-samples-counter-name></a>

* *counter_name* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-counter-name)  
  specifies name of the counter
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-counter-type></a>

* *counter_type* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-counter-type)  
  specifies type of the counter
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-counter-unit></a>

* *counter_unit* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-counter-unit)  
  specifies unit of the counter
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-counter-volume></a>

* *counter_volume* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-counter-volume)  
  specifies volume of the counter
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-resource-id></a>

* *resource_id* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-resource-id)  
  specifies resource id for the sample created
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-filter></a>

* *filter* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-filter)  
  optional filter query dictionary
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-orderby></a>

* *orderby* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-orderby)  
  optional param for specifying ordering of results
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-limit></a>

* *limit* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-limit)  
  optional param for maximum number of results returned
  

<a name=ScenarioCeilometerQueriescreate-and-query-samples-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerQueriescreate-and-query-samples-kwargs)  
  parameters for sample creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.queries](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/queries.py)

<hr />

#### CeilometerResource.get_tenant_resources [Scenario]

Get all tenant resources.

This scenario retrieves information about tenant resources using
GET /v2/resources/(resource_id)

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.resources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/resources.py)

<hr />

#### CeilometerResource.list_matched_resources [Scenario]

Get resources that matched fields from context and args.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerResourcelist-matched-resources-filter-by-user-id></a>

* *filter_by_user_id* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-filter-by-user-id)  
  flag for query by user_id
  

<a name=ScenarioCeilometerResourcelist-matched-resources-filter-by-project-id></a>

* *filter_by_project_id* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-filter-by-project-id)  
  flag for query by project_id
  

<a name=ScenarioCeilometerResourcelist-matched-resources-filter-by-resource-id></a>

* *filter_by_resource_id* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-filter-by-resource-id)  
  flag for query by resource_id
  

<a name=ScenarioCeilometerResourcelist-matched-resources-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-metadata-query)  
  dict with metadata fields and values for query
  

<a name=ScenarioCeilometerResourcelist-matched-resources-start-time></a>

* *start_time* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-start-time)  
  lower bound of resource timestamp in isoformat
  

<a name=ScenarioCeilometerResourcelist-matched-resources-end-time></a>

* *end_time* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-end-time)  
  upper bound of resource timestamp in isoformat
  

<a name=ScenarioCeilometerResourcelist-matched-resources-limit></a>

* *limit* [[ref]](#ScenarioCeilometerResourcelist-matched-resources-limit)  
  count of resources in response

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.resources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/resources.py)

<hr />

#### CeilometerResource.list_resources [Scenario]

Check all available queries for list resource request.

This scenario fetches list of all resources using GET /v2/resources.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerResourcelist-resources-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerResourcelist-resources-metadata-query)  
  dict with metadata fields and values for query
  

<a name=ScenarioCeilometerResourcelist-resources-start-time></a>

* *start_time* [[ref]](#ScenarioCeilometerResourcelist-resources-start-time)  
  lower bound of resource timestamp in isoformat
  

<a name=ScenarioCeilometerResourcelist-resources-end-time></a>

* *end_time* [[ref]](#ScenarioCeilometerResourcelist-resources-end-time)  
  upper bound of resource timestamp in isoformat
  

<a name=ScenarioCeilometerResourcelist-resources-limit></a>

* *limit* [[ref]](#ScenarioCeilometerResourcelist-resources-limit)  
  count of resources in response

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.resources](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/resources.py)

<hr />

#### CeilometerSamples.list_matched_samples [Scenario]

Get list of samples that matched fields from context and args.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerSampleslist-matched-samples-filter-by-user-id></a>

* *filter_by_user_id* [[ref]](#ScenarioCeilometerSampleslist-matched-samples-filter-by-user-id)  
  flag for query by user_id
  

<a name=ScenarioCeilometerSampleslist-matched-samples-filter-by-project-id></a>

* *filter_by_project_id* [[ref]](#ScenarioCeilometerSampleslist-matched-samples-filter-by-project-id)  
  flag for query by project_id
  

<a name=ScenarioCeilometerSampleslist-matched-samples-filter-by-resource-id></a>

* *filter_by_resource_id* [[ref]](#ScenarioCeilometerSampleslist-matched-samples-filter-by-resource-id)  
  flag for query by resource_id
  

<a name=ScenarioCeilometerSampleslist-matched-samples-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerSampleslist-matched-samples-metadata-query)  
  dict with metadata fields and values for query
  

<a name=ScenarioCeilometerSampleslist-matched-samples-limit></a>

* *limit* [[ref]](#ScenarioCeilometerSampleslist-matched-samples-limit)  
  count of samples in response

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.samples](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/samples.py)

<hr />

#### CeilometerSamples.list_samples [Scenario]

Fetch all available queries for list sample request.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerSampleslist-samples-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerSampleslist-samples-metadata-query)  
  dict with metadata fields and values for query
  

<a name=ScenarioCeilometerSampleslist-samples-limit></a>

* *limit* [[ref]](#ScenarioCeilometerSampleslist-samples-limit)  
  count of samples in response

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.samples](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/samples.py)

<hr />

#### CeilometerStats.create_meter_and_get_stats [Scenario]

Create a meter and fetch its statistics.

Meter is first created and then statistics is fetched for the same
using GET /v2/meters/(meter_name)/statistics.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerStatscreate-meter-and-get-stats-kwargs></a>

* *kwargs* [[ref]](#ScenarioCeilometerStatscreate-meter-and-get-stats-kwargs)  
  contains optional arguments to create a meter

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.stats](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/stats.py)

<hr />

#### CeilometerStats.get_stats [Scenario]

Fetch statistics for certain meter.

Statistics is fetched for the using
GET /v2/meters/(meter_name)/statistics.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCeilometerStatsget-stats-meter-name></a>

* *meter_name* [[ref]](#ScenarioCeilometerStatsget-stats-meter-name)  
  meter to take statistic for
  

<a name=ScenarioCeilometerStatsget-stats-filter-by-user-id></a>

* *filter_by_user_id* [[ref]](#ScenarioCeilometerStatsget-stats-filter-by-user-id)  
  flag for query by user_id
  

<a name=ScenarioCeilometerStatsget-stats-filter-by-project-id></a>

* *filter_by_project_id* [[ref]](#ScenarioCeilometerStatsget-stats-filter-by-project-id)  
  flag for query by project_id
  

<a name=ScenarioCeilometerStatsget-stats-filter-by-resource-id></a>

* *filter_by_resource_id* [[ref]](#ScenarioCeilometerStatsget-stats-filter-by-resource-id)  
  flag for query by resource_id
  

<a name=ScenarioCeilometerStatsget-stats-metadata-query></a>

* *metadata_query* [[ref]](#ScenarioCeilometerStatsget-stats-metadata-query)  
  dict with metadata fields and values for query
  

<a name=ScenarioCeilometerStatsget-stats-period></a>

* *period* [[ref]](#ScenarioCeilometerStatsget-stats-period)  
  the length of the time range covered by these stats
  

<a name=ScenarioCeilometerStatsget-stats-groupby></a>

* *groupby* [[ref]](#ScenarioCeilometerStatsget-stats-groupby)  
  the fields used to group the samples
  

<a name=ScenarioCeilometerStatsget-stats-aggregates></a>

* *aggregates* [[ref]](#ScenarioCeilometerStatsget-stats-aggregates)  
  name of function for samples aggregation
  

__Returns__:  
list of statistics data

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ceilometer.stats](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/stats.py)

<hr />

#### CeilometerTraits.create_user_and_list_trait_descriptions [Scenario]

Create user and fetch all trait descriptions.

This scenario creates user to store new event and
fetches list of all traits for certain event type using
GET /v2/event_types/<event_type>/traits.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ceilometer.traits](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/traits.py)

<hr />

#### CeilometerTraits.create_user_and_list_traits [Scenario]

Create user and fetch all event traits.

This scenario creates user to store new event and
fetches list of all traits for certain event type and
trait name using GET /v2/event_types/<event_type>/traits/<trait_name>.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ceilometer.traits](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ceilometer/traits.py)

<hr />

#### CinderQos.create_and_get_qos [Scenario]

Create a qos, then get details of the qos.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderQoscreate-and-get-qos-consumer></a>

* *consumer* [[ref]](#ScenarioCinderQoscreate-and-get-qos-consumer)  
  Consumer behavior
  

<a name=ScenarioCinderQoscreate-and-get-qos-write-iops-sec></a>

* *write_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-get-qos-write-iops-sec)  
  random write limitation
  

<a name=ScenarioCinderQoscreate-and-get-qos-read-iops-sec></a>

* *read_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-get-qos-read-iops-sec)  
  random read limitation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderQos.create_and_list_qos [Scenario]

Create a qos, then list all qos.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderQoscreate-and-list-qos-consumer></a>

* *consumer* [[ref]](#ScenarioCinderQoscreate-and-list-qos-consumer)  
  Consumer behavior
  

<a name=ScenarioCinderQoscreate-and-list-qos-write-iops-sec></a>

* *write_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-list-qos-write-iops-sec)  
  random write limitation
  

<a name=ScenarioCinderQoscreate-and-list-qos-read-iops-sec></a>

* *read_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-list-qos-read-iops-sec)  
  random read limitation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderQos.create_and_set_qos [Scenario]

Create a qos, then Add/Update keys in qos specs.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderQoscreate-and-set-qos-consumer></a>

* *consumer* [[ref]](#ScenarioCinderQoscreate-and-set-qos-consumer)  
  Consumer behavior
  

<a name=ScenarioCinderQoscreate-and-set-qos-write-iops-sec></a>

* *write_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-set-qos-write-iops-sec)  
  random write limitation
  

<a name=ScenarioCinderQoscreate-and-set-qos-read-iops-sec></a>

* *read_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-set-qos-read-iops-sec)  
  random read limitation
  

<a name=ScenarioCinderQoscreate-and-set-qos-set-consumer></a>

* *set_consumer* [[ref]](#ScenarioCinderQoscreate-and-set-qos-set-consumer)  
  update Consumer behavior
  

<a name=ScenarioCinderQoscreate-and-set-qos-set-write-iops-sec></a>

* *set_write_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-set-qos-set-write-iops-sec)  
  update random write limitation
  

<a name=ScenarioCinderQoscreate-and-set-qos-set-read-iops-sec></a>

* *set_read_iops_sec* [[ref]](#ScenarioCinderQoscreate-and-set-qos-set-read-iops-sec)  
  update random read limitation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderQos.create_qos_associate_and_disassociate_type [Scenario]

Create a qos, Associate and Disassociate the qos from volume type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderQoscreate-qos-associate-and-disassociate-type-consumer></a>

* *consumer* [[ref]](#ScenarioCinderQoscreate-qos-associate-and-disassociate-type-consumer)  
  Consumer behavior
  

<a name=ScenarioCinderQoscreate-qos-associate-and-disassociate-type-write-iops-sec></a>

* *write_iops_sec* [[ref]](#ScenarioCinderQoscreate-qos-associate-and-disassociate-type-write-iops-sec)  
  random write limitation
  

<a name=ScenarioCinderQoscreate-qos-associate-and-disassociate-type-read-iops-sec></a>

* *read_iops_sec* [[ref]](#ScenarioCinderQoscreate-qos-associate-and-disassociate-type-read-iops-sec)  
  random read limitation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.qos_specs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/qos_specs.py)

<hr />

#### CinderVolumeBackups.create_incremental_volume_backup [Scenario]

Create a incremental volume backup.

The scenario first create a volume, the create a backup, the backup
is full backup. Because Incremental backup must be based on the
full backup. finally create a incremental backup.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeBackupscreate-incremental-volume-backup-size></a>

* *size* [[ref]](#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-size)  
  volume size in GB
  

<a name=ScenarioCinderVolumeBackupscreate-incremental-volume-backup-do-delete></a>

* *do_delete* [[ref]](#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-do-delete)  
  deletes backup and volume after creating if True
  

<a name=ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-volume-kwargs)  
  optional args to create a volume
  

<a name=ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-backup-kwargs></a>

* *create_backup_kwargs* [[ref]](#ScenarioCinderVolumeBackupscreate-incremental-volume-backup-create-backup-kwargs)  
  optional args to create a volume backup

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volume_backups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_backups.py)

<hr />

#### CinderVolumeTypes.create_and_delete_encryption_type [Scenario]

Create and delete encryption type.

This scenario firstly creates an encryption type for a given
volume type, then deletes the created encryption type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-delete-encryption-type-create-specs></a>

* *create_specs* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-create-specs)  
  the encryption type specifications to add
  

<a name=ScenarioCinderVolumeTypescreate-and-delete-encryption-type-provider></a>

* *provider* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-provider)  
  The class that provides encryption support. For
  example, LuksEncryptor.
  

<a name=ScenarioCinderVolumeTypescreate-and-delete-encryption-type-cipher></a>

* *cipher* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-cipher)  
  The encryption algorithm or mode.
  

<a name=ScenarioCinderVolumeTypescreate-and-delete-encryption-type-key-size></a>

* *key_size* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-key-size)  
  Size of encryption key, in bits.
  

<a name=ScenarioCinderVolumeTypescreate-and-delete-encryption-type-control-location></a>

* *control_location* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-encryption-type-control-location)  
  Notional service where encryption is
  performed. Valid values are "front-end"
  or "back-end."
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_delete_volume_type [Scenario]

Create and delete a volume Type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-delete-volume-type-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-volume-type-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-and-delete-volume-type-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-and-delete-volume-type-is-public)  
  Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_get_volume_type [Scenario]

Create a volume Type, then get the details of the type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-get-volume-type-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-and-get-volume-type-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-and-get-volume-type-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-and-get-volume-type-is-public)  
  Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_list_encryption_type [Scenario]

Create and list encryption type.

This scenario firstly creates a volume type, secondly creates an
encryption type for the volume type, thirdly lists all encryption
types.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-list-encryption-type-create-specs></a>

* *create_specs* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-encryption-type-create-specs)  
  The encryption type specifications to add.
  DEPRECATED, specify arguments explicitly.
  

<a name=ScenarioCinderVolumeTypescreate-and-list-encryption-type-provider></a>

* *provider* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-encryption-type-provider)  
  The class that provides encryption support. For
  example, LuksEncryptor.
  

<a name=ScenarioCinderVolumeTypescreate-and-list-encryption-type-cipher></a>

* *cipher* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-encryption-type-cipher)  
  The encryption algorithm or mode.
  

<a name=ScenarioCinderVolumeTypescreate-and-list-encryption-type-key-size></a>

* *key_size* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-encryption-type-key-size)  
  Size of encryption key, in bits.
  

<a name=ScenarioCinderVolumeTypescreate-and-list-encryption-type-control-location></a>

* *control_location* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-encryption-type-control-location)  
  Notional service where encryption is
  performed. Valid values are "front-end"
  or "back-end."
  

<a name=ScenarioCinderVolumeTypescreate-and-list-encryption-type-search-opts></a>

* *search_opts* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-encryption-type-search-opts)  
  Options used when search for encryption types

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_list_volume_types [Scenario]

Create a volume Type, then list all types.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-list-volume-types-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-volume-types-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-and-list-volume-types-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-and-list-volume-types-is-public)  
  Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_set_volume_type_keys [Scenario]

Create and set a volume type's extra specs.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-volume-type-key></a>

* *volume_type_key* [[ref]](#ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-volume-type-key)  
  A dict of key/value pairs to be set
  

<a name=ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-and-set-volume-type-keys-is-public)  
  Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_update_encryption_type [Scenario]

Create and update encryption type.

This scenario firstly creates a volume type, secondly creates an
encryption type for the volume type, thirdly updates the encryption
type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-provider></a>

* *create_provider* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-provider)  
  The class that provides encryption support. For
  example, LuksEncryptor.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-cipher></a>

* *create_cipher* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-cipher)  
  The encryption algorithm or mode.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-key-size></a>

* *create_key_size* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-key-size)  
  Size of encryption key, in bits.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-control-location></a>

* *create_control_location* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-create-control-location)  
  Notional service where encryption is
  performed. Valid values are "front-end"
  or "back-end."
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-provider></a>

* *update_provider* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-provider)  
  The class that provides encryption support. For
  example, LuksEncryptor.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-cipher></a>

* *update_cipher* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-cipher)  
  The encryption algorithm or mode.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-key-size></a>

* *update_key_size* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-key-size)  
  Size of encryption key, in bits.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-control-location></a>

* *update_control_location* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-encryption-type-update-control-location)  
  Notional service where encryption is
  performed. Valid values are "front-end"
  or "back-end."
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_and_update_volume_type [Scenario]

create a volume type, then update the type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-and-update-volume-type-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-volume-type-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-and-update-volume-type-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-volume-type-is-public)  
  Volume type visibility
  

<a name=ScenarioCinderVolumeTypescreate-and-update-volume-type-update-name></a>

* *update_name* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-volume-type-update-name)  
  if True, can update name by generating random name.
  if False, don't update name.
  

<a name=ScenarioCinderVolumeTypescreate-and-update-volume-type-update-description></a>

* *update_description* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-volume-type-update-description)  
  update Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-and-update-volume-type-update-is-public></a>

* *update_is_public* [[ref]](#ScenarioCinderVolumeTypescreate-and-update-volume-type-update-is-public)  
  update Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_get_and_delete_encryption_type [Scenario]

Create get and delete an encryption type.

This scenario firstly creates an encryption type for a volome
type created in the context, then gets detailed information of
the created encryption type, finally deletes the created
encryption type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-provider></a>

* *provider* [[ref]](#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-provider)  
  The class that provides encryption support. For
  example, LuksEncryptor.
  

<a name=ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-cipher></a>

* *cipher* [[ref]](#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-cipher)  
  The encryption algorithm or mode.
  

<a name=ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-key-size></a>

* *key_size* [[ref]](#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-key-size)  
  Size of encryption key, in bits.
  

<a name=ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-control-location></a>

* *control_location* [[ref]](#ScenarioCinderVolumeTypescreate-get-and-delete-encryption-type-control-location)  
  Notional service where encryption is
  performed. Valid values are "front-end"
  or "back-end."
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_volume_type_add_and_list_type_access [Scenario]

Add and list volume type access for the given project.

This scenario first creates a private volume type, then add project
access and list project access to it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-add-and-list-type-access-is-public)  
  Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumeTypes.create_volume_type_and_encryption_type [Scenario]

Create encryption type.

This scenario first creates a volume type, then creates an encryption
type for the volume type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-create-specs></a>

* *create_specs* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-create-specs)  
  The encryption type specifications to add.
  DEPRECATED, specify arguments explicitly.
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-provider></a>

* *provider* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-provider)  
  The class that provides encryption support. For
  example, LuksEncryptor.
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-cipher></a>

* *cipher* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-cipher)  
  The encryption algorithm or mode.
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-key-size></a>

* *key_size* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-key-size)  
  Size of encryption key, in bits.
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-control-location></a>

* *control_location* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-control-location)  
  Notional service where encryption is
  performed. Valid values are "front-end"
  or "back-end."
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-description></a>

* *description* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-description)  
  Description of the volume type
  

<a name=ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeTypescreate-volume-type-and-encryption-type-is-public)  
  Volume type visibility

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.cinder.volume_types](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volume_types.py)

<hr />

#### CinderVolumes.create_and_accept_transfer [Scenario]

Create a volume transfer, then accept it.

Measure the "cinder transfer-create" and "cinder transfer-accept"
command performace.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-accept-transfer-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-accept-transfer-size)  
  volume size (integer, in GB)
  

<a name=ScenarioCinderVolumescreate-and-accept-transfer-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-accept-transfer-image)  
  image to be used to create initial volume
  

<a name=ScenarioCinderVolumescreate-and-accept-transfer-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-accept-transfer-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_attach_volume [Scenario]

Create a VM and attach a volume to it.

Simple test to create a VM and attach a volume, then
detach the volume and delete volume/VM.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-attach-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-attach-volume-size)  
  volume size (integer, in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-and-attach-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-attach-volume-image)  
  Glance image name to use for the VM
  

<a name=ScenarioCinderVolumescreate-and-attach-volume-flavor></a>

* *flavor* [[ref]](#ScenarioCinderVolumescreate-and-attach-volume-flavor)  
  VM flavor name
  

<a name=ScenarioCinderVolumescreate-and-attach-volume-create-volume-params></a>

* *create_volume_params* [[ref]](#ScenarioCinderVolumescreate-and-attach-volume-create-volume-params)  
  optional arguments for volume creation
  

<a name=ScenarioCinderVolumescreate-and-attach-volume-create-vm-params></a>

* *create_vm_params* [[ref]](#ScenarioCinderVolumescreate-and-attach-volume-create-vm-params)  
  optional arguments for VM creation
  

<a name=ScenarioCinderVolumescreate-and-attach-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-attach-volume-kwargs)  
  (deprecated) optional arguments for VM creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_delete_snapshot [Scenario]

Create and then delete a volume-snapshot.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between snapshot creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-delete-snapshot-force></a>

* *force* [[ref]](#ScenarioCinderVolumescreate-and-delete-snapshot-force)  
  when set to True, allows snapshot of a volume when
  the volume is attached to an instance
  

<a name=ScenarioCinderVolumescreate-and-delete-snapshot-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioCinderVolumescreate-and-delete-snapshot-min-sleep)  
  minimum sleep time between snapshot creation and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-and-delete-snapshot-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioCinderVolumescreate-and-delete-snapshot-max-sleep)  
  maximum sleep time between snapshot creation and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-and-delete-snapshot-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-delete-snapshot-kwargs)  
  optional args to create a snapshot

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_delete_volume [Scenario]

Create and then delete a volume.

Good for testing a maximal bandwidth of cloud. Optional 'min_sleep'
and 'max_sleep' parameters allow the scenario to simulate a pause
between volume creation and deletion (of random duration from
[min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-delete-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-delete-volume-size)  
  volume size (integer, in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-and-delete-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-delete-volume-image)  
  image to be used to create volume
  

<a name=ScenarioCinderVolumescreate-and-delete-volume-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioCinderVolumescreate-and-delete-volume-min-sleep)  
  minimum sleep time between volume creation and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-and-delete-volume-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioCinderVolumescreate-and-delete-volume-max-sleep)  
  maximum sleep time between volume creation and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-and-delete-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-delete-volume-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_extend_volume [Scenario]

Create and extend a volume and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-extend-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-extend-volume-size)  
  volume size (in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-and-extend-volume-new-size></a>

* *new_size* [[ref]](#ScenarioCinderVolumescreate-and-extend-volume-new-size)  
  volume new size (in GB) or
  dictionary, must contain two values:
       min - minimum size volumes will be created as;
       max - maximum size volumes will be created as.
  to extend.
  Notice: should be bigger volume size
  

<a name=ScenarioCinderVolumescreate-and-extend-volume-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioCinderVolumescreate-and-extend-volume-min-sleep)  
  minimum sleep time between volume extension and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-and-extend-volume-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioCinderVolumescreate-and-extend-volume-max-sleep)  
  maximum sleep time between volume extension and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-and-extend-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-extend-volume-kwargs)  
  optional args to extend the volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_get_volume [Scenario]

Create a volume and get the volume.

Measure the "cinder show" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-get-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-get-volume-size)  
  volume size (integer, in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-and-get-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-get-volume-image)  
  image to be used to create volume
  

<a name=ScenarioCinderVolumescreate-and-get-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-get-volume-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_list_snapshots [Scenario]

Create and then list a volume-snapshot.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-list-snapshots-force></a>

* *force* [[ref]](#ScenarioCinderVolumescreate-and-list-snapshots-force)  
  when set to True, allows snapshot of a volume when
  the volume is attached to an instance
  

<a name=ScenarioCinderVolumescreate-and-list-snapshots-detailed></a>

* *detailed* [[ref]](#ScenarioCinderVolumescreate-and-list-snapshots-detailed)  
  True if detailed information about snapshots
  should be listed
  

<a name=ScenarioCinderVolumescreate-and-list-snapshots-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-list-snapshots-kwargs)  
  optional args to create a snapshot

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-list-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-size)  
  volume size (integer, in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-and-list-volume-detailed></a>

* *detailed* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-detailed)  
  determines whether the volume listing should contain
  detailed information about all of them
  

<a name=ScenarioCinderVolumescreate-and-list-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-image)  
  image to be used to create volume
  

<a name=ScenarioCinderVolumescreate-and-list-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_list_volume_backups [Scenario]

Create and then list a volume backup.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-list-volume-backups-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-backups-size)  
  volume size in GB
  

<a name=ScenarioCinderVolumescreate-and-list-volume-backups-detailed></a>

* *detailed* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-backups-detailed)  
  True if detailed information about backup
  should be listed
  

<a name=ScenarioCinderVolumescreate-and-list-volume-backups-do-delete></a>

* *do_delete* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-backups-do-delete)  
  if True, a volume backup will be deleted
  

<a name=ScenarioCinderVolumescreate-and-list-volume-backups-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-backups-create-volume-kwargs)  
  optional args to create a volume
  

<a name=ScenarioCinderVolumescreate-and-list-volume-backups-create-backup-kwargs></a>

* *create_backup_kwargs* [[ref]](#ScenarioCinderVolumescreate-and-list-volume-backups-create-backup-kwargs)  
  optional args to create a volume backup

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_restore_volume_backup [Scenario]

Restore volume backup.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-restore-volume-backup-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-restore-volume-backup-size)  
  volume size in GB
  

<a name=ScenarioCinderVolumescreate-and-restore-volume-backup-do-delete></a>

* *do_delete* [[ref]](#ScenarioCinderVolumescreate-and-restore-volume-backup-do-delete)  
  if True, the volume and the volume backup will
  be deleted after creation.
  

<a name=ScenarioCinderVolumescreate-and-restore-volume-backup-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioCinderVolumescreate-and-restore-volume-backup-create-volume-kwargs)  
  optional args to create a volume
  

<a name=ScenarioCinderVolumescreate-and-restore-volume-backup-create-backup-kwargs></a>

* *create_backup_kwargs* [[ref]](#ScenarioCinderVolumescreate-and-restore-volume-backup-create-backup-kwargs)  
  optional args to create a volume backup

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_update_volume [Scenario]

Create a volume and update its name and description.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-update-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-update-volume-size)  
  volume size (integer, in GB)
  

<a name=ScenarioCinderVolumescreate-and-update-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-update-volume-image)  
  image to be used to create volume
  

<a name=ScenarioCinderVolumescreate-and-update-volume-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioCinderVolumescreate-and-update-volume-create-volume-kwargs)  
  dict, to be used to create volume
  

<a name=ScenarioCinderVolumescreate-and-update-volume-update-volume-kwargs></a>

* *update_volume_kwargs* [[ref]](#ScenarioCinderVolumescreate-and-update-volume-update-volume-kwargs)  
  dict, to be used to update volume
  update_volume_kwargs["update_name"]=True, if updating the
  name of volume.
  update_volume_kwargs["description"]="desp", if updating the
  description of volume.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_and_upload_volume_to_image [Scenario]

Create and upload a volume to image.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-size)  
  volume size (integers, in GB), or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-image)  
  image to be used to create volume.
  

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-force></a>

* *force* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-force)  
  when set to True volume that is attached to an instance
  could be uploaded to image
  

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-container-format></a>

* *container_format* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-container-format)  
  image container format
  

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-disk-format)  
  disk format for image
  

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-do-delete></a>

* *do_delete* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-do-delete)  
  deletes image and volume after uploading if True
  

<a name=ScenarioCinderVolumescreate-and-upload-volume-to-image-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-and-upload-volume-to-image-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_from_volume_and_delete_volume [Scenario]

Create volume from volume and then delete it.

Scenario for testing volume clone.Optional 'min_sleep' and 'max_sleep'
parameters allow the scenario to simulate a pause between volume
creation and deletion (of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-from-volume-and-delete-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-from-volume-and-delete-volume-size)  
  volume size (in GB), or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  Should be equal or bigger source volume size
  

<a name=ScenarioCinderVolumescreate-from-volume-and-delete-volume-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioCinderVolumescreate-from-volume-and-delete-volume-min-sleep)  
  minimum sleep time between volume creation and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-from-volume-and-delete-volume-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioCinderVolumescreate-from-volume-and-delete-volume-max-sleep)  
  maximum sleep time between volume creation and
  deletion (in seconds)
  

<a name=ScenarioCinderVolumescreate-from-volume-and-delete-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-from-volume-and-delete-volume-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_nested_snapshots_and_attach_volume [Scenario]

Create a volume from snapshot and attach/detach the volume.

This scenario create vm, volume, create it's snapshot, attach volume,
then create new volume from existing snapshot and so on,
with defined nested level, after all detach and delete them.
volume->snapshot->volume->snapshot->volume ...

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-image)  
  Glance image name to use for the VM
  

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-flavor></a>

* *flavor* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-flavor)  
  VM flavor name
  

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-size)  
  Volume size - dictionary, contains two values:
     min - minimum size volumes will be created as;
     max - maximum size volumes will be created as.
  default values: {"min": 1, "max": 5}
  

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-nested-level></a>

* *nested_level* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-nested-level)  
  amount of nested levels
  

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-volume-kwargs)  
  optional args to create a volume
  

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-snapshot-kwargs></a>

* *create_snapshot_kwargs* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-snapshot-kwargs)  
  optional args to create a snapshot
  

<a name=ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-vm-params></a>

* *create_vm_params* [[ref]](#ScenarioCinderVolumescreate-nested-snapshots-and-attach-volume-create-vm-params)  
  optional arguments for VM creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_snapshot_and_attach_volume [Scenario]

Create vm, volume, snapshot and attach/detach volume.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-snapshot-and-attach-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-snapshot-and-attach-volume-image)  
  Glance image name to use for the VM
  

<a name=ScenarioCinderVolumescreate-snapshot-and-attach-volume-flavor></a>

* *flavor* [[ref]](#ScenarioCinderVolumescreate-snapshot-and-attach-volume-flavor)  
  VM flavor name
  

<a name=ScenarioCinderVolumescreate-snapshot-and-attach-volume-volume-type></a>

* *volume_type* [[ref]](#ScenarioCinderVolumescreate-snapshot-and-attach-volume-volume-type)  
  Name of volume type to use
  

<a name=ScenarioCinderVolumescreate-snapshot-and-attach-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-snapshot-and-attach-volume-size)  
  Volume size - dictionary, contains two values:
     min - minimum size volumes will be created as;
     max - maximum size volumes will be created as.
  default values: {"min": 1, "max": 5}
  

<a name=ScenarioCinderVolumescreate-snapshot-and-attach-volume-create-vm-params></a>

* *create_vm_params* [[ref]](#ScenarioCinderVolumescreate-snapshot-and-attach-volume-create-vm-params)  
  optional arguments for VM creation
  

<a name=ScenarioCinderVolumescreate-snapshot-and-attach-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-snapshot-and-attach-volume-kwargs)  
  Optional parameters used during volume
  snapshot creation.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume [Scenario]

Create a volume.

Good test to check how influence amount of active volumes on
performance of creating new.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-volume-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-volume-size)  
  volume size (integer, in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-volume-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-volume-image)  
  image to be used to create volume
  

<a name=ScenarioCinderVolumescreate-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioCinderVolumescreate-volume-and-clone-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-volume-and-clone-size)  
  volume size (integer, in GB) or
  dictionary, must contain two values:
      min - minimum size volumes will be created as;
      max - maximum size volumes will be created as.
  

<a name=ScenarioCinderVolumescreate-volume-and-clone-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-volume-and-clone-image)  
  image to be used to create initial volume
  

<a name=ScenarioCinderVolumescreate-volume-and-clone-nested-level></a>

* *nested_level* [[ref]](#ScenarioCinderVolumescreate-volume-and-clone-nested-level)  
  amount of nested levels
  

<a name=ScenarioCinderVolumescreate-volume-and-clone-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-and-clone-kwargs)  
  optional args to create volumes

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_and_update_readonly_flag [Scenario]

Create a volume and then update its readonly flag.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-volume-and-update-readonly-flag-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-size)  
  volume size (integer, in GB)
  

<a name=ScenarioCinderVolumescreate-volume-and-update-readonly-flag-image></a>

* *image* [[ref]](#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-image)  
  image to be used to create volume
  

<a name=ScenarioCinderVolumescreate-volume-and-update-readonly-flag-read-only></a>

* *read_only* [[ref]](#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-read-only)  
  The value to indicate whether to update volume to
  read-only access mode
  

<a name=ScenarioCinderVolumescreate-volume-and-update-readonly-flag-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-and-update-readonly-flag-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_backup [Scenario]

Create a volume backup.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-volume-backup-size></a>

* *size* [[ref]](#ScenarioCinderVolumescreate-volume-backup-size)  
  volume size in GB
  

<a name=ScenarioCinderVolumescreate-volume-backup-do-delete></a>

* *do_delete* [[ref]](#ScenarioCinderVolumescreate-volume-backup-do-delete)  
  if True, a volume and a volume backup will
  be deleted after creation.
  

<a name=ScenarioCinderVolumescreate-volume-backup-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-backup-create-volume-kwargs)  
  optional args to create a volume
  

<a name=ScenarioCinderVolumescreate-volume-backup-create-backup-kwargs></a>

* *create_backup_kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-backup-create-backup-kwargs)  
  optional args to create a volume backup

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.create_volume_from_snapshot [Scenario]

Create a volume-snapshot, then create a volume from this snapshot.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumescreate-volume-from-snapshot-do-delete></a>

* *do_delete* [[ref]](#ScenarioCinderVolumescreate-volume-from-snapshot-do-delete)  
  if True, a snapshot and a volume will
  be deleted after creation.
  

<a name=ScenarioCinderVolumescreate-volume-from-snapshot-create-snapshot-kwargs></a>

* *create_snapshot_kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-from-snapshot-create-snapshot-kwargs)  
  optional args to create a snapshot
  

<a name=ScenarioCinderVolumescreate-volume-from-snapshot-kwargs></a>

* *kwargs* [[ref]](#ScenarioCinderVolumescreate-volume-from-snapshot-kwargs)  
  optional args to create a volume

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.list_transfers [Scenario]

List all transfers.

This simple scenario tests the "cinder transfer-list" command by
listing all the volume transfers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeslist-transfers-detailed></a>

* *detailed* [[ref]](#ScenarioCinderVolumeslist-transfers-detailed)  
  If True, detailed information about volume transfer
  should be listed
  

<a name=ScenarioCinderVolumeslist-transfers-search-opts></a>

* *search_opts* [[ref]](#ScenarioCinderVolumeslist-transfers-search-opts)  
  Search options to filter out volume transfers.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.list_types [Scenario]

List all volume types.

This simple scenario tests the cinder type-list command by listing
all the volume types.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeslist-types-search-opts></a>

* *search_opts* [[ref]](#ScenarioCinderVolumeslist-types-search-opts)  
  Options used when search for volume types
  

<a name=ScenarioCinderVolumeslist-types-is-public></a>

* *is_public* [[ref]](#ScenarioCinderVolumeslist-types-is-public)  
  If query public volume type

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.list_volumes [Scenario]

List all volumes.

This simple scenario tests the cinder list command by listing
all the volumes.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumeslist-volumes-detailed></a>

* *detailed* [[ref]](#ScenarioCinderVolumeslist-volumes-detailed)  
  True if detailed information about volumes
  should be listed
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### CinderVolumes.modify_volume_metadata [Scenario]

Modify a volume's metadata.

This requires a volume to be created with the volumes
context. Additionally, `sets * set_size` must be greater
than or equal to `deletes * delete_size`.

__Platform__: openstack

**Parameters**:

<a name=ScenarioCinderVolumesmodify-volume-metadata-sets></a>

* *sets* [[ref]](#ScenarioCinderVolumesmodify-volume-metadata-sets)  
  how many set_metadata operations to perform
  

<a name=ScenarioCinderVolumesmodify-volume-metadata-set-size></a>

* *set_size* [[ref]](#ScenarioCinderVolumesmodify-volume-metadata-set-size)  
  number of metadata keys to set in each
  set_metadata operation
  

<a name=ScenarioCinderVolumesmodify-volume-metadata-deletes></a>

* *deletes* [[ref]](#ScenarioCinderVolumesmodify-volume-metadata-deletes)  
  how many delete_metadata operations to perform
  

<a name=ScenarioCinderVolumesmodify-volume-metadata-delete-size></a>

* *delete_size* [[ref]](#ScenarioCinderVolumesmodify-volume-metadata-delete-size)  
  number of metadata keys to delete in each
  delete_metadata operation
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.cinder.volumes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/cinder/volumes.py)

<hr />

#### DesignateBasic.create_and_delete_domain [Scenario]

Create and then delete a domain.

Measure the performance of creating and deleting domains
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_records [Scenario]

Create and then delete records.

Measure the performance of creating and deleting records
with different level of load.

__Platform__: openstack

**Parameters**:

<a name=ScenarioDesignateBasiccreate-and-delete-records-records-per-domain></a>

* *records_per_domain* [[ref]](#ScenarioDesignateBasiccreate-and-delete-records-records-per-domain)  
  Records to create pr domain.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_recordsets [Scenario]

Create and then delete recordsets.

Measure the performance of creating and deleting recordsets
with different level of load.

__Platform__: openstack

**Parameters**:

<a name=ScenarioDesignateBasiccreate-and-delete-recordsets-recordsets-per-zone></a>

* *recordsets_per_zone* [[ref]](#ScenarioDesignateBasiccreate-and-delete-recordsets-recordsets-per-zone)  
  recordsets to create pr zone.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_server [Scenario]

Create and then delete a server.

Measure the performance of creating and deleting servers
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_delete_zone [Scenario]

Create and then delete a zone.

Measure the performance of creating and deleting zones
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioDesignateBasiccreate-and-list-records-records-per-domain></a>

* *records_per_domain* [[ref]](#ScenarioDesignateBasiccreate-and-list-records-records-per-domain)  
  Records to create pr domain.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioDesignateBasiccreate-and-list-recordsets-recordsets-per-zone></a>

* *recordsets_per_zone* [[ref]](#ScenarioDesignateBasiccreate-and-list-recordsets-recordsets-per-zone)  
  recordsets to create pr zone.

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'admin': True}

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

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.create_and_update_domain [Scenario]

Create and then update a domain.

Measure the performance of creating and updating domains
with different level of load.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioDesignateBasiclist-records-domain-id></a>

* *domain_id* [[ref]](#ScenarioDesignateBasiclist-records-domain-id)  
  Domain ID

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_recordsets [Scenario]

List Designate recordsets.

This simple scenario tests the openstack recordset list command by
listing all the recordsets in a zone.

__Platform__: openstack

**Parameters**:

<a name=ScenarioDesignateBasiclist-recordsets-zone-id></a>

* *zone_id* [[ref]](#ScenarioDesignateBasiclist-recordsets-zone-id)  
  Zone ID

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_servers [Scenario]

List Designate servers.

This simple scenario tests the designate server-list command by listing
all the servers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### DesignateBasic.list_zones [Scenario]

List Designate zones.

This simple scenario tests the openstack zone list command by listing
all the zones.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.designate.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/designate/basic.py)

<hr />

#### Dummy.openstack [Scenario]

Do nothing and sleep for the given number of seconds (0 by default).

Dummy.dummy can be used for testing performance of different
ScenarioRunners and of the ability of rally to store a large
amount of results.

__Platform__: openstack

**Parameters**:

<a name=ScenarioDummyopenstack-sleep></a>

* *sleep* [[ref]](#ScenarioDummyopenstack-sleep)  
  idle time of method (in seconds).

__Module__: [rally_openstack.scenarios.dummy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/dummy.py)

<hr />

#### EC2Servers.boot_server [Scenario]

Boot a server.

Assumes that cleanup is done elsewhere.

__Platform__: openstack

**Parameters**:

<a name=ScenarioEC2Serversboot-server-image></a>

* *image* [[ref]](#ScenarioEC2Serversboot-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioEC2Serversboot-server-flavor></a>

* *flavor* [[ref]](#ScenarioEC2Serversboot-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioEC2Serversboot-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioEC2Serversboot-server-kwargs)  
  optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ec2.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ec2/servers.py)

<hr />

#### EC2Servers.list_servers [Scenario]

List all servers.

This simple scenario tests the EC2 API list function by listing
all the servers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.ec2.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ec2/servers.py)

<hr />

#### GlanceImages.create_and_deactivate_image [Scenario]

Create an image, then deactivate it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGlanceImagescreate-and-deactivate-image-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-and-deactivate-image-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-and-deactivate-image-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-and-deactivate-image-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-and-deactivate-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-and-deactivate-image-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-and-deactivate-image-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-and-deactivate-image-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-and-deactivate-image-min-disk></a>

* *min_disk* [[ref]](#ScenarioGlanceImagescreate-and-deactivate-image-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-and-deactivate-image-min-ram></a>

* *min_ram* [[ref]](#ScenarioGlanceImagescreate-and-deactivate-image-min-ram)  
  The min ram of created images

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_delete_image [Scenario]

Create and then delete an image.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGlanceImagescreate-and-delete-image-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-and-delete-image-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-and-delete-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-and-delete-image-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-and-delete-image-min-disk></a>

* *min_disk* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-and-delete-image-min-ram></a>

* *min_ram* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-min-ram)  
  The min ram of created images
  

<a name=ScenarioGlanceImagescreate-and-delete-image-properties></a>

* *properties* [[ref]](#ScenarioGlanceImagescreate-and-delete-image-properties)  
  A dict of image metadata properties to set
  on the image
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_download_image [Scenario]

Create an image, then download data of the image.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGlanceImagescreate-and-download-image-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-and-download-image-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-and-download-image-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-and-download-image-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-and-download-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-and-download-image-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-and-download-image-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-and-download-image-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-and-download-image-min-disk></a>

* *min_disk* [[ref]](#ScenarioGlanceImagescreate-and-download-image-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-and-download-image-min-ram></a>

* *min_ram* [[ref]](#ScenarioGlanceImagescreate-and-download-image-min-ram)  
  The min ram of created images
  

<a name=ScenarioGlanceImagescreate-and-download-image-properties></a>

* *properties* [[ref]](#ScenarioGlanceImagescreate-and-download-image-properties)  
  A dict of image metadata properties to set
  on the image
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_get_image [Scenario]

Create and get detailed information of an image.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGlanceImagescreate-and-get-image-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-and-get-image-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-and-get-image-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-and-get-image-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-and-get-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-and-get-image-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-and-get-image-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-and-get-image-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-and-get-image-min-disk></a>

* *min_disk* [[ref]](#ScenarioGlanceImagescreate-and-get-image-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-and-get-image-min-ram></a>

* *min_ram* [[ref]](#ScenarioGlanceImagescreate-and-get-image-min-ram)  
  The min ram of created images
  

<a name=ScenarioGlanceImagescreate-and-get-image-properties></a>

* *properties* [[ref]](#ScenarioGlanceImagescreate-and-get-image-properties)  
  A dict of image metadata properties to set
  on the image
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioGlanceImagescreate-and-list-image-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-and-list-image-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-and-list-image-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-and-list-image-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-and-list-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-and-list-image-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-and-list-image-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-and-list-image-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-and-list-image-min-disk></a>

* *min_disk* [[ref]](#ScenarioGlanceImagescreate-and-list-image-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-and-list-image-min-ram></a>

* *min_ram* [[ref]](#ScenarioGlanceImagescreate-and-list-image-min-ram)  
  The min ram of created images
  

<a name=ScenarioGlanceImagescreate-and-list-image-properties></a>

* *properties* [[ref]](#ScenarioGlanceImagescreate-and-list-image-properties)  
  A dict of image metadata properties to set
  on the image
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_and_update_image [Scenario]

Create an image then update it.

Measure the "glance image-create" and "glance image-update" commands
performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGlanceImagescreate-and-update-image-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-and-update-image-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-and-update-image-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-and-update-image-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-and-update-image-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-and-update-image-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-and-update-image-remove-props></a>

* *remove_props* [[ref]](#ScenarioGlanceImagescreate-and-update-image-remove-props)  
  List of property names to remove.
  (It is only supported by Glance v2.)
  

<a name=ScenarioGlanceImagescreate-and-update-image-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-and-update-image-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-and-update-image-create-min-disk></a>

* *create_min_disk* [[ref]](#ScenarioGlanceImagescreate-and-update-image-create-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-and-update-image-create-min-ram></a>

* *create_min_ram* [[ref]](#ScenarioGlanceImagescreate-and-update-image-create-min-ram)  
  The min ram of created images
  

<a name=ScenarioGlanceImagescreate-and-update-image-create-properties></a>

* *create_properties* [[ref]](#ScenarioGlanceImagescreate-and-update-image-create-properties)  
  A dict of image metadata properties to set
  on the created image
  

<a name=ScenarioGlanceImagescreate-and-update-image-update-min-disk></a>

* *update_min_disk* [[ref]](#ScenarioGlanceImagescreate-and-update-image-update-min-disk)  
  The min disk of updated images
  

<a name=ScenarioGlanceImagescreate-and-update-image-update-min-ram></a>

* *update_min_ram* [[ref]](#ScenarioGlanceImagescreate-and-update-image-update-min-ram)  
  The min ram of updated images

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### GlanceImages.create_image_and_boot_instances [Scenario]

Create an image and boot several instances from it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-container-format></a>

* *container_format* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-container-format)  
  container format of image. Acceptable
  formats: ami, ari, aki, bare, and ovf
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-image-location></a>

* *image_location* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-image-location)  
  image file location
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-disk-format></a>

* *disk_format* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-disk-format)  
  disk format of image. Acceptable formats:
  ami, ari, aki, vhd, vmdk, raw, qcow2, vdi, and iso
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-visibility></a>

* *visibility* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-visibility)  
  The access permission for the created image
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-min-disk></a>

* *min_disk* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-min-disk)  
  The min disk of created images
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-min-ram></a>

* *min_ram* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-min-ram)  
  The min ram of created images
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-properties></a>

* *properties* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-properties)  
  A dict of image metadata properties to set
  on the image
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-flavor></a>

* *flavor* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-flavor)  
  Nova flavor to be used to launch an instance
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-number-instances></a>

* *number_instances* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-number-instances)  
  number of Nova servers to boot
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-boot-server-kwargs)  
  optional parameters to boot server
  

<a name=ScenarioGlanceImagescreate-image-and-boot-instances-kwargs></a>

* *kwargs* [[ref]](#ScenarioGlanceImagescreate-image-and-boot-instances-kwargs)  
  optional parameters to create server (deprecated)

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.glance.images](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/glance/images.py)

<hr />

#### Gnocchi.get_status [Scenario]

Get the status of measurements processing.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiget-status-detailed></a>

* *detailed* [[ref]](#ScenarioGnocchiget-status-detailed)  
  get detailed output

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.status](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/status.py)

<hr />

#### Gnocchi.list_capabilities [Scenario]

List supported aggregation methods.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.capabilities](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/capabilities.py)

<hr />

#### GnocchiArchivePolicy.create_archive_policy [Scenario]

Create archive policy.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiArchivePolicycreate-archive-policy-definition></a>

* *definition* [[ref]](#ScenarioGnocchiArchivePolicycreate-archive-policy-definition)  
  List of definitions
  

<a name=ScenarioGnocchiArchivePolicycreate-archive-policy-aggregation-methods></a>

* *aggregation_methods* [[ref]](#ScenarioGnocchiArchivePolicycreate-archive-policy-aggregation-methods)  
  List of aggregation methods

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy.py)

<hr />

#### GnocchiArchivePolicy.create_delete_archive_policy [Scenario]

Create archive policy and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiArchivePolicycreate-delete-archive-policy-definition></a>

* *definition* [[ref]](#ScenarioGnocchiArchivePolicycreate-delete-archive-policy-definition)  
  List of definitions
  

<a name=ScenarioGnocchiArchivePolicycreate-delete-archive-policy-aggregation-methods></a>

* *aggregation_methods* [[ref]](#ScenarioGnocchiArchivePolicycreate-delete-archive-policy-aggregation-methods)  
  List of aggregation methods

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy.py)

<hr />

#### GnocchiArchivePolicy.list_archive_policy [Scenario]

List archive policies.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy.py)

<hr />

#### GnocchiArchivePolicyRule.create_archive_policy_rule [Scenario]

Create archive policy rule.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-metric-pattern></a>

* *metric_pattern* [[ref]](#ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-metric-pattern)  
  Pattern for matching metrics
  

<a name=ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-archive-policy-name></a>

* *archive_policy_name* [[ref]](#ScenarioGnocchiArchivePolicyRulecreate-archive-policy-rule-archive-policy-name)  
  Archive policy name

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy_rule](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy_rule.py)

<hr />

#### GnocchiArchivePolicyRule.create_delete_archive_policy_rule [Scenario]

Create archive policy rule and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-metric-pattern></a>

* *metric_pattern* [[ref]](#ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-metric-pattern)  
  Pattern for matching metrics
  

<a name=ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-archive-policy-name></a>

* *archive_policy_name* [[ref]](#ScenarioGnocchiArchivePolicyRulecreate-delete-archive-policy-rule-archive-policy-name)  
  Archive policy name

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy_rule](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy_rule.py)

<hr />

#### GnocchiArchivePolicyRule.list_archive_policy_rule [Scenario]

List archive policy rules.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.archive_policy_rule](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/archive_policy_rule.py)

<hr />

#### GnocchiMetric.create_delete_metric [Scenario]

Create metric and then delete it.

__Platform__: openstack

__Introduced in__: 1.1.0

**Parameters**:

<a name=ScenarioGnocchiMetriccreate-delete-metric-archive-policy-name></a>

* *archive_policy_name* [[ref]](#ScenarioGnocchiMetriccreate-delete-metric-archive-policy-name)  
  Archive policy name
  

<a name=ScenarioGnocchiMetriccreate-delete-metric-resource-id></a>

* *resource_id* [[ref]](#ScenarioGnocchiMetriccreate-delete-metric-resource-id)  
  The resource ID to attach the metric to
  

<a name=ScenarioGnocchiMetriccreate-delete-metric-unit></a>

* *unit* [[ref]](#ScenarioGnocchiMetriccreate-delete-metric-unit)  
  The unit of the metric

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.metric](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/metric.py)

<hr />

#### GnocchiMetric.create_metric [Scenario]

Create metric.

__Platform__: openstack

__Introduced in__: 1.1.0

**Parameters**:

<a name=ScenarioGnocchiMetriccreate-metric-archive-policy-name></a>

* *archive_policy_name* [[ref]](#ScenarioGnocchiMetriccreate-metric-archive-policy-name)  
  Archive policy name
  

<a name=ScenarioGnocchiMetriccreate-metric-resource-id></a>

* *resource_id* [[ref]](#ScenarioGnocchiMetriccreate-metric-resource-id)  
  The resource ID to attach the metric to
  

<a name=ScenarioGnocchiMetriccreate-metric-unit></a>

* *unit* [[ref]](#ScenarioGnocchiMetriccreate-metric-unit)  
  The unit of the metric

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.metric](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/metric.py)

<hr />

#### GnocchiMetric.list_metric [Scenario]

List metrics.

__Platform__: openstack

__Introduced in__: 1.1.0

**Parameters**:

<a name=ScenarioGnocchiMetriclist-metric-limit></a>

* *limit* [[ref]](#ScenarioGnocchiMetriclist-metric-limit)  
  Maximum number of metrics to list

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.metric](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/metric.py)

<hr />

#### GnocchiResource.create_delete_resource [Scenario]

Create resource and then delete it.

__Platform__: openstack

__Introduced in__: 1.1.0

**Parameters**:

<a name=ScenarioGnocchiResourcecreate-delete-resource-resource-type></a>

* *resource_type* [[ref]](#ScenarioGnocchiResourcecreate-delete-resource-resource-type)  
  Type of the resource

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.resource](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource.py)

<hr />

#### GnocchiResource.create_resource [Scenario]

Create resource.

__Platform__: openstack

__Introduced in__: 1.1.0

**Parameters**:

<a name=ScenarioGnocchiResourcecreate-resource-resource-type></a>

* *resource_type* [[ref]](#ScenarioGnocchiResourcecreate-resource-resource-type)  
  Type of the resource

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.resource](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource.py)

<hr />

#### GnocchiResourceType.create_delete_resource_type [Scenario]

Create resource type and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiResourceTypecreate-delete-resource-type-attributes></a>

* *attributes* [[ref]](#ScenarioGnocchiResourceTypecreate-delete-resource-type-attributes)  
  List of attributes

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.resource_type](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource_type.py)

<hr />

#### GnocchiResourceType.create_resource_type [Scenario]

Create resource type.

__Platform__: openstack

**Parameters**:

<a name=ScenarioGnocchiResourceTypecreate-resource-type-attributes></a>

* *attributes* [[ref]](#ScenarioGnocchiResourceTypecreate-resource-type-attributes)  
  List of attributes

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.gnocchi.resource_type](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource_type.py)

<hr />

#### GnocchiResourceType.list_resource_type [Scenario]

List resource types.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.gnocchi.resource_type](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/gnocchi/resource_type.py)

<hr />

#### HeatStacks.create_and_delete_stack [Scenario]

Create and then delete a stack.

Measure the "heat stack-create" and "heat stack-delete" commands
performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-and-delete-stack-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-and-delete-stack-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-and-delete-stack-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-and-delete-stack-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-and-delete-stack-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-and-delete-stack-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-and-delete-stack-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-and-delete-stack-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_and_list_stack [Scenario]

Create a stack and then list all stacks.

Measure the "heat stack-create" and "heat stack-list" commands
performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-and-list-stack-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-and-list-stack-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-and-list-stack-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-and-list-stack-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-and-list-stack-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-and-list-stack-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-and-list-stack-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-and-list-stack-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_check_delete_stack [Scenario]

Create, check and delete a stack.

Measure the performance of the following commands:
- heat stack-create
- heat action-check
- heat stack-delete

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-check-delete-stack-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-check-delete-stack-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-check-delete-stack-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-check-delete-stack-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-check-delete-stack-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-check-delete-stack-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-check-delete-stack-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-check-delete-stack-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioHeatStackscreate-snapshot-restore-delete-stack-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-snapshot-restore-delete-stack-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-snapshot-restore-delete-stack-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-snapshot-restore-delete-stack-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-snapshot-restore-delete-stack-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-snapshot-restore-delete-stack-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-snapshot-restore-delete-stack-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-snapshot-restore-delete-stack-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_list_output [Scenario]

Create stack and list outputs by using new algorithm.

Measure performance of the following commands:
heat stack-create
heat output-list

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-stack-and-list-output-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-stack-and-list-output-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-stack-and-list-output-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-stack-and-list-output-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_list_output_via_API [Scenario]

Create stack and list outputs by using old algorithm.

Measure performance of the following commands:
heat stack-create
heat output-list

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-stack-and-list-output-via-API-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-via-API-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-stack-and-list-output-via-API-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-via-API-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-stack-and-list-output-via-API-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-via-API-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-stack-and-list-output-via-API-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-stack-and-list-output-via-API-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_scale [Scenario]

Create an autoscaling stack and invoke a scaling policy.

Measure the performance of autoscaling webhooks.

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-stack-and-scale-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-stack-and-scale-template-path)  
  path to template file that includes an
  OS::Heat::AutoScalingGroup resource
  

<a name=ScenarioHeatStackscreate-stack-and-scale-output-key></a>

* *output_key* [[ref]](#ScenarioHeatStackscreate-stack-and-scale-output-key)  
  the stack output key that corresponds to
  the scaling webhook
  

<a name=ScenarioHeatStackscreate-stack-and-scale-delta></a>

* *delta* [[ref]](#ScenarioHeatStackscreate-stack-and-scale-delta)  
  the number of instances the stack is expected to
  change by.
  

<a name=ScenarioHeatStackscreate-stack-and-scale-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-stack-and-scale-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-stack-and-scale-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-stack-and-scale-files)  
  files used in template (dict of file name to
  file path)
  

<a name=ScenarioHeatStackscreate-stack-and-scale-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-stack-and-scale-environment)  
  stack environment definition (dict)

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_show_output [Scenario]

Create stack and show output by using new algorithm.

Measure performance of the following commands:
heat stack-create
heat output-show

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-stack-and-show-output-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-output-key></a>

* *output_key* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-output-key)  
  the stack output key that corresponds to
  the scaling webhook
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_stack_and_show_output_via_API [Scenario]

Create stack and show output by using old algorithm.

Measure performance of the following commands:
heat stack-create
heat output-show

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-stack-and-show-output-via-API-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-via-API-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-via-API-output-key></a>

* *output_key* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-via-API-output-key)  
  the stack output key that corresponds to
  the scaling webhook
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-via-API-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-via-API-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-via-API-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-via-API-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-stack-and-show-output-via-API-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-stack-and-show-output-via-API-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioHeatStackscreate-suspend-resume-delete-stack-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-suspend-resume-delete-stack-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-suspend-resume-delete-stack-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-suspend-resume-delete-stack-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-suspend-resume-delete-stack-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-suspend-resume-delete-stack-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-suspend-resume-delete-stack-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-suspend-resume-delete-stack-environment)  
  stack environment definition

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.create_update_delete_stack [Scenario]

Create, update and then delete a stack.

Measure the "heat stack-create", "heat stack-update"
and "heat stack-delete" commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioHeatStackscreate-update-delete-stack-template-path></a>

* *template_path* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-template-path)  
  path to stack template file
  

<a name=ScenarioHeatStackscreate-update-delete-stack-updated-template-path></a>

* *updated_template_path* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-updated-template-path)  
  path to updated stack template file
  

<a name=ScenarioHeatStackscreate-update-delete-stack-parameters></a>

* *parameters* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-parameters)  
  parameters to use in heat template
  

<a name=ScenarioHeatStackscreate-update-delete-stack-updated-parameters></a>

* *updated_parameters* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-updated-parameters)  
  parameters to use in updated heat template
  If not specified then parameters will be
  used instead
  

<a name=ScenarioHeatStackscreate-update-delete-stack-files></a>

* *files* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-files)  
  files used in template
  

<a name=ScenarioHeatStackscreate-update-delete-stack-updated-files></a>

* *updated_files* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-updated-files)  
  files used in updated template. If not specified
  files value will be used instead
  

<a name=ScenarioHeatStackscreate-update-delete-stack-environment></a>

* *environment* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-environment)  
  stack environment definition
  

<a name=ScenarioHeatStackscreate-update-delete-stack-updated-environment></a>

* *updated_environment* [[ref]](#ScenarioHeatStackscreate-update-delete-stack-updated-environment)  
  environment definition for updated stack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.list_stacks_and_events [Scenario]

List events from tenant stacks.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### HeatStacks.list_stacks_and_resources [Scenario]

List all resources from tenant stacks.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.heat.stacks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/heat/stacks.py)

<hr />

#### IronicNodes.create_and_delete_node [Scenario]

Create and delete node.

__Platform__: openstack

**Parameters**:

<a name=ScenarioIronicNodescreate-and-delete-node-driver></a>

* *driver* [[ref]](#ScenarioIronicNodescreate-and-delete-node-driver)  
  The name of the driver used to manage this Node.
  

<a name=ScenarioIronicNodescreate-and-delete-node-properties></a>

* *properties* [[ref]](#ScenarioIronicNodescreate-and-delete-node-properties)  
  Key/value pair describing the physical
  characteristics of the node.
  

<a name=ScenarioIronicNodescreate-and-delete-node-kwargs></a>

* *kwargs* [[ref]](#ScenarioIronicNodescreate-and-delete-node-kwargs)  
  Optional additional arguments for node creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ironic.nodes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ironic/nodes.py)

<hr />

#### IronicNodes.create_and_list_node [Scenario]

Create and list nodes.

__Platform__: openstack

**Parameters**:

<a name=ScenarioIronicNodescreate-and-list-node-driver></a>

* *driver* [[ref]](#ScenarioIronicNodescreate-and-list-node-driver)  
  The name of the driver used to manage this Node.
  

<a name=ScenarioIronicNodescreate-and-list-node-properties></a>

* *properties* [[ref]](#ScenarioIronicNodescreate-and-list-node-properties)  
  Key/value pair describing the physical
  characteristics of the node.
  

<a name=ScenarioIronicNodescreate-and-list-node-associated></a>

* *associated* [[ref]](#ScenarioIronicNodescreate-and-list-node-associated)  
  Optional argument of list request. Either a Boolean
  or a string representation of a Boolean that indicates whether to
  return a list of associated (True or "True") or unassociated
  (False or "False") nodes.
  

<a name=ScenarioIronicNodescreate-and-list-node-maintenance></a>

* *maintenance* [[ref]](#ScenarioIronicNodescreate-and-list-node-maintenance)  
  Optional argument of list request. Either a Boolean
  or a string representation of a Boolean that indicates whether
  to return nodes in maintenance mode (True or "True"), or not in
  maintenance mode (False or "False").
  

<a name=ScenarioIronicNodescreate-and-list-node-detail></a>

* *detail* [[ref]](#ScenarioIronicNodescreate-and-list-node-detail)  
  Optional, boolean whether to return detailed
  information about nodes.
  

<a name=ScenarioIronicNodescreate-and-list-node-sort-dir></a>

* *sort_dir* [[ref]](#ScenarioIronicNodescreate-and-list-node-sort-dir)  
  Optional, direction of sorting, either 'asc' (the
  default) or 'desc'.
  

<a name=ScenarioIronicNodescreate-and-list-node-marker></a>

* *marker* [[ref]](#ScenarioIronicNodescreate-and-list-node-marker)  
  DEPRECATED since Rally 0.10.0
  

<a name=ScenarioIronicNodescreate-and-list-node-limit></a>

* *limit* [[ref]](#ScenarioIronicNodescreate-and-list-node-limit)  
  DEPRECATED since Rally 0.10.0
  

<a name=ScenarioIronicNodescreate-and-list-node-sort-key></a>

* *sort_key* [[ref]](#ScenarioIronicNodescreate-and-list-node-sort-key)  
  DEPRECATED since Rally 0.10.0
  

<a name=ScenarioIronicNodescreate-and-list-node-kwargs></a>

* *kwargs* [[ref]](#ScenarioIronicNodescreate-and-list-node-kwargs)  
  Optional additional arguments for node creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.ironic.nodes](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/ironic/nodes.py)

<hr />

#### K8sPods.create_pods [Scenario]

create pods and wait for them to be ready.

__Platform__: openstack

**Parameters**:

<a name=ScenarioK8sPodscreate-pods-manifests></a>

* *manifests* [[ref]](#ScenarioK8sPodscreate-pods-manifests)  
  manifest files used to create the pods

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.magnum.k8s_pods](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/k8s_pods.py)

<hr />

#### K8sPods.create_rcs [Scenario]

create rcs and wait for them to be ready.

__Platform__: openstack

**Parameters**:

<a name=ScenarioK8sPodscreate-rcs-manifests></a>

* *manifests* [[ref]](#ScenarioK8sPodscreate-rcs-manifests)  
  manifest files use to create the rcs

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.magnum.k8s_pods](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/k8s_pods.py)

<hr />

#### K8sPods.list_pods [Scenario]

List all pods.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.magnum.k8s_pods](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/k8s_pods.py)

<hr />

#### KeystoneBasic.add_and_remove_user_role [Scenario]

Create a user role add to a user and disassociate.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.authenticate_user_and_validate_token [Scenario]

Authenticate and validate a keystone token.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_add_and_list_user_roles [Scenario]

Create user role, add it and list user roles for given user.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_delete_ec2credential [Scenario]

Create and delete keystone ec2-credential.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_delete_role [Scenario]

Create a user role and delete it.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_delete_service [Scenario]

Create and delete service.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-delete-service-service-type></a>

* *service_type* [[ref]](#ScenarioKeystoneBasiccreate-and-delete-service-service-type)  
  type of the service
  

<a name=ScenarioKeystoneBasiccreate-and-delete-service-description></a>

* *description* [[ref]](#ScenarioKeystoneBasiccreate-and-delete-service-description)  
  description of the service

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_get_role [Scenario]

Create a user role and get it detailed information.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-get-role-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-get-role-kwargs)  
  Optional additional arguments for roles creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_ec2credentials [Scenario]

Create and List all keystone ec2-credentials.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_roles [Scenario]

Create a role, then list all roles.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-list-roles-create-role-kwargs></a>

* *create_role_kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-list-roles-create-role-kwargs)  
  Optional additional arguments for
  roles create
  

<a name=ScenarioKeystoneBasiccreate-and-list-roles-list-role-kwargs></a>

* *list_role_kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-list-roles-list-role-kwargs)  
  Optional additional arguments for roles list

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_services [Scenario]

Create and list services.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-list-services-service-type></a>

* *service_type* [[ref]](#ScenarioKeystoneBasiccreate-and-list-services-service-type)  
  type of the service
  

<a name=ScenarioKeystoneBasiccreate-and-list-services-description></a>

* *description* [[ref]](#ScenarioKeystoneBasiccreate-and-list-services-description)  
  description of the service

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_tenants [Scenario]

Create a keystone tenant with random name and list all tenants.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-list-tenants-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-list-tenants-kwargs)  
  Other optional parameters

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_list_users [Scenario]

Create a keystone user with random name and list all users.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-list-users-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-list-users-kwargs)  
  Other optional parameters to create users like
  "tenant_id", "enabled".
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_and_update_user [Scenario]

Create user and update the user.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-and-update-user-create-user-kwargs></a>

* *create_user_kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-update-user-create-user-kwargs)  
  Optional additional arguments for user
  creation
  

<a name=ScenarioKeystoneBasiccreate-and-update-user-update-user-kwargs></a>

* *update_user_kwargs* [[ref]](#ScenarioKeystoneBasiccreate-and-update-user-update-user-kwargs)  
  Optional additional arguments for user
  updation
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_delete_user [Scenario]

Create a keystone user with random name and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-delete-user-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-delete-user-kwargs)  
  Other optional parameters to create users like
  "tenant_id", "enabled".
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_tenant [Scenario]

Create a keystone tenant with random name.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-tenant-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-tenant-kwargs)  
  Other optional parameters

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_tenant_with_users [Scenario]

Create a keystone tenant and several users belonging to it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-tenant-with-users-users-per-tenant></a>

* *users_per_tenant* [[ref]](#ScenarioKeystoneBasiccreate-tenant-with-users-users-per-tenant)  
  number of users to create for the tenant
  

<a name=ScenarioKeystoneBasiccreate-tenant-with-users-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-tenant-with-users-kwargs)  
  Other optional parameters for tenant creation
  

__Returns__:  
keystone tenant instance

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_update_and_delete_tenant [Scenario]

Create, update and delete tenant.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-update-and-delete-tenant-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-update-and-delete-tenant-kwargs)  
  Other optional parameters for tenant creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_user [Scenario]

Create a keystone user with random name.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-user-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-user-kwargs)  
  Other optional parameters to create users like
  "tenant_id", "enabled".
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_user_set_enabled_and_delete [Scenario]

Create a keystone user, enable or disable it, and delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-enabled></a>

* *enabled* [[ref]](#ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-enabled)  
  Initial state of user 'enabled' flag. The user
  will be created with 'enabled' set to this
  value, and then it will be toggled.
  

<a name=ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-kwargs></a>

* *kwargs* [[ref]](#ScenarioKeystoneBasiccreate-user-set-enabled-and-delete-kwargs)  
  Other optional parameters to create user.

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### KeystoneBasic.create_user_update_password [Scenario]

Create user and update password for that user.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

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

**Parameters**:

<a name=ScenarioKeystoneBasicget-entities-service-name></a>

* *service_name* [[ref]](#ScenarioKeystoneBasicget-entities-service-name)  
  The name of the service to get by ID; or
  None, to create an ephemeral service and
  get it by ID.
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.keystone.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/keystone/basic.py)

<hr />

#### MagnumClusterTemplates.list_cluster_templates [Scenario]

List all cluster_templates.

Measure the "magnum cluster_template-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMagnumClusterTemplateslist-cluster-templates-limit></a>

* *limit* [[ref]](#ScenarioMagnumClusterTemplateslist-cluster-templates-limit)  
  (Optional) The maximum number of results to return
            per request, if:
  
  1) limit > 0, the maximum number of cluster_templates to return.
  2) limit param is NOT specified (None), the number of items
     returned respect the maximum imposed by the Magnum API
     (see Magnum's api.max_limit option).
  

<a name=ScenarioMagnumClusterTemplateslist-cluster-templates-kwargs></a>

* *kwargs* [[ref]](#ScenarioMagnumClusterTemplateslist-cluster-templates-kwargs)  
  optional additional arguments for cluster_templates
  listing
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.magnum.cluster_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/cluster_templates.py)

<hr />

#### MagnumClusters.create_and_list_clusters [Scenario]

create cluster and then list all clusters.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMagnumClusterscreate-and-list-clusters-node-count></a>

* *node_count* [[ref]](#ScenarioMagnumClusterscreate-and-list-clusters-node-count)  
  the cluster node count.
  

<a name=ScenarioMagnumClusterscreate-and-list-clusters-cluster-template-uuid></a>

* *cluster_template_uuid* [[ref]](#ScenarioMagnumClusterscreate-and-list-clusters-cluster-template-uuid)  
  optional, if user want to use an existing
  cluster_template
  

<a name=ScenarioMagnumClusterscreate-and-list-clusters-kwargs></a>

* *kwargs* [[ref]](#ScenarioMagnumClusterscreate-and-list-clusters-kwargs)  
  optional additional arguments for cluster creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.magnum.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/clusters.py)

<hr />

#### MagnumClusters.list_clusters [Scenario]

List all clusters.

Measure the "magnum clusters-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMagnumClusterslist-clusters-limit></a>

* *limit* [[ref]](#ScenarioMagnumClusterslist-clusters-limit)  
  (Optional) The maximum number of results to return
            per request, if:
  
  1) limit > 0, the maximum number of clusters to return.
  2) limit param is NOT specified (None), the number of items
     returned respect the maximum imposed by the Magnum API
     (see Magnum's api.max_limit option).
  

<a name=ScenarioMagnumClusterslist-clusters-kwargs></a>

* *kwargs* [[ref]](#ScenarioMagnumClusterslist-clusters-kwargs)  
  optional additional arguments for clusters listing

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.magnum.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/magnum/clusters.py)

<hr />

#### ManilaShares.attach_security_service_to_share_network [Scenario]

Attaches security service to share network.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharesattach-security-service-to-share-network-security-service-type></a>

* *security_service_type* [[ref]](#ScenarioManilaSharesattach-security-service-to-share-network-security-service-type)  
  type of security service to use.
  Should be one of following: 'ldap', 'kerberos' or
  'active_directory'.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_delete_share [Scenario]

Create and delete a share.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between share creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-and-delete-share-share-proto></a>

* *share_proto* [[ref]](#ScenarioManilaSharescreate-and-delete-share-share-proto)  
  share protocol, valid values are NFS, CIFS,
  GlusterFS and HDFS
  

<a name=ScenarioManilaSharescreate-and-delete-share-size></a>

* *size* [[ref]](#ScenarioManilaSharescreate-and-delete-share-size)  
  share size in GB, should be greater than 0
  

<a name=ScenarioManilaSharescreate-and-delete-share-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioManilaSharescreate-and-delete-share-min-sleep)  
  minimum sleep time in seconds (non-negative)
  

<a name=ScenarioManilaSharescreate-and-delete-share-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioManilaSharescreate-and-delete-share-max-sleep)  
  maximum sleep time in seconds (non-negative)
  

<a name=ScenarioManilaSharescreate-and-delete-share-kwargs></a>

* *kwargs* [[ref]](#ScenarioManilaSharescreate-and-delete-share-kwargs)  
  optional args to create a share

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_extend_share [Scenario]

Create and extend a share.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-and-extend-share-share-proto></a>

* *share_proto* [[ref]](#ScenarioManilaSharescreate-and-extend-share-share-proto)  
  share protocol for new share
  available values are NFS, CIFS, CephFS, GlusterFS and HDFS.
  

<a name=ScenarioManilaSharescreate-and-extend-share-size></a>

* *size* [[ref]](#ScenarioManilaSharescreate-and-extend-share-size)  
  size in GiB
  

<a name=ScenarioManilaSharescreate-and-extend-share-new-size></a>

* *new_size* [[ref]](#ScenarioManilaSharescreate-and-extend-share-new-size)  
  new size of the share in GiB
  

<a name=ScenarioManilaSharescreate-and-extend-share-snapshot-id></a>

* *snapshot_id* [[ref]](#ScenarioManilaSharescreate-and-extend-share-snapshot-id)  
  ID of the snapshot
  

<a name=ScenarioManilaSharescreate-and-extend-share-description></a>

* *description* [[ref]](#ScenarioManilaSharescreate-and-extend-share-description)  
  description of a share
  

<a name=ScenarioManilaSharescreate-and-extend-share-metadata></a>

* *metadata* [[ref]](#ScenarioManilaSharescreate-and-extend-share-metadata)  
  optional metadata to set on share creation
  

<a name=ScenarioManilaSharescreate-and-extend-share-share-network></a>

* *share_network* [[ref]](#ScenarioManilaSharescreate-and-extend-share-share-network)  
  either instance of ShareNetwork or text with ID
  

<a name=ScenarioManilaSharescreate-and-extend-share-share-type></a>

* *share_type* [[ref]](#ScenarioManilaSharescreate-and-extend-share-share-type)  
  either instance of ShareType or text with ID
  

<a name=ScenarioManilaSharescreate-and-extend-share-is-public></a>

* *is_public* [[ref]](#ScenarioManilaSharescreate-and-extend-share-is-public)  
  whether to set share as public or not.
  

<a name=ScenarioManilaSharescreate-and-extend-share-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioManilaSharescreate-and-extend-share-availability-zone)  
  availability zone of the share
  

<a name=ScenarioManilaSharescreate-and-extend-share-share-group-id></a>

* *share_group_id* [[ref]](#ScenarioManilaSharescreate-and-extend-share-share-group-id)  
  ID of the share group to which the share
  should belong
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_list_share [Scenario]

Create a share and list all shares.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between share creation and list
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-and-list-share-share-proto></a>

* *share_proto* [[ref]](#ScenarioManilaSharescreate-and-list-share-share-proto)  
  share protocol, valid values are NFS, CIFS,
  GlusterFS and HDFS
  

<a name=ScenarioManilaSharescreate-and-list-share-size></a>

* *size* [[ref]](#ScenarioManilaSharescreate-and-list-share-size)  
  share size in GB, should be greater than 0
  

<a name=ScenarioManilaSharescreate-and-list-share-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioManilaSharescreate-and-list-share-min-sleep)  
  minimum sleep time in seconds (non-negative)
  

<a name=ScenarioManilaSharescreate-and-list-share-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioManilaSharescreate-and-list-share-max-sleep)  
  maximum sleep time in seconds (non-negative)
  

<a name=ScenarioManilaSharescreate-and-list-share-detailed></a>

* *detailed* [[ref]](#ScenarioManilaSharescreate-and-list-share-detailed)  
  defines whether to get detailed list of shares or not
  

<a name=ScenarioManilaSharescreate-and-list-share-kwargs></a>

* *kwargs* [[ref]](#ScenarioManilaSharescreate-and-list-share-kwargs)  
  optional args to create a share

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_and_shrink_share [Scenario]

Create and shrink a share.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-and-shrink-share-share-proto></a>

* *share_proto* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-share-proto)  
  share protocol for new share
  available values are NFS, CIFS, CephFS, GlusterFS and HDFS.
  

<a name=ScenarioManilaSharescreate-and-shrink-share-size></a>

* *size* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-size)  
  size in GiB
  

<a name=ScenarioManilaSharescreate-and-shrink-share-new-size></a>

* *new_size* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-new-size)  
  new size of the share in GiB
  

<a name=ScenarioManilaSharescreate-and-shrink-share-snapshot-id></a>

* *snapshot_id* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-snapshot-id)  
  ID of the snapshot
  

<a name=ScenarioManilaSharescreate-and-shrink-share-description></a>

* *description* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-description)  
  description of a share
  

<a name=ScenarioManilaSharescreate-and-shrink-share-metadata></a>

* *metadata* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-metadata)  
  optional metadata to set on share creation
  

<a name=ScenarioManilaSharescreate-and-shrink-share-share-network></a>

* *share_network* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-share-network)  
  either instance of ShareNetwork or text with ID
  

<a name=ScenarioManilaSharescreate-and-shrink-share-share-type></a>

* *share_type* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-share-type)  
  either instance of ShareType or text with ID
  

<a name=ScenarioManilaSharescreate-and-shrink-share-is-public></a>

* *is_public* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-is-public)  
  whether to set share as public or not.
  

<a name=ScenarioManilaSharescreate-and-shrink-share-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-availability-zone)  
  availability zone of the share
  

<a name=ScenarioManilaSharescreate-and-shrink-share-share-group-id></a>

* *share_group_id* [[ref]](#ScenarioManilaSharescreate-and-shrink-share-share-group-id)  
  ID of the share group to which the share
  should belong
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_security_service_and_delete [Scenario]

Creates security service and then deletes.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-security-service-and-delete-security-service-type></a>

* *security_service_type* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-security-service-type)  
  security service type, permitted values
  are 'ldap', 'kerberos' or 'active_directory'.
  

<a name=ScenarioManilaSharescreate-security-service-and-delete-dns-ip></a>

* *dns_ip* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-dns-ip)  
  dns ip address used inside tenant's network
  

<a name=ScenarioManilaSharescreate-security-service-and-delete-server></a>

* *server* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-server)  
  security service server ip address or hostname
  

<a name=ScenarioManilaSharescreate-security-service-and-delete-domain></a>

* *domain* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-domain)  
  security service domain
  

<a name=ScenarioManilaSharescreate-security-service-and-delete-user></a>

* *user* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-user)  
  security identifier used by tenant
  

<a name=ScenarioManilaSharescreate-security-service-and-delete-password></a>

* *password* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-password)  
  password used by user
  

<a name=ScenarioManilaSharescreate-security-service-and-delete-description></a>

* *description* [[ref]](#ScenarioManilaSharescreate-security-service-and-delete-description)  
  security service description

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_share_network_and_delete [Scenario]

Creates share network and then deletes.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-share-network-and-delete-neutron-net-id></a>

* *neutron_net_id* [[ref]](#ScenarioManilaSharescreate-share-network-and-delete-neutron-net-id)  
  ID of Neutron network
  

<a name=ScenarioManilaSharescreate-share-network-and-delete-neutron-subnet-id></a>

* *neutron_subnet_id* [[ref]](#ScenarioManilaSharescreate-share-network-and-delete-neutron-subnet-id)  
  ID of Neutron subnet
  

<a name=ScenarioManilaSharescreate-share-network-and-delete-nova-net-id></a>

* *nova_net_id* [[ref]](#ScenarioManilaSharescreate-share-network-and-delete-nova-net-id)  
  ID of Nova network
  

<a name=ScenarioManilaSharescreate-share-network-and-delete-description></a>

* *description* [[ref]](#ScenarioManilaSharescreate-share-network-and-delete-description)  
  share network description

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_share_network_and_list [Scenario]

Creates share network and then lists it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-share-network-and-list-neutron-net-id></a>

* *neutron_net_id* [[ref]](#ScenarioManilaSharescreate-share-network-and-list-neutron-net-id)  
  ID of Neutron network
  

<a name=ScenarioManilaSharescreate-share-network-and-list-neutron-subnet-id></a>

* *neutron_subnet_id* [[ref]](#ScenarioManilaSharescreate-share-network-and-list-neutron-subnet-id)  
  ID of Neutron subnet
  

<a name=ScenarioManilaSharescreate-share-network-and-list-nova-net-id></a>

* *nova_net_id* [[ref]](#ScenarioManilaSharescreate-share-network-and-list-nova-net-id)  
  ID of Nova network
  

<a name=ScenarioManilaSharescreate-share-network-and-list-description></a>

* *description* [[ref]](#ScenarioManilaSharescreate-share-network-and-list-description)  
  share network description
  

<a name=ScenarioManilaSharescreate-share-network-and-list-detailed></a>

* *detailed* [[ref]](#ScenarioManilaSharescreate-share-network-and-list-detailed)  
  defines either to return detailed list of
  objects or not.
  

<a name=ScenarioManilaSharescreate-share-network-and-list-search-opts></a>

* *search_opts* [[ref]](#ScenarioManilaSharescreate-share-network-and-list-search-opts)  
  container of search opts such as
  "name", "nova_net_id", "neutron_net_id", etc.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.create_share_then_allow_and_deny_access [Scenario]

Create a share and allow and deny access to it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-proto></a>

* *share_proto* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-proto)  
  share protocol for new share
  available values are NFS, CIFS, CephFS, GlusterFS and HDFS.
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-type></a>

* *access_type* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-type)  
  represents the access type (e.g: 'ip', 'domain'...)
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-access></a>

* *access* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-access)  
  represents the object (e.g: '127.0.0.1'...)
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-level></a>

* *access_level* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-access-level)  
  access level to the share (e.g: 'rw', 'ro')
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-size></a>

* *size* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-size)  
  size in GiB
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-new-size></a>

* *new_size* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-new-size)  
  new size of the share in GiB
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-snapshot-id></a>

* *snapshot_id* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-snapshot-id)  
  ID of the snapshot
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-description></a>

* *description* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-description)  
  description of a share
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-metadata></a>

* *metadata* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-metadata)  
  optional metadata to set on share creation
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-network></a>

* *share_network* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-network)  
  either instance of ShareNetwork or text with ID
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-type></a>

* *share_type* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-type)  
  either instance of ShareType or text with ID
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-is-public></a>

* *is_public* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-is-public)  
  whether to set share as public or not.
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-availability-zone)  
  availability zone of the share
  

<a name=ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-group-id></a>

* *share_group_id* [[ref]](#ScenarioManilaSharescreate-share-then-allow-and-deny-access-share-group-id)  
  ID of the share group to which the share
  should belong
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.list_share_servers [Scenario]

Lists share servers.

Requires admin creds.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaShareslist-share-servers-search-opts></a>

* *search_opts* [[ref]](#ScenarioManilaShareslist-share-servers-search-opts)  
  container of following search opts:
  "host", "status", "share_network" and "project_id".
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.list_shares [Scenario]

Basic scenario for 'share list' operation.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaShareslist-shares-detailed></a>

* *detailed* [[ref]](#ScenarioManilaShareslist-shares-detailed)  
  defines either to return detailed list of
  objects or not.
  

<a name=ScenarioManilaShareslist-shares-search-opts></a>

* *search_opts* [[ref]](#ScenarioManilaShareslist-shares-search-opts)  
  container of search opts such as
  "name", "host", "share_type", etc.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### ManilaShares.set_and_delete_metadata [Scenario]

Sets and deletes share metadata.

This requires a share to be created with the shares
context. Additionally, `sets * set_size` must be greater
than or equal to `deletes * delete_size`.

__Platform__: openstack

**Parameters**:

<a name=ScenarioManilaSharesset-and-delete-metadata-sets></a>

* *sets* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-sets)  
  how many set_metadata operations to perform
  

<a name=ScenarioManilaSharesset-and-delete-metadata-set-size></a>

* *set_size* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-set-size)  
  number of metadata keys to set in each
  set_metadata operation
  

<a name=ScenarioManilaSharesset-and-delete-metadata-delete-size></a>

* *delete_size* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-delete-size)  
  number of metadata keys to delete in each
  delete_metadata operation
  

<a name=ScenarioManilaSharesset-and-delete-metadata-key-min-length></a>

* *key_min_length* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-key-min-length)  
  minimal size of metadata key to set
  

<a name=ScenarioManilaSharesset-and-delete-metadata-key-max-length></a>

* *key_max_length* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-key-max-length)  
  maximum size of metadata key to set
  

<a name=ScenarioManilaSharesset-and-delete-metadata-value-min-length></a>

* *value_min_length* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-value-min-length)  
  minimal size of metadata value to set
  

<a name=ScenarioManilaSharesset-and-delete-metadata-value-max-length></a>

* *value_max_length* [[ref]](#ScenarioManilaSharesset-and-delete-metadata-value-max-length)  
  maximum size of metadata value to set

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.manila.shares](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/manila/shares.py)

<hr />

#### MistralExecutions.create_execution_from_workbook [Scenario]

Scenario tests execution creation and deletion.

This scenario is a very useful tool to measure the
"mistral execution-create" and "mistral execution-delete"
commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMistralExecutionscreate-execution-from-workbook-definition></a>

* *definition* [[ref]](#ScenarioMistralExecutionscreate-execution-from-workbook-definition)  
  string (yaml string) representation of given file
  content (Mistral workbook definition)
  

<a name=ScenarioMistralExecutionscreate-execution-from-workbook-workflow-name></a>

* *workflow_name* [[ref]](#ScenarioMistralExecutionscreate-execution-from-workbook-workflow-name)  
  string the workflow name to execute. Should be
  one of the to workflows in the definition. If no
   workflow_name is passed, one of the workflows in
   the definition will be taken.
  

<a name=ScenarioMistralExecutionscreate-execution-from-workbook-wf-input></a>

* *wf_input* [[ref]](#ScenarioMistralExecutionscreate-execution-from-workbook-wf-input)  
  file containing a json string of mistral workflow
  input
  

<a name=ScenarioMistralExecutionscreate-execution-from-workbook-params></a>

* *params* [[ref]](#ScenarioMistralExecutionscreate-execution-from-workbook-params)  
  file containing a json string of mistral params
  (the string is the place to pass the environment)
  

<a name=ScenarioMistralExecutionscreate-execution-from-workbook-do-delete></a>

* *do_delete* [[ref]](#ScenarioMistralExecutionscreate-execution-from-workbook-do-delete)  
  if False than it allows to check performance
  in "create only" mode.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.mistral.executions](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/executions.py)

<hr />

#### MistralExecutions.list_executions [Scenario]

Scenario test mistral execution-list command.

This simple scenario tests the Mistral execution-list
command by listing all the executions.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMistralExecutionslist-executions-marker></a>

* *marker* [[ref]](#ScenarioMistralExecutionslist-executions-marker)  
  The last execution uuid of the previous page, displays
  list of executions after "marker".
  

<a name=ScenarioMistralExecutionslist-executions-limit></a>

* *limit* [[ref]](#ScenarioMistralExecutionslist-executions-limit)  
  number Maximum number of executions to return in a single
  result.
  

<a name=ScenarioMistralExecutionslist-executions-sort-keys></a>

* *sort_keys* [[ref]](#ScenarioMistralExecutionslist-executions-sort-keys)  
  id,description
  

<a name=ScenarioMistralExecutionslist-executions-sort-dirs></a>

* *sort_dirs* [[ref]](#ScenarioMistralExecutionslist-executions-sort-dirs)  
  [SORT_DIRS] Comma-separated list of sort directions.
  Default: asc.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.mistral.executions](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/executions.py)

<hr />

#### MistralWorkbooks.create_workbook [Scenario]

Scenario tests workbook creation and deletion.

This scenario is a very useful tool to measure the
"mistral workbook-create" and "mistral workbook-delete"
commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMistralWorkbookscreate-workbook-definition></a>

* *definition* [[ref]](#ScenarioMistralWorkbookscreate-workbook-definition)  
  string (yaml string) representation of given
  file content (Mistral workbook definition)
  

<a name=ScenarioMistralWorkbookscreate-workbook-do-delete></a>

* *do_delete* [[ref]](#ScenarioMistralWorkbookscreate-workbook-do-delete)  
  if False than it allows to check performance
  in "create only" mode.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.mistral.workbooks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/workbooks.py)

<hr />

#### MistralWorkbooks.list_workbooks [Scenario]

Scenario test mistral workbook-list command.

This simple scenario tests the Mistral workbook-list
command by listing all the workbooks.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.mistral.workbooks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/mistral/workbooks.py)

<hr />

#### MonascaMetrics.list_metrics [Scenario]

Fetch user's metrics.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMonascaMetricslist-metrics-kwargs></a>

* *kwargs* [[ref]](#ScenarioMonascaMetricslist-metrics-kwargs)  
  optional arguments for list query:
  name, dimensions, start_time, etc
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioMuranoEnvironmentscreate-and-deploy-environment-packages-per-env></a>

* *packages_per_env* [[ref]](#ScenarioMuranoEnvironmentscreate-and-deploy-environment-packages-per-env)  
  number of packages per environment

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

**Parameters**:

<a name=ScenarioMuranoPackagesimport-and-delete-package-package></a>

* *package* [[ref]](#ScenarioMuranoPackagesimport-and-delete-package-package)  
  path to zip archive that represents Murano
  application package or absolute path to folder with
  package components
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioMuranoPackagesimport-and-filter-applications-package></a>

* *package* [[ref]](#ScenarioMuranoPackagesimport-and-filter-applications-package)  
  path to zip archive that represents Murano
  application package or absolute path to folder with
  package components
  

<a name=ScenarioMuranoPackagesimport-and-filter-applications-filter-query></a>

* *filter_query* [[ref]](#ScenarioMuranoPackagesimport-and-filter-applications-filter-query)  
  dict that contains filter criteria, lately it
  will be passed as **kwargs to filter method
  e.g. {"category": "Web"}
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.murano.packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/packages.py)

<hr />

#### MuranoPackages.import_and_list_packages [Scenario]

Import Murano package and get list of packages.

Measure the "murano import-package" and "murano package-list" commands
performance.
It imports Murano package from "package" (if it is not a zip archive
then zip archive will be prepared) and gets list of imported packages.

__Platform__: openstack

**Parameters**:

<a name=ScenarioMuranoPackagesimport-and-list-packages-package></a>

* *package* [[ref]](#ScenarioMuranoPackagesimport-and-list-packages-package)  
  path to zip archive that represents Murano
  application package or absolute path to folder with
  package components
  

<a name=ScenarioMuranoPackagesimport-and-list-packages-include-disabled></a>

* *include_disabled* [[ref]](#ScenarioMuranoPackagesimport-and-list-packages-include-disabled)  
  specifies whether the disabled packages will
  be included in a the result or not.
  Default value is False.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioMuranoPackagespackage-lifecycle-package></a>

* *package* [[ref]](#ScenarioMuranoPackagespackage-lifecycle-package)  
  path to zip archive that represents Murano
  application package or absolute path to folder with
  package components
  

<a name=ScenarioMuranoPackagespackage-lifecycle-body></a>

* *body* [[ref]](#ScenarioMuranoPackagespackage-lifecycle-body)  
  dict object that defines what package property will be
  updated, e.g {"tags": ["tag"]} or {"enabled": "true"}
  

<a name=ScenarioMuranoPackagespackage-lifecycle-operation></a>

* *operation* [[ref]](#ScenarioMuranoPackagespackage-lifecycle-operation)  
  string object that defines the way of how package
  property will be updated, allowed operations are
  "add", "replace" or "delete".
  Default value is "replace".
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.murano.packages](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/murano/packages.py)

<hr />

#### NeutronBGPVPN.create_and_delete_bgpvpns [Scenario]

Create bgpvpn and delete the bgpvpn.

Measure the "neutron bgpvpn-create" and neutron bgpvpn-delete
command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-targets)  
  Route Targets that will be both imported and
  used for export
  

<a name=ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-export-targets)  
  Additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-route-distinguishers)  
  List of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-and-delete-bgpvpns-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_list_bgpvpns [Scenario]

Create a bgpvpn and then list all bgpvpns.

Measure the "neutron bgpvpn-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-targets)  
  Route Targets that will be both imported and
  used for export
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-export-targets)  
  Additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-route-distinguishers)  
  List of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-bgpvpns-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_list_networks_associations [Scenario]

Associate a network and list networks associations.

Measure the "neutron bgpvpn-create",
"neutron bgpvpn-net-assoc-create" and
"neutron bgpvpn-net-assoc-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-targets)  
  Route Targets that will be both imported and
  used for export
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-networks-associations-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-networks-associations-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-export-targets)  
  Additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-route-distinguishers)  
  List of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-networks-associations-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-networks-associations-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_list_routers_associations [Scenario]

Associate a router and list routers associations.

Measure the "neutron bgpvpn-create",
"neutron bgpvpn-router-assoc-create" and
"neutron bgpvpn-router-assoc-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-targets)  
  Route Targets that will be both imported and
  used for export
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-routers-associations-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-routers-associations-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-export-targets)  
  Additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-route-distinguishers)  
  List of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-and-list-routers-associations-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-and-list-routers-associations-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_and_update_bgpvpns [Scenario]

Create and Update bgpvpns.

Measure the "neutron bgpvpn-update" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-update-name></a>

* *update_name* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-update-name)  
  bool, whether or not to modify BGP VPN name
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-targets)  
  Route Targets that will be both imported
  and used for export
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-targets></a>

* *updated_route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-targets)  
  Updated Route Targets that will be both
  imported and used for export
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-import-targets></a>

* *updated_import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-import-targets)  
  Updated additional Route Targets that
  will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-export-targets)  
  additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-export-targets></a>

* *updated_export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-export-targets)  
  Updated additional Route Targets that
  will be used for export.
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-route-distinguishers)  
  list of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-distinguishers></a>

* *updated_route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-updated-route-distinguishers)  
  Updated list of route
  distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-and-update-bgpvpns-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_bgpvpn_assoc_disassoc_networks [Scenario]

Associate a network and disassociate it from a BGP VPN.

Measure the "neutron bgpvpn-create", "neutron bgpvpn-net-assoc-create"
and "neutron bgpvpn-net-assoc-delete" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-targets)  
  Route Targets that will be both imported and
  used for export
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-export-targets)  
  Additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-route-distinguishers)  
  List of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-networks-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronBGPVPN.create_bgpvpn_assoc_disassoc_routers [Scenario]

Associate a router and disassociate it from a BGP VPN.

Measure the "neutron bgpvpn-create",
"neutron bgpvpn-router-assoc-create" and
"neutron bgpvpn-router-assoc-delete" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-targets></a>

* *route_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-targets)  
  Route Targets that will be both imported and
  used for export
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-import-targets></a>

* *import_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-import-targets)  
  Additional Route Targets that will be imported
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-export-targets></a>

* *export_targets* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-export-targets)  
  Additional Route Targets that will be used
  for export.
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-distinguishers></a>

* *route_distinguishers* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-route-distinguishers)  
  List of route distinguisher strings
  

<a name=ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-bgpvpn-type></a>

* *bgpvpn_type* [[ref]](#ScenarioNeutronBGPVPNcreate-bgpvpn-assoc-disassoc-routers-bgpvpn-type)  
  type of VPN and the technology behind it.
  Acceptable formats: l2 and l3
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.neutron.bgpvpn](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/bgpvpn.py)

<hr />

#### NeutronLoadbalancerV1.create_and_delete_healthmonitors [Scenario]

Create a healthmonitor(v1) and delete healthmonitors(v1).

Measure the "neutron lb-healthmonitor-create" and "neutron
lb-healthmonitor-delete" command performance. The scenario creates
healthmonitors and deletes those healthmonitors.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-delete-healthmonitors-healthmonitor-create-args></a>

* *healthmonitor_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-delete-healthmonitors-healthmonitor-create-args)  
  dict, POST /lb/healthmonitors request
  options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_delete_pools [Scenario]

Create pools(v1) and delete pools(v1).

Measure the "neutron lb-pool-create" and "neutron lb-pool-delete"
command performance. The scenario creates a pool for every subnet
and then deletes those pools.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-delete-pools-pool-create-args></a>

* *pool_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-delete-pools-pool-create-args)  
  dict, POST /lb/pools request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_delete_vips [Scenario]

Create a vip(v1) and then delete vips(v1).

Measure the "neutron lb-vip-create" and "neutron lb-vip-delete"
command performance. The scenario creates a vip for pool and
then deletes those vips.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-delete-vips-pool-create-args></a>

* *pool_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-delete-vips-pool-create-args)  
  dict, POST /lb/pools request options
  

<a name=ScenarioNeutronLoadbalancerV1create-and-delete-vips-vip-create-args></a>

* *vip_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-delete-vips-vip-create-args)  
  dict, POST /lb/vips request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_list_healthmonitors [Scenario]

Create healthmonitors(v1) and list healthmonitors(v1).

Measure the "neutron lb-healthmonitor-list" command performance. This
scenario creates healthmonitors and lists them.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-list-healthmonitors-healthmonitor-create-args></a>

* *healthmonitor_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-list-healthmonitors-healthmonitor-create-args)  
  dict, POST /lb/healthmonitors request
  options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_list_pools [Scenario]

Create a pool(v1) and then list pools(v1).

Measure the "neutron lb-pool-list" command performance.
The scenario creates a pool for every subnet and then lists pools.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-list-pools-pool-create-args></a>

* *pool_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-list-pools-pool-create-args)  
  dict, POST /lb/pools request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_list_vips [Scenario]

Create a vip(v1) and then list vips(v1).

Measure the "neutron lb-vip-create" and "neutron lb-vip-list" command
performance. The scenario creates a vip for every pool created and
then lists vips.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-list-vips-vip-create-args></a>

* *vip_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-list-vips-vip-create-args)  
  dict, POST /lb/vips request options
  

<a name=ScenarioNeutronLoadbalancerV1create-and-list-vips-pool-create-args></a>

* *pool_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-list-vips-pool-create-args)  
  dict, POST /lb/pools request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_update_healthmonitors [Scenario]

Create a healthmonitor(v1) and update healthmonitors(v1).

Measure the "neutron lb-healthmonitor-create" and "neutron
lb-healthmonitor-update" command performance. The scenario creates
healthmonitors and then updates them.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-create-args></a>

* *healthmonitor_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-create-args)  
  dict, POST /lb/healthmonitors request
  options
  

<a name=ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-update-args></a>

* *healthmonitor_update_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-healthmonitors-healthmonitor-update-args)  
  dict, POST /lb/healthmonitors update
  options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_update_pools [Scenario]

Create pools(v1) and update pools(v1).

Measure the "neutron lb-pool-create" and "neutron lb-pool-update"
command performance. The scenario creates a pool for every subnet
and then update those pools.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-create-args></a>

* *pool_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-create-args)  
  dict, POST /lb/pools request options
  

<a name=ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-update-args></a>

* *pool_update_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-pools-pool-update-args)  
  dict, POST /lb/pools update options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV1.create_and_update_vips [Scenario]

Create vips(v1) and update vips(v1).

Measure the "neutron lb-vip-create" and "neutron lb-vip-update"
command performance. The scenario creates a pool for every subnet
and then update those pools.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV1create-and-update-vips-pool-create-args></a>

* *pool_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-vips-pool-create-args)  
  dict, POST /lb/pools request options
  

<a name=ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-create-args></a>

* *vip_create_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-create-args)  
  dict, POST /lb/vips request options
  

<a name=ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-update-args></a>

* *vip_update_args* [[ref]](#ScenarioNeutronLoadbalancerV1create-and-update-vips-vip-update-args)  
  dict, POST /lb/vips update options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v1](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v1.py)

<hr />

#### NeutronLoadbalancerV2.create_and_list_loadbalancers [Scenario]

Create a loadbalancer(v2) and then list loadbalancers(v2).

Measure the "neutron lbaas-loadbalancer-list" command performance.
The scenario creates a loadbalancer for every subnet and then lists
loadbalancers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronLoadbalancerV2create-and-list-loadbalancers-lb-create-args></a>

* *lb_create_args* [[ref]](#ScenarioNeutronLoadbalancerV2create-and-list-loadbalancers-lb-create-args)  
  dict, POST /lbaas/loadbalancers
  request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.loadbalancer_v2](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/loadbalancer_v2.py)

<hr />

#### NeutronNetworks.create_and_delete_floating_ips [Scenario]

Create and delete floating IPs.

Measure the "neutron floating-ip-create" and "neutron
floating-ip-delete" commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-network></a>

* *floating_network* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-network)  
  str, external network for floating IP creation
  

<a name=ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-ip-args></a>

* *floating_ip_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-floating-ips-floating-ip-args)  
  dict, POST /floatingips request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_networks [Scenario]

Create and delete a network.

Measure the "neutron net-create" and "net-delete" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-delete-networks-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-networks-network-create-args)  
  dict, POST /v2.0/networks request options

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_ports [Scenario]

Create and delete a port.

Measure the "neutron port-create" and "neutron port-delete"
commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-delete-ports-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-ports-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-delete-ports-port-create-args></a>

* *port_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-ports-port-create-args)  
  dict, POST /v2.0/ports request options
  

<a name=ScenarioNeutronNetworkscreate-and-delete-ports-ports-per-network></a>

* *ports_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-ports-ports-per-network)  
  int, number of ports for one network

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_routers [Scenario]

Create and delete a given number of routers.

Create a network, a given number of subnets and routers
and then delete all routers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-delete-routers-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-routers-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-delete-routers-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-routers-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-delete-routers-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-routers-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-delete-routers-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-routers-subnets-per-network)  
  int, number of subnets for one network
  

<a name=ScenarioNeutronNetworkscreate-and-delete-routers-router-create-args></a>

* *router_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-routers-router-create-args)  
  dict, POST /v2.0/routers request options

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_delete_subnets [Scenario]

Create and delete a given number of subnets.

The scenario creates a network, a given number of subnets and then
deletes subnets.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-delete-subnets-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-subnets-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-subnets-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-delete-subnets-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-delete-subnets-subnets-per-network)  
  int, number of subnets for one network

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_floating_ips [Scenario]

Create and list floating IPs.

Measure the "neutron floating-ip-create" and "neutron floating-ip-list"
commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-network></a>

* *floating_network* [[ref]](#ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-network)  
  str, external network for floating IP creation
  

<a name=ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-ip-args></a>

* *floating_ip_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-floating-ips-floating-ip-args)  
  dict, POST /floatingips request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-list-networks-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-networks-network-create-args)  
  dict, POST /v2.0/networks request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_ports [Scenario]

Create and a given number of ports and list all ports.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-list-ports-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-ports-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-list-ports-port-create-args></a>

* *port_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-ports-port-create-args)  
  dict, POST /v2.0/ports request options
  

<a name=ScenarioNeutronNetworkscreate-and-list-ports-ports-per-network></a>

* *ports_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-list-ports-ports-per-network)  
  int, number of ports for one network

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_routers [Scenario]

Create and a given number of routers and list all routers.

Create a network, a given number of subnets and routers
and then list all routers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-list-routers-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-routers-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-list-routers-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-routers-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-list-routers-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-list-routers-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-list-routers-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-list-routers-subnets-per-network)  
  int, number of subnets for one network
  

<a name=ScenarioNeutronNetworkscreate-and-list-routers-router-create-args></a>

* *router_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-routers-router-create-args)  
  dict, POST /v2.0/routers request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_list_subnets [Scenario]

Create and a given number of subnets and list all subnets.

The scenario creates a network, a given number of subnets and then
lists subnets.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-list-subnets-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-subnets-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated
  

<a name=ScenarioNeutronNetworkscreate-and-list-subnets-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-list-subnets-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-list-subnets-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-list-subnets-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-list-subnets-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-list-subnets-subnets-per-network)  
  int, number of subnets for one network

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_network [Scenario]

Create a network and show network details.

Measure the "neutron net-show" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-show-network-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-network-network-create-args)  
  dict, POST /v2.0/networks request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_ports [Scenario]

Create a given number of ports and show created ports in trun.

Measure the "neutron port-create" and "neutron port-show" commands
performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-show-ports-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-ports-network-create-args)  
  dict, POST /v2.0/networks request
  options.
  

<a name=ScenarioNeutronNetworkscreate-and-show-ports-port-create-args></a>

* *port_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-ports-port-create-args)  
  dict, POST /v2.0/ports request options
  

<a name=ScenarioNeutronNetworkscreate-and-show-ports-ports-per-network></a>

* *ports_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-show-ports-ports-per-network)  
  int, number of ports for one network

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_routers [Scenario]

Create and show a given number of routers.

Create a network, a given number of subnets and routers
and then show all routers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-show-routers-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-routers-network-create-args)  
  dict, POST /v2.0/networks request
  options
  

<a name=ScenarioNeutronNetworkscreate-and-show-routers-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-routers-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-show-routers-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-show-routers-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-show-routers-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-show-routers-subnets-per-network)  
  int, number of subnets for each network
  

<a name=ScenarioNeutronNetworkscreate-and-show-routers-router-create-args></a>

* *router_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-routers-router-create-args)  
  dict, POST /v2.0/routers request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_show_subnets [Scenario]

Create and show a subnet details.

The scenario creates a network, a given number of subnets
and show the subnet details. This scenario measures the
"neutron subnet-show" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-show-subnets-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-subnets-network-create-args)  
  dict, POST /v2.0/networks request
  options.
  

<a name=ScenarioNeutronNetworkscreate-and-show-subnets-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-show-subnets-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-show-subnets-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-show-subnets-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-show-subnets-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-show-subnets-subnets-per-network)  
  int, number of subnets for one network

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_networks [Scenario]

Create and update a network.

Measure the "neutron net-create and net-update" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-update-networks-network-update-args></a>

* *network_update_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-networks-network-update-args)  
  dict, PUT /v2.0/networks update request
  

<a name=ScenarioNeutronNetworkscreate-and-update-networks-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-networks-network-create-args)  
  dict, POST /v2.0/networks request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_ports [Scenario]

Create and update a given number of ports.

Measure the "neutron port-create" and "neutron port-update" commands
performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-update-ports-port-update-args></a>

* *port_update_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-ports-port-update-args)  
  dict, PUT /v2.0/ports update request options
  

<a name=ScenarioNeutronNetworkscreate-and-update-ports-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-ports-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-update-ports-port-create-args></a>

* *port_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-ports-port-create-args)  
  dict, POST /v2.0/ports request options
  

<a name=ScenarioNeutronNetworkscreate-and-update-ports-ports-per-network></a>

* *ports_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-update-ports-ports-per-network)  
  int, number of ports for one network

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_routers [Scenario]

Create and update a given number of routers.

Create a network, a given number of subnets and routers
and then updating all routers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-update-routers-router-update-args></a>

* *router_update_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-routers-router-update-args)  
  dict, PUT /v2.0/routers update options
  

<a name=ScenarioNeutronNetworkscreate-and-update-routers-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-routers-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-update-routers-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-routers-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-update-routers-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-update-routers-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-update-routers-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-update-routers-subnets-per-network)  
  int, number of subnets for one network
  

<a name=ScenarioNeutronNetworkscreate-and-update-routers-router-create-args></a>

* *router_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-routers-router-create-args)  
  dict, POST /v2.0/routers request options

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.create_and_update_subnets [Scenario]

Create and update a subnet.

The scenario creates a network, a given number of subnets
and then updates the subnet. This scenario measures the
"neutron subnet-update" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkscreate-and-update-subnets-subnet-update-args></a>

* *subnet_update_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-subnets-subnet-update-args)  
  dict, PUT /v2.0/subnets update options
  

<a name=ScenarioNeutronNetworkscreate-and-update-subnets-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-subnets-network-create-args)  
  dict, POST /v2.0/networks request
  options. Deprecated.
  

<a name=ScenarioNeutronNetworkscreate-and-update-subnets-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNeutronNetworkscreate-and-update-subnets-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNeutronNetworkscreate-and-update-subnets-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNeutronNetworkscreate-and-update-subnets-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNeutronNetworkscreate-and-update-subnets-subnets-per-network></a>

* *subnets_per_network* [[ref]](#ScenarioNeutronNetworkscreate-and-update-subnets-subnets-per-network)  
  int, number of subnets for one network

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.list_agents [Scenario]

List all neutron agents.

This simple scenario tests the "neutron agent-list" command by
listing all the neutron agents.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworkslist-agents-agent-args></a>

* *agent_args* [[ref]](#ScenarioNeutronNetworkslist-agents-agent-args)  
  dict, POST /v2.0/agents request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronNetworks.set_and_clear_router_gateway [Scenario]

Set and Remove the external network gateway from a router.

create an external network and a router, set external network
gateway for the router, remove the external network gateway from
the router.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronNetworksset-and-clear-router-gateway-enable-snat></a>

* *enable_snat* [[ref]](#ScenarioNeutronNetworksset-and-clear-router-gateway-enable-snat)  
  True if enable snat
  

<a name=ScenarioNeutronNetworksset-and-clear-router-gateway-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNeutronNetworksset-and-clear-router-gateway-network-create-args)  
  dict, POST /v2.0/networks request
  options
  

<a name=ScenarioNeutronNetworksset-and-clear-router-gateway-router-create-args></a>

* *router_create_args* [[ref]](#ScenarioNeutronNetworksset-and-clear-router-gateway-router-create-args)  
  dict, POST /v2.0/routers request options

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NeutronSecurityGroup.create_and_delete_security_group_rule [Scenario]

Create and delete Neutron security-group-rule.

Measure the "neutron security-group-rule-create" and "neutron
security-group-rule-delete" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-args></a>

* *security_group_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-args)  
  dict, POST /v2.0/security-groups
  request options
  

<a name=ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-rule-args></a>

* *security_group_rule_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-delete-security-group-rule-security-group-rule-args)  
  dict,
  POST /v2.0/security-group-rules request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_delete_security_groups [Scenario]

Create and delete Neutron security-groups.

Measure the "neutron security-group-create" and "neutron
security-group-delete" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-delete-security-groups-security-group-create-args></a>

* *security_group_create_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-delete-security-groups-security-group-create-args)  
  dict, POST /v2.0/security-groups
  request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_list_security_group_rules [Scenario]

Create and list Neutron security-group-rules.

Measure the "neutron security-group-rule-create" and "neutron
security-group-rule-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-args></a>

* *security_group_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-args)  
  dict, POST /v2.0/security-groups
  request options
  

<a name=ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-rule-args></a>

* *security_group_rule_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-list-security-group-rules-security-group-rule-args)  
  dict,
  POST /v2.0/security-group-rules request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_list_security_groups [Scenario]

Create and list Neutron security-groups.

Measure the "neutron security-group-create" and "neutron
security-group-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-list-security-groups-security-group-create-args></a>

* *security_group_create_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-list-security-groups-security-group-create-args)  
  dict, POST /v2.0/security-groups
  request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_show_security_group [Scenario]

Create and show Neutron security-group.

Measure the "neutron security-group-create" and "neutron
security-group-show" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-show-security-group-security-group-create-args></a>

* *security_group_create_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-show-security-group-security-group-create-args)  
  dict, POST /v2.0/security-groups
  request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_show_security_group_rule [Scenario]

Create and show Neutron security-group-rule.

Measure the "neutron security-group-rule-create" and "neutron
security-group-rule-show" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-args></a>

* *security_group_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-args)  
  dict, POST /v2.0/security-groups
  request options
  

<a name=ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-rule-args></a>

* *security_group_rule_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-show-security-group-rule-security-group-rule-args)  
  dict,
  POST /v2.0/security-group-rules request options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.security_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/security_groups.py)

<hr />

#### NeutronSecurityGroup.create_and_update_security_groups [Scenario]

Create and update Neutron security-groups.

Measure the "neutron security-group-create" and "neutron
security-group-update" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-create-args></a>

* *security_group_create_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-create-args)  
  dict, POST /v2.0/security-groups
  request options
  

<a name=ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-update-args></a>

* *security_group_update_args* [[ref]](#ScenarioNeutronSecurityGroupcreate-and-update-security-groups-security-group-update-args)  
  dict, PUT /v2.0/security-groups
  update options
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.neutron.network](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/neutron/network.py)

<hr />

#### NovaAgents.list_agents [Scenario]

List all builds.

Measure the "nova agent-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAgentslist-agents-hypervisor></a>

* *hypervisor* [[ref]](#ScenarioNovaAgentslist-agents-hypervisor)  
  List agent builds on a specific hypervisor.
  None (default value) means list for all
  hypervisors
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.agents](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/agents.py)

<hr />

#### NovaAggregates.create_aggregate_add_and_remove_host [Scenario]

Create an aggregate, add a host to and remove the host from it.

Measure "nova aggregate-add-host" and "nova aggregate-remove-host"
command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAggregatescreate-aggregate-add-and-remove-host-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-and-remove-host-availability-zone)  
  The availability zone of the aggregate

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_aggregate_add_host_and_boot_server [Scenario]

Scenario to create and verify an aggregate.

This scenario creates an aggregate, adds a compute host and metadata
to the aggregate, adds the same metadata to the flavor and creates an
instance. Verifies that instance host is one of the hosts in the
aggregate.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-image></a>

* *image* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-image)  
  The image ID to boot from
  

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-metadata></a>

* *metadata* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-metadata)  
  The metadata to be set as flavor extra specs
  

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-availability-zone)  
  The availability zone of the aggregate
  

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-ram></a>

* *ram* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-disk></a>

* *disk* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioNovaAggregatescreate-aggregate-add-host-and-boot-server-boot-server-kwargs)  
  Optional additional arguments to verify host
  aggregates
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_delete_aggregate [Scenario]

Create an aggregate and then delete it.

This scenario first creates an aggregate and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAggregatescreate-and-delete-aggregate-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioNovaAggregatescreate-and-delete-aggregate-availability-zone)  
  The availability zone of the aggregate

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_get_aggregate_details [Scenario]

Create an aggregate and then get its details.

This scenario first creates an aggregate and then get details of it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAggregatescreate-and-get-aggregate-details-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioNovaAggregatescreate-and-get-aggregate-details-availability-zone)  
  The availability zone of the aggregate

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_list_aggregates [Scenario]

Create a aggregate and then list all aggregates.

This scenario creates a aggregate and then lists all aggregates.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAggregatescreate-and-list-aggregates-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioNovaAggregatescreate-and-list-aggregates-availability-zone)  
  The availability zone of the aggregate

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.create_and_update_aggregate [Scenario]

Create an aggregate and then update its name and availability_zone.

This scenario first creates an aggregate and then update its name and
availability_zone

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAggregatescreate-and-update-aggregate-availability-zone></a>

* *availability_zone* [[ref]](#ScenarioNovaAggregatescreate-and-update-aggregate-availability-zone)  
  The availability zone of the aggregate

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAggregates.list_aggregates [Scenario]

List all nova aggregates.

Measure the "nova aggregate-list" command performance.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.aggregates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/aggregates.py)

<hr />

#### NovaAvailabilityZones.list_availability_zones [Scenario]

List all availability zones.

Measure the "nova availability-zone-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaAvailabilityZoneslist-availability-zones-detailed></a>

* *detailed* [[ref]](#ScenarioNovaAvailabilityZoneslist-availability-zones-detailed)  
  True if the availability-zone listing should contain
  detailed information about all of them
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.availability_zones](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/availability_zones.py)

<hr />

#### NovaFlavors.create_and_delete_flavor [Scenario]

Create flavor and delete the flavor.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-ram></a>

* *ram* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-disk></a>

* *disk* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-flavorid></a>

* *flavorid* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-flavorid)  
  ID for the flavor (optional). You can use the reserved
  value ``"auto"`` to have Nova generate a UUID for the
  flavor in cases where you cannot simply pass ``None``.
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-ephemeral></a>

* *ephemeral* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-ephemeral)  
  Ephemeral space size in GB (default 0).
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-swap></a>

* *swap* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-swap)  
  Swap space in MB
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-rxtx-factor></a>

* *rxtx_factor* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-rxtx-factor)  
  RX/TX factor
  

<a name=ScenarioNovaFlavorscreate-and-delete-flavor-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorscreate-and-delete-flavor-is-public)  
  Make flavor accessible to the public (default true).

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_and_get_flavor [Scenario]

Create flavor and get detailed information of the flavor.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorscreate-and-get-flavor-ram></a>

* *ram* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-disk></a>

* *disk* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-flavorid></a>

* *flavorid* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-flavorid)  
  ID for the flavor (optional). You can use the reserved
  value ``"auto"`` to have Nova generate a UUID for the
  flavor in cases where you cannot simply pass ``None``.
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-ephemeral></a>

* *ephemeral* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-ephemeral)  
  Ephemeral space size in GB (default 0).
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-swap></a>

* *swap* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-swap)  
  Swap space in MB
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-rxtx-factor></a>

* *rxtx_factor* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-rxtx-factor)  
  RX/TX factor
  

<a name=ScenarioNovaFlavorscreate-and-get-flavor-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorscreate-and-get-flavor-is-public)  
  Make flavor accessible to the public (default true).

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_and_list_flavor_access [Scenario]

Create a non-public flavor and list its access rules.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-ram></a>

* *ram* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-disk></a>

* *disk* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-flavorid></a>

* *flavorid* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-flavorid)  
  ID for the flavor (optional). You can use the reserved
  value ``"auto"`` to have Nova generate a UUID for the
  flavor in cases where you cannot simply pass ``None``.
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-ephemeral></a>

* *ephemeral* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-ephemeral)  
  Ephemeral space size in GB (default 0).
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-swap></a>

* *swap* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-swap)  
  Swap space in MB
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-rxtx-factor></a>

* *rxtx_factor* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-rxtx-factor)  
  RX/TX factor
  

<a name=ScenarioNovaFlavorscreate-and-list-flavor-access-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorscreate-and-list-flavor-access-is-public)  
  Make flavor accessible to the public (default true).

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_flavor [Scenario]

Create a flavor.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorscreate-flavor-ram></a>

* *ram* [[ref]](#ScenarioNovaFlavorscreate-flavor-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaFlavorscreate-flavor-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaFlavorscreate-flavor-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaFlavorscreate-flavor-disk></a>

* *disk* [[ref]](#ScenarioNovaFlavorscreate-flavor-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaFlavorscreate-flavor-flavorid></a>

* *flavorid* [[ref]](#ScenarioNovaFlavorscreate-flavor-flavorid)  
  ID for the flavor (optional). You can use the reserved
  value ``"auto"`` to have Nova generate a UUID for the
  flavor in cases where you cannot simply pass ``None``.
  

<a name=ScenarioNovaFlavorscreate-flavor-ephemeral></a>

* *ephemeral* [[ref]](#ScenarioNovaFlavorscreate-flavor-ephemeral)  
  Ephemeral space size in GB (default 0).
  

<a name=ScenarioNovaFlavorscreate-flavor-swap></a>

* *swap* [[ref]](#ScenarioNovaFlavorscreate-flavor-swap)  
  Swap space in MB
  

<a name=ScenarioNovaFlavorscreate-flavor-rxtx-factor></a>

* *rxtx_factor* [[ref]](#ScenarioNovaFlavorscreate-flavor-rxtx-factor)  
  RX/TX factor
  

<a name=ScenarioNovaFlavorscreate-flavor-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorscreate-flavor-is-public)  
  Make flavor accessible to the public (default true).

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_flavor_and_add_tenant_access [Scenario]

Create a flavor and Add flavor access for the given tenant.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ram></a>

* *ram* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-disk></a>

* *disk* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-flavorid></a>

* *flavorid* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-flavorid)  
  ID for the flavor (optional). You can use the reserved
  value ``"auto"`` to have Nova generate a UUID for the
  flavor in cases where you cannot simply pass ``None``.
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ephemeral></a>

* *ephemeral* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-ephemeral)  
  Ephemeral space size in GB (default 0).
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-swap></a>

* *swap* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-swap)  
  Swap space in MB
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-rxtx-factor></a>

* *rxtx_factor* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-rxtx-factor)  
  RX/TX factor
  

<a name=ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-add-tenant-access-is-public)  
  Make flavor accessible to the public (default true).

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.create_flavor_and_set_keys [Scenario]

Create flavor and set keys to the flavor.

Measure the "nova flavor-key" command performance.
the scenario first create a flavor,then add the extra specs to it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-ram></a>

* *ram* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-ram)  
  Memory in MB for the flavor
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-vcpus></a>

* *vcpus* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-vcpus)  
  Number of VCPUs for the flavor
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-disk></a>

* *disk* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-disk)  
  Size of local disk in GB
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-extra-specs></a>

* *extra_specs* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-extra-specs)  
  additional arguments for flavor set keys
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-flavorid></a>

* *flavorid* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-flavorid)  
  ID for the flavor (optional). You can use the reserved
  value ``"auto"`` to have Nova generate a UUID for the
  flavor in cases where you cannot simply pass ``None``.
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-ephemeral></a>

* *ephemeral* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-ephemeral)  
  Ephemeral space size in GB (default 0).
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-swap></a>

* *swap* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-swap)  
  Swap space in MB
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-rxtx-factor></a>

* *rxtx_factor* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-rxtx-factor)  
  RX/TX factor
  

<a name=ScenarioNovaFlavorscreate-flavor-and-set-keys-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorscreate-flavor-and-set-keys-is-public)  
  Make flavor accessible to the public (default true).

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaFlavors.list_flavors [Scenario]

List all flavors.

Measure the "nova flavor-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaFlavorslist-flavors-detailed></a>

* *detailed* [[ref]](#ScenarioNovaFlavorslist-flavors-detailed)  
  Whether flavor needs to be return with details
  (optional).
  

<a name=ScenarioNovaFlavorslist-flavors-is-public></a>

* *is_public* [[ref]](#ScenarioNovaFlavorslist-flavors-is-public)  
  Filter flavors with provided access type (optional).
  None means give all flavors and only admin has query
  access to all flavor types.
  

<a name=ScenarioNovaFlavorslist-flavors-marker></a>

* *marker* [[ref]](#ScenarioNovaFlavorslist-flavors-marker)  
  Begin returning flavors that appear later in the flavor
  list than that represented by this flavor id (optional).
  

<a name=ScenarioNovaFlavorslist-flavors-min-disk></a>

* *min_disk* [[ref]](#ScenarioNovaFlavorslist-flavors-min-disk)  
  Filters the flavors by a minimum disk space, in GiB.
  

<a name=ScenarioNovaFlavorslist-flavors-min-ram></a>

* *min_ram* [[ref]](#ScenarioNovaFlavorslist-flavors-min-ram)  
  Filters the flavors by a minimum RAM, in MB.
  

<a name=ScenarioNovaFlavorslist-flavors-limit></a>

* *limit* [[ref]](#ScenarioNovaFlavorslist-flavors-limit)  
  maximum number of flavors to return (optional).
  

<a name=ScenarioNovaFlavorslist-flavors-sort-key></a>

* *sort_key* [[ref]](#ScenarioNovaFlavorslist-flavors-sort-key)  
  Flavors list sort key (optional).
  

<a name=ScenarioNovaFlavorslist-flavors-sort-dir></a>

* *sort_dir* [[ref]](#ScenarioNovaFlavorslist-flavors-sort-dir)  
  Flavors list sort direction (optional).

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.flavors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/flavors.py)

<hr />

#### NovaHypervisors.list_and_get_hypervisors [Scenario]

List and Get hypervisors.

The scenario first lists all hypervisors, then get detailed information
of the listed hypervisors in turn.

Measure the "nova hypervisor-show" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaHypervisorslist-and-get-hypervisors-detailed></a>

* *detailed* [[ref]](#ScenarioNovaHypervisorslist-and-get-hypervisors-detailed)  
  True if the hypervisor listing should contain
  detailed information about all of them
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.list_and_get_uptime_hypervisors [Scenario]

List hypervisors,then display the uptime of it.

The scenario first list all hypervisors,then display
the uptime of the listed hypervisors in turn.

Measure the "nova hypervisor-uptime" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaHypervisorslist-and-get-uptime-hypervisors-detailed></a>

* *detailed* [[ref]](#ScenarioNovaHypervisorslist-and-get-uptime-hypervisors-detailed)  
  True if the hypervisor listing should contain
  detailed information about all of them
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.list_and_search_hypervisors [Scenario]

List all servers belonging to specific hypervisor.

The scenario first list all hypervisors,then find its hostname,
then list all servers belonging to the hypervisor

Measure the "nova hypervisor-servers <hostname>" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaHypervisorslist-and-search-hypervisors-detailed></a>

* *detailed* [[ref]](#ScenarioNovaHypervisorslist-and-search-hypervisors-detailed)  
  True if the hypervisor listing should contain
  detailed information about all of them
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.list_hypervisors [Scenario]

List hypervisors.

Measure the "nova hypervisor-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaHypervisorslist-hypervisors-detailed></a>

* *detailed* [[ref]](#ScenarioNovaHypervisorslist-hypervisors-detailed)  
  True if the hypervisor listing should contain
  detailed information about all of them
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaHypervisors.statistics_hypervisors [Scenario]

Get hypervisor statistics over all compute nodes.

Measure the "nova hypervisor-stats" command performance.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.hypervisors](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/hypervisors.py)

<hr />

#### NovaImages.list_images [Scenario]

[DEPRECATED] List all images.

Measure the "nova image-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaImageslist-images-detailed></a>

* *detailed* [[ref]](#ScenarioNovaImageslist-images-detailed)  
  True if the image listing
  should contain detailed information
  

<a name=ScenarioNovaImageslist-images-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaImageslist-images-kwargs)  
  Optional additional arguments for image listing

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioNovaKeypairboot-and-delete-server-with-keypair-image></a>

* *image* [[ref]](#ScenarioNovaKeypairboot-and-delete-server-with-keypair-image)  
  ID of the image to be used for server creation
  

<a name=ScenarioNovaKeypairboot-and-delete-server-with-keypair-flavor></a>

* *flavor* [[ref]](#ScenarioNovaKeypairboot-and-delete-server-with-keypair-flavor)  
  ID of the flavor to be used for server creation
  

<a name=ScenarioNovaKeypairboot-and-delete-server-with-keypair-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioNovaKeypairboot-and-delete-server-with-keypair-boot-server-kwargs)  
  Optional additional arguments for VM
  creation
  

<a name=ScenarioNovaKeypairboot-and-delete-server-with-keypair-server-kwargs></a>

* *server_kwargs* [[ref]](#ScenarioNovaKeypairboot-and-delete-server-with-keypair-server-kwargs)  
  Deprecated alias for boot_server_kwargs
  

<a name=ScenarioNovaKeypairboot-and-delete-server-with-keypair-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaKeypairboot-and-delete-server-with-keypair-kwargs)  
  Optional additional arguments for keypair creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaKeypair.create_and_delete_keypair [Scenario]

Create a keypair with random name and delete keypair.

This scenario creates a keypair and then delete that keypair.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaKeypaircreate-and-delete-keypair-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaKeypaircreate-and-delete-keypair-kwargs)  
  Optional additional arguments for keypair creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaKeypair.create_and_get_keypair [Scenario]

Create a keypair and get the keypair details.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaKeypaircreate-and-get-keypair-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaKeypaircreate-and-get-keypair-kwargs)  
  Optional additional arguments for keypair creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaKeypair.create_and_list_keypairs [Scenario]

Create a keypair with random name and list keypairs.

This scenario creates a keypair and then lists all keypairs.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaKeypaircreate-and-list-keypairs-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaKeypaircreate-and-list-keypairs-kwargs)  
  Optional additional arguments for keypair creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.keypairs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/keypairs.py)

<hr />

#### NovaServerGroups.create_and_delete_server_group [Scenario]

Create a server group, then delete it.

Measure the "nova server-group-create" and "nova server-group-delete"
command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerGroupscreate-and-delete-server-group-policies></a>

* *policies* [[ref]](#ScenarioNovaServerGroupscreate-and-delete-server-group-policies)  
  Server group policy
  

<a name=ScenarioNovaServerGroupscreate-and-delete-server-group-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServerGroupscreate-and-delete-server-group-kwargs)  
  The server group specifications to add.
  DEPRECATED, specify arguments explicitly.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.server_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/server_groups.py)

<hr />

#### NovaServerGroups.create_and_get_server_group [Scenario]

Create a server group, then get its detailed information.

Measure the "nova server-group-create" and "nova server-group-get"
command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerGroupscreate-and-get-server-group-policies></a>

* *policies* [[ref]](#ScenarioNovaServerGroupscreate-and-get-server-group-policies)  
  Server group policy
  

<a name=ScenarioNovaServerGroupscreate-and-get-server-group-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServerGroupscreate-and-get-server-group-kwargs)  
  The server group specifications to add.
  DEPRECATED, specify arguments explicitly.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.server_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/server_groups.py)

<hr />

#### NovaServerGroups.create_and_list_server_groups [Scenario]

Create a server group, then list all server groups.

Measure the "nova server-group-create" and "nova server-group-list"
command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerGroupscreate-and-list-server-groups-policies></a>

* *policies* [[ref]](#ScenarioNovaServerGroupscreate-and-list-server-groups-policies)  
  Server group policy
  

<a name=ScenarioNovaServerGroupscreate-and-list-server-groups-all-projects></a>

* *all_projects* [[ref]](#ScenarioNovaServerGroupscreate-and-list-server-groups-all-projects)  
  If True, display server groups from all
  projects(Admin only)
  

<a name=ScenarioNovaServerGroupscreate-and-list-server-groups-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServerGroupscreate-and-list-server-groups-kwargs)  
  The server group specifications to add.
  DEPRECATED, specify arguments explicitly.
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.server_groups](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/server_groups.py)

<hr />

#### NovaServers.boot_and_associate_floating_ip [Scenario]

Boot a server and associate a floating IP to it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-associate-floating-ip-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-associate-floating-ip-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-associate-floating-ip-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-associate-floating-ip-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-associate-floating-ip-create-floating-ip-args></a>

* *create_floating_ip_args* [[ref]](#ScenarioNovaServersboot-and-associate-floating-ip-create-floating-ip-args)  
  Optional additional arguments for
  floating ip creation
  

<a name=ScenarioNovaServersboot-and-associate-floating-ip-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-associate-floating-ip-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_bounce_server [Scenario]

Boot a server and run specified actions against it.

Actions should be passed into the actions parameter. Available actions
are 'hard_reboot', 'soft_reboot', 'stop_start', 'rescue_unrescue',
'pause_unpause', 'suspend_resume', 'lock_unlock' and 'shelve_unshelve'.
Delete server after all actions were completed.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-bounce-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-bounce-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-bounce-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-bounce-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-bounce-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-and-bounce-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-and-bounce-server-actions></a>

* *actions* [[ref]](#ScenarioNovaServersboot-and-bounce-server-actions)  
  list of action dictionaries, where each action
  dictionary speicifes an action to be performed
  in the following format:
  {"action_name": <no_of_iterations>}
  

<a name=ScenarioNovaServersboot-and-bounce-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-bounce-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_delete_multiple_servers [Scenario]

Boot multiple servers in a single request and delete them.

Deletion is done in parallel with one request per server, not
with a single request for all servers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-image)  
  The image to boot from
  

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-flavor)  
  Flavor used to boot instance
  

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-count></a>

* *count* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-count)  
  Number of instances to boot
  

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-and-delete-multiple-servers-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-delete-multiple-servers-kwargs)  
  Optional additional arguments for instance creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_delete_server [Scenario]

Boot and delete a server.

Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between volume creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-delete-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-delete-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-delete-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-delete-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-delete-server-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-and-delete-server-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-and-delete-server-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-and-delete-server-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-and-delete-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-and-delete-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-and-delete-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-delete-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_get_console_output [Scenario]

Get text console output from server.

This simple scenario tests the nova console-log command by retrieving
the text console log output.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-get-console-output-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-get-console-output-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-get-console-output-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-get-console-output-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-get-console-output-length></a>

* *length* [[ref]](#ScenarioNovaServersboot-and-get-console-output-length)  
  The number of tail log lines you would like to retrieve.
  None (default value) or -1 means unlimited length.
  

<a name=ScenarioNovaServersboot-and-get-console-output-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-get-console-output-kwargs)  
  Optional additional arguments for server creation
  

__Returns__:  
Text console log output for server

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_get_console_url [Scenario]

Retrieve a console url of a server.

This simple scenario tests retrieving the console url of a server.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-get-console-url-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-get-console-url-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-get-console-url-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-get-console-url-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-get-console-url-console-type></a>

* *console_type* [[ref]](#ScenarioNovaServersboot-and-get-console-url-console-type)  
  type can be novnc/xvpvnc for protocol vnc;
  spice-html5 for protocol spice; rdp-html5 for
  protocol rdp; serial for protocol serial.
  webmks for protocol mks (since version 2.8).
  

<a name=ScenarioNovaServersboot-and-get-console-url-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-get-console-url-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioNovaServersboot-and-list-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-list-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-list-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-list-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-list-server-detailed></a>

* *detailed* [[ref]](#ScenarioNovaServersboot-and-list-server-detailed)  
  True if the server listing should contain
  detailed information about all of them
  

<a name=ScenarioNovaServersboot-and-list-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-list-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioNovaServersboot-and-live-migrate-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-live-migrate-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-live-migrate-server-block-migration></a>

* *block_migration* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-block-migration)  
  Specifies the migration type
  

<a name=ScenarioNovaServersboot-and-live-migrate-server-disk-over-commit></a>

* *disk_over_commit* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-disk-over-commit)  
  Specifies whether to allow overcommit
  on migrated instance or not
  

<a name=ScenarioNovaServersboot-and-live-migrate-server-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-and-live-migrate-server-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-and-live-migrate-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-live-migrate-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_migrate_server [Scenario]

Migrate a server.

This scenario launches a VM on a compute node available in
the availability zone, and then migrates the VM
to another compute node on the same availability zone.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-migrate-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-migrate-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-migrate-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-migrate-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-migrate-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-migrate-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_rebuild_server [Scenario]

Rebuild a server.

This scenario launches a VM, then rebuilds that VM with a
different image.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-rebuild-server-from-image></a>

* *from_image* [[ref]](#ScenarioNovaServersboot-and-rebuild-server-from-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-rebuild-server-to-image></a>

* *to_image* [[ref]](#ScenarioNovaServersboot-and-rebuild-server-to-image)  
  image to be used to rebuild the instance
  

<a name=ScenarioNovaServersboot-and-rebuild-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-rebuild-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-rebuild-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-rebuild-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_show_server [Scenario]

Show server details.

This simple scenario tests the nova show command by retrieving
the server details.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-show-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-show-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-show-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-show-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-show-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-show-server-kwargs)  
  Optional additional arguments for server creation
  

__Returns__:  
Server details

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_and_update_server [Scenario]

Boot a server, then update its name and description.

The scenario first creates a server, then update it.
Assumes that cleanup is done elsewhere.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-and-update-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-and-update-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-update-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-and-update-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-and-update-server-description></a>

* *description* [[ref]](#ScenarioNovaServersboot-and-update-server-description)  
  update the server description
  

<a name=ScenarioNovaServersboot-and-update-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-and-update-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_lock_unlock_and_delete [Scenario]

Boot a server, lock it, then unlock and delete it.

Optional 'min_sleep' and 'max_sleep' parameters allow the
scenario to simulate a pause between locking and unlocking the
server (of random duration from min_sleep to max_sleep).

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-lock-unlock-and-delete-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-lock-unlock-and-delete-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-lock-unlock-and-delete-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-lock-unlock-and-delete-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-lock-unlock-and-delete-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-lock-unlock-and-delete-min-sleep)  
  Minimum sleep time between locking and unlocking
  in seconds
  

<a name=ScenarioNovaServersboot-lock-unlock-and-delete-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-lock-unlock-and-delete-max-sleep)  
  Maximum sleep time between locking and unlocking
  in seconds
  

<a name=ScenarioNovaServersboot-lock-unlock-and-delete-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-lock-unlock-and-delete-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-lock-unlock-and-delete-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-lock-unlock-and-delete-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server [Scenario]

Boot a server.

Assumes that cleanup is done elsewhere.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-auto-assign-nic></a>

* *auto_assign_nic* [[ref]](#ScenarioNovaServersboot-server-auto-assign-nic)  
  True if NICs should be assigned
  

<a name=ScenarioNovaServersboot-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_and_attach_interface [Scenario]

Create server and subnet, then attach the interface to it.

This scenario measures the "nova interface-attach" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-and-attach-interface-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-and-attach-interface-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-and-attach-interface-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-and-attach-interface-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-and-attach-interface-network-create-args></a>

* *network_create_args* [[ref]](#ScenarioNovaServersboot-server-and-attach-interface-network-create-args)  
  dict, POST /v2.0/networks request
  options.
  

<a name=ScenarioNovaServersboot-server-and-attach-interface-subnet-create-args></a>

* *subnet_create_args* [[ref]](#ScenarioNovaServersboot-server-and-attach-interface-subnet-create-args)  
  dict, POST /v2.0/subnets request options
  

<a name=ScenarioNovaServersboot-server-and-attach-interface-subnet-cidr-start></a>

* *subnet_cidr_start* [[ref]](#ScenarioNovaServersboot-server-and-attach-interface-subnet-cidr-start)  
  str, start value for subnets CIDR
  

<a name=ScenarioNovaServersboot-server-and-attach-interface-boot-server-args></a>

* *boot_server_args* [[ref]](#ScenarioNovaServersboot-server-and-attach-interface-boot-server-args)  
  Optional additional arguments for
  server creation
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_and_list_interfaces [Scenario]

Boot a server and list interfaces attached to it.

Measure the "nova boot" and "nova interface-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-and-list-interfaces-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-and-list-interfaces-image)  
  ID of the image to be used for server creation
  

<a name=ScenarioNovaServersboot-server-and-list-interfaces-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-and-list-interfaces-flavor)  
  ID of the flavor to be used for server creation
  

<a name=ScenarioNovaServersboot-server-and-list-interfaces-kwargs></a>

* ***kwargs* [[ref]](#ScenarioNovaServersboot-server-and-list-interfaces-kwargs)  
  Optional arguments for booting the instance

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_associate_and_dissociate_floating_ip [Scenario]

Boot a server associate and dissociate a floating IP from it.

The scenario first boot a server and create a floating IP. then
associate the floating IP to the server.Finally dissociate the floating
IP.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-create-floating-ip-args></a>

* *create_floating_ip_args* [[ref]](#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-create-floating-ip-args)  
  Optional additional arguments for
  floating ip creation
  

<a name=ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-server-associate-and-dissociate-floating-ip-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-image)  
  Glance image name to use for the VM
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-flavor)  
  VM flavor name
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-size></a>

* *size* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-block-migration></a>

* *block_migration* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-block-migration)  
  Specifies the migration type
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-disk-over-commit></a>

* *disk_over_commit* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-disk-over-commit)  
  Specifies whether to allow overcommit
  on migrated instance or not
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-boot-server-kwargs)  
  optional arguments for VM creation
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-create-volume-kwargs)  
  optional arguments for volume creation
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-live-migrate-max-sleep)  
  Maximum sleep time in seconds (non-negative)

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

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

**Parameters**:

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-image)  
  Glance image name to use for the VM
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-flavor)  
  VM flavor name
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-to-flavor></a>

* *to_flavor* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-to-flavor)  
  flavor to be used to resize the booted instance
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-volume-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-confirm></a>

* *confirm* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-confirm)  
  True if need to confirm resize else revert resize
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-do-delete></a>

* *do_delete* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-do-delete)  
  True if resources needs to be deleted explicitly
  else use rally cleanup to remove resources
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-boot-server-kwargs)  
  optional arguments for VM creation
  

<a name=ScenarioNovaServersboot-server-attach-created-volume-and-resize-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioNovaServersboot-server-attach-created-volume-and-resize-create-volume-kwargs)  
  optional arguments for volume creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_attach_volume_and_list_attachments [Scenario]

Create a VM, attach N volume to it and list server's attachemnt.

Measure the "nova volume-attachments" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-attach-volume-and-list-attachments-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-image)  
  Glance image name to use for the VM
  

<a name=ScenarioNovaServersboot-server-attach-volume-and-list-attachments-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-flavor)  
  VM flavor name
  

<a name=ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-size)  
  volume size (in GB), default 1G
  

<a name=ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-num></a>

* *volume_num* [[ref]](#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-volume-num)  
  the num of attached volume
  

<a name=ScenarioNovaServersboot-server-attach-volume-and-list-attachments-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-boot-server-kwargs)  
  optional arguments for VM creation
  

<a name=ScenarioNovaServersboot-server-attach-volume-and-list-attachments-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioNovaServersboot-server-attach-volume-and-list-attachments-create-volume-kwargs)  
  optional arguments for volume creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume [Scenario]

Boot a server from volume.

The scenario first creates a volume and then a server.
Assumes that cleanup is done elsewhere.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-from-volume-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-from-volume-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-from-volume-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-from-volume-volume-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-from-volume-volume-type></a>

* *volume_type* [[ref]](#ScenarioNovaServersboot-server-from-volume-volume-type)  
  specifies volume type when there are
  multiple backends
  

<a name=ScenarioNovaServersboot-server-from-volume-auto-assign-nic></a>

* *auto_assign_nic* [[ref]](#ScenarioNovaServersboot-server-from-volume-auto-assign-nic)  
  True if NICs should be assigned
  

<a name=ScenarioNovaServersboot-server-from-volume-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-server-from-volume-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume_and_delete [Scenario]

Boot a server from volume and then delete it.

The scenario first creates a volume and then a server.
Optional 'min_sleep' and 'max_sleep' parameters allow the scenario
to simulate a pause between volume creation and deletion
(of random duration from [min_sleep, max_sleep]).

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-volume-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-volume-type></a>

* *volume_type* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-volume-type)  
  specifies volume type when there are
  multiple backends
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-server-from-volume-and-delete-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-delete-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-type></a>

* *volume_type* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-volume-type)  
  specifies volume type when there are
  multiple backends
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-block-migration></a>

* *block_migration* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-block-migration)  
  Specifies the migration type
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-disk-over-commit></a>

* *disk_over_commit* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-disk-over-commit)  
  Specifies whether to allow overcommit
  on migrated instance or not
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-live-migrate-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-live-migrate-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

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

**Parameters**:

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-to-flavor></a>

* *to_flavor* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-to-flavor)  
  flavor to be used to resize the booted instance
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-volume-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-min-sleep></a>

* *min_sleep* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-min-sleep)  
  Minimum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-max-sleep></a>

* *max_sleep* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-max-sleep)  
  Maximum sleep time in seconds (non-negative)
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-confirm></a>

* *confirm* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-confirm)  
  True if need to confirm resize else revert resize
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-do-delete></a>

* *do_delete* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-do-delete)  
  True if resources needs to be deleted explicitly
  else use rally cleanup to remove resources
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-boot-server-kwargs></a>

* *boot_server_kwargs* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-boot-server-kwargs)  
  optional arguments for VM creation
  

<a name=ScenarioNovaServersboot-server-from-volume-and-resize-create-volume-kwargs></a>

* *create_volume_kwargs* [[ref]](#ScenarioNovaServersboot-server-from-volume-and-resize-create-volume-kwargs)  
  optional arguments for volume creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.boot_server_from_volume_snapshot [Scenario]

Boot a server from a snapshot.

The scenario first creates a volume and creates a
snapshot from this volume, then boots a server from
the created snapshot.
Assumes that cleanup is done elsewhere.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersboot-server-from-volume-snapshot-image></a>

* *image* [[ref]](#ScenarioNovaServersboot-server-from-volume-snapshot-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-snapshot-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersboot-server-from-volume-snapshot-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersboot-server-from-volume-snapshot-volume-size></a>

* *volume_size* [[ref]](#ScenarioNovaServersboot-server-from-volume-snapshot-volume-size)  
  volume size (in GB)
  

<a name=ScenarioNovaServersboot-server-from-volume-snapshot-volume-type></a>

* *volume_type* [[ref]](#ScenarioNovaServersboot-server-from-volume-snapshot-volume-type)  
  specifies volume type when there are
  multiple backends
  

<a name=ScenarioNovaServersboot-server-from-volume-snapshot-auto-assign-nic></a>

* *auto_assign_nic* [[ref]](#ScenarioNovaServersboot-server-from-volume-snapshot-auto-assign-nic)  
  True if NICs should be assigned
  

<a name=ScenarioNovaServersboot-server-from-volume-snapshot-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersboot-server-from-volume-snapshot-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.list_servers [Scenario]

List all servers.

This simple scenario test the nova list command by listing
all the servers.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerslist-servers-detailed></a>

* *detailed* [[ref]](#ScenarioNovaServerslist-servers-detailed)  
  True if detailed information about servers
  should be listed
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.pause_and_unpause_server [Scenario]

Create a server, pause, unpause and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerspause-and-unpause-server-image></a>

* *image* [[ref]](#ScenarioNovaServerspause-and-unpause-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServerspause-and-unpause-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServerspause-and-unpause-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServerspause-and-unpause-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServerspause-and-unpause-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServerspause-and-unpause-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServerspause-and-unpause-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.resize_server [Scenario]

Boot a server, then resize and delete it.

This test will confirm the resize by default,
or revert the resize if confirm is set to false.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersresize-server-image></a>

* *image* [[ref]](#ScenarioNovaServersresize-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersresize-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersresize-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersresize-server-to-flavor></a>

* *to_flavor* [[ref]](#ScenarioNovaServersresize-server-to-flavor)  
  flavor to be used to resize the booted instance
  

<a name=ScenarioNovaServersresize-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersresize-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersresize-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersresize-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.resize_shutoff_server [Scenario]

Boot a server and stop it, then resize and delete it.

This test will confirm the resize by default,
or revert the resize if confirm is set to false.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersresize-shutoff-server-image></a>

* *image* [[ref]](#ScenarioNovaServersresize-shutoff-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersresize-shutoff-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersresize-shutoff-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersresize-shutoff-server-to-flavor></a>

* *to_flavor* [[ref]](#ScenarioNovaServersresize-shutoff-server-to-flavor)  
  flavor to be used to resize the booted instance
  

<a name=ScenarioNovaServersresize-shutoff-server-confirm></a>

* *confirm* [[ref]](#ScenarioNovaServersresize-shutoff-server-confirm)  
  True if need to confirm resize else revert resize
  

<a name=ScenarioNovaServersresize-shutoff-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersresize-shutoff-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersresize-shutoff-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersresize-shutoff-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.shelve_and_unshelve_server [Scenario]

Create a server, shelve, unshelve and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServersshelve-and-unshelve-server-image></a>

* *image* [[ref]](#ScenarioNovaServersshelve-and-unshelve-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServersshelve-and-unshelve-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServersshelve-and-unshelve-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServersshelve-and-unshelve-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServersshelve-and-unshelve-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServersshelve-and-unshelve-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServersshelve-and-unshelve-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.snapshot_server [Scenario]

Boot a server, make its snapshot and delete both.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerssnapshot-server-image></a>

* *image* [[ref]](#ScenarioNovaServerssnapshot-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServerssnapshot-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServerssnapshot-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServerssnapshot-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServerssnapshot-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServerssnapshot-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServerssnapshot-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServers.suspend_and_resume_server [Scenario]

Create a server, suspend, resume and then delete it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServerssuspend-and-resume-server-image></a>

* *image* [[ref]](#ScenarioNovaServerssuspend-and-resume-server-image)  
  image to be used to boot an instance
  

<a name=ScenarioNovaServerssuspend-and-resume-server-flavor></a>

* *flavor* [[ref]](#ScenarioNovaServerssuspend-and-resume-server-flavor)  
  flavor to be used to boot an instance
  

<a name=ScenarioNovaServerssuspend-and-resume-server-force-delete></a>

* *force_delete* [[ref]](#ScenarioNovaServerssuspend-and-resume-server-force-delete)  
  True if force_delete should be used
  

<a name=ScenarioNovaServerssuspend-and-resume-server-kwargs></a>

* *kwargs* [[ref]](#ScenarioNovaServerssuspend-and-resume-server-kwargs)  
  Optional additional arguments for server creation

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.nova.servers](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/servers.py)

<hr />

#### NovaServices.list_services [Scenario]

List all nova services.

Measure the "nova service-list" command performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioNovaServiceslist-services-host></a>

* *host* [[ref]](#ScenarioNovaServiceslist-services-host)  
  List nova services on host
  

<a name=ScenarioNovaServiceslist-services-binary></a>

* *binary* [[ref]](#ScenarioNovaServiceslist-services-binary)  
  List nova services matching given binary

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.nova.services](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/nova/services.py)

<hr />

#### Quotas.cinder_get [Scenario]

Get quotas for Cinder.

Measure the "cinder quota-show" command performance

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.cinder_update [Scenario]

Update quotas for Cinder.

__Platform__: openstack

**Parameters**:

<a name=ScenarioQuotascinder-update-max-quota></a>

* *max_quota* [[ref]](#ScenarioQuotascinder-update-max-quota)  
  Max value to be updated for quota.

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.cinder_update_and_delete [Scenario]

Update and Delete quotas for Cinder.

__Platform__: openstack

**Parameters**:

<a name=ScenarioQuotascinder-update-and-delete-max-quota></a>

* *max_quota* [[ref]](#ScenarioQuotascinder-update-and-delete-max-quota)  
  Max value to be updated for quota.

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.neutron_update [Scenario]

Update quotas for neutron.

__Platform__: openstack

**Parameters**:

<a name=ScenarioQuotasneutron-update-max-quota></a>

* *max_quota* [[ref]](#ScenarioQuotasneutron-update-max-quota)  
  Max value to be updated for quota.

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.nova_get [Scenario]

Get quotas for nova.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.nova_update [Scenario]

Update quotas for Nova.

__Platform__: openstack

**Parameters**:

<a name=ScenarioQuotasnova-update-max-quota></a>

* *max_quota* [[ref]](#ScenarioQuotasnova-update-max-quota)  
  Max value to be updated for quota.

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### Quotas.nova_update_and_delete [Scenario]

Update and delete quotas for Nova.

__Platform__: openstack

**Parameters**:

<a name=ScenarioQuotasnova-update-and-delete-max-quota></a>

* *max_quota* [[ref]](#ScenarioQuotasnova-update-and-delete-max-quota)  
  Max value to be updated for quota.

__Requires platform(s)__:

* openstack with the next options: {u'admin': True, u'users': True}

__Module__: [rally_openstack.scenarios.quotas.quotas](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/quotas/quotas.py)

<hr />

#### SaharaClusters.create_and_delete_cluster [Scenario]

Launch and delete a Sahara Cluster.

This scenario launches a Hadoop cluster, waits until it becomes
'Active' and deletes it.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-flavor></a>

* *flavor* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-flavor)  
  Nova flavor that will be for nodes in the
  created node groups. Deprecated.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-master-flavor></a>

* *master_flavor* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-master-flavor)  
  Nova flavor that will be used for the master
  instance of the cluster
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-worker-flavor></a>

* *worker_flavor* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-worker-flavor)  
  Nova flavor that will be used for the workers of
  the cluster
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-workers-count></a>

* *workers_count* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-workers-count)  
  number of worker instances in a cluster
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-plugin-name></a>

* *plugin_name* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-plugin-name)  
  name of a provisioning plugin
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-hadoop-version></a>

* *hadoop_version* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-hadoop-version)  
  version of Hadoop distribution supported by
  the specified plugin.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-floating-ip-pool></a>

* *floating_ip_pool* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-floating-ip-pool)  
  floating ip pool name from which Floating
  IPs will be allocated. Sahara will determine
  automatically how to treat this depending on
  its own configurations. Defaults to None
  because in some cases Sahara may work w/o
  Floating IPs.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-volumes-per-node></a>

* *volumes_per_node* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-volumes-per-node)  
  number of Cinder volumes that will be
  attached to every cluster node
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-volumes-size></a>

* *volumes_size* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-volumes-size)  
  size of each Cinder volume in GB
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-auto-security-group></a>

* *auto_security_group* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-auto-security-group)  
  boolean value. If set to True Sahara will
  create a Security Group for each Node Group
  in the Cluster automatically.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-security-groups></a>

* *security_groups* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-security-groups)  
  list of security groups that will be used
  while creating VMs. If auto_security_group
  is set to True, this list can be left empty.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-node-configs></a>

* *node_configs* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-node-configs)  
  config dict that will be passed to each Node
  Group
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-cluster-configs></a>

* *cluster_configs* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-cluster-configs)  
  config dict that will be passed to the
  Cluster
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-enable-anti-affinity></a>

* *enable_anti_affinity* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-enable-anti-affinity)  
  If set to true the vms will be scheduled
  one per compute node.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-enable-proxy></a>

* *enable_proxy* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-enable-proxy)  
  Use Master Node of a Cluster as a Proxy node and
  do not assign floating ips to workers.
  

<a name=ScenarioSaharaClusterscreate-and-delete-cluster-use-autoconfig></a>

* *use_autoconfig* [[ref]](#ScenarioSaharaClusterscreate-and-delete-cluster-use-autoconfig)  
  If True, instances of the node group will be
  automatically configured during cluster
  creation. If False, the configuration values
  should be specify manually
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.sahara.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/clusters.py)

<hr />

#### SaharaClusters.create_scale_delete_cluster [Scenario]

Launch, scale and delete a Sahara Cluster.

This scenario launches a Hadoop cluster, waits until it becomes
'Active'. Then a series of scale operations is applied. The scaling
happens according to numbers listed in

__Platform__: openstack

**Parameters**:

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-flavor></a>

* *flavor* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-flavor)  
  Nova flavor that will be for nodes in the
  created node groups. Deprecated.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-master-flavor></a>

* *master_flavor* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-master-flavor)  
  Nova flavor that will be used for the master
  instance of the cluster
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-worker-flavor></a>

* *worker_flavor* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-worker-flavor)  
  Nova flavor that will be used for the workers of
  the cluster
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-workers-count></a>

* *workers_count* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-workers-count)  
  number of worker instances in a cluster
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-plugin-name></a>

* *plugin_name* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-plugin-name)  
  name of a provisioning plugin
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-hadoop-version></a>

* *hadoop_version* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-hadoop-version)  
  version of Hadoop distribution supported by
  the specified plugin.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-deltas></a>

* *deltas* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-deltas)  
  list of integers which will be used to add or
  remove worker nodes from the cluster
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-floating-ip-pool></a>

* *floating_ip_pool* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-floating-ip-pool)  
  floating ip pool name from which Floating
  IPs will be allocated. Sahara will determine
  automatically how to treat this depending on
  its own configurations. Defaults to None
  because in some cases Sahara may work w/o
  Floating IPs.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-neutron-net-id></a>

* *neutron_net_id* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-neutron-net-id)  
  id of a Neutron network that will be used
  for fixed IPs. This parameter is ignored when
  Nova Network is set up.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-per-node></a>

* *volumes_per_node* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-per-node)  
  number of Cinder volumes that will be
  attached to every cluster node
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-size></a>

* *volumes_size* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-volumes-size)  
  size of each Cinder volume in GB
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-auto-security-group></a>

* *auto_security_group* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-auto-security-group)  
  boolean value. If set to True Sahara will
  create a Security Group for each Node Group
  in the Cluster automatically.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-security-groups></a>

* *security_groups* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-security-groups)  
  list of security groups that will be used
  while creating VMs. If auto_security_group
  is set to True this list can be left empty.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-node-configs></a>

* *node_configs* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-node-configs)  
  configs dict that will be passed to each Node
  Group
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-cluster-configs></a>

* *cluster_configs* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-cluster-configs)  
  configs dict that will be passed to the
  Cluster
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-enable-anti-affinity></a>

* *enable_anti_affinity* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-enable-anti-affinity)  
  If set to true the vms will be scheduled
  one per compute node.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-enable-proxy></a>

* *enable_proxy* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-enable-proxy)  
  Use Master Node of a Cluster as a Proxy node and
  do not assign floating ips to workers.
  

<a name=ScenarioSaharaClusterscreate-scale-delete-cluster-use-autoconfig></a>

* *use_autoconfig* [[ref]](#ScenarioSaharaClusterscreate-scale-delete-cluster-use-autoconfig)  
  If True, instances of the node group will be
  automatically configured during cluster
  creation. If False, the configuration values
  should be specify manually
  

__Module__: [rally_openstack.scenarios.sahara.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/clusters.py)

<hr />

#### SaharaJob.create_launch_job [Scenario]

Create and execute a Sahara EDP Job.

This scenario Creates a Job entity and launches an execution on a
Cluster.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSaharaJobcreate-launch-job-job-type></a>

* *job_type* [[ref]](#ScenarioSaharaJobcreate-launch-job-job-type)  
  type of the Data Processing Job
  

<a name=ScenarioSaharaJobcreate-launch-job-configs></a>

* *configs* [[ref]](#ScenarioSaharaJobcreate-launch-job-configs)  
  config dict that will be passed to a Job Execution
  

<a name=ScenarioSaharaJobcreate-launch-job-job-idx></a>

* *job_idx* [[ref]](#ScenarioSaharaJobcreate-launch-job-job-idx)  
  index of a job in a sequence. This index will be
  used to create different atomic actions for each job
  in a sequence
  

__Module__: [rally_openstack.scenarios.sahara.jobs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/jobs.py)

<hr />

#### SaharaJob.create_launch_job_sequence [Scenario]

Create and execute a sequence of the Sahara EDP Jobs.

This scenario Creates a Job entity and launches an execution on a
Cluster for every job object provided.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSaharaJobcreate-launch-job-sequence-jobs></a>

* *jobs* [[ref]](#ScenarioSaharaJobcreate-launch-job-sequence-jobs)  
  list of jobs that should be executed in one context

__Module__: [rally_openstack.scenarios.sahara.jobs](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/jobs.py)

<hr />

#### SaharaJob.create_launch_job_sequence_with_scaling [Scenario]

Create and execute Sahara EDP Jobs on a scaling Cluster.

This scenario Creates a Job entity and launches an execution on a
Cluster for every job object provided. The Cluster is scaled according
to the deltas values and the sequence is launched again.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-jobs></a>

* *jobs* [[ref]](#ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-jobs)  
  list of jobs that should be executed in one context
  

<a name=ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-deltas></a>

* *deltas* [[ref]](#ScenarioSaharaJobcreate-launch-job-sequence-with-scaling-deltas)  
  list of integers which will be used to add or
  remove worker nodes from the cluster
  

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

**Parameters**:

<a name=ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-flavor></a>

* *flavor* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-flavor)  
  Nova flavor that will be for nodes in the
  created node groups
  

<a name=ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-plugin-name></a>

* *plugin_name* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-plugin-name)  
  name of a provisioning plugin
  

<a name=ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-hadoop-version></a>

* *hadoop_version* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-hadoop-version)  
  version of Hadoop distribution supported by
  the specified plugin.
  

<a name=ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-use-autoconfig></a>

* *use_autoconfig* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-and-list-node-group-templates-use-autoconfig)  
  If True, instances of the node group will be
  automatically configured during cluster
  creation. If False, the configuration values
  should be specify manually
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.sahara.node_group_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/node_group_templates.py)

<hr />

#### SaharaNodeGroupTemplates.create_delete_node_group_templates [Scenario]

Create and delete Sahara Node Group Templates.

This scenario creates and deletes two most common types of
Node Group Templates.

By default the templates are created for the vanilla Hadoop
provisioning plugin using the version 1.2.1

__Platform__: openstack

**Parameters**:

<a name=ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-flavor></a>

* *flavor* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-flavor)  
  Nova flavor that will be for nodes in the
  created node groups
  

<a name=ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-plugin-name></a>

* *plugin_name* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-plugin-name)  
  name of a provisioning plugin
  

<a name=ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-hadoop-version></a>

* *hadoop_version* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-hadoop-version)  
  version of Hadoop distribution supported by
  the specified plugin.
  

<a name=ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-use-autoconfig></a>

* *use_autoconfig* [[ref]](#ScenarioSaharaNodeGroupTemplatescreate-delete-node-group-templates-use-autoconfig)  
  If True, instances of the node group will be
  automatically configured during cluster
  creation. If False, the configuration values
  should be specify manually
  

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.sahara.node_group_templates](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/sahara/node_group_templates.py)

<hr />

#### SenlinClusters.create_and_delete_cluster [Scenario]

Create a cluster and then delete it.

Measure the "senlin cluster-create" and "senlin cluster-delete"
commands performance.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSenlinClusterscreate-and-delete-cluster-desired-capacity></a>

* *desired_capacity* [[ref]](#ScenarioSenlinClusterscreate-and-delete-cluster-desired-capacity)  
  The capacity or initial number of nodes
  owned by the cluster
  

<a name=ScenarioSenlinClusterscreate-and-delete-cluster-min-size></a>

* *min_size* [[ref]](#ScenarioSenlinClusterscreate-and-delete-cluster-min-size)  
  The minimum number of nodes owned by the cluster
  

<a name=ScenarioSenlinClusterscreate-and-delete-cluster-max-size></a>

* *max_size* [[ref]](#ScenarioSenlinClusterscreate-and-delete-cluster-max-size)  
  The maximum number of nodes owned by the cluster.
  -1 means no limit
  

<a name=ScenarioSenlinClusterscreate-and-delete-cluster-timeout></a>

* *timeout* [[ref]](#ScenarioSenlinClusterscreate-and-delete-cluster-timeout)  
  The timeout value in seconds for cluster creation
  

<a name=ScenarioSenlinClusterscreate-and-delete-cluster-metadata></a>

* *metadata* [[ref]](#ScenarioSenlinClusterscreate-and-delete-cluster-metadata)  
  A set of key value pairs to associate with the cluster

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.senlin.clusters](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/senlin/clusters.py)

<hr />

#### SwiftObjects.create_container_and_object_then_delete_all [Scenario]

Create container and objects then delete everything created.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSwiftObjectscreate-container-and-object-then-delete-all-objects-per-container></a>

* *objects_per_container* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-delete-all-objects-per-container)  
  int, number of objects to upload
  

<a name=ScenarioSwiftObjectscreate-container-and-object-then-delete-all-object-size></a>

* *object_size* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-delete-all-object-size)  
  int, temporary local object size
  

<a name=ScenarioSwiftObjectscreate-container-and-object-then-delete-all-kwargs></a>

* *kwargs* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-delete-all-kwargs)  
  dict, optional parameters to create container

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.create_container_and_object_then_download_object [Scenario]

Create container and objects then download all objects.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSwiftObjectscreate-container-and-object-then-download-object-objects-per-container></a>

* *objects_per_container* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-download-object-objects-per-container)  
  int, number of objects to upload
  

<a name=ScenarioSwiftObjectscreate-container-and-object-then-download-object-object-size></a>

* *object_size* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-download-object-object-size)  
  int, temporary local object size
  

<a name=ScenarioSwiftObjectscreate-container-and-object-then-download-object-kwargs></a>

* *kwargs* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-download-object-kwargs)  
  dict, optional parameters to create container

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.create_container_and_object_then_list_objects [Scenario]

Create container and objects then list all objects.

__Platform__: openstack

**Parameters**:

<a name=ScenarioSwiftObjectscreate-container-and-object-then-list-objects-objects-per-container></a>

* *objects_per_container* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-list-objects-objects-per-container)  
  int, number of objects to upload
  

<a name=ScenarioSwiftObjectscreate-container-and-object-then-list-objects-object-size></a>

* *object_size* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-list-objects-object-size)  
  int, temporary local object size
  

<a name=ScenarioSwiftObjectscreate-container-and-object-then-list-objects-kwargs></a>

* *kwargs* [[ref]](#ScenarioSwiftObjectscreate-container-and-object-then-list-objects-kwargs)  
  dict, optional parameters to create container

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.list_and_download_objects_in_containers [Scenario]

List and download objects in all containers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### SwiftObjects.list_objects_in_containers [Scenario]

List objects in all containers.

__Platform__: openstack

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.swift.objects](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/swift/objects.py)

<hr />

#### VMTasks.boot_runcommand_delete [Scenario]

Boot a server, run script specified in command and delete server.

__Platform__: openstack

**Parameters**:

<a name=ScenarioVMTasksboot-runcommand-delete-image></a>

* *image* [[ref]](#ScenarioVMTasksboot-runcommand-delete-image)  
  glance image name to use for the vm. Optional
  in case of specified "image_command_customizer" context
  

<a name=ScenarioVMTasksboot-runcommand-delete-flavor></a>

* *flavor* [[ref]](#ScenarioVMTasksboot-runcommand-delete-flavor)  
  VM flavor name
  

<a name=ScenarioVMTasksboot-runcommand-delete-username></a>

* *username* [[ref]](#ScenarioVMTasksboot-runcommand-delete-username)  
  ssh username on server, str
  

<a name=ScenarioVMTasksboot-runcommand-delete-password></a>

* *password* [[ref]](#ScenarioVMTasksboot-runcommand-delete-password)  
  Password on SSH authentication
  

<a name=ScenarioVMTasksboot-runcommand-delete-command></a>

* *command* [[ref]](#ScenarioVMTasksboot-runcommand-delete-command)  
  Command-specifying dictionary that either specifies
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
  

<a name=ScenarioVMTasksboot-runcommand-delete-volume-args></a>

* *volume_args* [[ref]](#ScenarioVMTasksboot-runcommand-delete-volume-args)  
  volume args for booting server from volume
  

<a name=ScenarioVMTasksboot-runcommand-delete-floating-network></a>

* *floating_network* [[ref]](#ScenarioVMTasksboot-runcommand-delete-floating-network)  
  external network name, for floating ip
  

<a name=ScenarioVMTasksboot-runcommand-delete-port></a>

* *port* [[ref]](#ScenarioVMTasksboot-runcommand-delete-port)  
  ssh port for SSH connection
  

<a name=ScenarioVMTasksboot-runcommand-delete-use-floating-ip></a>

* *use_floating_ip* [[ref]](#ScenarioVMTasksboot-runcommand-delete-use-floating-ip)  
  bool, floating or fixed IP for SSH connection
  

<a name=ScenarioVMTasksboot-runcommand-delete-force-delete></a>

* *force_delete* [[ref]](#ScenarioVMTasksboot-runcommand-delete-force-delete)  
  whether to use force_delete for servers
  

<a name=ScenarioVMTasksboot-runcommand-delete-wait-for-ping></a>

* *wait_for_ping* [[ref]](#ScenarioVMTasksboot-runcommand-delete-wait-for-ping)  
  whether to check connectivity on server creation
  

<a name=ScenarioVMTasksboot-runcommand-delete-max-log-length></a>

* *max_log_length* [[ref]](#ScenarioVMTasksboot-runcommand-delete-max-log-length)  
  The number of tail nova console-log lines user
  would like to retrieve
  

<a name=ScenarioVMTasksboot-runcommand-delete-kwargs></a>

* *kwargs* [[ref]](#ScenarioVMTasksboot-runcommand-delete-kwargs)  
  extra arguments for booting the server

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

__Module__: [rally_openstack.scenarios.vm.vmtasks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/vm/vmtasks.py)

<hr />

#### VMTasks.dd_load_test [Scenario]

Boot a server from a custom image and performs dd load test.

!!! note
    dd load test is prepared script by Rally team. It checks
    writing and reading metrics from the VM.

__Platform__: openstack

**Parameters**:

<a name=ScenarioVMTasksdd-load-test-image></a>

* *image* [[ref]](#ScenarioVMTasksdd-load-test-image)  
  glance image name to use for the vm. Optional
  in case of specified "image_command_customizer" context
  

<a name=ScenarioVMTasksdd-load-test-flavor></a>

* *flavor* [[ref]](#ScenarioVMTasksdd-load-test-flavor)  
  VM flavor name
  

<a name=ScenarioVMTasksdd-load-test-username></a>

* *username* [[ref]](#ScenarioVMTasksdd-load-test-username)  
  ssh username on server, str
  

<a name=ScenarioVMTasksdd-load-test-password></a>

* *password* [[ref]](#ScenarioVMTasksdd-load-test-password)  
  Password on SSH authentication
  

<a name=ScenarioVMTasksdd-load-test-interpreter></a>

* *interpreter* [[ref]](#ScenarioVMTasksdd-load-test-interpreter)  
  the interpreter to execute script with dd load test
  (defaults to /bin/sh)
  

<a name=ScenarioVMTasksdd-load-test-command></a>

* *command* [[ref]](#ScenarioVMTasksdd-load-test-command)  
  DEPRECATED. use interpreter instead.
  

<a name=ScenarioVMTasksdd-load-test-volume-args></a>

* *volume_args* [[ref]](#ScenarioVMTasksdd-load-test-volume-args)  
  volume args for booting server from volume
  

<a name=ScenarioVMTasksdd-load-test-floating-network></a>

* *floating_network* [[ref]](#ScenarioVMTasksdd-load-test-floating-network)  
  external network name, for floating ip
  

<a name=ScenarioVMTasksdd-load-test-port></a>

* *port* [[ref]](#ScenarioVMTasksdd-load-test-port)  
  ssh port for SSH connection
  

<a name=ScenarioVMTasksdd-load-test-use-floating-ip></a>

* *use_floating_ip* [[ref]](#ScenarioVMTasksdd-load-test-use-floating-ip)  
  bool, floating or fixed IP for SSH connection
  

<a name=ScenarioVMTasksdd-load-test-force-delete></a>

* *force_delete* [[ref]](#ScenarioVMTasksdd-load-test-force-delete)  
  whether to use force_delete for servers
  

<a name=ScenarioVMTasksdd-load-test-wait-for-ping></a>

* *wait_for_ping* [[ref]](#ScenarioVMTasksdd-load-test-wait-for-ping)  
  whether to check connectivity on server creation
  

<a name=ScenarioVMTasksdd-load-test-max-log-length></a>

* *max_log_length* [[ref]](#ScenarioVMTasksdd-load-test-max-log-length)  
  The number of tail nova console-log lines user
  would like to retrieve
  

<a name=ScenarioVMTasksdd-load-test-kwargs></a>

* *kwargs* [[ref]](#ScenarioVMTasksdd-load-test-kwargs)  
  extra arguments for booting the server

__Requires platform(s)__:

* openstack with the next options: {u'users': True}

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

**Parameters**:

<a name=ScenarioVMTasksruncommand-heat-workload></a>

* *workload* [[ref]](#ScenarioVMTasksruncommand-heat-workload)  
  workload to run
  

<a name=ScenarioVMTasksruncommand-heat-template></a>

* *template* [[ref]](#ScenarioVMTasksruncommand-heat-template)  
  path to heat template file
  

<a name=ScenarioVMTasksruncommand-heat-files></a>

* *files* [[ref]](#ScenarioVMTasksruncommand-heat-files)  
  additional template files
  

<a name=ScenarioVMTasksruncommand-heat-parameters></a>

* *parameters* [[ref]](#ScenarioVMTasksruncommand-heat-parameters)  
  parameters for heat template

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

**Parameters**:

<a name=ScenarioWatchercreate-audit-template-and-delete-goal></a>

* *goal* [[ref]](#ScenarioWatchercreate-audit-template-and-delete-goal)  
  The goal audit template is based on
  

<a name=ScenarioWatchercreate-audit-template-and-delete-strategy></a>

* *strategy* [[ref]](#ScenarioWatchercreate-audit-template-and-delete-strategy)  
  The strategy used to provide resource optimization
  algorithm
  

__Requires platform(s)__:

* openstack with the next options: {u'admin': True}

__Module__: [rally_openstack.scenarios.watcher.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/watcher/basic.py)

<hr />

#### Watcher.list_audit_templates [Scenario]

List existing audit templates.

Audit templates are being created by Audit Template Context.

__Platform__: openstack

**Parameters**:

<a name=ScenarioWatcherlist-audit-templates-name></a>

* *name* [[ref]](#ScenarioWatcherlist-audit-templates-name)  
  Name of the audit template
  

<a name=ScenarioWatcherlist-audit-templates-goal></a>

* *goal* [[ref]](#ScenarioWatcherlist-audit-templates-goal)  
  Name of the goal
  

<a name=ScenarioWatcherlist-audit-templates-strategy></a>

* *strategy* [[ref]](#ScenarioWatcherlist-audit-templates-strategy)  
  Name of the strategy
  

<a name=ScenarioWatcherlist-audit-templates-limit></a>

* *limit* [[ref]](#ScenarioWatcherlist-audit-templates-limit)  
  The maximum number of results to return per
  request, if:
  
    1) limit > 0, the maximum number of audit templates to return.
    2) limit == 0, return the entire list of audit_templates.
    3) limit param is NOT specified (None), the number of items
       returned respect the maximum imposed by the Watcher API
      (see Watcher's api.max_limit option).
  

<a name=ScenarioWatcherlist-audit-templates-sort-key></a>

* *sort_key* [[ref]](#ScenarioWatcherlist-audit-templates-sort-key)  
  Optional, field used for sorting.
  

<a name=ScenarioWatcherlist-audit-templates-sort-dir></a>

* *sort_dir* [[ref]](#ScenarioWatcherlist-audit-templates-sort-dir)  
  Optional, direction of sorting, either 'asc' (the
  default) or 'desc'.
  

<a name=ScenarioWatcherlist-audit-templates-detail></a>

* *detail* [[ref]](#ScenarioWatcherlist-audit-templates-detail)  
  Optional, boolean whether to return detailed information
  about audit_templates.
  

__Module__: [rally_openstack.scenarios.watcher.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/watcher/basic.py)

<hr />

#### ZaqarBasic.create_queue [Scenario]

Create a Zaqar queue with a random name.

__Platform__: openstack

**Parameters**:

<a name=ScenarioZaqarBasiccreate-queue-kwargs></a>

* *kwargs* [[ref]](#ScenarioZaqarBasiccreate-queue-kwargs)  
  other optional parameters to create queues like
  "metadata"
  

__Module__: [rally_openstack.scenarios.zaqar.basic](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/zaqar/basic.py)

<hr />

#### ZaqarBasic.producer_consumer [Scenario]

Serial message producer/consumer.

Creates a Zaqar queue with random name, sends a set of messages
and then retrieves an iterator containing those.

__Platform__: openstack

**Parameters**:

<a name=ScenarioZaqarBasicproducer-consumer-min-msg-count></a>

* *min_msg_count* [[ref]](#ScenarioZaqarBasicproducer-consumer-min-msg-count)  
  min number of messages to be posted
  

<a name=ScenarioZaqarBasicproducer-consumer-max-msg-count></a>

* *max_msg_count* [[ref]](#ScenarioZaqarBasicproducer-consumer-max-msg-count)  
  max number of messages to be posted
  

<a name=ScenarioZaqarBasicproducer-consumer-kwargs></a>

* *kwargs* [[ref]](#ScenarioZaqarBasicproducer-consumer-kwargs)  
  other optional parameters to create queues like
  "metadata"
  

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

**Parameters**:

<a name=Validatorcheck-cleanup-resources-admin-required></a>

* *admin_required* [[ref]](#Validatorcheck-cleanup-resources-admin-required)  
  describes access level to resource

__Module__: [rally_openstack.contexts.cleanup.base](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/contexts/cleanup/base.py)

<hr />

#### external_network_exists [Validator]

Validator checks that external network with given name exists.

__Platform__: openstack

**Parameters**:

<a name=Validatorexternal-network-exists-param-name></a>

* *param_name* [[ref]](#Validatorexternal-network-exists-param-name)  
  name of validated network

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### flavor_exists [Validator]

Returns validator for flavor.

__Platform__: openstack

**Parameters**:

<a name=Validatorflavor-exists-param-name></a>

* *param_name* [[ref]](#Validatorflavor-exists-param-name)  
  defines which variable should be used
  to get flavor id value.
  

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### image_exists [Validator]

Validator checks existed image or not.

__Platform__: openstack

**Parameters**:

<a name=Validatorimage-exists-param-name></a>

* *param_name* [[ref]](#Validatorimage-exists-param-name)  
  defines which variable should be used
  to get image id value.
  

<a name=Validatorimage-exists-nullable></a>

* *nullable* [[ref]](#Validatorimage-exists-nullable)  
  defines image id param is required

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### image_valid_on_flavor [Validator]

Returns validator for image could be used for current flavor.

__Platform__: openstack

**Parameters**:

<a name=Validatorimage-valid-on-flavor-flavor-param></a>

* *flavor_param* [[ref]](#Validatorimage-valid-on-flavor-flavor-param)  
  defines which variable should be used
  to get flavor id value.
  

<a name=Validatorimage-valid-on-flavor-image-param></a>

* *image_param* [[ref]](#Validatorimage-valid-on-flavor-image-param)  
  defines which variable should be used
  to get image id value.
  

<a name=Validatorimage-valid-on-flavor-validate-disk></a>

* *validate_disk* [[ref]](#Validatorimage-valid-on-flavor-validate-disk)  
  flag to indicate whether to validate flavor's
  disk. Should be True if instance is booted from
  image. Should be False if instance is booted
  from volume. Default value is True.
  

<a name=Validatorimage-valid-on-flavor-fail-on-404-image></a>

* *fail_on_404_image* [[ref]](#Validatorimage-valid-on-flavor-fail-on-404-image)  
  flag what indicate whether to validate image
  or not.
  

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_api_versions [Validator]

Validator checks component API versions.

__Platform__: openstack

**Parameters**:

<a name=Validatorrequired-api-versions-component></a>

* *component* [[ref]](#Validatorrequired-api-versions-component)  
  name of required component
  

<a name=Validatorrequired-api-versions-versions></a>

* *versions* [[ref]](#Validatorrequired-api-versions-versions)  
  version of required component

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_cinder_services [Validator]

Validator checks that specified Cinder service is available.

It uses Cinder client with admin permissions to call
'cinder service-list' call

__Platform__: openstack

**Parameters**:

<a name=Validatorrequired-cinder-services-services></a>

* *services* [[ref]](#Validatorrequired-cinder-services-services)  
  Cinder service name

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_clients [Validator]

Validator checks if specified OpenStack clients are available.

__Platform__: openstack

**Parameters**:

<a name=Validatorrequired-clients-components></a>

* *components* [[ref]](#Validatorrequired-clients-components)  
  list of client components names
  

<a name=Validatorrequired-clients-kwargs></a>

* ***kwargs* [[ref]](#Validatorrequired-clients-kwargs)  
  optional parameters:
  admin - bool, whether to use admin clients
  

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_neutron_extensions [Validator]

Validator checks if the specified Neutron extension is available.

__Platform__: openstack

**Parameters**:

<a name=Validatorrequired-neutron-extensions-extensions></a>

* *extensions* [[ref]](#Validatorrequired-neutron-extensions-extensions)  
  list of Neutron extensions

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### required_services [Validator]

Validator checks if specified OpenStack services are available.

__Platform__: openstack

**Parameters**:

<a name=Validatorrequired-services-services></a>

* *services* [[ref]](#Validatorrequired-services-services)  
  list with names of required services

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### valid_command [Validator]

Checks that parameter is a proper command-specifying dictionary.

Ensure that the command dictionary is a proper command-specifying
dictionary described in 'vmtasks.VMTasks.boot_runcommand_delete'
docstring.

__Platform__: openstack

**Parameters**:

<a name=Validatorvalid-command-param-name></a>

* *param_name* [[ref]](#Validatorvalid-command-param-name)  
  Name of parameter to validate
  

<a name=Validatorvalid-command-required></a>

* *required* [[ref]](#Validatorvalid-command-required)  
  Boolean indicating that the command dictionary is
  required
  

__Module__: [rally_openstack.scenarios.vm.vmtasks](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/scenarios/vm/vmtasks.py)

<hr />

#### validate_heat_template [Validator]

Validates heat template.

__Platform__: openstack

**Parameters**:

<a name=Validatorvalidate-heat-template-params></a>

* *params* [[ref]](#Validatorvalidate-heat-template-params)  
  list of parameters to be validated.

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### volume_type_exists [Validator]

Returns validator for volume types.

__Platform__: openstack

**Parameters**:

<a name=Validatorvolume-type-exists-param-name></a>

* *param_name* [[ref]](#Validatorvolume-type-exists-param-name)  
  defines variable to be used as the flag to
  determine if volume types should be checked for
  existence.
  

<a name=Validatorvolume-type-exists-nullable></a>

* *nullable* [[ref]](#Validatorvolume-type-exists-nullable)  
  defines volume_type param is required

__Module__: [rally_openstack.validators](https://github.com/openstack/rally-openstack/blob/master/rally_openstack/validators.py)

<hr />

#### workbook_contains_workflow [Validator]

Validate that workflow exist in workbook when workflow is passed.

__Platform__: openstack

**Parameters**:

<a name=Validatorworkbook-contains-workflow-workbook-param></a>

* *workbook_param* [[ref]](#Validatorworkbook-contains-workflow-workbook-param)  
  parameter containing the workbook definition
  

<a name=Validatorworkbook-contains-workflow-workflow-param></a>

* *workflow_param* [[ref]](#Validatorworkbook-contains-workflow-workflow-param)  
  parameter containing the workflow name

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