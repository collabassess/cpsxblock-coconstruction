# CPSXBlock: Co-constructed Items
This helper item allows the [CPSXBlock](https://github.com/collabassess/CPSXblock) to create environments that allow "co-constructed items." For example, suppose Alice and Bob are working on a problem set together. One particular question has two parts, and these parts are different for Alice and Bob:

<table>
    <tr>
        <td></td>
        <td>Alice</td>
        <td>Bob</td>
    </tr>
    <tr>
        <td>Part 1</td>
        <td>Find ...</td>
        <td>Suppose that... find...</td>
    </tr>
    <tr>
        <td>Part 2</td>
        <td colspan="2">Using what you previously found, compute...</td>
    </tr>
</table>

This XBlock allows the edX content creator to create interconnected questions in their collaborative sessions.

The structure used to implement this pattern is a little different. In order to determine the cohort of the user (without doing extra database queries), the "Part 2" question is duplicated, one visible only to Alice and the other only visible to Bob:

<table>
    <tr>
        <td></td>
        <td>Alice</td>
        <td>Bob</td>
    </tr>
    <tr>
        <td>Part 1</td>
        <td>Find ...</td>
        <td>Suppose that... find...</td>
    </tr>
    <tr>
        <td>Part 2</td>
        <td>Using what you previously found, compute...</td>
        <td>Using what you previously found, compute...</td>
    </tr>
</table>

This XBlock's nomenclature calls "Part 1" the `provider` questions (`provider_A` and `provider_B` for Alice and Bob, respectively) and "Part 2" the `receiver` questions (similar naming as the `providers`).

# Installation
The `CoConstructCPSXBlock` depends on the [CPSXBlock](https://github.com/collabasess/CPSXblock) which creates the collaborative environments. See the CPSXBlock repository for installation instructions on a new openedx instance. That installation process will include downloading and configuring the [CPSX API](https://github.com/collabassess/cpsx-api) which interfaces between the browser and the openedx MySQL database.

Once all of those are installed, perform these actions:
1. `$ git clone` this repository
2. `$ cd` into the newly downloaded repo
3. `$ npm i` to download the necessary NodeJS requirements
4. `$ ./install.sh` to build and install the project into openedx

Upgrading the XBlock is as simple as running `./upgrade.sh` in the repository directory. This script does nothing more than `git pull`ing this repo and then running `./install.sh`.

# Building
There are a couple steps to building this project. The first is rendering the XBlock's front-end code, and the second is building/running the test environment. The first task is to `git clone` this repository. 

## Building the front-end interface
The `CoConstructCPSXBlock` _has the possibility to use_ (but does not currently use) [React](https://reactjs.org) to render the status indicators and maintain the XBlock's state. As XBlocks [are not yet but will be](https://openedx.atlassian.net/wiki/spaces/FEDX/pages/122454990/React+evaluation+plan) written in React, this block uses [Webpack](https://webpack.js.org) to bundle the app into the `function BlockName(runtime, element) { ... }` pattern that `edx-platform` currently expects.

To build the app,
1. `$ npm i` to install all the requirements
2. `$ npm run build` to build the front-end for the first time
3. If you are working on the interface for some time, I recommend running the `webpack` watcher: `$ npm run watch`


## Running the XBlock
You will need [Docker](https://www.docker.com/get-docker). If you are using a Linux distro, [read here](https://docs.docker.com/compose/install/#install-compose) to learn how to properly install Docker Compose.

After Docker's installation, perform these tasks:
    
 1. `$ cd cpsxblock-coconstruction`
 2. `$ docker-compose build sdk && docker-compose build app` to create the SDK environment image and XBlock app
 3. `$ docker-compose up` starts the XBlock SDK server. 
 
 The XBlock will be live at `localhost:5000`.

