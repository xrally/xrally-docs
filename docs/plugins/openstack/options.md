# Available configuration options

## [DEFAULT]

```
# HTTP timeout for any of OpenStack service in seconds
# (floating point value)
#openstack_client_http_timeout = 180.0
```

## [openstack]

```
# Interval between checks when waiting for backup restoring.
# (floating point value)
# Deprecated group/name - benchmark/cinder_backup_restore_poll_interval
#cinder_backup_restore_poll_interval = 2.0
```

```
# Time to wait for cinder backup to be restored.
# (floating point value)
# Deprecated group/name - benchmark/cinder_backup_restore_timeout
#cinder_backup_restore_timeout = 600.0
```

```
# Interval between checks when waiting for volume creation.
# (floating point value)
# Deprecated group/name - benchmark/cinder_volume_create_poll_interval
#cinder_volume_create_poll_interval = 2.0
```

```
# Time to sleep after creating a resource before polling for it status
# (floating point value)
# Deprecated group/name - benchmark/cinder_volume_create_prepoll_delay
#cinder_volume_create_prepoll_delay = 2.0
```

```
# Time to wait for cinder volume to be created.
# (floating point value)
# Deprecated group/name - benchmark/cinder_volume_create_timeout
#cinder_volume_create_timeout = 600.0
```

```
# Interval between checks when waiting for volume deletion.
# (floating point value)
# Deprecated group/name - benchmark/cinder_volume_delete_poll_interval
#cinder_volume_delete_poll_interval = 2.0
```

```
# Time to wait for cinder volume to be deleted.
# (floating point value)
# Deprecated group/name - benchmark/cinder_volume_delete_timeout
#cinder_volume_delete_timeout = 600.0
```

```
# Number of cleanup threads to run
# (integer value)
# Deprecated group/name - cleanup/cleanup_threads
#cleanup_threads = 20
```

```
# Server boot poll interval
# (floating point value)
# Deprecated group/name - benchmark/ec2_server_boot_poll_interval
#ec2_server_boot_poll_interval = 1.0
```

```
# Time to sleep after boot before polling for status
# (floating point value)
# Deprecated group/name - benchmark/ec2_server_boot_prepoll_delay
#ec2_server_boot_prepoll_delay = 1.0
```

```
# Server boot timeout
# (floating point value)
# Deprecated group/name - benchmark/ec2_server_boot_timeout
#ec2_server_boot_timeout = 300.0
```

```
# Enable or disable osprofiler to trace the scenarios
# (boolean value)
# Deprecated group/name - benchmark/enable_profiler
#enable_profiler = True
```

```
# Alternate reference flavor RAM size used by test thatneed two flavors,
# like those that resize an instance
# (integer value)
# Deprecated group/name - tempest/flavor_ref_alt_ram
#flavor_ref_alt_ram = 128
```

```
# Primary flavor RAM size used by most of the test cases
# (integer value)
# Deprecated group/name - tempest/flavor_ref_ram
#flavor_ref_ram = 64
```

```
# Interval between checks when waiting for image creation.
# (floating point value)
# Deprecated group/name - benchmark/glance_image_create_poll_interval
#glance_image_create_poll_interval = 1.0
```

```
# Interval between checks when waiting for image creation.
# (floating point value)
# Deprecated group/name - benchmark/glance_image_create_poll_interval
#glance_image_create_poll_interval = 1.0
```

```
# Time to sleep after creating a resource before polling for it status
# (floating point value)
# Deprecated group/name - benchmark/glance_image_create_prepoll_delay
#glance_image_create_prepoll_delay = 2.0
```

```
# Time to sleep after creating a resource before polling for it status
# (floating point value)
# Deprecated group/name - benchmark/glance_image_create_prepoll_delay
#glance_image_create_prepoll_delay = 2.0
```

```
# Time to wait for glance image to be created.
# (floating point value)
# Deprecated group/name - benchmark/glance_image_create_timeout
#glance_image_create_timeout = 120.0
```

```
# Interval between checks when waiting for image deletion.
# (floating point value)
# Deprecated group/name - benchmark/glance_image_delete_poll_interval
#glance_image_delete_poll_interval = 1.0
```

