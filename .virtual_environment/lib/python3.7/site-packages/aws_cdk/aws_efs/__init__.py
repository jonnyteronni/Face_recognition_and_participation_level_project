"""
## Amazon Elastic File System Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This construct library allows you to set up AWS Elastic File System (EFS).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_efs as efs

my_vpc = ec2.Vpc(self, "VPC")
file_system = efs.FileSystem(self, "MyEfsFileSystem",
    vpc=my_vpc,
    encrypted=True,
    lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
    performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
    throughput_mode=efs.ThroughputMode.BURSTING
)
```

A file system can set `RemovalPolicy`. Default policy is `RETAIN`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
file_system = FileSystem(self, "EfsFileSystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)
```

### Access Point

An access point is an application-specific view into an EFS file system that applies an operating system user and
group, and a file system path, to any file system request made through the access point. The operating system user
and group override any identity information provided by the NFS client. The file system path is exposed as the
access point's root directory. Applications using the access point can only access data in its own directory and
below. To learn more, see [Mounting a File System Using EFS Access Points](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html).

Use `addAccessPoint` to create an access point from a fileSystem:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
file_system.add_access_point("AccessPoint")
```

By default, when you create an access point, the root(`/`) directory is exposed to the client connecting to
the access point. You may specify custom path with the `path` property. If `path` does not exist, it will be
created with the settings defined in the `creationInfo`. See
[Creating Access Points](https://docs.aws.amazon.com/efs/latest/ug/create-access-point.html) for more details.

### Connecting

To control who can access the EFS, use the `.connections` attribute. EFS has
a fixed default port, so you don't need to specify the port:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
file_system.connections.allow_default_port_from(instance)
```

### Mounting the file system using User Data

In order to automatically mount this file system during instance launch,
following code can be used as reference:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(self, "VPC")

file_system = efs.FileSystem(self, "MyEfsFileSystem",
    vpc=vpc,
    encrypted=True,
    lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
    performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
    throughput_mode=efs.ThroughputMode.BURSTING
)

inst = Instance(self, "inst",
    instance_type=InstanceType.of(InstanceClass.T2, InstanceSize.LARGE),
    machine_image=AmazonLinuxImage(
        generation=AmazonLinuxGeneration.AMAZON_LINUX_2
    ),
    vpc=vpc,
    vpc_subnets={
        "subnet_type": SubnetType.PUBLIC
    }
)

file_system.connections.allow_default_port_from(inst)

inst.user_data.add_commands("yum check-update -y", "yum upgrade -y", "yum install -y amazon-efs-utils", "yum install -y nfs-utils", "file_system_id_1=" + file_system.file_system_id, "efs_mount_point_1=/mnt/efs/fs1", "mkdir -p \"${efs_mount_point_1}\"", "test -f \"/sbin/mount.efs\" && echo \"${file_system_id_1}:/ ${efs_mount_point_1} efs defaults,_netdev\" >> /etc/fstab || " + "echo \"${file_system_id_1}.efs." + cdk.Stack.of(self).region + ".amazonaws.com:/ ${efs_mount_point_1} nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0\" >> /etc/fstab", "mount -a -t efs,nfs4 defaults")
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_kms
import aws_cdk.core


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.AccessPointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
    },
)
class AccessPointOptions:
    def __init__(
        self,
        *,
        create_acl: typing.Optional["Acl"] = None,
        path: typing.Optional[str] = None,
        posix_user: typing.Optional["PosixUser"] = None,
    ) -> None:
        """Options to create an AccessPoint.

        :param create_acl: Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        stability
        :stability: experimental
        """
        if isinstance(create_acl, dict):
            create_acl = Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = PosixUser(**posix_user)
        self._values = {}
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional["Acl"]:
        """Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        default
        :default: - None. The directory specified by ``path`` must exist.

        stability
        :stability: experimental
        """
        return self._values.get("create_acl")

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def posix_user(self) -> typing.Optional["PosixUser"]:
        """The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        default
        :default: - user identity not enforced

        see
        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        stability
        :stability: experimental
        """
        return self._values.get("posix_user")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.AccessPointProps",
    jsii_struct_bases=[AccessPointOptions],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
        "file_system": "fileSystem",
    },
)
class AccessPointProps(AccessPointOptions):
    def __init__(
        self,
        *,
        create_acl: typing.Optional["Acl"] = None,
        path: typing.Optional[str] = None,
        posix_user: typing.Optional["PosixUser"] = None,
        file_system: "IFileSystem",
    ) -> None:
        """Properties for the AccessPoint.

        :param create_acl: Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced
        :param file_system: The efs filesystem.

        stability
        :stability: experimental
        """
        if isinstance(create_acl, dict):
            create_acl = Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = PosixUser(**posix_user)
        self._values = {
            "file_system": file_system,
        }
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional["Acl"]:
        """Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        default
        :default: - None. The directory specified by ``path`` must exist.

        stability
        :stability: experimental
        """
        return self._values.get("create_acl")

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def posix_user(self) -> typing.Optional["PosixUser"]:
        """The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        default
        :default: - user identity not enforced

        see
        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        stability
        :stability: experimental
        """
        return self._values.get("posix_user")

    @builtins.property
    def file_system(self) -> "IFileSystem":
        """The efs filesystem.

        stability
        :stability: experimental
        """
        return self._values.get("file_system")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.Acl",
    jsii_struct_bases=[],
    name_mapping={
        "owner_gid": "ownerGid",
        "owner_uid": "ownerUid",
        "permissions": "permissions",
    },
)
class Acl:
    def __init__(self, *, owner_gid: str, owner_uid: str, permissions: str) -> None:
        """Permissions as POSIX ACL.

        :param owner_gid: Specifies the POSIX group ID to apply to the RootDirectory. Accepts values from 0 to 2^32 (4294967295).
        :param owner_uid: Specifies the POSIX user ID to apply to the RootDirectory. Accepts values from 0 to 2^32 (4294967295).
        :param permissions: Specifies the POSIX permissions to apply to the RootDirectory, in the format of an octal number representing the file's mode bits.

        stability
        :stability: experimental
        """
        self._values = {
            "owner_gid": owner_gid,
            "owner_uid": owner_uid,
            "permissions": permissions,
        }

    @builtins.property
    def owner_gid(self) -> str:
        """Specifies the POSIX group ID to apply to the RootDirectory.

        Accepts values from 0 to 2^32 (4294967295).

        stability
        :stability: experimental
        """
        return self._values.get("owner_gid")

    @builtins.property
    def owner_uid(self) -> str:
        """Specifies the POSIX user ID to apply to the RootDirectory.

        Accepts values from 0 to 2^32 (4294967295).

        stability
        :stability: experimental
        """
        return self._values.get("owner_uid")

    @builtins.property
    def permissions(self) -> str:
        """Specifies the POSIX permissions to apply to the RootDirectory, in the format of an octal number representing the file's mode bits.

        stability
        :stability: experimental
        """
        return self._values.get("permissions")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Acl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccessPoint(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-efs.CfnAccessPoint",
):
    """A CloudFormation ``AWS::EFS::AccessPoint``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html
    cloudformationResource:
    :cloudformationResource:: AWS::EFS::AccessPoint
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        file_system_id: str,
        access_point_tags: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "AccessPointTagProperty"]]]] = None,
        client_token: typing.Optional[str] = None,
        posix_user: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "PosixUserProperty"]] = None,
        root_directory: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RootDirectoryProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::EFS::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: ``AWS::EFS::AccessPoint.FileSystemId``.
        :param access_point_tags: ``AWS::EFS::AccessPoint.AccessPointTags``.
        :param client_token: ``AWS::EFS::AccessPoint.ClientToken``.
        :param posix_user: ``AWS::EFS::AccessPoint.PosixUser``.
        :param root_directory: ``AWS::EFS::AccessPoint.RootDirectory``.
        """
        props = CfnAccessPointProps(
            file_system_id=file_system_id,
            access_point_tags=access_point_tags,
            client_token=client_token,
            posix_user=posix_user,
            root_directory=root_directory,
        )

        jsii.create(CfnAccessPoint, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrAccessPointId")
    def attr_access_point_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: AccessPointId
        """
        return jsii.get(self, "attrAccessPointId")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """``AWS::EFS::AccessPoint.FileSystemId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-filesystemid
        """
        return jsii.get(self, "fileSystemId")

    @file_system_id.setter
    def file_system_id(self, value: str) -> None:
        jsii.set(self, "fileSystemId", value)

    @builtins.property
    @jsii.member(jsii_name="accessPointTags")
    def access_point_tags(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "AccessPointTagProperty"]]]]:
        """``AWS::EFS::AccessPoint.AccessPointTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-accesspointtags
        """
        return jsii.get(self, "accessPointTags")

    @access_point_tags.setter
    def access_point_tags(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "AccessPointTagProperty"]]]],
    ) -> None:
        jsii.set(self, "accessPointTags", value)

    @builtins.property
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[str]:
        """``AWS::EFS::AccessPoint.ClientToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-clienttoken
        """
        return jsii.get(self, "clientToken")

    @client_token.setter
    def client_token(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clientToken", value)

    @builtins.property
    @jsii.member(jsii_name="posixUser")
    def posix_user(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "PosixUserProperty"]]:
        """``AWS::EFS::AccessPoint.PosixUser``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-posixuser
        """
        return jsii.get(self, "posixUser")

    @posix_user.setter
    def posix_user(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "PosixUserProperty"]],
    ) -> None:
        jsii.set(self, "posixUser", value)

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RootDirectoryProperty"]]:
        """``AWS::EFS::AccessPoint.RootDirectory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-rootdirectory
        """
        return jsii.get(self, "rootDirectory")

    @root_directory.setter
    def root_directory(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RootDirectoryProperty"]],
    ) -> None:
        jsii.set(self, "rootDirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnAccessPoint.AccessPointTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AccessPointTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
        ) -> None:
            """
            :param key: ``CfnAccessPoint.AccessPointTagProperty.Key``.
            :param value: ``CfnAccessPoint.AccessPointTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html
            """
            self._values = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnAccessPoint.AccessPointTagProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html#cfn-efs-accesspoint-accesspointtag-key
            """
            return self._values.get("key")

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnAccessPoint.AccessPointTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-accesspointtag.html#cfn-efs-accesspoint-accesspointtag-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPointTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnAccessPoint.CreationInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "owner_gid": "ownerGid",
            "owner_uid": "ownerUid",
            "permissions": "permissions",
        },
    )
    class CreationInfoProperty:
        def __init__(self, *, owner_gid: str, owner_uid: str, permissions: str) -> None:
            """
            :param owner_gid: ``CfnAccessPoint.CreationInfoProperty.OwnerGid``.
            :param owner_uid: ``CfnAccessPoint.CreationInfoProperty.OwnerUid``.
            :param permissions: ``CfnAccessPoint.CreationInfoProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html
            """
            self._values = {
                "owner_gid": owner_gid,
                "owner_uid": owner_uid,
                "permissions": permissions,
            }

        @builtins.property
        def owner_gid(self) -> str:
            """``CfnAccessPoint.CreationInfoProperty.OwnerGid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-ownergid
            """
            return self._values.get("owner_gid")

        @builtins.property
        def owner_uid(self) -> str:
            """``CfnAccessPoint.CreationInfoProperty.OwnerUid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-owneruid
            """
            return self._values.get("owner_uid")

        @builtins.property
        def permissions(self) -> str:
            """``CfnAccessPoint.CreationInfoProperty.Permissions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-creationinfo.html#cfn-efs-accesspoint-creationinfo-permissions
            """
            return self._values.get("permissions")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreationInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnAccessPoint.PosixUserProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
    )
    class PosixUserProperty:
        def __init__(
            self,
            *,
            gid: str,
            uid: str,
            secondary_gids: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param gid: ``CfnAccessPoint.PosixUserProperty.Gid``.
            :param uid: ``CfnAccessPoint.PosixUserProperty.Uid``.
            :param secondary_gids: ``CfnAccessPoint.PosixUserProperty.SecondaryGids``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html
            """
            self._values = {
                "gid": gid,
                "uid": uid,
            }
            if secondary_gids is not None:
                self._values["secondary_gids"] = secondary_gids

        @builtins.property
        def gid(self) -> str:
            """``CfnAccessPoint.PosixUserProperty.Gid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-gid
            """
            return self._values.get("gid")

        @builtins.property
        def uid(self) -> str:
            """``CfnAccessPoint.PosixUserProperty.Uid``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-uid
            """
            return self._values.get("uid")

        @builtins.property
        def secondary_gids(self) -> typing.Optional[typing.List[str]]:
            """``CfnAccessPoint.PosixUserProperty.SecondaryGids``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-posixuser.html#cfn-efs-accesspoint-posixuser-secondarygids
            """
            return self._values.get("secondary_gids")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PosixUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnAccessPoint.RootDirectoryProperty",
        jsii_struct_bases=[],
        name_mapping={"creation_info": "creationInfo", "path": "path"},
    )
    class RootDirectoryProperty:
        def __init__(
            self,
            *,
            creation_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.CreationInfoProperty"]] = None,
            path: typing.Optional[str] = None,
        ) -> None:
            """
            :param creation_info: ``CfnAccessPoint.RootDirectoryProperty.CreationInfo``.
            :param path: ``CfnAccessPoint.RootDirectoryProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html
            """
            self._values = {}
            if creation_info is not None:
                self._values["creation_info"] = creation_info
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def creation_info(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.CreationInfoProperty"]]:
            """``CfnAccessPoint.RootDirectoryProperty.CreationInfo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html#cfn-efs-accesspoint-rootdirectory-creationinfo
            """
            return self._values.get("creation_info")

        @builtins.property
        def path(self) -> typing.Optional[str]:
            """``CfnAccessPoint.RootDirectoryProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-accesspoint-rootdirectory.html#cfn-efs-accesspoint-rootdirectory-path
            """
            return self._values.get("path")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RootDirectoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.CfnAccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "access_point_tags": "accessPointTags",
        "client_token": "clientToken",
        "posix_user": "posixUser",
        "root_directory": "rootDirectory",
    },
)
class CfnAccessPointProps:
    def __init__(
        self,
        *,
        file_system_id: str,
        access_point_tags: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.AccessPointTagProperty"]]]] = None,
        client_token: typing.Optional[str] = None,
        posix_user: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.PosixUserProperty"]] = None,
        root_directory: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.RootDirectoryProperty"]] = None,
    ) -> None:
        """Properties for defining a ``AWS::EFS::AccessPoint``.

        :param file_system_id: ``AWS::EFS::AccessPoint.FileSystemId``.
        :param access_point_tags: ``AWS::EFS::AccessPoint.AccessPointTags``.
        :param client_token: ``AWS::EFS::AccessPoint.ClientToken``.
        :param posix_user: ``AWS::EFS::AccessPoint.PosixUser``.
        :param root_directory: ``AWS::EFS::AccessPoint.RootDirectory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html
        """
        self._values = {
            "file_system_id": file_system_id,
        }
        if access_point_tags is not None:
            self._values["access_point_tags"] = access_point_tags
        if client_token is not None:
            self._values["client_token"] = client_token
        if posix_user is not None:
            self._values["posix_user"] = posix_user
        if root_directory is not None:
            self._values["root_directory"] = root_directory

    @builtins.property
    def file_system_id(self) -> str:
        """``AWS::EFS::AccessPoint.FileSystemId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-filesystemid
        """
        return self._values.get("file_system_id")

    @builtins.property
    def access_point_tags(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.AccessPointTagProperty"]]]]:
        """``AWS::EFS::AccessPoint.AccessPointTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-accesspointtags
        """
        return self._values.get("access_point_tags")

    @builtins.property
    def client_token(self) -> typing.Optional[str]:
        """``AWS::EFS::AccessPoint.ClientToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-clienttoken
        """
        return self._values.get("client_token")

    @builtins.property
    def posix_user(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.PosixUserProperty"]]:
        """``AWS::EFS::AccessPoint.PosixUser``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-posixuser
        """
        return self._values.get("posix_user")

    @builtins.property
    def root_directory(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAccessPoint.RootDirectoryProperty"]]:
        """``AWS::EFS::AccessPoint.RootDirectory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-accesspoint.html#cfn-efs-accesspoint-rootdirectory
        """
        return self._values.get("root_directory")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnFileSystem(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-efs.CfnFileSystem",
):
    """A CloudFormation ``AWS::EFS::FileSystem``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    cloudformationResource:
    :cloudformationResource:: AWS::EFS::FileSystem
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        backup_policy: typing.Optional[typing.Union["BackupPolicyProperty", aws_cdk.core.IResolvable]] = None,
        encrypted: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        file_system_policy: typing.Any = None,
        file_system_tags: typing.Optional[typing.List["ElasticFileSystemTagProperty"]] = None,
        kms_key_id: typing.Optional[str] = None,
        lifecycle_policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecyclePolicyProperty"]]]] = None,
        performance_mode: typing.Optional[str] = None,
        provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::EFS::FileSystem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_policy: ``AWS::EFS::FileSystem.BackupPolicy``.
        :param encrypted: ``AWS::EFS::FileSystem.Encrypted``.
        :param file_system_policy: ``AWS::EFS::FileSystem.FileSystemPolicy``.
        :param file_system_tags: ``AWS::EFS::FileSystem.FileSystemTags``.
        :param kms_key_id: ``AWS::EFS::FileSystem.KmsKeyId``.
        :param lifecycle_policies: ``AWS::EFS::FileSystem.LifecyclePolicies``.
        :param performance_mode: ``AWS::EFS::FileSystem.PerformanceMode``.
        :param provisioned_throughput_in_mibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
        :param throughput_mode: ``AWS::EFS::FileSystem.ThroughputMode``.
        """
        props = CfnFileSystemProps(
            backup_policy=backup_policy,
            encrypted=encrypted,
            file_system_policy=file_system_policy,
            file_system_tags=file_system_tags,
            kms_key_id=kms_key_id,
            lifecycle_policies=lifecycle_policies,
            performance_mode=performance_mode,
            provisioned_throughput_in_mibps=provisioned_throughput_in_mibps,
            throughput_mode=throughput_mode,
        )

        jsii.create(CfnFileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrFileSystemId")
    def attr_file_system_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: FileSystemId
        """
        return jsii.get(self, "attrFileSystemId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::EFS::FileSystem.FileSystemTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="fileSystemPolicy")
    def file_system_policy(self) -> typing.Any:
        """``AWS::EFS::FileSystem.FileSystemPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystempolicy
        """
        return jsii.get(self, "fileSystemPolicy")

    @file_system_policy.setter
    def file_system_policy(self, value: typing.Any) -> None:
        jsii.set(self, "fileSystemPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="backupPolicy")
    def backup_policy(
        self,
    ) -> typing.Optional[typing.Union["BackupPolicyProperty", aws_cdk.core.IResolvable]]:
        """``AWS::EFS::FileSystem.BackupPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-backuppolicy
        """
        return jsii.get(self, "backupPolicy")

    @backup_policy.setter
    def backup_policy(
        self,
        value: typing.Optional[typing.Union["BackupPolicyProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "backupPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::EFS::FileSystem.Encrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        """
        return jsii.get(self, "encrypted")

    @encrypted.setter
    def encrypted(
        self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]
    ) -> None:
        jsii.set(self, "encrypted", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicies")
    def lifecycle_policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecyclePolicyProperty"]]]]:
        """``AWS::EFS::FileSystem.LifecyclePolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-lifecyclepolicies
        """
        return jsii.get(self, "lifecyclePolicies")

    @lifecycle_policies.setter
    def lifecycle_policies(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "LifecyclePolicyProperty"]]]],
    ) -> None:
        jsii.set(self, "lifecyclePolicies", value)

    @builtins.property
    @jsii.member(jsii_name="performanceMode")
    def performance_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.PerformanceMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        """
        return jsii.get(self, "performanceMode")

    @performance_mode.setter
    def performance_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "performanceMode", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughputInMibps")
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        """``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-provisionedthroughputinmibps
        """
        return jsii.get(self, "provisionedThroughputInMibps")

    @provisioned_throughput_in_mibps.setter
    def provisioned_throughput_in_mibps(
        self, value: typing.Optional[jsii.Number]
    ) -> None:
        jsii.set(self, "provisionedThroughputInMibps", value)

    @builtins.property
    @jsii.member(jsii_name="throughputMode")
    def throughput_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.ThroughputMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-throughputmode
        """
        return jsii.get(self, "throughputMode")

    @throughput_mode.setter
    def throughput_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "throughputMode", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnFileSystem.BackupPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class BackupPolicyProperty:
        def __init__(self, *, status: str) -> None:
            """
            :param status: ``CfnFileSystem.BackupPolicyProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-backuppolicy.html
            """
            self._values = {
                "status": status,
            }

        @builtins.property
        def status(self) -> str:
            """``CfnFileSystem.BackupPolicyProperty.Status``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-backuppolicy.html#cfn-efs-filesystem-backuppolicy-status
            """
            return self._values.get("status")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnFileSystem.ElasticFileSystemTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ElasticFileSystemTagProperty:
        def __init__(self, *, key: str, value: str) -> None:
            """
            :param key: ``CfnFileSystem.ElasticFileSystemTagProperty.Key``.
            :param value: ``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html
            """
            self._values = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> str:
            """``CfnFileSystem.ElasticFileSystemTagProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html#cfn-efs-filesystem-elasticfilesystemtag-key
            """
            return self._values.get("key")

        @builtins.property
        def value(self) -> str:
            """``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-elasticfilesystemtag.html#cfn-efs-filesystem-elasticfilesystemtag-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticFileSystemTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-efs.CfnFileSystem.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"transition_to_ia": "transitionToIa"},
    )
    class LifecyclePolicyProperty:
        def __init__(self, *, transition_to_ia: str) -> None:
            """
            :param transition_to_ia: ``CfnFileSystem.LifecyclePolicyProperty.TransitionToIA``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html
            """
            self._values = {
                "transition_to_ia": transition_to_ia,
            }

        @builtins.property
        def transition_to_ia(self) -> str:
            """``CfnFileSystem.LifecyclePolicyProperty.TransitionToIA``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-lifecyclepolicy.html#cfn-efs-filesystem-lifecyclepolicy-transitiontoia
            """
            return self._values.get("transition_to_ia")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.CfnFileSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_policy": "backupPolicy",
        "encrypted": "encrypted",
        "file_system_policy": "fileSystemPolicy",
        "file_system_tags": "fileSystemTags",
        "kms_key_id": "kmsKeyId",
        "lifecycle_policies": "lifecyclePolicies",
        "performance_mode": "performanceMode",
        "provisioned_throughput_in_mibps": "provisionedThroughputInMibps",
        "throughput_mode": "throughputMode",
    },
)
class CfnFileSystemProps:
    def __init__(
        self,
        *,
        backup_policy: typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", aws_cdk.core.IResolvable]] = None,
        encrypted: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]] = None,
        file_system_policy: typing.Any = None,
        file_system_tags: typing.Optional[typing.List["CfnFileSystem.ElasticFileSystemTagProperty"]] = None,
        kms_key_id: typing.Optional[str] = None,
        lifecycle_policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.LifecyclePolicyProperty"]]]] = None,
        performance_mode: typing.Optional[str] = None,
        provisioned_throughput_in_mibps: typing.Optional[jsii.Number] = None,
        throughput_mode: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::EFS::FileSystem``.

        :param backup_policy: ``AWS::EFS::FileSystem.BackupPolicy``.
        :param encrypted: ``AWS::EFS::FileSystem.Encrypted``.
        :param file_system_policy: ``AWS::EFS::FileSystem.FileSystemPolicy``.
        :param file_system_tags: ``AWS::EFS::FileSystem.FileSystemTags``.
        :param kms_key_id: ``AWS::EFS::FileSystem.KmsKeyId``.
        :param lifecycle_policies: ``AWS::EFS::FileSystem.LifecyclePolicies``.
        :param performance_mode: ``AWS::EFS::FileSystem.PerformanceMode``.
        :param provisioned_throughput_in_mibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
        :param throughput_mode: ``AWS::EFS::FileSystem.ThroughputMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
        """
        self._values = {}
        if backup_policy is not None:
            self._values["backup_policy"] = backup_policy
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_policy is not None:
            self._values["file_system_policy"] = file_system_policy
        if file_system_tags is not None:
            self._values["file_system_tags"] = file_system_tags
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if lifecycle_policies is not None:
            self._values["lifecycle_policies"] = lifecycle_policies
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_in_mibps is not None:
            self._values["provisioned_throughput_in_mibps"] = provisioned_throughput_in_mibps
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode

    @builtins.property
    def backup_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnFileSystem.BackupPolicyProperty", aws_cdk.core.IResolvable]]:
        """``AWS::EFS::FileSystem.BackupPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-backuppolicy
        """
        return self._values.get("backup_policy")

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::EFS::FileSystem.Encrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
        """
        return self._values.get("encrypted")

    @builtins.property
    def file_system_policy(self) -> typing.Any:
        """``AWS::EFS::FileSystem.FileSystemPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystempolicy
        """
        return self._values.get("file_system_policy")

    @builtins.property
    def file_system_tags(
        self,
    ) -> typing.Optional[typing.List["CfnFileSystem.ElasticFileSystemTagProperty"]]:
        """``AWS::EFS::FileSystem.FileSystemTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
        """
        return self._values.get("file_system_tags")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def lifecycle_policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFileSystem.LifecyclePolicyProperty"]]]]:
        """``AWS::EFS::FileSystem.LifecyclePolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-lifecyclepolicies
        """
        return self._values.get("lifecycle_policies")

    @builtins.property
    def performance_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.PerformanceMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
        """
        return self._values.get("performance_mode")

    @builtins.property
    def provisioned_throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        """``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-provisionedthroughputinmibps
        """
        return self._values.get("provisioned_throughput_in_mibps")

    @builtins.property
    def throughput_mode(self) -> typing.Optional[str]:
        """``AWS::EFS::FileSystem.ThroughputMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-throughputmode
        """
        return self._values.get("throughput_mode")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMountTarget(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-efs.CfnMountTarget",
):
    """A CloudFormation ``AWS::EFS::MountTarget``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
    cloudformationResource:
    :cloudformationResource:: AWS::EFS::MountTarget
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        file_system_id: str,
        security_groups: typing.List[str],
        subnet_id: str,
        ip_address: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::EFS::MountTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param file_system_id: ``AWS::EFS::MountTarget.FileSystemId``.
        :param security_groups: ``AWS::EFS::MountTarget.SecurityGroups``.
        :param subnet_id: ``AWS::EFS::MountTarget.SubnetId``.
        :param ip_address: ``AWS::EFS::MountTarget.IpAddress``.
        """
        props = CfnMountTargetProps(
            file_system_id=file_system_id,
            security_groups=security_groups,
            subnet_id=subnet_id,
            ip_address=ip_address,
        )

        jsii.create(CfnMountTarget, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrIpAddress")
    def attr_ip_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: IpAddress
        """
        return jsii.get(self, "attrIpAddress")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """``AWS::EFS::MountTarget.FileSystemId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        """
        return jsii.get(self, "fileSystemId")

    @file_system_id.setter
    def file_system_id(self, value: str) -> None:
        jsii.set(self, "fileSystemId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[str]:
        """``AWS::EFS::MountTarget.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter
    def security_groups(self, value: typing.List[str]) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        """``AWS::EFS::MountTarget.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter
    def subnet_id(self, value: str) -> None:
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> typing.Optional[str]:
        """``AWS::EFS::MountTarget.IpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        """
        return jsii.get(self, "ipAddress")

    @ip_address.setter
    def ip_address(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ipAddress", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.CfnMountTargetProps",
    jsii_struct_bases=[],
    name_mapping={
        "file_system_id": "fileSystemId",
        "security_groups": "securityGroups",
        "subnet_id": "subnetId",
        "ip_address": "ipAddress",
    },
)
class CfnMountTargetProps:
    def __init__(
        self,
        *,
        file_system_id: str,
        security_groups: typing.List[str],
        subnet_id: str,
        ip_address: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::EFS::MountTarget``.

        :param file_system_id: ``AWS::EFS::MountTarget.FileSystemId``.
        :param security_groups: ``AWS::EFS::MountTarget.SecurityGroups``.
        :param subnet_id: ``AWS::EFS::MountTarget.SubnetId``.
        :param ip_address: ``AWS::EFS::MountTarget.IpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
        """
        self._values = {
            "file_system_id": file_system_id,
            "security_groups": security_groups,
            "subnet_id": subnet_id,
        }
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def file_system_id(self) -> str:
        """``AWS::EFS::MountTarget.FileSystemId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
        """
        return self._values.get("file_system_id")

    @builtins.property
    def security_groups(self) -> typing.List[str]:
        """``AWS::EFS::MountTarget.SecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
        """
        return self._values.get("security_groups")

    @builtins.property
    def subnet_id(self) -> str:
        """``AWS::EFS::MountTarget.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
        """
        return self._values.get("subnet_id")

    @builtins.property
    def ip_address(self) -> typing.Optional[str]:
        """``AWS::EFS::MountTarget.IpAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
        """
        return self._values.get("ip_address")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMountTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.FileSystemAttributes",
    jsii_struct_bases=[],
    name_mapping={"file_system_id": "fileSystemId", "security_group": "securityGroup"},
)
class FileSystemAttributes:
    def __init__(
        self, *, file_system_id: str, security_group: aws_cdk.aws_ec2.ISecurityGroup
    ) -> None:
        """Properties that describe an existing EFS file system.

        :param file_system_id: The File System's ID.
        :param security_group: The security group of the file system.

        stability
        :stability: experimental
        """
        self._values = {
            "file_system_id": file_system_id,
            "security_group": security_group,
        }

    @builtins.property
    def file_system_id(self) -> str:
        """The File System's ID.

        stability
        :stability: experimental
        """
        return self._values.get("file_system_id")

    @builtins.property
    def security_group(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        """The security group of the file system.

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.FileSystemProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "encrypted": "encrypted",
        "file_system_name": "fileSystemName",
        "kms_key": "kmsKey",
        "lifecycle_policy": "lifecyclePolicy",
        "performance_mode": "performanceMode",
        "provisioned_throughput_per_second": "provisionedThroughputPerSecond",
        "removal_policy": "removalPolicy",
        "security_group": "securityGroup",
        "throughput_mode": "throughputMode",
        "vpc_subnets": "vpcSubnets",
    },
)
class FileSystemProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        encrypted: typing.Optional[bool] = None,
        file_system_name: typing.Optional[str] = None,
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        lifecycle_policy: typing.Optional["LifecyclePolicy"] = None,
        performance_mode: typing.Optional["PerformanceMode"] = None,
        provisioned_throughput_per_second: typing.Optional[aws_cdk.core.Size] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        throughput_mode: typing.Optional["ThroughputMode"] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties of EFS FileSystem.

        :param vpc: VPC to launch the file system in.
        :param encrypted: Defines if the data at rest in the file system is encrypted or not. Default: - false
        :param file_system_name: The filesystem's name. Default: - CDK generated name
        :param kms_key: The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if
        :param lifecycle_policy: A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - none
        :param performance_mode: Enum to mention the performance mode of the file system. Default: - GENERAL_PURPOSE
        :param provisioned_throughput_per_second: Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allow all out bound traffic
        :param throughput_mode: Enum to mention the throughput mode of the file system. Default: - BURSTING
        :param vpc_subnets: Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            "vpc": vpc,
        }
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_name is not None:
            self._values["file_system_name"] = file_system_name
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_per_second is not None:
            self._values["provisioned_throughput_per_second"] = provisioned_throughput_per_second
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_group is not None:
            self._values["security_group"] = security_group
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch the file system in.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def encrypted(self) -> typing.Optional[bool]:
        """Defines if the data at rest in the file system is encrypted or not.

        default
        :default: - false

        stability
        :stability: experimental
        """
        return self._values.get("encrypted")

    @builtins.property
    def file_system_name(self) -> typing.Optional[str]:
        """The filesystem's name.

        default
        :default: - CDK generated name

        stability
        :stability: experimental
        """
        return self._values.get("file_system_name")

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key used for encryption.

        This is required to encrypt the data at rest if @encrypted is set to true.

        default
        :default: - if

        stability
        :stability: experimental
        encrypted:
        :encrypted:: is true, the default key for EFS (/aws/elasticfilesystem) is used
        """
        return self._values.get("kms_key")

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional["LifecyclePolicy"]:
        """A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("lifecycle_policy")

    @builtins.property
    def performance_mode(self) -> typing.Optional["PerformanceMode"]:
        """Enum to mention the performance mode of the file system.

        default
        :default: - GENERAL_PURPOSE

        stability
        :stability: experimental
        """
        return self._values.get("performance_mode")

    @builtins.property
    def provisioned_throughput_per_second(self) -> typing.Optional[aws_cdk.core.Size]:
        """Provisioned throughput for the file system.

        This is a required property if the throughput mode is set to PROVISIONED.
        Must be at least 1MiB/s.

        default
        :default: - none, errors out

        stability
        :stability: experimental
        """
        return self._values.get("provisioned_throughput_per_second")

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """The removal policy to apply to the file system.

        default
        :default: RemovalPolicy.RETAIN

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to assign to this file system.

        default
        :default: - creates new security group which allow all out bound traffic

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def throughput_mode(self) -> typing.Optional["ThroughputMode"]:
        """Enum to mention the throughput mode of the file system.

        default
        :default: - BURSTING

        stability
        :stability: experimental
        """
        return self._values.get("throughput_mode")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Which subnets to place the mount target in the VPC.

        default
        :default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-efs.IAccessPoint")
class IAccessPoint(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents an EFS AccessPoint.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAccessPointProxy

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> str:
        """The ARN of the AccessPoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> str:
        """The ID of the AccessPoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IAccessPointProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents an EFS AccessPoint.

    stability
    :stability: experimental
    """

    __jsii_type__ = "@aws-cdk/aws-efs.IAccessPoint"

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> str:
        """The ARN of the AccessPoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "accessPointArn")

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> str:
        """The ID of the AccessPoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "accessPointId")


@jsii.interface(jsii_type="@aws-cdk/aws-efs.IFileSystem")
class IFileSystem(
    aws_cdk.aws_ec2.IConnectable, aws_cdk.core.IResource, jsii.compat.Protocol
):
    """Interface to implement AWS File Systems.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFileSystemProxy

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon EFS.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> aws_cdk.core.IDependable:
        """Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        stability
        :stability: experimental
        """
        ...


class _IFileSystemProxy(
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable),
    jsii.proxy_for(aws_cdk.core.IResource),
):
    """Interface to implement AWS File Systems.

    stability
    :stability: experimental
    """

    __jsii_type__ = "@aws-cdk/aws-efs.IFileSystem"

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon EFS.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fileSystemId")

    @builtins.property
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> aws_cdk.core.IDependable:
        """Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mountTargetsAvailable")


@jsii.enum(jsii_type="@aws-cdk/aws-efs.LifecyclePolicy")
class LifecyclePolicy(enum.Enum):
    """EFS Lifecycle Policy, if a file is not accessed for given days, it will move to EFS Infrequent Access.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-lifecyclepolicies
    stability
    :stability: experimental
    """

    AFTER_7_DAYS = "AFTER_7_DAYS"
    """After 7 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_14_DAYS = "AFTER_14_DAYS"
    """After 14 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_30_DAYS = "AFTER_30_DAYS"
    """After 30 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_60_DAYS = "AFTER_60_DAYS"
    """After 60 days of not being accessed.

    stability
    :stability: experimental
    """
    AFTER_90_DAYS = "AFTER_90_DAYS"
    """After 90 days of not being accessed.

    stability
    :stability: experimental
    """


