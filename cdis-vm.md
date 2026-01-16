# CDIS IT VM

We have VMs from CDIS IT.  To access your VM, you'll need to be on the
uwmadison.vpn.wisc.edu VPN.  Read about how to connect to it here:
https://it.wisc.edu/services/wiscvpn/.

You can SSH like this (note that your NETID is your username, and also part of the VM name):

```
ssh NETID@cs544-NETID.cs.wisc.edu
```

Your password is your regular UW password, as you would use to access https://my.wisc.edu.

If you don't like typing your password everytime, you could paste your
public key (from your laptop) in this file (on your VM):
`~/.ssh/authorized_keys`.  Then your private key will be used to
authenticate with you SSH, and you won't need to type a password.

## Common Issues

* VPN access: this is supported by the DoIT Help Desk: https://kb.wisc.edu/helpdesk/
* Reboot: if you're VM got stuck (e.g., because you exhausted all available memory), you can reboot it here: https://proxmox.cs.wisc.edu.  Find your VM and choose the "Reset" option.
* proxmox issues: if you can't even see your VM on proxmox, you can raise a ticket by emailing CDIS IT: it@cdis.wisc.edu.  Note that when working correctly, you will get a warning that "You do not have a valid subscription for this server. Please visit www.proxmox.com to get a list of available options" because we are using the free tier of proxmox.
