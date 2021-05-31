# EDS

The Extensible Deployment System (EDS)

(*UNDER CONSTRUCTION*)

[![Build Status](https://travis-ci.org/manheim/eds.svg?branch=main)](https://travis-ci.org/manheim/eds)

## Overview

* Configure deployments using a single "eds.yml" file.
* Inherit from parent "eds.yml" files to stay DRY.
* Support multiple technologies using plugins.
* Let the EDS Worker do the work for you.

[EDS Slides](./docs/eds_slides.pdf)

## Worker Setup

## Usage

Add an `eds.yml` file to the root of your project. Add a webhook to send commit
events to your EDS Worker.

The format of `eds.yml`:

```yaml
version:
includes:
plugins:
    - id:
      type:
      version:
      parent:
          url:
          plugin_id:
      properties:
```

* `version`: (required) The version of EDS in the form of a pip install
  requirement.
* `include`: (optional) A list of `eds.yml` URLs to include.
* `plugins`: (required) A list of plugin configurations.
    * `id`: (required) An id to refer to this plugin configuraton.
    * `type`: (required) The type of plugin to be used.
    * `version`: (optional) The plugin version in the form of a pip install
      requirement. Not required for built-in plugins.
    * `parent`: (optional) A parent plugin configuration to inherit from.
        * `url`: (optional) The EDS url containing the plugin.  Not required, if
          included in this file.
        * `plugin_id`: (required) The plugin id.
    * `properties`: (optional) A properties dictionary.


## Built-in Plugins


## Plugin Interfaces

* [eds.config](./eds/interfaces/config.py)
* [eds.pipeline](./eds/interfaces/pipeline.py)
* [eds.pipeline_provider](./eds/interfaces/pipeline_provider.py)
* [eds.tags](./eds/interfaces/tags.py)
* [eds.task](./eds/interfaces/task.py)
* [eds.vcs_provider](./eds/interfaces/vcs_provider.py)
* [eds.worker](./eds/interfaces/worker.py)

