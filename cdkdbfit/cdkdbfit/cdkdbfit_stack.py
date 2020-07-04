from aws_cdk import (
    core,
    aws_ecr,
    aws_ecr_assets,
    aws_ecs,
    aws_ec2
)


class cdkdbfitStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create ecr repo
        repository = aws_ecr.Repository(
            self, "dbfit", image_scan_on_push=True, repository_name="dbfit",
        )

        # add image to repo
        dockerImageAsset = aws_ecr_assets.DockerImageAsset(
            self, "dbfitImg", directory="./", repository_name="dbfit", exclude=[
                'node_modules',
                '.git',
                'cdk.out'])
        # create task definition
        task_definition = aws_ecs.TaskDefinition(self, "dbfittask",
                                                 memory_mib="512",
                                                 cpu="256",
                                                 network_mode=aws_ecs.NetworkMode.AWS_VPC,
                                                 compatibility=aws_ecs.Compatibility.EC2_AND_FARGATE
                                                 )
        # get image from ecr repo
        container_image = aws_ecs.ContainerImage.from_docker_image_asset(
            dockerImageAsset)

        # add container to task definition
        container = task_definition.add_container(
            "dbfit-container", image=container_image,
            memory_reservation_mib=512, cpu=256)

        # add port mapping to expose to outside world
        port_mapping = aws_ecs.PortMapping(container_port=8085)
        container.add_port_mappings(port_mapping)

        # get vpc reference
        vpc = aws_ec2.Vpc.from_lookup(self, "VPC",
                                      # This imports the default VPC but you can also
                                      # specify a 'vpcName' or 'tags'.
                                      is_default=True
                                      )
        # create cluster
        # Create an ECS cluster
        cluster = aws_ecs.Cluster(self, "Cluster",
                                  vpc=vpc
                                  )

        # create security group for ecs service
        security_group = aws_ec2.SecurityGroup(self, "dbfitSG", vpc=vpc,
                                               security_group_name="dbfitGroup", allow_all_outbound=True
                                               )
        # open 8085 inbound
        security_group.add_ingress_rule(
            aws_ec2.Peer.ipv4('0.0.0.0/0'), aws_ec2.Port.tcp(8085), 'DBFit Routing')

        # start fargate service on cluster
        fargate_service = aws_ecs.FargateService(
            self, "dbfitservice", cluster=cluster, task_definition=task_definition, assign_public_ip=True, security_groups=[security_group])