```
# Time to wait for glance image to be deleted.
# (floating point value)
# Deprecated group/name - benchmark/glance_image_delete_timeout
#glance_image_delete_timeout = 120.0
```

```
# RAM size flavor used for orchestration test cases
# (integer value)
# Deprecated group/name - tempest/heat_instance_type_ram
#heat_instance_type_ram = 64
```

```
# Time interval(in sec) between checks when waiting for stack checking.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_check_poll_interval
#heat_stack_check_poll_interval = 1.0
```

```
# Time(in sec) to wait for stack to be checked.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_check_timeout
#heat_stack_check_timeout = 3600.0
```

```
# Time interval(in sec) between checks when waiting for stack creation.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_create_poll_interval
#heat_stack_create_poll_interval = 1.0
```

```
# Time(in sec) to sleep after creating a resource before polling for it
# status.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_create_prepoll_delay
#heat_stack_create_prepoll_delay = 2.0
```

```
# Time(in sec) to wait for heat stack to be created.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_create_timeout
#heat_stack_create_timeout = 3600.0
```

```
# Time interval(in sec) between checks when waiting for stack deletion.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_delete_poll_interval
#heat_stack_delete_poll_interval = 1.0
```

```
# Time(in sec) to wait for heat stack to be deleted.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_delete_timeout
#heat_stack_delete_timeout = 3600.0
```

```
# Role required for users to be able to manage Heat stacks
# (string value)
# Deprecated group/name - tempest/heat_stack_owner_role
#heat_stack_owner_role = 'heat_stack_owner'
```

```
# Time interval(in sec) between checks when waiting for stack to be
# restored.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_restore_poll_interval
#heat_stack_restore_poll_interval = 1.0
```

```
# Time(in sec) to wait for stack to be restored from snapshot.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_restore_timeout
#heat_stack_restore_timeout = 3600.0
```

```
# Time interval(in sec) between checks when waiting for stack resume.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_resume_poll_interval
#heat_stack_resume_poll_interval = 1.0
```

```
# Time(in sec) to wait for stack to be resumed.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_resume_timeout
#heat_stack_resume_timeout = 3600.0
```

```
# Time interval (in sec) between checks when waiting for a stack to
# scale up or down.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_scale_poll_interval
#heat_stack_scale_poll_interval = 1.0
```

```
# Time (in sec) to wait for stack to scale up or down.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_scale_timeout
#heat_stack_scale_timeout = 3600.0
```

```
# Time interval(in sec) between checks when waiting for stack snapshot
# to be created.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_snapshot_poll_interval
#heat_stack_snapshot_poll_interval = 1.0
```

```
# Time(in sec) to wait for stack snapshot to be created.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_snapshot_timeout
#heat_stack_snapshot_timeout = 3600.0
```

```
# Time interval(in sec) between checks when waiting for stack suspend.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_suspend_poll_interval
#heat_stack_suspend_poll_interval = 1.0
```

```
# Time(in sec) to wait for stack to be suspended.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_suspend_timeout
#heat_stack_suspend_timeout = 3600.0
```

```
# Time interval(in sec) between checks when waiting for stack update.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_update_poll_interval
#heat_stack_update_poll_interval = 1.0
```

```
# Time(in sec) to sleep after updating a resource before polling for it
# status.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_update_prepoll_delay
#heat_stack_update_prepoll_delay = 2.0
```

```
# Time(in sec) to wait for stack to be updated.
# (floating point value)
# Deprecated group/name - benchmark/heat_stack_update_timeout
#heat_stack_update_timeout = 3600.0
```

```
# Role for Heat template-defined users
# (string value)
# Deprecated group/name - tempest/heat_stack_user_role
#heat_stack_user_role = 'heat_stack_user'
```

```
# Image container format to use when creating the image
# (string value)
# Deprecated group/name - tempest/img_container_format
#img_container_format = 'bare'
```

```
# Image disk format to use when creating the image
# (string value)
# Deprecated group/name - tempest/img_disk_format
#img_disk_format = 'qcow2'
```

