python_clients_4_launchpad_api
==============================

Python scripts to create EDH cluster via Launchpad server

While waiting for Launchpad to become available, you can use python clients to create EDH cluster.

You'll need to start Launchpad server and portforward its port 8080 to your localhost.

On your launcher instance:
<pre><code># cd launchpad-server-2.0.0-SNAPSHOT
# ./bin/start
<code></pre>

Then on localhost:

<pre><code>ssh -i /path/to/launchpad/host/keyName.pem -L 8080:[your_launcher_instance_private_IP]:8080 ec2-user@[your_launcher_instance_public_IP].amazonaws.com
<code></pre>

The way I came up with the JSON specs/objects inside the python scripts is run the following command on an existing and valid AWS cluster that I built earlier:

You can easily get the JSON objects from a valid configuration file:

<pre><code># ./bin/launchpad validate <your_aws.conf> --lp.validate.dumpTemplates=true
<code></pre>

Remember to change all the random virtual instance id numbers (eg, those that look like this "6e3609d3-6gdf-5be0-9836-21984e80e3cd") if you're re-running these scripts within 24 hrs.
