# Cross-platform synchronization guide for conda environments

This guide helps when you need to transfer `conda` projects between different platforms. For example: from Linux x86_64 (normal computer) to Linux aarch64 (Raspberry Pi).

Activate the environment and making changes on your computer, then:

## Export the environment without build or architecture info
`conda env export --from-history > environment.yml`

## Copy the environment file to your Pi
`scp environment.yml <user-name>@<pi-ip>:/path/to/folder/`

For example:

`scp environment.yml polliconnect@192.168.1.1203:/home/polliconnect/`

## Create or update/recreate (if you are updating an existing environment) on the Pi

```
conda env remove -n myenv
conda env create -f environment.yml
```
