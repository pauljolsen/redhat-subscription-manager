Delete system from RedHat Subscription Manager
=============================

At Diligent, when a user deletes a virtual machine using our self-service portal, or via our API, or using our Ansible
modules, we need to delete that machine whether it's powered on or off and whether it's reponsive or not.  Rather than
having to log into the machine to run subscription-manager, we use this custom Ansible module.

This module takes your offline token, requests an access token, pages through all your systems to find the right one,
then gets its UUID and deletes it. Have a look at the module.  


```yaml  
- name: Delete a system from RedHat Subscription Manager
  rhsm_delete_system:
    token: "{{ my_rhsm_offline_token }}"
    hostname: nycserver01
```