@jsii.enum(jsii_type="@aws-cdk/aws-efs.PerformanceMode")
class PerformanceMode(enum.Enum):
    """EFS Performance mode.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
    stability
    :stability: experimental
    """

    GENERAL_PURPOSE = "GENERAL_PURPOSE"
    """This is the general purpose performance mode for most file systems.

    stability
    :stability: experimental
    """
    MAX_IO = "MAX_IO"
    """This performance mode can scale to higher levels of aggregate throughput and operations per second with a tradeoff of slightly higher latencies.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-efs.PosixUser",
    jsii_struct_bases=[],
    name_mapping={"gid": "gid", "uid": "uid", "secondary_gids": "secondaryGids"},
)
class PosixUser:
    def __init__(
        self,
        *,
        gid: str,
        uid: str,
        secondary_gids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Represents the PosixUser.

        :param gid: The POSIX group ID used for all file system operations using this access point.
        :param uid: The POSIX user ID used for all file system operations using this access point.
        :param secondary_gids: Secondary POSIX group IDs used for all file system operations using this access point. Default: - None

        stability
        :stability: experimental
        """
        self._values = {
            "gid": gid,
            "uid": uid,
        }
        if secondary_gids is not None:
            self._values["secondary_gids"] = secondary_gids

    @builtins.property
    def gid(self) -> str:
        """The POSIX group ID used for all file system operations using this access point.

        stability
        :stability: experimental
        """
        return self._values.get("gid")

    @builtins.property
    def uid(self) -> str:
        """The POSIX user ID used for all file system operations using this access point.

        stability
        :stability: experimental
        """
        return self._values.get("uid")

    @builtins.property
    def secondary_gids(self) -> typing.Optional[typing.List[str]]:
        """Secondary POSIX group IDs used for all file system operations using this access point.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get("secondary_gids")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PosixUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-efs.ThroughputMode")
class ThroughputMode(enum.Enum):
    """EFS Throughput mode.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-throughputmode
    stability
    :stability: experimental
    """

    BURSTING = "BURSTING"
    """This mode on Amazon EFS scales as the size of the file system in the standard storage class grows.

    stability
    :stability: experimental
    """
    PROVISIONED = "PROVISIONED"
    """This mode can instantly provision the throughput of the file system (in MiB/s) independent of the amount of data stored.

    stability
    :stability: experimental
    """


@jsii.implements(IAccessPoint)
class AccessPoint(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-efs.AccessPoint",
):
    """Represents the AccessPoint.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        file_system: "IFileSystem",
        create_acl: typing.Optional["Acl"] = None,
        path: typing.Optional[str] = None,
        posix_user: typing.Optional["PosixUser"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param file_system: The efs filesystem.
        :param create_acl: Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        stability
        :stability: experimental
        """
        props = AccessPointProps(
            file_system=file_system,
            create_acl=create_acl,
            path=path,
            posix_user=posix_user,
        )

        jsii.create(AccessPoint, self, [scope, id, props])

    @jsii.member(jsii_name="fromAccessPointId")
    @builtins.classmethod
    def from_access_point_id(
        cls, scope: aws_cdk.core.Construct, id: str, access_point_id: str
    ) -> "IAccessPoint":
        """Import an existing Access Point.

        :param scope: -
        :param id: -
        :param access_point_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromAccessPointId", [scope, id, access_point_id])

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> str:
        """The ARN of the Access Point.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "accessPointArn")

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> str:
        """The ID of the Access Point.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "accessPointId")

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> "IFileSystem":
        """The filesystem of the access point.

        stability
        :stability: experimental
        """
        return jsii.get(self, "fileSystem")


