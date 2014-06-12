%include common.inc

Name: sync-admin
Summary: XenClient Synchronizer XT administration tool
Source0: sync-cli.tar.gz
Source1: sync-database.tar.gz
BuildArch: noarch
Requires: sync-database = %{version}

%define desc Command-line administration tool for XenClient Synchronizer XT.

%include description.inc
%include python.inc