```
# Regular expression for name of a public image to discover it in the
# cloud and use it for the tests. Note that when Rally is searching for
# the image, case insensitive matching is performed. Specify nothing
# ('img_name_regex =') if you want to disable discovering. In this case
# Rally will create needed resources by itself if the values for the
# corresponding config options are not specified in the Tempest config
# file
# (string value)
# Deprecated group/name - tempest/img_name_regex
#img_name_regex = '^.*(cirros|testvm).*$'
```

```
# image URL
# (string value)
# Deprecated group/name - tempest/img_url
#img_url = 'http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img'
```

```
# Interval(in sec) between checks when waiting for node creation.
# (floating point value)
# Deprecated group/name - benchmark/ironic_node_create_poll_interval
#ironic_node_create_poll_interval = 1.0
```

```
# Ironic node create timeout
# (floating point value)
# Deprecated group/name - benchmark/ironic_node_create_timeout
#ironic_node_create_timeout = 300
```

```
# Ironic node create timeout
# (floating point value)
# Deprecated group/name - benchmark/ironic_node_delete_timeout
#ironic_node_delete_timeout = 300
```

```
# Ironic node poll interval
# (floating point value)
# Deprecated group/name - benchmark/ironic_node_poll_interval
#ironic_node_poll_interval = 1.0
```

```
# Time interval(in sec) between checks when waiting for k8s pod
# creation.
# (floating point value)
# Deprecated group/name - benchmark/k8s_pod_create_poll_interval
#k8s_pod_create_poll_interval = 1.0
```

```
# Time(in sec) to wait for k8s pod to be created.
# (floating point value)
# Deprecated group/name - benchmark/k8s_pod_create_timeout
#k8s_pod_create_timeout = 1200.0
```

```
# Time interval(in sec) between checks when waiting for k8s rc creation.
# (floating point value)
# Deprecated group/name - benchmark/k8s_rc_create_poll_interval
#k8s_rc_create_poll_interval = 1.0
```

```
# Time(in sec) to wait for k8s rc to be created.
# (floating point value)
# Deprecated group/name - benchmark/k8s_rc_create_timeout
#k8s_rc_create_timeout = 1200.0
```

```
# The default role name of the keystone to assign to users.
# (string value)
# Deprecated group/name - users_context/keystone_default_role
#keystone_default_role = 'member'
```

```
# Time interval(in sec) between checks when waiting for cluster
# creation.
# (floating point value)
# Deprecated group/name - benchmark/magnum_cluster_create_poll_interval
#magnum_cluster_create_poll_interval = 2.0
```

```
# Time(in sec) to sleep after creating a resource before polling for the
# status.
# (floating point value)
# Deprecated group/name - benchmark/magnum_cluster_create_prepoll_delay
#magnum_cluster_create_prepoll_delay = 5.0
```

```
# Time(in sec) to wait for magnum cluster to be created.
# (floating point value)
# Deprecated group/name - benchmark/magnum_cluster_create_timeout
#magnum_cluster_create_timeout = 2400.0
```

```
# Interval between checks when waiting for Manila access creation.
# (floating point value)
# Deprecated group/name - benchmark/manila_access_create_poll_interval
#manila_access_create_poll_interval = 3.0
```

```
# Timeout for Manila access creation.
# (floating point value)
# Deprecated group/name - benchmark/manila_access_create_timeout
#manila_access_create_timeout = 300.0
```

```
# Interval between checks when waiting for Manila access deletion.
# (floating point value)
# Deprecated group/name - benchmark/manila_access_delete_poll_interval
#manila_access_delete_poll_interval = 2.0
```

```
# Timeout for Manila access deletion.
# (floating point value)
# Deprecated group/name - benchmark/manila_access_delete_timeout
#manila_access_delete_timeout = 180.0
```

```
# Interval between checks when waiting for Manila share creation.
# (floating point value)
# Deprecated group/name - benchmark/manila_share_create_poll_interval
#manila_share_create_poll_interval = 3.0
```

```
# Delay between creating Manila share and polling for its status.
# (floating point value)
# Deprecated group/name - benchmark/manila_share_create_prepoll_delay
#manila_share_create_prepoll_delay = 2.0
```

```
# Timeout for Manila share creation.
# (floating point value)
# Deprecated group/name - benchmark/manila_share_create_timeout
#manila_share_create_timeout = 300.0
```

