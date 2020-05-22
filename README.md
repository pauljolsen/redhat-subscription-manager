Delete system from RedHat Subscription Manager
=============================

At Diligent, when a user deletes a virtual machine using our self-service portal, our API, or our Ansible
modules, we need to delete that machine whether it's powered on or off and whether it's responsive or not.  Rather than
having to log into the machine with Ansible to run subscription-manager, we use this custom Ansible module to communicate
directly with the RHSM API.  

This module takes your offline token, requests an access token, pages through all your systems to find the right one,
then deletes it. Have a look at the module.  


```yaml  
- name: Delete a system from RedHat Subscription Manager
  rhsm_delete_system:
    token: "{{ my_rhsm_offline_token }}"
    hostname: nycserver01
```