@jsii.implements(IFileSystem)
class FileSystem(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-efs.FileSystem",
):
    """The Elastic File System implementation of IFileSystem.

    It creates a new, empty file system in Amazon Elastic File System (Amazon EFS).
    It also creates mount target (AWS::EFS::MountTarget) implicitly to mount the
    EFS file system on an Amazon Elastic Compute Cloud (Amazon EC2) instance or another resource.

    see
    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    stability
    :stability: experimental
    resource:
    :resource:: AWS::EFS::FileSystem
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        encrypted: typing.Optional[bool] = None,
        file_system_name: typing.Optional[str] = None,
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        lifecycle_policy: typing.Optional["LifecyclePolicy"] = None,
        performance_mode: typing.Optional["PerformanceMode"] = None,
        provisioned_throughput_per_second: typing.Optional[aws_cdk.core.Size] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        throughput_mode: typing.Optional["ThroughputMode"] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Constructor for creating a new EFS FileSystem.

        :param scope: -
        :param id: -
        :param vpc: VPC to launch the file system in.
        :param encrypted: Defines if the data at rest in the file system is encrypted or not. Default: - false
        :param file_system_name: The filesystem's name. Default: - CDK generated name
        :param kms_key: The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if
        :param lifecycle_policy: A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - none
        :param performance_mode: Enum to mention the performance mode of the file system. Default: - GENERAL_PURPOSE
        :param provisioned_throughput_per_second: Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allow all out bound traffic
        :param throughput_mode: Enum to mention the throughput mode of the file system. Default: - BURSTING
        :param vpc_subnets: Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        props = FileSystemProps(
            vpc=vpc,
            encrypted=encrypted,
            file_system_name=file_system_name,
            kms_key=kms_key,
            lifecycle_policy=lifecycle_policy,
            performance_mode=performance_mode,
            provisioned_throughput_per_second=provisioned_throughput_per_second,
            removal_policy=removal_policy,
            security_group=security_group,
            throughput_mode=throughput_mode,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(FileSystem, self, [scope, id, props])

    @jsii.member(jsii_name="fromFileSystemAttributes")
    @builtins.classmethod
    def from_file_system_attributes(
        cls,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        file_system_id: str,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> "IFileSystem":
        """Import an existing File System from the given properties.

        :param scope: -
        :param id: -
        :param file_system_id: The File System's ID.
        :param security_group: The security group of the file system.

        stability
        :stability: experimental
        """
        attrs = FileSystemAttributes(
            file_system_id=file_system_id, security_group=security_group
        )

        return jsii.sinvoke(cls, "fromFileSystemAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAccessPoint")
    def add_access_point(
        self,
        id: str,
        *,
        create_acl: typing.Optional["Acl"] = None,
        path: typing.Optional[str] = None,
        posix_user: typing.Optional["PosixUser"] = None,
    ) -> "AccessPoint":
        """create access point from this filesystem.

        :param id: -
        :param create_acl: Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced

        stability
        :stability: experimental
        """
        access_point_options = AccessPointOptions(
            create_acl=create_acl, path=path, posix_user=posix_user
        )

        return jsii.invoke(self, "addAccessPoint", [id, access_point_options])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups/rules used to allow network connections to the file system.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        """The ID of the file system, assigned by Amazon EFS.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fileSystemId")

    @builtins.property
    @jsii.member(jsii_name="mountTargetsAvailable")
    def mount_targets_available(self) -> aws_cdk.core.IDependable:
        """Dependable that can be depended upon to ensure the mount targets of the filesystem are ready.

        stability
        :stability: experimental
        """
        return jsii.get(self, "mountTargetsAvailable")


__all__ = [
    "AccessPoint",
    "AccessPointOptions",
    "AccessPointProps",
    "Acl",
    "CfnAccessPoint",
    "CfnAccessPointProps",
    "CfnFileSystem",
    "CfnFileSystemProps",
    "CfnMountTarget",
    "CfnMountTargetProps",
    "FileSystem",
    "FileSystemAttributes",
    "FileSystemProps",
    "IAccessPoint",
    "IFileSystem",
    "LifecyclePolicy",
    "PerformanceMode",
    "PosixUser",
    "ThroughputMode",
]

publication.publish()