```
# Interval between checks when waiting for Manila share deletion.
# (floating point value)
# Deprecated group/name - benchmark/manila_share_delete_poll_interval
#manila_share_delete_poll_interval = 2.0
```

```
# Timeout for Manila share deletion.
# (floating point value)
# Deprecated group/name - benchmark/manila_share_delete_timeout
#manila_share_delete_timeout = 180.0
```

```
# mistral execution timeout
# (integer value)
# Deprecated group/name - benchmark/mistral_execution_timeout
#mistral_execution_timeout = 200
```

```
# Delay between creating Monasca metrics and polling for its elements.
# (floating point value)
# Deprecated group/name - benchmark/monasca_metric_create_prepoll_delay
#monasca_metric_create_prepoll_delay = 15.0
```

```
# Deploy environment check interval in seconds
# (integer value)
# Deprecated group/name - benchmark/deploy_environment_check_interval
#murano_deploy_environment_check_interval = 5
```

```
# A timeout in seconds for an environment deploy
# (integer value)
# Deprecated group/name - benchmark/deploy_environment_timeout
#murano_deploy_environment_timeout = 1200
```

```
# Neutron create loadbalancer poll interval
# (floating point value)
# Deprecated group/name - benchmark/neutron_create_loadbalancer_poll_interval
#neutron_create_loadbalancer_poll_interval = 2.0
```

```
# Neutron create loadbalancer timeout
# (floating point value)
# Deprecated group/name - benchmark/neutron_create_loadbalancer_timeout
#neutron_create_loadbalancer_timeout = 500.0
```

```
# Nova volume detach poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_detach_volume_poll_interval
#nova_detach_volume_poll_interval = 2.0
```

```
# Nova volume detach timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_detach_volume_timeout
#nova_detach_volume_timeout = 200.0
```

```
# Server boot poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_boot_poll_interval
#nova_server_boot_poll_interval = 2.0
```

```
# Time to sleep after boot before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_boot_prepoll_delay
#nova_server_boot_prepoll_delay = 1.0
```

```
# Server boot timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_boot_timeout
#nova_server_boot_timeout = 300.0
```

```
# Server delete poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_delete_poll_interval
#nova_server_delete_poll_interval = 2.0
```

```
# Time to sleep after delete before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_delete_prepoll_delay
#nova_server_delete_prepoll_delay = 2.0
```

```
# Server delete timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_delete_timeout
#nova_server_delete_timeout = 300.0
```

```
# Server image_create poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_image_create_poll_interval
#nova_server_image_create_poll_interval = 2.0
```

```
# Time to sleep after image_create before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_image_create_prepoll_delay
#nova_server_image_create_prepoll_delay = <None>
```

```
# Server image_create timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_image_create_timeout
#nova_server_image_create_timeout = 300.0
```

```
# Server image_delete poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_image_delete_poll_interval
#nova_server_image_delete_poll_interval = 2.0
```

```
# Time to sleep after image_delete before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_image_delete_prepoll_delay
#nova_server_image_delete_prepoll_delay = <None>
```

```
# Server image_delete timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_image_delete_timeout
#nova_server_image_delete_timeout = 300.0
```

```
# Server live_migrate poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_live_migrate_poll_interval
#nova_server_live_migrate_poll_interval = 2.0
```

```
# Time to sleep after live_migrate before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_live_migrate_prepoll_delay
#nova_server_live_migrate_prepoll_delay = 1.0
```

```
# Server live_migrate timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_live_migrate_timeout
#nova_server_live_migrate_timeout = 400.0
```

```
# Server migrate poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_migrate_poll_interval
#nova_server_migrate_poll_interval = 2.0
```

```
# Time to sleep after migrate before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_migrate_prepoll_delay
#nova_server_migrate_prepoll_delay = 1.0
```

```
# Server migrate timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_migrate_timeout
#nova_server_migrate_timeout = 400.0
```

```
# Server pause poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_pause_poll_interval
#nova_server_pause_poll_interval = 2.0
```

```
# Time to sleep after pause before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_pause_prepoll_delay
#nova_server_pause_prepoll_delay = 2.0
```

