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

# Installation

`TODO`

# Development
You will need [Docker](https://www.docker.com/get-docker). If you are using a Linux distro, [read here](https://docs.docker.com/compose/install/#install-compose) to learn how to properly install Docker Compose.

After installation, perform these tasks:
    
 1. `git clone` this repository
 2. `cd cpsxblock-coconstruction`
 3. `docker-compose build` to create the development image
 4. `docker-compose up` starts the XBlock SDK server. The XBlock will be live at `localhost:5000`

