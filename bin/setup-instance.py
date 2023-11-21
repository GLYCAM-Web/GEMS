#!/usr/bin/env python3
"""A Python script to configure a GEMS instance and it's instance_config.json.

# To force a delegator rebake:
$  $GEMSHOME/bin/setup-instance.py --rebake-delegator

"""
import shutil, argparse, os, sys, json, datetime

GemsPath = os.environ.get("GEMSHOME")
sys.path.append(GemsPath)
sys.path.append(
    GemsPath + "/gemsModules"
)  # Swarm needs /gemsModules. These sys path hacks would be simplified if we used pip to install gems.
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow
from gemsModules.systemoperations.instance_config import InstanceConfig


def argparser():
    """
    ```bash
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --add-host "${MD_GRPC_HOSTNAME};[MDaaS-RunMD];${MD_GRPC_HOST}:${MD_GRPC_PORT}"
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --set-sbatch-arguments "${MD_GRPC_HOSTNAME};MDaaS-RunMD;${SBATCH_ARGS}"
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --set-md-cluster-filesystem-path $MD_CLUSTER_FILESYSTEM_PATH
    $ python3 "${GEMSHOME}/bin/setup-instance.py" --gen_md_cluster_host_config
    ```
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--add-host",
        type=str,
        help="Add a host to the instance_config.json. Format: 'hostname,contexts,host:port'",
    )

    parser.add_argument(
        "--set-sbatch-arguments",
        type=str,
        help="Set the sbatch_arguments for a host in the instance_config.json. Format: 'hostname,context,sbatch_arguments'",
    )

    parser.add_argument(
        "--set-local-parameters",
        type=str,
        help="Set the local_parameters for a host in the instance_config.json. Format: 'hostname,context,local_parameters'",
    )

    parser.add_argument(
        "--gen-remote-md-cluster-config",
        type=str,
        help="Generate a partial remote MD cluster config file for the MD cluster host with the given filesystem path.",
    )

    parser.add_argument(
        "--set-md-cluster-filesystem-path",
        type=str,
        help="Sets the md_cluster_filesystem_path for the MD cluster host.",
    )

    return parser


def main():
    """Sets up a GEMS instance for the first time.

    Can be used by a DevEnv or manual GEMS setup.
    """
    ic = InstanceConfig()
    args = argparser().parse_args()

    force_reconfiguration = os.getenv("GEMS_FORCE_INSTANCE_RECONFIGURATION") == "True"
    if force_reconfiguration or not ic.is_configured:
        print("\nAbout to configure this GEMS instance...")
    else:
        print("\nThis GEMS instance is already configured. Exiting.")
        return

    SAVE = False
    if args.set_md_cluster_filesystem_path is not None:
        ic.set_md_filesystem_path(args.set_md_cluster_filesystem_path)
        SAVE = True

    if args.add_host is not None:
        hostname, contexts, hostport = args.add_host.split(";")
        host, port = hostport.split(":")
        contexts = contexts.strip("[]").split(",")
        print(
            f"Adding host: {hostname} with contexts: {contexts} and host: {host}:{port}"
        )
        ic.add_host(hostname, host, port, contexts)
        SAVE = True

    if args.set_sbatch_arguments is not None:
        (
            sbatch_hostname,
            sbatch_context,
            sbatch_arguments,
        ) = args.set_sbatch_arguments.split(";")
        sbatch_arguments = json.loads(sbatch_arguments)
        ic.add_keyed_arguments_to_host(
            "sbatch_arguments", sbatch_hostname, sbatch_context, sbatch_arguments
        )
        SAVE = True

    if args.set_local_parameters is not None:
        (
            local_parameters_hostname,
            local_parameters_context,
            local_parameters,
        ) = args.set_local_parameters.split(";")
        local_parameters = json.loads(local_parameters)
        ic.add_keyed_arguments_to_host(
            "local_parameters",
            local_parameters_hostname,
            local_parameters_context,
            local_parameters,
        )
        SAVE = True

    if SAVE:
        saved = ic.save()
        if saved and args.gen_remote_md_cluster_config is not None:
            if args.add_host is None:
                raise RuntimeError(
                    "Cannot generate a remote MD cluster config without adding a host first, please try again."
                )

            # create the command to run on the MD cluster host
            generating_cmd = (
                f"python3 $GEMSHOME/bin/setup-instance.py \\\n"
                f"--add-host '{hostname};[MDaaS-RunMD];{host}:{port}' \\\n"
                f"--set-sbatch-arguments '{hostname};MDaaS-RunMD;{json.dumps(ic['hosts'][hostname]['sbatch_arguments'])}' \\\n"
                f"--set-local-parameters '{hostname};MDaaS-RunMD;{json.dumps(ic['hosts'][hostname]['local_parameters'])}' \\\n"
                f"--set-md-cluster-filesystem-path {args.gen_remote_md_cluster_config}"
            )

            # print out the newly added host sub-dict because it will be useful for configuring the MD cluster host.
            print(
                "Please use the following command on the MD Cluster host if you have not already synchronized your instances:\n\n"
                f"{generating_cmd}\n\n(Ignore this message if you are in a DevEnv, it has been done for you.)\n"
            )

            # write out a bash script that can be used to generate the remote MD cluster config
            with open(
                os.path.join(GemsPath, "REMOTE_MD_CLUSTER_HOST_SETUP-git-ignore-me.sh"),
                "w",
            ) as f:
                # TODO/Q: write bash header? If we don't it's easier to just copy and paste the command from the file.
                f.write("#!/bin/bash\n\n")
                f.write(f"{generating_cmd}\n")
                print(
                    "Wrote out $GEMSHOME/REMOTE_MD_CLUSTER_HOST_SETUP-git-ignore-me.sh"
                )

    return ic


if __name__ == "__main__":  #
    main()