```
# Server pause timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_pause_timeout
#nova_server_pause_timeout = 300.0
```

```
# Server reboot poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_reboot_poll_interval
#nova_server_reboot_poll_interval = 2.0
```

```
# Time to sleep after reboot before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_reboot_prepoll_delay
#nova_server_reboot_prepoll_delay = 2.0
```

```
# Server reboot timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_reboot_timeout
#nova_server_reboot_timeout = 300.0
```

```
# Server rebuild poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_rebuild_poll_interval
#nova_server_rebuild_poll_interval = 1.0
```

```
# Time to sleep after rebuild before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_rebuild_prepoll_delay
#nova_server_rebuild_prepoll_delay = 1.0
```

```
# Server rebuild timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_rebuild_timeout
#nova_server_rebuild_timeout = 300.0
```

```
# Server rescue poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_rescue_poll_interval
#nova_server_rescue_poll_interval = 2.0
```

```
# Time to sleep after rescue before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_rescue_prepoll_delay
#nova_server_rescue_prepoll_delay = 2.0
```

```
# Server rescue timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_rescue_timeout
#nova_server_rescue_timeout = 300.0
```

```
# Server resize_confirm poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_confirm_poll_interval
#nova_server_resize_confirm_poll_interval = 2.0
```

```
# Time to sleep after resize_confirm before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_confirm_prepoll_delay
#nova_server_resize_confirm_prepoll_delay = <None>
```

```
# Server resize_confirm timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_confirm_timeout
#nova_server_resize_confirm_timeout = 200.0
```

```
# Server resize poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_poll_interval
#nova_server_resize_poll_interval = 5.0
```

```
# Time to sleep after resize before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_prepoll_delay
#nova_server_resize_prepoll_delay = 2.0
```

```
# Server resize_revert poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_revert_poll_interval
#nova_server_resize_revert_poll_interval = 2.0
```

```
# Time to sleep after resize_revert before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_revert_prepoll_delay
#nova_server_resize_revert_prepoll_delay = <None>
```

```
# Server resize_revert timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_revert_timeout
#nova_server_resize_revert_timeout = 200.0
```

```
# Server resize timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resize_timeout
#nova_server_resize_timeout = 400.0
```

```
# Server resume poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resume_poll_interval
#nova_server_resume_poll_interval = 2.0
```

```
# Time to sleep after resume before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resume_prepoll_delay
#nova_server_resume_prepoll_delay = 2.0
```

```
# Server resume timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_resume_timeout
#nova_server_resume_timeout = 300.0
```

```
# Server shelve poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_shelve_poll_interval
#nova_server_shelve_poll_interval = 2.0
```

```
# Time to sleep after shelve before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_shelve_prepoll_delay
#nova_server_shelve_prepoll_delay = 2.0
```

```
# Server shelve timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_shelve_timeout
#nova_server_shelve_timeout = 300.0
```

```
# Server start poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_start_poll_interval
#nova_server_start_poll_interval = 1.0
```

```
# Time to sleep after start before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_start_prepoll_delay
#nova_server_start_prepoll_delay = <None>
```

```
# Server start timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_start_timeout
#nova_server_start_timeout = 300.0
```

```
# Server stop poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_stop_poll_interval
#nova_server_stop_poll_interval = 2.0
```

```
# Time to sleep after stop before polling for status
# (floating point value)
#nova_server_stop_prepoll_delay = <None>
```

```
# Server stop timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_stop_timeout
#nova_server_stop_timeout = 300.0
```

```
# Server suspend poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_suspend_poll_interval
#nova_server_suspend_poll_interval = 2.0
```

```
# Time to sleep after suspend before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_suspend_prepoll_delay
#nova_server_suspend_prepoll_delay = 2.0
```

```
# Server suspend timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_suspend_timeout
#nova_server_suspend_timeout = 300.0
```

```
# Server unpause poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unpause_poll_interval
#nova_server_unpause_poll_interval = 2.0
```

```
# Time to sleep after unpause before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unpause_prepoll_delay
#nova_server_unpause_prepoll_delay = 2.0
```

```
# Server unpause timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unpause_timeout
#nova_server_unpause_timeout = 300.0
```

