#!/usr/bin/env python

import pysftp

# FTP server connection strings
sftp_host = "ssh.phx.nearlyfreespeech.net"
sftp_username = "me_avvocatodoraballabio"
sftp_key = "~/.ssh/nfs_melissa_rsa"
sftp_key_pw = ''

# Local paths
local_dir = "www"

# remote server paths
production_dir = "/home/public"

if __name__ == '__main__':

    print("Connecting to SFTP host " + sftp_host)

    with pysftp.Connection(sftp_host, username=sftp_username,
                           private_key=sftp_key, private_key_pass=sftp_key_pw) as sftp_conn:
        print("Starting directory transfer of " + local_dir)
        sftp_conn.put_r(local_dir, production_dir)

    print("Transfer complete")