```
# Server unrescue poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unrescue_poll_interval
#nova_server_unrescue_poll_interval = 2.0
```

```
# Time to sleep after unrescue before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unrescue_prepoll_delay
#nova_server_unrescue_prepoll_delay = 2.0
```

```
# Server unrescue timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unrescue_timeout
#nova_server_unrescue_timeout = 300.0
```

```
# Server unshelve poll interval
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unshelve_poll_interval
#nova_server_unshelve_poll_interval = 2.0
```

```
# Time to sleep after unshelve before polling for status
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unshelve_prepoll_delay
#nova_server_unshelve_prepoll_delay = 2.0
```

```
# Server unshelve timeout
# (floating point value)
# Deprecated group/name - benchmark/nova_server_unshelve_timeout
#nova_server_unshelve_timeout = 300.0
```

```
# Whether Neutron API is older then OpenStack Newton or not. Based in
# this option, some external fields for identifying resources can be
# applied.
# (boolean value)
#pre_newton_neutron = False
```

```
# ID of domain in which projects will be created.
# (string value)
# Deprecated group/name - users_context/project_domain
#project_domain = 'default'
```

```
# A timeout in seconds for deleting resources
# (integer value)
# Deprecated group/name - cleanup/resource_deletion_timeout
#resource_deletion_timeout = 600
```

```
# How many concurrent threads to use for serving roles context
# (integer value)
# Deprecated group/name - roles_context/resource_management_workers
#roles_context_resource_management_workers = 30
```

```
# Cluster status polling interval in seconds
# (integer value)
# Deprecated group/name - benchmark/sahara_cluster_check_interval
#sahara_cluster_check_interval = 5
```

```
# A timeout in seconds for a cluster create operation
# (integer value)
# Deprecated group/name - benchmark/sahara_cluster_create_timeout
#sahara_cluster_create_timeout = 1800
```

```
# A timeout in seconds for a cluster delete operation
# (integer value)
# Deprecated group/name - benchmark/sahara_cluster_delete_timeout
#sahara_cluster_delete_timeout = 900
```

```
# Job Execution status polling interval in seconds
# (integer value)
# Deprecated group/name - benchmark/sahara_job_check_interval
#sahara_job_check_interval = 5
```

```
# A timeout in seconds for a Job Execution to complete
# (integer value)
# Deprecated group/name - benchmark/sahara_job_execution_timeout
#sahara_job_execution_timeout = 600
```

```
# Amount of workers one proxy should serve to.
# (integer value)
# Deprecated group/name - benchmark/sahara_workers_per_proxy
#sahara_workers_per_proxy = 20
```

```
# Time in seconds to wait for senlin action to finish.
# (floating point value)
# Deprecated group/name - benchmark/senlin_action_timeout
#senlin_action_timeout = 3600
```

```
# Role required for users to be able to create Swift containers
# (string value)
# Deprecated group/name - tempest/swift_operator_role
#swift_operator_role = 'Member'
```

```
# User role that has reseller admin
# (string value)
# Deprecated group/name - tempest/swift_reseller_admin_role
#swift_reseller_admin_role = 'ResellerAdmin'
```

```
# ID of domain in which users will be created.
# (string value)
# Deprecated group/name - users_context/user_domain
#user_domain = 'default'
```

```
# The number of concurrent threads to use for serving users context.
# (integer value)
# Deprecated group/name - users_context/resource_management_workers
#users_context_resource_management_workers = 20
```

```
# Interval between checks when waiting for a VM to become pingable
# (floating point value)
# Deprecated group/name - benchmark/vm_ping_poll_interval
#vm_ping_poll_interval = 1.0
```

```
# Time to wait for a VM to become pingable
# (floating point value)
# Deprecated group/name - benchmark/vm_ping_timeout
#vm_ping_timeout = 120.0
```

```
# Watcher audit launch interval
# (floating point value)
# Deprecated group/name - benchmark/watcher_audit_launch_poll_interval
#watcher_audit_launch_poll_interval = 2.0
```

```
# Watcher audit launch timeout
# (integer value)
# Deprecated group/name - benchmark/watcher_audit_launch_timeout
#watcher_audit_launch_timeout = 300
```